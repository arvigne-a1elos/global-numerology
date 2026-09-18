# -*- coding: utf-8 -*-
# produtos/urna.py - Validação de Nomes de Urna (5 grafias por nome)
# ============================================================
# APRIMORAMENTO 2026-09-18:
#   * 5 grafias por candidato (cargo completo/abreviado x nome completo/abreviado)
#   * Gênero do cargo (masculino/feminino): a desinência altera o peso e a energia
#   * Cargos em 14 idiomas, com formas e abreviações traduzidas
#   * Observação do autor em 14 idiomas quando a energia escolhida != 8
#   * Nota antecipada de tradução em 14 idiomas (sugestões valem bônus)
#   * Interface RETROCOMPATÍVEL: retorna (results, ideal, sugs) - main.py não quebra
# ============================================================
from .mapa import reduzir, _LETRAS

# (completo, abrev, abrev_total) por cargo, idioma e gênero
CARGO_URNA = {
    "vereador": {
        "pt": {"masculino": ("Vereador", "Ver.", "Ver."), "feminino": ("Vereadora", "Ver.", "Ver.")},
        "en": {"masculino": ("Councilor", "Coun.", "Coun."), "feminino": ("Councilwoman", "Coun.", "Coun.")},
        "es": {"masculino": ("Concejal", "Conc.", "Conc."), "feminino": ("Concejala", "Conc.", "Conc.")},
        "it": {"masculino": ("Consigliere", "Cons.", "Cons."), "feminino": ("Consigliera", "Cons.", "Cons.")},
        "fr": {"masculino": ("Conseiller municipal", "Cons. mun.", "Cons."), "feminino": ("Conseillère municipale", "Cons. mun.", "Cons.")},
        "de": {"masculino": ("Stadtrat", "StR", "StR"), "feminino": ("Stadträtin", "StR", "StR")},
        "ja": {"masculino": ("市議会議員", "市議", "市議"), "feminino": ("市議会議員", "市議", "市議")},
        "zh": {"masculino": ("市议员", "市议员", "市议员"), "feminino": ("市议员", "市议员", "市议员")},
        "ru": {"masculino": ("Депутат горсовета", "Деп.", "Деп."), "feminino": ("Депутат горсовета", "Деп.", "Деп.")},
        "id": {"masculino": ("Anggota DPRD Kota", "Anggota", "Anggota"), "feminino": ("Anggota DPRD Kota", "Anggota", "Anggota")},
        "tr": {"masculino": ("Belediye Meclis Üyesi", "Üye", "Üye"), "feminino": ("Belediye Meclis Üyesi", "Üye", "Üye")},
        "vi": {"masculino": ("Ủy viên HĐ thành phố", "UV HĐTP", "UV"), "feminino": ("Ủy viên HĐ thành phố", "UV HĐTP", "UV")},
        "he": {"masculino": ("חבר מועצה", "ח״מ", "ח״מ"), "feminino": ("חברת מועצה", "ח״מ", "ח״מ")},
        "ar": {"masculino": ("عضو مجلس بلدي", "عضو", "عضو"), "feminino": ("عضو مجلس بلدي", "عضو", "عضو")},
    },
    "dep_estadual": {
        "pt": {"masculino": ("Deputado Estadual", "Dep. Estadual", "Dep. Est."), "feminino": ("Deputada Estadual", "Dep. Estadual", "Dep. Est.")},
        "en": {"masculino": ("State Deputy", "St. Dep.", "St. Dep."), "feminino": ("State Deputy", "St. Dep.", "St. Dep.")},
        "es": {"masculino": ("Diputado Estatal", "Dip. Est.", "Dip. Est."), "feminino": ("Diputada Estatal", "Dip. Est.", "Dip. Est.")},
        "it": {"masculino": ("Deputato Regionale", "Dep. Reg.", "Dep. Reg."), "feminino": ("Deputata Regionale", "Dep. Reg.", "Dep. Reg.")},
        "fr": {"masculino": ("Député régional", "Dép. rég.", "Dép. rég."), "feminino": ("Députée régionale", "Dép. rég.", "Dép. rég.")},
        "de": {"masculino": ("Landtagsabgeordneter", "MdL", "MdL"), "feminino": ("Landtagsabgeordnete", "MdL", "MdL")},
        "ja": {"masculino": ("州議会議員", "州議", "州議"), "feminino": ("州議会議員", "州議", "州議")},
        "zh": {"masculino": ("州议员", "州议员", "州议员"), "feminino": ("州议员", "州议员", "州议员")},
        "ru": {"masculino": ("Депутат региональный", "Деп.", "Деп."), "feminino": ("Депутат региональный", "Деп.", "Деп.")},
        "id": {"masculino": ("Anggota DPRD Provinsi", "Anggota", "Anggota"), "feminino": ("Anggota DPRD Provinsi", "Anggota", "Anggota")},
        "tr": {"masculino": ("Eyalet Milletvekili", "Mv.", "Mv."), "feminino": ("Eyalet Milletvekili", "Mv.", "Mv.")},
        "vi": {"masculino": ("Đại biểu HĐ bang", "ĐB HĐB", "ĐB"), "feminino": ("Đại biểu HĐ bang", "ĐB HĐB", "ĐB")},
        "he": {"masculino": ("חבר מועצה", "ח״מ", "ח״מ"), "feminino": ("חברת מועצה", "ח״מ", "ח״מ")},
        "ar": {"masculino": ("نائب إقليمي", "نائب", "نائب"), "feminino": ("نائب إقليمي", "نائب", "نائب")},
    },
    "dep_federal": {
        "pt": {"masculino": ("Deputado Federal", "Dep. Federal", "Dep. Fed."), "feminino": ("Deputada Federal", "Dep. Federal", "Dep. Fed.")},
        "en": {"masculino": ("Federal Deputy", "Fed. Dep.", "Fed. Dep."), "feminino": ("Federal Deputy", "Fed. Dep.", "Fed. Dep.")},
        "es": {"masculino": ("Diputado Federal", "Dip. Fed.", "Dip. Fed."), "feminino": ("Diputada Federal", "Dip. Fed.", "Dip. Fed.")},
        "it": {"masculino": ("Deputato Federale", "Dep. Fed.", "Dep. Fed."), "feminino": ("Deputata Federale", "Dep. Fed.", "Dep. Fed.")},
        "fr": {"masculino": ("Député fédéral", "Dép. féd.", "Dép. féd."), "feminino": ("Députée fédérale", "Dép. féd.", "Dép. féd.")},
        "de": {"masculino": ("Bundestagsabgeordneter", "MdB", "MdB"), "feminino": ("Bundestagsabgeordnete", "MdB", "MdB")},
        "ja": {"masculino": ("連邦議会議員", "連邦議", "連邦議"), "feminino": ("連邦議会議員", "連邦議", "連邦議")},
        "zh": {"masculino": ("联邦议员", "联邦议员", "联邦议员"), "feminino": ("联邦议员", "联邦议员", "联邦议员")},
        "ru": {"masculino": ("Депутат федеральный", "Деп.", "Деп."), "feminino": ("Депутат федеральный", "Деп.", "Деп.")},
        "id": {"masculino": ("Anggota DPR", "Anggota", "Anggota"), "feminino": ("Anggota DPR", "Anggota", "Anggota")},
        "tr": {"masculino": ("Federal Milletvekili", "Mv.", "Mv."), "feminino": ("Federal Milletvekili", "Mv.", "Mv.")},
        "vi": {"masculino": ("Đại biểu Quốc hội", "ĐB QH", "ĐB"), "feminino": ("Đại biểu Quốc hội", "ĐB QH", "ĐB")},
        "he": {"masculino": ("חבר הכנסת", "ח״כ", "ח״כ"), "feminino": ("חברת הכנסת", "ח״כ", "ח״כ")},
        "ar": {"masculino": ("نائب اتحادي", "نائب", "نائب"), "feminino": ("نائب اتحادي", "نائب", "نائب")},
    },
    "senador": {
        "pt": {"masculino": ("Senador", "Sen.", "Sen."), "feminino": ("Senadora", "Sen.", "Sen.")},
        "en": {"masculino": ("Senator", "Sen.", "Sen."), "feminino": ("Senator", "Sen.", "Sen.")},
        "es": {"masculino": ("Senador", "Sen.", "Sen."), "feminino": ("Senadora", "Sen.", "Sen.")},
        "it": {"masculino": ("Senatore", "Sen.", "Sen."), "feminino": ("Senatrice", "Sen.", "Sen.")},
        "fr": {"masculino": ("Sénateur", "Sén.", "Sén."), "feminino": ("Sénatrice", "Sén.", "Sén.")},
        "de": {"masculino": ("Senator", "Sen.", "Sen."), "feminino": ("Senatorin", "Sen.", "Sen.")},
        "ja": {"masculino": ("上院議員", "上院", "上院"), "feminino": ("上院議員", "上院", "上院")},
        "zh": {"masculino": ("参议员", "参议员", "参议员"), "feminino": ("参议员", "参议员", "参议员")},
        "ru": {"masculino": ("Сенатор", "Сен.", "Сен."), "feminino": ("Сенатор", "Сен.", "Сен.")},
        "id": {"masculino": ("Senator", "Sen.", "Sen."), "feminino": ("Senator", "Sen.", "Sen.")},
        "tr": {"masculino": ("Senatör", "Sen.", "Sen."), "feminino": ("Senatör", "Sen.", "Sen.")},
        "vi": {"masculino": ("Thượng nghị sĩ", "ThN", "ThN"), "feminino": ("Thượng nghị sĩ", "ThN", "ThN")},
        "he": {"masculino": ("סנטור", "סנ", "סנ"), "feminino": ("סנטורית", "סנ", "סנ")},
        "ar": {"masculino": ("عضو مجلس الشيوخ", "عضو", "عضو"), "feminino": ("عضو مجلس الشيوخ", "عضو", "عضو")},
    },
}

