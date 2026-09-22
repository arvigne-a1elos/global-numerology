# -*- coding: utf-8 -*-
"""
referencia/semantica.py
FONTE DE VERDADE SEMANTICA - A1ELOS GLOBAL NUMEROLOGY
Camadas: ENERGIA_SEMANTICA, VIDAS_SEMANTICA, FORMAS_CORES_SEMANTICA, LP_DESC_MASTER
Uso exclusivo na EXPLICACAO dos PDFs. Compatibilidade: tabela Cissay (docs-referencias.md).
14 idiomas: pt, en, es, it, fr, de, ja, zh, ru, id, tr, vi, he, ar. Fallback para pt.
"""

# 
# CAMADA 1: ENERGIA_SEMANTICA (1 a 9)
# 

ENERGIA_SEMANTICA_PT = {
    "1": "Liderança, masculino, início de novas atividades, início de ciclo, criatividade, Deus.",
    "2": "(feito com dois número 1 [11] - Deus duas vezes - Força divina dobrada), feminino, cooperação, sensibilidade artística, criatividade cultural e social.",
    "3": "Brilho, trindade, projeção, expressividade.",
    "4": "(Em caso específico raríssimo, feito por um 22 formado por dois 11 - Deus 4 vezes - Força Divina quadriplicada), trabalho, capacidade de organização e normatização.",
    "5": "Sentimento emocional, amor sexual, paixão, desejo, atração, envolvimento.",
    "6": "Amor altruísta, amor humanitário, amor espiritual, espiritualidade, evolução espiritual.",
    "7": "Conhecimento científico, conhecimento educacional, conhecimento acadêmico, sabedoria de estudos, transmite imagem de sábio.",
    "8": "Poder, prosperidade, dinheiro, fortuna, capacidade de liderança nata, postura alfa.",
    "9": "Encerramento de atividades, final de ciclo, conclusão, resgate de vidas passadas, conhecimento do todo, peso da compreensão espiritual do mundo.",
}

ENERGIA_SEMANTICA_EN = {
    "1": "Leadership, masculine, beginning of new activities, cycle start, creativity, God.",
    "2": "(composed of two number 1s [11] - God twice - doubled divine strength), feminine, cooperation, artistic sensitivity, cultural and social creativity.",
    "3": "Radiance, trinity, projection, expressiveness.",
    "4": "(In extremely rare cases, built from a 22 formed by two 11s - God 4 times - quadrupled divine strength), labor, capacity for organization and standardization.",
    "5": "Emotional feeling, sexual love, passion, desire, attraction, deep involvement.",
    "6": "Altruistic love, humanitarian love, spiritual love, spirituality, spiritual evolution.",
    "7": "Scientific knowledge, educational insight, academic knowledge, scholarly wisdom, projects the presence of a sage.",
    "8": "Power, prosperity, wealth, fortune, innate leadership ability, alpha posture.",
    "9": "Closing of endeavors, cycle completion, resolution, retrieval of past-life wisdom, holistic knowledge, depth of spiritual comprehension.",
}

ENERGIA_SEMANTICA_ES = {
    "1": "Liderazgo, masculino, inicio de nuevas actividades, inicio de ciclo, creatividad, Dios.",
    "2": "(compuesto por dos números 1 [11] - Dios dos veces - fuerza divina duplicada), femenino, cooperación, sensibilidad artística, creatividad cultural y social.",
    "3": "Brillo, trinidad, proyección, expresividad.",
    "4": "(En casos específicos sumamente raros, formado por un 22 derivado de dos 11 - Dios 4 veces - fuerza divina cuadruplicada), trabajo, capacidad de organización y estandarización.",
    "5": "Sentimiento emocional, amor sexual, pasión, deseo, atracción, involucramiento profundo.",
    "6": "Amor altruista, amor humanitario, amor espiritual, espiritualidad, evolución espiritual.",
    "7": "Conocimiento científico, conocimiento educativo, conocimiento académico, sabiduría de estudio, proyecta la presencia de un sabio.",
    "8": "Poder, prosperidad, dinero, fortuna, capacidad de liderazgo nato, postura alfa.",
    "9": "Cierre de actividades, fin de ciclo, conclusión, rescate de vidas pasadas, conocimiento del todo, peso de la comprensión espiritual del mundo.",
}

ENERGIA_SEMANTICA_IT = {
    "1": "Leadership, maschile, inizio di nuove attività, avvio del ciclo, creatività, Dio.",
    "2": "(costituito da due numeri 1 [11] - Dio due volte - forza divina raddoppiata), femminile, cooperazione, sensibilità artistica, creatività culturale e sociale.",
    "3": "Luminosità, trinità, proiezione, espressività.",
    "4": "(In casi rari e specifici, formato da un 22 generato da due 11 - Dio 4 volte - forza divina quadruplicata), lavoro, capacità organizzativa e standardizzazione.",
    "5": "Sentimento emotivo, amore sessuale, passione, desiderio, attrazione, profondo coinvolgimento.",
    "6": "Amore altruistico, amore umanitario, amore spirituale, spiritualità, evoluzione spirituale.",
    "7": "Conoscenza scientifica, visione educativa, sapere accademico, saggezza di studio, riflette l'immagine di un saggio.",
    "8": "Potere, prosperità, denaro, fortuna, naturale attitudine al comando, postura alfa.",
    "9": "Chiusura delle attività, compimento del ciclo, conclusione, riscatto delle vite passate, cognizione universale, profondità della comprensione spirituale.",
}

ENERGIA_SEMANTICA_FR = {
    "1": "Leadership, masculin, amorce de nouvelles activités, ouverture de cycle, créativité, Dieu.",
    "2": "(composé de deux chiffres 1 [11] - Dieu deux fois - force divine redoublée), féminin, coopération, sensibilité artistique, créativité culturelle et sociale.",
    "3": "Éclat, trinité, rayonnement, expressivité.",
    "4": "(Dans des cas rarissimes, issu d'un 22 formé de deux 11 - Dieu 4 fois - puissance divine quadruplée), travail, sens aigu de l'organisation et de la rigueur normative.",
    "5": "Sentiment émotionnel, amour charnel, passion, désir, attraction, implication ardente.",
    "6": "Amour altruiste, amour humanitaire, amour spirituel, transcendance, évolution spirituelle.",
    "7": "Savoir scientifique, compétence académique, rigueur d'étude, sagesse profonde, figure d'autorité éclairée.",
    "8": "Puissance, prospérité matérielle, fortune, sens inné du commandement, posture alpha.",
    "9": "Achèvement, aboutissement de cycle, résolution karmique, omniscience intuitive, poids sacré de la lucidité spirituelle.",
}

ENERGIA_SEMANTICA_DE = {
    "1": "Führungskraft, männlich, Beginn neuer Unternehmungen, Zyklusauftakt, Schöpferkraft, Gott.",
    "2": "(gebildet aus zwei Einsern [11] - Gott zweifach - verdoppelte göttliche Kraft), weiblich, Kooperation, künstlerische Feinfühligkeit, kulturelle und soziale Kreativität.",
    "3": "Strahlkraft, Dreifaltigkeit, Weitsicht, Ausdrucksstärke.",
    "4": "(In äußerst seltenen Fällen aus einer 22 gebildet, die auf zwei 11 beruht - Gott vierfach - vervierfachte göttliche Kraft), Arbeit, Ordnungs- und Normierungskompetenz.",
    "5": "Emotionale Hingabe, leidenschaftliche Liebe, Begehren, Anziehungskraft, tiefe Verbundenheit.",
    "6": "Selbstlose Liebe, humanitäre Liebe, geistige Liebe, Spiritualität, seelische Evolution.",
    "7": "Wissenschaftliche Erkenntnis, akademische Fundierung, Weisheit durch Studium, Ausstrahlung eines Weisen.",
    "8": "Macht, Wohlstand, finanzielle Fülle, angeborene Führungsautorität, souveräne Alpha-Haltung.",
    "9": "Vollendung, Zyklusabschluss, Lösung alter Lebenslasten, ganzheitliches Erkennen, Tiefe spiritueller Weltsicht.",
}

ENERGIA_SEMANTICA_JA = {
    "1": "統率力、男性性、新事業の始動、サイクルの起点、創造力、神性。",
    "2": "（二つの1から成る［11］- 神の二重の現れ - 倍増された神聖な力）、女性性、協調、芸術的感性、文化的・社会的な創造性。",
    "3": "輝き、三位一体、自己投射、表現力。",
    "4": "（二つの11から成る22という極めて稀な構造 - 神の四重の力 - 四倍の神聖な力）、労働、組織化および規範制定の能力。",
    "5": "情緒的な情愛、情熱、欲望、引力、深いつながり。",
    "6": "利他的な愛、人道的な愛、霊的な愛、精神性、魂の進化。",
    "7": "科学的知性、教育的見識、学問的探求、思索の叡智、賢者としての風格。",
    "8": "力、繁栄、富、天賦のリーダーシップ、確固たるアルファの資質。",
    "9": "活動の終結、サイクルの完了、前世の課題の解消、全体知、霊的世界観の深奥。",
}

ENERGIA_SEMANTICA_ZH = {
    "1": "领导力、阳性力量、开辟新篇、周期起点、创造力、神性。",
    "2": "（由两个1构成［11］- 双重神性 - 倍增的神圣力量）、阴性力量、合作、艺术感知力、人文与社会创造力。",
    "3": "光芒、三位一体、投射力、卓越表现力。",
    "4": "（在极少数情况下，由两个11构成的22形成 - 神之四倍印记 - 四倍神圣力量）、实干、组织与规范构建能力。",
    "5": "情感波澜、两性深情、激情、渴望、磁性吸引、深切投入。",
    "6": "无私利他之爱、人道之爱、灵性之爱、精神觉醒、灵魂进化。",
    "7": "科学洞察、教育底蕴、学术造诣、博学睿智、具学者与智者风范。",
    "8": "权柄、丰盛繁荣、财富掌控、天生领袖、领航者气度。",
    "9": "事项终章、周期圆满、了结前世因缘、通达全知、承担灵性领悟之重任。",
}

ENERGIA_SEMANTICA_RU = {
    "1": "Лидерство, мужское начало, запуск новых направлений, старт цикла, созидание, Бог.",
    "2": "(образовано из двух единиц [11] - Бог дважды - удвоенная божественная сила), женское начало, союз, тонкое художественное восприятие, социальное творчество.",
    "3": "Сияние, триединство, проекция, яркость самовыражения.",
    "4": "(В редчайших случаях - на основе 22, сложенного из двух 11 - Бог 4 раза - учетверенная божественная мощь), труд, структурирование и системность.",
    "5": "Эмоциональная глубина, чувственная любовь, страсть, влечение, подлинная привязанность.",
    "6": "Альтруистическая любовь, гуманистическое служение, духовная любовь, трансцендентность, эволюция духа.",
    "7": "Научный поиск, академическое знание, фундаментальное образование, аналитическая мудрость, архетип истинного мудреца.",
    "8": "Власть, процветание, материальный триумф, врожденная сила управления, позиция безусловного лидера.",
    "9": "Завершение дел, финал большого цикла, искупление прошлых воплощений, целостное ведение, вес духовной мудрости.",
}

