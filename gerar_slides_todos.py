# -*- coding: utf-8 -*-
# ================================================================
#  gerar_slides_todos.py
#  Gera os 14 decks de slides a partir do apresentacao_textos.py.
#  Salva em: static/apresentacao_slides_{lang}.pdf
#  Rode com:  python gerar_slides_todos.py
# ================================================================
import os, sys

IDIOMAS = ["pt", "en", "es", "it", "fr", "de", "ja", "zh",
           "ru", "he", "ar", "id", "tr", "vi"]

# --- Importa o gerador de slides do seu arquivo ---
# A análise confirmou a função gerar_pdf_slides no apresentacao_textos.py.
try:
    from apresentacao_textos import gerar_pdf_slides as gerar
    MODO = "gerar_pdf_slides"
except ImportError:
    # Fallback caso o nome da função no seu arquivo seja gerar_apresentacao
    from apresentacao_textos import gerar_apresentacao as gerar
    MODO = "gerar_apresentacao"

def gerar_um(lang):
    alvo = os.path.join("static", f"apresentacao_slides_{lang}.pdf")
    print(f"[{lang}] gerando {alvo} ...", end=" ", flush=True)

    # 1) Tenta chamadas possíveis e coleta o retorno
    retorno = None
    for args in ((lang,), (lang, "static"), (lang, os.path.abspath("static"))):
        try:
            retorno = gerar(*args)
            break
        except TypeError:
            continue
        except Exception as e:
            print(f"ERRO: {e}")
            return False

    # 2) Se retornou um caminho de arquivo válido, move para static/
    if isinstance(retorno, str) and retorno and os.path.exists(retorno):
        os.makedirs("static", exist_ok=True)
        os.replace(retorno, alvo)
        print("ok")
        return True

    # 3) Se não retornou caminho, procura o PDF recém-criado na pasta
    for candidato in (f"apresentacao_slides_{lang}.pdf",
                      f"apresentacao_{lang}.pdf",
                      f"Apresentacao-Slides-{lang}.pdf"):
        if os.path.exists(candidato):
            os.makedirs("static", exist_ok=True)
            os.replace(candidato, alvo)
            print("ok")
            return True

    print("FALHOU (confira o nome/assinatura da função no fim do apresentacao_textos.py)")
    return False

def main():
    os.makedirs("static", exist_ok=True)
    ok = 0
    for lang in IDIOMAS:
        if gerar_um(lang):
            ok += 1
    print(f"\nConcluído: {ok}/14. Confira a pasta static/ (apresentacao_slides_*.pdf)")

if __name__ == "__main__":
    main()
