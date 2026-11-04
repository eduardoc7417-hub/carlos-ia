"""Queda de energia: depois de um boot novo, o Otimizador volta a aplicar os ajustes (correção da 0.10)."""
import importlib.machinery
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

CAMINHO = sys.argv.pop(1) if len(sys.argv) > 1 else str(Path(__file__).parents[1] / "otimizador/carlos-otimizador")
carregador = importlib.machinery.SourceFileLoader("carlos_otimizador", CAMINHO)
spec = importlib.util.spec_from_loader("carlos_otimizador", carregador)
mod = importlib.util.module_from_spec(spec)
carregador.exec_module(mod)


class Queda(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        self.raiz = self.d / "raiz"
        self.boot("boot-1")
        (self.raiz / "proc/swaps").write_text("Filename Type Size Used Priority\n/dev/zram0 partition 100 0 100\n")

    def tearDown(self):
        self.tmp.cleanup()

    def boot(self, boot_id):
        """Simula um boot: o kernel volta aos valores padrão e ganha um boot_id novo."""
        for caminho, valor in (("proc/sys/vm/swappiness", "60"), ("proc/sys/kernel/random/boot_id", boot_id)):
            (self.raiz / caminho).parent.mkdir(parents=True, exist_ok=True)
            (self.raiz / caminho).write_text(valor)

    def otimizador(self):
        return mod.Otimizador(self.raiz, self.d / "etc", self.d / "estado", self.d / "run")

    def swappiness(self):
        return (self.raiz / "proc/sys/vm/swappiness").read_text()

    def test_volta_a_aplicar_depois_de_queda(self):
        self.otimizador().aplicar()      # aplica e "cai" sem reverter
        self.boot("boot-2")
        o = self.otimizador()
        o.aplicar()
        self.assertEqual(self.swappiness(), "100", o.situacoes)
        o.reverter()
        self.assertEqual(self.swappiness(), "60")

    def test_mesmo_boot_respeita_mudanca_de_fora(self):
        self.otimizador().aplicar()
        (self.raiz / "proc/sys/vm/swappiness").write_text("80")  # alguém mudou depois do Otimizador
        o = self.otimizador()            # o serviço reiniciou no mesmo boot
        o.aplicar()
        self.assertEqual(self.swappiness(), "80")


if __name__ == "__main__":
    unittest.main()