ENERGIA_SEMANTICA_ID = {
    "1": "Kepemimpinan, maskulin, permulaan aktivitas baru, awal siklus, kreativitas, Tuhan.",
    "2": "(tersusun dari dua angka 1 [11] - Kehadiran Ilahi dua kali - kekuatan ganda), feminin, kerja sama, kepekaan artistik, kreativitas budaya dan sosial.",
    "3": "Kecemerlangan, trinitas, proyeksi diri, daya ekspresi yang kuat.",
    "4": "(Dalam kasus yang sangat langka, berasal dari 22 yang dibentuk oleh dua 11 - Kehadiran Ilahi 4 kali - kekuatan berlipat empat), kerja nyata, ketertiban dan standarisasi.",
    "5": "Kedalaman emosional, cinta penuh hasrat, ketertarikan timbal balik, keterikatan batin.",
    "6": "Cinta tanpa pamrih, cinta kemanusiaan, cinta spiritual, kesadaran suci, evolusi jiwa.",
    "7": "Pengetahuan ilmiah, wawasan akademis, penguasaan teori, kebijaksanaan seorang terpelajar.",
    "8": "Kekuasaan, kemakmuran finansial, kelimpahan materi, otoritas alami, ketegasan pemimpin sejati.",
    "9": "Penuntasan tugas, penutupan siklus, pemulihan karma masa lalu, pemahaman holistik, bobot pemahaman spiritual duniawi.",
}

ENERGIA_SEMANTICA_TR = {
    "1": "Liderlik, eril güç, yeni girişimlerin başlangıcı, döngü başlangıcı, yaratıcılık, Tanrı.",
    "2": "(iki adet 1 rakamı ile oluşan [11] - İki kez Tanrı - ikiye katlanmış ilahi kudret), dişil enerji, iş birliği, sanatsal duyarlılık, kültürel ve toplumsal üretim.",
    "3": "Işıltı, üçleme, vizyon yansıtma, güçlü ifade yeteneği.",
    "4": "(Çok istisnai durumlarda, iki adet 11'den oluşan 22 ile gelen - 4 kez Tanrı - dört kat ilahi güç), emek, düzen kurma ve standartlaştırma kapasitesi.",
    "5": "Duygusal yoğunluk, tutkulu bağ, arzu, çekim, yüksek aidiyet hissi.",
    "6": "Karşılıksız sevgi, insaniyet, ruhsal sevgi, tinsellik, manevi tekamül.",
    "7": "Bilimsel bilgi, eğitsel derinlik, akademik kavrayış, araştırma bilgeliği, bilge duruşu.",
    "8": "Güç, refah, maddi kazanç, doğuştan gelen yöneticilik vasfı, alfa kararlılığı.",
    "9": "Faaliyetlerin tamamlanması, döngü sonu, geçmiş yaşamların dengelenmesi, bütünü görme, manevi kavrayışın ağırlığı.",
}

ENERGIA_SEMANTICA_VI = {
    "1": "Năng lực lãnh đạo, tính nam, khởi sự hoạt động mới, mở đầu chu kỳ, tính sáng tạo, Thượng Đế.",
    "2": "(tạo thành từ hai số 1 [11] - Thượng Đế hai lần - thần lực nhân đôi), tính nữ, cộng tác, nhạy cảm nghệ thuật, sáng tạo văn hóa và xã hội.",
    "3": "Rực rỡ, bộ ba hoàn hảo, sức lan tỏa, khả năng diễn đạt sắc sảo.",
    "4": "(Trường hợp đặc biệt hiếm có, tạo từ số 22 gồm hai số 11 - Thượng Đế 4 lần - thần lực gấp bốn), lao động thực chứng, năng lực tổ chức và quy chuẩn hóa.",
    "5": "Rung cảm sâu sắc, tình yêu nồng cháy, khát khao, sức lôi cuốn, sự gắn kết bền chặt.",
    "6": "Tình yêu vị tha, tình bác ái nhân loại, tình yêu tâm linh, sự thức tỉnh tinh thần.",
    "7": "Tri thức khoa học, học vấn uyên bác, trí tuệ nghiên cứu, cốt cách của bậc hiền triết.",
    "8": "Quyền lực, thịnh vượng tài chính, tài lộc, tố chất lãnh đạo bẩm sinh, phong thái đỉnh cao.",
    "9": "Khép lại hoạt động, hoàn tất chu kỳ, hóa giải duyên nợ tiền kiếp, quán chiếu toàn thể, trọng trách của sự thấu thị tâm linh.",
}

ENERGIA_SEMANTICA_HE = {
    "1": "מנהיגות, עוצמה גברית, פריצת פעילויות חדשות, ראשית מחזור, יצירתיות עילאית, אלוהות.",
    "2": "(מורכב מפעמיים הספרה 1 [11] - אלוהות כפולה - עוצמה שמימית מוכפלת), אנרגיה נשית, שיתוף פעולה, עידון אמנותי, יצירה תרבותית וחברתית.",
    "3": "זוהר, שילוש, הקרנה החוצה, כושר ביטוי יוצא דופן.",
    "4": "(במקרים נדירים במיוחד, נגזר מ-22 הנוצר מפעמיים 11 - אלוהות מרובעת - כוח שמימי מועצם פי ארבעה), עמל קפדני, כושר ארגון ומיסוד.",
    "5": "רגש פנימי סוער, אהבה פיזית ורומנטית, תשוקה, כוח משיכה, חיבור קרוב ועמוק.",
    "6": "אהבת הזולת ללא תנאי, אהבה הומניטרית, אהבה רוחנית, טהרה וצמיחה רוחנית מואצת.",
    "7": "ידע מדעי, השכלה מרובה, עמקות אקדמית, תבונת לימוד, מקרין נוכחות של חכם ומלומד.",
    "8": "סמכות, שגשוג כלכלי, הון חומרי, מנהיגות מולדת, מעמד ועוצמה נחרצת.",
    "9": "חתימת תהליכים, סגירת מעגל, תיקון גלגולים קודמים, ראיית השלם, משקל ההבנה הרוחנית של היקום.",
}

ENERGIA_SEMANTICA_AR = {
    "1": "القيادة، الطاقة الذكورية، انطلاق الأنشطة الجديدة، بداية الدورة الكونية، الإبداع، التجلي الإلهي.",
    "2": "(مكون من تكرار الرقم 1 [11] - القوة الإلهية المزدوجة)، الطاقة الأنثوية، التناغم والتعاون، الرهافة الفنية، الابتكار الاجتماعي والثقافي.",
    "3": "الإشراق والسطوع، الثالوث، الحضور والتأثير، فصاحة التعبير.",
    "4": "(في حالات استثنائية شديدة الندرة، ناتج عن 22 المشكل من اثنين 11 - القوة الإلهية المتضاعفة أربع مرات)، العمل البناء، التنظيم ووضع الأسس الثابتة.",
    "5": "المشاعر العاطفية الجياشة، العشق والشغف، الرغبة والانجذاب، الارتباط الوجداني الوثيق.",
    "6": "المحبة الإيثارية، الإنسانية، الحب الروحي النقي، السمو والارتقاء الروحي.",
    "7": "المعرفة العلمية، البصيرة الأكاديمية والتعليمية، حكمة البحث والتقصي، مهابة الحكماء.",
    "8": "النفوذ والقوة، الوفرة المادية، الازدهار، القيادة الفطرية الحازمة، المكانة العالية.",
    "9": "إنهاء المراحل، إتمام الدورة، استرداد حكمة الحيوات السابقة، الإدراك الكلي الشامل، ثقل الفهم الروحي العميق للكون.",
}

# 
# CAMADA 2: VIDAS_SEMANTICA (1 a 9)
# 

VIDAS_SEMANTICA_PT = {
    "1": "Primeira vida nesse plano e dimensão, veio para evoluir, um bebê espiritual, sem pecados e sem resgates, apenas aprendizado, energia masculina forte, energia yin.",
    "2": "Segunda vida nesse plano e dimensão, veio com talentos artísticos, sensibilidade a flor da pele, energia yang, energia feminina forte.",
    "3": "Terceira vida nesse plano e dimensão, veio com dualidade yin e yang equilibrada, com alta capacidade de comunicação em público, habilidade de se expressar facilmente e se projetar com brilho próprio.",
    "4": "Quarta vida nesse plano e dimensão, veio com a missão de construir, organizar, trabalhar, formalizar, montar coisas e situações, alguém que faz, não espera que alguém faça.",
    "5": "Quinta vida nesse plano e dimensão, veio com a missão de descobrir o amor, o desejo, o sexo e curtir a vida, aproveitar a vida e amar tudo e todos que lhe cercam, ser o laço emocional.",
    "6": "Sexta vida nesse plano e dimensão, veio com um dom espiritual que normalmente é acompanhado de uma extrema sensibilidade a odores, sons, sentimentos, emoções e tudo que cerca o mundo espiritual, com especial curiosidade por diversas culturas e crenças, pode até se definir por uma só, mas em geral tem dificuldade para encontrar seu caminho de crença, pois questiona muito a diferença entre religião e fé, sempre em busca de significado e Deus.",
    "7": "Sétima vida nesse plano e dimensão, veio com uma sede de conhecimento incansável, gosto pelos estudos, saber tudo sobre todas as coisas, não se dá por satisfeito com as informações que tem e por vezes busca saber sempre mais, vida de estudos e técnicas.",
    "8": "Oitava vida nesse plano e dimensão, veio para valorizar a materialidade das coisas, o poder, exercer a liderança, exercer o controle, valorizar a lógica do dinheiro em uma sociedade, o que definirá mérito ou demérito do abuso ou sabedoria desses dons diante da humanidade.",
    "9": "Nona vida nesse plano e dimensão, veio para encerrar o ciclo, resgatar pendências, última vida nesse plano e dimensão, traz consigo o conhecimento de vidas passadas e sabe das coisas sem saber como as sabe, lembrar de algo que nunca viveu e sentir que tem habilidades sem ter feito curso, apenas por dom, tem a obrigação de usar seus talentos em favor da evolução humana para sua própria evolução espiritual, arrematar o ciclo da alma.",
}

VIDAS_SEMANTICA_EN = {
    "1": "First life on this plane and dimension, came to evolve, a spiritual infant without past sins or karmic debts, focused solely on learning, strong masculine drive, internal yin force.",
    "2": "Second life on this plane and dimension, arrived with heightened artistic gifts, raw sensitivity, active yang expression, strong feminine intuition.",
    "3": "Third life on this plane and dimension, embodies a balanced harmony between yin and yang, commanding powerful public communication skills and projecting innate radiance.",
    "4": "Fourth life on this plane and dimension, charged with the mission to build, organize, labor, formalize, and manifest tangible reality; a doer who executes without waiting for others.",
    "5": "Fifth life on this plane and dimension, holds the calling to discover love, desire, intimacy, and earthly joys, radiating passion and acting as the emotional anchor for surrounding lives.",
    "6": "Sixth life on this plane and dimension, endowed with spiritual gifts and acute sensitivity to sounds, scents, and metaphysical energies, exploring varied creeds, questioning the divide between dogma and faith in pursuit of truth and God.",
    "7": "Seventh life on this plane and dimension, driven by an unquenchable thirst for knowledge, systematic research, and technical mastery, constantly seeking the underlying truth of all phenomena.",
    "8": "Eighth life on this plane and dimension, tasked with mastering material governance, commanding authority, wielding wealth wisely, where balance and ethics determine soul merit.",
    "9": "Ninth life on this plane and dimension, the ultimate closing cycle, carrying ancestral memories and untaught intuitive abilities, obligated to serve humanity's ascent to fulfill the soul's graduation.",
}

