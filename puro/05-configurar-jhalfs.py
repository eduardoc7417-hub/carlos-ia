"""Gera o arquivo `configuration` da jhalfs sem abrir o menu. Rodar como construtor:
python3 05-configurar-jhalfs.py
"""
import os
import shutil
import sys
from pathlib import Path

JHALFS = Path("/home/construtor/jhalfs")
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(JHALFS / "menu"))
os.chdir(JHALFS)
os.environ["CONFIG_"] = ""  # a jhalfs lê as opções sem o prefixo CONFIG_, como o Makefile dela faz
import kconfiglib  # noqa: E402

ESCOLHAS = {
    "BOOK_LFS_SYSD": "y",
    "COMMIT": "r13.1",          # livro fixo na versão 13.1
    "BUILDDIR": "/mnt/lfs",
    "GETPKG": "n",              # o 02-fontes.sh já baixou e conferiu
    "RUNMAKE": "n",             # o make roda separado, em segundo plano
    "TST_1": "y",               # só os testes críticos (binutils, gmp, mpfr, mpc, gcc)
    "INSTALL_LOG": "y",         # lista de arquivos por pacote: base do gerenciador de pacotes da etapa 2
    "STRIP": "y",
    "HAVE_FSTAB": "y",
    "FSTAB": "/home/construtor/fstab",
    "CONFIG_BUILD_KERNEL": "n", # o kernel e o GRUB ficam com o 06-kernel.sh
    "TIMEZONE": "America/Sao_Paulo",
    "LANG": "pt_BR.UTF-8",
    "PAGE_A4": "y",
    "HOSTNAME": "carlos-os",
    "INTERFACE": "enp0s3",      # placa de rede padrão do QEMU
    "IP_ADDR": "10.0.2.15",
    "DOMAIN": "localdomain",
    "KEYMAP": "br-abnt2",
    "REPORT": "y",
}

k = kconfiglib.Kconfig("Config.in", warn=False)
for nome, valor in ESCOLHAS.items():
    simbolo = k.syms[nome]
    if not simbolo.set_value(valor) and simbolo.str_value != valor:
        raise SystemExit(f"opção recusada: {nome}={valor}")
for nome, valor in ESCOLHAS.items():
    assert k.syms[nome].str_value == valor, f"{nome} ficou {k.syms[nome].str_value!r}"
shutil.copy(AQUI / "fstab", ESCOLHAS["FSTAB"])
k.write_config("configuration")
# Sem isto a jhalfs pergunta se a configuração foi salva no menu.
Path("configuration.old").unlink(missing_ok=True)
print("configuration gravada com", len(ESCOLHAS), "escolhas")