CARGO_LABEL = {
    "vereador": "Vereador",
    "dep_estadual": "Deputado Estadual",
    "dep_federal": "Deputado Federal",
    "senador": "Senador",
}

# Observação do autor (14 idiomas) - inserida quando a energia escolhida != 8
OBSERVACAO_AUTOR = {
    "pt": "O número ideal para o dinheiro e o poder é o 8. Ao escolher outro número essa energia não está assegurada, no entanto, o candidato pode preferir que a sua campanha esteja associada a uma outra energia que já lhe representa em uma camada social e, desse modo escolher essa energia para o seu nome de campanha e número de campanha, se for assim, selecione a energia adequada e depois a função para que isso possa ser pesquisado devidamente com os nomes ou números disponíveis. A escolha é sua e com total privacidade.",
    "en": "The ideal number for money and power is 8. By choosing another number, this energy is not assured. However, the candidate may prefer that their campaign be associated with another energy that already represents them in a social layer, and thus choose that energy for their campaign name and campaign number. If so, select the appropriate energy and then the function so that it can be properly researched with the available names or numbers. The choice is yours and with total privacy.",
    "es": "El número ideal para el dinero y el poder es el 8. Al elegir otro número, esta energía no está asegurada; sin embargo, el candidato puede preferir que su campaña esté asociada a otra energía que ya lo representa en una capa social y, de ese modo, elegir esa energía para su nombre de campaña y número de campaña. Si es así, seleccione la energía adecuada y luego la función para que esto pueda ser investigado debidamente con los nombres o números disponibles. La elección es suya y con total privacidad.",
    "fr": "Le nombre idéal pour l'argent et le pouvoir est le 8. En choisissant un autre nombre, cette énergie n'est pas assurée ; cependant, le candidat peut préférer que sa campagne soit associée à une autre énergie qui le représente déjà dans une couche sociale et, ainsi, choisir cette énergie pour son nom de campagne et son numéro de campagne. Si c'est le cas, sélectionnez l'énergie appropriée puis la fonction afin que cela puisse être recherché correctement avec les noms ou numéros disponibles. Le choix vous appartient et en toute confidentialité.",
    "de": "Die ideale Zahl für Geld und Macht ist die 8. Wenn Sie eine andere Zahl wählen, ist diese Energie nicht gewährleistet. Der Kandidat kann jedoch bevorzugen, dass seine Kampagne mit einer anderen Energie verbunden ist, die ihn bereits in einer sozialen Schicht repräsentiert, und auf diese Weise diese Energie für seinen Kampagnennamen und seine Kampagnennummer wählen. Wenn dies der Fall ist, wählen Sie die passende Energie und dann die Funktion, damit dies mit den verfügbaren Namen oder Nummern ordnungsgemäß recherchiert werden kann. Die Wahl liegt bei Ihnen und in völliger Privatsphäre.",
    "it": "Il numero ideale per il denaro e il potere è l'8. Scegliendo un altro numero, questa energia non è garantita; tuttavia, il candidato può preferire che la sua campagna sia associata a un'altra energia che già lo rappresenta in uno strato sociale e, in questo modo, scegliere quell'energia per il suo nome di campagna e numero di campagna. Se è così, selezioni l'energia appropriata e poi la funzione affinché ciò possa essere ricercato adeguatamente con i nomi o numeri disponibili. La scelta è sua e in totale privacy.",
    "ja": "お金と力にとって理想的な数字は8です。別の数字を選ぶと、このエネルギーは保証されません。ただし、候補者は、自分のキャンペーンが社会的な層で自分をすでに表している別のエネルギーと結びつくことを望む場合があり、その場合は、そのエネルギーをキャンペーン名とキャンペーン番号に選ぶことができます。その場合は、適切なエネルギーを選択し、次に関数を選択して、利用可能な名前や番号で適切に検索できるようにしてください。選択はあなた次第であり、完全なプライバシーが保たれます。",
    "zh": "金钱和权力的理想数字是8。选择另一个数字，这种能量就无法得到保证。然而，候选人可能更希望自己的竞选活动与另一种已经在社会层面代表他的能量相关联，从而选择这种能量作为他的竞选名称和竞选号码。如果是这样，请选择适当的能量，然后选择相应的功能，以便利用可用的名称或号码进行正确的搜索。选择权在您手中，并且完全保密。",
    "ru": "Идеальное число для денег и власти — 8. Выбирая другое число, эта энергия не гарантируется; однако кандидат может предпочесть, чтобы его кампания была связана с другой энергией, которая уже представляет его в социальном слое, и таким образом выбрать эту энергию для своего названия кампании и номера кампании. Если это так, выберите подходящую энергию, а затем функцию, чтобы это можно было должным образом исследовать с доступными именами или номерами. Выбор за вами и в полной конфиденциальности.",
    "id": "Angka ideal untuk uang dan kekuasaan adalah 8. Dengan memilih angka lain, energi ini tidak dijamin; namun, kandidat mungkin lebih memilih kampanye yang terkait dengan energi lain yang sudah mewakili dirinya dalam lapisan sosial, dan dengan demikian memilih energi itu untuk nama kampanye dan nomor kampanyenya. Jika demikian, pilih energi yang tepat dan kemudian fungsi tersebut agar dapat diteliti dengan baik menggunakan nama atau nomor yang tersedia. Pilihan ada di tangan Anda dan sepenuhnya privat.",
    "tr": "Para ve güç için ideal sayı 8'dir. Başka bir sayı seçildiğinde bu enerji garanti edilmez; ancak aday, kampanyasının kendisini zaten sosyal bir katmanda temsil eden başka bir enerjiyle ilişkilendirilmesini tercih edebilir ve bu nedenle kampanya adı ve kampanya numarası için bu enerjiyi seçebilir. Böyle ise, uygun enerjiyi ve ardından işlevi seçin ki bu, mevcut adlar veya numaralarla düzgün bir şekilde araştırılabilsin. Seçim sizin ve tamamen gizlilik içindedir.",
    "vi": "Con số lý tưởng cho tiền bạc và quyền lực là 8. Khi chọn một con số khác, năng lượng này không được đảm bảo; tuy nhiên, ứng viên có thể muốn chiến dịch của mình gắn với một năng lượng khác đã đại diện cho họ trong một tầng lớp xã hội, và do đó chọn năng lượng đó cho tên chiến dịch và số chiến dịch của mình. Nếu vậy, hãy chọn năng lượng phù hợp và sau đó chọn chức năng để điều này có thể được nghiên cứu đúng cách với các tên hoặc số có sẵn. Sự lựa chọn là của bạn và hoàn toàn riêng tư.",
    "he": "המספר האידיאלי לכסף ולכוח הוא 8. בבחירת מספר אחר, אנרגיה זו אינה מובטחת; עם זאת, המועמד עשוי להעדיף שהקמפיין שלו יהיה קשור לאנרגיה אחרת שכבר מייצגת אותו בשכבה חברתית, ובדרך זו לבחור באנרגיה זו עבור שם הקמפיין ומספר הקמפיין שלו. אם כך, בחרו את האנרגיה המתאימה ולאחר מכן את הפונקציה, כדי שניתן יהיה לחקור זאת כראוי עם השמות או המספרים הזמינים. הבחירה היא שלכם ובפרטיות מלאה.",
    "ar": "الرقم المثالي للمال والسلطة هو 8. عند اختيار رقم آخر، لا تكون هذه الطاقة مضمونة؛ ومع ذلك، قد يفضل المرشح أن ترتبط حملته بطاقة أخرى تمثله بالفعل في طبقة اجتماعية، وبالتالي يختار تلك الطاقة لاسم حملته ورقم حملته. إذا كان الأمر كذلك، فاختر الطاقة المناسبة ثم الوظيفة حتى يمكن البحث عن ذلك بشكل صحيح بالأسماء أو الأرقام المتاحة. الخيار لك وبخصوصية تامة.",
}