VIDAS_SEMANTICA_ES = {
    "1": "Primera vida en este plano y dimensión, vino para evolucionar, un infante espiritual sin deudas kármicas ni cargas previas, puro aprendizaje, energía masculina activa, fuerza yin interior.",
    "2": "Segunda vida en este plano y dimensión, dotada de talentos artísticos, sensibilidad a flor de piel, expresión yang, marcada fuerza femenina intuitiva.",
    "3": "Tercera vida en este plano y dimensión, equilibrio entre yin y yang, sobresaliente comunicación pública, habilidad nata de proyección y brillo propio.",
    "4": "Cuarta vida en este plano y dimensión, misión de construir, ordenar, trabajar, asentar estructuras y materializar; alguien resolutivo que actúa sin esperar a terceros.",
    "5": "Quinta vida en este plano y dimensión, vino a descubrir el amor, el deseo, la sensualidad y el gozo vital, convirtiéndose en el lazo emocional de su entorno.",
    "6": "Sexta vida en este plano y dimensión, don espiritual innato acompañado de hipersensibilidad a energías sutiles, sonidos y emociones; indaga sobre fe y religión buscando incansablemente a Dios.",
    "7": "Séptima vida en este plano y dimensión, sed incansable de conocimiento, vocación por el estudio profundo y la técnica, buscando siempre la raíz de todas las cosas.",
    "8": "Octava vida en este plano y dimensión, vino a dominar la materia, el liderazgo y las finanzas; su mérito o demérito radicará en el uso ético o abusivo del poder ante la humanidad.",
    "9": "Novena vida en este plano y dimensión, última encarnación de cierre, custodia saberes ancestrales sin estudio previo y dones innatos, con el deber moral de servir al progreso humano para culminar el ciclo del alma.",
}

VIDAS_SEMANTICA_IT = {
    "1": "Prima vita su questo piano e dimensione, venuta per evolvere, un neonato spirituale privo di debiti karmici, focalizzato sull'apprendimento puro, forte energia maschile, radice yin.",
    "2": "Seconda vita su questo piano e dimensione, dotata di talenti artistici, spiccata sensibilità emotiva, dinamica yang, intensa energia femminile interiore.",
    "3": "Terza vita su questo piano e dimensione, equilibrio perfetto tra yin e yang, grande eloquenza pubblica e naturale capacità di brillare.",
    "4": "Quarta vita su questo piano e dimensione, votata a costruire, organizzare, lavorare duramente e formalizzare strutture stabili; un realizzatore concreto e autonomo.",
    "5": "Quinta vita su questo piano e dimensione, giunta per comprendere l'amore, il desiderio, i sensi e la gioia dell'esistenza, agendo da ponte affettivo per il prossimo.",
    "6": "Sesta vita su questo piano e dimensione, dono spirituale accompagnato da ipersensibilità verso odori, suoni ed energie invisibili; esplora fedi diverse interrogandosi sul confine tra culto e fede autentica.",
    "7": "Settima vita su questo piano e dimensione, insaziabile sete di sapere, dedizione allo studio rigoroso e alle scienze esatte, costantemente proiettata verso la conoscenza superiore.",
    "8": "Ottava vita su questo piano e dimensione, chiamata a padroneggiare la materia, l'influenza e le leggi del denaro; il valore dell'anima dipenderà dall'equità con cui eserciterà il comando.",
    "9": "Nona vita su questo piano e dimensione, incarnazione conclusiva per sciogliere ogni residuo; custodisce memorie passate e talenti innati, con il sacro compito di guidare l'evoluzione altrui per compiere il ciclo della propria anima.",
}

VIDAS_SEMANTICA_FR = {
    "1": "Première vie sur ce plan, venue pour évoluer; un nouveau-né spirituel sans dettes karmiques, voué à l'apprentissage pur, énergie masculine affirmée, intériorité yin.",
    "2": "Deuxième vie sur ce plan, dotée de dons artistiques remarquables, d'une sensibilité à fleur de peau, dynamisme yang, profonde réceptivité féminine.",
    "3": "Troisième vie sur ce plan, alliance harmonieuse du yin et du yang, aisance oratoire naturelle et rayonnement personnel éclatant.",
    "4": "Quatrième vie sur ce plan, missionnée pour bâtir, ordonner, structurer et concrétiser les œuvres; une force motrice qui agit de son propre chef.",
    "5": "Cinquième vie sur ce plan, venue expérimenter l'amour, l'élan sensuel, la plénitude terrestre et devenir le catalyseur affectif de son entourage.",
    "6": "Sixième vie sur ce plan, investie d'une haute sensibilité spirituelle et perceptive; en quête d'absolu, elle sonde la frontière entre dogme et foi pure pour trouver Dieu.",
    "7": "Septième vie sur ce plan, portée par une soif intarissable d'érudition, d'analyse méthodique et de maîtrise technique des lois du monde.",
    "8": "Huitième vie sur ce plan, confrontée au pouvoir matériel, à l'autorité souveraine et aux flux financiers; son élévation dépendra de la justesse de son règne face à l'humanité.",
    "9": "Neuvième vie sur ce plan, ultime incarnation de scellement; détentrice de mémoires immémoriales et de dons spontanés, vouée au service du bien commun pour clore le cycle de l'âme.",
}

VIDAS_SEMANTICA_DE = {
    "1": "Erstes Leben auf dieser Ebene, angetreten zur Evolution; ein seelisches Neugeborenes ohne Altlasten, rein auf Erkenntnis ausgerichtet, starke männliche Urkraft, innere Yin-Prägung.",
    "2": "Zweites Leben auf dieser Ebene, ausgestattet mit künstlerischer Gabe, feinsten Sinnen, Yang-Ausdruck und tief empfundener weiblicher Kraft.",
    "3": "Drittes Leben auf dieser Ebene, getragen vom Gleichgewicht zwischen Yin und Yang, meisterhafter Rhetorik und unverwechselbarer Ausstrahlung.",
    "4": "Viertes Leben auf dieser Ebene, mit dem Auftrag zu erschaffen, zu ordnen, beharrlich zu wirken und Form zu geben; ein zupackender Geist, der eigenständig handelt.",
    "5": "Fünftes Leben auf dieser Ebene, bestimmt, Liebe, Sinnesfreude und Lebenslust zu ergründen und als emotionales Bindeglied seiner Mitwelt zu wirken.",
    "6": "Sechstes Leben auf dieser Ebene, gesegnet mit spiritueller Hellsichtigkeit und ausgeprägter Wahrnehmung feinstofflicher Ebenen; auf der Suche nach wahrer Gottesnähe jenseits reiner Konventionen.",
    "7": "Siebtes Leben auf dieser Ebene, beseelt von unstillbarem Wissensdrang, wissenschaftlicher Akribie und dem Drang, allen Erscheinungen auf den Grund zu gehen.",
    "8": "Achtes Leben auf dieser Ebene, gestellt vor die Prüfung von Macht, Besitz und gesellschaftlicher Führungsverantwortung; Reife bemisst sich am weisen Dienst an der Menschheit.",
    "9": "Neuntes Leben auf dieser Ebene, finale Vollendung und letzte irdische Existenz; ausgestattet mit unbewusstem Urwissen und Begabungen, verpflichtet zum Dienst am Aufstieg aller.",
}

VIDAS_SEMANTICA_JA = {
    "1": "この次元での第1世。カルマの負債を持たない霊的な幼児であり、純粋な学習と進化のために降臨。強固な男性的気質と内省的な陰の力を宿す。",
    "2": "この次元での第2世。際立った芸術的資質と極めて繊細な感性を帯び、積極的な陽の働きと深い女性的な直観を併せ持つ。",
    "3": "この次元での第3世。陰陽の調和が完成され、卓越した大衆伝達力と自らの輝きで人々を惹きつける力を持つ。",
    "4": "この次元での第4世。建設、体系化、着実な労働、現実の具現化を使命とし、他者を待たず自らの手で形を成す実行者。",
    "5": "この次元での第5世。愛、情熱、身体的歓喜、人生の妙味を享受し、周囲の人々を繋ぐ感情の絆となる役割を担う。",
    "6": "この次元での第6世。高度な霊的感受性を備え、微細な波動や感情に敏感。宗教と真の信仰の違いを探求し、神の真理を渇望する。",
    "7": "この次元での第7世。尽きることのない知識欲に満ち、学術的探求や専門技術の研鑽を重ね、森羅万象の真理を解き明かす生涯を送る。",
    "8": "この次元での第8世。物質界の統御、権力、富の循環を司る試練の生。その力と知恵を人類のためにどう行使するかが魂の価値を定める。",
    "9": "この次元での第9世。現世サイクルの終幕となる最後の転生。未習得の知識や過去世の英知を直感的に宿し、人類の進化に貢献して魂の旅を完結させる。",
}

VIDAS_SEMANTICA_ZH = {
    "1": "在此维度与界域的第一世，为进化而来；如同毫无因果业报的灵性婴儿，唯有学习前行，蕴含强大阳刚力量与内在潜伏之阴。",
    "2": "在此维度与界域的第二世，伴随艺术天赋与超敏知觉降临，展现外放之阳与深邃女性直觉之力。",
    "3": "在此维度与界域的第三世，阴阳交融平衡，具备超凡的公众沟通与自我光芒彰显之能。",
    "4": "在此维度与界域的第四世，肩负营造、规划、实干与建构实体的使命；雷厉风行，凡事亲力亲为。",
    "5": "在此维度与界域的第五世，旨在体验真爱、渴望、世俗之美并成为联结周遭人群的情感纽带。",
    "6": "在此维度与界域的第六世，赋予敏锐灵性与对能量波动的极度感知；在宗教与信仰之辨中追寻神性真谛。",
    "7": "在此维度与界域的第七世，怀揣永不止息的求知欲，笃志于研习与科学规律，誓求洞悉万物之理。",
    "8": "在此维度与界域的第八世，经受掌握物质权柄、统率大局及驾驭财富的考验；其功过全系于是否明智造福人间。",
    "9": "在此维度与界域的第九世，此生乃轮回周期的圆满总结；自带前世智慧与未学自通之天赋，当以奉献人类演进以完结灵魂宏愿。",
}

VIDAS_SEMANTICA_RU = {
    "1": "Первое воплощение в этом измерении: чистый эволюционный старт, духовный младенец без кармических долгов; путь познания с мощным мужским стержнем и скрытой силой инь.",
    "2": "Второе воплощение в этом измерении: тонкая художественная одаренность, обнаженная чувствительность, динамика ян и могучая женская интуиция.",
    "3": "Третье воплощение в этом измерении: гармония начал инь и ян, выдающийся ораторский дар, умение свободно транслировать собственный свет.",
    "4": "Четвертое воплощение в этом измерении: миссия созидания, упорядочивания и институционализации; неутомимый практик, созидающий реальность своими руками.",
    "5": "Пятое воплощение в этом измерении: постижение земной любви, страсти, радости бытия; роль чувственного центра для своего окружения.",
    "6": "Шестое воплощение в этом измерении: природный духовный дар и сверхчувствительность к энергиям; неустанный поиск Бога через преодоление догматов веры.",
    "7": "Седьмое воплощение в этом измерении: неутолимая жажда фундаментальных истин, академические изыскания и тяга к систематизации глубинных законов мироздания.",
    "8": "Восьмое воплощение в этом измерении: владение материей, проверка властью и большими финансовыми потоками; испытание этической зрелости перед лицом общества.",
    "9": "Девятое воплощение в этом измерении: триумфальный финал цикла, последнее рождение на этом плане; обладание врожденной памятью веков и долг служения миру ради освобождения души.",
}

