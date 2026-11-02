# -*- coding: utf-8 -*-
# produtos/imovel.py - Número do Imóvel (3 campos + sugestão única + dica traduzida)
from .mapa import reduzir

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _valor_alfanumerico(texto):
    """Dígitos somam direto; letras viram número pitagórico (A=1...I=9, J=1...Z=8).
    Ex.: 'B' -> 2 · '7' -> 7 · 'C2' -> 3+2=5"""
    if not texto:
        return None
    t = str(texto).upper()
    soma = 0
    tem_algo = False
    for ch in t:
        if ch.isdigit():
            soma += int(ch)
            tem_algo = True
        else:
            idx = LETRAS.find(ch)
            if idx >= 0:
                soma += (idx % 9) + 1
                tem_algo = True
    if not tem_algo:
        return None
    while soma > 9 and soma not in (11, 22, 33):
        soma = sum(int(d) for d in str(soma))
    return soma


# ===== SUGESTÃO ÚNICA POR ENERGIA (14 idiomas) =====
SUGESTOES_TRAD = {
    "pt": {1: "Lugar ideal para: empreendimentos e escritórios de negócios — energia de iniciativa e novos começos.",
           2: "Lugar ideal para: famílias, casais e ambientes de cuidado — energia de cooperação e paz.",
           3: "Lugar ideal para: agências, estúdios e espaços sociais — energia de criatividade e comunicação.",
           4: "Lugar ideal para: clínicas, escritórios e projetos de longo prazo — energia de estabilidade e trabalho.",
           5: "Lugar ideal para: comércio, viagens e transformações — energia de movimento e liberdade.",
           6: "Lugar ideal para: lares, escolas e serviços de saúde — energia de família e responsabilidade.",
           7: "Lugar ideal para: consultórios, bibliotecas e retiros — energia de estudo e espiritualidade.",
           8: "Lugar ideal para: empresas, bancos e finanças — energia de poder material e realização.",
           9: "Lugar ideal para: causas sociais, ONGs e acolhimento — energia de compaixão e conclusões."},
    "en": {1: "Ideal place for: ventures and business offices — energy of initiative and new beginnings.",
           2: "Ideal place for: families, couples and care settings — energy of cooperation and peace.",
           3: "Ideal place for: agencies, studios and social spaces — energy of creativity and communication.",
           4: "Ideal place for: clinics, offices and long-term projects — energy of stability and work.",
           5: "Ideal place for: commerce, travel and transformations — energy of movement and freedom.",
           6: "Ideal place for: homes, schools and health services — energy of family and responsibility.",
           7: "Ideal place for: consulting rooms, libraries and retreats — energy of study and spirituality.",
           8: "Ideal place for: companies, banks and finance — energy of material power and achievement.",
           9: "Ideal place for: social causes, NGOs and shelter — energy of compassion and completion."},
    "es": {1: "Lugar ideal para: emprendimientos y oficinas de negocios — energía de iniciativa y nuevos comienzos.",
           2: "Lugar ideal para: familias, parejas y espacios de cuidado — energía de cooperación y paz.",
           3: "Lugar ideal para: agencias, estudios y espacios sociales — energía de creatividad y comunicación.",
           4: "Lugar ideal para: clínicas, oficinas y proyectos de largo plazo — energía de estabilidad y trabajo.",
           5: "Lugar ideal para: comercio, viajes y transformaciones — energía de movimiento y libertad.",
           6: "Lugar ideal para: hogares, escuelas y servicios de salud — energía de familia y responsabilidad.",
           7: "Lugar ideal para: consultorios, bibliotecas y retiros — energía de estudio y espiritualidad.",
           8: "Lugar ideal para: empresas, bancos y finanzas — energía de poder material y realización.",
           9: "Lugar ideal para: causas sociales, ONGs y acogida — energía de compasión y conclusiones."},
    "it": {1: "Luogo ideale per: imprese e uffici commerciali — energia di iniziativa e nuovi inizi.",
           2: "Luogo ideale per: famiglie, coppie e ambienti di cura — energia di cooperazione e pace.",
           3: "Luogo ideale per: agenzie, studi e spazi sociali — energia di creatività e comunicazione.",
           4: "Luogo ideale per: cliniche, uffici e progetti a lungo termine — energia di stabilità e lavoro.",
           5: "Luogo ideale per: commercio, viaggi e trasformazioni — energia di movimento e libertà.",
           6: "Luogo ideale per: case, scuole e servizi sanitari — energia di famiglia e responsabilità.",
           7: "Luogo ideale per: consultori, biblioteche e ritiri — energia di studio e spiritualità.",
           8: "Luogo ideale per: aziende, banche e finanza — energia di potere materiale e realizzazione.",
           9: "Luogo ideale per: cause sociali, ONG e accoglienza — energia di compassione e conclusioni."},
    "fr": {1: "Lieu idéal pour : entreprises et bureaux d'affaires — énergie d'initiative et de nouveaux départs.",
           2: "Lieu idéal pour : familles, couples et lieux de soin — énergie de coopération et de paix.",
           3: "Lieu idéal pour : agences, studios et espaces sociaux — énergie de créativité et de communication.",
           4: "Lieu idéal pour : cliniques, bureaux et projets de long terme — énergie de stabilité et de travail.",
           5: "Lieu idéal pour : commerce, voyages et transformations — énergie de mouvement et de liberté.",
           6: "Lieu idéal pour : foyers, écoles et services de santé — énergie de famille et de responsabilité.",
           7: "Lieu idéal pour : cabinets, bibliothèques et retraites — énergie d'étude et de spiritualité.",
           8: "Lieu idéal pour : entreprises, banques et finance — énergie de pouvoir matériel et de réussite.",
           9: "Lieu idéal pour : causes sociales, ONG et accueil — énergie de compassion et d'accomplissement."},
    "de": {1: "Idealer Ort für: Unternehmen und Geschäftsbüros — Energie von Initiative und neuen Anfängen.",
           2: "Idealer Ort für: Familien, Paare und Pflegeräume — Energie von Zusammenarbeit und Frieden.",
           3: "Idealer Ort für: Agenturen, Studios und Soziales — Energie von Kreativität und Kommunikation.",
           4: "Idealer Ort für: Kliniken, Büros und Langzeitprojekte — Energie von Stabilität und Arbeit.",
           5: "Idealer Ort für: Handel, Reisen und Wandel — Energie von Bewegung und Freiheit.",
           6: "Idealer Ort für: Zuhause, Schulen und Gesundheitswesen — Energie von Familie und Verantwortung.",
           7: "Idealer Ort für: Praxen, Bibliotheken und Rückzugsorte — Energie von Studium und Spiritualität.",
           8: "Idealer Ort für: Firmen, Banken und Finanzen — Energie von materieller Kraft und Erfolg.",
           9: "Idealer Ort für: soziale Anliegen, NGOs und Aufnahme — Energie von Mitgefühl und Abschluss."},
    "ja": {1: "最適な用途：起業・ビジネスオフィス — 開拓と新たな始まりのエネルギー。",
           2: "最適な用途：家庭・カップル・ケアの場 — 協調と平和のエネルギー。",
           3: "最適な用途：代理店・スタジオ・社交場 — 創造とコミュニケーションのエネルギー。",
           4: "最適な用途：クリニック・事務所・長期プロジェクト — 安定と実務のエネルギー。",
           5: "最適な用途：商業・旅行・変革 — 動きと自由のエネルギー。",
           6: "最適な用途：住まい・学校・医療サービス — 家庭と責任のエネルギー。",
           7: "最適な用途：診療所・図書館・退養の場 — 学びと精神性のエネルギー。",
           8: "最適な用途：企業・銀行・金融 — 物質的力と達成のエネルギー。",
           9: "最適な用途：社会貢献・NGO・宿泊支援 — 思いやりと完成のエネルギー。"},
    "zh": {1: "理想用途：创业与商务办公室 — 开创与新起点的能量。",
           2: "理想用途：家庭、伴侣与照护场所 — 合作与和平的能量。",
           3: "理想用途：机构、工作室与社交空间 — 创造与沟通的能量。",
           4: "理想用途：诊所、办公室与长期项目 — 稳定与实干的能量。",
           5: "理想用途：商业、旅行与变革 — 行动与自由的能量。",
           6: "理想用途：住所、学校与医疗服务 — 家庭与责任的能量。",
           7: "理想用途：诊所、图书馆与静修处 — 学习与灵性的能量。",
           8: "理想用途：企业、银行与金融 — 物质力量与成就的能量。",
           9: "理想用途：公益事业、NGO与庇护 — 慈悲与圆满的能量。"},
    "ru": {1: "Идеальное место для: предприятий и бизнес-офисов — энергия инициативы и новых начинаний.",
           2: "Идеальное место для: семей, пар и мест заботы — энергия сотрудничества и мира.",
           3: "Идеальное место для: агентств, студий и социальных пространств — энергия творчества и общения.",
           4: "Идеальное место для: клиник, офисов и долгосрочных проектов — энергия стабильности и труда.",
           5: "Идеальное место для: торговли, путешествий и перемен — энергия движения и свободы.",
           6: "Идеальное место для: домов, школ и служб здоровья — энергия семьи и ответственности.",
           7: "Идеальное место для: кабинетов, библиотек и уединения — энергия учёбы и духовности.",
           8: "Идеальное место для: компаний, банков и финансов — энергия материальной силы и достижений.",
           9: "Идеальное место для: социальных целей, НКО и приюта — энергия сострадания и завершения."},
    "id": {1: "Tempat ideal untuk: usaha dan kantor bisnis — energi inisiatif dan permulaan baru.",
           2: "Tempat ideal untuk: keluarga, pasangan dan ruang perawatan — energi kerja sama dan kedamaian.",
           3: "Tempat ideal untuk: agensi, studio dan ruang sosial — energi kreativitas dan komunikasi.",
           4: "Tempat ideal untuk: klinik, kantor dan proyek jangka panjang — energi stabilitas dan kerja.",
           5: "Tempat ideal untuk: perdagangan, perjalanan dan transformasi — energi gerak dan kebebasan.",
           6: "Tempat ideal untuk: rumah, sekolah dan layanan kesehatan — energi keluarga dan tanggung jawab.",
           7: "Tempat ideal untuk: praktik, perpustakaan dan retret — energi belajar dan spiritualitas.",
           8: "Tempat ideal untuk: perusahaan, bank dan keuangan — energi kekuatan material dan prestasi.",
           9: "Tempat ideal untuk: tujuan sosial, LSM dan perlindungan — energi welas asih dan penyelesaian."},
    "tr": {1: "İdeal yer: girişimler ve iş ofisleri — inisiyatif ve yeni başlangıçlar enerjisi.",
           2: "İdeal yer: aileler, çiftler ve bakım ortamları — iş birliği ve barış enerjisi.",
           3: "İdeal yer: ajanslar, stüdyolar ve sosyal alanlar — yaratıcılık ve iletişim enerjisi.",
           4: "İdeal yer: klinikler, ofisler ve uzun vadeli projeler — istikrar ve çalışma enerjisi.",
           5: "İdeal yer: ticaret, seyahat ve dönüşümler — hareket ve özgürlük enerjisi.",
           6: "İdeal yer: yuvalar, okullar ve sağlık hizmetleri — aile ve sorumluluk enerjisi.",
           7: "İdeal yer: muayenehaneler, kütüphaneler ve inzivalar — çalışma ve maneviyat enerjisi.",
           8: "İdeal yer: şirketler, bankalar ve finans — maddi güç ve başarı enerjisi.",
           9: "İdeal yer: sosyal davalardaki kurumlar, STK'lar ve sığınaklar — şefkat ve tamamlanma enerjisi."},
    "vi": {1: "Nơi lý tưởng cho: doanh nghiệp khởi sự và văn phòng kinh doanh — năng lượng chủ động và khởi đầu mới.",
           2: "Nơi lý tưởng cho: gia đình, các cặp đôi và nơi chăm sóc — năng lượng hợp tác và hòa bình.",
           3: "Nơi lý tưởng cho: đại lý, phòng thu và không gian xã hội — năng lượng sáng tạo và giao tiếp.",
           4: "Nơi lý tưởng cho: phòng khám, văn phòng và dự án dài hạn — năng lượng ổn định và làm việc.",
           5: "Nơi lý tưởng cho: thương mại, du lịch và chuyển đổi — năng lượng vận động và tự do.",
           6: "Nơi lý tưởng cho: mái ấm, trường học và dịch vụ y tế — năng lượng gia đình và trách nhiệm.",
           7: "Nơi lý tưởng cho: phòng mạch, thư viện và nơi tĩnh dưỡng — năng lượng học tập và tâm linh.",
           8: "Nơi lý tưởng cho: công ty, ngân hàng và tài chính — năng lượng sức mạnh vật chất và thành tựu.",
           9: "Nơi lý tưởng cho: hoạt động xã hội, NGO và nơi nương tựa — năng lượng từ bi và viên mãn."},
    "he": {1: "מקום אידיאלי עבור: יזמות ומשרדי עסקים — אנרגיית יוזמה והתחלות חדשות.",
           2: "מקום אידיאלי עבור: משפחות, זוגות ומרחבי טיפול — אנרגיית שיתוף פעולה ושלום.",
           3: "מקום אידיאלי עבור: סוכנויות, אולפנים ומרחבים חברתיים — אנרגיית יצירתיות ותקשורת.",
           4: "מקום אידיאלי עבור: מרפאות, משרדים ופרויקטים ארוכי טווח — אנרגיית יציבות ועבודה.",
           5: "מקום אידיאלי עבור: מסחר, נסיעות ושינויים — אנרגיית תנועה וחופש.",
           6: "מקום אידיאלי עבור: בתים, בתי ספר ושירותי בריאות — אנרגיית משפחה ואחריות.",
           7: "מקום אידיאלי עבור: קליניקות, ספריות ומקומות נסיגה — אנרגיית לימוד ורוחניות.",
           8: "מקום אידיאלי עבור: חברות, בנקים ופיננסים — אנרגיית כוח חומרי והישגים.",
           9: "מקום אידיאלי עבור: מטרות חברתיות, ארגוני NGO ומקלט — אנרגיית חמלה והשלמה."},
    "ar": {1: "المكان المناسب لـ: المشاريع والمكاتب التجارية — طاقة المبادرة والبدايات الجديدة.",
           2: "المكان المناسب لـ: العائلات والأزواج وأماكن الرعاية — طاقة التعاون والسلام.",
           3: "المكان المناسب لـ: الوكالات والاستوديوهات والمساحات الاجتماعية — طاقة الإبداع والتواصل.",
           4: "المكان المناسب لـ: العيادات والمكاتب والمشاريع طويلة الأمد — طاقة الاستقرار والعمل.",
           5: "المكان المناسب لـ: التجارة والسفر والتحولات — طاقة الحركة والحرية.",
           6: "المكان المناسب لـ: المنازل والمدارس والخدمات الصحية — طاقة العائلة والمسؤولية.",
           7: "المكان المناسب لـ: العيادات والمكتبات وأماكن الخلوة — طاقة الدراسة والروحانية.",
           8: "المكان المناسب لـ: الشركات والبنوك والتمويل — طاقة القوة المادية والإنجاز.",
           9: "المكان المناسب لـ: القضايا الاجتماعية والمنظمات غير الحكومية والإيواء — طاقة التعاطف والإتمام."},
}

