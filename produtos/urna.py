# -*- coding: utf-8 -*-
# produtos/urna.py - Validação de Nomes de Urna (5 grafias por nome + cálculo letra a letra)
# RETROCOMPATÍVEL: mantém o retorno (results, ideal, sugs) que o main.py espera,
# mas cada resultado já traz as 5 grafias, o destaque das que somam 8 e a
# observação do autor traduzida em 14 idiomas.
from .mapa import reduzir, _LETRAS

# ---------------------------------------------------------------------------
# 1. GRAFIAS POR CARGO (5 formas de escrita)
# ---------------------------------------------------------------------------
CARGO_GRAFIAS = {
    "vereador":     {"completo": "Vereador",            "abrev": "Ver.",        "abrev_total": "Ver."},
    "dep_estadual": {"completo": "Deputado Estadual",   "abrev": "Dep. Estadual", "abrev_total": "Dep. Est."},
    "dep_federal":  {"completo": "Deputado Federal",    "abrev": "Dep. Federal",  "abrev_total": "Dep. Fed."},
    "senador":      {"completo": "Senador",             "abrev": "Sen.",        "abrev_total": "Sen."},
}

CARGO_LABEL = {
    "vereador": "Vereador",
    "dep_estadual": "Dep. Estadual",
    "dep_federal": "Dep. Federal",
    "senador": "Senador",
}