VIDAS_SEMANTICA_ID = {
    "1": "Kehidupan pertama di dimensi ini, hadir murni untuk berevolusi; jiwa baru tanpa beban karma masa lalu, fokus pada pembelajaran awal, berdaya maskulin kuat dengan energi yin batin.",
    "2": "Kehidupan kedua di dimensi ini, membawa bakat kesenian, kepekaan rasa yang mendalam, pancaran yang, serta intuisi feminin yang dominan.",
    "3": "Kehidupan ketiga di dimensi ini, perpaduan seimbang antara yin dan yang, kepiawaian bertutur di depan khalayak, serta pesona batiniah yang terpancar nyata.",
    "4": "Kehidupan keempat di dimensi ini, mengemban tugas membangun, menata tatanan, bekerja nyata, dan menyusun pranata; sosok mandiri yang bertindak tanpa berpangku tangan.",
    "5": "Kehidupan kelima di dimensi ini, datang menyelami keindahan cinta, gairah, kesenangan duniawi yang sehat, dan menjadi perekat emosional bagi sesama.",
    "6": "Kehidupan keenam di dimensi ini, karunia indra spiritual dan kepekaan rasa terhadap frekuensi halus; mencari kebenaran hakiki dan Tuhan di atas sekat-sekat formal.",
    "7": "Kehidupan ketujuh di dimensi ini, dahaga keilmuan yang tak terpuaskan, dedikasi pada riset mendalam serta metode terstruktur untuk menyingkap rahasia alam.",
    "8": "Kehidupan kedelapan di dimensi ini, ujian penaklukan materi, kepemimpinan mutlak, dan tata kelola kekayaan; kehormatan sejati diukur dari keadilan dalam memimpin.",
    "9": "Kehidupan kesembilan di dimensi ini, putaran penutup siklus reinkarnasi; membawa memori bawaan purba dan talenta alami untuk dibaktikan demi pencerahan sesama.",
}

VIDAS_SEMANTICA_TR = {
    "1": "Bu boyuttaki ilk yaşam; tekamül amacıyla gelmiş, geçmiş karmik borcu bulunmayan, saf öğrenmeye odaklı, güçlü eril enerjiye ve içsel yin potansiyeline sahip bir ruhani bebek.",
    "2": "Bu boyuttaki ikinci yaşam; sanatsal yetenekler, derin duygusal hassasiyet, dışa dönük yang enerjisi ve güçlü sezgisel dişil güçle bezenmiş bir varoluş.",
    "3": "Bu boyuttaki üçüncü yaşam; dengeli yin-yang uyumu, kitleleri etkileyen konuşma yetisi ve kendine has ışığıyla dikkat çekme kabiliyeti.",
    "4": "Bu boyuttaki dördüncü yaşam; inşa etme, düzenleme, üretme ve somutlaştırma görevi; başkalarını beklemeden harekete geçen kararlı bir uygulayıcı.",
    "5": "Bu boyuttaki beşinci yaşam; sevgiyi, arzuyu ve yaşamın tüm zenginliğini tatma, çevresine duygusal bir köprü olma misyonu.",
    "6": "Bu boyuttaki altıncı yaşam; durugörü benzeri manevi yetenekler ve yüksek algı kapasitesi; din ile saf inanç arasındaki farkı sorgulayarak Tanrı'ya ulaşma arayışı.",
    "7": "Bu boyuttaki yedinci yaşam; tükenmek bilmeyen bir öğrenme tutkusu, akademik derinlik ve teknik uzmanlıkla her şeyin özünü kavrama çabası.",
    "8": "Bu boyuttaki sekizinci yaşam; maddeye hükmetme, otorite kurma ve paranın dinamiklerini yönetme dersi; gücün insanlık hayrına kullanımıyla belirlenen bir sınav.",
    "9": "Bu boyuttaki dokuzuncu yaşam; döngüyü tamamlayan son enkarnasyon; geçmiş çağların bilgisini doğuştan taşıyan ve ruhunu özgürleştirmek için insanlığa hizmetle yükümlü olan nihai aşama.",
}

VIDAS_SEMANTICA_VI = {
    "1": "Kiếp sống đầu tiên ở chiều không gian này, đến để tiến hóa; một linh hồn sơ sinh không vướng nghiệp báo, thuần khiết học hỏi, mang năng lượng nam tính mạnh mẽ và cốt cách âm.",
    "2": "Kiếp sống thứ hai ở chiều không gian này, sở hữu năng khiếu nghệ thuật, tâm hồn đa cảm, biểu hiện dương tính rõ nét cùng trực giác nữ tính sâu sắc.",
    "3": "Kiếp sống thứ ba ở chiều không gian này, âm dương cân bằng, tài hùng biện trước công chúng và hào quang tự thân cuốn hút.",
    "4": "Kiếp sống thứ tư ở chiều không gian này, sứ mệnh kiến tạo, quy hoạch, lao động bền bỉ và hiện thực hóa; một con người hành động quyết đoán.",
    "5": "Kiếp sống thứ năm ở chiều không gian này, khám phá tình yêu, đam mê, tận hưởng cuộc sống và trở thành sợi dây kết nối tình cảm cho muôn người.",
    "6": "Kiếp sống thứ sáu ở chiều không gian này, thiên bẩm tâm linh cùng sự nhạy cảm tột độ với năng lượng vi tế; trăn trở giữa giáo điều và đức tin để tìm về Thượng Đế.",
    "7": "Kiếp sống thứ bảy ở chiều không gian này, khao khát tri thức vô tận, say mê nghiên cứu học thuật và đúc rút chân lý từ các phương pháp chuẩn xác.",
    "8": "Kiếp sống thứ tám ở chiều không gian này, thử thách làm chủ vật chất, thực thi quyền lực và điều phối tài chính; phẩm hạnh được định đoạt qua sự công tâm.",
    "9": "Kiếp sống thứ chín ở chiều không gian này, hoàn tất chu kỳ sinh tử; mang theo tuệ giác tiền kiếp và tài năng bẩm sinh, gánh vác sứ mệnh nâng đỡ nhân loại để linh hồn đắc đạo.",
}

VIDAS_SEMANTICA_HE = {
    "1": "גלגול ראשון במימד זה, הגעה לצורך התפתחות בסיסית; תינוק רוחני ללא משקעי עבר או חובות קארמתיים, למידה טהורה, עוצמה גברית פעילה עם שורש יין פנימי.",
    "2": "גלגול שני במימד זה, מצויד בכישורים אמנותיים מובהקים, רגישות חושית עמוקה, ביטוי יאנג פעיל ועוצמה נשית אינטואיטיבית.",
    "3": "גלגול שלישי במימד זה, איזון מלא בין יין ליאנג, כושר ביטוי רטורי בפני קהל ויכולת הקרנה זוהרת שאינה תלויה בדבר.",
    "4": "גלגול רביעי במימד זה, שליחות של בנייה מעשית, ארגון, עבודה מאומצת ומיסוד מבנים חברתיים; אישיות יוזמת הפועלת ללא דיחוי.",
    "5": "גלגול חמישי במימד זה, ייעוד של גילוי האהבה, התשוקה ושמחת החיים הארצית, תוך היותו העוגן והדבק הרגשי של סביבתו.",
    "6": "גלגול שישי במימד זה, חסד רוחני מולד ורגישות קיצונית לתדרים, צלילים ורגשות; חיפוש מתמיד אחר ההבדל בין דת ממוסדת לאמונה חיה באל.",
    "7": "גלגול שביעי במימד זה, צימאון בלתי נדלה לידע עיוני, חקר שיטתי של חוקי היקום וחתירה מתמדת למומחיות מדעית ותרבותית.",
    "8": "גלגול שמיני במימד זה, התמודדות עם עוצמה חומרית, הנהגת ציבור ושליטה בממון; מבחן מוסרי שבו החוכמה והיושרה מול החברה יקבעו את זכויות הנשמה.",
    "9": "גלגול תשיעי במימד זה, חתימת מעגל הגלגולים הארצי; נשיאת זיכרון קדום ויכולות מולדות ללא צורך בלמידה מוקדמת, ומחויבות לשרת את האנושות כולה לחתימת מסע הנשמה.",
}

VIDAS_SEMANTICA_AR = {
    "1": "التجسد الأول في هذا البعد الكوني، جاء ليتطور كوليد روحي دون خطايا سابقة أو أثقال كارمية، مكرس للتعلم بطاقة ذكورية فاعلة وقوة يين كامنة.",
    "2": "التجسد الثاني في هذا البعد، أتى بمواهب فنية ورهافة حس مفرطة، متسلحاً بديناميكية يانغ وحدس أنثوي عميق.",
    "3": "التجسد الثالث في هذا البعد، توازن ناضج بين طاقتي الين واليانغ، مصحوب بفصاحة وبلاغة للتخاطب مع الجماهير وسطوع كاريزمي طبيعي.",
    "4": "التجسد الرابع في هذا البعد، مهمته التشييد، النظام، البذل العملي، وترسيخ الاستقرار؛ صانع للأحداث لا ينتظر مساعدة من أحد.",
    "5": "التجسد الخامس في هذا البعد، رسالته عيش مشاعر العاطفة والشغف وتذوق ملذات الحياة المشروعة، ليكون رابط المحبة في محيطه.",
    "6": "التجسد السادس في هذا البعد، يمتلك هبة روحية موروثة وإحساساً فائقاً بالطاقات الخفية؛ يبحث في أسرار الإيمان الحقيقي في سبيله نحو الله.",
    "7": "التجسد السابع في هذا البعد، شغف علمي لا ينضب بالدراسة الأكاديمية والتقنية، وسعي دؤوب للإحاطة التامة بجوهر العلوم والأشياء.",
    "8": "التجسد الثامن في هذا البعد، اختبار للسيادة المادية، القيادة المطلقة، وإدارة الثروات؛ وتتحدد قيمته وفق عدله أو جوره في استخدام النفوذ بين البشر.",
    "9": "التجسد التاسع في هذا البعد، ختام دورة الحياة التجسدية؛ يحمل المعرفة اللدنية والقدرات الفطرية، وعليه توظيف مواهبه لخدمة رقي الإنسانية لتتويج رحلة الروح.",
}

# 
# CAMADA 3: FORMAS_CORES_SEMANTICA (1 a 9)
# 