# Nota antecipada de tradução (14 idiomas) - sugestões valem bônus
NOTA_TRADUCAO = {
    "pt": "Se você identificar alguma grafia ou pronúncia incorreta nesta tradução, aceitamos sugestões que aperfeiçoem o site. Elas valem brindes bônus do site pela colaboração voluntária.",
    "en": "If you notice any incorrect spelling or pronunciation in this translation, we welcome suggestions that improve the site. They earn site bonus gifts for voluntary collaboration.",
    "es": "Si identificas alguna grafía o pronunciación incorrecta en esta traducción, aceptamos sugerencias que perfeccionen el sitio. Valen regalos bono del sitio por la colaboración voluntaria.",
    "fr": "Si vous repérez une faute d'orthographe ou de prononciation dans cette traduction, nous acceptons des suggestions qui améliorent le site. Elles donnent droit à des cadeaux bonus du site pour la collaboration volontaire.",
    "de": "Wenn Sie eine falsche Schreibweise oder Aussprache in dieser Übersetzung bemerken, nehmen wir Vorschläge an, die die Website verbessern. Sie erhalten dafür Bonus-Geschenke der Website für die freiwillige Mitarbeit.",
    "it": "Se noti un'ortografia o una pronuncia errata in questa traduzione, accettiamo suggerimenti che migliorino il sito. Valgono regali bonus del sito per la collaborazione volontaria.",
    "ja": "この翻訳に誤った表記や発音を見つけた場合は、サイトを改善する提案を受け付けています。自主的な協力に対してサイトのボーナス特典を差し上げます。",
    "zh": "如果您发现此翻译中有任何拼写或发音错误，我们欢迎改进网站的建议。您的自愿合作将获得网站奖励。",
    "ru": "Если вы заметили неправильное написание или произношение в этом переводе, мы принимаем предложения по улучшению сайта. За добровольное сотрудничество вы получите бонусные подарки сайта.",
    "id": "Jika Anda menemukan ejaan atau pengucapan yang salah dalam terjemahan ini, kami menerima saran untuk menyempurnakan situs. Saran tersebut bernilai hadiah bonus situs untuk kerja sama sukarela.",
    "tr": "Bu çeviride yanlış bir yazım veya telaffuz fark ederseniz, siteyi geliştiren önerileri kabul ediyoruz. Gönüllü iş birliği için site bonus hediyeleri kazanırsınız.",
    "vi": "Nếu bạn phát hiện lỗi chính tả hoặc phát âm sai trong bản dịch này, chúng tôi hoan nghênh các đề xuất cải thiện trang web. Chúng có giá trị nhận quà tặng thưởng từ trang web cho sự hợp tác tự nguyện.",
    "he": "אם תבחינו בשגיאת כתיב או הגייה בתרגום זה, אנו מקבלים הצעות המשפרות את האתר. הן מזכות במתנות בונוס מהאתר עבור שיתוף פעולה התנדבותי.",
    "ar": "إذا لاحظت أي خطأ إملائي أو نطق في هذه الترجمة، فنحن نقبل الاقتراحات التي تحسّن الموقع. وهي تستحق هدايا مكافأة من الموقع مقابل التعاون الطوعي.",
}