# ---------------------------------------------------------------------------
# 2. OBSERVAÇÃO DO AUTOR (14 idiomas) — inserida quando não há grafia ideal
# ---------------------------------------------------------------------------
OBSERVACAO_AUTOR = {
    "pt": "O número ideal para o dinheiro e o poder é o 8. Ao escolher outro número essa energia não está assegurada, no entanto, o candidato pode preferir que a sua campanha esteja associada a uma outra energia que já lhe representa em uma camada social e, desse modo escolher essa energia para o seu nome de campanha e número de campanha, se for assim, selecione a energia adequada e depois a função para que isso possa ser pesquisado devidamente com os nomes ou números disponíveis. A escolha é sua e com total privacidade.",
    "en": "The ideal number for money and power is 8. By choosing another number, this energy is not assured. However, the candidate may prefer that their campaign be associated with another energy that already represents them in a social layer, and thus choose that energy for their campaign name and campaign number. If so, select the appropriate energy and then the function so that it can be properly researched with the available names or numbers. The choice is yours and with total privacy.",
    "es": "El número ideal para el dinero y el poder es el 8. Al elegir otro número, esta energía no está asegurada; sin embargo, el candidato puede preferir que su campaña esté asociada a otra energía que ya lo representa en una capa social y, de ese modo, elegir esa energía para su nombre de campaña y número de campaña. Si es así, seleccione la energía adecuada y luego la función para que esto pueda ser investigado debidamente con los nombres o números disponibles. La elección es suya y con total privacidad.",
    "fr": "Le nombre idéal pour l'argent et le pouvoir est le 8. En choisissant un autre nombre, cette énergie n'est pas assurée ; cependant, le candidat peut préférer que sa campagne soit associée à une autre énergie qui le représente déjà dans une couche sociale et, ainsi, choisir cette énergie pour son nom de campagne et son numéro de campagne. Si c'est le cas, sélectionnez l'énergie appropriée puis la fonction afin que cela puisse être recherché correctement avec les noms ou numéros disponibles. Le choix vous appartient et en toute confidentialité.",
    "de": "Die ideale Zahl für Geld und Macht ist die 8. Wenn Sie eine andere Zahl wählen, ist diese Energie nicht gewährleistet. Der Kandidat kann jedoch bevorzugen, dass seine Kampagne mit einer anderen Energie verbunden ist, die ihn bereits in einer sozialen Schicht repräsentiert, und auf diese Weise diese Energie für seinen Kampagnennamen und seine Kampagnennummer wählen. Wenn dies der Fall ist, wählen Sie die passende Energie und dann die Funktion, damit dies mit den verfügbaren Namen oder Nummern ordnungsgemäß recherchiert werden kann. Die Wahl liegt bei Ihnen und in völliger Privatsphäre.",
    "it": "Il numero ideale per il denaro e il potere è l'8. Scegliendo un altro numero, questa energia non è garantita; tuttavia, il candidato può preferire che la sua campagna sia associata a un'altra energia che già lo rappresenta in uno strato sociale e, in questo modo, scegliere quell'energia per il suo nome di campagna e numero di campagna. Se è così, selezioni l'energia appropriata e poi la funzione affinché ciò possa essere ricercato adeguatamente con i nomi o numeri disponibili. La scelta è sua e in totale privacy.",
    "nl": "Het ideale getal voor geld en macht is de 8. Door een ander getal te kiezen, is deze energie niet verzekerd; de kandidaat kan er echter de voorkeur aan geven dat zijn campagne wordt geassocieerd met een andere energie die hem al vertegenwoordigt in een sociale laag en op die manier die energie kiezen voor zijn campagnenaam en campagnenummer. Als dat zo is, selecteer dan de juiste energie en vervolgens de functie, zodat dit op de juiste manier kan worden onderzocht met de beschikbare namen of nummers. De keuze is aan u en met volledige privacy.",
    "ru": "Идеальное число для денег и власти — 8. Выбирая другое число, эта энергия не гарантируется; однако кандидат может предпочесть, чтобы его кампания была связана с другой энергией, которая уже представляет его в социальном слое, и таким образом выбрать эту энергию для своего названия кампании и номера кампании. Если это так, выберите подходящую энергию, а затем функцию, чтобы это можно было должным образом исследовать с доступными именами или номерами. Выбор за вами и в полной конфиденциальности.",
    "ja": "お金と力にとって理想的な数字は8です。別の数字を選ぶと、このエネルギーは保証されません。ただし、候補者は、自分のキャンペーンが社会的な層で自分をすでに表している別のエネルギーと結びつくことを望む場合があり、その場合は、そのエネルギーをキャンペーン名とキャンペーン番号に選ぶことができます。その場合は、適切なエネルギーを選択し、次に関数を選択して、利用可能な名前や番号で適切に検索できるようにしてください。選択はあなた次第であり、完全なプライバシーが保たれます。",
    "zh": "金钱和权力的理想数字是8。选择另一个数字，这种能量就无法得到保证。然而，候选人可能更希望自己的竞选活动与另一种已经在社会层面代表他的能量相关联，从而选择这种能量作为他的竞选名称和竞选号码。如果是这样，请选择适当的能量，然后选择相应的功能，以便利用可用的名称或号码进行正确的搜索。选择权在您手中，并且完全保密。",
    "ko": "돈과 권력에 이상적인 숫자는 8입니다. 다른 숫자를 선택하면 이 에너지가 보장되지 않습니다. 그러나 후보자는 자신의 캠페인이 이미 사회적 계층에서 자신을 대표하는 다른 에너지와 연관되기를 원할 수 있으며, 그렇게 되면 그 에너지를 캠페인 이름과 캠페인 번호로 선택할 수 있습니다. 그렇다면 적절한 에너지를 선택한 다음 기능을 선택하여 사용 가능한 이름이나 번호로 제대로 검색할 수 있도록 하십시오. 선택은 전적으로 귀하의 몫이며 완전한 개인정보가 보호됩니다.",
    "ar": "الرقم المثالي للمال والسلطة هو 8. عند اختيار رقم آخر، لا تكون هذه الطاقة مضمونة؛ ومع ذلك، قد يفضل المرشح أن ترتبط حملته بطاقة أخرى تمثله بالفعل في طبقة اجتماعية، وبالتالي يختار تلك الطاقة لاسم حملته ورقم حملته. إذا كان الأمر كذلك، فاختر الطاقة المناسبة ثم الوظيفة حتى يمكن البحث عن ذلك بشكل صحيح بالأسماء أو الأرقام المتاحة. الخيار لك وبخصوصية تامة.",
    "he": "המספר האידיאלי לכסף ולכוח הוא 8. בבחירת מספר אחר, אנרגיה זו אינה מובטחת; עם זאת, המועמד עשוי להעדיף שהקמפיין שלו יהיה קשור לאנרגיה אחרת שכבר מייצגת אותו בשכבה חברתית, ובדרך זו לבחור באנרגיה זו עבור שם הקמפיין ומספר הקמפיין שלו. אם כך, בחרו את האנרגיה המתאימה ולאחר מכן את הפונקציה, כדי שניתן יהיה לחקור זאת כראוי עם השמות או המספרים הזמינים. הבחירה היא שלכם ובפרטיות מלאה.",
    "hi": "पैसे और शक्ति के लिए आदर्श संख्या 8 है। कोई अन्य संख्या चुनने पर यह ऊर्जा सुनिश्चित नहीं होती; हालाँकि, उम्मीदवार चाह सकता है कि उसका अभियान किसी ऐसी अन्य ऊर्जा से जुड़ा हो जो पहले से ही उसे एक सामाजिक स्तर में प्रतिनिधित्व करती है, और इस प्रकार वह उस ऊर्जा को अपने अभियान के नाम और अभियान संख्या के लिए चुन सकता है। यदि ऐसा है, तो उपयुक्त ऊर्जा और फिर कार्य का चयन करें ताकि उपलब्ध नामों या संख्याओं के साथ इसकी उचित खोज की जा सके। चुनाव आपका है और पूर्ण गोपनीयता के साथ।",
}