FORMAS_CORES_PT = {
    "1": {
        "forma": "Ponto: um ponto, o começo de tudo",
        "cor": "Branco, a mistura de todas as cores do arco-íris; a pureza do branco é a fusão de todas as cores, e como a luz contém todas elas, contém todas as energias",
        "texto": "O início é uma folha em branco e um ponto de partida.",
    },
    "2": {
        "forma": "Reta: o caminho entre dois pontos, nem sempre o mais curto; em uma superfície plana sim, mas em uma superfície curva não; aprender qual caminho tomar para ligar os dois pontos é o aprendizado principal",
        "cor": "Preto, o contraponto ao branco; na dualidade das cores, como o xadrez, preto e branco, vermelho e azul, a cor certa é o preto, pois é o contraponto ao branco; a cor mais limpa é a que não aceita nenhuma delas e se protege de todas as demais energias",
        "texto": "A dualidade das cores marca o caminho; escolher o contraponto é o aprendizado.",
    },
    "3": {
        "forma": "Triângulo: símbolo da perfeição; pai, filho e espírito santo; em diversas crenças pelo mundo e na própria matemática pitagórica, o símbolo da compreensão da dualidade humana com Deus",
        "cor": "Amarelo, a cor do brilho intenso",
        "texto": "A luz que melhor define essa energia é a do brilho intenso.",
    },
    "4": {
        "forma": "Quadrado: ordem no caos, trabalho dignificante, obra, legado; o símbolo da maturidade, do equilíbrio, da base sólida que tudo sustenta, ângulos retos e firmes",
        "cor": "Azul, a cor que transmite segurança e verdade",
        "texto": "A base sólida sustenta a obra.",
    },
    "5": {
        "forma": "Pentagrama, pentágono: cinco lados, uma figura de poder sensual e de domínio físico",
        "cor": "Rosa e vermelho, o sangue, passional, intenso, vivo",
        "texto": "Energia viva, intensa e apaixonada.",
    },
    "6": {
        "forma": "Hexágono, hexagrama: seis lados",
        "cor": "Laranja, bege e marrom, o espectro das cores dos mestres, das evoluções espirituais e da magia",
        "texto": "Compreensão do bem e do mal e sabedoria para escolher agir corretamente.",
    },
    "7": {
        "forma": "Heptágono (uma pirâmide também serve): sete lados, base quatro e lado três; símbolo da perfeição, do conhecimento profundo, espiritual e humano, da maturidade da alma, do compromisso e da responsabilidade que acompanham tanto saber",
        "cor": "Verde, a cor da cura",
        "texto": "O saber traz maturidade e responsabilidade.",
    },
    "8": {
        "forma": "Octógono: oito lados",
        "cor": "Dourada, prateada e bronzeada, o poder tem brilho nas cores",
        "texto": "Com grandes poderes vêm grandes obrigações.",
    },
    "9": {
        "forma": "Eneágono: nove lados",
        "cor": "Lilás, roxo e violeta, as cores da transmutação, da evolução completa, da transformação do ser",
        "texto": "A transformação completa do ser.",
    },
}

FORMAS_CORES_EN = {
    "1": {
        "forma": "Point: a single point, the origin of all existence",
        "cor": "White, the synthesis of all spectrum hues; its purity mirrors the fusion of all cosmic light and vibratory frequencies",
        "texto": "The beginning is an unblemished canvas and a singular point of departure.",
    },
    "2": {
        "forma": "Line: the trajectory between two points, not always linear across non-planar realities; choosing the true trajectory constitutes the primary lesson",
        "cor": "Black, the eternal counterpoint to white; resisting external influx, it shields against discordant vibrations",
        "texto": "Chromatic duality guides the path; discerning the counterpoint is the ultimate lesson.",
    },
    "3": {
        "forma": "Triangle: supreme emblem of divine perfection, the trinity across world traditions, unifying human duality with the Creator",
        "cor": "Yellow, radiant brilliance and mental illumination",
        "texto": "The luminosity defining this vibration is that of pure brilliance.",
    },
    "4": {
        "forma": "Square: structural order within chaos, enduring legacy, equilibrium, the unyielding bedrock of right angles",
        "cor": "Blue, embodying truth, stability, and enduring security",
        "texto": "An unshakeable foundation sustains the great work.",
    },
    "5": {
        "forma": "Pentagram/Pentagon: fivefold geometry, an insignia of sensual potency, bodily sovereignty, and dynamic vitality",
        "cor": "Rose and red, primal blood, passionate intensity, and vital pulse",
        "texto": "Living, fervent, and intensely magnetic energy.",
    },
    "6": {
        "forma": "Hexagon/Hexagram: sixfold balance uniting micro and macrocosm",
        "cor": "Orange, beige, and earthy brown, the sacred palette of adept masters, spiritual evolution, and natural magic",
        "texto": "Discerning light from darkness and mastering righteous action through wisdom.",
    },
    "7": {
        "forma": "Heptagon or Pyramid: sevenfold manifestation, reconciling base four with triangle three; depth of soul maturity and ethical gravitas",
        "cor": "Green, vibrational restoration and holistic healing",
        "texto": "Profound wisdom commands maturity and sacred accountability.",
    },
    "8": {
        "forma": "Octagon: eightfold symmetry of material and cosmic authority",
        "cor": "Gold, silver, and burnished bronze, the radiant hues of sovereignty",
        "texto": "Immense power entails immense accountability.",
    },
    "9": {
        "forma": "Enneagon: ninefold closure, the sacred threshold of completion",
        "cor": "Lilac, amethyst, and deep violet, the frequencies of spiritual transmutation and soul alchemy",
        "texto": "The holistic and definitive transformation of being.",
    },
}

FORMAS_CORES_ES = {
    "1": {
        "forma": "Punto: un punto, el origen de toda manifestación",
        "cor": "Blanco, la amalgama de los colores del espectro; pureza luminosa que alberga todas las energías posibles",
        "texto": "El inicio es un lienzo en blanco y un punto de partida.",
    },
    "2": {
        "forma": "Recta: la senda entre dos puntos, variable en planos dimensionales curvos; discernir el rumbo correcto es el aprendizaje primordial",
        "cor": "Negro, el contrapunto absoluto al blanco; el manto que resguarda la esencia no aceptando intromisiones vibratorias",
        "texto": "La dualidad cromática traza el camino; elegir el contrapunto es el verdadero aprendizaje.",
    },
    "3": {
        "forma": "Triángulo: símbolo de perfección y trinidad, conjunción pitagórica entre la dualidad humana y la divinidad",
        "cor": "Amarillo, el resplandor de la luminosidad intensa",
        "texto": "La luz que mejor encarna esta energía es la del brillo supremo.",
    },
    "4": {
        "forma": "Cuadrado: orden frente al caos, obra dignificante, base firme de ángulos rectos que sustentan la madurez",
        "cor": "Azul, el tono de la certeza, la seguridad y la verdad inmutable",
        "texto": "La base sólida sustenta la obra perdurable.",
    },
    "5": {
        "forma": "Pentagrama, pentágono: cinco lados, arquetipo de poder sensorial y dominio en el plano físico",
        "cor": "Rosa y rojo carmesí, la sangre, lo pasional, lo vivo y vehemente",
        "texto": "Energía viva, ardiente y apasionada.",
    },
    "6": {
        "forma": "Hexágono, hexagrama: seis lados de equilibrio armónico",
        "cor": "Naranja, ocre y marrón, la gama de los grandes maestros, la ascensión espiritual y la magia sabia",
        "texto": "Comprensión del bien y del mal y discernimiento para obrar con justicia.",
    },
    "7": {
        "forma": "Heptágono (o pirámide): siete lados, base cuatro y cúspide tres; madurez del alma y compromiso sagrado",
        "cor": "Verde, la tonalidad de la regeneración y la cura",
        "texto": "El saber profundo exige madurez y responsabilidad.",
    },
    "8": {
        "forma": "Octógono: ocho lados que rigen el poder y la justicia cósmica",
        "cor": "Dorado, plateado y bronce, el destello resplandeciente del triunfo",
        "texto": "A grandes poderes corresponden grandes obligaciones.",
    },
    "9": {
        "forma": "Eneágono: nueve lados que sellan el ciclo evolutivo",
        "cor": "Lila, púrpura y violeta, las frecuencias de la transmutación y elevación espiritual",
        "texto": "La transformación completa del ser.",
    },
}

FORMAS_CORES_IT = {
    "1": {
        "forma": "Punto: l'origine primordiale, il principio assoluto",
        "cor": "Bianco, la convergenza di ogni raggio visibile; la sintesi di tutte le energie cosmiche",
        "texto": "Il principio è un foglio immacolato e un punto di partenza.",
    },
    "2": {
        "forma": "Retta: il legame tra due punti nello spazio; comprendere la giusta rotta costituisce l'insegnamento cardine",
        "cor": "Nero, la naturale antitesi del bianco; scudo impassibile che non assorbe turbamenti esterni",
        "texto": "La dualità cromatica guida il percorso; abbracciare il contrappunto è la vera conquista.",
    },
    "3": {
        "forma": "Triangolo: la perfezione trinitaria, l'accordo pitagorico fra l'uomo e l'Eterno",
        "cor": "Giallo, l'irradiazione della mente lucida",
        "texto": "La luce che contraddistingue questa forza è quella del puro splendore.",
    },
    "4": {
        "forma": "Quadrato: l'ordine nel disordine, fondamento incrollabile, rettitudine e stabilità d'opera",
        "cor": "Blu, fedeltà, autenticità e fermezza interiore",
        "texto": "La solida base sostiene l'opera imperitura.",
    },
    "5": {
        "forma": "Pentagono/Pentagramma: struttura a cinque punte, vigore sensoriale e sovranità materiale",
        "cor": "Rosa e rosso, sangue vitale, slancio passionale e magnetico",
        "texto": "Energia vibrante, intensa e carica di passione.",
    },
    "6": {
        "forma": "Esagono, esagramma: architettura sacra a sei lati",
        "cor": "Arancio, ambra e bruno, cromie dei maestri d'Oriente e d'Occidente, sapienza e alchimia",
        "texto": "Intendere la luce e l'ombra e operare con retta saggezza.",
    },
    "7": {
        "forma": "Ettagono o piramide: sintesi del quattro con il tre, coronamento della consapevolezza interiore",
        "cor": "Verde, frequenza di armonia e rinnovamento vitale",
        "texto": "Il sapere profondo esige gravità e sacra responsabilità.",
    },
    "8": {
        "forma": "Ottagono: geometria di dominio, equilibrio tra terra e cielo",
        "cor": "Oro, argento e bronzo lucente, la brillantezza dell'autorità",
        "texto": "Da grandi poteri derivano grandi e solenni doveri.",
    },
    "9": {
        "forma": "Enneagono: nove vertici di consumazione finale",
        "cor": "Lilla, porpora e indaco, il fuoco trasmutativo dell'essenza",
        "texto": "La totale trasmutazione dell'essere.",
    },
}

FORMAS_CORES_FR = {
    "1": {
        "forma": "Point: l'étincelle première, matrice de tout commencement",
        "cor": "Blanc, fusion intégrale des longueurs d'onde; source primordiale de toutes les fréquences",
        "texto": "L'aube est une page blanche et un point de jaillissement.",
    },
    "2": {
        "forma": "Ligne droite: lien tendu entre deux pôles; discerner la voie juste demeure l'initiation fondamentale",
        "cor": "Noir, contrepoint radical de la lumière, sanctuaire qui préserve l'énergie de toute dispersion",
        "texto": "La polarité des teintes guide le voyage; choisir le contrepoint est la leçon suprême.",
    },
    "3": {
        "forma": "Triangle: sceau de la perfection ternaire, harmonie de l'humain et du divin",
        "cor": "Jaune solaire, incandescence de l'esprit",
        "texto": "L'énergie s'illustre par l'éclat flamboyant de la lumière.",
    },
    "4": {
        "forma": "Carré: triomphe de la méthode, pérennité du socle, rigueur rassurante des angles parfaits",
        "cor": "Bleu profond, sceau de la loyauté, de la clarté et de la paix pérenne",
        "texto": "Une assise immuable porte les plus grandes réalisations.",
    },
    "5": {
        "forma": "Pentagramme, pentagone: géométrie à cinq branches, puissance de l'instinct et affirmation vitale",
        "cor": "Rose et rouge pourpre, sève du sang, ferveur et impulsion amoureuse",
        "texto": "Une pulsation ardente, magnétique et insoumise.",
    },
    "6": {
        "forma": "Hexagone, hexagramme: six pans unifiant les dimensions supérieures",
        "cor": "Orange, ocre et terre cuite, vibrations des initiateurs et des mystères sacrés",
        "texto": "Comprendre les dualités pour agir selon la droiture éclairée.",
    },
    "7": {
        "forma": "Heptagone (ou pyramide): sept faces unissant la matière (4) et l'esprit (3); maturité initiatique",
        "cor": "Vert émeraude, onde de guérison et d'alignement",
        "texto": "L'élévation de la pensée impose rigueur et gravité morale.",
    },
    "8": {
        "forma": "Octogone: huit côtés canalisant le rayonnement de la souveraineté",
        "cor": "Or, argent et bronze noble, le reflet du triomphe légitime",
        "texto": "Aux plus hautes charges incombent les plus vastes devoirs.",
    },
    "9": {
        "forma": "Ennéagone: les neuf seuils de l'accomplissement suprême",
        "cor": "Lilas, améthyste et violet sacerdotal, vecteurs de la transmutation alchimique",
        "texto": "L'élévation intégrale et l'apothéose de l'être.",
    },
}