def observacao_autor(lang="pt"):
    return OBSERVACAO_AUTOR.get(lang, OBSERVACAO_AUTOR["pt"])

def nota_traducao(lang="pt"):
    return NOTA_TRADUCAO.get(lang, NOTA_TRADUCAO["pt"])

def _formas(cargo_key, lang, genero):
    d = CARGO_URNA.get(cargo_key, CARGO_URNA["vereador"])
    g = d.get(lang, d.get("pt", d["pt"]))
    f = g.get(genero, g.get("masculino", g["masculino"]))
    return f  # (completo, abrev, abrev_total)

def _energia_grafia(texto):
    limpo = texto.upper().replace(" ", "").replace(".", "").replace("-", "").replace(",", "")
    letras = []
    st = 0
    for c in limpo:
        v = _LETRAS.get(c, 0)
        letras.append({"letra": c, "valor": v})
        st += v
    en = reduzir(st)
    expl = (f"Grafia '{texto}' tem ENERGIA 8! Ideal para candidatura."
            if en == 8 else f"Grafia '{texto}' tem energia {en}.")
    return {"nome": texto.strip(), "forma": texto.strip(), "soma": st,
            "energia": en, "eh_ideal": en == 8, "explicacao": expl,
            "letras": letras}

def _extrair_nome_base(texto, cargo_key, lang, genero):
    c, a, at = _formas(cargo_key, lang, genero)
    for pref in [f"{c} ", f"{c} - ", f"{a} ", f"{a} - ", f"{at} "]:
        if texto.startswith(pref):
            resto = texto[len(pref):].strip()
            if resto:
                return resto
    return texto.strip()

