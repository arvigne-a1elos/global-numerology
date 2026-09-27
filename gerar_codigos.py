# gerar_codigos.py — roda LOCALMENTE, não vai para a internet
# Uso: python gerar_codigos.py --produto nome_pet --energia 5 --liberacao colaboracao --idioma pt --qtd 3
import json, secrets, argparse, os

COD_ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def _checksum(base):
    soma = sum(COD_ALFABETO.index(ch) for ch in base)
    return COD_ALFABETO[soma % len(COD_ALFABETO)]

def _gerar():
    base = "".join(secrets.choice(COD_ALFABETO) for _ in range(7))
    return f"A1-{base[:4]}-{base[4:]}{_checksum(base)}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--produto", required=True)
    ap.add_argument("--energia", default="")
    ap.add_argument("--liberacao", default="colaboracao")
    ap.add_argument("--idioma", default="pt")
    ap.add_argument("--qtd", type=int, default=1)
    args = ap.parse_args()

    arq = "bonus_codes.json"
    dados = {}
    if os.path.exists(arq):
        with open(arq) as f: dados = json.load(f)

    for _ in range(args.qtd):
        cod = _gerar()
        dados[cod] = {
            "produto": args.produto,
            "energia": args.energia,
            "liberacao": args.liberacao,
            "idioma": args.idioma,
            "usado": False,
            "criado_em": "",
            "data_uso": None
        }
        print(cod)

    with open(arq, "w") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"\n{args.qtd} código(s) gravado(s) em {arq}")

if __name__ == "__main__":
    main()
