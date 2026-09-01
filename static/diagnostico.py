# -*- coding: utf-8 -*-
# diagnostico.py - Localiza o colchete/chave/parêntese não fechado
import sys

def diagnosticar(caminho):
    with open(caminho, encoding="utf-8") as f:
        linhas = f.readlines()

    abertura = {')': '(', ']': '[', '}': '{'}
    pilha = []  # (char_abertura, numero_linha)
    for num, linha in enumerate(linhas, 1):
        for ch in linha:
            if ch in '([{':
                pilha.append((ch, num))
            elif ch in ')]}':
                if not pilha:
                    print(f"ERRO: '{ch}' na linha {num} sem abertura correspondente.")
                    return
                topo, _ = pilha[-1]
                if abertura[ch] != topo:
                    print(f"ERRO: '{ch}' na linha {num} fecha algo diferente de '{topo}' (aberto na linha {pilha[-1][1]}).")
                    return
                pilha.pop()

    if pilha:
        print(f"FALTAM {len(pilha)} fechamento(s). O primeiro não fechado:")
        for ch, num in pilha[:5]:
            print(f"  - '{ch}' aberto na linha {num}")
    else:
        print("OK: todos os colchetes/chaves/parênteses estão balanceados.")

if __name__ == "__main__":
    diagnosticar(sys.argv[1] if len(sys.argv) > 1 else "apresentacao_textos.py")