FORMAS_CORES_DE = {
    "1": {
        "forma": "Punkt: der Urpunkt, Ursprung jeglicher Existenz",
        "cor": "Weiß, die ungeteilte Synthese aller Spektralfarben, Quell aller kosmischen Schwingung",
        "texto": "Der Anfang ist ein unbeschriebenes Blatt und ein fester Ausgangspunkt.",
    },
    "2": {
        "forma": "Gerade: die Verbindung zweier Pole; das Verstehen des wahren Weges ist die Kernaufgabe",
        "cor": "Schwarz, der unerschütterliche Gegenpol; schützende Tiefe, die fremde Einflüsse abwehrt",
        "texto": "Die Dualität weist den Pfad; das Erkennen des Gegenpols ist die eigentliche Reifung.",
    },
    "3": {
        "forma": "Dreieck: Dreifaltigkeit und Sinnbild vollendeter Ordnung des Geistes mit der Schöpfung",
        "cor": "Gelb, das intensive Leuchten schöpferischer Klarheit",
        "texto": "Das Leuchten reinen Glanzes definiert diese Schwingung.",
    },
    "4": {
        "forma": "Quadrat: Meisterschaft über das Chaos, Festigkeit der Grundmauern, unverrückbares Fundament",
        "cor": "Blau, die Farbe unerschütterlicher Wahrheit und Geborgenheit",
        "texto": "Ein starkes Fundament trägt das bleibende Werk.",
    },
    "5": {
        "forma": "Pentagramm, Fünfeck: fünffache Form, Zeichen physischer Vitalität und sinnlicher Willenskraft",
        "cor": "Rosa und feuriges Rot, das Blut des Lebens, leidenschaftlich und pulsierend",
        "texto": "Lebendige, fordernde und hingebungsvolle Kraft.",
    },
    "6": {
        "forma": "Sechseck, Hexagramm: vollendete sechseckige Symmetrie",
        "cor": "Orange, Ocker und Erdbraun, das Schwingungsfeld geistiger Lehrer und seelischer Transformation",
        "texto": "Erkenntnis von Gut und Böse und die Weisheit zu aufrechtem Handeln.",
    },
    "7": {
        "forma": "Heptagon oder Pyramide: Siebeneck, Basis vier vereint mit Drei; Reife des Geistes",
        "cor": "Grün, die Farbe tiefgreifender Heilung und Erneuerung",
        "texto": "Großes Wissen gebietet unbedingte Verantwortung.",
    },
    "8": {
        "forma": "Achteck: acht Kanten als Tor zwischen irdischer Macht und höherem Gesetz",
        "cor": "Gold, Silber und edle Bronze, Glanz wahrer Regentschaft",
        "texto": "Große Vollmacht verlangt uneingeschränkte Pflichterfüllung.",
    },
    "9": {
        "forma": "Enneagon: neun Seiten als Abschluss der irdischen Skala",
        "cor": "Lila, Purpur und Violett, Schwingungen der Transmutation und Vollendung",
        "texto": "Die ganzheitliche Wandlung des gesamten Seins.",
    },
}

FORMAS_CORES_JA = {
    "1": {
        "forma": "点（ポイント）：すべての事象の源点、原初の始まり",
        "cor": "白、虹のすべての色彩が融合した光。全周波数を包含する純粋なエネルギーの根源",
        "texto": "始まりとは、白紙の画布であり、唯一無二の出発点である。",
    },
    "2": {
        "forma": "直線：二点を結ぶ軌跡。曲面においては最短とは限らず、選ぶべき道を見極めることこそが主たる学び",
        "cor": "黒、白に対する絶対的な対照。外的な雑音を拒絶し、固有の純度を守護する遮蔽の力",
        "texto": "色彩の二元性が道を示し、対極を見定めることこそが生の修練となる。",
    },
    "3": {
        "forma": "三角形：完全性の象徴。三位一体、人間と神性の統合を表す幾何学",
        "cor": "黄色、知性と生命力が放つ強烈な輝き",
        "texto": "この力を最も力強く物語るのは、比類なき光輝である。",
    },
    "4": {
        "forma": "四角形：混沌を統べる秩序、揺るぎなき基盤、尊厳ある労働の結晶",
        "cor": "青、真理、確信、不変の安全を伝える色彩",
        "texto": "堅牢なる土台が、永続する事業を支える。",
    },
    "5": {
        "forma": "五芒星・五角形：五辺の幾何学、官能的な活力と物質次元における支配力",
        "cor": "ピンクと赤、血の脈動、情熱、躍動感あふれる生命の炎",
        "texto": "生気に満ち、激しく熱烈なエネルギー。",
    },
    "6": {
        "forma": "六角形・六芒星：調和と超越を象徴する六つの頂点",
        "cor": "橙、ベージュ、褐色。精神的指導者、魂の進化、秘儀を司る大地の色",
        "texto": "善悪を弁別し、正道を選択する深き智慧。",
    },
    "7": {
        "forma": "七角形（またはピラミッド）：四角の基礎と三角の頂が織りなす七つの面。魂の円熟と責任",
        "cor": "緑、全人的な治癒と再生の色彩",
        "texto": "高邁なる知識は、魂の円熟と厳格な責任を伴う。",
    },
    "8": {
        "forma": "八角形：権力、統治、高次の正義を司る八辺の構造",
        "cor": "黄金、銀、青銅。力ある者が放つ至高の輝き",
        "texto": "大いなる力には、大いなる義務が伴う。",
    },
    "9": {
        "forma": "九角形：進化の円環を完結させる九つの境界",
        "cor": "薄紫、紫、バイオレット。完全な変容と昇華をもたらす色彩",
        "texto": "存在の完全なる変容と成就。",
    },
}

FORMAS_CORES_ZH = {
    "1": {
        "forma": "原点：万物的起点，造化的基石",
        "cor": "白色，融合光谱中的万千色彩；光的纯净蕴含宇宙一切初始能量",
        "texto": "开端是一张洁白无瑕的画布，也是不可动摇的起点。",
    },
    "2": {
        "forma": "直线：两点之间的连线；在弯曲的维度中探寻真正的轨道，乃是首要的生命功课",
        "cor": "黑色，白色的绝对对立与守护者；不容杂质侵蚀，屏蔽外界干扰的清明屏障",
        "texto": "色彩的二元性标示前路，洞察对立之统一是最高智慧。",
    },
    "3": {
        "forma": "三角形：完美三位一体的徽记，统合人性与神圣维度的毕达哥拉斯法则",
        "cor": "黄色，代表精神启迪的炽烈光华",
        "texto": "最能彰显该能量的特质，莫过于炽烈璀璨的光芒。",
    },
    "4": {
        "forma": "正方形：混沌之中的严整秩序，承载传世基业的稳固直角基底",
        "cor": "蓝色，传递坚定不移的安全、真实与信义",
        "texto": "唯有坚实稳固的基石，方能承载传世基业。",
    },
    "5": {
        "forma": "五角星/五边形：五行律动之形，感官力量与生命活力的最高体现",
        "cor": "粉色与鲜红，血液奔涌，炽热激情，生生不息",
        "texto": "充满勃勃生机、深沉炽烈的磁性力量。",
    },
    "6": {
        "forma": "六边形/六角星：微观与宏观交汇的六方和合之美",
        "cor": "橙色、米色与赭石色，大师的灵性气场、精神升华与厚重智慧之色",
        "texto": "明辨是非善恶，以超然智慧躬行正道。",
    },
    "7": {
        "forma": "七边形（亦或金字塔形）：基四合顶三的七维结构；昭示灵魂成熟与崇高责任",
        "cor": "绿色，万物复苏与身心治愈之光",
        "texto": "渊博的学识必然伴随灵魂的成熟与沉甸甸的责任。",
    },
    "8": {
        "forma": "八边形：平衡乾坤两界的威仪之相",
        "cor": "金、银与古铜，世俗与精神领袖的灿烂华光",
        "texto": "掌控巨大权力者，必当承载宏大责任。",
    },
    "9": {
        "forma": "九边形：闭环圆满的九维界碑",
        "cor": "浅紫、正紫与深紫罗兰，灵魂彻底蜕变升华与涅槃之光",
        "texto": "生命本质的全面蜕变与终极飞跃。",
    },
}

FORMAS_CORES_RU = {
    "1": {
        "forma": "Точка: первопричина, исходный пункт всего сущего",
        "cor": "Белый, слияние всех цветов радуги; чистота, аккумулирующая всю мощь видимого и невидимого спектра",
        "texto": "Начало есть чистый лист и единственная отправная точка.",
    },
    "2": {
        "forma": "Прямая: путь между двумя точками; поиск верного направления в искривленном пространстве – главный урок",
        "cor": "Черный, вечный противовес белому; глубинная броня, отвергающая сторонние помехи и сохраняющая истинную суть",
        "texto": "Цветовой дуализм указывает направление; постижение противоположности есть ключ к мудрости.",
    },
    "3": {
        "forma": "Треугольник: триединство совершенства, объединяющее человеческую двойственность с Творцом",
        "cor": "Желтый, интенсивное сияние ментальной ясности",
        "texto": "Свет, который точнее всего раскрывает эту силу, – сияние высшей чистоты.",
    },
    "4": {
        "forma": "Квадрат: структурированный порядок из хаоса, надежная основа, прямой угол непоколебимой прочности",
        "cor": "Синий, воплощение спокойствия, истины и незыблемой безопасности",
        "texto": "Прочный фундамент держит великое творение.",
    },
    "5": {
        "forma": "Пентаграмма, пятиугольник: пятиконечная фигура витальной силы и власти над материей",
        "cor": "Розовый и алый, цвет живой крови, страсти, неукротимого желания",
        "texto": "Живая, страстная и всепоглощающая энергия.",
    },
    "6": {
        "forma": "Гексагон, гексаграмма: гармония шести граней макрокосма",
        "cor": "Оранжевый, бежевый и теплый коричневый; спектр духовных наставников, эволюции сознания и древней мудрости",
        "texto": "Осознание добра и зла и зрелость праведного выбора.",
    },
    "7": {
        "forma": "Гептагон (или пирамида): семь граней, соединяющих земной квадрат и триединый дух; зрелость души",
        "cor": "Зеленый, вибрация исцеления и баланса",
        "texto": "Фундаментальное знание рождает зрелость и высочайшую ответственность.",
    },
    "8": {
        "forma": "Октагон: восьмигранный контур верховной власти и управления",
        "cor": "Золотой, серебряный и бронзовый, сияние неподдельного авторитета",
        "texto": "Великая сила налагает великие обязательства.",
    },
    "9": {
        "forma": "Эннеагон: девять граней финального триумфа",
        "cor": "Лиловый, пурпурный и фиолетовый; пламя алхимической трансмутации духа",
        "texto": "Абсолютная и совершенная трансформация естества.",
    },
}