def validar_nomes_urna(nomes, cargo_key, lang="pt", genero="masculino", nome_base=""):
    """Recebe as grafias completas (cargo + nome) e calcula a energia de cada uma.
    Mantém o retorno (results, ideal, sugs) para não quebrar o main.py.
    Cada result carrega 'observacao' (quando nao ha energia 8) e 'nota_traducao'."""
    nt = nota_traducao(lang)
    results = []
    for texto in nomes:
        if not texto.strip():
            continue
        r = _energia_grafia(texto)
        r["nota_traducao"] = nt
        results.append(r)
    ideal = any(r["eh_ideal"] for r in results)
    for r in results:
        r["observacao"] = None if (ideal or r["eh_ideal"]) else observacao_autor(lang)
    base = nome_base.strip() or (_extrair_nome_base(results[0]["forma"], cargo_key, lang, genero) if results else "")
    sugs = []
    if not ideal and base:
        c, a, at = _formas(cargo_key, lang, genero)
        cand = [f"{c} {base}", f"{a} {base}", f"{at} {base}", f"{base} - {c}"]
        for txt in cand:
            g = _energia_grafia(txt)
            sugs.append({"nome": g["forma"], "energia": g["energia"], "eh_ideal": g["eh_ideal"]})
            if len(sugs) >= 3:
                break
        sugs.sort(key=lambda s: (not s["eh_ideal"], s["energia"]))
        sugs = sugs[:3]
    return results, ideal, sugs