def observacao_autor(lang="pt"):
    return OBSERVACAO_AUTOR.get(lang, OBSERVACAO_AUTOR["pt"])

# ---------------------------------------------------------------------------
# 3. CÁLCULO LETRA A LETRA DE UMA GRAFIA
# ---------------------------------------------------------------------------
def _energia_grafia(texto):
    limpo = texto.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
    letras = []
    st = 0
    for c in limpo:
        v = _LETRAS.get(c, 0)
        letras.append({"letra": c, "valor": v})
        st += v
    en = reduzir(st)
    return {"forma": texto, "soma": st, "energia": en,
            "eh_ideal": en == 8, "letras": letras}

# ---------------------------------------------------------------------------
# 4. GERAÇÃO DAS 5 GRAFIAS DE UM NOME
# ---------------------------------------------------------------------------
def _gerar_grafias(nome, cargo_key):
    g = CARGO_GRAFIAS.get(cargo_key, CARGO_GRAFIAS["vereador"])
    n = nome.strip()
    completo, abrev, abrev_total = g["completo"], g["abrev"], g["abrev_total"]
    formas = [
        f"{completo} {n}",        # 1. cargo completo antes do nome
        f"{n} - {completo}",      # 2. cargo completo depois do nome
        f"{abrev} {n}",           # 3. cargo abreviado antes do nome
        f"{n} - {abrev}",         # 4. cargo abreviado depois do nome
        f"{abrev_total} {n}",     # 5. abreviação total antes do nome
    ]
    return [_energia_grafia(f) for f in formas]

# ---------------------------------------------------------------------------
# 5. FUNÇÃO PRINCIPAL — RETROCOMPATÍVEL (results, ideal, sugs)
# ---------------------------------------------------------------------------
def validar_nomes_urna(nomes, cargo_key, lang="pt"):
    """
    Para cada nome, gera as 5 grafias, calcula a energia de cada uma e destaca
    as que somam 8 (IDEAL). Mantém o retorno (results, ideal, sugs) para não
    quebrar o main.py, mas cada result agora traz 'grafias' e 'observacao'.
    """
    results = []
    for nome in nomes:
        if not nome.strip():
            continue
        grafias = _gerar_grafias(nome, cargo_key)
        tem_ideal = any(g["eh_ideal"] for g in grafias)
        # Mantém os campos originais (nome, energia, soma, eh_ideal, letras)
        # para o gerador de PDF atual continuar funcionando, e adiciona grafias.
        results.append({
            "nome": nome.strip().title(),
            "energia": next((g["energia"] for g in grafias if g["eh_ideal"]), grafias[0]["energia"]),
            "soma": next((g["soma"] for g in grafias if g["eh_ideal"]), grafias[0]["soma"]),
            "eh_ideal": tem_ideal,
            "explicacao": (f"Nome {nome.strip().title()} tem grafia com ENERGIA 8! "
                           f"Ideal para candidatura." if tem_ideal
                           else f"Nome {nome.strip().title()}: veja as 5 grafias e suas energias."),
            "letras": grafias[0]["letras"],
            "grafias": grafias,
            "observacao": None if tem_ideal else observacao_autor(lang),
        })
    ideal = any(r["eh_ideal"] for r in results)
    # Sugestões (mantém o comportamento original de até 3)
    sugs = []
    if not ideal:
        lbl = CARGO_LABEL.get(cargo_key, "")
        for nome in nomes:
            if not nome.strip():
                continue
            for nt in [f"{lbl[:3]} {nome.strip()}", f"{nome.strip()} - {lbl.lower()[:3]}"]:
                total = sum(_LETRAS.get(c, 0) for c in nt.upper().replace(" ", ""))
                en = reduzir(total)
                sugs.append({"nome": nt.title(), "energia": en, "eh_ideal": en == 8})
                if len(sugs) >= 3:
                    break
            if len(sugs) >= 3:
                break
    return results, ideal, sugs[:3]
