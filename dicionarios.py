# -*- coding: utf-8 -*-
# dicionarios.py - Base de dados e internacionalização

# ============================================================
# PREÇOS — FONTE DE VERDADE ÚNICA
# Cotação âncora: 1 USD = 5,40 BRL
# Stripe (prices_1_.csv) + capas + tabela de controle
# Validação: todo preço reduz numerologicamente a 8
# ============================================================Microsoft Windows [versão 10.0.19045.6466]

TRAD = {
    "pt": {
        "express": "Mapa Express (R$ 8,00)", "completo": "Mapa Completo (R$ 17,00)",
        "significado": "Significado", "caminho_vida": "Caminho da Vida", "expressao": "Expressão", "motivacao": "Motivação",
        "personalidade": "Personalidade", "destino": "Destino", "seu_perfil": "Seu Perfil Numerológico", "analise": "Análise Detalhada",
        "positivo": "Aspectos Positivos", "negativo": "Aspectos Negativos", "licao": "Lição de Vida", "ciclos": "Ciclos de Vida",
        "formativo": "Ciclo Formativo", "produtivo": "Ciclo Produtivo", "colheita": "Ciclo da Colheita", "desafios": "Desafios",
        "menor1": "Desafio Menor 1", "menor2": "Desafio Menor 2", "principal": "Desafio Principal", "realizacoes": "Realizações",
        "juventude": "1ª Realização (Juventude)", "vida_adulta": "2ª Realização (Vida Adulta)", "maturidade": "3ª Realização (Maturidade)",
        "legado": "4ª Realização (Legado)", "vibracao": "Vibração de Nascimento", "grade": "Grade Energética",
        "presentes": "Energias Presentes", "carencias": "Carências Energéticas", "nota_final": "Nota Final", "regente": "Regente",
        "download": "Baixar PDF", "voltar": "Voltar", "confirmado": "Pagamento Confirmado!", "gerado": "Seu mapa foi gerado com sucesso.",
        "nenhum": "Nenhum",
    },
    "en": {
        "express": "Express Map ($ 17.00)", "completo": "Full Map ($ 152.00)",
        "significado": "Meaning", "caminho_vida": "Life Path", "expressao": "Expression", "motivacao": "Motivation",
        "personalidade": "Personality", "destino": "Destiny", "seu_perfil": "Your Numerological Profile", "analise": "Detailed Analysis",
        "positivo": "Positive Aspects", "negativo": "Negative Aspects", "licao": "Life Lesson", "ciclos": "Life Cycles",
        "formativo": "Formative Cycle", "produtivo": "Productive Cycle", "colheita": "Harvest Cycle", "desafios": "Challenges",
        "menor1": "Minor Challenge 1", "menor2": "Minor Challenge 2", "principal": "Main Challenge", "realizacoes": "Achievements",
        "juventude": "1st Achievement (Youth)", "vida_adulta": "2nd Achievement (Adulthood)", "maturidade": "3rd Achievement (Maturity)",
        "legado": "4th Achievement (Legacy)", "vibracao": "Birth Vibration", "grade": "Energy Grid",
        "presentes": "Present Energies", "carencias": "Energy Gaps", "nota_final": "Final Score", "regente": "Ruler",
        "download": "Download PDF", "voltar": "Back", "confirmado": "Payment Confirmed!", "gerado": "Your map was successfully generated.",
        "nenhum": "None",
    },
    "es": {
        "express": "Mapa Express (17,00 €)", "completo": "Mapa Completo (152,00 €)",
        "significado": "Significado", "caminho_vida": "Camino de la Vida", "expressao": "Expresión", "motivacao": "Motivación",
        "personalidade": "Personalidad", "destino": "Destino", "seu_perfil": "Tu Perfil Numerológico", "analise": "Análisis Detallado",
        "positivo": "Aspectos Positivos", "negativo": "Aspectos Negativos", "licao": "Lección de Vida", "ciclos": "Ciclos de Vida",
        "formativo": "Ciclo Formativo", "produtivo": "Ciclo Productivo", "colheita": "Ciclo de Cosecha", "desafios": "Desafíos",
        "menor1": "Desafío Menor 1", "menor2": "Desafío Menor 2", "principal": "Desafío Principal", "realizacoes": "Logros",
        "juventude": "1er Logro (Juventud)", "vida_adulta": "2do Logro (Vida Adulta)", "maturidade": "3er Logro (Madurez)",
        "legado": "4to Logro (Legado)", "vibracao": "Vibración de Nacimiento", "grade": "Rejilla Energética",
        "presentes": "Energías Presentes", "carencias": "Carencias Energéticas", "nota_final": "Nota Final", "regente": "Regente",
        "download": "Descargar PDF", "voltar": "Volver", "confirmado": "¡Pago Confirmado!", "gerado": "Tu mapa ha sido generado con éxito.",
        "nenhum": "Ninguno",
    },
    "fr": {
        "express": "Carte Express (17,00 €)", "completo": "Carte Complète (152,00 €)",
        "significado": "Signification", "caminho_vida": "Chemin de Vie", "expressao": "Expression", "motivacao": "Motivation",
        "personalidade": "Personnalité", "destino": "Destin", "seu_perfil": "Votre Profil Numérologique", "analise": "Analyse Détaillée",
        "positivo": "Aspects Positifs", "negativo": "Aspects Négatifs", "licao": "Leçon de Vie", "ciclos": "Cycles de Vie",
        "formativo": "Cycle Formatif", "produtivo": "Cycle Productif", "colheita": "Cycle de Récolte", "desafios": "Défis",
        "menor1": "Défi Mineur 1", "menor2": "Défi Mineur 2", "principal": "Défi Principal", "realizacoes": "Réalisations",
        "juventude": "1ère Réalisation (Jeunesse)", "vida_adulta": "2ème Réalisation (Âge Adulte)", "maturidade": "3ème Réalisation (Maturité)",
        "legado": "4ème Réalisation (Héritage)", "vibracao": "Vibration de Naissance", "grade": "Grille Énergétique",
        "presentes": "Énergies Présentes", "carencias": "Carences Énergétiques", "nota_final": "Note Finale", "regente": "Régent",
        "download": "Télécharger PDF", "voltar": "Retour", "confirmado": "Paiement Confirmé !", "gerado": "Votre carte a été générée avec succès.",
        "nenhum": "Aucun",
    },
    "de": {
        "express": "Express-Karte (17,00 €)", "completo": "Vollständige Karte (152,00 €)",
        "significado": "Bedeutung", "caminho_vida": "Lebensweg", "expressao": "Ausdruck", "motivacao": "Motivation",
        "personalidade": "Persönlichkeit", "destino": "Schicksal", "seu_perfil": "Ihr numerologisches Profil", "analise": "Detaillierte Analyse",
        "positivo": "Positive Aspekte", "negativo": "Negative Aspekte", "licao": "Lebenslektion", "ciclos": "Lebenszyklen",
        "formativo": "Bildungszyklus", "produtivo": "Produktiver Zyklus", "colheita": "Erntezyklus", "desafios": "Herausforderungen",
        "menor1": "Kleine Herausforderung 1", "menor2": "Kleine Herausforderung 2", "principal": "Hauptherausforderung", "realizacoes": "Erfolge",
        "juventude": "1. Erfolg (Jugend)", "vida_adulta": "2. Erfolg (Erwachsenenalter)", "maturidade": "3. Erfolg (Reife)",
        "legado": "4. Erfolg (Vermächtnis)", "vibracao": "Geburtsschwingung", "grade": "Energiegitter",
        "presentes": "Vorhandene Energien", "carencias": "Energielücken", "nota_final": "Endnote", "regente": "Regent",
        "download": "PDF herunterladen", "voltar": "Zurück", "confirmado": "Zahlung bestätigt!", "gerado": "Ihre Karte wurde erfolgreich erstellt.",
        "nenhum": "Keine",
    },
    "it": {
        "express": "Mappa Express (17,00 €)", "completo": "Mappa Completa (152,00 €)",
        "significado": "Significato", "caminho_vida": "Cammino della Vita", "expressao": "Espressione", "motivacao": "Motivazione",
        "personalidade": "Personalità", "destino": "Destino", "seu_perfil": "Il Tuo Profilo Numerologico", "analise": "Analisi Dettagliata",
        "positivo": "Aspetti Positivi", "negativo": "Aspetti Negativi", "licao": "Lezione di Vita", "ciclos": "Cicli di Vita",
        "formativo": "Ciclo Formativo", "produtivo": "Ciclo Produttivo", "colheita": "Ciclo del Raccolto", "desafios": "Sfide",
        "menor1": "Sfida Minore 1", "menor2": "Sfida Minore 2", "principal": "Sfida Principale", "realizacoes": "Traguardi",
        "juventude": "1° Traguardo (Giovinezza)", "vida_adulta": "2° Traguardo (Età Adulta)", "maturidade": "3° Traguardo (Maturità)",
        "legado": "4° Traguardo (Eredità)", "vibracao": "Vibrazione di Nascita", "grade": "Griglia Energetica",
        "presentes": "Energie Presenti", "carencias": "Carenze Energetiche", "nota_final": "Voto Finale", "regente": "Reggente",
        "download": "Scarica PDF", "voltar": "Indietro", "confirmado": "Pagamento Confermato!", "gerado": "La tua mappa è stata generata con successo.",
        "nenhum": "Nessuno",
    },
    "ja": {
        "express": "エクスプレスマップ (¥ 1.376)", "completo": "フルマップ (¥ 16.856)",
        "significado": "意味", "caminho_vida": "ライフパス", "expressao": "表現", "motivacao": "動機",
        "personalidade": "性格", "destino": "運命", "seu_perfil": "あなたの数秘術プロファイル", "analise": "詳細分析",
        "positivo": "ポジティブな側面", "negativo": "ネガティブな側面", "licao": "人生の教訓", "ciclos": "ライフサイクル",
        "formativo": "形成期", "produtivo": "生産期", "colheita": "収穫期", "desafios": "課題",
        "menor1": "マイナーチャレンジ 1", "menor2": "マイナーチャレンジ 2", "principal": "メインチャレンジ", "realizacoes": "達成",
        "juventude": "第1の達成 (青春)", "vida_adulta": "第2の達成 (成人)", "maturidade": "第3の達成 (成熟)",
        "legado": "第4の達成 (遺産)", "vibracao": "誕生の波動", "grade": "エネルギーマトリックス",
        "presentes": "存在するエネルギー", "carencias": "不足しているエネルギー", "nota_final": "最終評価", "regente": "支配星",
        "download": "PDFをダウンロード", "voltar": "戻る", "confirmado": "支払い確認済み!", "gerado": "マップの生成に成功しました。",
        "nenhum": "なし",
    },
    "zh": {
        "express": "快速解读 (¥ 53,00)", "completo": "完整解读 (¥ 647,00)",
        "significado": "含义", "caminho_vida": "生命道路", "expressao": "表现", "motivacao": "动机",
        "personalidade": "个性", "destino": "命运", "seu_perfil": "您的命理档案", "analise": "详细分析",
        "positivo": "积极方面", "negativo": "消极方面", "licao": "人生课题", "ciclos": "人生周期",
        "formativo": "形成期", "produtivo": "生产期", "colheita": "收获期", "desafios": "挑战",
        "menor1": "小挑战 1", "menor2": "小挑战 2", "principal": "主要挑战", "realizacoes": "成就",
        "juventude": "第一成就 (青年)", "vida_adulta": "第二成就 (成年)", "maturidade": "第三成就 (成熟)",
        "legado": "第四成就 (遗产)", "vibracao": "出生振动", "grade": "能量网格",
        "presentes": "存在的能量", "carencias": "缺失的能量", "nota_final": "最终评语", "regente": "主宰",
        "download": "下载PDF", "voltar": "返回", "confirmado": "付款已确认!", "gerado": "您的解读图已成功生成。",
        "nenhum": "无",
    },
    "ru": {
        "express": "Экспресс-карта (₽ 440,00)", "completo": "Полная карта (₽ 5.390,00)",
        "significado": "Значение", "caminho_vida": "Путь жизни", "expressao": "Выражение", "motivacao": "Мотивация",
        "personalidade": "Личность", "destino": "Судьба", "seu_perfil": "Ваш нумерологический профиль", "analise": "Детальный анализ",
        "positivo": "Положительные аспекты", "negativo": "Отрицательные аспекты", "licao": "Урок жизни", "ciclos": "Жизненные циклы",
        "formativo": "Формирующий цикл", "produtivo": "Продуктивный цикл", "colheita": "Цикл урожая", "desafios": "Вызовы",
        "menor1": "Малый вызов 1", "menor2": "Малый вызов 2", "principal": "Главный вызов", "realizacoes": "Достижения",
        "juventude": "1-е достижение (Юность)", "vida_adulta": "2-е достижение (Взрослая жизнь)", "maturidade": "3-е достижение (Зрелость)",
        "legado": "4-е достижение (Наследие)", "vibracao": "Вибрация рождения", "grade": "Энергетическая сетка",
        "presentes": "Присутствующие энергии", "carencias": "Энергетические пробелы", "nota_final": "Итоговая оценка", "regente": "Правитель",
        "download": "Скачать PDF", "voltar": "Назад", "confirmado": "Платёж подтверждён!", "gerado": "Ваша карта успешно создана.",
        "nenhum": "Нет",
    },
    "he": {
        "express": "מפה מהירה (₪ 53.00)", "completo": "מפה מלאה (₪ 647.00)",
        "significado": "משמעות", "caminho_vida": "נתיב החיים", "expressao": "הבעה", "motivacao": "מוטיבציה",
        "personalidade": "אישיות", "destino": "גורל", "seu_perfil": "הפרופיל הנומרולוגי שלך", "analise": "ניתוח מפורט",
        "positivo": "היבטים חיוביים", "negativo": "היבטים שליליים", "licao": "שיעור חיים", "ciclos": "מחזורי חיים",
        "formativo": "מחזור מעצב", "produtivo": "מחזור יצרני", "colheita": "מחזור קציר", "desafios": "אתגרים",
        "menor1": "אתגר קטן 1", "menor2": "אתגר קטן 2", "principal": "אתגר עיקרי", "realizacoes": "הישגים",
        "juventude": "הישג ראשון (נעורים)", "vida_adulta": "הישג שני (בגרות)", "maturidade": "הישג שלישי (בשלות)",
        "legado": "הישג רביעי (מורשת)", "vibracao": "תנודת לידה", "grade": "רשת אנרגיה",
        "presentes": "אנרגיות נוכחות", "carencias": "פערי אנרגיה", "nota_final": "ציון סופי", "regente": "שליט",
        "download": "הורד PDF", "voltar": "חזור", "confirmado": "התשלום אושר!", "gerado": "המפה שלך נוצרה בהצלחה.",
        "nenhum": "אין",
    },
    "ar": {
        "express": "خريطة سريعة (AED 53.00)", "completo": "خريطة كاملة (AED 647.00)",
        "significado": "المعنى", "caminho_vida": "مسار الحياة", "expressao": "التعبير", "motivacao": "الدافع",
        "personalidade": "الشخصية", "destino": "المصير", "seu_perfil": "ملفك العددي", "analise": "تحليل مفصل",
        "positivo": "الجوانب الإيجابية", "negativo": "الجوانب السلبية", "licao": "درس الحياة", "ciclos": "دورات الحياة",
        "formativo": "الدورة التكوينية", "produtivo": "الدورة الإنتاجية", "colheita": "دورة الحصاد", "desafios": "التحديات",
        "menor1": "التحدي الأصغر 1", "menor2": "التحدي الأصغر 2", "principal": "التحدي الرئيسي", "realizacoes": "الإنجازات",
        "juventude": "الإنجاز الأول (الشباب)", "vida_adulta": "الإنجاز الثاني (البلوغ)", "maturidade": "الإنجاز الثالث (النضج)",
        "legado": "الإنجاز الرابع (الإرث)", "vibracao": "اهتزاز الميلاد", "grade": "شبكة الطاقة",
        "presentes": "الطاقات الحاضرة", "carencias": "فجوات الطاقة", "nota_final": "النتيجة النهائية", "regente": "الحاكم",
        "download": "تحميل PDF", "voltar": "رجوع", "confirmado": "تم تأكيد الدفع!", "gerado": "تم إنشاء خريطتك بنجاح.",
        "nenhum": "لا شيء",
    },
    "id": {
        "express": "Peta Ekspres (Rp 10.952,00)", "completo": "Peta Lengkap (Rp 134.162,00)",
        "significado": "Arti", "caminho_vida": "Jalan Hidup", "expressao": "Ekspresi", "motivacao": "Motivasi",
        "personalidade": "Kepribadian", "destino": "Takdir", "seu_perfil": "Profil Numerologi Anda", "analise": "Analisis Terperinci",
        "positivo": "Aspek Positif", "negativo": "Aspek Negatif", "licao": "Pelajaran Hidup", "ciclos": "Siklus Hidup",
        "formativo": "Siklus Formatif", "produtivo": "Siklus Produktif", "colheita": "Siklus Panen", "desafios": "Tantangan",
        "menor1": "Tantangan Kecil 1", "menor2": "Tantangan Kecil 2", "principal": "Tantangan Utama", "realizacoes": "Pencapaian",
        "juventude": "Pencapaian ke-1 (Masa Muda)", "vida_adulta": "Pencapaian ke-2 (Dewasa)", "maturidade": "Pencapaian ke-3 (Kematangan)",
        "legado": "Pencapaian ke-4 (Warisan)", "vibracao": "Getaran Kelahiran", "grade": "Kisi Energi",
        "presentes": "Energi yang Hadir", "carencias": "Kekurangan Energi", "nota_final": "Nilai Akhir", "regente": "Penguasa",
        "download": "Unduh PDF", "voltar": "Kembali", "confirmado": "Pembayaran Dikonfirmasi!", "gerado": "Peta Anda berhasil dibuat.",
        "nenhum": "Tidak Ada",
        "numeros_principais": "Angka Utama Anda", "caminho_ciclos": "Jalan Hidup dan Siklus",
        "desafios_realizacoes": "Tantangan dan Pencapaian", "como_calculamos": "Bagaimana kami menghitung?",
        "por_que_energia_8": "Mengapa energi 8?", "energia_8_ideal": "Energi 8 — IDEAL:", "alternativas": "Alternatif:",
    },
    "tr": {
        "express": "Ekspres Harita (₺ 62,00)", "completo": "Tam Harita (₺ 764,00)",
        "significado": "Anlam", "caminho_vida": "Yaşam Yolu", "expressao": "İfade", "motivacao": "Motivasyon",
        "personalidade": "Kişilik", "destino": "Kader", "seu_perfil": "Numeroloji Profiliniz", "analise": "Detaylı Analiz",
        "positivo": "Olumlu Yönler", "negativo": "Olumsuz Yönler", "licao": "Yaşam Dersi", "ciclos": "Yaşam Döngüleri",
        "formativo": "Biçimlendirici Döngü", "produtivo": "Üretken Döngü", "colheita": "Hasat Döngüsü", "desafios": "Zorluklar",
        "menor1": "Küçük Zorluk 1", "menor2": "Küçük Zorluk 2", "principal": "Ana Zorluk", "realizacoes": "Başarılar",
        "juventude": "1. Başarı (Gençlik)", "vida_adulta": "2. Başarı (Yetişkinlik)", "maturidade": "3. Başarı (Olgunluk)",
        "legado": "4. Başarı (Miras)", "vibracao": "Doğum Titreşimi", "grade": "Enerji Izgarası",
        "presentes": "Mevcut Enerjiler", "carencias": "Enerji Eksikleri", "nota_final": "Final Notu", "regente": "Yönetici",
        "download": "PDF İndir", "voltar": "Geri", "confirmado": "Ödeme Onaylandı!", "gerado": "Haritanız başarıyla oluşturuldu.",
        "nenhum": "Yok",
        "numeros_principais": "Ana Numaralarınız", "caminho_ciclos": "Yaşam Yolu ve Döngüler",
        "desafios_realizacoes": "Zorluklar ve Başarılar", "como_calculamos": "Nasıl hesaplıyoruz?",
        "por_que_energia_8": "Neden enerji 8?", "energia_8_ideal": "Enerji 8 — İDEAL:", "alternativas": "Alternatifler:",
    },
    "vi": {
        "express": "Bản đồ Nhanh (₫ 24.992)", "completo": "Bản đồ Đầy đủ (₫ 306.152)",
        "significado": "Ý nghĩa", "caminho_vida": "Đường đời", "expressao": "Biểu hiện", "motivacao": "Động lực",
        "personalidade": "Tính cách", "destino": "Số phận", "seu_perfil": "Hồ sơ Thần số học của bạn", "analise": "Phân tích chi tiết",
        "positivo": "Khía cạnh tích cực", "negativo": "Khía cạnh tiêu cực", "licao": "Bài học cuộc sống", "ciclos": "Chu kỳ cuộc đời",
        "formativo": "Chu kỳ hình thành", "produtivo": "Chu kỳ sản xuất", "colheita": "Chu kỳ thu hoạch", "desafios": "Thách thức",
        "menor1": "Thách thức nhỏ 1", "menor2": "Thách thức nhỏ 2", "principal": "Thách thức chính", "realizacoes": "Thành tựu",
        "juventude": "Thành tựu thứ 1 (Tuổi trẻ)", "vida_adulta": "Thành tựu thứ 2 (Trưởng thành)", "maturidade": "Thành tựu thứ 3 (Chín chắn)",
        "legado": "Thành tựu thứ 4 (Di sản)", "vibracao": "Rung động sinh", "grade": "Lưới năng lượng",
        "presentes": "Năng lượng hiện diện", "carencias": "Thiếu hụt năng lượng", "nota_final": "Điểm cuối cùng", "regente": "Người cai quản",
        "download": "Tải PDF", "voltar": "Quay lại", "confirmado": "Thanh toán đã xác nhận!", "gerado": "Bản đồ của bạn đã được tạo thành công.",
        "nenhum": "Không có",
        "numeros_principais": "Các Số Chính của Bạn", "caminho_ciclos": "Đường đời và Chu kỳ",
        "desafios_realizacoes": "Thách thức và Thành đạt", "como_calculamos": "Chúng tôi tính như thế nào?",
        "por_que_energia_8": "Tại sao là năng lượng 8?", "energia_8_ideal": "Năng lượng 8 — LÝ TƯỞNG:", "alternativas": "Phương án thay thế:",
    },
}
         
# ===== NOMES DOS 23 PRODUTOS =====
PRODUTOS = {
    "pt": {"express": "Mapa Express", "vida": "Qual Vida/Ano", "completo": "Mapa Completo",
        "ia": "Pesquisa IA de Nomes", "urna": "Validacao Nome de Urna", "eleitoral": "Numero Eleitoral",
        "imovel": "Numero do Imovel", "calendario": "Calendario Mensal Energetico",
        "artistico": "Validacao Nome Artistico", "bebe": "Planejamento Nome de Bebe",
        "assinatura": "Validacao de Assinaturas", "negocio": "Nome para Negocio/Produto",
        "casal": "Mapa do Casal", "familia": "Mapa Familia Premium", "coletivo": "Bonus Coletivo/Empresarial",
        "nome_pet": "Nome do Pet", "nickname": "Nickname Digital", "nome_dominio": "Nome do Dominio",
        "nome_canal": "Nome do Canal", "nome_equipe": "Nome da Equipe", "nome_ong": "Nome de ONG, Associacao, Instituto ou Fundacao",
        "nome_projeto": "Nome do Projeto", "nome_evento": "Nome do Evento"},
    "en": {"express": "Express Map", "vida": "Life Phase & Year", "completo": "Complete Map",
        "ia": "AI Name Search", "urna": "Ballot Name Validation", "eleitoral": "Electoral Number",
        "imovel": "Property Number", "calendario": "Monthly Energy Calendar",
        "artistico": "Artistic Name Validation", "bebe": "Baby Name Planning",
        "assinatura": "Signature Validation", "negocio": "Business & Product Name",
        "casal": "Couple Map", "familia": "Premium Family Map", "coletivo": "Corporate Bonus",
        "nome_pet": "Pet Name", "nickname": "Digital Nickname", "nome_dominio": "Domain Name",
        "nome_canal": "Channel Name", "nome_equipe": "Team Name", "nome_ong": "NGO, Association, Institute or Foundation Name",
        "nome_projeto": "Project Name", "nome_evento": "Event Name"},
    "es": {"express": "Mapa Exprés", "vida": "Ciclo de Vida y Año", "completo": "Mapa Completo",
        "ia": "Búsqueda IA de Nombres", "urna": "Validación Nombre de Urna", "eleitoral": "Número Electoral",
        "imovel": "Número de la Propiedad", "calendario": "Calendario Mensual Energético",
        "artistico": "Validación Nombre Artístico", "bebe": "Planificación Nombre de Bebé",
        "assinatura": "Validación de Firmas", "negocio": "Nombre para Negocio/Producto",
        "casal": "Mapa de Pareja", "familia": "Mapa Familiar Premium", "coletivo": "Bono Corporativo",
        "nome_pet": "Nombre de la Mascota", "nickname": "Apodo Digital", "nome_dominio": "Nombre de Dominio",
        "nome_canal": "Nombre del Canal", "nome_equipe": "Nombre del Equipo", "nome_ong": "Nombre de ONG, Asociacion, Instituto o Fundacion",
        "nome_projeto": "Nombre del Proyecto", "nome_evento": "Nombre del Evento"},
    "it": {"express": "Mappa Espressa", "vida": "Fase di Vita e Anno", "completo": "Mappa Completa",
        "ia": "Ricerca IA Nomi", "urna": "Validazione Nome della Scheda", "eleitoral": "Numero Elettorale",
        "imovel": "Numero dell'Immobile", "calendario": "Calendario Mensile Energetico",
        "artistico": "Validazione Nome d'Arte", "bebe": "Pianificazione Nome del Bambino",
        "assinatura": "Validazione delle Firme", "negocio": "Nome per Business/Prodotto",
        "casal": "Mappa di Coppia", "familia": "Mappa Famiglia Premium", "coletivo": "Bonus Aziendale",
        "nome_pet": "Nome dell'Animale", "nickname": "Nickname Digitale", "nome_dominio": "Nome del Dominio",
        "nome_canal": "Nome del Canale", "nome_equipe": "Nome della Squadra", "nome_ong": "Nome di ONG, Associazione, Istituto o Fondazione",
        "nome_projeto": "Nome del Progetto", "nome_evento": "Nome dell'Evento"},
    "fr": {"express": "Carte Express", "vida": "Phase de Vie et Année", "completo": "Carte Complète",
        "ia": "Recherche IA de Noms", "urna": "Validation Nom du Bulletin", "eleitoral": "Numéro Électoral",
        "imovel": "Numéro du Bien", "calendario": "Calendrier Mensuel Énergétique",
        "artistico": "Validation Nom de Scène", "bebe": "Planification Prénom de Bébé",
        "assinatura": "Validation des Signatures", "negocio": "Nom pour Entreprise/Produit",
        "casal": "Carte du Couple", "familia": "Carte Famille Premium", "coletivo": "Bonus d'Entreprise",
        "nome_pet": "Nom de l'Animal", "nickname": "Pseudo Numerique", "nome_dominio": "Nom de Domaine",
        "nome_canal": "Nom de la Chaine", "nome_equipe": "Nom de l'Equipe", "nome_ong": "Nom d'ONG, Association, Institut ou Fondation",
        "nome_projeto": "Nom du Projet", "nome_evento": "Nom de l'Evenement"},
    "de": {"express": "Express-Karte", "vida": "Lebensphase & Jahr", "completo": "Vollständige Karte",
        "ia": "KI-Namenssuche", "urna": "Stimmzettelname-Validierung", "eleitoral": "Wahlnummer",
        "imovel": "Immobiliennummer", "calendario": "Monatlicher Energiekalender",
        "artistico": "Künstlername-Validierung", "bebe": "Babynamen-Planung",
        "assinatura": "Unterschrifts-Validierung", "negocio": "Name für Unternehmen/Produkt",
        "casal": "Paar-Karte", "familia": "Premium-Familien-Karte", "coletivo": "Unternehmensbonus",
        "nome_pet": "Haustiername", "nickname": "Digitaler Spitzname", "nome_dominio": "Domainname",
        "nome_canal": "Kanalname", "nome_equipe": "Teamname", "nome_ong": "Name von NGO, Verein, Institut oder Stiftung",
        "nome_projeto": "Projektname", "nome_evento": "Veranstaltungsname"},
    "ja": {"express": "エクスプレスマップ", "vida": "ライフステージと年", "completo": "完全マップ",
        "ia": "AI名前検索", "urna": "投票用紙名の検証", "eleitoral": "選挙番号",
        "imovel": "不動産番号", "calendario": "月間エネルギーカレンダー",
        "artistico": "芸名の検証", "bebe": "赤ちゃんの名前計画",
        "assinatura": "署名の検証", "negocio": "ビジネス・商品名",
        "casal": "カップルマップ", "familia": "プレミアム家族マップ", "coletivo": "法人ボーナス",
        "nome_pet": "ペットの名前", "nickname": "デジタルニックネーム", "nome_dominio": "ドメイン名",
        "nome_canal": "チャンネル名", "nome_equipe": "チーム名", "nome_ong": "NGO・協会・研究所・財団の名前",
        "nome_projeto": "プロジェクト名", "nome_evento": "イベント名"},
    "zh": {"express": "快速地图", "vida": "生命阶段与年份", "completo": "完整地图",
        "ia": "AI名字搜索", "urna": "选票名称验证", "eleitoral": "选举号码",
        "imovel": "房产号码", "calendario": "每月能量日历",
        "artistico": "艺名验证", "bebe": "宝宝取名规划",
        "assinatura": "签名验证", "negocio": "企业/产品名称",
        "casal": "情侣地图", "familia": "高级家庭地图", "coletivo": "企业奖励",
        "nome_pet": "宠物名字", "nickname": "数字昵称", "nome_dominio": "域名",
        "nome_canal": "频道名称", "nome_equipe": "团队名称", "nome_ong": "非政府组织、协会、研究所或基金会名称",
        "nome_projeto": "项目名称", "nome_evento": "活动名称"},
    "ru": {"express": "Экспресс-карта", "vida": "Жизненный этап и год", "completo": "Полная карта",
        "ia": "ИИ-поиск имён", "urna": "Проверка названия бюллетеня", "eleitoral": "Избирательный номер",
        "imovel": "Номер недвижимости", "calendario": "Ежемесячный энергетический календарь",
        "artistico": "Проверка сценического имени", "bebe": "Планирование имени ребёнка",
        "assinatura": "Проверка подписей", "negocio": "Название для бизнеса/продукта",
        "casal": "Карта пары", "familia": "Премиальная семейная карта", "coletivo": "Корпоративный бонус",
        "nome_pet": "Имя питомца", "nickname": "Цифровой никнейм", "nome_dominio": "Имя домена",
        "nome_canal": "Название канала", "nome_equipe": "Название команды", "nome_ong": "Название НКО, ассоциации, института или фонда",
        "nome_projeto": "Название проекта", "nome_evento": "Название события"},
    "he": {"express": "מפה מהירה", "vida": "שלב חיים ושנה", "completo": "מפה מלאה",
        "ia": "חיפוש שמות AI", "urna": "אימות שם פתק", "eleitoral": "מספר בחירות",
        "imovel": "מספר נכס", "calendario": "לוח אנרגיה חודשי",
        "artistico": "אימות שם במה", "bebe": "תכנון שם לתינוק",
        "assinatura": "אימות חתימות", "negocio": "שם לעסק/מוצר",
        "nome_pet": "שם חיית המחמד", "nickname": "כינוי דיגיטלי", "nome_dominio": "שם דומיין",
        "nome_canal": "שם הערוץ", "nome_equipe": "שם הצוות", "nome_ong": "שם עמותה, ארגון, מכון או קרן",
        "nome_projeto": "שם הפרויקט", "nome_evento": "שם האירוע",
        "casal": "מפת זוג", "familia": "מפת משפחה פרימיום", "coletivo": "בונוס ארגוני"},
    "ar": {"express": "خريطة سريعة", "vida": "مرحلة الحياة والسنة", "completo": "خريطة كاملة",
        "ia": "بحث الأسماء بالذكاء الاصطناعي", "urna": "التحقق من اسم الاقتراع", "eleitoral": "الرقم الانتخابي",
        "imovel": "رقم العقار", "calendario": "تقويم الطاقة الشهري",
        "artistico": "التحقق من الاسم الفني", "bebe": "تخطيط اسم الطفل",
        "assinatura": "التحقق من التوقيعات", "negocio": "اسم للأعمال/المنتج",
        "casal": "خريطة الزوجين", "familia": "خريطة العائلة المميزة", "coletivo": "مكافأة الشركات",
        "nome_pet": "اسم الحيوان الأليف", "nickname": "اللقب الرقمي", "nome_dominio": "اسم النطاق",
        "nome_canal": "اسم القناة", "nome_equipe": "اسم الفريق", "nome_ong": "اسم منظمة أو جمعية أو معهد أو مؤسسة",
        "nome_projeto": "اسم المشروع", "nome_evento": "اسم الفعالية"},
    "id": {"express": "Peta Ekspres", "vida": "Tahap Hidup & Tahun", "completo": "Peta Lengkap",
        "ia": "Pencarian Nama AI", "urna": "Validasi Nama Surat Suara", "eleitoral": "Nomor Pemilihan",
        "imovel": "Nomor Properti", "calendario": "Kalender Energi Bulanan",
        "artistico": "Validasi Nama Artistik", "bebe": "Perencanaan Nama Bayi",
        "assinatura": "Validasi Tanda Tangan", "negocio": "Nama untuk Bisnis/Produk",
        "casal": "Peta Pasangan", "familia": "Peta Keluarga Premium", "coletivo": "Bonus Kolektif/Perusahaan",
        "nome_pet": "Nama Hewan Peliharaan", "nickname": "Nama Panggilan Digital", "nome_dominio": "Nama Domain",
        "nome_canal": "Nama Saluran", "nome_equipe": "Nama Tim", "nome_ong": "Nama LSM, Asosiasi, Institut atau Yayasan",
        "nome_projeto": "Nama Proyek", "nome_evento": "Nama Acara"},
    "tr": {"express": "Ekspres Harita", "vida": "Yaşam Evresi & Yıl", "completo": "Tam Harita",
        "ia": "AI İsim Arama", "urna": "Oy Pusulası Adı Doğrulama", "eleitoral": "Seçim Numarası",
        "imovel": "Mülk Numarası", "calendario": "Aylık Enerji Takvimi",
        "artistico": "Sanat Adı Doğrulama", "bebe": "Bebek Adı Planlama",
        "assinatura": "İmza Doğrulama", "negocio": "İşletme/Ürün Adı",
        "casal": "Çift Haritası", "familia": "Premium Aile Haritası", "coletivo": "Kolektif/Kurumsal Bonus",
        "nome_pet": "Evcil Hayvan Adı", "nickname": "Dijital Takma Ad", "nome_dominio": "Alan Adı",
        "nome_canal": "Kanal Adı", "nome_equipe": "Takım Adı", "nome_ong": "STK, Dernek, Enstitü veya Vakıf Adı",
        "nome_projeto": "Proje Adı", "nome_evento": "Etkinlik Adı"},
    "vi": {"express": "Bản đồ Nhanh", "vida": "Giai đoạn cuộc sống & Năm", "completo": "Bản đồ Đầy đủ",
        "ia": "Tìm kiếm tên AI", "urna": "Xác minh Tên Phiếu bầu", "eleitoral": "Số Bầu cử",
        "imovel": "Số Bất động sản", "calendario": "Lịch năng lượng hàng tháng",
        "artistico": "Xác minh Tên nghệ danh", "bebe": "Lên kế hoạch Tên bé",
        "assinatura": "Xác minh Chữ ký", "negocio": "Tên cho Doanh nghiệp/Sản phẩm",
        "casal": "Bản đồ Cặp đôi", "familia": "Bản đồ Gia đình Cao cấp", "coletivo": "Thưởng Tập thể/Doanh nghiệp",
        "nome_pet": "Tên Thú cưng", "nickname": "Biệt danh Kỹ thuật số", "nome_dominio": "Tên Miền",
        "nome_canal": "Tên Kênh", "nome_equipe": "Tên Đội nhóm", "nome_ong": "Tên Tổ chức phi chính phủ, Hiệp hội, Viện hoặc Quỹ",
        "nome_projeto": "Tên Dự án", "nome_evento": "Tên Sự kiện"}
}

# ===== TEXTOS DOS PDFS (14 IDIOMAS) =====
PDF_TEXTS = {
    "pt": {"t_express": "MAPA EXPRESS", "t_completo": "MAPA COMPLETO", "t_urna": "VALIDACAO DE NOME DE URNA", "t_eleitoral": "NUMERO ELEITORAL",
           "numero": "Numero", "valor": "Valor", "caminho": "Caminho de Vida", "expressao": "Expressao", "motivacao": "Motivacao", "personalidade": "Personalidade", "destino": "Destino",
           "cargo": "Cargo", "sugestoes": "Sugestoes:", "op8": "Opcoes com Energia 8 - IDEAL:", "op_alt": "Opcoes Alternativas:", "num_existente": "Numero existente",
           "ciclos": "Ciclo 1 (0-{a}a) | Ciclo 2 ({b}-{c}a) | Ciclo 3 ({d}+a)", "desafios": "Desafios: {x} | {y} | Principal {z}", "ano_pessoal": "Ano Pessoal {ano}: {v}",
           "grade": "Grade: Presentes {p} | Carencias {c}", "baixar": "BAIXAR PDF", "confirmado": "Confirmado!", "gerado": "Ola {nome}, seu {prod} foi gerado.",
           "voltar": "Voltar", "qr_titulo": "Seu PDF nao pode ser gerado.", "qr_instrucao": "Escaneie o QRCode abaixo para acessar seu documento.", "entrega": "Documento sigiloso - entrega por PDF/QRCode."},
    "en": {"t_express": "EXPRESS MAP", "t_completo": "COMPLETE MAP", "t_urna": "BALLOT NAME VALIDATION", "t_eleitoral": "ELECTORAL NUMBER",
           "numero": "Number", "valor": "Value", "caminho": "Life Path", "expressao": "Expression", "motivacao": "Soul Urge", "personalidade": "Personality", "destino": "Destiny",
           "cargo": "Position", "sugestoes": "Suggestions:", "op8": "Options with Energy 8 - IDEAL:", "op_alt": "Alternative Options:", "num_existente": "Existing number",
           "ciclos": "Cycle 1 (0-{a}) | Cycle 2 ({b}-{c}) | Cycle 3 ({d}+)", "desafios": "Challenges: {x} | {y} | Main {z}", "ano_pessoal": "Personal Year {ano}: {v}",
           "grade": "Grid: Present {p} | Missing {c}", "baixar": "DOWNLOAD PDF", "confirmado": "Confirmed!", "gerado": "Hello {nome}, your {prod} has been generated.",
           "voltar": "Back", "qr_titulo": "Your PDF could not be generated.", "qr_instrucao": "Scan the QR code below to access your document.", "entrega": "Confidential document - delivered via PDF/QRCode."},
    "es": {"t_express": "MAPA EXPRES", "t_completo": "MAPA COMPLETO", "t_urna": "VALIDACION NOMBRE DE URNA", "t_eleitoral": "NUMERO ELECTORAL",
           "numero": "Numero", "valor": "Valor", "caminho": "Camino de la Vida", "expressao": "Expresion", "motivacao": "Motivacion", "personalidade": "Personalidad", "destino": "Destino",
           "cargo": "Cargo", "sugestoes": "Sugerencias:", "op8": "Opciones con Energia 8 - IDEAL:", "op_alt": "Opciones Alternativas:", "num_existente": "Numero existente",
           "ciclos": "Ciclo 1 (0-{a}) | Ciclo 2 ({b}-{c}) | Ciclo 3 ({d}+)", "desafios": "Desafios: {x} | {y} | Principal {z}", "ano_pessoal": "Ano Personal {ano}: {v}",
           "grade": "Cuadricula: Presentes {p} | Ausentes {c}", "baixar": "DESCARGAR PDF", "confirmado": "Confirmado!", "gerado": "Hola {nome}, tu {prod} fue generado.",
           "voltar": "Volver", "qr_titulo": "Tu PDF no pudo generarse.", "qr_instrucao": "Escanea el codigo QR para acceder a tu documento.", "entrega": "Documento confidencial - entrega por PDF/QRCode."},
    "it": {"t_express": "MAPPA ESPRESSA", "t_completo": "MAPPA COMPLETA", "t_urna": "VALIDAZIONE NOME DELLA SCHEDA", "t_eleitoral": "NUMERO ELETTORALE",
           "numero": "Numero", "valor": "Valore", "caminho": "Sentiero della Vita", "expressao": "Espressione", "motivacao": "Spinta dell'Anima", "personalidade": "Personalita", "destino": "Destino",
           "cargo": "Carica", "sugestoes": "Suggerimenti:", "op8": "Opzioni con Energia 8 - IDEALE:", "op_alt": "Opzioni Alternative:", "num_existente": "Numero esistente",
           "ciclos": "Ciclo 1 (0-{a}) | Ciclo 2 ({b}-{c}) | Ciclo 3 ({d}+)", "desafios": "Sfide: {x} | {y} | Principale {z}", "ano_pessoal": "Anno Personale {ano}: {v}",
           "grade": "Griglia: Presenti {p} | Mancanti {c}", "baixar": "SCARICA PDF", "confirmado": "Confermato!", "gerado": "Ciao {nome}, il tuo {prod} e stato generato.",
           "voltar": "Indietro", "qr_titulo": "Il tuo PDF non puo essere generato.", "qr_instrucao": "Scansiona il QR code per accedere al documento.", "entrega": "Documento riservato - consegna via PDF/QRCode."},
    "fr": {"t_express": "CARTE EXPRESS", "t_completo": "CARTE COMPLETE", "t_urna": "VALIDATION NOM DU BULLETIN", "t_eleitoral": "NUMERO ELECTORAL",
           "numero": "Numero", "valor": "Valeur", "caminho": "Chemin de Vie", "expressao": "Expression", "motivacao": "Elan de l'Ame", "personalidade": "Personnalite", "destino": "Destin",
           "cargo": "Poste", "sugestoes": "Suggestions :", "op8": "Options avec Energie 8 - IDEAL :", "op_alt": "Options Alternatives :", "num_existente": "Numero existant",
           "ciclos": "Cycle 1 (0-{a}) | Cycle 2 ({b}-{c}) | Cycle 3 ({d}+)", "desafios": "Defis : {x} | {y} | Principal {z}", "ano_pessoal": "Annee Personnelle {ano} : {v}",
           "grade": "Grille : Presents {p} | Manquants {c}", "baixar": "TELECHARGER PDF", "confirmado": "Confirme !", "gerado": "Bonjour {nome}, votre {prod} a ete genere.",
           "voltar": "Retour", "qr_titulo": "Votre PDF n'a pas pu etre genere.", "qr_instrucao": "Scannez le QR code pour acceder a votre document.", "entrega": "Document confidentiel - livraison par PDF/QRCode."},
    "de": {"t_express": "EXPRESS-KARTE", "t_completo": "VOLLSTANDIGE KARTE", "t_urna": "STIMMZETTELNAME-VALIDIERUNG", "t_eleitoral": "WAHLNUMMER",
           "numero": "Zahl", "valor": "Wert", "caminho": "Lebensweg", "expressao": "Ausdruck", "motivacao": "Seelenwunsch", "personalidade": "Personlichkeit", "destino": "Schicksal",
           "cargo": "Position", "sugestoes": "Vorschlage:", "op8": "Optionen mit Energie 8 - IDEAL:", "op_alt": "Alternative Optionen:", "num_existente": "Bestehende Nummer",
           "ciclos": "Zyklus 1 (0-{a}) | Zyklus 2 ({b}-{c}) | Zyklus 3 ({d}+)", "desafios": "Herausforderungen: {x} | {y} | Haupt {z}", "ano_pessoal": "Persoenliches Jahr {ano}: {v}",
           "grade": "Raster: Vorhanden {p} | Fehlend {c}", "baixar": "PDF HERUNTERLADEN", "confirmado": "Bestaetigt!", "gerado": "Hallo {nome}, Ihr {prod} wurde erstellt.",
           "voltar": "Zurueck", "qr_titulo": "Ihr PDF konnte nicht erstellt werden.", "qr_instrucao": "Scannen Sie den QR-Code, um auf Ihr Dokument zuzugreifen.", "entrega": "Vertrauliches Dokument - Lieferung per PDF/QRCode."},
    "ja": {"t_express": "エクスプレスマップ", "t_completo": "完全マップ", "t_urna": "投票用紙名の検証", "t_eleitoral": "選挙番号",
           "numero": "数字", "valor": "値", "caminho": "ライフパス", "expressao": "表現", "motivacao": "魂の欲求", "personalidade": "性格", "destino": "運命",
           "cargo": "役職", "sugestoes": "提案:", "op8": "エネルギー8のオプション - 理想的:", "op_alt": "代替オプション:", "num_existente": "既存の番号",
           "ciclos": "サイクル1 (0-{a}) | サイクル2 ({b}-{c}) | サイクル3 ({d}+)", "desafios": "課題: {x} | {y} | 主要 {z}", "ano_pessoal": "パーソナルイヤー {ano}: {v}",
           "grade": "グリッド: あり {p} | 欠け {c}", "baixar": "PDFをダウンロード", "confirmado": "確認済み!", "gerado": "{nome} さん、{prod} が生成されました。",
           "voltar": "戻る", "qr_titulo": "PDFを生成できませんでした。", "qr_instrucao": "下のQRコードをスキャンして文書にアクセスしてください。", "entrega": "機密文書 - PDF/QRコードで納品。"},
    "zh": {"t_express": "快速地图", "t_completo": "完整地图", "t_urna": "选票名称验证", "t_eleitoral": "选举号码",
           "numero": "数字", "valor": "数值", "caminho": "生命路径", "expressao": "表达", "motivacao": "灵魂冲动", "personalidade": "个性", "destino": "命运",
           "cargo": "职位", "sugestoes": "建议:", "op8": "能量8选项 - 理想:", "op_alt": "备选方案:", "num_existente": "现有号码",
           "ciclos": "周期1 (0-{a}) | 周期2 ({b}-{c}) | 周期3 ({d}+)", "desafios": "挑战: {x} | {y} | 主要 {z}", "ano_pessoal": "个人年份 {ano}: {v}",
           "grade": "网格: 存在 {p} | 缺失 {c}", "baixar": "下载PDF", "confirmado": "已确认!", "gerado": "您好 {nome}，您的{prod}已生成。",
           "voltar": "返回", "qr_titulo": "无法生成PDF。", "qr_instrucao": "扫描下方二维码访问您的文档。", "entrega": "保密文档 - 通过PDF/二维码交付。"},
    "ru": {"t_express": "ЭКСПРЕСС-КАРТА", "t_completo": "ПОЛНАЯ КАРТА", "t_urna": "ПРОВЕРКА НАЗВАНИЯ БЮЛЛЕТЕНЯ", "t_eleitoral": "ИЗБИРАТЕЛЬНЫЙ НОМЕР",
           "numero": "Число", "valor": "Значение", "caminho": "Путь Жизни", "expressao": "Выражение", "motivacao": "Порыв Души", "personalidade": "Личность", "destino": "Судьба",
           "cargo": "Должность", "sugestoes": "Предложения:", "op8": "Варианты с Энергией 8 - ИДЕАЛ:", "op_alt": "Альтернативные варианты:", "num_existente": "Существующий номер",
           "ciclos": "Цикл 1 (0-{a}) | Цикл 2 ({b}-{c}) | Цикл 3 ({d}+)", "desafios": "Вызовы: {x} | {y} | Главный {z}", "ano_pessoal": "Личный год {ano}: {v}",
           "grade": "Сетка: Есть {p} | Нет {c}", "baixar": "СКАЧАТЬ PDF", "confirmado": "Подтверждено!", "gerado": "Здравствуйте {nome}, ваш {prod} создан.",
           "voltar": "Назад", "qr_titulo": "Не удалось создать PDF.", "qr_instrucao": "Отсканируйте QR-код ниже, чтобы получить доступ к документу.", "entrega": "Конфиденциальный документ - доставка через PDF/QRCode."},
    "he": {"t_express": "מפה מהירה", "t_completo": "מפה מלאה", "t_urna": "אימות שם פתק", "t_eleitoral": "מספר בחירות",
           "numero": "מספר", "valor": "ערך", "caminho": "נתיב החיים", "expressao": "ביטוי", "motivacao": "דחף הנשמה", "personalidade": "אישיות", "destino": "גורל",
           "cargo": "תפקיד", "sugestoes": "הצעות:", "op8": "אפשרויות עם אנרגיה 8 - אידיאלי:", "op_alt": "אפשרויות חלופיות:", "num_existente": "מספר קיים",
           "ciclos": "מחזור 1 (0-{a}) | מחזור 2 ({b}-{c}) | מחזור 3 ({d}+)", "desafios": "אתגרים: {x} | {y} | עיקרי {z}", "ano_pessoal": "שנה אישית {ano}: {v}",
           "grade": "רשת: קיימים {p} | חסרים {c}", "baixar": "הורד PDF", "confirmado": "אושר!", "gerado": "שלום {nome}, ה-{prod} שלך נוצר.",
           "voltar": "חזור", "qr_titulo": "לא ניתן היה ליצור את ה-PDF.", "qr_instrucao": "סרוק את קוד ה-QR למטה כדי לגשת למסמך שלך.", "entrega": "מסמך חסוי - מסירה באמצעות PDF/QRCode."},
    "ar": {"t_express": "خريطة سريعة", "t_completo": "خريطة كاملة", "t_urna": "التحقق من اسم الاقتراع", "t_eleitoral": "الرقم الانتخابي",
           "numero": "الرقم", "valor": "القيمة", "caminho": "مسار الحياة", "expressao": "التعبير", "motivacao": "دافع الروح", "personalidade": "الشخصية", "destino": "القدر",
           "cargo": "المنصب", "sugestoes": "اقتراحات:", "op8": "خيارات بالطاقة 8 - مثالي:", "op_alt": "خيارات بديلة:", "num_existente": "الرقم الموجود",
           "ciclos": "دورة 1 (0-{a}) | دورة 2 ({b}-{c}) | دورة 3 ({d}+)", "desafios": "التحديات: {x} | {y} | الرئيسي {z}", "ano_pessoal": "السنة الشخصية {ano}: {v}",
           "grade": "الشبكة: موجودة {p} | ناقصة {c}", "baixar": "تحميل PDF", "confirmado": "تم التأكيد!", "gerado": "مرحباً {nome}، تم إنشاء {prod} الخاص بك.",
           "voltar": "رجوع", "qr_titulo": "تعذر إنشاء ملف PDF الخاص بك.", "qr_instrucao": "امسح رمز QR أدناه للوصول إلى مستندك.", "entrega": "مستند سري - التسليم عبر PDF/QRCode."},
     "id": {"t_express": "PETA EKSPRES", "t_completo": "PETA LENGKAP", "t_urna": "VALIDASI NAMA SURAT SUARA", "t_eleitoral": "NOMOR PEMILIHAN",
           "numero": "Nomor", "valor": "Nilai", "caminho": "Jalan Hidup", "expressao": "Ekspresi", "motivacao": "Dorongan Jiwa", "personalidade": "Kepribadian", "destino": "Takdir",
           "cargo": "Jabatan", "sugestoes": "Saran:", "op8": "Opsi dengan Energi 8 - IDEAL:", "op_alt": "Opsi Alternatif:", "num_existente": "Nomor yang ada",
           "ciclos": "Siklus 1 (0-{a}) | Siklus 2 ({b}-{c}) | Siklus 3 ({d}+)", "desafios": "Tantangan: {x} | {y} | Utama {z}", "ano_pessoal": "Tahun Pribadi {ano}: {v}",
           "grade": "Kisi: Ada {p} | Kurang {c}", "baixar": "UNDUH PDF", "confirmado": "Dikonfirmasi!", "gerado": "Halo {nome}, {prod} Anda telah dibuat.",
           "voltar": "Kembali", "qr_titulo": "PDF Anda tidak dapat dibuat.", "qr_instrucao": "Pindai kode QR di bawah untuk mengakses dokumen Anda.", "entrega": "Dokumen rahasia - pengiriman via PDF/QRCode."},
     "tr": {"t_express": "EKSPRES HARITA", "t_completo": "TAM HARITA", "t_urna": "OY PUSLASINA ADI DOĞRULAMA", "t_eleitoral": "SEÇİM NUMARASI",
           "numero": "Sayı", "valor": "Değer", "caminho": "Yaşam Yolu", "expressao": "İfade", "motivacao": "Ruh Arzusu", "personalidade": "Kişilik", "destino": "Kader",
           "cargo": "Görev", "sugestoes": "Öneriler:", "op8": "Enerji 8'li Seçenekler - İDEAL:", "op_alt": "Alternatif Seçenekler:", "num_existente": "Mevcut numara",
           "ciclos": "Döngü 1 (0-{a}) | Döngü 2 ({b}-{c}) | Döngü 3 ({d}+)", "desafios": "Zorluklar: {x} | {y} | Ana {z}", "ano_pessoal": "Kişisel Yıl {ano}: {v}",
           "grade": "Izgara: Mevcut {p} | Eksik {c}", "baixar": "PDF İNDİR", "confirmado": "Onaylandı!", "gerado": "Merhaba {nome}, {prod} oluşturuldu.",
           "voltar": "Geri", "qr_titulo": "PDF'niz oluşturulamadı.", "qr_instrucao": "Belize erişmek için aşağıdaki QR kodunu tarayın.", "entrega": "Gizli belge - PDF/QRCode ile teslim."},
     "vi": {"t_express": "BẢN ĐỒ NHANH", "t_completo": "BẢN ĐỒ ĐẦY ĐỦ", "t_urna": "XÁC MINH TÊN PHIẾU BẦU", "t_eleitoral": "SỐ BẦU CỬ",
           "numero": "Số", "valor": "Giá trị", "caminho": "Đường đời", "expressao": "Biểu hiện", "motivacao": "Khao khát tâm", "personalidade": "Tính cách", "destino": "Số phận",
           "cargo": "Chức vụ", "sugestoes": "Gợi ý:", "op8": "Tùy chọn Năng lượng 8 - LÝ TƯỞNG:", "op_alt": "Tùy chọn Thay thế:", "num_existente": "Số hiện có",
           "ciclos": "Chu kỳ 1 (0-{a}) | Chu kỳ 2 ({b}-{c}) | Chu kỳ 3 ({d}+)", "desafios": "Thách thức: {x} | {y} | Chính {z}", "ano_pessoal": "Năm Cá nhân {ano}: {v}",
           "grade": "Lưới: Có {p} | Thiếu {c}", "baixar": "TẢI PDF", "confirmado": "Đã xác nhận!", "gerado": "Xin chào {nome}, {prod} của bạn đã được tạo.",
           "voltar": "Quay lại", "qr_titulo": "Không thể tạo PDF của bạn.", "qr_instrucao": "Quét mã QR bên dưới để truy cập tài liệu của bạn.", "entrega": "Tài liệu bí mật - giao qua PDF/QRCode."}
}
# ===== SEÇÕES DOS PDFS (14 IDIOMAS) =====
PDF_SECOES = {
    "pt": {"numeros_principais": "Seus Números Principais", "caminho_ciclos": "Caminho da Vida e Ciclos",
           "desafios_realizacoes": "Desafios e Realizações", "como_calculamos": "Como calculamos?",
           "por_que_energia_8": "Por que a energia 8?", "energia_8_ideal": "Energia 8 — IDEAL:", "alternativas": "Alternativas:"},
    "en": {"numeros_principais": "Your Main Numbers", "caminho_ciclos": "Life Path and Cycles",
           "desafios_realizacoes": "Challenges and Achievements", "como_calculamos": "How do we calculate?",
           "por_que_energia_8": "Why energy 8?", "energia_8_ideal": "Energy 8 — IDEAL:", "alternativas": "Alternatives:"},
    "es": {"numeros_principais": "Tus Números Principales", "caminho_ciclos": "Camino de la Vida y Ciclos",
           "desafios_realizacoes": "Desafíos y Logros", "como_calculamos": "¿Cómo calculamos?",
           "por_que_energia_8": "¿Por qué la energía 8?", "energia_8_ideal": "Energía 8 — IDEAL:", "alternativas": "Alternativas:"},
    "it": {"numeros_principais": "I Tuoi Numeri Principali", "caminho_ciclos": "Percorso di Vita e Cicli",
           "desafios_realizacoes": "Sfide e Traguardi", "como_calculamos": "Come calcoliamo?",
           "por_que_energia_8": "Perché l'energia 8?", "energia_8_ideal": "Energia 8 — IDEALE:", "alternativas": "Alternative:"},
    "fr": {"numeros_principais": "Vos Nombres Principaux", "caminho_ciclos": "Chemin de Vie et Cycles",
           "desafios_realizacoes": "Défis et Réalisations", "como_calculamos": "Comment calculons-nous ?",
           "por_que_energia_8": "Pourquoi l'énergie 8 ?", "energia_8_ideal": "Énergie 8 — IDÉAL :", "alternativas": "Alternatives :"},
    "de": {"numeros_principais": "Ihre Hauptzahlen", "caminho_ciclos": "Lebensweg und Zyklen",
           "desafios_realizacoes": "Herausforderungen und Erfolge", "como_calculamos": "Wie berechnen wir?",
           "por_que_energia_8": "Warum Energie 8?", "energia_8_ideal": "Energie 8 — IDEAL:", "alternativas": "Alternativen:"},
    "ja": {"numeros_principais": "あなたの主要な数字", "caminho_ciclos": "ライフパスと周期",
           "desafios_realizacoes": "課題と達成", "como_calculamos": "どう計算しますか？",
           "por_que_energia_8": "なぜエネルギー8なのか？", "energia_8_ideal": "エネルギー8 — 理想的:", "alternativas": "代替案:"},
    "zh": {"numeros_principais": "你的主要数字", "caminho_ciclos": "生命道路与周期",
           "desafios_realizacoes": "挑战与成就", "como_calculamos": "我们如何计算？",
           "por_que_energia_8": "为什么是能量8？", "energia_8_ideal": "能量8 — 理想:", "alternativas": "备选方案:"},
    "ru": {"numeros_principais": "Ваши главные числа", "caminho_ciclos": "Путь жизни и циклы",
           "desafios_realizacoes": "Вызовы и достижения", "como_calculamos": "Как мы считаем?",
           "por_que_energia_8": "Почему энергия 8?", "energia_8_ideal": "Энергия 8 — ИДЕАЛ:", "alternativas": "Альтернативы:"},
    "he": {"numeros_principais": "המספרים העיקריים שלך", "caminho_ciclos": "נתיב החיים ומחזורים",
           "desafios_realizacoes": "אתגרים והישגים", "como_calculamos": "איך אנחנו מחשבים?",
           "por_que_energia_8": "למה אנרגיה 8?", "energia_8_ideal": "אנרגיה 8 — אידיאלי:", "alternativas": "חלופות:"},
    "ar": {"numeros_principais": "أرقامك الرئيسية", "caminho_ciclos": "مسار الحياة والدورات",
           "desafios_realizacoes": "التحديات والإنجازات", "como_calculamos": "كيف نحسب؟",
           "por_que_energia_8": "لماذا الطاقة 8؟", "energia_8_ideal": "الطاقة 8 — مثالي:", "alternativas": "بدائل:"},
    "id": {"numeros_principais": "Angka Utama Anda", "caminho_ciclos": "Jalan Hidup dan Siklus",
           "desafios_realizacoes": "Tantangan dan Pencapaian", "como_calculamos": "Bagaimana kami menghitung?",
           "por_que_energia_8": "Mengapa energi 8?", "energia_8_ideal": "Energi 8 — IDEAL:", "alternativas": "Alternatif:"},
    "tr": {"numeros_principais": "Ana Numaralarınız", "caminho_ciclos": "Yaşam Yolu ve Döngüler",
           "desafios_realizacoes": "Zorluklar ve Başarılar", "como_calculamos": "Nasıl hep hesaplıyoruz?",
           "por_que_energia_8": "Neden enerji 8?", "energia_8_ideal": "Enerji 8 — İDEAL:", "alternativas": "Alternatifler:"},
    "vi": {"numeros_principais": "Các Số Chính của Bạn", "caminho_ciclos": "Đường đời và Chu kỳ",
           "desafios_realizacoes": "Thách thức và Thành đạt", "como_calculamos": "Chúng tôi tính như thế nào?",
           "por_que_energia_8": "Tại sao là năng lượng 8?", "energia_8_ideal": "Năng lượng 8 — LÝ TƯỞNG:", "alternativas": "Phương án thay thế:"}
}

# ===== BOAS-VINDAS, PERIODOS E CABEÇALHOS DE REALIZAÇÕES (14 IDIOMAS) =====
BOAS_VINDAS = {
    "pt": "Seja bem-vindo(a)! Este relatório revela as energias que moldam a sua essência. Que a sabedoria dos números ilumine o seu caminho.",
    "en": "Welcome! This report reveals the energies that shape your essence. May the wisdom of numbers illuminate your path.",
    "es": "¡Bienvenido(a)! Este informe revela las energías que moldean tu esencia. Que la sabiduría de los números ilumine tu camino.",
    "it": "Benvenuto/a! Questo report rivela le energie che plasmano la tua essenza. Che la saggezza dei numeri illumini il tuo cammino.",
    "fr": "Bienvenue ! Ce rapport révèle les énergies qui façonnent votre essence. Que la sagesse des nombres éclaire votre chemin.",
    "de": "Willkommen! Dieser Bericht offenbart die Energien, die Ihr Wesen prägen. Möge die Weisheit der Zahlen Ihren Weg erhellen.",
    "ja": "ようこそ！このレポートは、あなたの本質を形作るエネルギーを明らかにします。数字の叡智があなたの道を照らしますように。",
    "zh": "欢迎！这份报告揭示了塑造您本质的能量。愿数字的智慧照亮您的道路。",
    "ru": "Добро пожаловать! Этот отчёт раскрывает энергии, формирующие вашу сущность. Пусть мудрость чисел осветит ваш путь.",
    "he": "ברוכים הבאים! דוח זה חושף את האנרגיות המעצבות את מהותכם. שתיאיר חכמת המספרים את דרככם.",
    "ar": "مرحباً بك! يكشف هذا التقرير الطاقات التي تشكل جوهرك. لتنير حكمة الأرقام طريقك.",
    "id": "Selamat datang! Laporan ini mengungkap energi yang membentuk esensi Anda. Semoga kebijaksanaan angka mencerahkan jalan Anda.",
    "tr": "Hoş geldiniz! Bu rapor özünüzü şekillendiren enerjileri ortaya koyar. Sayıların bilgeliği yolunuzu aydınlatsın.",
    "vi": "Chào bạn! Báo cáo này tiết lộ những năng lượng định hình bản chất của bạn. Cầu trí tuệ của các con số soi sáng con đường của bạn."
}
PERIODOS = {
    "pt": ("0 a 28/36 anos", "28/36 a 54/63 anos", "54/63 anos em diante"),
    "en": ("0 to 28/36 years", "28/36 to 54/63 years", "54/63 years and beyond"),
    "es": ("0 a 28/36 años", "28/36 a 54/63 años", "54/63 años en adelante"),
    "it": ("0-28/36 anni", "28/36-54/63 anni", "54/63 anni in poi"),
    "fr": ("0 à 28/36 ans", "28/36 à 54/63 ans", "54/63 ans et plus"),
    "de": ("0 bis 28/36 Jahre", "28/36 bis 54/63 Jahre", "54/63 Jahre und mehr"),
    "ja": ("0〜28/36歳", "28/36〜54/63歳", "54/63歳以上"),
    "zh": ("0至28/36岁", "28/36至54/63岁", "54/63岁以上"),
    "ru": ("0-28/36 лет", "28/36-54/63 лет", "54/63 лет и старше"),
    "he": ("0-28/36 שנים", "28/36-54/63 שנים", "54/63 ומעלה"),
    "ar": ("0-28/36 سنة", "28/36-54/63 سنة", "54/63 سنة فأكثر"),
    "id": ("0-28/36 tahun", "28/36-54/63 tahun", "54/63 tahun ke atas"),
    "tr": ("0-28/36 yıl", "28/36-54/63 yıl", "54/63 yıl ve üzeri"),
    "vi": ("0-28/36 tuổi", "28/36-54/63 tuổi", "54/63 tuổi trở lên")
}
REALIZ_HEAD = {
    "pt": ("Fase", "Período"), "en": ("Phase", "Period"), "es": ("Fase", "Período"),
    "it": ("Fase", "Periodo"), "fr": ("Phase", "Période"), "de": ("Phase", "Zeitraum"),
    "ja": ("段階", "期間"), "zh": ("阶段", "时期"), "ru": ("Этап", "Период"),
    "he": ("שלב", "תקופה"), "ar": ("المرحلة", "الفترة"), "id": ("Fase", "Periode"),
    "tr": ("Aşama", "Dönem"), "vi": ("Giai đoạn", "Thời kỳ")
}

# ===== AMOR_TXT — DISTINÇÃO 5 E 6 NO AMOR (12 IDIOMAS) =====
# REGRA DE OURO: 5 = amor romântico/paixão | 6 = amor espiritual/humanitário
AMOR_TXT = {
    5: {
        "pt": "No amor, o 5 é paixão e sensualidade: atração intensa, sedução e desejo de liberdade afetiva.",
        "en": "In love, 5 is passion and sensuality: intense attraction, seduction and a desire for affective freedom.",
        "es": "En el amor, el 5 es pasión y sensualidad: atracción intensa, seducción y deseo de libertad afectiva.",
        "it": "In amore, il 5 è passione e sensualità: attrazione intensa, seduzione e desiderio di libertà affettiva.",
        "fr": "En amour, le 5 est passion et sensualité : attraction intense, séduction et désir de liberté affective.",
        "de": "In der Liebe ist die 5 Leidenschaft und Sinnlichkeit: intensive Anziehung, Verführung und Freiheitsdrang.",
        "ja": "恋愛において5は情熱と官能性：激しい魅力、誘惑、そして自由な愛の欲求。",
        "zh": "在爱情中，5是激情与感官：强烈的吸引、诱惑以及对情感自由的渴望。",
        "ru": "В любви 5 — это страсть и чувственность: сильное влечение, соблазн и стремление к свободе чувств.",
        "he": "באהבה, 5 הוא תשוקה וחושניות: משיכה עוצמתית, פיתוי ורצון לחופש רגשי.",
        "ar": "في الحب، 5 هو شغف وحسية: انجذاب شديد وإغراء ورغبة في الحرية العاطفية.",
        "id": "Dalam cinta, 5 adalah gairah dan sensualitas: daya tarik yang kuat, godaan, dan keinginan akan kebebasan afektif.",
        "tr": "Aşkta 5, tutku ve şehvettir: yoğun çekim, baştan çıkarma ve duygusal özgürlük arzusu.",
        "vi": "Trong tình yêu, 5 là đam mê và gợi cảm: sự hấp dẫn mãnh liệt, quyến rũ và khao khát tự do tình cảm."
    },
    6: {
        "pt": "No amor, o 6 é amor humano e solidário: cuidado, compaixão, família e responsabilidade afetiva.",
        "en": "In love, 6 is human and solidary love: care, compassion, family and affective responsibility.",
        "es": "En el amor, el 6 es amor humano y solidario: cuidado, compasión, familia y responsabilidad afectiva.",
        "it": "In amore, il 6 è amore umano e solidale: cura, compassione, famiglia e responsabilità affettiva.",
        "fr": "En amour, le 6 est amour humain et solidaire : soin, compassion, famille et responsabilité affective.",
        "de": "In der Liebe ist die 6 menschliche und solidarische Liebe: Fürsorge, Mitgefühl, Familie und Verantwortung.",
        "ja": "恋愛において6は人間的で連帯する愛：思いやり、慈愛、家族、そして感情的な責任。",
        "zh": "在爱情中，6是人文与团结之爱：关怀、同情、家庭与情感责任。",
        "ru": "В любви 6 — это человеческая и солидарная любовь: забота, сострадание, семья и эмоциональная ответственность.",
        "he": "באהבה, 6 הוא אהבה אנושית ומלאת סולידריות: אכפתיות, חמלה, משפחה ואחריות רגשית.",
        "ar": "في الحب، 6 هو حب إنساني وتضامني: رعاية ورحمة وأسرة ومسؤولية عاطفية.",
        "id": "Dalam cinta, 6 adalah cinta manusiawi dan solidaritas: kepedulian, kasih sayang, keluarga, dan tanggung jawab afetif.",
        "tr": "Aşkta 6, insani ve dayanışmacı sevgidir: şefkat, merhamet, aile ve duygusal sorumluluk.",
        "vi": "Trong tình yêu, 6 là tình yêu nhân văn và đoàn kết: sự quan tâm, lòng trắc ẩn, gia đình và trách nhiệm tình cảm."
    }
}

# ===== ENERGIAS_TXT — DESCRIÇÕES DAS ENERGIAS 1 A 9 (14 IDIOMAS) =====
# Cards da seção "Energias de Pesquisa" + alimenta PDFs. 5 e 6 trazem a distinção do amor.
ENERGIAS_TXT = {
    1: {
        "pt": "Liderança: coragem, pioneirismo e inspiração.",
        "en": "Leadership: courage, pioneering and inspiration.",
        "es": "Liderazgo: coraje, pionerismo e inspiración.",
        "it": "Leadership: coraggio, spirito pionieristico e ispirazione.",
        "fr": "Leadership : courage, esprit pionnier et inspiration.",
        "de": "Führung: Mut, Pioniergeist und Inspiration.",
        "ja": "リーダーシップ：勇気、開拓者精神、ひらめき。",
        "zh": "领导力：勇气、开拓精神与灵感。",
        "ru": "Лидерство: смелость, первопроходчество и вдохновение.",
        "he": "מנהיגות: אומץ, חלוציות והשראה.",
        "ar": "القيادة: شجاعة وريادة وإلهام.",
        "id": "Kepemimpinan: keberanian, jiwa perintis, dan inspirasi.",
        "tr": "Liderlik: cesaret, öncülük ve ilham.",
        "vi": "Lãnh đạo: lòng dũng cảm, tinh thần tiên phong và cảm hứng."
    },
    2: {
        "pt": "Cooperação: diplomacia, sensibilidade e união.",
        "en": "Cooperation: diplomacy, sensitivity and union.",
        "es": "Cooperación: diplomacia, sensibilidad y unión.",
        "it": "Cooperazione: diplomazia, sensibilità e unione.",
        "fr": "Coopération : diplomatie, sensibilité et union.",
        "de": "Zusammenarbeit: Diplomatie, Feingefühl und Einheit.",
        "ja": "協力：外交、感受性、団結。",
        "zh": "合作：外交、敏感与团结。",
        "ru": "Сотрудничество: дипломатия, чуткость и единство.",
        "he": "שיתוף פעולה: דיפלומטיה, רגישות ואחדות.",
        "ar": "التعاون: دبلوماسية وحساسية واتحاد.",
        "id": "Kerja Sama: diplomasi, kepekaan, dan persatuan.",
        "tr": "İşbirliği: diplomasi, hassasiyet ve birlik.",
        "vi": "Hợp tác: ngoại giao, nhạy cảm và đoàn kết."
    },
    3: {
        "pt": "Criatividade: expressão, comunicação e otimismo.",
        "en": "Creativity: expression, communication and optimism.",
        "es": "Creatividad: expresión, comunicación y optimismo.",
        "it": "Creatività: espressione, comunicazione e ottimismo.",
        "fr": "Créativité : expression, communication et optimisme.",
        "de": "Kreativität: Ausdruck, Kommunikation und Optimismus.",
        "ja": "創造性：表現、コミュニケーション、楽観。",
        "zh": "创造力：表达、沟通与乐观。",
        "ru": "Творчество: выражение, общение и оптимизм.",
        "he": "יצירתיות: ביטוי, תקשורת ואופטימיות.",
        "ar": "الإبداع: تعبير وتواصل وتفاؤل.",
        "id": "Kreativitas: ekspresi, komunikasi, dan optimisme.",
        "tr": "Yaratıcılık: ifade, iletişim ve iyimserlik.",
        "vi": "Sáng tạo: biểu đạt, giao tiếp và lạc quan."
    },
    4: {
        "pt": "Estrutura: organização, disciplina e segurança.",
        "en": "Structure: organization, discipline and security.",
        "es": "Estructura: organización, disciplina y seguridad.",
        "it": "Struttura: organizzazione, disciplina e sicurezza.",
        "fr": "Structure : organisation, discipline et sécurité.",
        "de": "Struktur: Organisation, Disziplin und Sicherheit.",
        "ja": "構造：組織、規律、安全。",
        "zh": "结构：组织、纪律与安全。",
        "ru": "Структура: организация, дисциплина и безопасность.",
        "he": "מבנה: ארגון, משמעת וביטחון.",
        "ar": "البنية: تنظيم وانضباط وأمان.",
        "id": "Struktur: organisasi, disiplin, dan keamanan.",
        "tr": "Yapı: organizasyon, disiplin ve güvenlik.",
        "vi": "Cấu trúc: tổ chức, kỷ luật và an toàn."   
    },
    5: {
        "pt": "Liberdade: aventura, adaptabilidade e versatilidade. O 5 fala do amor romântico/paixão.",
        "en": "Freedom: adventure, adaptability and versatility. 5 speaks of romantic/passionate love.",
        "es": "Libertad: aventura, adaptabilidad y versatilidad. El 5 habla del amor romántico/pasión.",
        "it": "Libertà: avventura, adattabilità e versatilità. Il 5 parla dell'amore romantico/passione.",
        "fr": "Liberté : aventure, adaptabilité et polyvalence. Le 5 parle de l'amour romantique/passion.",
        "de": "Freiheit: Abenteuer, Anpassungsfähigkeit und Vielseitigkeit. Die 5 spricht von romantischer/leidenschaftlicher Liebe.",
        "ja": "自由：冒険、適応力、多才。5はロマンチックな愛・情熱を語ります。",
        "zh": "自由：冒险、适应与多才。5代表浪漫/激情之爱。",
        "ru": "Свобода: приключения, адаптивность и универсальность. 5 говорит о романтической/страстной любви.",
        "he": "חופש: הרפתקאות, יכולת הסתגלות ורב-גוניות. 5 מדבר על אהבה רומנטית/תשוקה.",
        "ar": "الحرية: مغامرة وتكيف وتعدد مواهب. 5 يتحدث عن الحب الرومانسي/الشغف.",
        "id": "Kebebasan: petualangan, kemampuan beradaptasi, dan keserbagunaan. 5 berbicara tentang cinta romantis/gairah.",
        "tr": "Özgürlük: macera, uyum sağlama ve çok yönlülük. 5, romantik/tutkulu aşktan söz eder.",
        "vi": "Tự do: phiêu lưu, khả năng thích nghi và linh hoạt. Số 5 nói về tình yêu lãng mạn/đam mê."
    },
    6: {
        "pt": "Harmonia: amor humano, compaixão e responsabilidade. O 6 fala do amor espiritual/humanitário.",
        "en": "Harmony: human love, compassion and responsibility. 6 speaks of spiritual/humanitarian love.",
        "es": "Armonía: amor humano, compasión y responsabilidad. El 6 habla del amor espiritual/humanitario.",
        "it": "Armonia: amore umano, compassione e responsabilità. Il 6 parla dell'amore spirituale/umanitario.",
        "fr": "Harmonie : amour humain, compassion et responsabilité. Le 6 parle de l'amour spirituel/humanitaire.",
        "de": "Harmonie: menschliche Liebe, Mitgefühl und Verantwortung. Die 6 spricht von spiritueller/humanitärer Liebe.",
        "ja": "調和：人間愛、慈愛、責任。6は精神的な愛・人道を語ります。",
        "zh": "和谐：人文之爱、同情与责任。6代表精神/人道之爱。",
        "ru": "Гармония: человеческая любовь, сострадание и ответственность. 6 говорит о духовной/гуманитарной любви.",
        "he": "הרמוניה: אהבה אנושית, חמלה ואחריות. 6 מדבר על אהבה רוחנית/הומניטרית.",
        "ar": "الانسجام: حب إنساني ورحمة ومسؤولية. 6 يتحدث عن الحب الروحي/الإنساني.",
        "id": "Harmoni: cinta manusiawi, kasih sayang, dan tanggung jawab. 6 berbicara tentang cinta spiritual/kemanusiaan.",
        "tr": "Uyum: insani sevgi, şefkat ve sorumluluk. 6, manevi/insani aşktan söz eder.",
        "vi": "Hòa hợp: tình yêu nhân văn, lòng trắc ẩn và trách nhiệm. Số 6 nói về tình yêu tâm linh/nhân đạo."
    },
    7: {
        "pt": "Espiritualidade: introspecção, sabedoria e profundidade.",
        "en": "Spirituality: introspection, wisdom and depth.",
        "es": "Espiritualidad: introspección, sabiduría y profundidad.",
        "it": "Spiritualità: introspezione, saggezza e profondità.",
        "fr": "Spiritualité : introspection, sagesse et profondeur.",
        "de": "Spiritualität: Innenschau, Weisheit und Tiefe.",
        "ja": "精神性：内省、知恵、深み。",
        "zh": "灵性：内省、智慧与深度。",
        "ru": "Духовность: самоанализ, мудрость и глубина.",
        "he": "רוחניות: התבוננות פנימית, חוכמה ועומק.",
        "ar": "الروحانية: استبطان وحكمة وعمق.",
        "id": "Spiritualitas: introspeksi, kebijaksanaan, dan kedalaman.",
        "tr": "Maneviyat: içe dönüş, bilgelik ve derinlik.",
        "vi": "Tâm linh: nội tâm, trí tuệ và chiều sâu." 
    },
    8: {
        "pt": "Poder: realização, autoridade e prosperidade.",
        "en": "Power: achievement, authority and prosperity.",
        "es": "Poder: logro, autoridad y prosperidad.",
        "it": "Potere: realizzazione, autorità e prosperità.",
        "fr": "Pouvoir : accomplissement, autorité et prospérité.",
        "de": "Macht: Leistung, Autorität und Wohlstand.",
        "ja": "力：達成、権威、豊かさ。",
        "zh": "力量：成就、权威与丰盛。",
        "ru": "Сила: достижение, власть и процветание.",
        "he": "כוח: הישג, סמכות ושפע.",
        "ar": "القوة: إنجاز وسلطة وازدهار.",
        "id": "Kekuatan: pencapaian, otoritas, dan kemakmuran.",
        "tr": "Güç: başarı, otorite ve refah.",
        "vi": "Sức mạnh: thành tựu, quyền uy và thịnh vượng."
    },
    9: {
        "pt": "Humanitarismo: compaixão, conclusão e serviço ao todo.",
        "en": "Humanitarianism: compassion, completion and service to all.",
        "es": "Humanitarismo: compasión, conclusión y servicio al todo.",
        "it": "Umanitarismo: compassione, compimento e servizio al tutto.",
        "fr": "Humanitarisme : compassion, achèvement et service au tout.",
        "de": "Humanitarismus: Mitgefühl, Vollendung und Dienst am Ganzen.",
        "ja": "人道主義：思いやり、完結、全体への奉仕。",
        "zh": "人道主义：同情、圆满与服务整体。",
        "ru": "Гуманизм: сострадание, завершение и служение целому.",
        "he": "הומניטריות: חמלה, השלמה ושירות לכלל.",
        "ar": "الإنسانية: رحمة وإنجاز وخدمة الكل.",
        "id": "Humanitarianisme: kasih sayang, penyelesaian, dan pelayanan kepada keseluruhan.",
        "tr": "İnsaniyet: şefkat, tamamlama ve bütüne hizmet.",
        "vi": "Nhân đạo: lòng trắc ẩn, hoàn thành và phục vụ tổng thể."
    }
}

# ============================================================
# EXPRESS_TXT — MAPA EXPRESS
# Derivado do SIG (Monique Cissay). Sem aprofundamento:
# 1 frase por campo. O SIG completo fica para o Mapa Completo.
# Assinatura idêntica ao SIG: (titulo, positivo, negativo, licao)
# ============================================================
EXPRESS_TXT = {
    "pt": {
        1: ("Individualidade",
            "Original, criativo, líder nato e independente — energia do início e do impulso criador.",
            "Egoísta, arrogante e impulsivo — tende a centralizar decisões e não delegar.",
            "Desenvolver humildade: a liderança verdadeira inspira, não impõe."),

        2: ("Associação",
            "Diplomata, sensível e pacificador — sua presença acalma e harmoniza ambientes.",
            "Indeciso, carente e dependente da opinião alheia — evita conflitos a qualquer custo.",
            "Desenvolver autoconfiança: sua sensibilidade é um dom, não uma fraqueza."),

        3: ("Criação",
            "Criativo, comunicativo e otimista — tem o dom da palavra e da expressão artística.",
            "Superficial, disperso e exagerado — espalha energia sem concluir projetos.",
            "Desenvolver foco: qualidade sobre quantidade."),

        4: ("Trabalho",
            "Prático, disciplinado e confiável — é o alicerce de qualquer projeto ou equipe.",
            "Rígido, teimoso e resistente a inovações — pode perder oportunidades por medo do novo.",
            "Desenvolver flexibilidade: a vida também pede espontaneidade."),

        5: ("Liberdade",
            "Versátil, aventureiro e magnético — tem sede de vida e de experiências.",
            "Impulsivo, irresponsável e inconsequente — pode ferir quem ama com sua imprevisibilidade.",
            "Equilibrar liberdade com responsabilidade: a verdadeira liberdade inclui respeito pelo outro."),

        6: ("Família",
            "Responsável, amoroso e protetor — é o pilar emocional dos seus.",
            "Superprotetor e intrometido — tende a querer controlar por amor.",
            "Amar sem controlar: cuidar de si também é cuidar dos outros."),

        7: ("Sabedoria",
            "Sábio, analítico e espiritual — busca a verdade onde ninguém mais olha.",
            "Frio, sarcástico e isolado — pode se sentir superior intelectualmente.",
            "Equilibrar razão e emoção: a sabedoria só tem valor quando compartilhada."),

        8: ("Poder",
            "Poderoso, realizador e próspero — nasceu para liderar e construir riqueza.",
            "Materialista, autoritário e workaholic — pode sacrificar pessoas em nome do sucesso.",
            "Usar o poder com integridade: o verdadeiro sucesso é medido pelo bem que se faz."),

        9: ("Humanidade",
            "Humanitário, generoso e compassivo — enxerga o quadro maior da existência.",
            "Melancólico e disperso — tende a fugir da realidade concreta.",
            "Perdoar e deixar ir: o desapego é libertador."),

        11: ("Mestre Inspirador",
            "Intuitivo, iluminado e visionário — canaliza energias superiores.",
            "Ansioso, nervoso e distante — a pressão da alta vibração é difícil de suportar.",
            "Equilibrar o mundo espiritual com o material: aterrar os insights."),

        22: ("Mestre Construtor",
            "Realizador e visionário prático — transforma sonhos em realidade em larga escala.",
            "Ambicioso excessivo e prepotente — o peso do grande potencial pode esmagar.",
            "Construir sem escravizar-se ao trabalho: grandes obras precisam de um mestre em paz."),
    }
}

# =====================================================================
# SIG - Significados completos dos números (Monique Cissay)
# Cada entrada: (Título, Aspectos Positivos, Aspectos Negativos, Lição)
# =====================================================================
SIG = {
    1: ("Individualidade",
        "Símbolo: Círculo. Dia: Domingo. Planeta: Sol. Elemento: Fogo. Cor: Amarelo. Órgãos: Coração. "
        "Original, criativo, líder nato, independente, forte, determinado, pioneiro. Energia do começo, "
        "do impulso criador. Pessoas com este número são visionárias que não têm medo de trilhar caminhos "
        "novos. Têm iniciativa própria e não depende de outros para agir. Quando canalizada positivamente, "
        "esta energia constrói impérios e revoluciona paradigmas. Sua presença é marcante e sua determinação inabalável.",
        "Egoísta, arrogante, dominador, impulsivo, teimoso, impaciente. Tende a centralizar decisões e "
        "não delegar. Pode se tornar autoritário e inflexível, afastando aqueles que poderiam colaborar "
        "com seus projetos. O excesso de individualidade pode isolá-lo e prejudicar suas relações.",
        "Desenvolver humildade e saber trabalhar em equipe. Lembrar que ninguém realiza grandes feitos "
        "sozinho. A liderança verdadeira inspira, não impõe. Compartilhar o protagonismo amplia seu poder "
        "de realização e constrói legados duradouros."),
    2: ("Associação",
        "Símbolo: Semicírculo. Dia: Segunda-feira. Planeta: Lua. Elemento: Água. Cor: Verde. "
        "Diplomata, sensível, cooperativo, pacificador, intuitivo, detalhista, bom ouvinte. Sua presença "
        "acalma e harmoniza ambientes. Tem o dom de unir pessoas e encontrar soluções que agradam a todos. "
        "Sua intuição é refinada e raramente se engana sobre as pessoas. É o fio de ouro que tece relações "
        "duradouras e significativas.",
        "Indeciso, carente, submisso, hipersensível, dependente da opinião alheia, tímido. Evita conflitos "
        "a qualquer custo, mesmo quando necessário se posicionar. Pode se anular em relações para manter "
        "a paz aparente, o que gera frustração interna.",
        "Desenvolver autoconfiança e independência emocional. Dizer não quando necessário. Sua sensibilidade "
        "é um dom, não uma fraqueza. A verdadeira paz vem do equilíbrio interno, não da aprovação externa."),
    3: ("Criação",
        "Símbolo: Triângulo. Dia: Terça-feira. Planeta: Júpiter. Elemento: Ar. Cor: Violeta. "
        "Criativo, comunicativo, otimista, carismático, talentoso para artes. Ilumina qualquer ambiente "
        "com sua presença. Tem o dom da palavra e da expressão artística. Sua energia é contagiante e "
        "atrai pessoas naturalmente. É a personificação da alegria de viver e da criatividade sem limites.",
        "Superficial, disperso, exagerado, dramático. Tende a espalhar energia em muitas direções sem "
        "concluir projetos. Pode usar o talento dramático para manipular situações e pessoas.",
        "Desenvolver foco e profundidade na expressão. Canalizar tanto talento para uma direção específica. "
        "Qualidade sobre quantidade."),
    4: ("Trabalho",
        "Símbolo: Quadrado. Dia: Quarta-feira. Planeta: Urano. Elemento: Terra. Cor: Azul. "
        "Prático, disciplinado, confiável, leal, persistente, organizado, eficiente, dedicado, honesto. "
        "É o alicerce de qualquer projeto ou equipe. Não desiste até ver o trabalho bem feito. Valoriza "
        "a estabilidade e a segurança acima de tudo. Sua solidez inspira confiança em todos ao redor.",
        "Rígido, teimoso, lento para mudar, materialista em excesso, resistente a inovações. Pode se "
        "prender a rotinas desnecessárias e perder oportunidades por medo do novo.",
        "Desenvolver flexibilidade e leveza. Nem tudo precisa ser tão sério. A vida também pede "
        "espontaneidade. Confie mais no fluxo da vida."),
    5: ("Liberdade",
        "Símbolo: Estrela. Dia: Quinta-feira. Planeta: Mercúrio. Elemento: Ar. Cor: Laranja. "
        "Livre, versátil, aventureiro, progressista, inteligente, curioso, adaptável, magnético. "
        "Sua energia é contagiante e atrai pessoas e situações novas com facilidade. Tem sede de vida "
        "e de experiências. É a personificação da liberdade e da exploração.",
        "Impulsivo, irresponsável, ansioso, inconsequente, excessivo em prazeres. Pode ferir quem ama "
        "com sua imprevisibilidade. O excesso de liberdade pode se tornar libertinagem.",
        "Equilibrar liberdade com responsabilidade. A verdadeira liberdade inclui respeito pelo outro. "
        "Buscar consistência sem perder a essência."),
    6: ("Família",
        "Símbolo: Hexágono. Dia: Sexta-feira. Planeta: Vênus. Elemento: Terra. Cor: Rosa. "
        "Responsável, amoroso, protetor, justo, compassivo, artístico, conselheiro nato. É o pilar "
        "emocional dos seus. Tem um senso de justiça aguçado e não mede esforços para proteger quem ama.",
        "Superprotetor, intrometido, ansioso com os outros. Tende a querer controlar por amor. Pode se "
        "sentir responsável por problemas que não são seus.",
        "Amar sem controlar. Respeitar o espaço alheio. Cuidar de si também é cuidar dos outros. "
        "O amor verdadeiro é liberdade."),
    7: ("Sabedoria",
        "Símbolo: Heptágono. Dia: Sábado. Planeta: Netuno. Elemento: Água. Cor: Índigo. "
        "Sábio, analítico, espiritual, intuitivo, perfeccionista, reservado, filósofo, mente brilhante. "
        "Busca a verdade onde ninguém mais olha. Tem uma conexão profunda com o invisível.",
        "Frio, sarcástico, isolado, desconfiado. Pode se sentir superior intelectualmente. "
        "A solidão pode se transformar em amargura.",
        "Equilibrar razão e emoção. Compartilhar conhecimento. A sabedoria só tem valor quando compartilhada."),
    8: ("Poder",
        "Símbolo: Octógono. Dia: Domingo. Planeta: Saturno. Elemento: Terra. Cor: Vermelho. "
        "Poderoso, realizador, próspero, estrategista, ambicioso, visionário. Nasceu para liderar "
        "e construir riqueza. Transforma visão em realidade com eficiência. Atrai o sucesso naturalmente.",
        "Materialista, autoritário, workaholic, impaciente. Pode sacrificar pessoas em nome do sucesso. "
        "O poder sem ética corrompe.",
        "Usar o poder com integridade. O verdadeiro sucesso é medido pelo bem que se faz. "
        "Dinheiro é meio, não fim."),
    9: ("Humanidade",
        "Símbolo: Nonágono. Dia: Terça-feira. Planeta: Marte. Elemento: Fogo. Cor: Carmim. "
        "Humanitário, generoso, compassivo, sábio, tolerante, inspirador, altruísta. Enxerga o quadro "
        "maior da existência. Sua alma é velha e carrega sabedoria de muitas vidas.",
        "Melancólico, disperso, vitimista. Tende a fugir da realidade concreta. Refugia-se em ideais "
        "inalcançáveis.",
        "Perdoar e deixar ir. Confiar no fluxo da vida. O desapego é libertador. Cuidar de si para "
        "cuidar do mundo."),
    11: ("Mestre Inspirador",
        "Intuitivo, iluminado, inspirador, visionário. Canaliza energias superiores. Acesso ao "
        "conhecimento além do racional. Presença magnética e inspiradora. Eleva todos ao seu redor "
        "com sua luz interior.",
        "Ansioso, nervoso, distante, fanático. A pressão da alta vibração é difícil de suportar. "
        "Pode sentir-se incompreendido e deslocado.",
        "Equilibrar o mundo espiritual com o material. Aterrar os insights. Cuidar do corpo tanto "
        "quanto do espírito."),
    22: ("Mestre Construtor",
        "Realizador, visionário prático. Capaz de transformar sonhos em realidade em larga escala. "
        "Combina visão espiritual com ação concreta. Potencial ilimitado. É o arquiteto do futuro, "
        "construindo obras que beneficiam a humanidade.",
        "Ambicioso excessivo, estressado, prepotente. O peso do grande potencial pode esmagar e "
        "levar ao esgotamento.",
        "Construir sem escravizar-se ao trabalho. O equilíbrio entre fazer e ser. Grandes obras "
        "precisam de um mestre em paz."),
    33: ("Mestre Amoroso",
        "Amor incondicional, compaixão universal, cura emocional. Mestre do amor e da luz. "
        "Eleva todos ao seu redor.",
        "Sobrecarregado emocionalmente, mártir. Pode absorver dores alheias.",
        "Amar sem se sacrificar. Cuidar do corpo tanto quanto do espírito.")
}

# =====================================================================
# CAM - Caminhos de Vida (descrição + exemplos históricos)
# =====================================================================
CAM = {
    1: ("Realização",
        "Sua missão é abrir caminhos, liderar e inovar. Você veio ao mundo para ser pioneiro, para "
        "criar oportunidades onde antes não existiam. Tem coragem, força de vontade e determinação para "
        "alcançar grandes feitos. Seu maior desafio é aprender que liderar também significa servir e "
        "inspirar outros a brilhar. Pessoas como Napoleão Bonaparte, Walt Disney, Steve Jobs e Pelé "
        "compartilham este caminho de realização e pioneirismo."),
    2: ("Paz e Cooperação",
        "Sua missão é cooperar, equilibrar e servir como ponte entre as pessoas. Você veio para trazer "
        "harmonia e diplomacia. Sua sensibilidade é sua maior ferramenta. O mundo precisa de sua "
        "capacidade de unir opostos e criar consenso. Princesa Diana, Abraham Lincoln e Roberto Carlos "
        "são exemplos deste percurso de paz."),
    3: ("Alegria e Criação",
        "Sua missão é comunicar, criar e inspirar alegria. Você veio para expressar a beleza da vida "
        "através da arte e da palavra. Seu carisma ilumina quem está ao seu redor. Oscar Wilde, Charles "
        "Dickens, Jim Carrey e Paul McCartney são exemplos deste caminho de criação."),
    4: ("Ação e Estrutura",
        "Sua missão é construir, organizar e criar estrutura. Você veio para estabelecer bases sólidas "
        "com disciplina e transformar o caos em ordem. Sua confiabilidade é seu maior trunfo. Bill Gates, "
        "Sigmund Freud e Margaret Thatcher compartilham esta jornada de construção."),
    5: ("Evolução e Liberdade",
        "Sua missão é experimentar, mudar e evoluir. Você veio para quebrar paradigmas e inspirar "
        "libertação. Sua versatilidade é sua força motriz. Franklin Roosevelt, Cristiano Ronaldo e "
        "Mick Jagger são exemplos de transformação."),
    6: ("Conciliação e Responsabilidade",
        "Sua missão é servir, cuidar e harmonizar. Você veio para criar beleza e amor no mundo. "
        "Seu coração generoso guia seus passos e toca quem está ao seu redor. John F. Kennedy, "
        "Elvis Presley e Joana d'Arc são exemplos deste caminho."),
    7: ("Sabedoria e Perfeição",
        "Sua missão é buscar a verdade e evoluir espiritualmente. Você veio para compreender os "
        "mistérios da existência e transmitir sabedoria. Stephen Hawking, Marie Curie, Nikola Tesla "
        "e Alan Turing compartilham este caminho de conhecimento."),
    8: ("Justiça e Prosperidade",
        "Sua missão é manifestar abundância com sabedoria. Você veio para realizar grandes obras e "
        "mostrar que prosperidade e ética andam juntas. Henry Ford, Getúlio Vargas, Silvio Santos e "
        "Júlio Iglesias são exemplos de realização material com propósito."),
    9: ("Sabedoria e Humanitarismo",
        "Sua missão é servir a humanidade com compaixão. Você veio para concluir ciclos e inspirar. "
        "Sua alma carrega sabedoria de muitas vidas. Gandhi, Martin Luther King Jr., Madre Teresa e "
        "John Lennon são exemplos de serviço à humanidade."),
    11: ("Inspiração Divina",
        "Sua missão é iluminar e elevar a consciência coletiva. Você é um canal de intuição superior. "
        "Winston Churchill, Albert Einstein, Mozart e Marilyn Monroe são exemplos desta inspiração."),
    22: ("Construção em Grande Escala",
        "Sua missão é realizar grandes obras que beneficiam a humanidade. Você é o arquiteto do futuro. "
        "Oprah Winfrey, Thomas Edison, Simon Bolívar e Frank Lloyd Wright são exemplos de construção "
        "em larga escala."),
    33: ("Mestre Amoroso",
        "Sua missão é elevar a consciência através do amor incondicional. Você veio para curar corações.")
   
}

# =====================================================================
# DES - Desafios (interpretação por número)
# =====================================================================
DES = {
    0: "Equilíbrio natural. Você possui equilíbrio nesta área, apenas flua com a vida.",
    1: "Superar o egoísmo e desenvolver liderança servidora. O poder verdadeiro está em empoderar outros.",
    2: "Vencer a timidez e a dependência emocional. Desenvolver autoconfiança para expressar suas necessidades.",
    3: "Evitar a dispersão e cultivar foco. Concentrar a energia criativa em projetos concretos.",
    4: "Superar a rigidez e abraçar mudanças. Flexibilidade e adaptação são chaves para o crescimento.",
    5: "Controlar os excessos e cultivar disciplina. Liberdade com responsabilidade leva à maturidade.",
    6: "Evitar a superproteção. Confiar que seus entes queridos podem fazer suas próprias escolhas.",
    7: "Vencer o isolamento e compartilhar seu conhecimento com o mundo. A sabedoria só existe quando compartilhada.",
    8: "Equilibrar ambição com ética e generosidade. O sucesso material que beneficia outros é o verdadeiro.",
    9: "Superar o desapego excessivo. Aprender a concluir ciclos sem culpa e confiar no fluxo da vida."
}

# =====================================================================
# VIB - Vibração do dia de nascimento
# =====================================================================
VIB = {
    1: "Nasceu sob vibração 1. Líder nato, pioneiro, individualista. Energia criadora e iniciadora. "
       "Tem coragem para abrir caminhos onde ninguém andou. Veio para aprender a liderar com humildade e serviço.",
    2: "Nasceu sob vibração 2. Sensível, diplomata, cooperativo. Sua força está na parceria e na harmonia. "
       "Intuição aguçada. Veio para aprender o equilíbrio entre dar e receber.",
    3: "Nasceu sob vibração 3. Comunicativo, criativo, otimista. Alegria contagiosa. A palavra é sua "
       "ferramenta mais poderosa. Veio para alegrar o mundo com sua arte.",
    4: "Nasceu sob vibração 4. Trabalhador, disciplinado, prático. Solidez constrói bases seguras. "
       "Veio para aprender que a verdadeira segurança vem de dentro.",
    5: "Nasceu sob vibração 5. Livre, versátil, aventureiro. Sua energia busca experiências e transformação. "
       "Curiosidade move sua alma. Veio para experimentar a plenitude da vida.",
    6: "Nasceu sob vibração 6. Amoroso, responsável, familiar. Missão de cuidar e harmonizar. "
       "O amor é sua maior força. Veio para aprender que amar é libertar.",
    7: "Nasceu sob vibração 7. Sábio, introspectivo, espiritual. Busca pelo conhecimento profundo. "
       "O silêncio é seu mestre. Veio para compreender os mistérios da existência.",
    8: "Nasceu sob vibração 8. Poderoso, realizador, próspero. Energia atrai abundância. "
       "Nasceu para construir. Veio para aprender que o poder verdadeiro é serviço.",
    9: "Nasceu sob vibração 9. Humanitário, generoso, compassivo. Alma velha e sábia. "
       "Missão de servir ao coletivo. Veio para concluir ciclos e ensinar o desapego.",
        11: "Nasceu sob vibração 11. Mestre intuitivo. Canaliza energias superiores com sabedoria e inspiração. "
       "Presença magnética. Veio para equilibrar luz espiritual com os pés no chão.",
    22: "Nasceu sob vibração 22. Mestre construtor. Capaz de transformar os maiores sonhos em realidade concreta. "
       "Visão prática. Veio para construir para a humanidade."
}

# ============================================================
# INGLÊS — EXPRESS
# ============================================================
EXPRESS_TXT_EN = {
    1: ("Individuality",
        "Original, creative, born leader and independent — the energy of beginnings and creative impulse.",
        "Selfish, arrogant and impulsive — tends to centralize decisions and never delegate.",
        "Develop humility: true leadership inspires, it does not impose."),

    2: ("Association",
        "Diplomatic, sensitive and peacemaking — their presence calms and harmonizes any environment.",
        "Indecisive, needy and dependent on others' opinions — avoids conflict at any cost.",
        "Develop self-confidence: your sensitivity is a gift, not a weakness."),

    3: ("Creation",
        "Creative, communicative and optimistic — gifted with words and artistic expression.",
        "Superficial, scattered and exaggerated — spreads energy without finishing projects.",
        "Develop focus: quality over quantity."),

    4: ("Work",
        "Practical, disciplined and reliable — the foundation of any project or team.",
        "Rigid, stubborn and resistant to innovation — may lose opportunities through fear of the new.",
        "Develop flexibility: life also asks for spontaneity."),

    5: ("Freedom",
        "Versatile, adventurous and magnetic — thirsts for life and experience.",
        "Impulsive, irresponsible and reckless — can hurt loved ones through unpredictability.",
        "Balance freedom with responsibility: true freedom includes respect for others."),

    6: ("Family",
        "Responsible, loving and protective — the emotional pillar of their own.",
        "Overprotective and intrusive — tends to control through love.",
        "Love without controlling: caring for yourself is also caring for others."),

    7: ("Wisdom",
        "Wise, analytical and spiritual — seeks truth where no one else looks.",
        "Cold, sarcastic and isolated — may feel intellectually superior.",
        "Balance reason and emotion: wisdom only has value when shared."),

    8: ("Power",
        "Powerful, accomplished and prosperous — born to lead and build wealth.",
        "Materialistic, authoritarian and workaholic — may sacrifice people in the name of success.",
        "Use power with integrity: true success is measured by the good it does."),

    9: ("Humanity",
        "Humanitarian, generous and compassionate — sees the larger picture of existence.",
        "Melancholic and scattered — tends to flee from concrete reality.",
        "Forgive and let go: detachment is liberating."),

    11: ("Master Inspirer",
         "Intuitive, illuminated and visionary — channels higher energies.",
         "Anxious, nervous and distant — the pressure of high vibration is hard to bear.",
         "Balance the spiritual with the material: ground your insights."),

    22: ("Master Builder",
         "Accomplished and practical visionary — turns dreams into reality at large scale.",
         "Excessively ambitious and overbearing — the weight of great potential can crush.",
         "Build without enslaving yourself to work: great works need a master at peace."),
}

# ============================================================
# INGLÊS — COMPLETO (SIG com metadados)
# ============================================================
SIG_EN = {
    1: ("Individuality",
        "Symbol: Circle. Day: Sunday. Planet: Sun. Element: Fire. Colour: Yellow. Organs: Heart. "
        "Original, creative, born leader, independent, strong, determined, pioneer. The energy of beginning, "
        "of creative impulse. People with this number are visionaries unafraid to walk new paths. "
        "They show initiative and do not depend on others to act. When channelled positively, "
        "this energy builds empires and revolutionizes paradigms. Their presence is striking and their determination unshakeable.",
        "Selfish, arrogant, domineering, impulsive, stubborn, impatient. Tends to centralize decisions and "
        "never delegate. May become authoritarian and inflexible, driving away those who could collaborate "
        "on their projects. Excess individuality can isolate them and damage their relationships.",
        "Develop humility and learn to work in a team. Remember that no one achieves great deeds alone. "
        "True leadership inspires, it does not impose. Sharing the spotlight expands your power of "
        "achievement and builds lasting legacies."),

    2: ("Association",
        "Symbol: Semicircle. Day: Monday. Planet: Moon. Element: Water. Colour: Green. "
        "Diplomat, sensitive, cooperative, peacemaker, intuitive, detail-oriented, good listener. Their presence "
        "calms and harmonizes environments. They have the gift of uniting people and finding solutions that please everyone. "
        "Their intuition is refined and rarely wrong about people. It is the golden thread that weaves lasting "
        "and meaningful relationships.",
        "Indecisive, needy, submissive, hypersensitive, dependent on others' opinions, shy. Avoids conflict "
        "at any cost, even when standing up is necessary. May erase themselves in relationships to keep "
        "apparent peace, which generates inner frustration.",
        "Develop self-confidence and emotional independence. Say no when necessary. Your sensitivity "
        "is a gift, not a weakness. True peace comes from inner balance, not external approval."),

    3: ("Creation",
        "Symbol: Triangle. Day: Tuesday. Planet: Jupiter. Element: Air. Colour: Violet. "
        "Creative, communicative, optimistic, charismatic, gifted in the arts. Illuminates any environment "
        "with their presence. They have the gift of words and artistic expression. Their energy is contagious and "
        "naturally attracts people. They are the embodiment of joy in living and limitless creativity.",
        "Superficial, scattered, exaggerated, dramatic. Tends to spread energy in many directions without "
        "finishing projects. May use dramatic talent to manipulate situations and people.",
        "Develop focus and depth in expression. Channel so much talent into a specific direction. "
        "Quality over quantity."),

    4: ("Work",
        "Symbol: Square. Day: Wednesday. Planet: Uranus. Element: Earth. Colour: Blue. "
        "Practical, disciplined, reliable, loyal, persistent, organized, efficient, dedicated, honest. "
        "They are the foundation of any project or team. They do not give up until the work is well done. Value "
        "stability and security above all. Their solidity inspires confidence in everyone around them.",
        "Rigid, stubborn, slow to change, excessively materialistic, resistant to innovation. May become "
        "attached to unnecessary routines and lose opportunities through fear of the new.",
        "Develop flexibility and lightness. Not everything needs to be so serious. Life also asks for "
        "spontaneity. Trust more in the flow of life."),

    5: ("Freedom",
        "Symbol: Star. Day: Thursday. Planet: Mercury. Element: Air. Colour: Orange. "
        "Free, versatile, adventurous, progressive, intelligent, curious, adaptable, magnetic. "
        "Their energy is contagious and attracts new people and situations with ease. They thirst for life "
        "and experience. They are the embodiment of freedom and exploration.",
        "Impulsive, irresponsible, anxious, reckless, excessive in pleasures. May hurt those they love "
        "through unpredictability. Excess freedom can become libertinism.",
        "Balance freedom with responsibility. True freedom includes respect for others. "
        "Seek consistency without losing your essence."),

    6: ("Family",
        "Symbol: Hexagon. Day: Friday. Planet: Venus. Element: Earth. Colour: Pink. "
        "Responsible, loving, protective, fair, compassionate, artistic, born counsellor. They are the "
        "emotional pillar of their own. They have a sharp sense of justice and spare no effort to protect those they love.",
        "Overprotective, intrusive, anxious about others. Tends to want to control through love. May feel "
        "responsible for problems that are not theirs.",
        "Love without controlling. Respect others' space. Caring for yourself is also caring for others. "
        "True love is freedom."),

    7: ("Wisdom",
        "Symbol: Heptagon. Day: Saturday. Planet: Neptune. Element: Water. Colour: Indigo. "
        "Wise, analytical, spiritual, intuitive, perfectionist, reserved, philosopher, brilliant mind. "
        "Seeks truth where no one else looks. Has a deep connection with the invisible.",
        "Cold, sarcastic, isolated, distrustful. May feel intellectually superior. "
        "Solitude can turn into bitterness.",
        "Balance reason and emotion. Share knowledge. Wisdom only has value when shared."),

    8: ("Power",
        "Symbol: Octagon. Day: Sunday. Planet: Saturn. Element: Earth. Colour: Red. "
        "Powerful, accomplished, prosperous, strategist, ambitious, visionary. Born to lead "
        "and build wealth. Turns vision into reality with efficiency. Attracts success naturally.",
        "Materialistic, authoritarian, workaholic, impatient. May sacrifice people in the name of success. "
        "Power without ethics corrupts.",
        "Use power with integrity. True success is measured by the good one does. "
        "Money is a means, not an end."),

    9: ("Humanity",
        "Symbol: Nonagon. Day: Tuesday. Planet: Mars. Element: Fire. Colour: Crimson. "
        "Humanitarian, generous, compassionate, wise, tolerant, inspiring, altruistic. Sees the larger "
        "picture of existence. Their soul is old and carries the wisdom of many lives.",
        "Melancholic, scattered, victim-minded. Tends to flee from concrete reality. Takes refuge in "
        "unreachable ideals.",
        "Forgive and let go. Trust the flow of life. Detachment is liberating. Care for yourself in order to "
        "care for the world."),

    11: ("Master Inspirer",
         "Intuitive, illuminated, inspiring, visionary. Channels higher energies. Access to "
         "knowledge beyond the rational. Magnetic and inspiring presence. Elevates everyone around "
         "them with their inner light.",
         "Anxious, nervous, distant, fanatical. The pressure of high vibration is hard to bear. "
         "May feel misunderstood and out of place.",
         "Balance the spiritual world with the material. Ground your insights. Care for the body as much "
         "as for the spirit."),

    22: ("Master Builder",
         "Accomplished, practical visionary. Able to turn dreams into reality at large scale. "
         "Combines spiritual vision with concrete action. Limitless potential. They are the architect of the future, "
         "building works that benefit humanity.",
         "Excessively ambitious, stressed, overbearing. The weight of great potential can crush and "
         "lead to burnout.",
         "Build without enslaving yourself to work. Balance between doing and being. Great works "
         "need a master at peace."),
}

# ============================================================
# INGLÊS — CAMINHO DE VIDA (CAM)
# ============================================================
CAM_EN = {
    1: ("Accomplishment",
        "Your mission is to open paths, lead and innovate. You came into the world to be a pioneer, to "
        "create opportunities where none existed before. You have the courage, willpower and determination to "
        "achieve great deeds. Your greatest challenge is learning that leading also means serving and "
        "inspiring others to shine. People such as Napoleon Bonaparte, Walt Disney, Steve Jobs and Pelé "
        "share this path of accomplishment and pioneering."),
    2: ("Peace and Cooperation",
        "Your mission is to cooperate, balance and serve as a bridge between people. You came to bring "
        "harmony and diplomacy. Your sensitivity is your greatest tool. The world needs your "
        "ability to unite opposites and create consensus. Princess Diana, Abraham Lincoln and Roberto Carlos "
        "are examples of this path of peace."),
    3: ("Joy and Creation",
        "Your mission is to communicate, create and inspire joy. You came to express the beauty of life "
        "through art and the word. Your charisma illuminates those around you. Oscar Wilde, Charles "
        "Dickens, Jim Carrey and Paul McCartney are examples of this path of creation."),
    4: ("Action and Structure",
        "Your mission is to build, organize and create structure. You came to establish solid foundations "
        "with discipline and turn chaos into order. Your reliability is your greatest asset. Bill Gates, "
        "Sigmund Freud and Margaret Thatcher share this journey of construction."),
    5: ("Evolution and Freedom",
        "Your mission is to experience, change and evolve. You came to break paradigms and inspire "
        "liberation. Your versatility is your driving force. Franklin Roosevelt, Cristiano Ronaldo and "
        "Mick Jagger are examples of transformation."),
    6: ("Reconciliation and Responsibility",
        "Your mission is to serve, care and harmonize. You came to create beauty and love in the world. "
        "Your generous heart guides your steps and touches those around you. John F. Kennedy, "
        "Elvis Presley and Joan of Arc are examples of this path."),
    7: ("Wisdom and Perfection",
        "Your mission is to seek truth and evolve spiritually. You came to understand the "
        "mysteries of existence and transmit wisdom. Stephen Hawking, Marie Curie, Nikola Tesla "
        "and Alan Turing share this path of knowledge."),
    8: ("Justice and Prosperity",
        "Your mission is to manifest abundance with wisdom. You came to accomplish great works and "
        "show that prosperity and ethics go together. Henry Ford, Getúlio Vargas, Silvio Santos and "
        "Julio Iglesias are examples of material achievement with purpose."),
    9: ("Wisdom and Humanitarianism",
        "Your mission is to serve humanity with compassion. You came to close cycles and inspire. "
        "Your soul carries the wisdom of many lives. Gandhi, Martin Luther King Jr., Mother Teresa and "
        "John Lennon are examples of service to humanity."),
    11: ("Divine Inspiration",
         "Your mission is to illuminate and elevate collective consciousness. You are a channel of higher intuition. "
         "Winston Churchill, Albert Einstein, Mozart and Marilyn Monroe are examples of this inspiration."),
    22: ("Construction at Great Scale",
         "Your mission is to accomplish great works that benefit humanity. You are the architect of the future. "
         "Oprah Winfrey, Thomas Edison, Simón Bolívar and Frank Lloyd Wright are examples of construction "
         "at large scale."),
    33: ("Loving Master",
         "Your mission is to elevate consciousness through unconditional love. You came to heal hearts."),
}

# ============================================================
# INGLÊS — DESAFIOS (DES)
# ============================================================
DES_EN = {
    0: "Natural balance. You have balance in this area — simply flow with life.",
    1: "Overcome selfishness and develop servant leadership. True power lies in empowering others.",
    2: "Overcome shyness and emotional dependency. Build self-confidence to express your needs.",
    3: "Avoid dispersion and cultivate focus. Concentrate creative energy on concrete projects.",
    4: "Overcome rigidity and embrace change. Flexibility and adaptation are keys to growth.",
    5: "Control excesses and cultivate discipline. Freedom with responsibility leads to maturity.",
    6: "Avoid overprotection. Trust that your loved ones can make their own choices.",
    7: "Overcome isolation and share your knowledge with the world. Wisdom exists only when shared.",
    8: "Balance ambition with ethics and generosity. Material success that benefits others is the true one.",
    9: "Overcome excessive detachment. Learn to close cycles without guilt and trust the flow of life.",
}

# ============================================================
# INGLÊS — VIBRAÇÃO DE NASCIMENTO (VIB)
# ============================================================
VIB_EN = {
    1: "Born under vibration 1. Born leader, pioneer, individualist. Creative and initiating energy. "
       "Has the courage to open paths where no one has walked. Came to learn to lead with humility and service.",
    2: "Born under vibration 2. Sensitive, diplomat, cooperative. Their strength lies in partnership and harmony. "
       "Sharp intuition. Came to learn the balance between giving and receiving.",
    3: "Born under vibration 3. Communicative, creative, optimistic. Contagious joy. The word is their "
       "most powerful tool. Came to gladden the world with their art.",
    4: "Born under vibration 4. Hardworking, disciplined, practical. Solidity builds safe foundations. "
       "Came to learn that true security comes from within.",
    5: "Born under vibration 5. Free, versatile, adventurous. Their energy seeks experience and transformation. "
       "Curiosity moves their soul. Came to experience the fullness of life.",
    6: "Born under vibration 6. Loving, responsible, family-oriented. Mission to care and harmonize. "
       "Love is their greatest strength. Came to learn that loving is setting free.",
    7: "Born under vibration 7. Wise, introspective, spiritual. Search for deep knowledge. "
       "Silence is their master. Came to understand the mysteries of existence.",
    8: "Born under vibration 8. Powerful, accomplished, prosperous. Energy attracts abundance. "
       "Born to build. Came to learn that true power is service.",
    9: "Born under vibration 9. Humanitarian, generous, compassionate. Old and wise soul. "
       "Mission to serve the collective. Came to close cycles and teach detachment.",
    11: "Born under vibration 11. Intuitive master. Channels higher energies with wisdom and inspiration. "
        "Magnetic presence. Came to balance spiritual light with feet on the ground.",
    22: "Born under vibration 22. Master builder. Able to turn the greatest dreams into concrete reality. "
        "Practical vision. Came to build for humanity.",
}

# ============================================================
# ESPANHOL — EXPRESS
# ============================================================
EXPRESS_TXT_ES = {
    1: ("Individualidad",
        "Original, creativo, líder nato e independiente — energía del comienzo y del impulso creador.",
        "Egoísta, arrogante e impulsivo — tiende a centralizar decisiones y no delegar.",
        "Desarrollar la humildad: el liderazgo verdadero inspira, no impone."),
    2: ("Asociación",
        "Diplomático, sensible y pacificador — su presencia calma y armoniza los ambientes.",
        "Indeciso, dependiente y pendiente de la opinión ajena — evita el conflicto a cualquier precio.",
        "Desarrollar la autoconfianza: su sensibilidad es un don, no una debilidad."),
    3: ("Creación",
        "Creativo, comunicativo y optimista — tiene el don de la palabra y de la expresión artística.",
        "Superficial, disperso y exagerado — reparte su energía sin concluir los proyectos.",
        "Desarrollar el enfoque: calidad sobre cantidad."),
    4: ("Trabajo",
        "Práctico, disciplinado y fiable — es el cimiento de cualquier proyecto o equipo.",
        "Rígido, obstinado y resistente a las innovaciones — puede perder oportunidades por miedo a lo nuevo.",
        "Desarrollar la flexibilidad: la vida también pide espontaneidad."),
    5: ("Libertad",
        "Versátil, aventurero y magnético — tiene sed de vida y de experiencias.",
        "Impulsivo, irresponsable e inconsecuente — puede herir a quien ama con su imprevisibilidad.",
        "Equilibrar libertad y responsabilidad: la verdadera libertad incluye el respeto al otro."),
    6: ("Familia",
        "Responsable, amoroso y protector — es el pilar emocional de los suyos.",
        "Sobreprotector e invasivo — tiende a querer controlar por amor.",
        "Amar sin controlar: cuidar de sí también es cuidar de los demás."),
    7: ("Sabiduría",
        "Sabio, analítico y espiritual — busca la verdad donde nadie más mira.",
        "Frío, sarcástico y aislado — puede sentirse intelectualmente superior.",
        "Equilibrar razón y emoción: la sabiduría solo tiene valor cuando se comparte."),
    8: ("Poder",
        "Poderoso, realizador y próspero — nació para liderar y construir riqueza.",
        "Materialista, autoritario y adicto al trabajo — puede sacrificar personas en nombre del éxito.",
        "Usar el poder con integridad: el verdadero éxito se mide por el bien que se hace."),
    9: ("Humanidad",
        "Humanitario, generoso y compasivo — percibe el cuadro mayor de la existencia.",
        "Melancólico y disperso — tiende a huir de la realidad concreta.",
        "Perdonar y dejar ir: el desapego es liberador."),
    11: ("Maestro Inspirador",
         "Intuitivo, iluminado y visionario — canaliza energías superiores.",
         "Ansioso, nervioso y distante — la presión de la alta vibración es difícil de soportar.",
         "Equilibrar el mundo espiritual con el material: aterrizar las intuiciones."),
    22: ("Maestro Constructor",
         "Realizador y visionario práctico — transforma sueños en realidad a gran escala.",
         "Ambicioso en exceso y prepotente — el peso del gran potencial puede aplastar.",
         "Construir sin esclavizarse al trabajo: las grandes obras necesitan un maestro en paz."),
}

# ============================================================
# ESPANHOL — COMPLETO (SIG con metadatos)
# ============================================================
SIG_ES = {
    1: ("Individualidad",
        "Símbolo: Círculo. Día: Domingo. Planeta: Sol. Elemento: Fuego. Color: Amarillo. Órganos: Corazón. "
        "Original, creativo, líder nato, independiente, fuerte, determinado, pionero. Energía del comienzo, "
        "del impulso creador. Las personas con este número son visionarias que no temen recorrer caminos "
        "nuevos. Tienen iniciativa propia y no dependen de otros para actuar. Cuando se canaliza positivamente, "
        "esta energía construye imperios y revoluciona paradigmas. Su presencia es notable y su determinación inquebrantable.",
        "Egoísta, arrogante, dominante, impulsivo, obstinado, impaciente. Tiende a centralizar decisiones y "
        "no delegar. Puede volverse autoritario e inflexible, alejando a quienes podrían colaborar "
        "en sus proyectos. El exceso de individualidad puede aislarlo y perjudicar sus relaciones.",
        "Desarrollar la humildad y saber trabajar en equipo. Recordar que nadie realiza grandes hazañas "
        "solo. El liderazgo verdadero inspira, no impone. Compartir el protagonismo amplía su poder "
        "de realización y construye legados duraderos."),
    2: ("Asociación",
        "Símbolo: Semicírculo. Día: Lunes. Planeta: Luna. Elemento: Agua. Color: Verde. "
        "Diplomático, sensible, cooperativo, pacificador, intuitivo, detallista, buen oyente. Su presencia "
        "calma y armoniza los ambientes. Tiene el don de unir personas y encontrar soluciones que agradan a todos. "
        "Su intuición es refinada y rara vez se equivoca con las personas. Es el hilo de oro que teje relaciones "
        "duraderas y significativas.",
        "Indeciso, dependiente, sumiso, hipersensible, pendiente de la opinión ajena, tímido. Evita los conflictos "
        "a cualquier precio, incluso cuando es necesario posicionarse. Puede anularse en las relaciones para mantener "
        "una paz aparente, lo que genera frustración interna.",
        "Desarrollar la autoconfianza y la independencia emocional. Decir no cuando sea necesario. Su sensibilidad "
        "es un don, no una debilidad. La verdadera paz viene del equilibrio interno, no de la aprobación externa."),
    3: ("Creación",
        "Símbolo: Triángulo. Día: Martes. Planeta: Júpiter. Elemento: Aire. Color: Violeta. "
        "Creativo, comunicativo, optimista, carismático, talentoso para las artes. Ilumina cualquier ambiente "
        "con su presencia. Tiene el don de la palabra y de la expresión artística. Su energía es contagiosa y "
        "atrae personas con naturalidad. Es la personificación de la alegría de vivir y de la creatividad sin límites.",
        "Superficial, disperso, exagerado, dramático. Tiende a repartir energía en muchas direcciones sin "
        "concluir proyectos. Puede usar el talento dramático para manipular situaciones y personas.",
        "Desarrollar el enfoque y la profundidad en la expresión. Canalizar tanto talento hacia una dirección concreta. "
        "Calidad sobre cantidad."),
    4: ("Trabajo",
        "Símbolo: Cuadrado. Día: Miércoles. Planeta: Urano. Elemento: Tierra. Color: Azul. "
        "Práctico, disciplinado, fiable, leal, persistente, organizado, eficiente, dedicado, honesto. "
        "Es el cimiento de cualquier proyecto o equipo. No desiste hasta ver el trabajo bien hecho. Valora "
        "la estabilidad y la seguridad por encima de todo. Su solidez inspira confianza en todos los que lo rodean.",
        "Rígido, obstinado, lento para cambiar, materialista en exceso, resistente a las innovaciones. Puede "
        "aferrarse a rutinas innecesarias y perder oportunidades por miedo a lo nuevo.",
        "Desarrollar la flexibilidad y la ligereza. No todo tiene que ser tan serio. La vida también pide "
        "espontaneidad. Confiar más en el fluir de la vida."),
    5: ("Libertad",
        "Símbolo: Estrella. Día: Jueves. Planeta: Mercurio. Elemento: Aire. Color: Naranja. "
        "Libre, versátil, aventurero, progresista, inteligente, curioso, adaptable, magnético. "
        "Su energía es contagiosa y atrae personas y situaciones nuevas con facilidad. Tiene sed de vida "
        "y de experiencias. Es la personificación de la libertad y de la exploración.",
        "Impulsivo, irresponsable, ansioso, inconsecuente, excesivo en los placeres. Puede herir a quien ama "
        "con su imprevisibilidad. El exceso de libertad puede convertirse en libertinaje.",
        "Equilibrar libertad y responsabilidad. La verdadera libertad incluye el respeto al otro. "
        "Buscar consistencia sin perder la esencia."),
    6: ("Familia",
        "Símbolo: Hexágono. Día: Viernes. Planeta: Venus. Elemento: Tierra. Color: Rosa. "
        "Responsable, amoroso, protector, justo, compasivo, artístico, consejero nato. Es el pilar "
        "emocional de los suyos. Tiene un agudo sentido de la justicia y no escatima esfuerzos para proteger a quien ama.",
        "Sobreprotector, invasivo, ansioso por los demás. Tiende a querer controlar por amor. Puede "
        "sentirse responsable de problemas que no son suyos.",
        "Amar sin controlar. Respetar el espacio ajeno. Cuidar de sí también es cuidar de los demás. "
        "El amor verdadero es libertad."),
    7: ("Sabiduría",
        "Símbolo: Heptágono. Día: Sábado. Planeta: Neptuno. Elemento: Agua. Color: Índigo. "
        "Sabio, analítico, espiritual, intuitivo, perfeccionista, reservado, filósofo, mente brillante. "
        "Busca la verdad donde nadie más mira. Tiene una conexión profunda con lo invisible.",
        "Frío, sarcástico, aislado, desconfiado. Puede sentirse intelectualmente superior. "
        "La soledad puede transformarse en amargura.",
        "Equilibrar razón y emoción. Compartir el conocimiento. La sabiduría solo tiene valor cuando se comparte."),
    8: ("Poder",
        "Símbolo: Octógono. Día: Domingo. Planeta: Saturno. Elemento: Tierra. Color: Rojo. "
        "Poderoso, realizador, próspero, estratega, ambicioso, visionario. Nació para liderar "
        "y construir riqueza. Transforma la visión en realidad con eficiencia. Atrae el éxito con naturalidad.",
        "Materialista, autoritario, adicto al trabajo, impaciente. Puede sacrificar personas en nombre del éxito. "
        "El poder sin ética corrompe.",
        "Usar el poder con integridad. El verdadero éxito se mide por el bien que se hace. "
        "El dinero es un medio, no un fin."),
    9: ("Humanidad",
        "Símbolo: Nonágono. Día: Martes. Planeta: Marte. Elemento: Fuego. Color: Carmesí. "
        "Humanitario, generoso, compasivo, sabio, tolerante, inspirador, altruista. Percibe el cuadro "
        "mayor de la existencia. Su alma es vieja y lleva la sabiduría de muchas vidas.",
        "Melancólico, disperso, victimista. Tiende a huir de la realidad concreta. Se refugia en ideales "
        "inalcanzables.",
        "Perdonar y dejar ir. Confiar en el fluir de la vida. El desapego es liberador. Cuidar de sí para "
        "cuidar del mundo."),
    11: ("Maestro Inspirador",
         "Intuitivo, iluminado, inspirador, visionario. Canaliza energías superiores. Acceso al "
         "conocimiento más allá de lo racional. Presencia magnética e inspiradora. Eleva a todos los que lo rodean "
         "con su luz interior.",
         "Ansioso, nervioso, distante, fanático. La presión de la alta vibración es difícil de soportar. "
         "Puede sentirse incomprendido y fuera de lugar.",
         "Equilibrar el mundo espiritual con el material. Aterrizar las intuiciones. Cuidar del cuerpo tanto "
         "como del espíritu."),
    22: ("Maestro Constructor",
         "Realizador, visionario práctico. Capaz de transformar sueños en realidad a gran escala. "
         "Combina visión espiritual con acción concreta. Potencial ilimitado. Es el arquitecto del futuro, "
         "construyendo obras que benefician a la humanidad.",
         "Ambicioso en exceso, estresado, prepotente. El peso del gran potencial puede aplastar y "
         "llevar al agotamiento.",
         "Construir sin esclavizarse al trabajo. El equilibrio entre hacer y ser. Las grandes obras "
         "necesitan un maestro en paz."),
}

# ============================================================
# ESPANHOL — CAMINHO DE VIDA (CAM)
# ============================================================
CAM_ES = {
    1: ("Realización",
        "Su misión es abrir caminos, liderar e innovar. Usted vino al mundo para ser pionero, para "
        "crear oportunidades donde antes no existían. Tiene coraje, fuerza de voluntad y determinación para "
        "alcanzar grandes hazañas. Su mayor desafío es aprender que liderar también significa servir e "
        "inspirar a otros a brillar. Personas como Napoleón Bonaparte, Walt Disney, Steve Jobs y Pelé "
        "comparten este camino de realización y pionerismo."),
    2: ("Paz y Cooperación",
        "Su misión es cooperar, equilibrar y servir como puente entre las personas. Usted vino para traer "
        "armonía y diplomacia. Su sensibilidad es su mayor herramienta. El mundo necesita su "
        "capacidad de unir opuestos y crear consenso. Lady Di, Abraham Lincoln y Roberto Carlos "
        "son ejemplos de este recorrido de paz."),
    3: ("Alegría y Creación",
        "Su misión es comunicar, crear e inspirar alegría. Usted vino para expresar la belleza de la vida "
        "a través del arte y de la palabra. Su carisma ilumina a quienes lo rodean. Oscar Wilde, Charles "
        "Dickens, Jim Carrey y Paul McCartney son ejemplos de este camino de creación."),
    4: ("Acción y Estructura",
        "Su misión es construir, organizar y crear estructura. Usted vino para establecer bases sólidas "
        "con disciplina y transformar el caos en orden. Su fiabilidad es su mayor baza. Bill Gates, "
        "Sigmund Freud y Margaret Thatcher comparten esta jornada de construcción."),
    5: ("Evolución y Libertad",
        "Su misión es experimentar, cambiar y evolucionar. Usted vino para romper paradigmas e inspirar "
        "la liberación. Su versatilidad es su fuerza motriz. Franklin Roosevelt, Cristiano Ronaldo y "
        "Mick Jagger son ejemplos de transformación."),
    6: ("Conciliación y Responsabilidad",
        "Su misión es servir, cuidar y armonizar. Usted vino para crear belleza y amor en el mundo. "
        "Su corazón generoso guía sus pasos y toca a quienes lo rodean. John F. Kennedy, "
        "Elvis Presley y Juana de Arco son ejemplos de este camino."),
    7: ("Sabiduría y Perfección",
        "Su misión es buscar la verdad y evolucionar espiritualmente. Usted vino para comprender los "
        "misterios de la existencia y transmitir sabiduría. Stephen Hawking, Marie Curie, Nikola Tesla "
        "y Alan Turing comparten este camino de conocimiento."),
    8: ("Justicia y Prosperidad",
        "Su misión es manifestar abundancia con sabiduría. Usted vino para realizar grandes obras y "
        "mostrar que prosperidad y ética van juntas. Henry Ford, Getúlio Vargas, Silvio Santos y "
        "Julio Iglesias son ejemplos de realización material con propósito."),
    9: ("Sabiduría y Humanitarismo",
        "Su misión es servir a la humanidad con compasión. Usted vino para cerrar ciclos e inspirar. "
        "Su alma lleva la sabiduría de muchas vidas. Gandhi, Martin Luther King Jr., Madre Teresa y "
        "John Lennon son ejemplos de servicio a la humanidad."),
    11: ("Inspiración Divina",
         "Su misión es iluminar y elevar la conciencia colectiva. Usted es un canal de intuición superior. "
         "Winston Churchill, Albert Einstein, Mozart y Marilyn Monroe son ejemplos de esta inspiración."),
    22: ("Construcción a Gran Escala",
         "Su misión es realizar grandes obras que benefician a la humanidad. Usted es el arquitecto del futuro. "
         "Oprah Winfrey, Thomas Edison, Simón Bolívar y Frank Lloyd Wright son ejemplos de construcción "
         "a gran escala."),
    33: ("Maestro Amoroso",
         "Tu misión es elevar la conciencia a través del amor incondicional. Viniste a sanar corazones."),
}

# ============================================================
# ESPANHOL — DESAFÍOS (DES)
# ============================================================
DES_ES = {
    0: "Equilibrio natural. Usted posee equilibrio en esta área, simplemente fluya con la vida.",
    1: "Superar el egoísmo y desarrollar un liderazgo servidor. El poder verdadero está en empoderar a otros.",
    2: "Vencer la timidez y la dependencia emocional. Desarrollar autoconfianza para expresar sus necesidades.",
    3: "Evitar la dispersión y cultivar el enfoque. Concentrar la energía creativa en proyectos concretos.",
    4: "Superar la rigidez y abrazar los cambios. La flexibilidad y la adaptación son claves para el crecimiento.",
    5: "Controlar los excesos y cultivar la disciplina. La libertad con responsabilidad lleva a la madurez.",
    6: "Evitar la sobreprotección. Confiar en que sus seres queridos pueden tomar sus propias decisiones.",
    7: "Vencer el aislamiento y compartir su conocimiento con el mundo. La sabiduría solo existe cuando se comparte.",
    8: "Equilibrar la ambición con la ética y la generosidad. El éxito material que beneficia a otros es el verdadero.",
    9: "Superar el desapego excesivo. Aprender a cerrar ciclos sin culpa y confiar en el fluir de la vida.",
}

# ============================================================
# ESPANHOL — VIBRACIÓN DE NACIMIENTO (VIB)
# ============================================================
VIB_ES = {
    1: "Nació bajo la vibración 1. Líder nato, pionero, individualista. Energía creadora e iniciadora. "
       "Tiene el coraje de abrir caminos donde nadie ha transitado. Vino para aprender a liderar con humildad y servicio.",
    2: "Nació bajo la vibración 2. Sensible, diplomático, cooperativo. Su fuerza está en la cooperación y la armonía. "
       "Intuición aguda. Vino para aprender el equilibrio entre dar y recibir.",
    3: "Nació bajo la vibración 3. Comunicativo, creativo, optimista. Alegría contagiosa. La palabra es su "
       "herramienta más poderosa. Vino para alegrar el mundo con su arte.",
    4: "Nació bajo la vibración 4. Trabajador, disciplinado, práctico. La solidez construye bases seguras. "
       "Vino para aprender que la verdadera seguridad viene de dentro.",
    5: "Nació bajo la vibración 5. Libre, versátil, aventurero. Su energía busca experiencias y transformación. "
       "La curiosidad mueve su alma. Vino para experimentar la plenitud de la vida.",
    6: "Nació bajo la vibración 6. Amoroso, responsable, familiar. Misión de cuidar y armonizar. "
       "El amor es su mayor fuerza. Vino para aprender que amar es liberar.",
    7: "Nació bajo la vibración 7. Sabio, introspectivo, espiritual. Búsqueda del conocimiento profundo. "
       "El silencio es su maestro. Vino para comprender los misterios de la existencia.",
    8: "Nació bajo la vibración 8. Poderoso, realizador, próspero. Su energía atrae la abundancia. "
       "Nació para construir. Vino para aprender que el poder verdadero es servicio.",
    9: "Nació bajo la vibración 9. Humanitario, generoso, compasivo. Alma vieja y sabia. "
       "Misión de servir al colectivo. Vino para cerrar ciclos y enseñar el desapego.",
    11: "Nació bajo la vibración 11. Maestro intuitivo. Canaliza energías superiores con sabiduría e inspiración. "
        "Presencia magnética. Vino para equilibrar la luz espiritual con los pies en la tierra.",
    22: "Nació bajo la vibración 22. Maestro constructor. Capaz de transformar los mayores sueños en realidad concreta. "
        "Visión práctica. Vino para construir para la humanidad.",
}

# ============================================================
# FRANCÊS — EXPRESS
# ============================================================
EXPRESS_TXT_FR = {
    1: ("Individualité",
        "Original, créatif, leader-né et indépendant — énergie du commencement et de l'impulsion créatrice.",
        "Égoïste, arrogant et impulsif — tend à centraliser les décisions et à ne jamais déléguer.",
        "Développer l'humilité : le vrai leadership inspire, il n'impose pas."),
    2: ("Association",
        "Diplomate, sensible et pacificateur — sa présence apaise et harmonise les environnements.",
        "Indécis, dépendant et influençable — évite le conflit à tout prix.",
        "Développer la confiance en soi : votre sensibilité est un don, pas une faiblesse."),
    3: ("Création",
        "Créatif, communicatif et optimiste — doté du don de la parole et de l'expression artistique.",
        "Superficiel, dispersé et exagéré — disperse son énergie sans achever ses projets.",
        "Développer la concentration : la qualité prime sur la quantité."),
    4: ("Travail",
        "Pratique, discipliné et fiable — il est le fondement de tout projet ou de toute équipe.",
        "Rigide, têtu et résistant aux innovations — peut perdre des occasions par peur du nouveau.",
        "Développer la souplesse : la vie demande aussi de la spontanéité."),
    5: ("Liberté",
        "Polyvalent, aventureux et magnétique — il a soif de vie et d'expériences.",
        "Impulsif, irresponsable et inconséquent — peut blesser ceux qu'il aime par son imprévisibilité.",
        "Équilibrer liberté et responsabilité : la vraie liberté inclut le respect de l'autre."),
    6: ("Famille",
        "Responsable, aimant et protecteur — il est le pilier émotionnel des siens.",
        "Surprotecteur et envahissant — tend à vouloir contrôler par amour.",
        "Aimer sans contrôler : prendre soin de soi, c'est aussi prendre soin des autres."),
    7: ("Sagesse",
        "Sage, analytique et spirituel — cherche la vérité là où personne ne regarde.",
        "Froid, sarcastique et isolé — peut se sentir intellectuellement supérieur.",
        "Équilibrer raison et émotion : la sagesse n'a de valeur que lorsqu'elle est partagée."),
    8: ("Pouvoir",
        "Puissant, réalisateur et prospère — né pour diriger et bâtir la richesse.",
        "Matérialiste, autoritaire et bourreau de travail — peut sacrifier des personnes au nom du succès.",
        "User du pouvoir avec intégrité : le vrai succès se mesure au bien que l'on fait."),
    9: ("Humanité",
        "Humanitaire, généreux et compatissant — perçoit le tableau d'ensemble de l'existence.",
        "Mélancolique et dispersé — tend à fuir la réalité concrète.",
        "Pardonner et lâcher prise : le détachement libère."),
    11: ("Maître Inspirateur",
         "Intuitif, illuminé et visionnaire — canalise des énergies supérieures.",
         "Anxieux, nerveux et distant — la pression de la haute vibration est difficile à supporter.",
         "Équilibrer le monde spirituel et le monde matériel : ancrer les intuitions."),
    22: ("Maître Bâtisseur",
         "Réalisateur et visionnaire pratique — transforme les rêves en réalité à grande échelle.",
         "Excessivement ambitieux et arrogant — le poids du grand potentiel peut écraser.",
         "Bâtir sans s'asservir au travail : les grandes œuvres ont besoin d'un maître en paix."),
}

# ============================================================
# FRANCÊS — COMPLETO (SIG avec métadonnées)
# ============================================================
SIG_FR = {
    1: ("Individualité",
        "Symbole : Cercle. Jour : Dimanche. Planète : Soleil. Élément : Feu. Couleur : Jaune. Organes : Cœur. "
        "Original, créatif, leader-né, indépendant, fort, déterminé, pionnier. Énergie du commencement, "
        "de l'impulsion créatrice. Les personnes portant ce nombre sont des visionnaires qui ne craignent pas "
        "d'emprunter des chemins nouveaux. Elles font preuve d'initiative et ne dépendent pas des autres pour agir. "
        "Lorsqu'elle est canalisée positivement, cette énergie bâtit des empires et révolutionne les paradigmes. "
        "Leur présence est marquante et leur détermination inébranlable.",
        "Égoïste, arrogant, dominateur, impulsif, têtu, impatient. Tend à centraliser les décisions et "
        "à ne jamais déléguer. Peut devenir autoritaire et inflexible, éloignant ceux qui pourraient collaborer "
        "à ses projets. L'excès d'individualité peut l'isoler et nuire à ses relations.",
        "Développer l'humilité et apprendre à travailler en équipe. Se rappeler que nul n'accomplit de grandes "
        "choses seul. Le vrai leadership inspire, il n'impose pas. Partager la vedette élargit son pouvoir "
        "de réalisation et bâtit des héritages durables."),
    2: ("Association",
        "Symbole : Demi-cercle. Jour : Lundi. Planète : Lune. Élément : Eau. Couleur : Vert. "
        "Diplomate, sensible, coopératif, pacificateur, intuitif, attentif aux détails, bon auditeur. Sa présence "
        "apaise et harmonise les environnements. Il a le don d'unir les personnes et de trouver des solutions qui plaisent à tous. "
        "Son intuition est fine et se trompe rarement sur les gens. C'est le fil d'or qui tisse des relations "
        "durables et significatives.",
        "Indécis, dépendant, soumis, hypersensible, influençable, timide. Évite le conflit "
        "à tout prix, même lorsqu'il faut se positionner. Peut s'effacer dans les relations pour maintenir "
        "une paix apparente, ce qui génère une frustration intérieure.",
        "Développer la confiance en soi et l'indépendance émotionnelle. Savoir dire non quand c'est nécessaire. "
        "Votre sensibilité est un don, pas une faiblesse. La vraie paix vient de l'équilibre intérieur, "
        "non de l'approbation extérieure."),
    3: ("Création",
        "Symbole : Triangle. Jour : Mardi. Planète : Jupiter. Élément : Air. Couleur : Violet. "
        "Créatif, communicatif, optimiste, charismatique, doué pour les arts. Il illumine tout environnement "
        "par sa présence. Il a le don de la parole et de l'expression artistique. Son énergie est contagieuse et "
        "attire naturellement les gens. Il incarne la joie de vivre et la créativité sans limites.",
        "Superficiel, dispersé, exagéré, dramatique. Tend à disperser son énergie dans plusieurs directions sans "
        "achever ses projets. Peut utiliser son talent dramatique pour manipuler les situations et les personnes.",
        "Développer la concentration et la profondeur dans l'expression. Canaliser tant de talent dans une direction précise. "
        "La qualité prime sur la quantité."),
    4: ("Travail",
        "Symbole : Carré. Jour : Mercredi. Planète : Uranus. Élément : Terre. Couleur : Bleu. "
        "Pratique, discipliné, fiable, loyal, persévérant, organisé, efficace, dévoué, honnête. "
        "Il est le fondement de tout projet ou de toute équipe. Il n'abandonne pas avant que le travail soit bien fait. "
        "Il valorise la stabilité et la sécurité par-dessus tout. Sa solidité inspire confiance à tous ceux qui l'entourent.",
        "Rigide, têtu, lent à changer, excessivement matérialiste, résistant aux innovations. Peut "
        "s'attacher à des routines inutiles et perdre des occasions par peur du nouveau.",
        "Développer la souplesse et la légèreté. Tout ne doit pas être si sérieux. La vie demande aussi "
        "de la spontanéité. Faire davantage confiance au flux de la vie."),
    5: ("Liberté",
        "Symbole : Étoile. Jour : Jeudi. Planète : Mercure. Élément : Air. Couleur : Orange. "
        "Libre, polyvalent, aventureux, progressiste, intelligent, curieux, adaptable, magnétique. "
        "Son énergie est contagieuse et attire facilement des personnes et des situations nouvelles. Il a soif de vie "
        "et d'expériences. Il incarne la liberté et l'exploration.",
        "Impulsif, irresponsable, anxieux, inconséquent, excessif dans les plaisirs. Peut blesser ceux qu'il aime "
        "par son imprévisibilité. L'excès de liberté peut devenir libertinage.",
        "Équilibrer liberté et responsabilité. La vraie liberté inclut le respect de l'autre. "
        "Chercher la constance sans perdre son essence."),
    6: ("Famille",
        "Symbole : Hexagone. Jour : Vendredi. Planète : Vénus. Élément : Terre. Couleur : Rose. "
        "Responsable, aimant, protecteur, juste, compatissant, artistique, conseiller-né. Il est le pilier "
        "émotionnel des siens. Il a un sens aigu de la justice et ne ménage pas ses efforts pour protéger ceux qu'il aime.",
        "Surprotecteur, envahissant, anxieux pour les autres. Tend à vouloir contrôler par amour. Peut se "
        "sentir responsable de problèmes qui ne sont pas les siens.",
        "Aimer sans contrôler. Respecter l'espace d'autrui. Prendre soin de soi, c'est aussi prendre soin des autres. "
        "Le véritable amour est liberté."),
    7: ("Sagesse",
        "Symbole : Heptagone. Jour : Samedi. Planète : Neptune. Élément : Eau. Couleur : Indigo. "
        "Sage, analytique, spirituel, intuitif, perfectionniste, réservé, philosophe, esprit brillant. "
        "Il cherche la vérité là où personne ne regarde. Il a une connexion profonde avec l'invisible.",
        "Froid, sarcastique, isolé, méfiant. Peut se sentir intellectuellement supérieur. "
        "La solitude peut se transformer en amertume.",
        "Équilibrer raison et émotion. Partager son savoir. La sagesse n'a de valeur que lorsqu'elle est partagée."),
    8: ("Pouvoir",
        "Symbole : Octogone. Jour : Dimanche. Planète : Saturne. Élément : Terre. Couleur : Rouge. "
        "Puissant, réalisateur, prospère, stratège, ambitieux, visionnaire. Né pour diriger "
        "et bâtir la richesse. Il transforme la vision en réalité avec efficacité. Il attire le succès naturellement.",
        "Matérialiste, autoritaire, bourreau de travail, impatient. Peut sacrifier des personnes au nom du succès. "
        "Le pouvoir sans éthique corrompt.",
        "User du pouvoir avec intégrité. Le vrai succès se mesure au bien que l'on fait. "
        "L'argent est un moyen, non une fin."),
    9: ("Humanité",
        "Symbole : Ennéagone. Jour : Mardi. Planète : Mars. Élément : Feu. Couleur : Cramoisi. "
        "Humanitaire, généreux, compatissant, sage, tolérant, inspirant, altruiste. Il perçoit le tableau "
        "d'ensemble de l'existence. Son âme est ancienne et porte la sagesse de nombreuses vies.",
        "Mélancolique, dispersé, victimaire. Tend à fuir la réalité concrète. Se réfugie dans des idéaux "
        "inaccessibles.",
        "Pardonner et lâcher prise. Faire confiance au flux de la vie. Le détachement libère. Prendre soin de soi pour "
        "prendre soin du monde."),
    11: ("Maître Inspirateur",
         "Intuitif, illuminé, inspirant, visionnaire. Canalise des énergies supérieures. Accès à "
         "un savoir au-delà du rationnel. Présence magnétique et inspirante. Il élève tous ceux qui l'entourent "
         "par sa lumière intérieure.",
         "Anxieux, nerveux, distant, fanatique. La pression de la haute vibration est difficile à supporter. "
         "Peut se sentir incompris et déplacé.",
         "Équilibrer le monde spirituel et le monde matériel. Ancrer les intuitions. Prendre soin du corps autant "
         "que de l'esprit."),
    22: ("Maître Bâtisseur",
         "Réalisateur, visionnaire pratique. Capable de transformer les rêves en réalité à grande échelle. "
         "Il allie vision spirituelle et action concrète. Potentiel illimité. Il est l'architecte de l'avenir, "
         "bâtissant des œuvres qui bénéficient à l'humanité.",
         "Excessivement ambitieux, stressé, arrogant. Le poids du grand potentiel peut écraser et "
         "mener à l'épuisement.",
         "Bâtir sans s'asservir au travail. L'équilibre entre faire et être. Les grandes œuvres "
         "ont besoin d'un maître en paix."),
}

# ============================================================
# FRANCÊS — CHEMIN DE VIE (CAM)
# ============================================================
CAM_FR = {
    1: ("Réalisation",
        "Votre mission est d'ouvrir des chemins, de diriger et d'innover. Vous êtes venu au monde pour être "
        "pionnier, pour créer des opportunités là où il n'en existait aucune. Vous avez le courage, la volonté et la "
        "détermination pour accomplir de grandes choses. Votre plus grand défi est d'apprendre que diriger signifie aussi "
        "servir et inspirer les autres à briller. Des personnes comme Napoléon Bonaparte, Walt Disney, Steve Jobs et Pelé "
        "partagent ce chemin de réalisation et de pionnier."),
    2: ("Paix et Coopération",
        "Votre mission est de coopérer, d'équilibrer et de servir de pont entre les personnes. Vous êtes venu apporter "
        "l'harmonie et la diplomatie. Votre sensibilité est votre meilleur outil. Le monde a besoin de votre "
        "capacité à unir les opposés et à créer un consensus. Lady Diana, Abraham Lincoln et Roberto Carlos "
        "sont des exemples de ce parcours de paix."),
    3: ("Joie et Création",
        "Votre mission est de communiquer, de créer et d'inspirer la joie. Vous êtes venu exprimer la beauté de la vie "
        "à travers l'art et la parole. Votre charisme illumine ceux qui vous entourent. Oscar Wilde, Charles "
        "Dickens, Jim Carrey et Paul McCartney sont des exemples de ce chemin de création."),
    4: ("Action et Structure",
        "Votre mission est de bâtir, d'organiser et de créer de la structure. Vous êtes venu établir des bases solides "
        "avec discipline et transformer le chaos en ordre. Votre fiabilité est votre meilleur atout. Bill Gates, "
        "Sigmund Freud et Margaret Thatcher partagent ce parcours de construction."),
    5: ("Évolution et Liberté",
        "Votre mission est d'expérimenter, de changer et d'évoluer. Vous êtes venu briser les paradigmes et inspirer "
        "la libération. Votre polyvalence est votre force motrice. Franklin Roosevelt, Cristiano Ronaldo et "
        "Mick Jagger sont des exemples de transformation."),
    6: ("Conciliation et Responsabilité",
        "Votre mission est de servir, de prendre soin et d'harmoniser. Vous êtes venu créer de la beauté et de l'amour dans le monde. "
        "Votre cœur généreux guide vos pas et touche ceux qui vous entourent. John F. Kennedy, "
        "Elvis Presley et Jeanne d'Arc sont des exemples de ce chemin."),
    7: ("Sagesse et Perfection",
        "Votre mission est de chercher la vérité et d'évoluer spirituellement. Vous êtes venu comprendre les "
        "mystères de l'existence et transmettre la sagesse. Stephen Hawking, Marie Curie, Nikola Tesla "
        "et Alan Turing partagent ce chemin de connaissance."),
    8: ("Justice et Prospérité",
        "Votre mission est de manifester l'abondance avec sagesse. Vous êtes venu accomplir de grandes œuvres et "
        "montrer que prospérité et éthique vont de pair. Henry Ford, Getúlio Vargas, Silvio Santos et "
        "Julio Iglesias sont des exemples de réalisation matérielle avec un but."),
    9: ("Sagesse et Humanitarisme",
        "Votre mission est de servir l'humanité avec compassion. Vous êtes venu clore des cycles et inspirer. "
        "Votre âme porte la sagesse de nombreuses vies. Gandhi, Martin Luther King Jr., Mère Teresa et "
        "John Lennon sont des exemples de service à l'humanité."),
    11: ("Inspiration Divine",
         "Votre mission est d'illuminer et d'élever la conscience collective. Vous êtes un canal d'intuition supérieure. "
         "Winston Churchill, Albert Einstein, Mozart et Marilyn Monroe sont des exemples de cette inspiration."),
    22: ("Construction à Grande Échelle",
         "Votre mission est d'accomplir de grandes œuvres qui bénéficient à l'humanité. Vous êtes l'architecte de l'avenir. "
         "Oprah Winfrey, Thomas Edison, Simón Bolívar et Frank Lloyd Wright sont des exemples de construction "
         "à grande échelle."),
    33: ("Maître Amoureux",
         "Ta mission est d'élever la conscience à travers l'amour inconditionnel. Tu es venu pour guérir les cœurs."),
}

# ============================================================
# FRANCÊS — DÉFIS (DES)
# ============================================================
DES_FR = {
    0: "Équilibre naturel. Vous possédez l'équilibre dans ce domaine, il suffit de suivre le cours de la vie.",
    1: "Surmonter l'égoïsme et développer un leadership au service des autres. Le vrai pouvoir est de donner du pouvoir aux autres.",
    2: "Vaincre la timidité et la dépendance affective. Développer la confiance en soi pour exprimer ses besoins.",
    3: "Éviter la dispersion et cultiver la concentration. Canaliser l'énergie créative vers des projets concrets.",
    4: "Surmonter la rigidité et accueillir le changement. La souplesse et l'adaptation sont les clés de la croissance.",
    5: "Maîtriser les excès et cultiver la discipline. La liberté avec responsabilité mène à la maturité.",
    6: "Éviter la surprotection. Faire confiance à vos proches pour faire leurs propres choix.",
    7: "Vaincre l'isolement et partager votre savoir avec le monde. La sagesse n'existe que lorsqu'elle est partagée.",
    8: "Équilibrer l'ambition avec l'éthique et la générosité. Le succès matériel qui profite aux autres est le véritable.",
    9: "Surmonter le détachement excessif. Apprendre à clore des cycles sans culpabilité et faire confiance au flux de la vie.",
}

# ============================================================
# FRANCÊS — VIBRATION DE NAISSANCE (VIB)
# ============================================================
VIB_FR = {
    1: "Né sous la vibration 1. Leader-né, pionnier, individualiste. Énergie créatrice et initiatrice. "
       "Il a le courage d'ouvrir des chemins où personne n'a marché. Venu apprendre à diriger avec humilité et service.",
    2: "Né sous la vibration 2. Sensible, diplomate, coopératif. Sa force réside dans le partenariat et l'harmonie. "
       "Intuition aiguisée. Venu apprendre l'équilibre entre donner et recevoir.",
    3: "Né sous la vibration 3. Communicatif, créatif, optimiste. Joie contagieuse. La parole est son "
       "outil le plus puissant. Venu égayer le monde de son art.",
    4: "Né sous la vibration 4. Travailleur, discipliné, pratique. La solidité bâtit des bases sûres. "
       "Venu apprendre que la vraie sécurité vient de l'intérieur.",
    5: "Né sous la vibration 5. Libre, polyvalent, aventureux. Son énergie cherche l'expérience et la transformation. "
       "La curiosité meut son âme. Venu expérimenter la plénitude de la vie.",
    6: "Né sous la vibration 6. Aimant, responsable, familial. Mission de prendre soin et d'harmoniser. "
       "L'amour est sa plus grande force. Venu apprendre qu'aimer, c'est libérer.",
    7: "Né sous la vibration 7. Sage, introspectif, spirituel. Recherche de la connaissance profonde. "
       "Le silence est son maître. Venu comprendre les mystères de l'existence.",
    8: "Né sous la vibration 8. Puissant, réalisateur, prospère. Son énergie attire l'abondance. "
       "Né pour bâtir. Venu apprendre que le vrai pouvoir est service.",
    9: "Né sous la vibration 9. Humanitaire, généreux, compatissant. Âme ancienne et sage. "
       "Mission de servir le collectif. Venu clore des cycles et enseigner le détachement.",
    11: "Né sous la vibration 11. Maître intuitif. Canalise des énergies supérieures avec sagesse et inspiration. "
        "Présence magnétique. Venu équilibrer la lumière spirituelle avec les pieds sur terre.",
    22: "Né sous la vibration 22. Maître bâtisseur. Capable de transformer les plus grands rêves en réalité concrète. "
        "Vision pratique. Venu bâtir pour l'humanité.",
}

# ============================================================
# ALEMÃO — EXPRESS
# ============================================================
EXPRESS_TXT_DE = {
    1: ("Individualität",
        "Originell, kreativ, geborene Führungspersönlichkeit und unabhängig — Energie des Anfangs und des schöpferischen Impulses.",
        "Egoistisch, arrogant und impulsiv — neigt dazu, Entscheidungen zu zentralisieren und nie zu delegieren.",
        "Demut entwickeln: wahre Führung inspiriert, sie zwingt nicht auf."),
    2: ("Verbundenheit",
        "Diplomatisch, feinfühlig und friedensstiftend — seine Gegenwart beruhigt und harmonisiert jede Umgebung.",
        "Unentschlossen, bedürftig und von der Meinung anderer abhängig — vermeidet Konflikte um jeden Preis.",
        "Selbstvertrauen entwickeln: Ihre Feinfühligkeit ist eine Gabe, keine Schwäche."),
    3: ("Schöpfung",
        "Kreativ, kommunikativ und optimistisch — mit der Gabe des Wortes und des künstlerischen Ausdrucks.",
        "Oberflächlich, zerstreut und übertrieben — verstreut Energie, ohne Projekte zu beenden.",
        "Fokus entwickeln: Qualität vor Quantität."),
    4: ("Arbeit",
        "Praktisch, diszipliniert und zuverlässig — das Fundament jedes Projekts und jedes Teams.",
        "Starr, stur und innovationsresistent — kann durch Angst vor dem Neuen Chancen verlieren.",
        "Flexibilität entwickeln: das Leben verlangt auch Spontaneität."),
    5: ("Freiheit",
        "Vielseitig, abenteuerlustig und magnetisch — dürstet nach Leben und Erfahrungen.",
        "Impulsiv, verantwortungslos und unbedacht — kann durch Unberechenbarkeit geliebte Menschen verletzen.",
        "Freiheit mit Verantwortung in Einklang bringen: wahre Freiheit schließt den Respekt vor anderen ein."),
    6: ("Familie",
        "Verantwortungsvoll, liebevoll und beschützend — die emotionale Säule der Seinen.",
        "Überfürsorglich und übergriffig — neigt dazu, aus Liebe kontrollieren zu wollen.",
        "Lieben ohne zu kontrollieren: für sich zu sorgen heißt auch, für andere zu sorgen."),
    7: ("Weisheit",
        "Weise, analytisch und spirituell — sucht die Wahrheit dort, wo niemand sonst hinsieht.",
        "Kalt, sarkastisch und isoliert — kann sich intellektuell überlegen fühlen.",
        "Vernunft und Gefühl in Einklang bringen: Weisheit hat nur Wert, wenn sie geteilt wird."),
    8: ("Macht",
        "Mächtig, verwirklichend und erfolgreich — geboren zu führen und Wohlstand aufzubauen.",
        "Materialistisch, autoritär und workaholic — kann im Namen des Erfolgs Menschen opfern.",
        "Macht mit Integrität ausüben: wahrer Erfolg misst sich am Guten, das man tut."),
    9: ("Menschlichkeit",
        "Humanitär, großzügig und mitfühlend — erkennt das größere Bild der Existenz.",
        "Melancholisch und zerstreut — neigt dazu, vor der konkreten Wirklichkeit zu fliehen.",
        "Vergeben und loslassen: Losgelöstheit befreit."),
    11: ("Meisterhafter Inspirator",
         "Intuitiv, erleuchtet und visionär — kanalisiert höhere Energien.",
         "Ängstlich, nervös und distanziert — der Druck der hohen Schwingung ist schwer zu ertragen.",
         "Die spirituelle mit der materiellen Welt in Einklang bringen: Erkenntnisse erden."),
    22: ("Meisterhafter Baumeister",
         "Verwirklichend und praktischer Visionär — verwandelt Träume in großem Maßstab in Wirklichkeit.",
         "Übermäßig ehrgeizig und anmaßend — das Gewicht des großen Potenzials kann erdrücken.",
         "Bauen, ohne sich der Arbeit zu versklaven: große Werke brauchen einen Meister in Frieden."),
}

# ============================================================
# ALEMÃO — COMPLETO (SIG mit Metadaten)
# ============================================================
SIG_DE = {
    1: ("Individualität",
        "Symbol: Kreis. Tag: Sonntag. Planet: Sonne. Element: Feuer. Farbe: Gelb. Organe: Herz. "
        "Originell, kreativ, geborene Führungspersönlichkeit, unabhängig, stark, entschlossen, Pionier. Energie des Anfangs, "
        "des schöpferischen Impulses. Menschen mit dieser Zahl sind Visionäre, die keine Angst haben, neue Wege "
        "zu gehen. Sie zeigen Eigeninitiative und sind beim Handeln nicht von anderen abhängig. Positiv kanalisiert, "
        "baut diese Energie Imperien auf und revolutioniert Paradigmen. Ihre Präsenz ist markant und ihre Entschlossenheit unerschütterlich.",
        "Egoistisch, arrogant, herrschsüchtig, impulsiv, stur, ungeduldig. Neigt dazu, Entscheidungen zu zentralisieren und "
        "nie zu delegieren. Kann autoritär und unflexibel werden und jene vertreiben, die an "
        "seinen Projekten mitarbeiten könnten. Das Übermaß an Individualität kann isolieren und Beziehungen schädigen.",
        "Demut entwickeln und lernen, im Team zu arbeiten. Bedenken, dass niemand große Taten "
        "allein vollbringt. Wahre Führung inspiriert, sie zwingt nicht auf. Den Rampenlicht zu teilen erweitert die Kraft "
        "der Verwirklichung und baut dauerhafte Vermächtnisse auf."),
    2: ("Verbundenheit",
        "Symbol: Halbkreis. Tag: Montag. Planet: Mond. Element: Wasser. Farbe: Grün. "
        "Diplomatisch, feinfühlig, kooperativ, friedensstiftend, intuitiv, detailgenau, guter Zuhörer. Seine Gegenwart "
        "beruhigt und harmonisiert Umgebungen. Er hat die Gabe, Menschen zu verbinden und Lösungen zu finden, die allen gefallen. "
        "Seine Intuition ist fein und irrt sich selten in Menschen. Er ist der goldene Faden, der dauerhafte "
        "und bedeutungsvolle Beziehungen webt.",
        "Unentschlossen, bedürftig, unterwürfig, überempfindlich, von der Meinung anderer abhängig, schüchtern. Vermeidet Konflikte "
        "um jeden Preis, selbst wenn eine Positionierung nötig wäre. Kann sich in Beziehungen aufgeben, um "
        "scheinbaren Frieden zu wahren, was innere Frustration erzeugt.",
        "Selbstvertrauen und emotionale Unabhängigkeit entwickeln. Nein sagen, wenn nötig. Ihre Feinfühligkeit "
        "ist eine Gabe, keine Schwäche. Wahrer Friede kommt aus innerem Gleichgewicht, nicht aus äußerer Anerkennung."),
    3: ("Schöpfung",
        "Symbol: Dreieck. Tag: Dienstag. Planet: Jupiter. Element: Luft. Farbe: Violett. "
        "Kreativ, kommunikativ, optimistisch, charismatisch, künstlerisch begabt. Er erhellt jede Umgebung "
        "durch seine Gegenwart. Er hat die Gabe des Wortes und des künstlerischen Ausdrucks. Seine Energie ist ansteckend und "
        "zieht Menschen auf natürliche Weise an. Er verkörpert die Lebensfreude und die grenzenlose Kreativität.",
        "Oberflächlich, zerstreut, übertrieben, dramatisch. Neigt dazu, Energie in viele Richtungen zu verstreuen, ohne "
        "Projekte zu beenden. Kann das dramatische Talent nutzen, um Situationen und Menschen zu manipulieren.",
        "Fokus und Tiefe im Ausdruck entwickeln. So viel Talent in eine konkrete Richtung kanalisieren. "
        "Qualität vor Quantität."),
    4: ("Arbeit",
        "Symbol: Quadrat. Tag: Mittwoch. Planet: Uranus. Element: Erde. Farbe: Blau. "
        "Praktisch, diszipliniert, zuverlässig, loyal, ausdauernd, organisiert, effizient, hingegeben, ehrlich. "
        "Er ist das Fundament jedes Projekts und jedes Teams. Er gibt nicht auf, bis die Arbeit gut gemacht ist. Er schätzt "
        "Stabilität und Sicherheit über alles. Seine Solidität inspiriert Vertrauen bei allen um ihn herum.",
        "Starr, stur, langsam im Wandel, übermäßig materialistisch, innovationsresistent. Kann "
        "an unnötigen Routinen festhalten und durch Angst vor dem Neuen Chancen verlieren.",
        "Flexibilität und Leichtigkeit entwickeln. Nicht alles muss so ernst sein. Das Leben verlangt auch "
        "Spontaneität. Mehr dem Fluss des Lebens vertrauen."),
    5: ("Freiheit",
        "Symbol: Stern. Tag: Donnerstag. Planet: Merkur. Element: Luft. Farbe: Orange. "
        "Frei, vielseitig, abenteuerlustig, fortschrittlich, intelligent, neugierig, anpassungsfähig, magnetisch. "
        "Seine Energie ist ansteckend und zieht neue Menschen und Situationen mühelos an. Er dürstet nach Leben "
        "und Erfahrungen. Er verkörpert Freiheit und Erforschung.",
        "Impulsiv, verantwortungslos, ängstlich, unbedacht, maßlos in Genüssen. Kann jene verletzen, die er liebt, "
        "durch seine Unberechenbarkeit. Übermäßige Freiheit kann zu Zügellosigkeit werden.",
        "Freiheit mit Verantwortung in Einklang bringen. Wahre Freiheit schließt den Respekt vor anderen ein. "
        "Beständigkeit suchen, ohne das Wesen zu verlieren."),
    6: ("Familie",
        "Symbol: Sechseck. Tag: Freitag. Planet: Venus. Element: Erde. Farbe: Rosa. "
        "Verantwortungsvoll, liebevoll, beschützend, gerecht, mitfühlend, künstlerisch, geborener Ratgeber. Er ist die "
        "emotionale Säule der Seinen. Er hat einen scharfen Gerechtigkeitssinn und scheut keine Mühe, um jene zu schützen, die er liebt.",
        "Überfürsorglich, übergriffig, ängstlich um andere. Neigt dazu, aus Liebe kontrollieren zu wollen. Kann sich "
        "für Probleme verantwortlich fühlen, die nicht seine sind.",
        "Lieben ohne zu kontrollieren. Den Raum anderer respektieren. Für sich zu sorgen heißt auch, für andere zu sorgen. "
        "Wahre Liebe ist Freiheit."),
    7: ("Weisheit",
        "Symbol: Siebeneck. Tag: Samstag. Planet: Neptun. Element: Wasser. Farbe: Indigo. "
        "Weise, analytisch, spirituell, intuitiv, perfektionistisch, zurückhaltend, Philosoph, brillanter Geist. "
        "Er sucht die Wahrheit dort, wo niemand sonst hinsieht. Er hat eine tiefe Verbindung zum Unsichtbaren.",
        "Kalt, sarkastisch, isoliert, misstrauisch. Kann sich intellektuell überlegen fühlen. "
        "Einsamkeit kann zu Bitterkeit werden.",
        "Vernunft und Gefühl in Einklang bringen. Wissen teilen. Weisheit hat nur Wert, wenn sie geteilt wird."),
    8: ("Macht",
        "Symbol: Achteck. Tag: Sonntag. Planet: Saturn. Element: Erde. Farbe: Rot. "
        "Mächtig, verwirklichend, erfolgreich, Stratege, ehrgeizig, visionär. Geboren zu führen "
        "und Wohlstand aufzubauen. Er verwandelt Vision in Wirklichkeit mit Effizienz. Er zieht Erfolg auf natürliche Weise an.",
        "Materialistisch, autoritär, workaholic, ungeduldig. Kann im Namen des Erfolgs Menschen opfern. "
        "Macht ohne Ethik korrumpiert.",
        "Macht mit Integrität ausüben. Wahrer Erfolg misst sich am Guten, das man tut. "
        "Geld ist Mittel, nicht Zweck."),
    9: ("Menschlichkeit",
        "Symbol: Neuneck. Tag: Dienstag. Planet: Mars. Element: Feuer. Farbe: Karmesinrot. "
        "Humanitär, großzügig, mitfühlend, weise, tolerant, inspirierend, altruistisch. Er erkennt das größere "
        "Bild der Existenz. Seine Seele ist alt und trägt die Weisheit vieler Leben.",
        "Melancholisch, zerstreut, opferbetont. Neigt dazu, vor der konkreten Wirklichkeit zu fliehen. Flüchtet sich in "
        "unerreichbare Ideale.",
        "Vergeben und loslassen. Dem Fluss des Lebens vertrauen. Losgelöstheit befreit. Für sich sorgen, um "
        "für die Welt zu sorgen."),
    11: ("Meisterhafter Inspirator",
         "Intuitiv, erleuchtet, inspirierend, visionär. Kanalisiert höhere Energien. Zugang zu "
         "Wissen jenseits des Rationalen. Magnetische und inspirierende Präsenz. Er erhebt alle um sich herum "
         "durch sein inneres Licht.",
         "Ängstlich, nervös, distanziert, fanatisch. Der Druck der hohen Schwingung ist schwer zu ertragen. "
         "Kann sich unverstanden und fehl am Platz fühlen.",
         "Die spirituelle mit der materiellen Welt in Einklang bringen. Erkenntnisse erden. Den Körper ebenso "
         "pflegen wie den Geist."),
    22: ("Meisterhafter Baumeister",
         "Verwirklichend, praktischer Visionär. Fähig, Träume in großem Maßstab in Wirklichkeit zu verwandeln. "
         "Er verbindet spirituelle Vision mit konkretem Handeln. Grenzenloses Potenzial. Er ist der Architekt der Zukunft, "
         "der Werke baut, die der Menschheit dienen.",
         "Übermäßig ehrgeizig, gestresst, anmaßend. Das Gewicht des großen Potenzials kann erdrücken und "
         "zur Erschöpfung führen.",
         "Bauen, ohne sich der Arbeit zu versklaven. Das Gleichgewicht zwischen Tun und Sein. Große Werke "
         "brauchen einen Meister in Frieden."),
}

# ============================================================
# ALEMÃO — LEBENSWEG (CAM)
# ============================================================
CAM_DE = {
    1: ("Verwirklichung",
        "Ihre Mission ist es, Wege zu öffnen, zu führen und zu erneuern. Sie sind in die Welt gekommen, um Pionier zu sein, "
        "um Chancen zu schaffen, wo zuvor keine waren. Sie haben Mut, Willenskraft und Entschlossenheit, um "
        "große Taten zu vollbringen. Ihre größte Herausforderung ist zu lernen, dass Führen auch Dienen bedeutet und "
        "andere zu inspirieren, zu glänzen. Menschen wie Napoleon Bonaparte, Walt Disney, Steve Jobs und Pelé "
        "teilen diesen Weg der Verwirklichung und Pionierarbeit."),
    2: ("Frieden und Zusammenarbeit",
        "Ihre Mission ist es, zu kooperieren, auszugleichen und als Brücke zwischen Menschen zu dienen. Sie sind gekommen, um "
        "Harmonie und Diplomatie zu bringen. Ihre Feinfühligkeit ist Ihr wichtigstes Werkzeug. Die Welt braucht Ihre "
        "Fähigkeit, Gegensätze zu verbinden und Konsens zu schaffen. Lady Diana, Abraham Lincoln und Roberto Carlos "
        "sind Beispiele dieses Weges des Friedens."),
    3: ("Freude und Schöpfung",
        "Ihre Mission ist es, zu kommunizieren, zu erschaffen und Freude zu inspirieren. Sie sind gekommen, um die Schönheit des Lebens "
        "durch Kunst und Wort auszudrücken. Ihr Charisma erhellt jene um Sie herum. Oscar Wilde, Charles "
        "Dickens, Jim Carrey und Paul McCartney sind Beispiele dieses Weges der Schöpfung."),
    4: ("Handeln und Struktur",
        "Ihre Mission ist es, zu bauen, zu organisieren und Struktur zu schaffen. Sie sind gekommen, um solide Grundlagen "
        "mit Disziplin zu errichten und Chaos in Ordnung zu verwandeln. Ihre Zuverlässigkeit ist Ihr größter Trumpf. Bill Gates, "
        "Sigmund Freud und Margaret Thatcher teilen diesen Weg des Bauens."),
    5: ("Entwicklung und Freiheit",
        "Ihre Mission ist es, zu erfahren, zu verändern und sich zu entwickeln. Sie sind gekommen, um Paradigmen zu brechen und Befreiung "
        "zu inspirieren. Ihre Vielseitigkeit ist Ihre Triebkraft. Franklin Roosevelt, Cristiano Ronaldo und "
        "Mick Jagger sind Beispiele der Verwandlung."),
    6: ("Ausgleich und Verantwortung",
        "Ihre Mission ist es, zu dienen, zu sorgen und zu harmonisieren. Sie sind gekommen, um Schönheit und Liebe in die Welt zu bringen. "
        "Ihr großzügiges Herz leitet Ihre Schritte und berührt jene um Sie herum. John F. Kennedy, "
        "Elvis Presley und Jeanne d'Arc sind Beispiele dieses Weges."),
    7: ("Weisheit und Vollkommenheit",
        "Ihre Mission ist es, die Wahrheit zu suchen und spirituell zu wachsen. Sie sind gekommen, um die "
        "Geheimnisse der Existenz zu verstehen und Weisheit zu vermitteln. Stephen Hawking, Marie Curie, Nikola Tesla "
        "und Alan Turing teilen diesen Weg des Wissens."),
    8: ("Gerechtigkeit und Wohlstand",
        "Ihre Mission ist es, Fülle mit Weisheit zu manifestieren. Sie sind gekommen, um große Werke zu vollbringen und "
        "zu zeigen, dass Wohlstand und Ethik zusammengehen. Henry Ford, Getúlio Vargas, Silvio Santos und "
        "Julio Iglesias sind Beispiele materieller Verwirklichung mit Sinn."),
    9: ("Weisheit und Humanismus",
        "Ihre Mission ist es, der Menschheit mit Mitgefühl zu dienen. Sie sind gekommen, um Zyklen zu schließen und zu inspirieren. "
        "Ihre Seele trägt die Weisheit vieler Leben. Gandhi, Martin Luther King Jr., Mutter Teresa und "
        "John Lennon sind Beispiele des Dienstes an der Menschheit."),
    11: ("Göttliche Inspiration",
         "Ihre Mission ist es, zu erleuchten und das kollektive Bewusstsein zu heben. Sie sind ein Kanal höherer Intuition. "
         "Winston Churchill, Albert Einstein, Mozart und Marilyn Monroe sind Beispiele dieser Inspiration."),
    22: ("Bauen in großem Maßstab",
         "Ihre Mission ist es, große Werke zu vollbringen, die der Menschheit dienen. Sie sind der Architekt der Zukunft. "
         "Oprah Winfrey, Thomas Edison, Simón Bolívar und Frank Lloyd Wright sind Beispiele des Bauens "
         "in großem Maßstab."),
    33: ("Liebevoller Meister",
         "Deine Mission ist es, das Bewusstsein durch bedingungslose Liebe zu erheben. Du kamst, um Herzen zu heilen."),
}

# ============================================================
# ALEMÃO — HERAUSFORDERUNGEN (DES)
# ============================================================
DES_DE = {
    0: "Natürliches Gleichgewicht. Sie haben in diesem Bereich Gleichgewicht, fließen Sie einfach mit dem Leben.",
    1: "Egoismus überwinden und dienende Führung entwickeln. Wahre Macht liegt darin, andere zu befähigen.",
    2: "Schüchternheit und emotionale Abhängigkeit überwinden. Selbstvertrauen aufbauen, um Bedürfnisse auszudrücken.",
    3: "Zerstreuung vermeiden und Fokus kultivieren. Schöpferische Energie auf konkrete Projekte konzentrieren.",
    4: "Starrheit überwinden und Wandel annehmen. Flexibilität und Anpassung sind Schlüssel zum Wachstum.",
    5: "Maßlosigkeit kontrollieren und Disziplin kultivieren. Freiheit mit Verantwortung führt zur Reife.",
    6: "Überfürsorge vermeiden. Vertrauen, dass Ihre Lieben eigene Entscheidungen treffen können.",
    7: "Isolation überwinden und Wissen mit der Welt teilen. Weisheit existiert nur, wenn sie geteilt wird.",
    8: "Ehrgeiz mit Ethik und Großzügigkeit ausbalancieren. Materieller Erfolg, der anderen dient, ist der wahre.",
    9: "Übermäßige Losgelöstheit überwinden. Lernen, Zyklen ohne Schuld zu schließen und dem Fluss des Lebens zu vertrauen.",
}

# ============================================================
# ALEMÃO — GEBURTSSCHWINGUNG (VIB)
# ============================================================
VIB_DE = {
    1: "Geboren unter Schwingung 1. Geborene Führungspersönlichkeit, Pionier, Individualist. Schöpferische und initiierende Energie. "
       "Hat den Mut, Wege zu öffnen, auf denen niemand gegangen ist. Gekommen, um mit Demut und Dienst zu führen.",
    2: "Geboren unter Schwingung 2. Feinfühlig, diplomatisch, kooperativ. Seine Stärke liegt in Partnerschaft und Harmonie. "
       "Scharfe Intuition. Gekommen, um das Gleichgewicht zwischen Geben und Nehmen zu lernen.",
    3: "Geboren unter Schwingung 3. Kommunikativ, kreativ, optimistisch. Ansteckende Freude. Das Wort ist sein "
       "mächtigstes Werkzeug. Gekommen, um die Welt mit seiner Kunst zu erheitern.",
    4: "Geboren unter Schwingung 4. Fleißig, diszipliniert, praktisch. Solidität baut sichere Grundlagen. "
       "Gekommen, um zu lernen, dass wahre Sicherheit von innen kommt.",
    5: "Geboren unter Schwingung 5. Frei, vielseitig, abenteuerlustig. Seine Energie sucht Erfahrung und Verwandlung. "
       "Neugier bewegt seine Seele. Gekommen, um die Fülle des Lebens zu erfahren.",
    6: "Geboren unter Schwingung 6. Liebevoll, verantwortungsvoll, familienorientiert. Mission zu sorgen und zu harmonisieren. "
       "Liebe ist seine größte Kraft. Gekommen, um zu lernen, dass Lieben Befreien bedeutet.",
    7: "Geboren unter Schwingung 7. Weise, introspectiv, spirituell. Suche nach tiefem Wissen. "
       "Die Stille ist sein Meister. Gekommen, um die Geheimnisse der Existenz zu verstehen.",
    8: "Geboren unter Schwingung 8. Mächtig, verwirklichend, erfolgreich. Seine Energie zieht Fülle an. "
       "Geboren zu bauen. Gekommen, um zu lernen, dass wahre Macht Dienst ist.",
    9: "Geboren unter Schwingung 9. Humanitär, großzügig, mitfühlend. Alte und weise Seele. "
       "Mission, dem Kollektiv zu dienen. Gekommen, um Zyklen zu schließen und Loslassen zu lehren.",
    11: "Geboren unter Schwingung 11. Meisterhafter Intuitiver. Kanalisiert höhere Energien mit Weisheit und Inspiration. "
        "Magnetische Präsenz. Gekommen, um das spirituelle Licht mit beiden Füßen auf der Erde zu balancieren.",
    22: "Geboren unter Schwingung 22. Meisterhafter Baumeister. Fähig, die größten Träume in konkrete Wirklichkeit zu verwandeln. "
        "Praktische Vision. Gekommen, um für die Menschheit zu bauen.",
}

# ============================================================
# ITALIANO — EXPRESS
# ============================================================
EXPRESS_TXT_IT = {
    1: ("Individualità",
        "Originale, creativo, leader nato e indipendente — energia dell'inizio e dell'impulso creatore.",
        "Egoista, arrogante e impulsivo — tende a centralizzare le decisioni e a non delegare mai.",
        "Sviluppare l'umiltà: la vera leadership ispira, non impone."),
    2: ("Associazione",
        "Diplomatico, sensibile e pacificatore — la sua presenza calma e armonizza gli ambienti.",
        "Indeciso, bisognoso e dipendente dall'opinione altrui — evita il conflitto a ogni costo.",
        "Sviluppare la fiducia in sé: la tua sensibilità è un dono, non una debolezza."),
    3: ("Creazione",
        "Creativo, comunicativo e ottimista — dotato del dono della parola e dell'espressione artistica.",
        "Superficiale, disperso ed esagerato — disperde l'energia senza concludere i progetti.",
        "Sviluppare la concentrazione: la qualità prima della quantità."),
    4: ("Lavoro",
        "Pratico, disciplinato e affidabile — è il fondamento di ogni progetto o squadra.",
        "Rigido, testardo e resistente alle novità — può perdere occasioni per paura del nuovo.",
        "Sviluppare la flessibilità: la vita chiede anche spontaneità."),
    5: ("Libertà",
        "Versatile, avventuroso e magnetico — ha sete di vita e di esperienze.",
        "Impulsivo, irresponsabile e inconcludente — può ferire chi ama con la sua imprevedibilità.",
        "Equilibrare libertà e responsabilità: la vera libertà include il rispetto dell'altro."),
    6: ("Famiglia",
        "Responsabile, amorevole e protettivo — è il pilastro emotivo dei suoi.",
        "Iperprotettivo e invadente — tende a voler controllare per amore.",
        "Amare senza controllare: prendersi cura di sé è anche prendersi cura degli altri."),
    7: ("Saggezza",
        "Saggio, analitico e spirituale — cerca la verità dove nessun altro guarda.",
        "Freddo, sarcastico e isolato — può sentirsi intellettualmente superiore.",
        "Equilibrare ragione ed emozione: la saggezza ha valore solo quando è condivisa."),
    8: ("Potere",
        "Potente, realizzatore e prospero — nato per guidare e costruire ricchezza.",
        "Materialista, autoritario e stacanovista — può sacrificare persone in nome del successo.",
        "Usare il potere con integrità: il vero successo si misura dal bene che si fa."),
    9: ("Umanità",
        "Umanitario, generoso e compassionevole — vede il quadro più ampio dell'esistenza.",
        "Malinconico e disperso — tende a fuggire dalla realtà concreta.",
        "Perdonare e lasciar andare: il distacco è liberatorio."),
    11: ("Maestro Ispiratore",
         "Intuitivo, illuminato e visionario — canalizza energie superiori.",
         "Ansioso, nervoso e distante — la pressione dell'alta vibrazione è difficile da sopportare.",
         "Equilibrare il mondo spirituale con il materiale: radicare le intuizioni."),
    22: ("Maestro Costruttore",
         "Realizzatore e visionario pratico — trasforma i sogni in realtà su larga scala.",
         "Ambizioso in eccesso e prepotente — il peso del grande potenziale può schiacciare.",
         "Costruire senza farsi schiavo del lavoro: le grandi opere hanno bisogno di un maestro in pace."),
}

# ============================================================
# ITALIANO — COMPLETO (SIG con metadati)
# ============================================================
SIG_IT = {
    1: ("Individualità",
        "Simbolo: Cerchio. Giorno: Domenica. Pianeta: Sole. Elemento: Fuoco. Colore: Giallo. Organi: Cuore. "
        "Originale, creativo, leader nato, indipendente, forte, determinato, pioniere. Energia dell'inizio, "
        "dell'impulso creatore. Le persone con questo numero sono visionarie che non temono di percorrere strade "
        "nuove. Hanno iniziativa propria e non dipendono dagli altri per agire. Quando è canalizzata positivamente, "
        "questa energia costruisce imperi e rivoluziona paradigmi. La loro presenza è notevole e la loro determinazione incrollabile.",
        "Egoista, arrogante, dominatore, impulsivo, testardo, impaziente. Tende a centralizzare le decisioni e "
        "a non delegare mai. Può diventare autoritario e inflessibile, allontanando chi potrebbe collaborare "
        "ai suoi progetti. L'eccesso di individualità può isolarlo e danneggiare le relazioni.",
        "Sviluppare l'umiltà e saper lavorare in squadra. Ricordare che nessuno compie grandi imprese "
        "da solo. La vera leadership ispira, non impone. Condividere il protagonismo amplia il potere "
        "di realizzazione e costruisce lasciti duraturi."),
    2: ("Associazione",
        "Simbolo: Semicerchio. Giorno: Lunedì. Pianeta: Luna. Elemento: Acqua. Colore: Verde. "
        "Diplomatico, sensibile, cooperativo, pacificatore, intuitivo, attento ai dettagli, buon ascoltatore. La sua presenza "
        "calma e armonizza gli ambienti. Ha il dono di unire le persone e di trovare soluzioni che piacciono a tutti. "
        "La sua intuizione è raffinata e raramente si sbaglia sulle persone. È il filo d'oro che tesse relazioni "
        "durature e significative.",
        "Indeciso, bisognoso, sottomesso, ipersensibile, dipendente dall'opinione altrui, timido. Evita i conflitti "
        "a ogni costo, anche quando è necessario prendere posizione. Può annullarsi nelle relazioni per mantenere "
        "una pace apparente, cosa che genera frustrazione interiore.",
        "Sviluppare la fiducia in sé e l'indipendenza emotiva. Dire di no quando serve. La tua sensibilità "
        "è un dono, non una debolezza. La vera pace viene dall'equilibrio interiore, non dall'approvazione esterna."),
    3: ("Creazione",
        "Simbolo: Triangolo. Giorno: Martedì. Pianeta: Giove. Elemento: Aria. Colore: Viola. "
        "Creativo, comunicativo, ottimista, carismatico, dotato per le arti. Illumina ogni ambiente "
        "con la sua presenza. Ha il dono della parola e dell'espressione artistica. La sua energia è contagiosa e "
        "attrae le persone naturalmente. È la personificazione della gioia di vivere e della creatività senza limiti.",
        "Superficiale, disperso, esagerato, drammatico. Tende a spargere energia in molte direzioni senza "
        "concludere i progetti. Può usare il talento drammatico per manipolare situazioni e persone.",
        "Sviluppare concentrazione e profondità nell'espressione. Canalizzare tanto talento in una direzione precisa. "
        "La qualità prima della quantità."),
    4: ("Lavoro",
        "Simbolo: Quadrato. Giorno: Mercoledì. Pianeta: Urano. Elemento: Terra. Colore: Blu. "
        "Pratico, disciplinato, affidabile, leale, persistente, organizzato, efficiente, dedito, onesto. "
        "È il fondamento di ogni progetto o squadra. Non si arrende finché il lavoro non è ben fatto. Valorizza "
        "la stabilità e la sicurezza sopra ogni cosa. La sua solidità ispira fiducia in tutti coloro che lo circondano.",
        "Rigido, testardo, lento al cambiamento, materialista in eccesso, resistente alle novità. Può "
        "attaccarsi a routine inutili e perdere occasioni per paura del nuovo.",
        "Sviluppare flessibilità e leggerezza. Non tutto deve essere così serio. La vita chiede anche "
        "spontaneità. Fidarsi di più del flusso della vita."),
    5: ("Libertà",
        "Simbolo: Stella. Giorno: Giovedì. Pianeta: Mercurio. Elemento: Aria. Colore: Arancione. "
        "Libero, versatile, avventuroso, progressista, intelligente, curioso, adattabile, magnetico. "
        "La sua energia è contagiosa e attrae con facilità persone e situazioni nuove. Ha sete di vita "
        "e di esperienze. È la personificazione della libertà e dell'esplorazione.",
        "Impulsivo, irresponsabile, ansioso, inconcludente, eccessivo nei piaceri. Può ferire chi ama "
        "con la sua imprevedibilità. L'eccesso di libertà può diventare libertinaggio.",
        "Equilibrare libertà e responsabilità. La vera libertà include il rispetto dell'altro. "
        "Cercare coerenza senza perdere l'essenza."),
    6: ("Famiglia",
        "Simbolo: Esagono. Giorno: Venerdì. Pianeta: Venere. Elemento: Terra. Colore: Rosa. "
        "Responsabile, amorevole, protettivo, giusto, compassionevole, artistico, consigliere nato. È il pilastro "
        "emotivo dei suoi. Ha un acuto senso di giustizia e non risparmia sforzi per proteggere chi ama.",
        "Iperprotettivo, invadente, ansioso per gli altri. Tende a voler controllare per amore. Può "
        "sentirsi responsabile di problemi che non sono suoi.",
        "Amare senza controllare. Rispettare lo spazio altrui. Prendersi cura di sé è anche prendersi cura degli altri. "
        "Il vero amore è libertà."),
    7: ("Saggezza",
        "Simbolo: Ettagono. Giorno: Sabato. Pianeta: Nettuno. Elemento: Acqua. Colore: Indaco. "
        "Saggio, analitico, spirituale, intuitivo, perfezionista, riservato, filosofo, mente brillante. "
        "Cerca la verità dove nessun altro guarda. Ha una connessione profonda con l'invisibile.",
        "Freddo, sarcastico, isolato, diffidente. Può sentirsi intellettualmente superiore. "
        "La solitudine può trasformarsi in amarezza.",
        "Equilibrare ragione ed emozione. Condividere la conoscenza. La saggezza ha valore solo quando è condivisa."),
    8: ("Potere",
        "Simbolo: Ottagono. Giorno: Domenica. Pianeta: Saturno. Elemento: Terra. Colore: Rosso. "
        "Potente, realizzatore, prospero, stratega, ambizioso, visionario. Nato per guidare "
        "e costruire ricchezza. Trasforma la visione in realtà con efficienza. Attrae il successo naturalmente.",
        "Materialista, autoritario, stacanovista, impaziente. Può sacrificare persone in nome del successo. "
        "Il potere senza etica corrompe.",
        "Usare il potere con integrità. Il vero successo si misura dal bene che si fa. "
        "Il denaro è un mezzo, non un fine."),
    9: ("Umanità",
        "Simbolo: Nonagono. Giorno: Martedì. Pianeta: Marte. Elemento: Fuoco. Colore: Cremisi. "
        "Umanitario, generoso, compassionevole, saggio, tollerante, ispiratore, altruista. Vede il quadro "
        "più ampio dell'esistenza. La sua anima è antica e porta la saggezza di molte vite.",
        "Malinconico, disperso, vittimista. Tende a fuggire dalla realtà concreta. Si rifugia in ideali "
        "irraggiungibili.",
        "Perdonare e lasciar andare. Fidarsi del flusso della vita. Il distacco è liberatorio. Prendersi cura di sé per "
        "prendersi cura del mondo."),
    11: ("Maestro Ispiratore",
         "Intuitivo, illuminato, ispiratore, visionario. Canalizza energie superiori. Accesso alla "
         "conoscenza oltre il razionale. Presenza magnetica e ispiratrice. Eleva tutti coloro che lo circondano "
         "con la sua luce interiore.",
         "Ansioso, nervoso, distante, fanatico. La pressione dell'alta vibrazione è difficile da sopportare. "
         "Può sentirsi incompreso e fuori posto.",
         "Equilibrare il mondo spirituale con il materiale. Radicare le intuizioni. Prendersi cura del corpo tanto "
         "quanto dello spirito."),
    22: ("Maestro Costruttore",
         "Realizzatore, visionario pratico. Capace di trasformare i sogni in realtà su larga scala. "
         "Combina visione spirituale e azione concreta. Potenziale illimitato. È l'architetto del futuro, "
         "che costruisce opere che beneficiano l'umanità.",
         "Ambizioso in eccesso, stressato, prepotente. Il peso del grande potenziale può schiacciare e "
         "portare all'esaurimento.",
         "Costruire senza farsi schiavo del lavoro. L'equilibrio tra fare ed essere. Le grandi opere "
         "hanno bisogno di un maestro in pace."),
}

# ============================================================
# ITALIANO — CAMMINO DI VITA (CAM)
# ============================================================
CAM_IT = {
    1: ("Realizzazione",
        "La tua missione è aprire strade, guidare e innovare. Sei venuto al mondo per essere pioniere, per "
        "creare opportunità dove prima non esistevano. Hai coraggio, forza di volontà e determinazione per "
        "raggiungere grandi imprese. La tua più grande sfida è imparare che guidare significa anche servire e "
        "ispirare gli altri a brillare. Persone come Napoleone Bonaparte, Walt Disney, Steve Jobs e Pelé "
        "condividono questo cammino di realizzazione e pionierismo."),
    2: ("Pace e Cooperazione",
        "La tua missione è cooperare, equilibrare e servire come ponte tra le persone. Sei venuto per portare "
        "armonia e diplomazia. La tua sensibilità è il tuo strumento più potente. Il mondo ha bisogno della tua "
        "capacità di unire gli opposti e creare consenso. Lady Diana, Abraham Lincoln e Roberto Carlos "
        "sono esempi di questo percorso di pace."),
    3: ("Gioia e Creazione",
        "La tua missione è comunicare, creare e ispirare gioia. Sei venuto per esprimere la bellezza della vita "
        "attraverso l'arte e la parola. Il tuo carisma illumina chi ti sta intorno. Oscar Wilde, Charles "
        "Dickens, Jim Carrey e Paul McCartney sono esempi di questo cammino di creazione."),
    4: ("Azione e Struttura",
        "La tua missione è costruire, organizzare e creare struttura. Sei venuto per stabilire basi solide "
        "con disciplina e trasformare il caos in ordine. La tua affidabilità è il tuo miglior punto di forza. Bill Gates, "
        "Sigmund Freud e Margaret Thatcher condividono questo percorso di costruzione."),
    5: ("Evoluzione e Libertà",
        "La tua missione è sperimentare, cambiare ed evolvere. Sei venuto per rompere i paradigmi e ispirare "
        "la liberazione. La tua versatilità è la tua forza motrice. Franklin Roosevelt, Cristiano Ronaldo e "
        "Mick Jagger sono esempi di trasformazione."),
    6: ("Conciliare e Responsabilità",
        "La tua missione è servire, prenderti cura e armonizzare. Sei venuto per creare bellezza e amore nel mondo. "
        "Il tuo cuore generoso guida i tuoi passi e tocca chi ti sta intorno. John F. Kennedy, "
        "Elvis Presley e Giovanna d'Arco sono esempi di questo cammino."),
    7: ("Saggezza e Perfezione",
        "La tua missione è cercare la verità ed evolvere spiritualmente. Sei venuto per comprendere i "
        "misteri dell'esistenza e trasmettere saggezza. Stephen Hawking, Marie Curie, Nikola Tesla "
        "e Alan Turing condividono questo cammino di conoscenza."),
    8: ("Giustizia e Prosperità",
        "La tua missione è manifestare abbondanza con saggezza. Sei venuto per realizzare grandi opere e "
        "dimostrare che prosperità ed etica vanno insieme. Henry Ford, Getúlio Vargas, Silvio Santos e "
        "Julio Iglesias sono esempi di realizzazione materiale con scopo."),
    9: ("Saggezza e Umanitarismo",
        "La tua missione è servire l'umanità con compassione. Sei venuto per chiudere cicli e ispirare. "
        "La tua anima porta la saggezza di molte vite. Gandhi, Martin Luther King Jr., Madre Teresa e "
        "John Lennon sono esempi di servizio all'umanità."),
    11: ("Ispirazione Divina",
         "La tua missione è illuminare ed elevare la coscienza collettiva. Sei un canale di intuizione superiore. "
         "Winston Churchill, Albert Einstein, Mozart e Marilyn Monroe sono esempi di questa ispirazione."),
    22: ("Costruzione su Larga Scala",
         "La tua missione è realizzare grandi opere che beneficiano l'umanità. Sei l'architetto del futuro. "
         "Oprah Winfrey, Thomas Edison, Simón Bolívar e Frank Lloyd Wright sono esempi di costruzione "
         "su larga scala."),
    33: ("Maestro Amoroso",
         "La tua missione è elevare la coscienza attraverso l'amore incondizionato. Sei venuto per guarire i cuori."),
}

# ============================================================
# ITALIANO — SFIDE (DES)
# ============================================================
DES_IT = {
    0: "Equilibrio naturale. Hai equilibrio in quest'area, semplicemente segui il flusso della vita.",
    1: "Superare l'egoismo e sviluppare una leadership servente. Il vero potere sta nel dare potere agli altri.",
    2: "Vincere la timidezza e la dipendenza emotiva. Sviluppare fiducia in sé per esprimere i propri bisogni.",
    3: "Evitare la dispersione e coltivare la concentrazione. Concentrare l'energia creativa su progetti concreti.",
    4: "Superare la rigidità e abbracciare i cambiamenti. Flessibilità e adattamento sono chiavi per la crescita.",
    5: "Controllare gli eccessi e coltivare la disciplina. La libertà con responsabilità porta alla maturità.",
    6: "Evitare l'iperprotezione. Fidarsi che i propri cari possano fare le proprie scelte.",
    7: "Vincere l'isolamento e condividere la propria conoscenza con il mondo. La saggezza esiste solo quando è condivisa.",
    8: "Equilibrare l'ambizione con l'etica e la generosità. Il successo materiale che beneficia gli altri è quello vero.",
    9: "Superare il distacco eccessivo. Imparare a chiudere i cicli senza colpa e fidarsi del flusso della vita.",
}

# ============================================================
# ITALIANO — VIBRAZIONE DI NASCITA (VIB)
# ============================================================
VIB_IT = {
    1: "Nato sotto la vibrazione 1. Leader nato, pioniere, individualista. Energia creatrice e iniziatrice. "
       "Ha il coraggio di aprire strade dove nessuno ha camminato. Venuto per imparare a guidare con umiltà e servizio.",
    2: "Nato sotto la vibrazione 2. Sensibile, diplomatico, cooperativo. La sua forza sta nella partnership e nell'armonia. "
       "Intuizione acuta. Venuto per imparare l'equilibrio tra dare e ricevere.",
    3: "Nato sotto la vibrazione 3. Comunicativo, creativo, ottimista. Gioia contagiosa. La parola è il suo "
       "strumento più potente. Venuto per allietare il mondo con la sua arte.",
    4: "Nato sotto la vibrazione 4. Lavoratore, disciplinato, pratico. La solidità costruisce basi sicure. "
       "Venuto per imparare che la vera sicurezza viene da dentro.",
    5: "Nato sotto la vibrazione 5. Libero, versatile, avventuroso. La sua energia cerca esperienza e trasformazione. "
       "La curiosità muove la sua anima. Venuto per sperimentare la pienezza della vita.",
    6: "Nato sotto la vibrazione 6. Amorevole, responsabile, familiare. Missione di curare e armonizzare. "
       "L'amore è la sua più grande forza. Venuto per imparare che amare è liberare.",
    7: "Nato sotto la vibrazione 7. Saggio, introspettivo, spirituale. Ricerca della conoscenza profonda. "
       "Il silenzio è il suo maestro. Venuto per comprendere i misteri dell'esistenza.",
    8: "Nato sotto la vibrazione 8. Potente, realizzatore, prospero. La sua energia attrae l'abbondanza. "
       "Nato per costruire. Venuto per imparare che il vero potere è servizio.",
    9: "Nato sotto la vibrazione 9. Umanitario, generoso, compassionevole. Anima antica e saggia. "
       "Missione di servire il collettivo. Venuto per chiudere cicli e insegnare il distacco.",
    11: "Nato sotto la vibrazione 11. Maestro intuitivo. Canalizza energie superiori con saggezza e ispirazione. "
        "Presenza magnetica. Venuto per equilibrare la luce spirituale con i piedi per terra.",
    22: "Nato sotto la vibrazione 22. Maestro costruttore. Capace di trasformare i più grandi sogni in realtà concreta. "
        "Visione pratica. Venuto per costruire per l'umanità.",
}

# ============================================================
# JAPONÊS — EXPRESS
# ============================================================
EXPRESS_TXT_JA = {
    1: ("個性",
        "独創的で創造力豊か、生まれながらのリーダー。始まりと創造の衝動のエネルギーを持ちます。",
        "利己的で傲慢、衝動的になりがち。決定を集中させ、委任しようとしません。",
        "謙虚さを育むこと。真のリーダーシップは押し付けるのではなく、鼓舞するものです。"),
    2: ("調和",
        "外交的で繊細、平和を導く人。その存在は場を落ち着かせ、調和させます。",
        "優柔不断で依存心が強く、他人の意見に左右されがち。対立を何としても避けます。",
        "自信を育むこと。あなたの繊細さは弱さではなく、贈り物です。"),
    3: ("創造",
        "創造的でコミュニケーション上手、楽観的。言葉と芸術表現の才能に恵まれています。",
        "表面的で散漫、誇張しがち。エネルギーを分散させ、企画を完成させません。",
        "集中力を育むこと。量より質です。"),
    4: ("仕事",
        "実直的で規律正しく、信頼できる人。あらゆる企画やチームの土台となります。",
        "頑固で融通が利かず、革新に抵抗します。新しいものへの恐れから機会を逃しがちです。",
        "柔軟性を育むこと。人生には自発性も求められます。"),
    5: ("自由",
        "多才で冒険心旺盛、魅力的。人生と経験への渇望があります。",
        "衝動的で無責任、無分別になりがち。予測不能さで愛する人を傷つけることがあります。",
        "自由と責任のバランスを取ること。真の自由には他者への敬意が含まれます。"),
    6: ("家族",
        "責任感が強く愛情深く、保護的。家族の心の支えです。",
        "過保護で干渉しがち。愛ゆえに支配しようとします。",
        "支配せずに愛すること。自分を大切にすることも、他人を大切にすることです。"),
    7: ("知恵",
        "賢明で分析的、精神的。誰も見ない場所で真実を探します。",
        "冷たく皮肉で孤立しがち。知的に優越感を持つことがあります。",
        "理性と感情のバランスを取ること。知恵は分かち合ってこそ価値があります。"),
    8: ("力",
        "力強く実現力があり、繁栄する人。導き、富を築くために生まれました。",
        "物質主義的で権威的、仕事中毒になりがち。成功のために人を犠牲にすることがあります。",
        "誠実に力を使うこと。真の成功は行った善によって測られます。"),
    9: ("人類愛",
        "人道主義的で寛大、思いやり深い。存在の大きな全体像を見通します。",
        "憂鬱で散漫になりがち。具体的な現実から逃れようとします。",
        "許し、手放すこと。執着を手放すことが解放につながります。"),
    11: ("導き手のマスター",
         "直感的で悟りを開き、先見性がある。高次のエネルギーを引き寄せます。",
         "不安で神経質、距離を置きがち。高い波動のプレッシャーは耐え難いものです。",
         "精神世界と物質世界のバランスを取ること。直感を地に足のついたものに。"),
    22: ("建設者のマスター",
         "実現力があり、実践的な先見者。夢を大規模に現実へと変えます。",
         "過度な野心と傲慢さ。大きな可能性の重みが押しつぶすことがあります。",
         "仕事に縛られずに築くこと。偉大な作品には平和なマイスターが必要です。"),
}

# ============================================================
# JAPONÊS — COMPLETO (SIG メタデータ付き)
# ============================================================
SIG_JA = {
    1: ("個性",
        "シンボル：円。曜日：日曜日。惑星：太陽。要素：火。色：黄色。臓器：心臓。"
        "独創的、創造的、生まれながらのリーダー、独立的、強靭、決断力がある、先駆者。始まりと創造の衝動のエネルギー。"
        "この数を持つ人は、新しい道を歩むことを恐れない先見者です。自らの意志で行動し、他人に依存しません。"
        "前向きに活かせば、このエネルギーは帝国を築き、パラダイムを革新します。その存在感は際立ち、決意は揺るぎません。",
        "利己的、傲慢、支配的、衝動的、頑固、せっかち。決定を集中させ、委任しようとしません。"
        "権威的で融通が利かなくなり、協力してくれる人々を遠ざけることがあります。"
        "過度な個人主義は孤立を招き、人間関係を損なうことがあります。",
        "謙虚さを育み、チームで働くことを学ぶこと。偉業は一人では成し遂げられないと心に留めること。"
        "真のリーダーシップは押し付けるのではなく、鼓舞するものです。主役を分かち合うことで実現力が広がり、"
        "永続する遺産が築かれます。"),
    2: ("調和",
        "シンボル：半円。曜日：月曜日。惑星：月。要素：水。色：緑。"
        "外交的、繊細、協調的、平和を導く、直感的、細部に気づく、聞き上手。その存在は場を落ち着かせ、調和させます。"
        "人々を結びつけ、皆が満足する解決策を見出す才能があります。直感は鋭く、人を見誤ることはほとんどありません。"
        "永続的で意義深い関係を織りなす金の糸です。",
        "優柔不断、依存心、従順、過敏、他人の意見に左右される、内気。"
        "立場を明確にすべき時でも、対立を何としても避けます。"
        "見せかけの平和を保つために関係の中で自分を殺し、内面に不満を蓄積することがあります。",
        "自信と情緒的な自立を育むこと。必要な時には「いいえ」と言えること。"
        "あなたの繊細さは弱さではなく、贈り物です。真の平和は外からの承認ではなく、内なる均衡から生まれます。"),
    3: ("創造",
        "シンボル：三角形。曜日：火曜日。惑星：木星。要素：風。色：紫。"
        "創造的、コミュニケーション上手、楽観的、カリスマ的、芸術の才能。その存在で場を照らします。"
        "言葉と芸術表現の才能に恵まれています。エネルギーは伝染し、自然に人を引き寄せます。"
        "生きる喜びと無限の創造性の体現者です。",
        "表面的、散漫、誇張、芝居がかり。エネルギーを多方面に分散させ、企画を完成させません。"
        "芝居がかった才能を使って状況や人を操ることがあります。",
        "表現における集中力と深みを育むこと。才能を具体的な方向に注ぐこと。量より質です。"),
    4: ("仕事",
        "シンボル：四角形。曜日：水曜日。惑星：天王星。要素：土。色：青。"
        "実直的、規律正しい、信頼できる、誠実、粘り強い、整理整頓が得意、効率的、献身的、正直。"
        "あらゆる企画やチームの土台です。仕事がきちんと仕上がるまで諦めません。"
        "何よりも安定と安心を重んじます。その堅実さは周囲すべての信頼を集めます。",
        "頑固、融通が利かない、変化が遅い、過度な物質主義、革新への抵抗。"
        "不要な習慣に固執し、新しいものへの恐れから機会を逃すことがあります。",
        "柔軟性と軽やかさを育むこと。すべてがそれほど深刻である必要はありません。"
        "人生には自発性も求められます。人生の流れにもっと身を委ねること。"),
    5: ("自由",
        "シンボル：星。曜日：木曜日。惑星：水星。要素：風。色：オレンジ。"
        "自由、多才、冒険心旺盛、進歩的、知的、好奇心旺盛、適応力がある、魅力的。"
        "エネルギーは伝染し、新しい人や状況を容易に引き寄せます。人生と経験への渇望があります。"
        "自由と探求の体現者です。",
        "衝動的、無責任、不安、無分別、快楽に溺れがち。予測不能さで愛する人を傷つけることがあります。"
        "過度な自由は放縦になり得ます。",
        "自由と責任のバランスを取ること。真の自由には他者への敬意が含まれます。"
        "本質を失わずに一貫性を求めること。"),
    6: ("家族",
        "シンボル：六角形。曜日：金曜日。惑星：金星。要素：土。色：ピンク。"
        "責任感が強い、愛情深い、保護的、公正、思いやり深い、芸術的、生まれながらの助言者。家族の心の支えです。"
        "正義感が鋭く、愛する人を守るために努力を惜しみません。",
        "過保護、干渉しがち、他人への過度な心配。愛ゆえに支配しようとします。"
        "自分の問題ではないことに責任を感じることがあります。",
        "支配せずに愛すること。他人の空間を尊重すること。自分を大切にすることは、他人を大切にすることでもあります。"
        "真の愛は自由です。"),
    7: ("知恵",
        "シンボル：七角形。曜日：土曜日。惑星：海王星。要素：水。色：藍。"
        "賢明、分析的、精神的、直感的、完璧主義的、控えめ、哲学的、優れた知性。誰も見ない場所で真実を探します。"
        "目に見えないものとの深い繋がりがあります。",
        "冷たい、皮肉、孤立、疑い深い。知的に優越感を持つことがあります。"
        "孤独が苦々しさに変わることもあります。",
        "理性と感情のバランスを取ること。知識を分かち合うこと。知恵は分かち合ってこそ価値があります。"),
    8: ("力",
        "シンボル：八角形。曜日：日曜日。惑星：土星。要素：土。色：赤。"
        "力強い、実現力がある、繁栄する、戦略家、野心的、先見的。導き、富を築くために生まれました。"
        "ビジョンを効率的に現実へと変えます。自然に成功を引き寄せます。",
        "物質主義的、権威的、仕事中毒、せっかち。成功のために人を犠牲にすることがあります。"
        "倫理なき力は堕落します。",
        "誠実に力を使うこと。真の成功は行った善によって測られます。金銭は手段であり、目的ではありません。"),
    9: ("人類愛",
        "シンボル：九角形。曜日：火曜日。惑星：火星。要素：火。色：深紅。"
        "人道主義的、寛大、思いやり深い、賢明、寛容、鼓舞する、利他的。存在の大きな全体像を見通します。"
        "その魂は古く、幾多の人生の知恵を宿しています。",
        "憂鬱、散漫、被害者意識。具体的な現実から逃れようとします。"
        "手の届かない理想に逃げ込みます。",
        "許し、手放すこと。人生の流れを信頼すること。執着を手放すことが解放につながります。"
        "世界のために自分を大切にすること。"),
    11: ("導き手のマスター",
         "直感的、悟りを開いた、鼓舞する、先見的。高次のエネルギーを引き寄せます。理性を超えた知識へのアクセス。"
         "磁力的で鼓舞する存在感。内なる光で周囲すべてを高めます。",
         "不安、神経質、距離を置く、狂信的。高い波動のプレッシャーは耐え難いものです。"
         "理解されず、場違いだと感じることがあります。",
         "精神世界と物質世界のバランスを取ること。直感を地に足のついたものに。"
         "精神と同じくらい身体も大切にすること。"),
    22: ("建設者のマスター",
         "実現力がある、実践的な先見者。夢を大規模に現実へと変える力。精神的なビジョンと具体的な行動を結びつけます。"
         "無限の可能性。未来の建築家として、人類に資する作品を築きます。",
         "過度な野心、ストレス、傲慢。大きな可能性の重みが押しつぶし、"
         "燃え尽きにつながることがあります。",
         "仕事に縛られずに築くこと。行うことと在ることの均衡。偉大な作品には平和なマイスターが必要です。"),
}

# ============================================================
# JAPONÊS — ライフパス (CAM)
# ============================================================
CAM_JA = {
    1: ("達成",
        "あなたの使命は道を開き、導き、革新することです。先駆者として、これまで存在しなかった機会を創り出すために生まれました。"
        "偉業を成し遂げる勇気、意志力、決断力があります。最大の課題は、導くことは仕えることでもあり、"
        "他者が輝くよう鼓舞することだと学ぶことです。ナポレオン・ボナパルト、ウォルト・ディズニー、スティーブ・ジョブズ、ペレのような人々が"
        "この達成と先駆者の道を共有しています。"),
    2: ("平和と協力",
        "あなたの使命は協力し、均衡を取り、人と人との橋渡しをすることです。調和と外交をもたらすために生まれました。"
        "あなたの繊細さが最大の道具です。世界は対立するものを結びつけ、合意を創り出すあなたの力を必要としています。"
        "ダイアナ妃、エイブラハム・リンカーン、ロベルト・カルロスがこの平和の道の例です。"),
    3: ("喜びと創造",
        "あなたの使命は伝え、創り出し、喜びを鼓舞することです。芸術と言葉を通じて人生の美しさを表現するために生まれました。"
        "あなたのカリスマは周囲を照らします。オスカー・ワイルド、チャールズ・ディケンズ、ジム・キャリー、"
        "ポール・マッカートニーがこの創造の道の例です。"),
    4: ("行動と構造",
        "あなたの使命は築き、組織し、構造を創り出すことです。規律をもって強固な基盤を築き、混沌を秩序へと変えるために生まれました。"
        "あなたの信頼性が最大の強みです。ビル・ゲイツ、ジークムント・フロイト、マーガレット・サッチャーが"
        "この建設の道を共有しています。"),
    5: ("進化と自由",
        "あなたの使命は経験し、変わり、進化することです。パラダイムを打ち破り、解放を鼓舞するために生まれました。"
        "あなたの多才さが原動力です。フランクリン・ルーズベルト、クリスティアーノ・ロナウド、"
        "ミック・ジャガーが変革の例です。"),
    6: ("調停と責任",
        "あなたの使命は仕え、ケアし、調和させることです。世界に美と愛を創り出すために生まれました。"
        "あなたの寛大な心が歩みを導き、周囲に触れます。ジョン・F・ケネディ、エルヴィス・プレスリー、"
        "ジャンヌ・ダルクがこの道の例です。"),
    7: ("知恵と完成",
        "あなたの使命は真実を求め、精神的に進化することです。存在の神秘を理解し、知恵を伝えるために生まれました。"
        "スティーブン・ホーキング、マリー・キュリー、ニコラ・テスラ、アラン・チューリングが"
        "この知識の道を共有しています。"),
    8: ("正義と繁栄",
        "あなたの使命は知恵をもって豊かさを顕現させることです。偉業を成し遂げ、繁栄と倫理が両立することを示すために生まれました。"
        "ヘンリー・フォード、ジェトゥリオ・ヴァルガス、シルビオ・サントス、"
        "フリオ・イグレシアスが目的ある物質的実現の例です。"),
    9: ("知恵と人道主義",
        "あなたの使命は思いやりをもって人類に仕えることです。周期を閉じ、鼓舞するために生まれました。"
        "あなたの魂は幾多の人生の知恵を宿しています。ガンジー、マーティン・ルーサー・キング・ジュニア、マザー・テレサ、"
        "ジョン・レノンが人類への奉仕の例です。"),
    11: ("神聖なインスピレーション",
         "あなたの使命は集合的意識を照らし、高めることです。高次の直感のチャネルです。"
         "ウィンストン・チャーチル、アルバート・アインシュタイン、モーツァルト、マリリン・モンローがこのインスピレーションの例です。"),
    22: ("大規模な建設",
         "あなたの使命は人類に資する偉業を成し遂げることです。あなたは未来の建築家です。"
         "オプラ・ウィンフリー、トーマス・エジソン、シモン・ボリバル、フランク・ロイド・ライトが"
         "大規模な建設の例です。"),
    33: ("愛のマスター",
         "あなたの使命は、無条件の愛を通じて意識を高めること。心を癒すために生まれてきたのです。"),
}

# ============================================================
# JAPONÊS — 課題 (DES)
# ============================================================
DES_JA = {
    0: "自然な均衡。この領域では均衡が保たれています。人生の流れに身を委ねてください。",
    1: "利己心を克服し、奉仕するリーダーシップを育むこと。真の力は他者を力づけることにあります。",
    2: "内気さと情緒的依存を克服すること。自分のニーズを表現する自信を育むこと。",
    3: "散漫を避け、集中力を養うこと。創造エネルギーを具体的な企画に注ぐこと。",
    4: "頑固さを克服し、変化を受け入れること。柔軟性と適応力が成長の鍵です。",
    5: "過剰を抑え、規律を養うこと。責任を伴う自由が成熟へと導きます。",
    6: "過保護を避けること。大切な人が自ら選択できると信頼すること。",
    7: "孤立を克服し、知識を世界と分かち合うこと。知恵は分かち合ってこそ存在します。",
    8: "野心と倫理、寛大さのバランスを取ること。他者に資する物質的成功こそ真の成功です。",
    9: "過度な執着のなさを克服すること。罪悪感なく周期を閉じ、人生の流れを信頼することを学ぶこと。",
}

# ============================================================
# JAPONÊS — 誕生の波動 (VIB)
# ============================================================
VIB_JA = {
    1: "波動1のもとに生まれました。生まれながらのリーダー、先駆者、個人主義者。創造的で開始のエネルギー。"
       "誰も歩んだことのない道を開く勇気があります。謙虚さと奉仕をもって導くことを学ぶために生まれました。",
    2: "波動2のもとに生まれました。繊細で外交的、協調的。その力は協働と調和にあります。"
       "鋭い直感。与えることと受け取ることの均衡を学ぶために生まれました。",
    3: "波動3のもとに生まれました。コミュニケーション上手で創造的、楽観的。伝染する喜び。言葉が最も強力な道具です。"
       "その芸術で世界を明るくするために生まれました。",
    4: "波動4のもとに生まれました。勤勉で規律正しく、実直的。堅実さが安全な基盤を築きます。"
       "真の安全は内側から来ることを学ぶために生まれました。",
    5: "波動5のもとに生まれました。自由で多才、冒険心旺盛。そのエネルギーは経験と変容を求めます。"
       "好奇心が魂を動かします。人生の充実を経験するために生まれました。",
    6: "波動6のもとに生まれました。愛情深く責任感が強く、家族的。ケアし調和させる使命。"
       "愛が最大の力です。愛することは解放することだと学ぶために生まれました。",
    7: "波動7のもとに生まれました。賢明で内省的、精神的。深い知識の探求。"
       "沈黙が師です。存在の神秘を理解するために生まれました。",
    8: "波動8のもとに生まれました。力強く実現力があり、繁栄する。そのエネルギーは豊かさを引き寄せます。"
       "築くために生まれました。真の力は奉仕であることを学ぶために生まれました。",
    9: "波動9のもとに生まれました。人道主義的で寛大、思いやり深い。古い賢い魂。"
       "集合に仕える使命。周期を閉じ、執着の手放し方を教えるために生まれました。",
    11: "波動11のもとに生まれました。直感のマスター。知恵とインスピレーションで高次のエネルギーを引き寄せます。"
        "磁力的な存在感。精神的な光を地に足をつけて均衡させるために生まれました。",
    22: "波動22のもとに生まれました。建設のマスター。最も大きな夢を具体的な現実へと変える力があります。"
        "実践的なビジョン。人類のために築くために生まれました。",
}

# =====================================================================
# BLOCO ZH — CHINÊS
# =====================================================================
EXPRESS_TXT_ZH = {
    1: ("个性", "有原创力、有创造力、天生的领导者和独立者——开创与创造冲动的能量。",
        "自私、傲慢、冲动——倾向于集中决策，不懂得授权。",
        "培养谦逊：真正的领导力是激励，而非强加。"),
    2: ("协作", "外交家、敏感、和平使者——你的存在能安抚与调和环境。",
        "犹豫不决、缺乏安全感、依赖他人意见——不惜一切代价回避冲突。",
        "培养自信：你的敏感是一种天赋，不是弱点。"),
    3: ("创造", "有创造力、善于沟通、乐观——拥有语言和艺术表达的天赋。",
        "肤浅、分散、夸张——精力分散，难以完成项目。",
        "培养专注：质量胜于数量。"),
    4: ("工作", "务实、自律、可靠——是任何项目或团队的基石。",
        "僵化、固执、抗拒创新——可能因惧怕新事物而错失机会。",
        "培养灵活性：生活也需要即兴与自发。"),
    5: ("自由", "多才多艺、爱冒险、有魅力——渴望生活与体验。",
        "冲动、不负责任、不计后果——反复无常可能伤害所爱之人。",
        "在自由与责任之间取得平衡：真正的自由包含对他人的尊重。"),
    6: ("家庭", "有责任感、有爱心、有保护欲——是亲人的情感支柱。",
        "过度保护、爱管闲事——容易以爱的名义想要控制。",
        "爱而不控制：照顾自己也是照顾他人。"),
    7: ("智慧", "睿智、善于分析、有灵性——在无人注视之处探寻真理。",
        "冷漠、讽刺、孤僻——容易在智识上自感优越。",
        "平衡理性与情感：智慧唯有分享才有价值。"),
    8: ("力量", "强大、有成就、兴旺发达——生来就是要领导和创造财富。",
        "物质主义、专断、工作狂——可能为了成功而牺牲他人。",
        "以正直使用力量：真正的成功以所行的善来衡量。"),
    9: ("人道", "博爱、慷慨、有同情心——能看到存在的更大图景。",
        "忧郁、涣散——倾向于逃避具体的现实。",
        "宽恕并放下：超脱即是解脱。"),
    11: ("灵感大师", "直觉敏锐、 enlightened、有远见——传导更高层次的能量。",
        "焦虑、紧张、疏离——高振动的压力难以承受。",
        "平衡灵性世界与物质世界：让灵感落地。"),
    22: ("建设大师", "实干且有远见——能在大规模上把梦想变为现实。",
        "野心过度、专横——巨大潜能的重量可能压垮人。",
        "建设而不被工作奴役：伟大的工程需要一个内心平静的主人。"),
}

SIG_ZH = {
    1: ("个性",
        "象征：圆。日：星期日。行星：太阳。元素：火。颜色：黄色。器官：心脏。"
        "有原创力、有创造力、天生的领导者、独立、坚强、果断、开拓者。这是开创的能量，"
        "是创造冲动的能量。拥有此数的人是有远见的开拓者，不惧走前人未走之路。他们主动进取，"
        "不依赖他人行动。当这份能量得到正向引导，它能建立帝国、颠覆范式。其存在令人瞩目，决心不可动摇。",
        "自私、傲慢、支配欲强、冲动、固执、缺乏耐心。倾向于集中决策，不懂得授权。"
        "可能变得专断僵化，疏远本可协作的人。过度的个性可能导致孤立，损害人际关系。",
        "培养谦逊，学会团队合作。记住没有人能独自成就伟业。真正的领导力是激励，而非强加。"
        "分享主导权能放大你的成就，铸就持久的遗产。"),
    2: ("协作",
        "象征：半圆。日：星期一。行星：月亮。元素：水。颜色：绿色。"
        "外交家、敏感、乐于合作、和平使者、直觉敏锐、注重细节、善于倾听。你的存在能安抚与调和环境。"
        "你有凝聚人心、找到皆大欢喜之策的天赋。你的直觉细腻，对人的判断很少出错。"
        "你是编织持久而有意义的关系的金线。",
        "犹豫不决、缺乏安全感、顺从、过度敏感、依赖他人意见、羞怯。不惜一切代价回避冲突，"
        "即使需要表明立场。可能为了维持表面和平而在关系中委屈自己，造成内心的挫败。",
        "培养自信与情感独立。必要时学会说不。你的敏感是一种天赋，不是弱点。"
        "真正的和平来自内在的平衡，而非外界的认可。"),
    3: ("创造",
        "象征：三角。日：星期二。行星：木星。元素：风。颜色：紫罗兰。"
        "有创造力、善于沟通、乐观、有魅力、有艺术天赋。你的存在点亮任何环境。"
        "你拥有语言和艺术表达的天赋。你的能量富有感染力，自然吸引人群。"
        "你是生活之乐与无限创造力的化身。",
        "肤浅、分散、夸张、戏剧化。倾向于把精力洒向多个方向而无法完成项目。"
        "可能利用戏剧天赋操纵局势与人心。",
        "培养表达的专注与深度。把才华导向具体的方向。质量胜于数量。"),
    4: ("工作",
        "象征：四方。日：星期三。行星：天王星。元素：土。颜色：蓝色。"
        "务实、自律、可靠、忠诚、坚韧、有条理、高效、敬业、诚实。你是任何项目或团队的基石。"
        "不看到工作圆满完成绝不放弃。你最重视稳定与安全。你的可靠让身边所有人都感到安心。",
        "僵化、固执、抗拒改变、过度物质主义、排斥创新。可能陷入不必要的常规，"
        "因惧怕新事物而错失机会。",
        "培养灵活与轻盈。不必事事如此严肃。生活也需要即兴。"
        "多信任生命的流动。"),
    5: ("自由",
        "象征：星形。日：星期四。行星：水星。元素：风。颜色：橙色。"
        "自由、多才多艺、爱冒险、进步、聪明、好奇、适应力强、有魅力。"
        "你的能量富有感染力，轻易吸引新的人与事。你渴望生活与体验。"
        "你是自由与探索的化身。",
        "冲动、不负责任、焦虑、不计后果、沉溺享乐。反复无常可能伤害所爱之人。"
        "过度的自由可能沦为放纵。",
        "在自由与责任之间取得平衡。真正的自由包含对他人的尊重。"
        "在不忘本质的前提下追求一贯性。"),
    6: ("家庭",
        "象征：六边形。日：星期五。行星：金星。元素：土。颜色：粉色。"
        "有责任感、有爱心、有保护欲、公正、有同情心、有艺术气质、天生的顾问。你是亲人的情感支柱。"
        "你有敏锐的正义感，不惜一切保护所爱之人。",
        "过度保护、爱管闲事、为他人焦虑。容易以爱的名义想要控制。"
        "可能把不属于自己的责任扛在肩上。",
        "爱而不控制。尊重他人的空间。照顾自己也是照顾他人。"
        "真正的爱是自由。"),
    7: ("智慧",
        "象征：七边形。日：星期六。行星：海王星。元素：水。颜色：靛蓝。"
        "睿智、善于分析、有灵性、直觉敏锐、追求完美、内敛、哲学气质、头脑出众。"
        "在无人注视之处探寻真理。与无形世界有着深厚的连接。",
        "冷漠、讽刺、孤僻、多疑。容易在智识上自感优越。"
        "孤独可能化为苦涩。",
        "平衡理性与情感。分享所学。智慧唯有分享才有价值。"),
    8: ("力量",
        "象征：八角。日：星期日。行星：土星。元素：土。颜色：红色。"
        "强大、有成就、兴旺、善于谋略、有野心、有远见。生来就是要领导和创造财富。"
        "高效地把愿景变为现实。自然吸引成功。",
        "物质主义、专断、工作狂、缺乏耐心。可能为了成功而牺牲他人。"
        "没有伦理的权力会腐化。",
        "以正直使用力量。真正的成功以所行的善来衡量。"
        "金钱是手段，不是目的。"),
    9: ("人道",
        "象征：九边形。日：星期二。行星：火星。元素：火。颜色：绯红。"
        "博爱、慷慨、有同情心、睿智、宽容、鼓舞人心、利他。能看到存在的更大图景。"
        "你的灵魂古老，承载着许多世累积的智慧。",
        "忧郁、涣散、自怜。倾向于逃避具体的现实。"
        "躲进无法实现的理想之中。",
        "宽恕并放下。信任生命的流动。超脱即是解脱。"
        "照顾自己，才能照顾世界。"),
    11: ("灵感大师",
        "直觉敏锐、觉悟、鼓舞人心、有远见。传导更高层次的能量。"
        "触及超越理性的知识。存在充满磁性与启发性。"
        "以内在之光提升身边的所有人。",
        "焦虑、紧张、疏离、偏执。高振动的压力难以承受。"
        "可能感到不被理解、格格不入。",
        "平衡灵性世界与物质世界。让灵感落地。"
        "照顾身体，如同照顾灵魂。"),
    22: ("建设大师",
        "实干、有务实的远见。能在大规模上把梦想变为现实。"
        "结合灵性视野与具体行动。潜能无限。你是未来的建筑师，"
        "建造造福人类的作品。",
        "野心过度、压力大、专横。巨大潜能的重量可能压垮人，导致耗竭。",
        "建设而不被工作奴役。在行动与存在之间取得平衡。"
        "伟大的工程需要一个内心平静的主人。"),
    33: ("大爱大师",
        "无条件的爱、普世的同情、情感的疗愈。爱与光的大师。"
        "提升身边的所有人。",
        "情感上不堪重负、殉道者倾向。可能吸收他人的痛苦。",
        "爱而不自我牺牲。照顾身体，如同照顾灵魂。"),
}

CAM_ZH = {
    1: ("实现", "你的使命是开辟道路、领导与创新。你为成为开拓者而来，在无人之处创造机会。你有勇气、意志力和决心去成就伟大的事业。你最大的挑战是领悟：领导也意味着服务，是激励他人发光。拿破仑·波拿巴、华特·迪士尼、史蒂夫·乔布斯和贝利都走在这一实现与开拓的人生路上。"),
    2: ("和平与合作", "你的使命是合作、平衡，并作为人与人之间的桥梁来服务。你为带来和谐与外交而来。你的敏感是你最大的工具。世界需要你联结对立、促成共识的能力。戴安娜王妃、亚伯拉罕·林肯和罗伯特·卡洛斯是这条和平之路的典范。"),
    3: ("喜悦与创造", "你的使命是沟通、创造并激发喜悦。你为通过艺术与语言表达生命之美而来。你的魅力照亮身边的人。奥斯卡·王尔德、查尔斯·狄更斯、金·凯瑞和保罗·麦卡特尼都走在这一创造之路上。"),
    4: ("行动与结构", "你的使命是建设、组织并建立结构。你为以纪律建立坚实基础、化混沌为秩序而来。你的可靠是你最大的资本。比尔·盖茨、西格蒙德·弗洛伊德和玛格丽特·撒切尔共同走过这段建设之旅。"),
    5: ("进化与自由", "你的使命是体验、改变与进化。你为打破范式、激励解放而来。你的多才多艺是你的动力之源。富兰克林·罗斯福、克里斯蒂亚诺·罗纳尔多和米克·贾格尔是变革的典范。"),
    6: ("调和与责任", "你的使命是服务、关爱与调和。你为在世间创造美与爱而来。你慷慨的心指引脚步、感动身边之人。约翰·肯尼迪、猫王埃尔维斯·普雷斯利和圣女贞德是这条路的典范。"),
    7: ("智慧与完美", "你的使命是探寻真理并灵性进化。你为领悟存在的奥秘并传递智慧而来。史蒂芬·霍金、玛丽·居里、尼古拉·特斯拉和艾伦·图灵共同走过这条求知之路。"),
    8: ("正义与繁荣", "你的使命是以智慧彰显丰盛。你为成就伟大的事业而来，证明繁荣与伦理并行不悖。亨利·福特、热图利奥·瓦加斯、西尔维奥·桑托斯和胡里奥·伊格莱西亚斯是有目的的物质成就的典范。"),
    9: ("智慧与人道主义", "你的使命是以同情服务人类。你为圆满轮回、启迪他人而来。你的灵魂承载着许多世的智慧。甘地、马丁·路德·金、特蕾莎修女和约翰·列侬是为人类服务的典范。"),
    11: ("神圣灵感", "你的使命是照亮并提升集体意识。你是高等直觉的通道。温斯顿·丘吉尔、阿尔伯特·爱因斯坦、莫扎特和玛丽莲·梦露是这一灵感的典范。"),
    22: ("大规模建设", "你的使命是成就造福人类的伟大工程。你是未来的建筑师。奥普拉·温弗瑞、托马斯·爱迪生、西蒙·玻利瓦尔和弗兰克·劳埃德·赖特是大规模建设的典范。"),
    33: ("大爱大师", "你的使命是通过无条件的爱提升意识。你为疗愈人心而来。"),
}

DES_ZH = {
    0: "天然的平衡。你在这个领域拥有平衡，只需顺应生活流动。",
    1: "克服自我，培养服务型的领导力。真正的力量在于赋能他人。",
    2: "战胜羞怯与情感依赖。培养自信，以表达自己的需要。",
    3: "避免分散，培养专注。把创造性能量集中于具体的项目。",
    4: "克服僵化，拥抱改变。灵活与适应是成长的关键。",
    5: "控制过度，培养自律。有责任的自由带来成熟。",
    6: "避免过度保护。相信你所爱的人能够做出自己的选择。",
    7: "克服孤立，与世界分享你的知识。智慧唯有分享才存在。",
    8: "平衡野心与伦理及慷慨。造福他人的成功才是真正的成功。",
    9: "克服过度的超脱。学会无愧疚地圆满轮回，信任生命的流动。",
}

VIB_ZH = {
    1: "生于振动1。天生的领导者、开拓者、独立者。开创与启动的能量。有勇气走无人走过的路。为学会以谦逊与服务来领导而来。",
    2: "生于振动2。敏感、外交家、乐于合作。你的力量在伙伴关系与和谐之中。直觉敏锐。为学习给予与接受之间的平衡而来。",
    3: "生于振动3。善于沟通、有创造力、乐观。感染力十足的喜悦。语言是你最有力的工具。为以艺术点亮世界而来。",
    4: "生于振动4。勤勉、自律、务实。坚实筑就安全的根基。为领悟真正的安全感来自内在而来。",
    5: "生于振动5。自由、多才多艺、爱冒险。你的能量追寻体验与蜕变。好奇心驱动你的灵魂。为体验生命的圆满而来。",
    6: "生于振动6。有爱心、有责任感、重视家庭。使命是关爱与调和。爱是你最大的力量。为领悟爱即解放而来。",
    7: "生于振动7。睿智、内省、有灵性。追寻深层的知识。寂静是你的老师。为领悟存在的奥秘而来。",
    8: "生于振动8。强大、有成就、兴旺。能量吸引丰盛。为建设而生。为领悟真正的力量是服务而来。",
    9: "生于振动9。博爱、慷慨、有同情心。古老而智慧的灵魂。使命是服务集体。为圆满轮回、教导超脱而来。",
    11: "生于振动11。直觉大师。以智慧与灵感传导更高层次的能量。存在充满磁性。为平衡灵性之光与脚踏实地而来。",
    22: "生于振动22。建设大师。能把最大的梦想化为具体的现实。视野务实。为人类而建设。",
}

# =====================================================================
# BLOCO RU — RUSSO
# =====================================================================
EXPRESS_TXT_RU = {
    1: ("Индивидуальность", "Оригинальный, творческий, прирожденный лидер и независимый — энергия первопроходца и созидания.",
        "Эгоизм, высокомерие, импульсивность — склонность концентрировать решения и не делегировать.",
        "Развивайте скромность: настоящее лидерство — вдохновлять, а не навязывать."),
    2: ("Сотрудничество", "Дипломатичный, чувствительный, миротворец — ваше присутствие успокаивает и гармонизирует.",
        "Нерешительность, неуверенность, зависимость от чужого мнения — избегание конфликта любой ценой.",
        "Развивайте уверенность: ваша чувствительность — дар, а не слабость."),
    3: ("Творчество", "Творческий, общительный, оптимист — дар слова и художественного выражения.",
        "Поверхностность, распыленность, преувеличение — рассеянная энергия мешает завершать проекты.",
        "Развивайте сосредоточенность: качество важнее количества."),
    4: ("Труд", "Практичный, дисциплинированный, надежный — фундамент любого проекта или команды.",
        "Ригидность, упрямство, сопротивление новому — страх перед новым может закрывать возможности.",
        "Развивайте гибкость: жизнь требует и импровизации."),
    5: ("Свобода", "Разносторонний, приключенческий, обаятельный — жажда жизни и переживаний.",
        "Импульсивность, безответственность, неосмотрительность — переменчивость может ранить близких.",
        "Балансируйте свободу и ответственность: настоящая свобода уважает других."),
    6: ("Семья", "Ответственный, любящий, защитник — эмоциональная опора близких.",
        "Гиперопека, вмешательство — легко захотеть контролировать под видом любви.",
        "Любите без контроля: забота о себе — это забота о других."),
    7: ("Мудрость", "Мудрый, аналитичный, духовный — ищет истину там, где никто не смотрит.",
        "Холодность, сарказм, замкнутость — склонность к интеллектуальному превосходству.",
        "Балансируйте разум и чувство: мудрость ценна лишь вsharing."),
    8: ("Сила", "Мощный, достигающий, процветающий — рожден, чтобы вести и создавать богатство.",
        "Материализм, авторитарность, трудоголизм — может жертвовать другими ради успеха.",
        "Используйте силу честно: настоящий успех измеряется добром."),
    9: ("Гуманизм", "Филантроп, щедрый, сострадательный — видит большую картину бытия.",
        "Меланхолия, рассеянность — склонность избегать конкретной реальности.",
        "Прощайте и отпускайте: отрешенность — освобождение."),
    11: ("Мастер вдохновения", "Интуитивный, просветленный, визионер — проводит энергию более высоких сфер.",
        "Тревога, напряжение, отчуждение — давление высокой вибрации тяжело нести.",
        "Балансируйте духовное и материальное: заземляйте вдохновение."),
    22: ("Мастер-строитель", "Практик с видением — воплощает мечты в масштабе.",
        "Сверхамбициозность, деспотичность — вес огромного потенциала может раздавить.",
        "Стройте, не будучи рабом труда: великому делу нужен спокойный хозяин."),
}

SIG_RU = {
    1: ("Индивидуальность",
        "Символ: круг. День: воскресенье. Планета: Солнце. Стихия: огонь. Цвет: желтый. Орган: сердце. "
        "Оригинальный, творческий, прирожденный лидер, независимый, сильный, решительный, первопроходец. Это энергия начинания, "
        "энергия импульса к созиданию. Обладатель этого числа — дальновидный первопроходец, не боящийся идти непроторенными путями. "
        "Он инициативен и не зависит от действий других. Направленная позитивно, эта энергия строит империи и меняет парадигмы. "
        "Его присутствие заметно, решимость непоколебима.",
        "Эгоизм, высокомерие, властность, импульсивность, упрямство, нетерпеливость. Склонность концентрировать решения "
        "и не делегировать. Может стать авторитарным и ригидным, отдаляя тех, с кем мог бы сотрудничать. "
        "Избыток индивидуальности ведет к изоляции и вредит отношениям.",
        "Развивайте скромность и учитесь работать в команде. Помните: никто не строит величие в одиночку. "
        "Настоящее лидерство — вдохновлять, а не навязывать. Разделение лидерства умножает достижения и оставляет прочное наследие."),
    2: ("Сотрудничество",
        "Символ: полукруг. День: понедельник. Планета: Луна. Стихия: вода. Цвет: зеленый. "
        "Дипломатичный, чувствительный, склонный к сотрудничеству, миротворец, интуитивный, внимательный к деталям, умеющий слушать. "
        "Ваше присутствие успокаивает и гармонизирует. У вас есть дар объединять людей и находить решения, устраивающие всех. "
        "Ваша интуиция тонка, и в оценке людей вы редко ошибаетесь. Вы — золотая нить, плетущая прочные и значимые отношения.",
        "Нерешительность, неуверенность, покорность, гиперчувствительность, зависимость от чужого мнения, застенчивость. "
        "Избегаете конфликта любой ценой, даже когда нужно обозначить позицию. Может жертвовать собой в отношениях ради видимого мира, "
        "создавая внутреннюю фрустрацию.",
        "Развивайте уверенность и эмоциональную независимость. Учитесь говорить «нет», когда это необходимо. "
        "Ваша чувствительность — дар, а не слабость. Настоящий мир рождается из внутреннего равновесия, а не из внешнего одобрения."),
    3: ("Творчество",
        "Символ: треугольник. День: вторник. Планета: Юпитер. Стихия: воздух. Цвет: фиолетовый. "
        "Творческий, общительный, оптимистичный, обаятельный, с художественной одаренностью. Ваше присутствие освещает любое пространство. "
        "У вас есть дар слова и художественного выражения. Ваша энергия заразительна и естественно притягивает людей. "
        "Вы — воплощение радости жизни и безграничного творчества.",
        "Поверхностность, распыленность, преувеличение, драматизация. Склонность рассеивать энергию во множестве направлений, "
        "не завершая проектов. Может использовать дар драмы для манипуляции ситуациями и людьми.",
        "Развивайте сосредоточенность и глубину выражения. Направьте талант в конкретное русло. Качество важнее количества."),
    4: ("Труд",
        "Символ: квадрат. День: среда. Планета: Уран. Стихия: земля. Цвет: синий. "
        "Практичный, дисциплинированный, надежный, верный, стойкий, организованный, эффективный, преданный, честный. "
        "Вы — фундамент любого проекта или команды. Не отступаете, пока работа не выполнена как следует. "
        "Стабильность и безопасность для вас превыше всего. Ваша надежность дает спокойствие всем вокруг.",
        "Ригидность, упрямство, сопротивление переменам, избыточный материализм, неприятие инноваций. "
        "Может застревать в ненужной рутине и упускать возможности из страха перед новым.",
        "Развивайте гибкость и легкость. Не все должно быть так серьезно. Жизнь требует импровизации. "
        "Больше доверяйте потоку жизни."),
    5: ("Свобода",
        "Символ: звезда. День: четверг. Планета: Меркурий. Стихия: воздух. Цвет: оранжевый. "
        "Свободолюбивый, разносторонний, любящий приключения, прогрессивный, умный, любопытный, адаптивный, обаятельный. "
        "Ваша энергия заразительна и легко притягивает новое — людей и события. Вы жаждете жить и переживать. "
        "Вы — воплощение свободы и исследования.",
        "Импульсивность, безответственность, тревожность, неосмотрительность, погоня за удовольствиями. "
        "Переменчивость может ранить близких. Избыток свободы может стать распущенностью.",
        "Балансируйте свободу и ответственность. Настоящая свобода уважает других. "
        "Ищите последовательность, не теряя сути."),
    6: ("Семья",
        "Символ: шестиугольник. День: пятница. Планета: Венера. Стихия: земля. Цвет: розовый. "
        "Ответственный, любящий, защитник, справедливый, сострадательный, артистичный, прирожденный советчик. "
        "Вы — эмоциональная опора близких. У вас острое чувство справедливости, и вы защищаете любимых любой ценой.",
        "Гиперопека, вмешательство, тревога за других. Легко захотеть контролировать под видом любви. "
        "Может брать на себя ответственность, которая вам не принадлежит.",
        "Любите без контроля. Уважайте чужое пространство. Забота о себе — это забота о других. "
        "Настоящая любовь — это свобода."),
    7: ("Мудрость",
        "Символ: семиугольник. День: суббота. Планета: Нептун. Стихия: вода. Цвет: индиго. "
        "Мудрый, аналитичный, духовный, интуитивный, перфекционист, замкнутый, философский, выдающийся ум. "
        "Ищет истину там, где никто не смотрит. Глубокая связь с невидимым миром.",
        "Холодность, сарказм, отчужденность, недоверчивость. Склонность к интеллектуальному превосходству. "
        "Одиночество может стать горечью.",
        "Балансируйте разум и чувство. Делитесь тем, чему научились. Мудрость существует лишь в sharing."),
    8: ("Сила",
        "Символ: восьмиугольник. День: воскресенье. Планета: Сатурн. Стихия: земля. Цвет: красный. "
        "Мощный, достигающий, процветающий, стратегичный, амбициозный, дальновидный. Рожден, чтобы вести и создавать богатство. "
        "Эффективно воплощает видение в реальность. Естественно притягивает успех.",
        "Материализм, авторитарность, трудоголизм, нетерпеливость. Может жертвовать другими ради успеха. "
        "Власть без этики разлагает.",
        "Используйте силу честно. Настоящий успех измеряется добром, которое вы делаете. "
        "Деньги — средство, а не цель."),
    9: ("Гуманизм",
        "Символ: девятиугольник. День: вторник. Планета: Марс. Стихия: огонь. Цвет: алый. "
        "Филантроп, щедрый, сострадательный, мудрый, терпимый, вдохновляющий, альтруист. Видит большую картину бытия. "
        "Ваша душа древняя и несет мудрость многих воплощений.",
        "Меланхолия, рассеянность, жалость к себе. Склонность избегать конкретной реальности. "
        "Укрывается в несбыточных идеалах.",
        "Прощайте и отпускайте. Доверьтесь потоку жизни. Отрешенность — освобождение. "
        "Заботьтесь о себе, чтобы заботиться о мире."),
    11: ("Мастер вдохновения",
        "Интуитивный, просветленный, вдохновляющий, визионер. Проводит энергию более высоких сфер. "
        "Касается знания, превосходящего разум. Его присутствие магнитно и вдохновляет. "
        "Внутренним светом возвышает всех вокруг.",
        "Тревога, напряжение, отчуждение, паранойя. Давление высокой вибрации тяжело нести. "
        "Может чувствовать себя непонятым, чужим.",
        "Балансируйте духовное и материальное. Заземляйте вдохновение. "
        "Заботьтесь о теле так же, как о душе."),
    22: ("Мастер-строитель",
        "Практик с практическим видением. Воплощает мечты в масштабе. "
        "Соединяет духовное зрение с конкретным действием. Потенциал безграничен. Вы — архитектор будущего, "
        "строящий дела на благо человечества.",
        "Сверхамбициозность, стресс, деспотичность. Вес огромного потенциала может раздавить и привести к истощению.",
        "Стройте, не будучи рабом труда. Балансируйте действие и бытие. "
        "Великому делу нужен спокойный хозяин."),
    33: ("Мастер вселюбви",
        "Безусловная любовь, всеобщее сострадание, эмоциональное исцеление. Мастер любви и света. "
        "Возвышает всех вокруг.",
        "Эмоциональная перегрузка, склонность к самопожертвованию. Может впитывать чужую боль.",
        "Любите, не жертвуя собой. Заботьтесь о теле так же, как о душе."),
}

CAM_RU = {
    1: ("Реализация", "Ваша миссия — прокладывать пути, вести и innovate. Вы пришли как первопроходец, создавая возможности там, где их нет. У вас есть смелость, воля и решимость для великих дел. Ваш главный вызов — понять: лидерство означает и служение, и вдохновение других сиять. Наполеон Бонапарт, Уолт Дисней, Стив Джобс и Пеле прошли этим путем реализации и первопроходчества."),
    2: ("Мир и сотрудничество", "Ваша миссия — сотрудничать, уравновешивать и служить мостом между людьми. Вы пришли нести гармонию и дипломатию. Ваша чувствительность — ваш главный инструмент. Мир нуждается в вашей способности соединять противоположности и строить консенсус. Принцесса Диана, Авраам Линкольн и Роберто Карлос — образцы этого мирного пути."),
    3: ("Радость и творчество", "Ваша миссия — общаться, творить и вдохновлять радость. Вы пришли выражать красоту жизни через искусство и слово. Ваше обаяние освещает окружающих. Оскар Уайльд, Чарльз Диккенс, Джим Керри и Пол Маккартни прошли этим творческим путем."),
    4: ("Действие и структура", "Ваша миссия — строить, организовывать и создавать структуры. Вы пришли установить прочный фундамент дисциплиной, превращая хаос в порядок. Ваша надежность — ваш главный капитал. Билл Гейтс, Зигмунд Фрейд и Маргарет Тэтчер прошли этим строительным путем."),
    5: ("Эволюция и свобода", "Ваша миссия — переживать, изменять и эволюционировать. Вы пришли разрушать парадигмы и вдохновлять освобождение. Ваша разносторонность — источник вашей силы. Франклин Рузвельт, Криштиану Роналду и Мик Джаггер — образцы трансформации."),
    6: ("Гармония и ответственность", "Ваша миссия — служить, заботиться и гармонизировать. Вы пришли создавать красоту и любовь в мире. Ваше щедрое сердце ведет ваши шаги и трогает окружающих. Джон Кеннеди, Элвис Пресли и Жанна д'Арк — образцы этого пути."),
    7: ("Мудрость и совершенство", "Ваша миссия — искать истину и духовно эволюционировать. Вы пришли понять тайны бытия и передать мудрость. Стивен Хокинг, Мария Кюри, Никола Тесла и Алан Тьюринг прошли этим путем поиска."),
    8: ("Справедливость и процветание", "Ваша миссия — проявлять изобилие с мудростью. Вы пришли совершать великие дела, доказывая, что процветание и этика идут рука об руку. Генри Форд, Жетулиу Варгас, Силвиу Сантос и Хулио Иглесиас — образцы материального достижения с целью."),
    9: ("Мудрость и гуманизм", "Ваша миссия — служить человечеству с состраданием. Вы пришли завершить цикл воплощений и просвещать других. Ваша душа несет мудрость многих жизней. Ганди, Мартин Лютер Кинг, Мать Тереза и Джон Леннон — образцы служения человечеству."),
    11: ("Божественное вдохновение", "Ваша миссия — озарять и возвышать коллективное сознание. Вы — канал высшей интуиции. Уинстон Черчилль, Альберт Эйнштейн, Моцарт и Мэрилин Монро — образцы этого вдохновения."),
    22: ("Строительство в масштабе", "Ваша миссия — осуществлять великие дела на благо человечества. Вы — архитектор будущего. Опра Уинфри, Томас Эдисон, Симон Боливар и Фрэнк Ллойд Райт — образцы масштабного строительства."),
    33: ("Мастер вселюбви", "Ваша миссия — возвышать сознание через безусловную любовь. Вы пришли исцелять сердца."),
}

DES_RU = {
    0: "Природное равновесие. В этой сфере у вас есть баланс — просто позвольте жизни течь.",
    1: "Преодолейте эго, развивайте лидерство через служение. Настоящая сила — возвышать других.",
    2: "Победите застенчивость и эмоциональную зависимость. Развивайте уверенность, чтобы выразить свои потребности.",
    3: "Избегайте распыления, развивайте сосредоточенность. Направьте творческую энергию в конкретные проекты.",
    4: "Преодолейте ригидность, примите перемены. Гибкость и адаптивность — ключи к росту.",
    5: "Контролируйте излишества, развивайте дисциплину. Свобода с ответственностью приносит зрелость.",
    6: "Избегайте гиперопеки. Доверьте близким право делать собственный выбор.",
    7: "Преодолейте изоляцию, поделитесь знанием с миром. Мудрость существует лишь в sharing.",
    8: "Балансируйте амбиции с этикой и щедростью. Успех во благо других — настоящий успех.",
    9: "Преодолейте избыточную отрешенность. Учитесь завершать циклы без чувства вины, доверяя потоку жизни.",
}

VIB_RU = {
    1: "Рожден в вибрации 1. Прирожденный лидер, первопроходец, независимый. Энергия начинания и инициирования. Смелость идти непроторенными путями. Пришел научиться лидировать со скромностью и служением.",
    2: "Рожден в вибрации 2. Чувствительный, дипломатичный, склонный к сотрудничеству. Ваша сила — в партнерстве и гармонии. Тонкая интуиция. Пришел научиться равновесию между давать и получать.",
    3: "Рожден в вибрации 3. Общительный, творческий, оптимист. Заразительная радость. Слово — ваш сильнейший инструмент. Пришел освещать мир через искусство.",
    4: "Рожден в вибрации 4. Трудолюбивый, дисциплинированный, практичный. Прочные основания создают настоящую безопасность. Пришел понять, что настоящая безопасность приходит изнутри.",
    5: "Рожден в вибрации 5. Свободолюбивый, разносторонний, любящий приключения. Ваша энергия ищет переживания и трансформации. Любопытство движет вашей душой. Пришел пережить полноту жизни.",
    6: "Рожден в вибрации 6. Любящий, ответственный, семейный. Миссия — забота и гармония. Любовь — ваша величайшая сила. Пришел понять, что любовь освобождает.",
    7: "Рожден в вибрации 7. Мудрый, интровертный, духовный. Ищет глубокое знание. Тишина — ваш учитель. Пришел понять тайны бытия.",
    8: "Рожден в вибрации 8. Мощный, достигающий, процветающий. Энергия притягивает изобилие. Рожден строить. Пришел понять, что настоящая сила — служение.",
    9: "Рожден в вибрации 9. Филантроп, щедрый, сострадательный. Древняя и мудрая душа. Миссия — служить коллективу. Пришел завершить цикл воплощений и научить отрешенности.",
    11: "Рожден в вибрации 11. Мастер интуиции. Проводит энергию более высоких сфер с мудростью и вдохновением. Магнитное присутствие. Пришел уравновесить свет духа и заземление.",
    22: "Рожден в вибрации 22. Мастер-строитель. Воплощает величайшие мечты в конкретную реальность. Практическое видение. Строит для человечества.",
}

# =====================================================================
# BLOCO AR — ÁRABE
# =====================================================================
EXPRESS_TXT_AR = {
    1: ("الفردية", "أصيل ومبدع وقائد فطري ومستقل — طاقة البدء والإبداع.",
        "الأنانية والكبرياء والاندفاع — الميل إلى تمركز القرارات وعدم التفويض.",
        "طوّر التواضع: القيادة الحقيقية هي الإلهام لا الإملاء."),
    2: ("التعاون", "دبلوماسي وحساس وصانع سلام — حضورك يهدّئ ويوازن المحيط.",
        "التردد وعدم الأمان والاعتماد على رأي الآخرين — تجنّب الصراع مهما كلف الأمر.",
        "طوّر الثقة: حساسيتك موهبة وليست ضعفًا."),
    3: ("الإبداع", "مبدع ومتواصل ومتفائل — موهبة الكلمة والتعبير الفني.",
        "سطحية وتشتت ومبالغة — الطاقة المشتبكة تعيق إتمام المشاريع.",
        "طوّر التركيز: الجودة أهم من الكم."),
    4: ("العمل", "عملي ومنضبط وموثوق — أساس أي مشروع أو فريق.",
        "التصلب والعناد ومقاومة الجديد — الخوف من الجديد قد يغلق الفرص.",
        "طوّر المرونة: الحياة تحتاج أيضًا الارتجال."),
    5: ("الحرية", "متنوع المواهب ومحب للمغامرة وساحر — عطش للحياة والتجربة.",
        "الاندفاع وعدم المسؤولية وعدم الحساب — التقلّب قد يؤذي الأحبة.",
        "وازن بين الحرية والمسؤولية: الحرية الحقيقية تحترم الآخرين."),
    6: ("العائلة", "مسؤول ومحب وحامٍ — الدعم العاطفي للأحبة.",
        "الحماية المفرطة والفضول — سهولة الرغبة في السيطرة باسم الحب.",
        "أحب دون سيطرة: رعاية نفسك هي رعاية الآخرين."),
    7: ("الحكمة", "حكيم وتحليلي وروحي — يبحث عن الحقيقة حيث لا ينظر أحد.",
        "البرود والسخرية والانعزال — الميل إلى التفوق الفكري.",
        "وازن العقل والعاطفة: الحكمة لا قيمة لها إلا في المشاركة."),
    8: ("القوة", "قوي ومنجز ومزدهر — وُلد ليقود ويصنع الثروة.",
        "المادية والاستبداد وعبد العمل — قد يضحّي بالآخرين من أجل النجاح.",
        "استخدم القوة بنزاهة: النجاح الحقيقي يُقاس بالخير."),
    9: ("الإنسانية", "إنساني وكريم ومتعاطف — يرى الصورة الكبرى للوجود.",
        "الكآبة والتشتت — الميل إلى الهروب من الواقع الملموس.",
        "اسامح ودع الرحيل: التخلي هو التحرر."),
    11: ("سيّد الإلهام", "بديهي ومستنير وصاحب رؤية — ينقل طاقة المستويات الأعلى.",
        "القلق والتوتر والعزلة — ضغط الاهتزاز العالي ثقيل.",
        "وازن الروحي والمادي: ثبّت الإلهام في الأرض."),
    22: ("سيّد البناء", "عملي صاحب رؤية — يجسّد الأحلام على نطاق واسع.",
        "الطموح المفرط والاستبداد — ثقل الإمكانات الهائلة قد يَنسِم صاحبه.",
        "ابنِ دون أن تكون عبدًا للعمل: للعمل العظيم صاحب هادئ."),
}

SIG_AR = {
    1: ("الفردية",
        "الرمز: الدائرة. اليوم: الأحد. الكوكب: الشمس. العنصر: النار. اللون: الأصفر. العضو: القلب. "
        "أصيل ومبدع وقائد فطري ومستقل وقوي وحاسم ورائد. هذه طاقة البدء، طاقة الاندفاع نحو الإبداع. "
        "صاحب هذا الرقم رائد صاحب رؤية لا يخشى سلوك الطرق التي لم تُسلك. فهو مبادر لا يعتمد على أفعال الآخرين. "
        "وتوجيهها بشكل إيجابي يبني الإمبراطوريات ويغيّر النماذج. حضوره ملحوظ وعزيمته لا تتزعزع.",
        "الأنانية والكبرياء والهيمنة والاندفاع والعناد ونفاد الصبر. الميل إلى تمركز القرارات وعدم التفويض. "
        "قد يصبح مستبدًا جامدًا فيبتعد عن من كان يمكن التعاون معهم. الإفراط في الفردية يقود إلى العزلة ويضر بالعلاقات.",
        "طوّر التواضع وتعلّم العمل في فريق. تذكّر: لا أحد يبني العظمة وحدًا. القيادة الحقيقية هي الإلهام لا الإملاء. "
        "تقاسم القيادة يضاعف إنجازاتك ويصنع إرثًا دائمًا."),
    2: ("التعاون",
        "الرمز: نصف الدائرة. اليوم: الاثنين. الكوكب: القمر. العنصر: الماء. اللون: الأخضر. "
        "دبلوماسي وحساس وودود وصانع سلام وبديهي ودقيق ويجيد الإصغاء. حضورك يهدّئ ويوازن المحيط. "
        "لديك موهبة جمع الناس وإيجاد حلول ترضي الجميع. حدسك رقيق ونادرًا ما تخطئ في تقدير الناس. "
        "أنت الخيط الذهبي الذي ينسج علاقات متينة وهادفة.",
        "التردد وعدم الأمان والاستسلام والحساسية المفرطة والاعتماد على رأي الآخرين والخجل. تجنّب الصراع مهما كلف الأمر، "
        "حتى عند الحاجة إلى إعلان الموقف. قد يضحي بنفسه في العلاقات من أجل سلام ظاهر، مانعًا الإحباط الداخلي.",
        "طوّر الثقة والاستقلال العاطفي. تعلّم قول «لا» عند الضرورة. حساسيتك موهبة وليست ضعفًا. "
        "السلام الحقيقي يولد من التوازن الداخلي، لا من الاعتراف الخارجي."),
    3: ("الإبداع",
        "الرمز: المثلث. اليوم: الثلاثاء. الكوكب: المشتري. العنصر: الهواء. اللون: البنفسجي. "
        "مبدع ومتواصل ومتفائل وساحر وموهوب فنيًا. حضورك ينير أي مكان. "
        "لديك موهبة الكلمة والتعبير الفني. طاقتك مُعدية وتجذب الناس طبيعيًا. "
        "أنت تجسيد بهجة الحياة والإبداع اللامحدود.",
        "السطحية والتشتت والمبالغة والميل dramatization. الميل إلى نثر الطاقة في اتجاهات متعددة دون إتمام المشاريع. "
        "قد يستخدم موهبة الدراما للتلاعب بالمواقف والأشخاص.",
        "طوّر التركيز والعمق في التعبير. وجّه الموهبة نحو مسار محدد. الجودة أهم من الكم."),
    4: ("العمل",
        "الرمز: المربع. اليوم: الأربعاء. الكوكب: أورانوس. العنصر: الأرض. اللون: الأزرق. "
        "عملي ومنضبط وموثوق ووفاء وصبور ومنظم وفعال ومتفانٍ وصادق. أنت أساس أي مشروع أو فريق. "
        "لا تنسحب حتى تُنجز العمل كما يجب. الاستقرار والأمان أولوياتك القصوى. موثوقيتك تمنح راحة الجميع.",
        "التصلب والعناد ومقاومة التغيير والمادية المفرطة ورفض الابتكار. قد ينغلق في روتين غير ضروري "
        "ويفتقد الفرص خوفًا من الجديد.",
        "طوّر المرونة والخفة. ليس كل شيء يستحق هذا الجد. الحياة تحتاج أيضًا الارتجال. "
        "ثق أكثر في تدفق الحياة."),
    5: ("الحرية",
        "الرمز: النجمة. اليوم: الخميس. الكوكب: عطارد. العنصر: الهواء. اللون: البرتقالي. "
        "محب للحرية ومتنوع المواهب ومحب للمغامرة وتقدمي وذكي وفضولي ومتكيف وساحر. "
        "طاقتك مُعدية وتجذب الجديد بسهولة، أشخاصًا وأحداثًا. أنت عطشى للحياة والتجربة. "
        "أنت تجسيد الحرية والاستكشاف.",
        "الاندفاع وعدم المسؤولية والقلق وعدم الحساب والانغماس في المتع. التقلّب قد يؤذي الأحبة. "
        "الإفراط في الحرية قد يصبح فجورًا.",
        "وازن بين الحرية والمسؤولية. الحرية الحقيقية تحترم الآخرين. "
        "ابحث عن الاتساق دون أن تفقد جوهرك."),
    6: ("العائلة",
        "الرمز: السدس. اليوم: الجمعة. الكوكب: الزهرة. العنصر: الأرض. اللون: الوردي. "
        "مسؤول ومحب وحامٍ وعادل ومتعاطف وفني ومستشار فطري. أنت الدعم العاطفي للأحبة. "
        "لديك حس عالٍ بالعدالة وتحمي الأحبة مهما كلف الأمر.",
        "الحماية المفرطة والفضول والقلق على الآخرين. سهولة الرغبة في السيطرة باسم الحب. "
        "قد يحمل مسؤولية لا تعود إليه.",
        "أحب دون سيطرة. احترم مساحة الآخرين. رعاية نفسك هي رعاية الآخرين. "
        "الحب الحقيقي هو الحرية."),
    7: ("الحكمة",
        "الرمز: السبعي. اليوم: السبت. الكوكب: نبتون. العنصر: الماء. اللون: النيلي. "
        "حكيم وتحليلي وروحي وبديهي و perfectionist منعزل وفلسفي وعقل استثنائي. "
        "يبحث عن الحقيقة حيث لا ينظر أحد. صلة عميقة بالعالم غير المرئي.",
        "البرود والسخرية والانعزال وعدم الثقة. الميل إلى التفوق الفكري. "
        "الوحدة قد تتحول إلى مرارة.",
        "وازن العقل والعاطفة. شارك ما تعلمته. الحكمة لا توجد إلا في المشاركة."),
    8: ("القوة",
        "الرمز: الثماني. اليوم: الأحد. الكوكب: زحل. العنصر: الأرض. اللون: الأحمر. "
        "قوي ومنجز ومزدهر واستراتيجي وطموح صاحب رؤية. وُلد ليقود ويصنع الثروة. "
        "يجسّد الرؤية في الواقع بكفاءة. يجذب النجاح طبيعيًا.",
        "المادية والاستبداد وعبد العمل ونفاد الصبر. قد يضحّي بالآخرين من أجل النجاح. "
        "السلطة دون أخلاقية فاسدة.",
        "استخدم القوة بنزاهة. النجاح الحقيقي يُقاس بالخير الذي تصنعه. "
        "المال وسيلة لا هدف."),
    9: ("الإنسانية",
        "الرمز: التساعي. اليوم: الثلاثاء. الكوكب: المريخ. العنصر: النار. اللون: القرمزي. "
        "إنساني وكريم ومتعاطف وحكيم ومتسامح ومُلهِم ونزيل. يرى الصورة الكبرى للوجود. "
        "روحك قديمة تحمل حكمة تجسيدات عديدة.",
        "الكآبة والتشتت والشفقة على الذات. الميل إلى الهروب من الواقع الملموس. "
        "يحتمي في مثاليات لا تتحقق.",
        "اسامح ودع الرحيل. ثق بتدفق الحياة. التخلي هو التحرر. "
        "اعتنِ بنفسك لتعتني بالعالم."),
    11: ("سيّد الإلهام",
        "بديهي ومستنير ومُلهِم صاحب رؤية. ينقل طاقة المستويات الأعلى. "
        "يلمس معرفةً تفوق العقل. حضوره مغناطيسي ومُلهم. "
        "يرفع من حوله بنوره الداخلي.",
        "القلق والتوتر والعزلة والبارانويا. ضغط الاهتزاز العالي ثقيل. "
        "قد يشعر بأنه غير مفهوم وغريب.",
        "وازن الروحي والمادي. ثبّت الإلهام في الأرض. "
        "اعتنِ بالجسد كما تعتني بالروح."),
    22: ("سيّد البناء",
        "عملي صاحب رؤية عملية. يجسّد الأحلام على نطاق واسع. "
        "يجمع الرؤية الروحية مع الفعل الملموس. الإمكانات لا حدود لها. أنت مهندس المستقبل، "
        "تبني أعمالًا في مصلحة الإنسانية.",
        "الطموح المفرط والضغط والاستبداد. ثقل الإمكانات الهائلة قد يَنسِم صاحبه ويؤدي إلى الإرهاق.",
        "ابنِ دون أن تكون عبدًا للعمل. وازن بين الفعل والوجود. "
        "للعمل العظيم صاحب هادئ."),
    33: ("سيّد الحب الكوني",
        "الحب غير المشروط والتعاطف الكوني والشفاء العاطفي. سيّد الحب والنور. "
        "يرفع من حوله جميعًا.",
        "الحمل العاطفي المفرط والميل إلى الاستشهاد الذاتي. قد يمتص ألم الآخرين.",
        "أحب دون تضحية بالنفس. اعتنِ بالجسد كما تعتني بالروح."),
}

CAM_AR = {
    1: ("الإنجاز", "رسالتك هي فتح الطرق والقيادة والابتكار. جئت لتكون رائدًا يخلق الفرص حيث لا توجد. لديك الشجاعة والإرادة والعزيمة لأعمال عظيمة. تحديك الأكبر أن تدرك: القيادة تعني أيضًا الخدمة، وإلهام الآخرين ليتألقوا. نابليون بونابرت ووالت ديزني وستيف جوبز وبيليه ساروا هذا الطريق."),
    2: ("السلام والتعاون", "رسالتك هي التعاون والتوازن والخدمة كجسر بين الناس. جئت لتحمل الانسجام والدبلوماسية. حساسيتك هي أداتك الأعظم. العالم يحتاج قدرتك على توحيد المتضادات وبناء الإجماع. الأميرة ديانا وأبراهام لينكولن وروبرتو كارلوس قدوة هذا الطريق."),
    3: ("الفرح والإبداع", "رسالتك هي التواصل والإبداع وإلهام الفرح. جئت لتعبّر عن جمال الحياة بالفن والكلمة. سحرك يضيء من حولك. أوسكار وايلد وتشارلز ديكنز وجيم كيري وبول مكارتني ساروا هذا الطريق الإبداعي."),
    4: ("الفعل والبنية", "رسالتك هي البناء والتنظيم وإنشاء الهياكل. جئت لتضع أساسًا متينًا بالانضباط، محوّلًا الفوضى إلى نظام. موثوقيتك هي رأس مالك الأعظم. بيل غيتس وسيغموند فرويد ومارغريت تاتشر ساروا هذا الطريق البنائي."),
    5: ("التطور والحرية", "رسالتك هي التجربة والتغيير والتطور. جئت لكسر النماذج وإلهام التحرر. تنوع مواهبك هو مصدر قوتك. فرانكلين روزفلت وكريستيانو رونالدو وميك جاغر قدوة التحوّل."),
    6: ("الانسجام والمسؤولية", "رسالتك هي الخدمة والرعاية والانسجام. جئت لتخلق الجمال والحب في العالم. قلبك الكريم يقود خطاك ويمسّ من حولك. جون كينيدي وإلفيس بريسلي وجان دارك قدوة هذا الطريق."),
    7: ("الحكمة والكمال", "رسالتك هي البحث عن الحقيقة والتطور الروحي. جئت لتفهم أسرار الوجود وتنقل الحكمة. ستيفن هوكينغ وماري كوري ونيكولا تيسلا وألان تورينغ ساروا طريق البحث هذا."),
    8: ("العدالة والازدهار", "رسالتك هي تجسيد الوفرة بالحكمة. جئت لتحقق أعمالًا عظيمة، مُثبتًا أن الازدهار والأخلاق يسيران معًا. هنري فورد وجيتوليو فارغاس وسيلفيو سانتوس وخوليو إغليسياس قدوة الإنجاز المادي الهادف."),
    9: ("الحكمة والإنسانية", "رسالتك هي خدمة الإنسانية بالتعاطف. جئت لتُكمل دورة التجسدات وتُنير الآخرين. روحك تحمل حكمة حياة عديدة. غاندي ومارتن لوثر كينغ والأم تيريزا وجون لينون قدوة خدمة الإنسانية."),
    11: ("الإلهام الإلهي", "رسالتك هي الإشراق ورفع الوعي الجمعي. أنت قناة الحدس الأعلى. ونستون تشرشل وألبرت أينشتاين وموتسارت ومارلين مونرو قدوة هذا الإلهام."),
    22: ("البناء على نطاق واسع", "رسالتك هي تحقيق أعمال عظيمة في مصلحة الإنسانية. أنت مهندس المستقبل. أوبرا وينفري وتوماس إديسون وسيمون بوليفار وفرانك لويد رايت قدوة البناء الواسع."),
    33: ("سيّد الحب الكوني", "رسالتك هي رفع الوعي بالحب غير المشروط. جئت لتشفي القلوب."),
}

DES_AR = {
    0: "توازن طبيعي. في هذا المجال لديك توازن، فقط دع الحياة تجري.",
    1: "تغلّب على الأنا وطوّر القيادة بالخدمة. القوة الحقيقية في تمكين الآخرين.",
    2: "تغلّب على الخجل والاعتماد العاطفي. طوّر الثقة لتعبّر عن حاجاتك.",
    3: "تجنّب التشتت وطوّر التركيز. وجّه الطاقة الإبداعية نحو مشاريع محددة.",
    4: "تغلّب على التصلب واحضن التغيير. المرونة والتكيف مفتاحا النمو.",
    5: "اضبط الإفراط وطوّر الانضباط. الحرية مع المسؤولية تُثمر النضج.",
    6: "تجنّب الحماية المفرطة. ثق بأحبتك ليختاروا اختياراتهم بأنفسهم.",
    7: "تغلّب على العزلة وشارك معرفتك مع العالم. الحكمة لا توجد إلا في المشاركة.",
    8: "وازن الطموح بالأخلاقية والكرم. النجاح في مصلحة الآخرين هو النجاح الحقيقي.",
    9: "تغلّب على التخلي المفرط. تعلّم إتمام الدورات بلا ذنب، وثق بتدفق الحياة.",
}

VIB_AR = {
    1: "وُلد في اهتزاز 1. قائد فطري ورائد ومستقل. طاقة البدء والانطلاق. شجاعة سلوك الطرق التي لم تُسلك. جئت ليتعلم القيادة بالتواضع والخدمة.",
    2: "وُلد في اهتزاز 2. حساس ودبلوماسي وودود. قوتك في الشراكة والانسجام. حدس رقيق. جئت ليتعلم التوازن بين العطاء والتلقي.",
    3: "وُلد في اهتزاز 3. متواصل ومبدع ومتفائل. فرح مُعدٍ. الكلمة أقوى أدواتك. جئت لينير العالم بالفن.",
    4: "وُلد في اهتزاز 4. كادح ومنضبط وعملي. الأسس المتينة تصنع الأمان الحقيقي. جئت ليتفهم أن الأمان الحقيقي يأتي من الداخل.",
    5: "وُلد في اهتزاز 5. محب للحرية ومتنوع المواهب ومحب للمغامرة. طاقته تبحث عن التجارب والتحولات. الفضول يحرّك روحه. جئت ليعيش حياة كاملة.",
    6: "وُلد في اهتزاز 6. محب ومسؤول وعائلي. مهمته الرعاية والانسجام. الحب قوته الأعظم. جئت ليتفهم أن الحب تحرير.",
    7: "وُلد في اهتزاز 7. حكيم ومتأمل وروحي. يبحث عن المعرفة العميقة. الصمت معلمه. جئت ليتفهم أسرار الوجود.",
    8: "وُلد في اهتزاز 8. قوي ومنجز ومزدهر. طاقته تجذب الوفرة. وُلد ليبنِ. جئت ليتفهم أن القوة الحقيقية هي الخدمة.",
    9: "وُلد في اهتزاز 9. إنساني وكريم ومتعاطف. روح قديمة حكيمة. مهمته خدمة الجماعة. جئت ليُكمل دورة التجسدات ويعلّم التخلي.",
    11: "وُلد في اهتزاز 11. سيّد الحدس. ينقل طاقة المستويات الأعلى بالحكمة والإلهام. حضور مغناطيسي. جئت ليوازن نور الروح والثبات في الأرض.",
    22: "وُلد في اهتزاز 22. سيّد البناء. يجسّد أعظم الأحلام في واقع ملموس. رؤية عملية. يبني للإنسانية.",
}

# =====================================================================
# BLOCO HE — HEBRAICO
# =====================================================================
EXPRESS_TXT_HE = {
    1: ("אינדיבידואליות", "מקורי, יצירתי, מנהיג טבעי ועצמאי — אנרגיית הפתיחה והיצירה.",
        "אגוצנטריות, גאווה, אימפולסיביות — נטייה לרכז החלטות ולא להאציל סמכויות.",
        "פתח ענווה: מנהיגות אמיתית היא להעניק השראה, לא לכפות."),
    2: ("שיתוף פעולה", "דיפלומט, רגיש, עושה שלום — נוכחותך מרגיעה ומאזנת את הסביבה.",
        "היסוס, חוסר ביטחון, תלות בדעת אחרים — הימנעות מקונפליקט בכל מחיר.",
        "פתח ביטחון עצמי: הרגישות שלך היא מתנה, לא חולשה."),
    3: ("יצירתיות", "יצירתי, חברתי, אופטימי — כישרון המילה והביטוי האמנותי.",
        "שטחיות, פיזור, הגזמה — אנרגיה מפוזרת מקשה על השלמת פרויקטים.",
        "פתח ריכוז: האיכות חשובה מהכמות."),
    4: ("עבודה", "מעשי, ממושמע, אמין — אבן יסוד של כל פרויקט או צוות.",
        "קשיחות, עקשנות, התנגדות לחדשנות — פחד מהחדש עלול לסגור הזדמנויות.",
        "פתח גמישות: החיים דורשות גם אלתור."),
    5: ("חופש", "רב-כישרונות, אוהב הרפתקאות, קסום — צמא לחיים ולחוויה.",
        "אימפולסיביות, חוסר אחריות, חוסר התחשבות — התפכחות עלולה לפגוע ביקירים.",
        "אזן בין חופש לאחריות: חופש אמיתי מכבד את האחרים."),
    6: ("משפחה", "אחראי, אוהב, מגן — העמוד הרגשי של היקירים.",
        "הגנת יתר, התערבות — קל לרצות לשלוט בשם האהבה.",
        "אהוב בלי לשלוט: טיפול בעצמך הוא טיפול באחרים."),
    7: ("חוכמה", "חכם, אנליטי, רוחני — מחפש את האמת שם שאף אחד לא מביט.",
        "קור רוח, סרקזם, התבודדות — נטייה לעליונות אינטלקטואלית.",
        "אזן תבונה ורגש: חוכמה שווה רק בשיתוף."),
    8: ("כוח", "עוצמתי, משיג, משגשג — נולד להוביל וליצור עושר.",
        "חומרנות, דיקטטוריות, התמכרות לעבודה — עלול להקריב אחרים למען ההצלחה.",
        "השתמש בכוח ביושר: הצלחה אמיתית נמדדת בטוב."),
    9: ("הומניזם", "פילנתרופ, נדיב, חמלתי — רואה את התמונה הגדולה של הקיום.",
        "מלנכוליה, פיזור — נטייה להימלט מהמציאות הקונקרטית.",
        "סלח ושחרר: ההתנתקות היא שחרור."),
    11: ("אדון ההשראה", "אינטואיטיבי, מואר, בעל חזון — מעביר אנרגיה של מישורים גבוהים.",
        "חרדה, מתח, ניכור — הלחץ של הרטט הגבוה כבד.",
        "אזן בין רוחניות לחומר: קרקע את ההשראה."),
    22: ("אדון הבנייה", "מעשי עם חזון — מממש חלומות בקנה מידה גדול.",
        "שאפתנות יתר, סמכותנות — משקל הפוטנציאל העצום עלול לרסק.",
        "בנה בלי להיות עבד של העבודה: ליצירה הגדולה בעלים שקט."),
}

SIG_HE = {
    1: ("אינדיבידואליות",
        "סמל: עיגול. יום: ראשון. כוכב לכת: שמש. יסוד: אש. צבע: צהוב. איבר: לב. "
        "מקורי, יצירתי, מנהיג טבעי, עצמאי, חזק, החלטי, חלוץ. זו אנרגיית ההתחלה, אנרגיית הדחף ליצירה. "
        "בעל המספר הזה חלוץ בעל ראייה שאינו פוחד ללכת בדרכים שלא נסללו. הוא יוזם ואינו תלוי בפעולות אחרים. "
        "מונחה לחיוב, האנרגיה הזו בונה אימפריות ומשנה פרדיגמות. נוכחותו בולטת ונחישותו בלתי מתפשרת.",
        "אגוצנטריות, גאווה, שליטה, אימפולסיביות, עקשנות, חוסר סבלנות. נטייה לרכז החלטות ולא להאציל. "
        "עלול להפוך סמכותני ונוקשה ולרחוק את מי שהיה יכול לשתף פעולה איתם. עודף אינדיבידואליות מוביל לבידוד ופוגע ביחסים.",
        "פתח ענווה ולמד לעבוד בצוות. זכור: אף אחד לא בונה גדולות לבדו. מנהיגות אמיתית היא להעניק השראה, לא לכפות. "
        "חלוקת מנהיגות מכפילה את הישגיך ומותיר מורשת מתמשכת."),
    2: ("שיתוף פעולה",
        "סמל: חצי עיגול. יום: שני. כוכב לכת: ירח. יסוד: מים. צבע: ירוק. "
        "דיפלומט, רגיש, שותף, עושה שלום, אינטואיטיבי, קשוב לפרטים, יודע להקשיב. נוכחותך מרגיעה ומאזנת. "
        "יש לך כישרון לחבר אנשים ולמצוא פתרונות שמספקים את כולם. האינטואיציה שלך עדינה ואתה טועה לעיתים רחוקות בשיפוט אנשים. "
        "אתה חוט הזהב שאורג יחסים יציבים ומשמעותיים.",
        "היסוס, חוסר ביטחון, כניעה, רגישות יתר, תלות בדעת אחרים, ביישנות. נמנע מקונפליקט בכל מחיר, "
        "גם כשצריך להצהיר על עמדה. עלול להקריב את עצמו ביחסים למען שלום ראוותני, מייצר תסכול פנימי.",
        "פתח ביטחון עצמי ועצמאות רגשית. למד לומר «לא» כשצריך. הרגישות שלך היא מתנה, לא חולשה. "
        "שלום אמיתי נולד מאיזון פנימי, לא מהכרה חיצונית."),
    3: ("יצירתיות",
        "סמל: משולש. יום: שלישי. כוכב לכת: צדק. יסוד: אוויר. צבע: סגול. "
        "יצירתי, חברתי, אופטימי, מקסים, מוכשר אמנותית. נוכחותך מאירה כל חלל. "
        "יש לך כישרון המילה והביטוי האמנותי. האנרגיה שלך מדבקת ומושכת אנשים באופן טבעי. "
        "אתה ההתגלמות של שמחת החיים והיצירתיות האינסופית.",
        "שטחיות, פיזור, הגזמה, דרמטיזציה. נטייה לפזר את האנרגיה לכמה כיוונים בלי להשלים פרויקטים. "
        "עלול להשתמש בכישרון הדרמה לתמרן סיטואציות ואנשים.",
        "פתח ריכוז ועומק בביטוי. כוון את הכישרון לכיוון קונקרטי. האיכות חשובה מהכמות."),
    4: ("עבודה",
        "סמל: ריבוע. יום: רביעי. כוכב לכת: אורנוס. יסוד: אדמה. צבע: כחול. "
        "מעשי, ממושמע, אמין, נאמן, סבלני, מאורגן, יעיל, מסור, כן. אתה אבן היסוד של כל פרויקט או צוות. "
        "לא מוותר עד שהעבודה נעשית כמו שצריך. היציבות והביטחון הם בראש סדר העדיפויות שלך. האמינות שלך נותנת שקט לכולם.",
        "קשיחות, עקשנות, התנגדות לשינוי, חומרנות יתר, דחיית חדשנות. עלול להיתקע בשגרה מיותרת "
        "ולפספס הזדמנויות מפחד מהחדש.",
        "פתח גמישות וקלות. לא הכל דורש רצינות כזו. החיים דורשות גם אלתור. "
        "תן אמון יותר בזרימת החיים."),
    5: ("חופש",
        "סמל: כוכב. יום: חמישי. כוכב לכת: כוכב חמה. יסוד: אוויר. צבע: כתום. "
        "אוהב חופש, רב-כישרונות, אוהב הרפתקאות, מתקדם, חכם, סקרן, מסתגל, מקסים. "
        "האנרגיה שלך מדבקת ומושכת בקלות החדש — אנשים ואירועים. אתה צמא לחיים ולחוויה. "
        "אתה ההתגלמות של החופש והחקירה.",
        "אימפולסיביות, חוסר אחריות, חרדה, חוסר התחשבות, התמכרות להנאות. ההתפכחות עלולה לפגוע ביקירים. "
        "עודף חופש עלול להפוך להוללות.",
        "אזן בין חופש לאחריות. חופש אמיתי מכבד את האחרים. "
        "חפש התמדה בלי לאבד את המהות."),
    6: ("משפחה",
        "סמל: משושה. יום: שישי. כוכב לכת: נוגה. יסוד: אדמה. צבע: ורוד. "
        "אחראי, אוהב, מגן, צודק, חמלתי, אמנותי, יועץ טבעי. אתה העמוד הרגשי של היקירים. "
        "יש לך תחושת צדק חדה ואתה מגן על האהובים בכל מחיר.",
        "הגנת יתר, התערבות, דאגה לאחרים. קל לרצות לשלוט בשם האהבה. "
        "עלול לשאת אחריות שאינה שלו.",
        "אהוב בלי לשלוט. כבד את המרחב של האחרים. טיפול בעצמך הוא טיפול באחרים. "
        "אהבה אמיתית היא חופש."),
    7: ("חוכמה",
        "סמל: משובע. יום: שבת. כוכב לכת: נפטון. יסוד: מים. צבע: אינדיגו. "
        "חכם, אנליטי, רוחני, אינטואיטיבי, פרפקציוניסט, מופנם, פילוסופי, מוח יוצא מן הכלל. "
        "מחפש את האמת שם שאף אחד לא מביט. קשר עמוק לעולם הבלתי נראה.",
        "קור רוח, סרקזם, ניכור, חשדנות. נטייה לעליונות אינטלקטואלית. "
        "הבדידות עלולה להפוך למרירות.",
        "אזן תבונה ורגש. שתף במה שלמדת. חוכמה קיימת רק בשיתוף."),
    8: ("כוח",
        "סמל: מתומן. יום: ראשון. כוכב לכת: שבתאי. יסוד: אדמה. צבע: אדום. "
        "עוצמתי, משיג, משגשג, אסטרטגי, שאפתן, בעל חזון. נולד להוביל וליצור עושר. "
        "מממש את החזון במציאות ביעילות. מושך הצלחה באופן טבעי.",
        "חומרנות, דיקטטוריות, התמכרות לעבודה, חוסר סבלנות. עלול להקריב אחרים למען ההצלחה. "
        "כוח בלי אתיקה משחית.",
        "השתמש בכוח ביושר. הצלחה אמיתית נמדדת בטוב שאתה עושה. "
        "הכסף אמצעי, לא מטרה."),
    9: ("הומניזם",
        "סמל: תשיעיון. יום: שלישי. כוכב לכת: מאדים. יסוד: אש. צבע: שני. "
        "פילנתרופ, נדיב, חמלתי, חכם, סובלני, מעורר השראה, אלטרואיסט. רואה את התמונה הגדולה של הקיום. "
        "הנשמה שלך עתיקה ונושאת חוכמה של גלגולים רבים.",
        "מלנכוליה, פיזור, רחמים עצמיים. נטייה להימלט מהמציאות הקונקרטית. "
        "מסתתר באידיאלים שלא מתממשים.",
        "סלח ושחרר. תן אמון בזרימת החיים. ההתנתקות היא שחרור. "
        "דאג לעצמך כדי לדאוג לעולם."),
    11: ("אדון ההשראה",
        "אינטואיטיבי, מואר, מעורר השראה, בעל חזון. מעביר אנרגיה של מישורים גבוהים. "
        "נוגע בידע שעולה על השכל. נוכחות מגנטית ומעוררת השראה. "
        "מרים את כל הסובבים באורו הפנימי.",
        "חרדה, מתח, ניכור, פרנויה. הלחץ של הרטט הגבוה כבד. "
        "עלול להרגיש לא מובן וזר.",
        "אזן בין רוחניות לחומר. קרקע את ההשראה. "
        "טפל בגוף כמו בנשמה."),
    22: ("אדון הבנייה",
        "מעשי עם חזון מעשי. מממש חלומות בקנה מידה גדול. "
        "משלב ראייה רוחנית עם פעולה קונקרטית. הפוטנציאל בלתי מוגבל. אתה אדריכל העתיד, "
        "בונה מפעלים לטובת האנושות.",
        "שאפתנות יתר, לחץ, סמכותנות. משקל הפוטנציאל העצום עלול לרסק ולהוביל לאפיסת כוחות.",
        "בנה בלי להיות עבד של העבודה. אזן בין פעולה לקיום. "
        "ליצירה הגדולה בעלים שקט."),
    33: ("אדון האהבה הקוסמית",
        "אהבה בלתי מותנית, חמלה קוסמית, ריפוי רגשי. אדון האהבה והאור. "
        "מרים את כל הסובבים.",
        "עומס רגשי, נטייה להקרבה עצמית. עלול לספוג את כאב האחרים.",
        "אהוב בלי הקרבה עצמית. טפל בגוף כמו בנשמה."),
}

CAM_HE = {
    1: ("הגשמה", "השליחות שלך היא לפתוח דרכים, להוביל ולחדש. באת להיות חלוץ שיוצר הזדמנויות שם שאין. יש לך את האומץ, הרצון והנחישות למעשים גדולים. האתגר הגדול שלך הוא להבין: מנהיגות משמעות גם שירות, והענקת השראה לאחרים לזהור. נפוליאון בונפרטה, וולט דיסני, סטיב ג'ובס ופלה צעדו בדרך זו של הגשמה וחלוציות."),
    2: ("שלום ושיתוף פעולה", "השליחות שלך היא לשתף פעולה, לאזן ולשרת כגשר בין אנשים. באת להביא הרמוניה ודיפלומטיה. הרגישות שלך היא הכלי הגדול שלך. העולם צריך את יכולתך לאחד התנגדויות ולבנות קונצנזוס. הנסיכה דיאנה, אברהם לינקולן ורוברטו קרלוס הם דוגמה לדרך השלום הזו."),
    3: ("שמחה ויצירתיות", "השליחות שלך היא לתקשר, ליצור ולעורר שמחה. באת לבטא את היופי של החיים דרך אמנות ומילה. הקסם שלך מאיר את הסובבים. אוסקר ויילד, צ'ארלס דיקנס, ג'ים קארי ופול מקרטני צעדו בדרך היצירתית הזו."),
    4: ("פעולה ומבנה", "השליחות שלך היא לבנות, לארגן ולהקים מבנים. באת להציב יסוד מוצק במשמעת, מהפך כאוס לסדר. האמינות שלך היא הונך הגדול. ביל גייטס, זיגמונד פרויד ומרגרט תאצ'ר צעדו בדרך הבנייה הזו."),
    5: ("אבולוציה וחופש", "השליחות שלך היא לחוות, לשנות ולהתפתח. באת לשבור פרדיגמות ולהעניק השראה לשחרור. ריבוי הכישרונות שלך הוא מקור הכוח שלך. פרנקלין רוזוולט, כריסטיאנו רונאלדו ומיק ג'אגר הם דוגמה לטרנספורמציה."),
    6: ("הרמוניה ואחריות", "השליחות שלך היא לשרת, לטפל ולהרמוניז. באת ליצור יופי ואהבה בעולם. ליבך הנדיב מוביל את צעדיך ונוגע בסובבים. ג'ון קנדי, אלביס פרסלי וז'אן ד'ארק הם דוגמה לדרך זו."),
    7: ("חוכמה ושלמות", "השליחות שלך היא לחפש את האמת ולהתפתח רוחנית. באת להבין את סודות הקיום ולהעביר חוכמה. סטיבן הוקינג, מארי קירי, ניקולה טסלה ואלן טיורינג צעדו בדרך החיפוש הזו."),
    8: ("צדק ושגשוג", "השליחות שלך היא לממש שפע בחוכמה. באת להשיג מעשים גדולים, מוכיח ששגשוג ואתיקה הולכים יחד. הנרי פורד, ז'טוליו ורגס, סילביו סנטוס וחוליו איגלסיאס הם דוגמה להישג חומרי בעל מטרה."),
    9: ("חוכמה והומניזם", "השליחות שלך היא לשרת את האנושות בחמלה. באת להשלים את מחזור הגלגולים ולהאיר אחרים. הנשמה שלך נושאת חוכמה של חיים רבים. גנדי, מרטין לותר קינג, האם תרזה וג'ון לנון הם דוגמה לשירות האנושות."),
    11: ("השראה אלוהית", "השליחות שלך היא להאיר ולהרים את התודעה הקולקטיבית. אתה ערוץ לאינטואיציה העליונה. וינסטון צ'רצ'יל, אלברט איינשטיין, מוצרט ומרילין מונרו הם דוגמה להשראה זו."),
    22: ("בנייה בקנה מידה גדול", "השליחות שלך היא להשיג מעשים גדולים לטובת האנושות. אתה אדריכל העתיד. אופרה וינפרי, תומאס אדיסון, סימון בוליבר ופרנק לויד רייט הם דוגמה לבנייה בקנה מידה גדול."),
    33: ("אדון האהבה הקוסמית", "השליחות שלך היא להרים את התודעה דרך אהבה בלתי מותנית. באת לרפא לבבות."),
}

DES_HE = {
    0: "איזון טבעי. בתחום הזה יש לך איזון — רק תן לחיים לזרום.",
    1: "התגבר על האגו, פתח מנהיגות בשירות. הכוח האמיתי הוא בהעצמת אחרים.",
    2: "התגבר על הביישנות והתלות הרגשית. פתח ביטחון עצמי כדי לבטא את צרכיך.",
    3: "הימנע מפיזור, פתח ריכוז. כוון את האנרגיה היצירתית לפרויקטים קונקרטיים.",
    4: "התגבר על קשיחות, קבל שינוי. גמישות והסתגלות הם מפתחות הצמיחה.",
    5: "שלוט בעודפים, פתח משמעת. חופש עם אחריות מניב בגרות.",
    6: "הימנע מהגנת יתר. תן אמון ליקירים לעשות את הבחירות שלהם בעצמם.",
    7: "התגבר על התבודדות, שתף את הידע שלך עם העולם. חוכמה קיימת רק בשיתוף.",
    8: "אזן שאפתנות עם אתיקה ונדיבות. הצלחה לטובת אחרים היא ההצלחה האמיתית.",
    9: "התגבר על התנתקות יתר. למד להשלים מחזורים בלי אשמה, תן אמון בזרימת החיים.",
}

VIB_HE = {
    1: "נולד ברטט 1. מנהיג טבעי, חלוץ, עצמאי. אנרגיית ההתחלה והיציאה לדרך. אומץ ללכת בדרכים שלא נסללו. בא ללמוד להוביל בענווה ובשירות.",
    2: "נולד ברטט 2. רגיש, דיפלומט, שותף. כוחך בשותפות ובהרמוניה. אינטואיציה עדינה. בא ללמוד את האיזון בין לתת ולקבל.",
    3: "נולד ברטט 3. חברתי, יצירתי, אופטימי. שמחה מדבקת. המילה היא כלי החזק שלך. בא להאיר את העולם באמנות.",
    4: "נולד ברטט 4. חרוץ, ממושמע, מעשי. יסודות מוצקים יוצרים ביטחון אמיתי. בא להבין שביטחון אמיתי בא מבפנים.",
    5: "נולד ברטט 5. אוהב חופש, רב-כישרונות, אוהב הרפתקאות. האנרגיה שלו מחפשת חוויות וטרנספורמציות. הסקרנות מניעה את נשמתו. בא לחיות חיים מלאים.",
    6: "נולד ברטט 6. אוהב, אחראי, משפחתי. שליחותו טיפול והרמוניה. האהבה היא כוחו הגדול. בא להבין שאהבה משחררת.",
    7: "נולד ברטט 7. חכם, מתבונן, רוחני. מחפש ידע עמוק. השקט הוא מורהו. בא להבין את סודות הקיום.",
    8: "נולד ברטט 8. עוצמתי, משיג, משגשג. האנרגיה שלו מושכת שפע. נולד לבנות. בא להבין שהכוח האמיתי הוא שירות.",
    9: "נולד ברטט 9. פילנתרופ, נדיב, חמלתי. נשמה עתיקה וחכמה. שליחותו לשרת את הקולקטיב. בא להשלים את מחזור הגלגולים וללמד התנתקות.",
    11: "נולד ברטט 11. אדון האינטואיציה. מעביר אנרגיה של מישורים גבוהים בחוכמה ובהשראה. נוכחות מגנטית. בא לאזן את אור הרוח עם קרקוע.",
    22: "נולד ברטט 22. אדון הבנייה. מממש את החלומות הגדולים ביותר במציאות קונקרטית. ראייה מעשית. בונה למען האנושות.",
}

# =====================================================================
# BLOCO ID — INDONÉSIO
# =====================================================================
EXPRESS_TXT_ID = {
    1: ("Individualitas", "Orisinal, kreatif, pemimpin alami dan mandiri — energi keberangkatan dan penciptaan.",
        "Egoisme, kesombongan, impulsif — kecenderungan memusatkan keputusan dan tidak mendelegasikan.",
        "Kembangkan kerendahan hati: kepemimpinan sejati adalah menginspirasi, bukan memaksakan."),
    2: ("Kolaborasi", "Diplomatis, peka, pembawa damai — kehadiranmu menenangkan dan menyeimbangkan lingkungan.",
        "Ragu-ragu, tidak percaya diri, bergantung pada pendapat orang lain — menghindari konflik dengan segala cara.",
        "Kembangkan kepercayaan diri: kepekaanmu adalah anugerah, bukan kelemahan."),
    3: ("Kreativitas", "Kreatif, komunikatif, optimis — bakat kata dan ekspresi seni.",
        "Dangkal, terpecah, berlebihan — energi terpencar menghambat penyelesaian proyek.",
        "Kembangkan fokus: kualitas lebih penting daripada kuantitas."),
    4: ("Kerja", "Praktis, disiplin, andal — batu fondasi dari setiap proyek atau tim.",
        "Kaku, keras kepala, menolak inovasi — takut pada hal baru dapat menutup peluang.",
        "Kembangkan fleksibilitas: hidup juga membutuhkan improvisasi."),
    5: ("Kebebasan", "Serba bisa, petualang, memesona — haus akan kehidupan dan pengalaman.",
        "Impulsif, tidak bertanggung jawab, gegabah — kemauan berubah dapat menyakiti orang terkasih.",
        "Seimbangkan kebebasan dan tanggung jawab: kebebasan sejati menghormati orang lain."),
    6: ("Keluarga", "Bertanggung jawab, penyayang, pelindung — pilar emosi bagi orang terkasih.",
        "Melindungi berlebihan, ikut campur — mudah ingin mengendalikan atas nama cinta.",
        "Cintai tanpa mengendalikan: merawat diri adalah merawat orang lain."),
    7: ("Kebijaksanaan", "Bijak, analitis, spiritual — mencari kebenaran di tempat yang tak dilihat siapa pun.",
        "Dingin, sarkastis, tertutup — kecenderungan merasa unggul secara intelektual.",
        "Seimbangkan akal dan perasaan: kebijaksanaan hanya berharga jika dibagikan."),
    8: ("Kekuasaan", "Perkasa, berprestasi, makmur — lahir untuk memimpin dan menciptakan kekayaan.",
        "Materialistis, otoriter, pekerja keras berlebihan — dapat mengorbankan orang lain demi sukses.",
        "Gunakan kekuasaan dengan integritas: sukses sejati diukur dengan kebaikan."),
    9: ("Kemanusiaan", "Filantropis, murah hati, penuh welas asih — melihat gambaran besar keberadaan.",
        "Melankolis, terpecah perhatian — cenderung menghindari kenyataan yang konkret.",
        "Ampuni dan lepaskan: ketidakterikatan adalah pembebasan."),
    11: ("Guru Inspirasi", "Intuitif, tercerahkan, visioner — menyalurkan energi tingkat yang lebih tinggi.",
        "Cemas, tegang, terasing — tekanan getaran tinggi berat untuk ditanggung.",
        "Seimbangkan dunia rohani dan material: groundkan inspirasi."),
    22: ("Guru Pembangun", "Praktis dengan visi — mewujudkan mimpi dalam skala besar.",
        "Ambisi berlebihan, otoriter — beban potensi raksasa dapat menghimpit.",
        "Bangun tanpa menjadi budak kerja: karya agung butuh pemilik yang tenang."),
}

SIG_ID = {
    1: ("Individualitas",
        "Simbol: lingkaran. Hari: Minggu. Planet: Matahari. Elemen: Api. Warna: kuning. Organ: jantung. "
        "Orisinal, kreatif, pemimpin alami, mandiri, kuat, tegas, perintis. Ini energi keberangkatan, "
        "energi dorongan untuk mencipta. Pemilik angka ini adalah perintis berwawasan yang tak takut menempuh jalan yang belum dilalui. "
        "Ia berinisiatif dan tidak bergantung pada tindakan orang lain. Diarahkan secara positif, energi ini membangun kerajaan dan mengubah paradigma. "
        "Kehadirannya menonjol dan tekadnya tak tergoyahkan.",
        "Egoisme, kesombongan, dominasi, impulsif, keras kepala, tidak sabar. Kecenderungan memusatkan keputusan "
        "dan tidak mendelegasikan. Dapat menjadi otoriter dan kaku, menjauhi mereka yang bisa diajak berkolaborasi. "
        "Kelebihan individualitas mengarah pada isolasi dan merusak hubungan.",
        "Kembangkan kerendahan hati dan belajar bekerja dalam tim. Ingat: tak seorang pun membangun keagungan sendirian. "
        "Kepemimpinan sejati adalah menginspirasi, bukan memaksakan. Membagikan kepemimpinan melipatgandakan pencapaianmu "
        "dan meninggalkan warisan yang bertahan lama."),
    2: ("Kolaborasi",
        "Simbol: setengah lingkaran. Hari: Senin. Planet: Bulan. Elemen: Air. Warna: hijau. "
        "Diplomatis, peka, suka berkolaborasi, pembawa damai, intuitif, teliti, pendengar yang baik. Kehadiranmu menenangkan dan menyeimbangkan. "
        "Kamu punya bakat menyatukan orang dan menemukan solusi yang memuaskan semua pihak. Intuisimu halus dan jarang salah menilai orang. "
        "Kamu benang emas yang merajut hubungan yang kokoh dan bermakna.",
        "Ragu-ragu, tidak percaya diri, tunduk, terlalu peka, bergantung pada pendapat orang lain, pemalu. Menghindari konflik dengan segala cara, "
        "bahkan saat perlu menyatakan sikap. Dapat mengorbankan diri dalam hubungan demi damai semu, menciptakan frustrasi batin.",
        "Kembangkan kepercayaan diri dan kemandirian emosional. Belajarlah berkata «tidak» saat perlu. Kepekaanmu adalah anugerah, bukan kelemahan. "
        "Damai sejati lahir dari keseimbangan batin, bukan pengakuan dari luar."),
    3: ("Kreativitas",
        "Simbol: segitiga. Hari: Selasa. Planet: Jupiter. Elemen: Udara. Warna: ungu. "
        "Kreatif, komunikatif, optimis, memesona, berbakat secara artistik. Kehadiranmu menerangi ruang mana pun. "
        "Kamu punya bakat kata dan ekspresi seni. Energimu menular dan secara alami menarik orang. "
        "Kamu perwujudan kegembiraan hidup dan kreativitas tanpa batas.",
        "Dangkal, terpecah, berlebihan, teatrikal. Kecenderungan memecah energi ke banyak arah tanpa menyelesaikan proyek. "
        "Dapat menggunakan bakat drama untuk memanipulasi situasi dan orang.",
        "Kembangkan fokus dan kedalaman ekspresi. Arahkan bakat ke arah yang konkret. Kualitas lebih penting daripada kuantitas."),
    4: ("Kerja",
        "Simbol: persegi. Hari: Rabu. Planet: Uranus. Elemen: Tanah. Warna: biru. "
        "Praktis, disiplin, andal, setia, ulet, terorganisir, efisien, berdedikasi, jujur. Kamu batu fondasi setiap proyek atau tim. "
        "Tak menyerah sampai pekerjaan selesai dengan baik. Stabilitas dan keamanan adalah prioritas utamamu. Keandalanmu memberi ketenangan bagi semua orang.",
        "Kaku, keras kepala, menolak perubahan, terlalu materialistis, menolak inovasi. Dapat terjebak dalam rutinitas yang tidak perlu "
        "dan kehilangan peluang karena takut pada hal baru.",
        "Kembangkan fleksibilitas dan kelonggaran. Tidak semua harus begitu serius. Hidup juga membutuhkan improvisasi. "
        "Lebih percayalah pada aliran kehidupan."),
    5: ("Kebebasan",
        "Simbol: bintang. Hari: Kamis. Planet: Merkurius. Elemen: Udara. Warna: oranye. "
        "Cinta kebebasan, serba bisa, petualang, progresif, cerdas, ingin tahu, adaptif, memesona. "
        "Energimu menular dan mudah menarik hal-hal baru — orang dan peristiwa. Kamu haus akan kehidupan dan pengalaman. "
        "Kamu perwujudan kebebasan dan eksplorasi.",
        "Impulsif, tidak bertanggung jawab, cemas, gegabah, larut dalam kesenangan. Kemauan berubah dapat menyakiti orang terkasih. "
        "Kebebasan berlebihan dapat menjadi kenikmatan tanpa kendali.",
        "Seimbangkan kebebasan dan tanggung jawab. Kebebasan sejati menghormati orang lain. "
        "Cari konsistensi tanpa kehilangan esensi."),
    6: ("Keluarga",
        "Simbol: segi enam. Hari: Jumat. Planet: Venus. Elemen: Tanah. Warna: merah muda. "
        "Bertanggung jawab, penyayang, pelindung, adil, welas asih, artistik, penasihat alami. Kamu pilar emosi bagi orang terkasih. "
        "Kamu punya keadilan yang tajam dan melindungi orang terkasih dengan segala cara.",
        "Melindungi berlebihan, ikut campur, khawatir pada orang lain. Mudah ingin mengendalikan atas nama cinta. "
        "Dapat memikul tanggung jawab yang bukan miliknya.",
        "Cintai tanpa mengendalikan. Hargai ruang orang lain. Merawat diri adalah merawat orang lain. "
        "Cinta sejati adalah kebebasan."),
    7: ("Kebijaksanaan",
        "Simbol: segi tujuh. Hari: Sabtu. Planet: Neptunus. Elemen: Air. Warna: nila. "
        "Bijak, analitis, spiritual, intuitif, perfeksionis, introvert, filosofis, otak luar biasa. "
        "Mencari kebenaran di tempat yang tak dilihat siapa pun. Ikatan dalam dengan dunia tak terlihat.",
        "Dingin, sarkastis, terasing, curiga. Kecenderungan merasa unggul secara intelektual. "
        "Kesendirianan dapat berubah menjadi kepahitan.",
        "Seimbangkan akal dan perasaan. Bagikan apa yang kamu pelajari. Kebijaksanaan hanya ada dalam pembagian."),
    8: ("Kekuasaan",
        "Simbol: segi delapan. Hari: Minggu. Planet: Saturnus. Elemen: Tanah. Warna: merah. "
        "Perkasa, berprestasi, makmur, strategis, ambisius, visioner. Lahir untuk memimpin dan menciptakan kekayaan. "
        "Mewujudkan visi menjadi kenyataan dengan efisien. Secara alami menarik kesuksesan.",
        "Materialistis, otoriter, kerja berlebihan, tidak sabar. Dapat mengorbankan orang lain demi sukses. "
        "Kekuasaan tanpa etika merusak.",
        "Gunakan kekuasaan dengan integritas. Sukses sejati diukur dengan kebaikan yang kamu lakukan. "
        "Uang adalah sarana, bukan tujuan."),
    9: ("Kemanusiaan",
        "Simbol: segi sembilan. Hari: Selasa. Planet: Mars. Elemen: Api. Warna: merah kirmizi. "
        "Filantropis, murah hati, welas asih, bijak, toleran, menginspirasi, altruistik. Melihat gambaran besar keberadaan. "
        "Jiwamu purba dan membawa kebijaksanaan banyak kehidupan.",
        "Melankolis, terpecah perhatian, menyayangi diri. Cenderung menghindari kenyataan yang konkret. "
        "Berlindung dalam ideal yang tak terwujud.",
        "Ampuni dan lepaskan. Percayalah pada aliran kehidupan. Ketidakterikatan adalah pembebasan. "
        "Rawat dirimu agar dapat merawat dunia."),
    11: ("Guru Inspirasi",
        "Intuitif, tercerahkan, menginspirasi, visioner. Menyalurkan energi tingkat yang lebih tinggi. "
        "Menyentuh pengetahuan yang melampaui akal. Kehadiran magnetis dan menginspirasi. "
        "Mengangkat semua yang di sekitarnya dengan cahaya batinnya.",
        "Cemas, tegang, terasing, paranoid. Tekanan getaran tinggi berat untuk ditanggung. "
        "Dapat merasa tak dipahami dan asing.",
        "Seimbangkan dunia rohani dan material. Groundkan inspirasi. "
        "Rawat tubuh seperti merawat jiwa."),
    22: ("Guru Pembangun",
        "Praktis dengan visi praktis. Mewujudkan mimpi dalam skala besar. "
        "Menggabungkan pandangan rohani dengan tindakan konkret. Potensinya tak terbatas. Kamu arsitek masa depan, "
        "membangun karya demi kebaikan umat manusia.",
        "Ambisi berlebihan, stres, otoriter. Beban potensi raksasa dapat menghimpit dan menyebabkan kelelahan.",
        "Bangun tanpa menjadi budak kerja. Seimbangkan tindakan dan keberadaan. "
        "Karya agung butuh pemilik yang tenang."),
    33: ("Guru Cinta Kosmik",
        "Cinta tanpa syarat, welas asih kosmik, penyembuhan emosional. Guru cinta dan cahaya. "
        "Mengangkat semua yang di sekitarnya.",
        "Beban emosional berlebihan, kecenderungan berkorban diri. Dapat menyerap penderitaan orang lain.",
        "Cintai tanpa mengorbankan diri. Rawat tubuh seperti merawat jiwa."),
}

CAM_ID = {
    1: ("Pencapaian", "Misi adalah membuka jalan, memimpin, dan berinovasi. Datang menjadi perintis yang menciptakan peluang di tempat yang tak ada peluang. Kamu punya keberanian, kehendak, dan keteguhan untuk karya agung. Tantangan terbesarmu adalah memahami: kepemimpinan juga berarti melayani, dan menginspirasi orang lain untuk bersinar. Napoleon Bonaparte, Walt Disney, Steve Jobs, dan Pelé telah menempuh jalan pencapaian dan keperintisan ini."),
    2: ("Damai dan Kolaborasi", "Misi adalah berkolaborasi, menyeimbangkan, dan melayani sebagai jembatan antar manusia. Datang membawa harmoni dan diplomasi. Kepekaanmu adalah alat terbesarmu. Dunia membutuhkan kemampuanmu menyatukan keberlawanan dan membangun konsensus. Putri Diana, Abraham Lincoln, dan Roberto Carlos adalah teladan jalan damai ini."),
    3: ("Kegembiraan dan Kreativitas", "Misi adalah berkomunikasi, berkarya, dan menginspirasi kegembiraan. Datang mengekspresikan keindahan hidup melalui seni dan kata. Pesonamu menerangi orang di sekitarmu. Oscar Wilde, Charles Dickens, Jim Carrey, dan Paul McCartney telah menempuh jalan kreatif ini."),
    4: ("Tindakan dan Struktur", "Misi adalah membangun, mengorganisir, dan menciptakan struktur. Datang menetapkan fondasi kokoh dengan disiplin, mengubah kekacauan menjadi ketertiban. Keandalanmu adalah modal terbesarmu. Bill Gates, Sigmund Freud, dan Margaret Thatcher telah menempuh jalan pembangunan ini."),
    5: ("Evolusi dan Kebebasan", "Misi adalah mengalami, mengubah, dan berevolusi. Datang meruntuhkan paradigma dan menginspirasi pembebasan. Keserba-bisaanmu adalah sumber kekuatanmu. Franklin Roosevelt, Cristiano Ronaldo, dan Mick Jagger adalah teladan transformasi."),
    6: ("Harmoni dan Tanggung Jawab", "Misi adalah melayani, merawat, dan mengharmoniskan. Datang menciptakan keindahan dan cinta di dunia. Hati yang murah hatimu memimpin langkahmu dan menyentuh orang di sekitar. John F. Kennedy, Elvis Presley, dan Jeanne d'Arc adalah teladan jalan ini."),
    7: ("Kebijaksanaan dan Kesempurnaan", "Misi adalah mencari kebenaran dan berevolusi secara spiritual. Datang memahami rahasia keberadaan dan menyampaikan kebijaksanaan. Stephen Hawking, Marie Curie, Nikola Tesla, dan Alan Turing telah menempuh jalan pencarian ini."),
    8: ("Keadilan dan Kemakmuran", "Misi adalah mewujudkan kelimpahan dengan kebijaksanaan. Datang mencapai karya agung, membuktikan bahwa kemakmuran dan etika berjalan bersama. Henry Ford, Getúlio Vargas, Silvio Santos, dan Julio Iglesias adalah teladan pencapaian material yang bermakna."),
    9: ("Kebijaksanaan dan Kemanusiaan", "Misi adalah melayani umat manusia dengan welas asih. Datang menuntaskan siklus reinkarnasi dan mencerahkan orang lain. Jiwamu membawa kebijaksanaan banyak kehidupan. Gandhi, Martin Luther King, Ibu Teresa, dan John Lennon adalah teladan pelayanan kemanusiaan."),
    11: ("Inspirasi Ilahi", "Misi adalah mencerahkan dan mengangkat kesadaran kolektif. Kamu adalah saluran intuisi tertinggi. Winston Churchill, Albert Einstein, Mozart, dan Marilyn Monroe adalah teladan inspirasi ini."),
    22: ("Pembangunan Skala Besar", "Misi adalah mencapai karya agung demi kebaikan umat manusia. Kamu arsitek masa depan. Oprah Winfrey, Thomas Edison, Simón Bolívar, dan Frank Lloyd Wright adalah teladan pembangunan skala besar."),
    33: ("Guru Cinta Kosmik", "Misi adalah mengangkat kesadaran melalui cinta tanpa syarat. Datang menyembuhkan hati."),
}

DES_ID = {
    0: "Keseimbangan alami. Di bidang ini kamu memiliki keseimbangan — biarkan hidup mengalir.",
    1: "Takluki ego, kembangkan kepemimpinan melalui pelayanan. Kekuatan sejati adalah memberdayakan orang lain.",
    2: "Takluki rasa malu dan ketergantungan emosional. Kembangkan kepercayaan diri untuk menyatakan kebutuhanmu.",
    3: "Hindari perpecahan, kembangkan fokus. Arahkan energi kreatif ke proyek yang konkret.",
    4: "Takluki kekakuan, peluk perubahan. Fleksibilitas dan adaptasi adalah kunci pertumbuhan.",
    5: "Kendalikan kelebihan, kembangkan disiplin. Kebebasan dengan tanggung jawab menghasilkan kedewasaan.",
    6: "Hindari melindungi berlebihan. Percayai orang terkasih untuk membuat pilihan mereka sendiri.",
    7: "Takluki keterasingan, bagikan pengetahuanmu dengan dunia. Kebijaksanaan hanya ada dalam pembagian.",
    8: "Seimbangkan ambisi dengan etika dan kedermawanan. Sukses demi kebaikan orang lain adalah sukses sejati.",
    9: "Takluki ketidakterikatan berlebihan. Belajarlah menuntaskan siklus tanpa rasa bersalah, percayalah pada aliran kehidupan.",
}

VIB_ID = {
    1: "Lahir dalam getaran 1. Pemimpin alami, perintis, mandiri. Energi keberangkatan dan inisiasi. Keberanian menempuh jalan yang belum dilalui. Datang belajar memimpin dengan kerendahan hati dan pelayanan.",
    2: "Lahir dalam getaran 2. Peka, diplomatis, suka kolaborasi. Kekuatanmu dalam kemitraan dan harmoni. Intuisi halus. Datang belajar keseimbangan antara memberi dan menerima.",
    3: "Lahir dalam getaran 3. Komunikatif, kreatif, optimis. Kegembiraan yang menular. Kata adalah alat terkuatmu. Datang menerangi dunia melalui seni.",
    4: "Lahir dalam getaran 4. Tekun, disiplin, praktis. Fondasi kokoh menciptakan keamanan sejati. Datang memahami bahwa keamanan sejati berasal dari dalam.",
    5: "Lahir dalam getaran 5. Cinta kebebasan, serba bisa, petualang. Energinya mencari pengalaman dan transformasi. Rasa ingin tahu menggerakkan jiwanya. Datang menjalani hidup secara utuh.",
    6: "Lahir dalam getaran 6. Penyayang, bertanggung jawab, memihak keluarga. Misinya merawat dan mengharmoniskan. Cinta adalah kekuatan terbesarnya. Datang memahami bahwa cinta membebaskan.",
    7: "Lahir dalam getaran 7. Bijak, introvert, spiritual. Mencari pengetahuan yang dalam. Kesunyian adalah gurunya. Datang memahami rahasia keberadaan.",
    8: "Lahir dalam getaran 8. Perkasa, berprestasi, makmur. Energinya menarik kelimpahan. Lahir untuk membangun. Datang memahami bahwa kekuatan sejati adalah pelayanan.",
    9: "Lahir dalam getaran 9. Filantropis, murah hati, welas asih. Jiwa purba dan bijaksana. Misinya melayani kolektif. Datang menuntaskan siklus reinkarnasi dan mengajarkan ketidakterikatan.",
    11: "Lahir dalam getaran 11. Guru intuisi. Menyalurkan energi tingkat yang lebih tinggi dengan kebijaksanaan dan inspirasi. Kehadiran magnetis. Datang menyeimbangkan cahaya jiwa dengan keterikatan bumi.",
    22: "Lahir dalam getaran 22. Guru pembangun. Mewujudkan mimpi terbesar menjadi kenyataan konkret. Visi praktis. Membangun demi umat manusia.",
}

# =====================================================================
# BLOCO TR — TURCO
# =====================================================================
EXPRESS_TXT_TR = {
    1: ("Bireysellik", "Özgün, yaratıcı, doğuştan lider ve bağımsız — başlangıç ve yaratma enerjisi.",
        "Bencillik, kibir, dürtüsellik — kararları merkezleştirme ve yetki devri yapmama eğilimi.",
        "Alçakgönüllülüğü geliştirin: gerçek liderlik ilham vermektir, dayatmak değil."),
    2: ("İşbirliği", "Diplomat, duyarlı, barış elçisi — varlığınız ortamı sakinleştirir ve dengeleyici.",
        "Kararsızlık, güvensizlik, başkalarının görüşüne bağımlılık — her pahasına çatışmadan kaçınma.",
        "Özgüveninizi geliştirin: duyarlılığınız bir hediyedir, zayıflık değil."),
    3: ("Yaratıcılık", "Yaratıcı, iletişimci, iyimser — sözün ve sanatsal ifadenin yeteneği.",
        "Yüzeysellik, dağınıklık, abartı — dağılan enerji projeleri tamamlamayı engeller.",
        "Odaklanmayı geliştirin: nicelik değil, nitelik önemlidir."),
    4: ("Emek", "Pratik, disiplinli, güvenilir — her projenin ya da ekibin temel taşı.",
        "Katılık, inatçılık, yeniliğe direnç — yeniden korkmak fırsatları kapatabilir.",
        "Esnekliği geliştirin: hayat da doğaçlama ister."),
    5: ("Özgürlük", "Çok yönlü, maceracı, karizmatik — hayata ve deneyime suskuş.",
        "Dürtüsellik, sorumsuzluk, hesapsızlık — değişkenlik sevdiklerinizi yaralayabilir.",
        "Özgürlükle sorumluluğu dengeleyin: gerçek özgürlük başkalarına saygı duyar."),
    6: ("Aile", "Sorumlu, sevecen, koruyucu — sevdiklerinin duygusal dayanağı.",
        "Aşırı korumacılık, her şeye karışma — sevgi adına denetlemek istemek.",
        "Kontrol etmeden sevin: kendinize bakmak, başkalarına bakmaktır."),
    7: ("Bilgelik", "Bilge, analitik, ruhsal — kimsenin bakmadığı yerde gerçeği arar.",
        "Soğukluk, alaycılık, içine kapanıklık — entelektüel üstünlük eğilimi.",
        "Aklı duygula dengeleyin: bilgelik yalnızca paylaşımla değerlidir."),
    8: ("Güç", "Güçlü, başaran, zenginlik getiren — liderlik ve zenginlik yaratmak için doğar.",
        "Materyalizm, otoriterlik, işkoliklik — başarı uğruna başkalarını feda edebilir.",
        "Gücü dürüstlük kullanın: gerçek başarı yaptığınız iyilikle ölçülür."),
    9: ("İnsancılık", "Hayırsever, cömert, şefkatli — varoluşun büyük resmini görür.",
        "Melankoli, dağınıklık — somut gerçeklikten kaçma eğilimi.",
        "Affedin ve bırakın: kopuş, kurtuluştur."),
    11: ("İlham Ustası", "Sezgisel, aydınlanmış, vizyoner — daha yüksek düzeylerin enerjisini taşır.",
        "Kaygı, gerginlik, kopukluk — yüksek titreşimin baskısı ağır taşınır.",
        "Ruhaniyle maddiyatı dengeleyin: ilhamı toprağa indirin."),
    22: ("Kurucu Ustası", "Vizyonu olan pratik — hayalleri büyük ölçekte gerçeğe çevirir.",
        "Aşırı hırs, buyurganlık — devasa potansiyelin ağırlığı ezebilir.",
        "İş kölesi olmadan inşa edin: büyük eserin sakin bir sahibi gerekir."),
}

SIG_TR = {
    1: ("Bireysellik",
        "Sembol: daire. Gün: Pazar. Gezegen: Güneş. Öğe: ateş. Renk: sarı. Organ: kalp. "
        "Özgün, yaratıcı, doğuştan lider, bağımsız, güçlü, kararlı, öncü. Bu, başlangıç enerjisi, yaratma dürtüsünün enerjisidir. "
        "Bu sayının sahibi, yürümemiş yollardan yürümekten korkmayan ileri görüşlü bir öncüdür. Girişimcidir, başkalarının eylemine bağımlı değildir. "
        "Olumlu yönlendirildiğinde bu enerji imparatorluklar kurar, paradigmaları değiştirir. Varlığı belirgindir, azmi sarsılmaz.",
        "Bencillik, kibir, hâkimiyet, dürtüsellik, inatçılık, sabırsızlık. Kararları merkezleştirme ve yetki devri yapmama eğilimi. "
        "Otoriter ve katı hâle gelebilir, işbirliği yapabileceği insanları uzaklaştırabilir. Bireysellikteki aşırılık izolasyona yol açar, ilişkilere zarar verir.",
        "Alçakgönüllülüğü geliştirin ve ekip çalışmasını öğrenin. Unutmayın: kimse büyüklüğü tek başına inşa etmez. Gerçek liderlik ilham vermektir, dayatmak değil. "
        "Liderliği paylaşmak başarılarınızı çoğaltır ve kalıcı bir miras bırakır."),
    2: ("İşbirliği",
        "Sembol: yarım daire. Gün: Pazartesi. Gezegen: Ay. Öğe: su. Renk: yeşil. "
        "Diplomat, duyarlı, işbirliğine açık, barış elçisi, sezgisel, ayrıntılara dikkat eden, iyi dinleyen. Varlığınız sakinleştirir ve dengeleyic. "
        "İnsanları birleştirme ve herkesi memnun eden çözümler bulma yeteneğiniz var. Sezginiz incedir, insanları değerlendirmede nadiren yanılırsınız. "
        "Sağlam ve anlamlı ilişkiler dokuyan altın sinirseniz.",
        "Kararsızlık, güvensizlik, boyun eğme, aşırı duyarlılık, başkalarının görüşüne bağımlılık, utangaçlık. Her pahasına çatışmadan kaçınırsınız, "
        "söz söylemeniz gerektiğinde bile. Görünürde barış uğruna ilişkilerde kendinizi feda edebilir, içsel bir hayal kırıklığı yaratabilirsiniz.",
        "Özgüveni ve duygusal bağımsızlığı geliştirin. Gerektiğinde «hayır» demeyi öğrenin. Duyarlılığınız bir hediyedir, zayıflık değil. "
        "Gerçek barış içsel dengeden doğar, dışsal onaydan değil."),
    3: ("Yaratıcılık",
        "Sembol: üçgen. Gün: Salı. Gezegen: Jüpiter. Öğe: hava. Renk: mor. "
        "Yaratıcı, iletişimci, iyimser, karizmatik, sanatsal yetenekli. Varlığınız her mekânı aydınlatır. "
        "Sözün ve sanatsal ifadenin yeteneğine sahipsiniz. Enerjiniz bulaşıcıdır ve insanları doğal olarak çeker. "
        "Yaşam sevincinin ve sonsuz yaratıcılığın tecessümüsünüz.",
        "Yüzeysellik, dağınıklık, abartı, dramatizasyon. Enerjiyi projeleri tamamlamadan birçok yöne saçma eğilimi. "
        "Drama yeteneğini durumlara ve insanları yönlendirmek için kullanabilir.",
        "İfade odaklılık ve derinliği geliştirin. Yeteneği somut bir yöne kanalize edin. Nicelik değil, nitelik önemlidir."),
    4: ("Emek",
        "Sembol: kare. Gün: Çarşamba. Gezegen: Uranüs. Öğe: toprak. Renk: mavi. "
        "Pratik, disiplinli, güvenilir, sadık, dirençli, düzenli, verimli, özverili, dürüst. Her projenin ya da ekibin temel taşısın. "
        "İş düzgün tamamlanana kadar vazgeçmezsiniz. İstikrar ve güvenlik en büyük önceliğinizdir. Güvenilirliğiniz herkese huzur verir.",
        "Katılık, inatçılık, değişime direnç, aşırı materyalizm, yeniliğe karşı. Gereksiz rutine takılabilir "
        "ve yeniden korktuğu için fırsatları kaçırabilir.",
        "Esneklik ve hafifliği geliştirin. Her şey bu kadar ciddi olmalı değil. Hayat da doğaçlama ister. "
        "Hayatın akışına daha çok güvenin."),
    5: ("Özgürlük",
        "Sembol: yıldız. Gün: Perşembe. Gezegen: Merkür. Öğe: hava. Renk: turuncu. "
        "Özgürlük seven, çok yönlü, maceracı, ilerici, zeki, meraklı, uyum sağlayabilen, karizmatik. "
        "Enerjiniz bulaşıcıdır, yeniyi kolaylıkla çeker — insanları ve olayları. Hayata ve deneyime suskuşsunuz. "
        "Özgürlüğün ve keşifseverliğin tecessümüsünüz.",
        "Dürtüsellik, sorumsuzluk, kaygı, hesapsızlık, hazlara dalarlık. Değişkenlik sevdiklerinizi yaralayabilir. "
        "Özgürlükteki aşırılık ahlaksızlığa dönüşebilir.",
        "Özgürlükle sorumluluğu dengeleyin. Gerçek özgürlük başkalarına saygı duyar. "
        "Özünü kaybetmeden tutarlılık arayın."),
    6: ("Aile",
        "Sembol: altıgen. Gün: Cuma. Gezegen: Venüs. Öğe: toprak. Renk: pembe. "
        "Sorumlu, sevecen, koruyucu, adil, şefkatli, sanatsal, doğuştan danışman. Sevdiklerinizin duygusal dayanağısın. "
        "Keskin bir adalet duygunuz var ve sevdiklerinizi her pahasına korursunuz.",
        "Aşırı korumacılık, her şeye karışma, başkaları için kaygı. Sevgi adına denetlemek istemek kolaydır. "
        "Kendisine ait olmayan sorumluluk taşıyabilir.",
        "Kontrol etmeden sevin. Başkalarının alanına saygı gösterin. Kendinize bakmak, başkalarına bakmaktır. "
        "Gerçek sevgi özgürlüktür."),
    7: ("Bilgelik",
        "Sembol: yedigen. Gün: Cumartesi. Gezegen: Neptün. Öğe: su. Renk: çivit mavisi. "
        "Bilge, analitik, ruhsal, sezgisel, mükemmeliyetçi, içe dönük, felsefi, olağanüstü bir akıl. "
        "Kimsenin bakmadığı yerde gerçeği arar. Görünmeyen dünyaya derin bir bağ vardır.",
        "Soğukluk, alaycılık, kopukluk, şüpheci. Entelektüel üstünlük eğilimi. "
        "Yalnızlık acıya dönüşebilir.",
        "Aklı duygula dengeleyin. Öğrendiklerinizi paylaşın. Bilgelik yalnızca paylaşımla var olur."),
    8: ("Güç",
        "Sembol: sekizgen. Gün: Pazar. Gezegen: Satürn. Öğe: toprak. Renk: kırmızı. "
        "Güçlü, başaran, zenginlik getiren, stratejik, hırslı, vizyoner. Liderlik ve zenginlik yaratmak için doğar. "
        "Vizyonu verimli bir şekilde gerçeğe çevirir. Başarıyı doğal olarak çeker.",
        "Materyalizm, otoriterlik, işkoliklik, sabırsızlık. Başarı uğruna başkalarını feda edebilir. "
        "Ahlaksız güç yozlaştırır.",
        "Gücü dürüstlük kullanın. Gerçek başarı yaptığınız iyilikle ölçülür. "
        "Para araçtır, amaç değildir."),
    9: ("İnsancılık",
        "Sembol: dokuzgen. Gün: Salı. Gezegen: Mars. Öğe: ateş. Renk: kıpkırmızı. "
        "Hayırsever, cömert, şefkatli, bilge, hoşgörülü, ilham verici, özgeci. Varoluşun büyük resmini görür. "
        "Ruhunuz kadimdir, birçok hayattan gelen bilgeliği taşır.",
        "Melankoli, dağınıklık, kendine acıma. Somut gerçeklikten kaçma eğilimi. "
        "Gerçekleşmeyen ideallere sığınabilir.",
        "Affedin ve bırakın. Hayatın akışına güvenin. Kopuş, kurtuluştur. "
        "Dünyaya bakabilmek için önce kendinize iyi bakın."),
    11: ("İlham Ustası",
        "Sezgisel, aydınlanmış, ilham verici, vizyoner. Daha yüksek düzeylerin enerjisini taşır. "
        "Aklı aşan bilgiye dokunur. Varlığı manyetik ve ilham vericidir. "
        "İç ışığıyla etrafındaki herkesi yükseltir.",
        "Kaygı, gerginlik, kopukluk, paranoya. Yüksek titreşimin baskısı ağır taşınır. "
        "Anlaşılmamış ve yabancı hissedebilir.",
        "Ruhaniyle maddiyatı dengeleyin. İlhamı toprağa indirin. "
        "Ruha baktığınız gibi bedene de bakın."),
    22: ("Kurucu Ustası",
        "Pratik vizyonlu. Hayalleri büyük ölçekte gerçeğe çevirir. "
        "Ruhani görüşü somut eylemle birleştirir. Potansiyeli sınırsızdır. Geleceğin mimarısınız, "
        "insanlığın yararına eserler inşa edersiniz.",
        "Aşırı hırs, stres, buyurganlık. Devasa potansiyelin ağırlığı ezebilir, tükenmişliğe yol açabilir.",
        "İş kölesi olmadan inşa edin. Eylemle varoluşu dengeleyin. "
        "Büyük eserin sakin bir sahibi gerekir."),
    33: ("Evrensel Sevgi Ustası",
        "Koşulsuz sevgi, evrensel şefkat, duygusal şifa. Sevgi ve ışık ustası. "
        "Etrafındaki herkesi yükseltir.",
        "Duygusal aşırı yükleme, kendini feda eğilimi. Başkalarının acısını emebilir.",
        "Kendini feda etmeden sevin. Ruha baktığınız gibi bedene de bakın."),
}

CAM_TR = {
    1: ("Gerçekleşme", "Görevin yol açmak, liderlik etmek ve yenilik etmektir. Fırsatların olmadığı yerde fırsat yaratan bir öncü olmak için geldin. Büyük işler için cesaretin, iraden ve azmin var. En büyük meydan okuman şunu kavramaktır: liderlik aynı zamanda hizmet etmek ve başkalarını parlamaları için ilham vermektir. Napoleon Bonaparte, Walt Disney, Steve Jobs ve Pelé bu gerçekleşme ve öncülük yolunda yürüdü."),
    2: ("Barış ve İşbirliği", "Görevin işbirliği yapmak, dengelemek ve insanlar arasında köprü olarak hizmet etmektir. Uyum ve diplomasi getirmek için geldin. Duyarlılığın en büyük aracındır. Dünya, karşıtlıkları birleştirmek ve uzlaşma inşa etme yeteneğine ihtiyaç duyuyor. Prenses Diana, Abraham Lincoln ve Roberto Carlos bu barışçıl yolun örnekleridir."),
    3: ("Neşe ve Yaratıcılık", "Görevin iletişim kurmak, yaratmak ve neşeyi ilham etmektir. Hayatın güzelliğini sanat ve sözle ifade etmek için geldin. Karizman etrafındaki insanları aydınlatır. Oscar Wilde, Charles Dickens, Jim Carrey ve Paul McCartney bu yaratıcı yolda yürüdü."),
    4: ("Eylem ve Yapı", "Görevin inşa etmek, örgütlemek ve yapılar kurmaktır. Kaosu düzene çevirerek disiplinle sağlam bir temel atmak için geldin. Güvenilirliğin en büyük sermayendir. Bill Gates, Sigmund Freud ve Margaret Thatcher bu kurucu yolda yürüdü."),
    5: ("Evrim ve Özgürlük", "Görevin deneyimlemek, değiştirmek ve evrimleşmektir. Paradigmaları kırmak ve kurtuluş ilham etmek için geldin. Çok yönlülüğün güç kaynağındır. Franklin Roosevelt, Cristiano Ronaldo ve Mick Jagger dönüşümün örnekleridir."),
    6: ("Uyum ve Sorumluluk", "Görevin hizmet etmek, şefkat göstermek ve uyum sağlamaktır. Dünyada güzellik ve sevgi yaratmak için geldin. Cömert kalbin adımlarını yönlendirir ve etrafındakilere dokunur. John Kennedy, Elvis Presley ve Jeanne d'Arc bu yolun örnekleridir."),
    7: ("Bilgelik ve Kusursuzluk", "Görevin gerçeği aramak ve ruhsal olarak evrimleşmektir. Varoluşun sırlarını kavramak ve bilgeliği aktarmak için geldin. Stephen Hawking, Marie Curie, Nikola Tesla ve Alan Turing bu arayış yolunda yürüdü."),
    8: ("Adalet ve Refah", "Görevin bolluğu bilgelikle görünür kılmaktır. Büyük eserler başarmak, refahın etikle birlikte yürüdüğünü kanıtlamak için geldin. Henry Ford, Getúlio Vargas, Silvio Santos ve Julio Iglesias amaçlı maddi başarının örnekleridir."),
    9: ("Bilgelik ve İnsancılık", "Görevin insanlığı şefkatle hizmet etmektir. Ruhani yolculuğun döngüsünü tamamlamak ve başkalarını aydınlatmak için geldin. Ruhun birçok hayatın bilgeliğini taşır. Gandhi, Martin Luther King, Anne Teresa ve John Lennon insanlığa hizmetin örnekleridir."),
    11: ("İlahi İlham", "Görevin kolektif bilinci aydınlatmak ve yükseltmektir. Yüce sezginin kanalısın. Winston Churchill, Albert Einstein, Mozart ve Marilyn Monroe bu ilhamın örnekleridir."),
    22: ("Büyük Ölçekli İnşa", "Görevin insanlığın yararına büyük eserler başarmaktır. Geleceğin mimarısın. Oprah Winfrey, Thomas Edison, Simón Bolívar ve Frank Lloyd Wright büyük ölçekli inşanın örnekleridir."),
    33: ("Evrensel Sevgi Ustası", "Görevin bilinci koşulsuz sevgiyle yükseltmektir. Kalpleri iyileştirmek için geldin."),
}

DES_TR = {
    0: "Doğal denge. Bu alanda denge sende — hayata akmaya bırak.",
    1: "Egonu yen, hizmet üzerinden liderliği geliştir. Gerçek güç başkalarını güçlendirmektir.",
    2: "Utanç duygusunu ve duygusal bağımlılığı yen. İhtiyaçlarını ifade etmek için özgüveni geliştir.",
    3: "Dağınıklıktan kaçın, odaklanmayı geliştir. Yaratıcı enerjiyi somut projelere yönlendir.",
    4: "Katılığı yen, değişimi kucakla. Esneklik ve uyum büyümenin anahtarıdır.",
    5: "Aşırılıkları kontrol et, disiplini geliştir. Sorumlulukla özgürlük olgunluk getirir.",
    6: "Aşırı korumacılıktan kaçın. Sevdiklerine kendi seçimlerini yapma güvenini ver.",
    7: "İzolasyonu yen, bilginle dünyayı paylaş. Bilgelik yalnızca paylaşımla var olur.",
    8: "Hırsı etik ve cömertlikle dengele. Başkalarının iyiliği için olan başarı gerçek başarıdır.",
    9: "Aşırı kopuşu yen. Suçluluk duymadan döngüleri tamamlamayı öğren, hayatın akışına güven.",
}

VIB_TR = {
    1: "1 titreşiminde doğdun. Doğuştan lider, öncü, bağımsız. Başlangıç ve atılım enerjisi. Yürümemiş yollardan yürüme cesareti. Alçakgönüllükle ve hizmetle liderlik etmeyi öğrenmek için geldi.",
    2: "2 titreşiminde doğdun. Duyarlı, diplomat, işbirlikçi. Gücün ortaklık ve uyumdadır. İnce sezgi. Vermekle almak arasındaki dengeyi öğrenmek için geldi.",
    3: "3 titreşiminde doğdun. İletişimci, yaratıcı, iyimser. Bulaşıcı neşe. Söz en güçlü aracındır. Sanatla dünyayı aydınlatmak için geldi.",
    4: "4 titreşiminde doğdun. Çalışkan, disiplinli, pratik. Sağlam temeller gerçek güvenliği yaratır. Gerçek güvenliğin içeriden geldiğini anlamak için geldi.",
    5: "5 titreşiminde doğdun. Özgürlük seven, çok yönlü, maceracı. Enerjisi deneyim ve dönüşüm arar. Merak ruhunu yönlendirir. Hayatı dolu dolu yaşamak için geldi.",
    6: "6 titreşiminde doğdun. Sevecen, sorumlu, aile öncü. Görevi şefkat ve uyumdur. Sevgi en büyük gücüdür. Sevginin özgürleştirdiğini anlamak için geldi.",
    7: "7 titreşiminde doğdun. Bilge, içe dönük, ruhsal. Derin bilgi arar. Sessizlik onun öğretmenidir. Varoluşun sırlarını anlamak için geldi.",
    8: "8 titreşiminde doğdun. Güçlü, başaran, zenginlik getiren. Enerjisi bolluk çeker. İnşa etmek için doğdu. Gerçek gücün hizmet olduğunu anlamak için geldi.",
    9: "9 titreşiminde doğdun. Hayırsever, cömert, şefkatli. Kadim ve bilge ruh. Görevi kolektife hizmet etmektir. Ruhani döngüyü tamamlamak ve kopuşu öğretmek için geldi.",
    11: "11 titreşiminde doğdun. Sezgi ustası. Daha yüksek düzeylerin enerjisini bilgelik ve ilhamla taşır. Manyetik varlık. Ruhun ışığıyla toprak bağını dengelemek için geldi.",
    22: "22 titreşiminde doğdun. Kurucu usta. En büyük hayalleri somut gerçeğe çevirir. Pratik vizyon. İnsanlık için inşa eder.",
}

# =====================================================================
# BLOCO VI — VIETNAMITA
# =====================================================================
EXPRESS_TXT_VI = {
    1: ("Cá tính", "Sáng tạo, độc đáo, lãnh đạo bẩm sinh và độc lập — năng lượng khởi đầu và kiến tạo.",
        "Ích kỷ, kiêu ngạo, bốc đồng — xu hướng tập trung quyền quyết định, không ủy quyền.",
        "Rèn khiêm nhường: lãnh đạo đích thực là truyền cảm hứng, không phải áp đặt."),
    2: ("Hợp tác", "Ngoại giao, nhạy cảm, người kiến tạo hòa bình — sự hiện diện của bạn xoa dịu và cân bằng môi trường.",
        "Do dự, thiếu tự tin, phụ thuộc ý kiến người khác — né tránh xung đột bằng mọi giá.",
        "Rèn sự tự tin: sự nhạy cảm của bạn là món quà, không phải điểm yếu."),
    3: ("Sáng tạo", "Sáng tạo, giao tiếp giỏi, lạc quan — tài năng ngôn từ và biểu đạt nghệ thuật.",
        "Hời hợt, phân tán, cường điệu — năng lượng dàn trải cản trở hoàn thành dự án.",
        "Rèn sự tập trung: chất lượng quan trọng hơn số lượng."),
    4: ("Lao động", "Thực tế, kỷ luật, đáng tin — nền móng của mọi dự án hay đội nhóm.",
        "Cứng nhắc, bướng bỉnh, kháng cự đổi mới — nỗi sợ cái mới có thể khép lại cơ hội.",
        "Rèn sự linh hoạt: cuộc sống cũng cần cả ứng biến."),
    5: ("Tự do", "Đa tài, yêu phiêu lưu, quyến rũ — khát khao sống và trải nghiệm.",
        "Bốc đồng, thiếu trách nhiệm, bất chấp — tính thất thường có thể làm tổn thương người thân yêu.",
        "Cân bằng tự do và trách nhiệm: tự do đích thực tôn trọng người khác."),
    6: ("Gia đình", "Có trách nhiệm, yêu thương, che chở — điểm tựa cảm xúc của người thân.",
        "Bao bọc quá mức, xen vào việc người khác — dễ muốn kiểm soát nhân danh tình yêu.",
        "Yêu mà không kiểm soát: chăm sóc mình cũng là chăm sóc người khác."),
    7: ("Trí tuệ", "Thông tuệ, phân tích, tâm linh — tìm kiếm chân lý nơi không ai ngắm nhìn.",
        "Lạnh lùng, mỉa mai, thu mình — xu hướng tự cho mình ưu việt về trí tuệ.",
        "Cân bằng lý trí và cảm xúc: trí tuệ chỉ có giá trị khi được chia sẻ."),
    8: ("Sức mạnh", "Mạnh mẽ, thành đạt, thịnh vượng — sinh ra để dẫn dắt và kiến tạo sự giàu có.",
        "Duy vật, độc đoán, nghiện công việc — có thể hy sinh người khác vì thành công.",
        "Sử dụng sức mạnh với chính trực: thành công đích thực đo bằng điều tốt bạn làm."),
    9: ("Nhân văn", "Nhân đạo, hào phóng, giàu lòng trắc ẩn — nhìn thấy bức tranh lớn của tồn tại.",
        "U sầu, phân tán — xu hướng trốn tránh hiện thực cụ thể.",
        "Tha thứ và buông bỏ: buông bỏ chính là giải thoát."),
    11: ("Bậc thầy truyền cảm hứng", "Trực giác, giác ngộ, tầm nhìn xa — dẫn truyền năng lượng của những tầng cao hơn.",
        "Lo âu, căng thẳng, xa cách — áp lực của tần số cao rất nặng để gánh.",
        "Cân bằng tâm linh và vật chất: hạ cảm hứng xuống mặt đất."),
    22: ("Bậc thầy kiến tạo", "Thực tế với tầm nhìn — hiện thực hóa ước mơ ở quy mô lớn.",
        "Tham vọng quá mức, độc tài — sức nặng của tiềm năng khổng lồ có thể đè nát.",
        "Kiến tạo mà không làm nô lệ công việc: kiệt tác cần một chủ nhân thanh thản."),
}

SIG_VI = {
    1: ("Cá tính",
        "Biểu tượng: vòng tròn. Ngày: Chủ nhật. Hành tinh: Mặt trời. Nguyên tố: Hỏa. Màu: vàng. Cơ quan: tim. "
        "Độc đáo, sáng tạo, lãnh đạo bẩm sinh, độc lập, mạnh mẽ, quyết đoán, tiên phong. Đây là năng lượng khởi đầu, "
        "năng lượng của xung lực kiến tạo. Người mang số này là nhà tiên phong có tầm nhìn, không sợ đi những con đường chưa ai đi. "
        "Họ chủ động, không phụ thuộc vào hành động của người khác. Định hướng tích cực, năng lượng này xây đế quốc và thay đổi mô hình tư duy. "
        "Sự hiện diện nổi bật và ý chí sắt đá.",
        "Ích kỷ, kiêu ngạo, độc đoán, bốc đồng, bướng bỉnh, thiếu kiên nhẫn. Xu hướng tập trung quyền quyết định, không ủy quyền. "
        "Có thể trở nên chuyên chế và cứng nhắc, xa lánh những người đáng có thể hợp tác. Thừa quá cá tính dẫn đến cô lập và tổn hại các mối quan hệ.",
        "Rèn khiêm nhường và học làm việc nhóm. Nhớ rằng: không ai kiến tạo vĩ đại một mình. Lãnh đạo đích thực là truyền cảm hứng, không phải áp đặt. "
        "Chia sẻ quyền lãnh đạo nhân đôi thành quả và để lại di sản bền vững."),
    2: ("Hợp tác",
        "Biểu tượng: nửa vòng tròn. Ngày: Thứ hai. Hành tinh: Mặt trăng. Nguyên tố: Thủy. Màu: xanh lá. "
        "Ngoại giao, nhạy cảm, hợp tác, kiến tạo hòa bình, trực giác, tỉ mỉ, biết lắng nghe. Sự hiện diện xoa dịu và cân bằng. "
        "Bạn có tài kết nối con người và tìm giải pháp khiến mọi bên hài lòng. Trực giác tinh tế, hiếm khi đánh giá sai con người. "
        "Bạn là sợi chỉ vàng dệt nên những mối quan hệ bền chặt và ý nghĩa.",
        "Do dự, thiếu tự tin, phục tùng, quá nhạy cảm, phụ thuộc ý kiến người khác, nhút nhát. Né tránh xung đột bằng mọi giá, "
        "ngay cả khi cần bày tỏ lập trường. Có thể hy sinh mình trong quan hệ vì hòa bình bề ngoài, tạo nỗi hụt hẫng bên trong.",
        "Rèn sự tự tin và độc lập cảm xúc. Học nói «không» khi cần. Sự nhạy cảm của bạn là món quà, không phải điểm yếu. "
        "Hòa bình đích thực sinh ra từ cân bằng nội tâm, không phải sự công nhận từ bên ngoài."),
    3: ("Sáng tạo",
        "Biểu tượng: tam giác. Ngày: Thứ ba. Hành tinh: Mộc tinh. Nguyên tố: Phong. Màu: tím. "
        "Sáng tạo, giao tiếp giỏi, lạc quan, quyến rũ, tài năng nghệ thuật. Sự hiện diện soi sáng bất kỳ không gian nào. "
        "Bạn có tài ngôn từ và biểu đạt nghệ thuật. Năng lượng lan tỏa, tự nhiên thu hút mọi người. "
        "Bạn là hiện thân của niềm vui sống và sáng tạo vô biên.",
        "Hời hợt, phân tán, cường điệu, kịch tính hóa. Xu hướng dàn trải năng lượng nhiều hướng mà không hoàn thành dự án. "
        "Có thể dùng tài kịch để thao túng tình huống và con người.",
        "Rèn sự tập trung và chiều sâu biểu đạt. Định hướng tài năng vào con đường cụ thể. Chất lượng quan trọng hơn số lượng."),
    4: ("Lao động",
        "Biểu tượng: hình vuông. Ngày: Thứ tư. Hành tinh: Thiên vương tinh. Nguyên tố: Thổ. Màu: xanh dương. "
        "Thực tế, kỷ luật, đáng tin, trung thành, bền bỉ, ngăn nắp, hiệu quả, tận tụy, ngay thẳng. Bạn là nền móng của mọi dự án hay đội nhóm. "
        "Không bỏ cuộc cho đến khi công việc hoàn thành đúng chuẩn. Sự ổn định và an toàn là ưu tiên số một. Sự đáng tin của bạn mang lại bình yên cho mọi người.",
        "Cứng nhắc, bướng bỉnh, kháng cự thay đổi, duy vật quá mức, bài xích đổi mới. Có thể mắc kẹt trong thói quen không cần thiết "
        "và bỏ lỡ cơ hội vì sợ cái mới.",
        "Rèn sự linh hoạt và nhẹ nhàng. Không phải việc gì cũng nghiêm trọng thế. Cuộc sống cũng cần ứng biến. "
        "Hãy tin vào dòng chảy của cuộc sống hơn."),
    5: ("Tự do",
        "Biểu tượng: ngôi sao. Ngày: Thứ năm. Hành tinh: Sao Thủy. Nguyên tố: Phong. Màu: cam. "
        "Yêu tự do, đa tài, yêu phiêu lưu, tiến bộ, thông minh, ham hiểu biết, dễ thích nghi, quyến rũ. "
        "Năng lượng lan tỏa, dễ dàng thu hút cái mới — cả người lẫn sự kiện. Bạn khát khao sống và trải nghiệm. "
        "Bạn là hiện thân của tự do và khám phá.",
        "Bốc đồng, thiếu trách nhiệm, lo âu, bất chấp, sa đà khoái lạc. Tính thất thường có thể làm tổn thương người thân yêu. "
        "Tự do quá đà có thể biến thành buông thả.",
        "Cân bằng tự do và trách nhiệm. Tự do đích thực tôn trọng người khác. "
        "Tìm kiếm sự nhất quán mà không mất bản chất."),
    6: ("Gia đình",
        "Biểu tượng: lục giác. Ngày: Thứ sáu. Hành tinh: Kim tinh. Nguyên tố: Thổ. Màu: hồng. "
        "Có trách nhiệm, yêu thương, che chở, công bằng, trắc ẩn, nghệ sĩ, cố vấn bẩm sinh. Bạn là điểm tựa cảm xúc của người thân. "
        "Bạn có ý thức công bằng sắc bén và bảo vệ người yêu thương bằng mọi giá.",
        "Bao bọc quá mức, xen vào việc người khác, lo lắng thay người khác. Dễ muốn kiểm soát nhân danh tình yêu. "
        "Có thể gánh trách nhiệm không thuộc về mình.",
        "Yêu mà không kiểm soát. Tôn trọng không gian của người khác. Chăm sóc mình cũng là chăm sóc người khác. "
        "Tình yêu đích thực là tự do."),
    7: ("Trí tuệ",
        "Biểu tượng: thất giác. Ngày: Thứ bảy. Hành tinh: Hải vương tinh. Nguyên tố: Thủy. Màu: chàm. "
        "Thông tuệ, phân tích, tâm linh, trực giác, cầu toàn, hướng nội, triết lý, bộ óc xuất chúng. "
        "Tìm kiếm chân lý nơi không ai ngắm nhìn. Gắn kết sâu xa với thế giới vô hình.",
        "Lạnh lùng, mỉa mai, xa cách, hoài nghi. Xu hướng tự cho mình ưu việt về trí tuệ. "
        "Cô đơn có thể biến thành cay đắng.",
        "Cân bằng lý trí và cảm xúc. Chia sẻ điều đã học. Trí tuệ chỉ tồn tại trong sự chia sẻ."),
    8: ("Sức mạnh",
        "Biểu tượng: bát giác. Ngày: Chủ nhật. Hành tinh: Thổ tinh. Nguyên tố: Thổ. Màu: đỏ. "
        "Mạnh mẽ, thành đạt, thịnh vượng, chiến lược, tham vọng, tầm nhìn xa. Sinh ra để dẫn dắt và kiến tạo sự giàu có. "
        "Hiện thực hóa tầm nhìn một cách hiệu quả. Tự nhiên thu hút thành công.",
        "Duy vật, độc đoán, nghiện công việc, thiếu kiên nhẫn. Có thể hy sinh người khác vì thành công. "
        "Quyền lực không có đạo đức sẽ tha hóa.",
        "Sử dụng sức mạnh với chính trực. Thành công đích thực đo bằng điều tốt bạn làm. "
        "Tiền là phương tiện, không phải đích đến."),
    9: ("Nhân văn",
        "Biểu tượng: cửu giác. Ngày: Thứ ba. Hành tinh: Hỏa tinh. Nguyên tố: Hỏa. Màu: đỏ thẫm. "
        "Nhân đạo, hào phóng, trắc ẩn, thông tuệ, khoan dung, truyền cảm hứng, vị tha. Nhìn thấy bức tranh lớn của tồn tại. "
        "Tâm hồn bạn cổ xưa, mang trí tuệ của nhiều kiếp sống.",
        "U sầu, phân tán, thương hại bản thân. Xu hướng trốn tránh hiện thực cụ thể. "
        "Trốn vào những lý tưởng không thể hiện thực hóa.",
        "Tha thứ và buông bỏ. Tin vào dòng chảy cuộc sống. Buông bỏ chính là giải thoát. "
        "Chăm sóc mình để có thể chăm sóc thế giới."),
    11: ("Bậc thầy truyền cảm hứng",
        "Trực giác, giác ngộ, truyền cảm hứng, tầm nhìn xa. Dẫn truyền năng lượng của những tầng cao hơn. "
        "Chạm đến tri thức vượt lý trí. Sự hiện diện từ tính và đầy cảm hứng. "
        "Nâng đỡ mọi người xung quanh bằng ánh sáng nội tâm.",
        "Lo âu, căng thẳng, xa cách, hoang tưởng. Áp lực của tần số cao rất nặng để gánh. "
        "Có thể cảm thấy không được thấu hiểu, lạc lõng.",
        "Cân bằng tâm linh và vật chất. Hạ cảm hứng xuống mặt đất. "
        "Chăm sóc thể xác như chăm sóc tâm hồn."),
    22: ("Bậc thầy kiến tạo",
        "Thực tế với tầm nhìn thực tiễn. Hiện thực hóa ước mơ ở quy mô lớn. "
        "Kết hợp tầm nhìn tâm linh với hành động cụ thể. Tiềm năng vô hạn. Bạn là kiến trúc sư của tương lai, "
        "kiến tạo những công trình vì lợi ích nhân loại.",
        "Tham vọng quá mức, căng thẳng, độc đoán. Sức nặng của tiềm năng khổng lồ có thể đè nát, dẫn đến kiệt sức.",
        "Kiến tạo mà không làm nô lệ công việc. Cân bằng hành động và hiện hữu. "
        "Kiệt tác cần một chủ nhân thanh thản."),
    33: ("Bậc thầy tình yêu vũ trụ",
        "Tình yêu vô điều kiện, lòng trắc ẩn vũ trụ, chữa lành cảm xúc. Bậc thầy của tình yêu và ánh sáng. "
        "Nâng đỡ tất cả những người xung quanh.",
        "Quá tải cảm xúc, xu hướng tự hy sinh. Có thể hấp thụ nỗi đau của người khác.",
        "Yêu mà không tự hy sinh. Chăm sóc thể xác như chăm sóc tâm hồn."),
}

CAM_VI = {
    1: ("Viên mãn", "Sứ mệnh của bạn là mở đường, dẫn dắt và đổi mới. Bạn sinh ra để là người tiên phong kiến tạo cơ hội nơi chưa có cơ hội. Bạn có lòng can đảm, ý chí và nghị lực cho những sự nghiệp vĩ đại. Thử thách lớn nhất của bạn là thấu hiểu: lãnh đạo cũng là phục vụ, và truyền cảm hứng cho người khác tỏa sáng. Napoléon Bonaparte, Walt Disney, Steve Jobs và Pelé đã đi trên con đường viên mãn và tiên phong này."),
    2: ("Hòa bình và Hợp tác", "Sứ mệnh của bạn là hợp tác, cân bằng và phục vụ như cây cầu giữa con người. Bạn sinh ra để mang đến hòa hợp và ngoại giao. Sự nhạy cảm là công cụ lớn nhất của bạn. Thế giới cần khả năng kết nối các mặt đối lập và kiến tạo đồng thuận của bạn. Công nương Diana, Abraham Lincoln và Roberto Carlos là tấm gương của con đường hòa bình này."),
    3: ("Vui vẻ và Sáng tạo", "Sứ mệnh của bạn là giao tiếp, sáng tạo và truyền niềm vui. Bạn sinh ra để bày tỏ vẻ đẹp cuộc sống qua nghệ thuật và ngôn từ. Sức quyến rũ của bạn soi sáng những người xung quanh. Oscar Wilde, Charles Dickens, Jim Carrey và Paul McCartney đã đi trên con đường sáng tạo này."),
    4: ("Hành động và Cấu trúc", "Sứ mệnh của bạn là xây dựng, tổ chức và tạo lập cấu trúc. Bạn sinh ra để đặt nền móng vững chắc bằng kỷ luật, biến hỗn loạn thành trật tự. Sự đáng tin là tài sản lớn nhất của bạn. Bill Gates, Sigmund Freud và Margaret Thatcher đã đi trên con đường kiến tạo này."),
    5: ("Tiến hóa và Tự do", "Sứ mệnh của bạn là trải nghiệm, thay đổi và tiến hóa. Bạn sinh ra để phá vỡ mô hình tư duy và truyền cảm hứng giải phóng. Sự đa tài là nguồn sức mạnh của bạn. Franklin Roosevelt, Cristiano Ronaldo và Mick Jagger là tấm gương của sự chuyển hóa."),
    6: ("Hài hòa và Trách nhiệm", "Sứ mệnh của bạn là phục vụ, chăm sóc và tạo hài hòa. Bạn sinh ra để kiến tạo vẻ đẹp và tình yêu trong thế giới. Trái tim hào phóng dẫn lối bước chân và chạm đến những người xung quanh. John Kennedy, Elvis Presley và Jeanne d'Arc là tấm gương của con đường này."),
    7: ("Trí tuệ và Hoàn hảo", "Sứ mệnh của bạn là tìm kiếm chân lý và tiến hóa tâm linh. Bạn sinh ra để thấu hiểu những bí ẩn của tồn tại và truyền đạt trí tuệ. Stephen Hawking, Marie Curie, Nikola Tesla và Alan Turing đã đi trên con đường tìm kiếm này."),
    8: ("Công lý và Thịnh vượng", "Sứ mệnh của bạn là hiện thực hóa sự sung túc bằng trí tuệ. Bạn sinh ra để làm nên sự nghiệp vĩ đại, chứng minh rằng thịnh vượng và đạo đức đi cùng nhau. Henry Ford, Getúlio Vargas, Silvio Santos và Julio Iglesias là tấm gương thành tựu vật chất có mục đích."),
    9: ("Trí tuệ và Nhân văn", "Sứ mệnh của bạn là phục vụ nhân loại bằng lòng trắc ẩn. Bạn sinh ra để hoàn tất vòng luân hồi và soi sáng người khác. Tâm hồn bạn mang trí tuệ của nhiều kiếp sống. Gandhi, Martin Luther King, Mẹ Teresa và John Lennon là tấm gương phục vụ nhân loại."),
    11: ("Cảm hứng Thần thánh", "Sứ mệnh của bạn là soi sáng và nâng cao ý thức tập thể. Bạn là kênh dẫn của trực giác tối thượng. Winston Churchill, Albert Einstein, Mozart và Marilyn Monroe là tấm gương của cảm hứng này."),
    22: ("Kiến tạo Quy mô lớn", "Sứ mệnh của bạn là làm nên sự nghiệp vĩ đại vì lợi ích nhân loại. Bạn là kiến trúc sư của tương lai. Oprah Winfrey, Thomas Edison, Simón Bolívar và Frank Lloyd Wright là tấm gương kiến tạo quy mô lớn."),
    33: ("Bậc thầy Tình yêu Vũ trụ", "Sứ mệnh của bạn là nâng cao ý thức qua tình yêu vô điều kiện. Bạn sinh ra để chữa lành trái tim."),
}

DES_VI = {
    0: "Cân bằng tự nhiên. Trong lĩnh vực này bạn đã có sự cân bằng — cứ để cuộc sống trôi chảy.",
    1: "Vượt qua cái tôi, rèn lãnh đạo qua phục vụ. Sức mạnh đích thực là nâng đỡ người khác.",
    2: "Vượt qua sự nhút nhát và phụ thuộc cảm xúc. Rèn sự tự tin để bày tỏ nhu cầu của mình.",
    3: "Tránh sự phân tán, rèn sự tập trung. Định hướng năng lượng sáng tạo vào dự án cụ thể.",
    4: "Vượt qua sự cứng nhắc, đón nhận thay đổi. Linh hoạt và thích nghi là chìa khóa tăng trưởng.",
    5: "Kiểm soát sự dư thừa, rèn kỷ luật. Tự đi kèm trách nhiệm mang lại trưởng thành.",
    6: "Tránh bao bọc quá mức. Tin tưởng để người thân tự lựa chọn con đường của họ.",
    7: "Vượt qua sự cô lập, chia sẻ tri thức với thế giới. Trí tuệ chỉ tồn tại trong sự chia sẻ.",
    8: "Cân bằng tham vọng với đạo đức và hào phóng. Thành công vì lợi ích người khác là thành công đích thực.",
    9: "Vượt qua sự buông bỏ quá mức. Học hoàn tất vòng đời không cảm giác tội lỗi, tin vào dòng chảy cuộc sống.",
}

VIB_VI = {
    1: "Sinh trong tần số 1. Lãnh đạo bẩm sinh, tiên phong, độc lập. Năng lượng khởi đầu và xuất phát. Can đảm đi những con đường chưa ai đi. Sinh ra để học lãnh đạo với khiêm nhường và phục vụ.",
    2: "Sinh trong tần số 2. Nhạy cảm, ngoại giao, hợp tác. Sức mạnh của bạn nằm trong đối tác và hòa hợp. Trực giác tinh tế. Sinh ra để học sự cân bằng giữa cho và nhận.",
    3: "Sinh trong tần số 3. Giao tiếp giỏi, sáng tạo, lạc quan. Niềm vui lan tỏa. Ngôn từ là công cụ mạnh nhất của bạn. Sinh ra để soi sáng thế giới qua nghệ thuật.",
    4: "Sinh trong tần số 4. Cần cù, kỷ luật, thực tế. Nền móng vững chắc kiến tạo sự an toàn đích thực. Sinh ra để hiểu rằng an toàn đích thực đến từ bên trong.",
    5: "Sinh trong tần số 5. Yêu tự do, đa tài, yêu phiêu lưu. Năng lượng tìm kiếm trải nghiệm và chuyển hóa. Sự ham hiểu biết thúc đẩy tâm hồn. Sinh ra để sống trọn vẹn cuộc đời.",
    6: "Sinh trong tần số 6. Yêu thương, có trách nhiệm, gắn bó gia đình. Sứ mệnh là chăm sóc và tạo hài hòa. Tình yêu là sức mạnh lớn nhất. Sinh ra để hiểu rằng tình yêu giải phóng.",
    7: "Sinh trong tần số 7. Thông tuệ, hướng nội, tâm linh. Tìm kiếm tri thức sâu xa. Sự tĩnh lặng là người thầy. Sinh ra để thấu hiểu những bí ẩn của tồn tại.",
    8: "Sinh trong tần số 8. Mạnh mẽ, thành đạt, thịnh vượng. Năng lượng thu hút sung túc. Sinh ra để kiến tạo. Sinh ra để hiểu rằng sức mạnh đích thực là phục vụ.",
    9: "Sinh trong tần số 9. Nhân đạo, hào phóng, trắc ẩn. Tâm hồn cổ xưa và trí tuệ. Sứ mệnh là phục vụ tập thể. Sinh ra để hoàn tất vòng luân hồi và dạy sự buông bỏ.",
    11: "Sinh trong tần số 11. Bậc thầy trực giác. Dẫn truyền năng lượng của những tầng cao hơn bằng trí tuệ và cảm hứng. Sự hiện diện từ tính. Sinh ra để cân bằng ánh sáng tâm linh và vững chân trên đất.",
    22: "Sinh trong tần số 22. Bậc thầy kiến tạo. Hiện thực hóa những ước mơ lớn nhất thành hiện thực cụ thể. Tầm nhìn thực tiễn. Kiến tạo vì nhân loại.",
}

# ============================================================
# CAMADA MULTILÍNGUE — obrigatoriamente DEPOIS de SIG/CAM/DES/VIB
#                                        e DEPOIS de *_EN
# ============================================================

EXPRESS_TXT["en"] = EXPRESS_TXT_EN
SIG_I18N = {"pt": SIG, "en": SIG_EN}
CAM_I18N = {"pt": CAM, "en": CAM_EN}
DES_I18N = {"pt": DES, "en": DES_EN}
VIB_I18N = {"pt": VIB, "en": VIB_EN}
EXPRESS_TXT["es"] = EXPRESS_TXT_ES
SIG_I18N["es"] = SIG_ES
CAM_I18N["es"] = CAM_ES
DES_I18N["es"] = DES_ES
VIB_I18N["es"] = VIB_ES
EXPRESS_TXT["fr"] = EXPRESS_TXT_FR
SIG_I18N["fr"] = SIG_FR
CAM_I18N["fr"] = CAM_FR
DES_I18N["fr"] = DES_FR
VIB_I18N["fr"] = VIB_FR
EXPRESS_TXT["de"] = EXPRESS_TXT_DE
SIG_I18N["de"] = SIG_DE
CAM_I18N["de"] = CAM_DE
DES_I18N["de"] = DES_DE
VIB_I18N["de"] = VIB_DE
EXPRESS_TXT["it"] = EXPRESS_TXT_IT
SIG_I18N["it"] = SIG_IT
CAM_I18N["it"] = CAM_IT
DES_I18N["it"] = DES_IT
VIB_I18N["it"] = VIB_IT
EXPRESS_TXT["ja"] = EXPRESS_TXT_JA
SIG_I18N["ja"] = SIG_JA
CAM_I18N["ja"] = CAM_JA
DES_I18N["ja"] = DES_JA
VIB_I18N["ja"] = VIB_JA
EXPRESS_TXT["zh"] = EXPRESS_TXT_ZH
SIG_I18N["zh"] = SIG_ZH
CAM_I18N["zh"] = CAM_ZH
DES_I18N["zh"] = DES_ZH
VIB_I18N["zh"] = VIB_ZH
EXPRESS_TXT["ru"] = EXPRESS_TXT_RU
SIG_I18N["ru"] = SIG_RU
CAM_I18N["ru"] = CAM_RU
DES_I18N["ru"] = DES_RU
VIB_I18N["ru"] = VIB_RU
EXPRESS_TXT["ar"] = EXPRESS_TXT_AR
SIG_I18N["ar"] = SIG_AR
CAM_I18N["ar"] = CAM_AR
DES_I18N["ar"] = DES_AR
VIB_I18N["ar"] = VIB_AR
EXPRESS_TXT["he"] = EXPRESS_TXT_HE
SIG_I18N["he"] = SIG_HE
CAM_I18N["he"] = CAM_HE
DES_I18N["he"] = DES_HE
VIB_I18N["he"] = VIB_HE
EXPRESS_TXT["id"] = EXPRESS_TXT_ID
SIG_I18N["id"] = SIG_ID
CAM_I18N["id"] = CAM_ID
DES_I18N["id"] = DES_ID
VIB_I18N["id"] = VIB_ID
EXPRESS_TXT["tr"] = EXPRESS_TXT_TR
SIG_I18N["tr"] = SIG_TR
CAM_I18N["tr"] = CAM_TR
DES_I18N["tr"] = DES_TR
VIB_I18N["tr"] = VIB_TR
EXPRESS_TXT["vi"] = EXPRESS_TXT_VI
SIG_I18N["vi"] = SIG_VI
CAM_I18N["vi"] = CAM_VI
DES_I18N["vi"] = DES_VI
VIB_I18N["vi"] = VIB_VI

# ============================================================
# FECHAMENTO DO EXPRESS_TXT: chaves pt + idiomas sem bloco próprio
# ============================================================
# O bloco PT é o dicionário principal, então precisa ser registrado em "pt".
EXPRESS_TXT.setdefault("pt", EXPRESS_TXT)

# Idiomas sem bloco próprio caem no inglês (rede de segurança).
# Com os 14 blocos concluídos, a tupla está vazia — o loop não executa.
for _lang_sem_bloco in ():
    if _lang_sem_bloco not in EXPRESS_TXT:
        EXPRESS_TXT[_lang_sem_bloco] = EXPRESS_TXT.get("en", EXPRESS_TXT)

# ===== Funções de acesso =====

def t(chave, lang):
    d = TRAD.get(lang, TRAD["pt"])
    return d.get(chave, TRAD["pt"].get(chave, chave))

# ============================================================
# CAMADA MULTILÍNGUE
# Os dicionários PT (SIG, CAM, DES, VIB) são a fonte.
# Os _I18N começam só com "pt" e recebem os 13 idiomas
# incrementalmente — nada quebra enquanto traduz.
# ORDEM OBRIGATÓRIA: esta seção vem DEPOIS de SIG, CAM, DES, VIB.
# ============================================================

# ===== Funções de acesso =====

def get_sig(n, lang="pt"):
    """Express: 4 campos curtos, sem aprofundamento."""
    d = EXPRESS_TXT.get(lang) or EXPRESS_TXT["pt"]
    return d.get(n) or (t("nenhum", lang), "", "", "")

def get_sig_full(n, lang="pt"):
    """Completo: texto integral da Cissay, com metadados."""
    d = SIG_I18N.get(lang) or SIG_I18N["pt"]
    return d.get(n) or (t("nenhum", lang), "", "", "")

def get_cam(n, lang="pt"):
    """Descrição do Caminho de Vida (título + texto) no idioma pedido."""
    d = CAM_I18N.get(lang, CAM_I18N["pt"]).get(n)
    if not d:
        return ("", "")
    return d

def get_des(n, lang="pt"):
    """Interpretação do Desafio no idioma pedido."""
    return DES_I18N.get(lang, DES_I18N["pt"]).get(n, "")

def get_vib(n, lang="pt"):
    """Texto da Vibração do dia de nascimento no idioma pedido."""
    return VIB_I18N.get(lang, VIB_I18N["pt"]).get(n, "")
