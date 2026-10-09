# -*- coding: utf-8 -*-
"""
renomear_jp.py - Renomeia em bloco as capas japonesas (jp¥ -> jpy)
Rode dentro da pasta raiz do repositorio capas-a1elos.

USO:
  python renomear_jp.py            -> MODO PREVIEW (so lista, nao altera)
  python renomear_jp.py --executar -> renomeia de verdade
"""

import os, sys

# Simbolos de iene possiveis: ¥ (U+00A5) e ￥ (U+FFE5)
SIMBOLOS = ["\u00A5", "\uFFE5"]

def main():
    executar = "--executar" in sys.argv
    alterados = []

    for raiz, _, arquivos in os.walk("."):
        for nome in arquivos:
            if any(s in nome for s in SIMBOLOS):
                novo = nome
                for s in SIMBOLOS:
                    novo = novo.replace(s, "y")
                alterados.append((nome, novo))
                if executar:
                    os.rename(os.path.join(raiz, nome), os.path.join(raiz, novo))

    print(f"Arquivos com simbolo de iene: {len(alterados)} (esperado: 24)")
    for antigo, novo in alterados:
        print(f"  {antigo}  ->  {novo}")

    if not executar:
        print("\nMODO PREVIEW: nada foi alterado.")
        print("Para renomear de verdade: python renomear_jp.py --executar")

if __name__ == "__main__":
    main()
