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
# ===== SEÇÕES DOS PDFS (12 IDIOMAS) =====
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

# ===== BOAS-VINDAS, PERIODOS E CABEÇALHOS DE REALIZAÇÕES (12 IDIOMAS) =====
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