FORMAS_CORES_ID = {
    "1": {
        "forma": "Titik: satu titik tunggal, muasal segala sesuatu",
        "cor": "Putih, perpaduan seluruh spektrum cahaya; kemurnian total yang mengandung segala potensi energi",
        "texto": "Awal mula adalah selembar kertas putih dan sebuah titik tolak.",
    },
    "2": {
        "forma": "Garis lurus: lintasan antara dua titik; menentukan jalan yang tepat merupakan intisari pembelajaran utama",
        "cor": "Hitam, lawan sejati dari putih; perlindungan murni yang menolak intervensi luar untuk menjaga kemurnian",
        "texto": "Dualitas warna menandai lintasan; mengenali sang penyeimbang adalah hikmah sejati.",
    },
    "3": {
        "forma": "Segitiga: lambang kesempurnaan trinitas, bertemunya sifat insani dan keilahian",
        "cor": "Kuning, pancaran kemilau yang cemerlang",
        "texto": "Cahaya yang paling mencerminkan daya ini adalah kilau yang benderang.",
    },
    "4": {
        "forma": "Persegi: keteraturan dalam kekacauan, pilar penopang ketahanan yang kokoh",
        "cor": "Biru, pembawa rasa aman, kesungguhan, dan keteguhan",
        "texto": "Landasan yang kokoh menopang karya yang abadi.",
    },
    "5": {
        "forma": "Pentagram/Pentagon: bangun lima sisi, perlambang daya ragawi dan daya tarik pesona tubuh",
        "cor": "Merah muda dan merah darah, penuh gelora hidup dan gairah asmara",
        "texto": "Energi yang hidup, membara, dan memikat.",
    },
    "6": {
        "forma": "Heksagon/Heksagram: keseimbangan enam arah mata angin batin",
        "cor": "Oranye, krem, dan cokelat tanah; warna para guru bijak, kebangkitan batin, dan keluhuran budi",
        "texto": "Paham akan baik dan buruk serta memiliki kearifan untuk bertindak adil.",
    },
    "7": {
        "forma": "Heptagon (atau piramida): tujuh sisi, perpaduan alas empat dan puncak tiga; kematangan spiritual",
        "cor": "Hijau, warna keselarasan dan pemulihan jiwa",
        "texto": "Tingginya ilmu menuntut kedewasaan dan tanggung jawab moral yang luhur.",
    },
    "8": {
        "forma": "Oktagon: delapan sisi kekuasaan dan kedaulatan kepemimpinan",
        "cor": "Emas, perak, dan perunggu; pendaran wibawa sejati",
        "texto": "Bersama kekuasaan yang besar, terpikul tanggung jawab yang agung.",
    },
    "9": {
        "forma": "Eneagon: sembilan sudut yang menutup lingkaran kesempurnaan",
        "cor": "Lilak, ungu, dan lembayung; warna peralihan wujud jiwa dan transmutasi batin",
        "texto": "Transformasi menyeluruh atas eksistensi diri.",
    },
}

FORMAS_CORES_TR = {
    "1": {
        "forma": "Nokta: tek bir nokta, her şeyin başlangıcı",
        "cor": "Beyaz, tüm renk tayfının kusursuz birleşimi; tüm titreşimleri bağrında taşıyan saf ışık",
        "texto": "Başlangıç, tertemiz beyaz bir sayfa ve bir çıkış noktasıdır.",
    },
    "2": {
        "forma": "Doğru: iki nokta arasındaki hat; en doğru güzergahı keşfetmek temel hayat dersidir",
        "cor": "Siyah, beyazın kusursuz zıddı; dış tesirleri keserek öz enerjiyi muhafaza eden zırh",
        "texto": "Renklerin kutupsallığı yolu çizer; karşıtını doğru seçmek erdemdir.",
    },
    "3": {
        "forma": "Üçgen: mükemmelliğin ve üçlü birliğin simgesi; insan ile Yaratıcı arasındaki ahenk",
        "cor": "Sarı, yüksek aklın ve canlılığın parlak ışığı",
        "texto": "Bu enerjiyi en iyi tanımlayan ışık, göz alıcı bir parlaklıktır.",
    },
    "4": {
        "forma": "Kare: kaosun içindeki nizam, sağlam temel, dik açıların getirdiği güven ve süreklilik",
        "cor": "Mavi, mutlak güveni, doğruluğu ve huzuru fısıldayan renk",
        "texto": "Sağlam bir zemin, kalıcı bir eseri ayakta tutar.",
    },
    "5": {
        "forma": "Pentagram/Beşgen: beş kenarlı biçim, fiziksel kudretin ve duyusal cazibenin ifadesi",
        "cor": "Pembe ve kan kırmızısı; tutkulu, coşkun, son derece canlı",
        "texto": "Canlı, yakıcı ve derin bir tutku enerjisi.",
    },
    "6": {
        "forma": "Heksagon/Heksagram: evrensel ahengin altı köşeli geometrisi",
        "cor": "Turuncu, bej ve toprak kahvesi; üstatların, ruhsal tekamülün ve kadim sırların renkleri",
        "texto": "İyiyi ve kötüyü kavrama, doğru davranışı seçecek bilgeliğe erişme hali.",
    },
    "7": {
        "forma": "Heptagon (veya piramit): yedi kenar, dörtlü taban ile üçlü zirvenin birleşimi; ruhsal olgunluk",
        "cor": "Yeşil, şifanın ve dengelenmenin rengi",
        "texto": "Derin bilgi, ruhsal olgunluk ve mutlak sorumluluk gerektirir.",
    },
    "8": {
        "forma": "Sekizgen: iktidarın, dengeli otoritenin ve hakkaniyetin sekiz köşesi",
        "cor": "Altın, gümüş ve tunç; gücün ışıltılı tonları",
        "texto": "Büyük güçler, büyük yükümlülükler getirir.",
    },
    "9": {
        "forma": "Dokuzgen: döngüyü nihayete erdiren dokuz cephe",
        "cor": "Lila, eflatun ve koyu mor; ruhsal simyanın ve tam dönüşümün renkleri",
        "texto": "Varlığın bütünsel ve kesin dönüşümü.",
    },
}

FORMAS_CORES_VI = {
    "1": {
        "forma": "Điểm: một điểm duy nhất, cội nguồn của vạn vật",
        "cor": "Trắng, sự hòa quyện của toàn bộ sắc cầu vồng; ánh sáng nguyên sơ chứa đựng mọi tần số năng lượng",
        "texto": "Khởi đầu là một trang giấy trắng và một xuất phát điểm duy nhất.",
    },
    "2": {
        "forma": "Đường thẳng: tuyến nối giữa hai điểm; thấu suốt lộ trình tối ưu là bài học tiến hóa căn bản",
        "cor": "Đen, mặt đối lập tuyệt đối của trắng; lá chắn tĩnh lặng bảo vệ sự thuần khiết khỏi tạp niệm",
        "texto": "Sự đối ngẫu sắc màu vạch lối; thấu hiểu điểm đối trọng là bước tiến của nhận thức.",
    },
    "3": {
        "forma": "Tam giác: biểu tượng của sự hoàn hảo, sự kết hợp giữa con người và Đấng Tạo Hóa",
        "cor": "Vàng, ánh sáng rực rỡ của trí tuệ và sự biểu đạt",
        "texto": "Ánh sáng định danh cho năng lượng này là nguồn rực rỡ chói lòa.",
    },
    "4": {
        "forma": "Hình vuông: trật tự giữa hỗn mang, nền móng vững chắc của những góc vuông bền vững",
        "cor": "Xanh dương, biểu trưng của sự an định, chân lý và sự thật",
        "texto": "Nền tảng vững chắc nâng đỡ công trình trường tồn.",
    },
    "5": {
        "forma": "Ngũ giác/Ngôi sao năm cánh: hình thể năm cạnh quyền năng, làm chủ thế giới cảm quan",
        "cor": "Hồng và đỏ thắm, dòng máu nhiệt huyết, nồng nàn và mãnh liệt",
        "texto": "Nguồn năng lượng sống động, mãnh liệt và đầy đam mê.",
    },
    "6": {
        "forma": "Lục giác/Ngôi sao sáu cánh: hình học cân bằng giữa vi mô và vĩ mô",
        "cor": "Cam, be và nâu đất, phổ màu của bậc thầy, sự thức tỉnh tâm linh và thuật giả kim tự nhiên",
        "texto": "Thấu suốt thiện ác và đạt đến sự minh triết để hành sự chuẩn mực.",
    },
    "7": {
        "forma": "Thất giác (hoặc kim tự tháp): bảy mặt hòa hợp giữa đế vuông (4) và đỉnh tam giác (3); độ chín của linh hồn",
        "cor": "Xanh lá, tần số của sự chữa lành và phục hồi",
        "texto": "Tri thức uyên thâm đòi hỏi sự chín chắn và trách nhiệm thiêng liêng.",
    },
    "8": {
        "forma": "Bát giác: hình khối tám cạnh biểu thị quyền lực và sự điều phối thế gian",
        "cor": "Vàng kim, ánh bạc và đồng sáng; vinh quang rạng rỡ của người lãnh đạo",
        "texto": "Quyền năng lớn lao đi liền với trách nhiệm vĩ đại.",
    },
    "9": {
        "forma": "Cửu giác: chín cạnh khép lại chu kỳ tiến hóa",
        "cor": "Tím nhạt, tím hoa cà và tím thẫm; màu sắc của sự chuyển hóa và thăng hoa tuyệt đối",
        "texto": "Sự chuyển hóa toàn diện và viên mãn của bản thể.",
    },
}