# ===== DICA DE HARMONIZAÇÃO (14 idiomas) =====
DICAS_HARMONIZACAO = {
    "pt": "💡 Dica: a energia do imóvel é fixa, mas cada ambiente pode ter a sua. Numere ou dê nome às salas e portas — cada palavra ou número vibra em uma energia que se soma à do local. Nossas ferramentas de nomenclatura (Nome para Negócio/Produto) indicam a melhor designação para cada cômodo.",
    "en": "💡 Tip: the energy of the property is fixed, but each room can have its own. Number or name the rooms and doors — every word or number carries an energy that adds to the place. Our naming tools (Business/Product Name) indicate the best designation for each room.",
    "es": "💡 Consejo: la energía del inmueble es fija, pero cada ambiente puede tener la suya. Numere o dé nombre a las salas y puertas — cada palabra o número vibra en una energía que se suma a la del lugar. Nuestras herramientas de nomenclatura (Nombre para Negocio/Producto) indican la mejor designación para cada ambiente.",
    "it": "💡 Consiglio: l'energia dell'immobile è fissa, ma ogni ambiente può avere la propria. Numerate o date un nome alle stanze e alle porte — ogni parola o numero vibra in un'energia che si somma a quella del luogo. I nostri strumenti di denominazione (Nome per Business/Prodotto) indicano la migliore designazione per ogni ambiente.",
    "fr": "💡 Conseil : l'énergie de l'immeuble est fixe, mais chaque pièce peut avoir la sienne. Numérotez ou nommez les salles et les portes — chaque mot ou nombre vibre dans une énergie qui s'ajoute à celle du lieu. Nos outils de dénomination (Nom pour Business/Produit) indiquent la meilleure désignation pour chaque pièce.",
    "de": "💡 Tipp: Die Energie des Gebäudes ist fest, aber jeder Raum kann seine eigene haben. Nummerieren oder benennen Sie Räume und Türen — jedes Wort oder jede Zahl vibriert in einer Energie, die sich zu der des Ortes addiert. Unsere Benennungstools (Name für Business/Produkt) zeigen die beste Bezeichnung für jeden Raum.",
    "ja": "💡 ヒント：建物のエネルギーは固定ですが、各部屋には固有のエネルギーを持たせられます。部屋やドアに番号や名前を付けましょう — 言葉や数字はその場所のエネルギーに加わります。命名ツール（ビジネス/製品名）が各部屋に最適な呼称を示します。",
    "zh": "💡 提示：建筑物的能量是固定的，但每个房间可以有自己的能量。为房间和门编号或命名 — 每个词语或数字都携带着能量，叠加到场所之中。我们的命名工具（商业/产品名称）会为每个房间指示最佳称谓。",
    "ru": "💡 Совет: энергия здания фиксирована, но у каждого помещения может быть своя. Пронумеруйте или назовите комнаты и двери — каждое слово или число несёт энергию, которая добавляется к энергии места. Наши инструменты нейминга (Название для бизнеса/продукта) укажут лучшее обозначение для каждого помещения.",
    "id": "💡 Tips: energi bangunan bersifat tetap, tetapi setiap ruangan dapat memiliki energi sendiri. Beri nomor atau nama pada ruangan dan pintu — setiap kata atau angka membawa energi yang menambah energi tempat. Alat penamaan kami (Nama Bisnis/Produk) menunjukkan sebutan terbaik untuk setiap ruangan.",
    "tr": "💡 İpucu: binanın enerjisi sabittir, ancak her odanın kendi enerjisi olabilir. Odalara ve kapılara numara veya isim verin — her kelime veya sayı, mekânın enerjisine eklenen bir enerji taşır. İsimlendirme araçlarımız (İş/Ürün Adı) her oda için en uygun adlandırmayı gösterir.",
    "vi": "💡 Mẹo: năng lượng của tòa nhà là cố định, nhưng mỗi phòng có thể có năng lượng riêng. Đánh số hoặc đặt tên cho các phòng và cửa — mỗi từ hoặc con số mang một năng lượng cộng vào năng lượng của nơi. Công cụ đặt tên của chúng tôi (Tên Doanh nghiệp/Sản phẩm) chỉ định cách gọi tốt nhất cho từng phòng.",
    "he": "💡 טיפ: האנרגיה של הבניין קבועה, אך לכל חדר יכולה להיות אנרגיה משלו. מספרו או תנו שם לחדרים ולדלתות — כל מילה או מספר נושאים אנרגיה שמתווספת לאנרגיית המקום. כלי השמות שלנו (שם לעסק/מוצר) מציעים את הכינוי המיטבי לכל חדר.",
    "ar": "💡 نصيحة: طاقة المبنى ثابتة، لكن لكل غرفة طاقتها الخاصة. رقّم أو سمِّ الغرف والأبواب — كل كلمة أو رقم تحمل طاقة تُضاف إلى طاقة المكان. أدوات التسمية لدينا (اسم للأعمال/المنتج) تحدد التسمية الأنسب لكل غرفة.",
}

