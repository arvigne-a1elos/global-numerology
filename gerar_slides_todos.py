# -*- coding: utf-8 -*-
# gerar_slides_todos.py
# Gera os 14 decks de slides a partir do apresentacao_textos.py.
# Salva em: static/apresentacao_slides_{lang}.pdf
# Rode com: python gerar_slides_todos.py
import os

IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh",
           "ru", "he", "ar", "id", "tr", "vi"]

from apresentacao_textos import gerar_pdf_slides as gerar

def gerar_um(lang):
    alvo = os.path.join("static", f"apresentacao_slides_{lang}.pdf")
    print(f"[{lang}] gerando {alvo} ...", end=" ", flush=True)
    try:
        retorno = gerar(lang)
    except TypeError:
        print("FALHOU: assinatura inesperada. Confira a definicao de gerar_pdf_slides no fim do apresentacao_textos.py")
        return False
    except Exception as e:
        print(f"ERRO: {type(e).__name__}: {e}")
        return False
    # Caso 1: a funcao retornou um caminho valido
    if isinstance(retorno, str) and retorno and os.path.exists(retorno):
        os.makedirs("static", exist_ok=True)
        if os.path.abspath(retorno) != os.path.abspath(alvo):
            os.replace(retorno, alvo)
        print("ok (retorno=caminho)")
        return True
    # Caso 2: retornou None e salvou o arquivo em algum nome conhecido
    for candidato in (f"apresentacao_slides_{lang}.pdf",
                      f"apresentacao_{lang}.pdf",
                      f"Apresentacao-Slides-{lang}.pdf",
                      f"slides_{lang}.pdf",
                      os.path.join("static", f"apresentacao_slides_{lang}.pdf")):
        if os.path.exists(candidato):
            os.makedirs("static", exist_ok=True)
            if os.path.abspath(candidato) != os.path.abspath(alvo):
                os.replace(candidato, alvo)
            print("ok (arquivo localizado)")
            return True
    print(f"FALHOU: retorno={retorno!r}. Confira onde gerar_pdf_slides salva o PDF.")
    return False

def main():
    os.makedirs("static", exist_ok=True)
    ok = 0
    for lang in IDIOMAS:
        if gerar_um(lang):
            ok += 1
    print(f"\nConcluido: {ok}/14. Confira a pasta static/ (apresentacao_slides_*.pdf)")

if __name__ == "__main__":
    main()