FORMAS_CORES_HE = {
    "1": {
        "forma": "נקודה: נקודה אחת בודדת, ראשית הכל",
        "cor": "לבן, מיזוג כל קשת הצבעים; טוהר הלבן הוא איחוד האורות וטומן בחובו את כל העוצמות",
        "texto": "ההתחלה היא דף חלק ונקי, ונקודת מוצא אחת.",
    },
    "2": {
        "forma": "קו ישר: הנתיב בין שתי נקודות; בחירת הדרך הנכונה לחיבורן היא תמצית השיעור והלמידה",
        "cor": "שחור, הניגוד המשלים ללבן; המסך המגן שאינו סופג הפרעות שווא ושומר על פנימיותו",
        "texto": "הדואליות של הצבעים מסמנת את הנתיב; בחירת נקודת הנגד היא הלימוד העמוק.",
    },
    "3": {
        "forma": "משולש: סמל השלמות, החיבור המשולש בין האדם לדמות האלוהית",
        "cor": "צהוב, צבע הבוהק הטהור והתבונה המאירה",
        "texto": "האור המגדיר אנרגיה זו בצורה הטובה ביותר הוא אור הזוהר העז.",
    },
    "4": {
        "forma": "ריבוע: סדר בתוך הכאוס, יציבות, מבנה ישר זווית המבטיח בסיס איתן וקבוע",
        "cor": "כחול, המשרה תחושת ביטחון, נאמנות ואמת ללא עוררין",
        "texto": "היסוד המוצק מחזיק את המבנה השלם.",
    },
    "5": {
        "forma": "מחומש, פנטגרם: צורה בעלת חמש צלעות, סמל לעוצמת החושים והעולם הגשמי",
        "cor": "ורוד ואדום עמוק, זרימת הדם, יצר ותשוקה חיה וסוערת",
        "texto": "אנרגיה חיה, תוססת וספוגת תשוקה.",
    },
    "6": {
        "forma": "משושה, הקסגרמה: שש צלעות באיזון מושלם",
        "cor": "כתום, בז' וחום אדמה; גוני המאסטרים הגדולים, ההתעלות והסודות הרוחניים",
        "texto": "הבחנה פנימית בין טוב לרע ותבונת מעשה נכונה וראויה.",
    },
    "7": {
        "forma": "משובע (או פירמידה): שבעה היבטים המשלבים את הבסיס הארצי עם השפיץ העליון; בשלות הנשמה",
        "cor": "ירוק, צבע המרפא והאיזון השלם",
        "texto": "דעת רחבה מחייבת בגרות אישית ואחריות עליונה.",
    },
    "8": {
        "forma": "מתומן: שמונה צלעות של שליטה וסמכות מאוזנת",
        "cor": "זהב, כסף וברונזה בוהקת; הברק הנלווה לעוצמה והנהגה",
        "texto": "עם סמכות גדולה באה אחריות כבדה ובלתי מתפשרת.",
    },
    "9": {
        "forma": "תשע-צלעות (מתושע): חותם השלמת המעגל",
        "cor": "לילך, ארגמן וסגול עמוק; תדרי הטרנסמוטציה וההתעלות הסופית",
        "texto": "הטרנספורמציה השלמה והכוללת של ההוויה כולה.",
    },
}

FORMAS_CORES_AR = {
    "1": {
        "forma": "النقطة: نقطة مفردة، أصل كل بداية",
        "cor": "الأبيض، اندماج سائر ألوان الطيف النوراني؛ النقاء المطلق الحاوي لجميع الطاقات التكوينية",
        "texto": "البداية صفحة بيضاء ناصعة ونقطة انطلاق أولى.",
    },
    "2": {
        "forma": "المستقيم: المسار الواصل بين نقطتين؛ وإدراك السبيل القويم للربط بينهما هو الدرس الجوهري",
        "cor": "الأسود، النظير المطلق للأبيض؛ الدرع الحامي الذي يصد التشتت ليحفظ الطاقة الذاتية",
        "texto": "ثنائية الألوان ترسم المعالم؛ واختيار النظير الحقيقي هو تمام الإدراك.",
    },
    "3": {
        "forma": "المثلث: رمز الكمال الإلهي، توافق الثالوث الكوني وتناغم البعد البشري مع الخالق",
        "cor": "الأصفر، قبس الإشراق المتقد والذكاء الوهاج",
        "texto": "النور الذي يعبر بأصدق بيان عن هذه الطاقة هو التوهج الشديد.",
    },
    "4": {
        "forma": "المربع: إرساء النظام في قلب الفوضى، إتقان العمل، والأركان القائمة على الثبات والرسوخ",
        "cor": "الأزرق، مبعث الأمان، والصدق، واليقين الراسخ",
        "texto": "الأساس المتين يرفع البنيان الشامخ على مر العصور.",
    },
    "5": {
        "forma": "المخمس، النجمة الخماسية: خمسة أضلاع حاكمة لسيادة الحواس والطاقة الحيوية للجسد",
        "cor": "الوردي والأحمر القاني، دفق الحياة، العاطفة الجياشة والشغف المتوقد",
        "texto": "طاقة نابضة بالحياة، مشتعلة وعميقة التأثير.",
    },
    "6": {
        "forma": "المسدس، النجمة السداسية: توازن محكم بستة أركان كونية",
        "cor": "البرتقالي والبيج والبني، درجات ألوان المعلمين والارتقاء الروحي والحكمة الأصيلة",
        "texto": "التمييز بين الخير والشر والتحلي بالحكمة لسلوك المسار القويم.",
    },
    "7": {
        "forma": "المسبع (أو الهرم): سبعة أوجه تجمع أركان القاعدة الأربعة وقمة المثلث الثلاثية؛ نضج الروح",
        "cor": "الأخضر، لون الشفاء التام والسلام الداخلي",
        "texto": "غزارة العلم تورث نضجاً عميقاً ومسؤولية كبرى.",
    },
    "8": {
        "forma": "المثمن: ثمانية أضلاع تجسد هيبة القيادة والعدالة النافذة",
        "cor": "الذهبي، الفضي والبرونزي؛ بريق المجد والنفوذ الرفيع",
        "texto": "مع عظيم السلطة والقدرة تتضاعف الالتزامات الجسام.",
    },
    "9": {
        "forma": "المتسع: تسعة أضلاع تختتم مسار الدورة الكونية",
        "cor": "الليلكي، الأرجواني والبنفسجي؛ طيف التحول الروحي الكلي والخلاص",
        "texto": "التحول الأسمى والنهائي لجوهر الكينونة.",
    },
}

# 
# CAMADA 4: LP_DESC_MASTER (11, 22, 33)
# 

LP_DESC_MASTER = {
    "pt": {
        11: "Mestre intuitivo.",
        22: "Mestre construtor.",
        33: "Mestre do amor.",
    },
    "en": {
        11: "Intuitive master.",
        22: "Master builder.",
        33: "Master of love.",
    },
    "es": {
        11: "Maestro intuitivo.",
        22: "Maestro constructor.",
        33: "Maestro del amor.",
    },
    "it": {
        11: "Maestro intuitivo.",
        22: "Maestro costruttore.",
        33: "Maestro dell'amore.",
    },
    "fr": {
        11: "Maître intuitif.",
        22: "Maître bâtisseur.",
        33: "Maître de l'amour.",
    },
    "de": {
        11: "Intuitiver Meister.",
        22: "Baumeister-Meister.",
        33: "Meister der Liebe.",
    },
    "ja": {
        11: "直感のマスター。",
        22: "建設のマスター。",
        33: "愛のマスター。",
    },
    "zh": {
        11: "直觉大师。",
        22: "建造大师。",
        33: "爱的大师。",
    },
    "ru": {
        11: "Интуитивный мастер.",
        22: "Мастер-строитель.",
        33: "Мастер любви.",
    },
    "id": {
        11: "Master intuitif.",
        22: "Master pembangun.",
        33: "Master cinta.",
    },
    "tr": {
        11: "Sezgisel usta.",
        22: "İnşaat ustası.",
        33: "Aşk ustası.",
    },
    "vi": {
        11: "Bậc thầy trực giác.",
        22: "Bậc thầy kiến tạo.",
        33: "Bậc thầy tình yêu.",
    },
    "he": {
        11: "מאסטר אינטואיטיבי.",
        22: "מאסטר בונה.",
        33: "מאסטר של אהבה.",
    },
    "ar": {
        11: "سيد الحدس.",
        22: "سيد البناء.",
        33: "سيد الحب.",
    },
}

# 
# CONSOLIDAÇÃO GLOBAL POR IDIOMA (Mapeamento Unificado)
# 

ENERGIA_SEMANTICA = {
    "pt": ENERGIA_SEMANTICA_PT,
    "en": ENERGIA_SEMANTICA_EN,
    "es": ENERGIA_SEMANTICA_ES,
    "it": ENERGIA_SEMANTICA_IT,
    "fr": ENERGIA_SEMANTICA_FR,
    "de": ENERGIA_SEMANTICA_DE,
    "ja": ENERGIA_SEMANTICA_JA,
    "zh": ENERGIA_SEMANTICA_ZH,
    "ru": ENERGIA_SEMANTICA_RU,
    "id": ENERGIA_SEMANTICA_ID,
    "tr": ENERGIA_SEMANTICA_TR,
    "vi": ENERGIA_SEMANTICA_VI,
    "he": ENERGIA_SEMANTICA_HE,
    "ar": ENERGIA_SEMANTICA_AR,
}

VIDAS_SEMANTICA = {
    "pt": VIDAS_SEMANTICA_PT,
    "en": VIDAS_SEMANTICA_EN,
    "es": VIDAS_SEMANTICA_ES,
    "it": VIDAS_SEMANTICA_IT,
    "fr": VIDAS_SEMANTICA_FR,
    "de": VIDAS_SEMANTICA_DE,
    "ja": VIDAS_SEMANTICA_JA,
    "zh": VIDAS_SEMANTICA_ZH,
    "ru": VIDAS_SEMANTICA_RU,
    "id": VIDAS_SEMANTICA_ID,
    "tr": VIDAS_SEMANTICA_TR,
    "vi": VIDAS_SEMANTICA_VI,
    "he": VIDAS_SEMANTICA_HE,
    "ar": VIDAS_SEMANTICA_AR,
}

FORMAS_CORES_SEMANTICA = {
    "pt": FORMAS_CORES_PT,
    "en": FORMAS_CORES_EN,
    "es": FORMAS_CORES_ES,
    "it": FORMAS_CORES_IT,
    "fr": FORMAS_CORES_FR,
    "de": FORMAS_CORES_DE,
    "ja": FORMAS_CORES_JA,
    "zh": FORMAS_CORES_ZH,
    "ru": FORMAS_CORES_RU,
    "id": FORMAS_CORES_ID,
    "tr": FORMAS_CORES_TR,
    "vi": FORMAS_CORES_VI,
    "he": FORMAS_CORES_HE,
    "ar": FORMAS_CORES_AR,
}

# 
# FUNÇÕES DE CONSULTA COM RETROALIMENTAÇÃO (FALLBACK AUTOMÁTICO PARA 'pt')
# 

def _normalizar(chave):
    """Garante coerência de comparação convertendo para string limpa."""
    return str(chave).strip()

def _registro(dicionario, chave, lang):
    """Busca o valor no idioma solicitado, recorrendo a 'pt' caso não encontre."""
    d = dicionario.get(lang) or dicionario.get("pt") or {}
    c = _normalizar(chave)
    if c in d:
        return d[c]
    return dicionario.get("pt", {}).get(c, "")

def obter_texto_energia(numero, lang="pt"):
    """Retorna a descrição arquetípica da energia do número (1 a 9)."""
    return _registro(ENERGIA_SEMANTICA, numero, lang)

def obter_texto_vida(numero, lang="pt"):
    """Retorna a narrativa existencial e espiritual da vida associada (1 a 9)."""
    return _registro(VIDAS_SEMANTICA, numero, lang)

def obter_descricao_mestre(numero, lang="pt"):
    """Retorna o texto de síntese para números-mestre (11, 22, 33)."""
    try:
        n_int = int(str(numero).strip())
    except (ValueError, TypeError):
        return ""
    d_lang = LP_DESC_MASTER.get(lang) or LP_DESC_MASTER.get("pt") or {}
    if n_int in d_lang:
        return d_lang[n_int]
    return LP_DESC_MASTER.get("pt", {}).get(n_int, "")

def renderizar_forma_cor(numero, lang="pt"):
    """
    Retorna o dicionário estruturado contendo a geometria, a cor e a frase
    afirmativa para renderização gráfica ou textual nos laudos analíticos.
    """
    d = FORMAS_CORES_SEMANTICA.get(lang) or FORMAS_CORES_SEMANTICA.get("pt") or {}
    c = _normalizar(numero)
    reg = d.get(c) or FORMAS_CORES_SEMANTICA.get("pt", {}).get(c, {})
    return {
        "forma": reg.get("forma", ""),
        "cor": reg.get("cor", ""),
        "texto": reg.get("texto", ""),
    }