# Dica traduzida por idioma
DICAS_HARMONIZACAO = {
    "pt": "💡 Dica: a energia do imóvel é fixa, mas cada ambiente pode ter a sua. Numere ou dê nome às salas e portas — cada palavra ou número vibra em uma energia que se soma à do local. Nossas ferramentas de nomenclatura (Nome para Negócio/Produto) indicam a melhor designação para cada cômodo.",
    "en": "💡 Tip: the energy of the property is fixed, but each room can have its own. Number or name the rooms and doors — every word or number carries an energy that adds to the place. Our naming tools (Business/Product Name) indicate the best designation for each room.",
    # ... es, it, fr, de, ja, zh, ru, he, ar, id, tr, vi
}

def analisar_imovel(dado, dado2="", dado3="", lang="pt"):
    """Recebe os 3 campos do modal. Qualquer combinação >= 1 campo gera o PDF.
    Ex.: imóvel 81, escritório 7, sala B -> 9 + 7 + 2 = 18 -> (9)"""
    partes = [_valor_alfanumerico(dado),
              _valor_alfanumerico(dado2),
              _valor_alfanumerico(dado3)]
    partes = [p for p in partes if p is not None]
    if not partes:
        return {"numero": str(dado), "energia": None, "ok": False}
    total = sum(partes)
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(d) for d in str(total))
    return {
        "numero": " + ".join(str(x) for x in [dado, dado2, dado3] if str(x).strip()),
        "partes": partes,
        "soma": sum(partes),
        "energia": total,
        "sugestao": SUGESTOES_TRAD.get(lang, SUGESTOES_TRAD["pt"]).get(total, SUGESTOES_TRAD["pt"].get(total, "")),
        "dica": DICAS_HARMONIZACAO.get(lang, DICAS_HARMONIZACAO["pt"]),
        "ok": True,
    }
