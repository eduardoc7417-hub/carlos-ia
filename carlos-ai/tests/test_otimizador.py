"""Testa o Otimizador em uma árvore falsa: nada do sistema real é alterado."""
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

CAMINHO = sys.argv.pop(1) if len(sys.argv) > 1 else str(Path(__file__).parents[1] / "otimizador/carlos-otimizador")
carregador = importlib.machinery.SourceFileLoader("carlos_otimizador", CAMINHO)
spec = importlib.util.spec_from_loader("carlos_otimizador", carregador)
mod = importlib.util.module_from_spec(spec)
carregador.exec_module(mod)


class Teste(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Path(self.tmp.name) / "raiz"
        base = {
            "proc/sys/vm/swappiness": "60\n",
            "proc/sys/vm/page-cluster": "3\n",
            "proc/sys/vm/dirty_writeback_centisecs": "500\n",
            "proc/sys/kernel/nmi_watchdog": "1\n",
            "proc/swaps": "Filename Type Size Used Priority\n",
            "sys/kernel/mm/lru_gen/min_ttl_ms": "0\n",
            "sys/kernel/mm/transparent_hugepage/enabled": "[always] madvise never\n",
            "sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference": "balance_performance\n",
            "sys/devices/system/cpu/cpu1/cpufreq/energy_performance_preference": "balance_performance\n",
            "proc/pressure/memory": "some avg10=0 avg60=0 avg300=0 total=0\nfull avg10=0 avg60=0 avg300=9.00 total=0\n",
        }
        for caminho, valor in base.items():
            self.escrever(caminho, valor)
        self.novo()

    def tearDown(self):
        self.tmp.cleanup()

    def novo(self):
        d = Path(self.tmp.name)
        self.o = mod.Otimizador(self.r, d / "etc", d / "estado", d / "run")

    def escrever(self, caminho, valor):
        p = self.r / caminho
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(valor)

    def ler(self, caminho):
        return (self.r / caminho).read_text().strip()

    def bateria(self, ligada):
        self.escrever("sys/class/power_supply/BAT0/type", "Battery\n")
        self.escrever("sys/class/power_supply/BAT0/present", "1\n")
        self.escrever("sys/class/power_supply/AC/type", "Mains\n")
        self.escrever("sys/class/power_supply/AC/online", "0\n" if ligada else "1\n")

    def test_aplica_lista_e_reverte(self):
        self.o.aplicar()
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "1000")
        self.assertEqual(self.ler("sys/kernel/mm/transparent_hugepage/enabled"), "madvise")
        self.assertEqual(self.ler("proc/sys/vm/swappiness"), "60", "sem zram não muda")
        self.assertEqual(self.ler("proc/sys/vm/dirty_writeback_centisecs"), "500", "na tomada não muda")
        self.o.reverter()
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "0")
        self.assertEqual(self.ler("sys/kernel/mm/transparent_hugepage/enabled"), "always")

    def test_zram(self):
        self.escrever("proc/swaps", "Filename Type Size Used Priority\n/dev/zram0 partition 1 0 100\n")
        self.o.aplicar()
        self.assertEqual(self.ler("proc/sys/vm/swappiness"), "100")
        self.assertEqual(self.ler("proc/sys/vm/page-cluster"), "0")

    def test_bateria_vai_e_volta(self):
        self.bateria(True)
        self.o.aplicar()
        self.assertEqual(self.ler("proc/sys/vm/dirty_writeback_centisecs"), "1500")
        self.assertEqual(self.ler("sys/devices/system/cpu/cpu1/cpufreq/energy_performance_preference"), "balance_power")
        self.bateria(False)
        self.o.aplicar()
        self.assertEqual(self.ler("proc/sys/vm/dirty_writeback_centisecs"), "500")
        self.assertEqual(self.ler("sys/devices/system/cpu/cpu1/cpufreq/energy_performance_preference"), "balance_performance")

    def test_ppd_tem_prioridade_na_energia(self):
        self.bateria(True)
        self.escrever("ppd-ativo", "")
        self.o.aplicar()
        self.assertEqual(self.ler("sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference"), "balance_performance")
        self.assertEqual(self.ler("proc/sys/vm/dirty_writeback_centisecs"), "1500")

    def test_nao_briga_com_o_usuario(self):
        self.o.aplicar()
        self.escrever("sys/kernel/mm/lru_gen/min_ttl_ms", "5\n")
        self.o.aplicar()
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "5")
        self.o.reverter()
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "5", "reverter não apaga a escolha do usuário")

    def test_reverte_depois_de_queda(self):
        self.o.aplicar()
        self.novo()  # processo novo, sem memória: usa originais.json
        self.o.aplicar()  # não pode tomar 1000 como original
        self.o.reverter()
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "0")

    def test_config_desliga_por_id_e_nao_aceita_caminho(self):
        d = Path(self.tmp.name) / "etc"
        d.mkdir()
        (d / "config.json").write_text(json.dumps({"desligados": ["memoria-thp-madvise"],
                                                   "ajustes": [{"caminho": "proc/sys/vm/swappiness", "valor": "1"}]}))
        self.o.aplicar()
        self.assertEqual(self.ler("sys/kernel/mm/transparent_hugepage/enabled"), "[always] madvise never")
        self.assertEqual(self.ler("proc/sys/vm/swappiness"), "60")
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "1000")

    def test_desligar_depois_reverte(self):
        self.o.aplicar()
        d = Path(self.tmp.name) / "etc"
        d.mkdir()
        (d / "config.json").write_text('{"ativo": false}')
        self.o.aplicar()
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "0")

    def test_sugere_sem_alterar(self):
        antes = {str(p): p.read_text() for p in self.r.rglob("*") if p.is_file()}
        self.o.coletar_sugestoes()
        ids = {s["id"] for s in self.o.sugestoes}
        self.assertIn("memoria-pressao", ids)
        self.assertIn("memoria-sem-swap", ids)
        self.assertEqual(antes, {str(p): p.read_text() for p in self.r.rglob("*") if p.is_file()})
        publicado = json.loads((Path(self.tmp.name) / "run/estado.json").read_text())
        self.assertTrue(publicado["sugestoes"])
        self.assertEqual(os.stat(Path(self.tmp.name) / "run/estado.json").st_mode & 0o777, 0o644)

    def test_servico_reverte_ao_receber_sigterm(self):
        d = Path(self.tmp.name)
        processo = subprocess.Popen([sys.executable, CAMINHO, "servir", "--raiz", str(self.r), "--etc", str(d / "etc"),
                                     "--estado", str(d / "estado"), "--publico", str(d / "run")])
        limite = time.monotonic() + 15
        while self.ler("sys/kernel/mm/lru_gen/min_ttl_ms") != "1000" and time.monotonic() < limite:
            time.sleep(0.1)
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "1000")
        rss = next(int(l.split()[1]) for l in Path(f"/proc/{processo.pid}/status").read_text().splitlines()
                   if l.startswith("VmRSS"))
        print(f"\nRSS do serviço: {rss / 1024:.1f} MB", flush=True)
        self.assertLess(rss, 64 * 1024, "precisa caber no MemoryMax do serviço")
        processo.terminate()
        self.assertEqual(processo.wait(15), 0)
        self.assertEqual(self.ler("sys/kernel/mm/lru_gen/min_ttl_ms"), "0")

    def test_caminho_ausente(self):
        os.unlink(self.r / "sys/kernel/mm/lru_gen/min_ttl_ms")
        self.o.aplicar()
        self.assertEqual(self.o.situacoes["memoria-mglru-protecao"], "não disponível neste computador")


if __name__ == "__main__":
    unittest.main()
