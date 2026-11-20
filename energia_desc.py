# -*- coding: utf-8 -*-
"""A1ELOS - o que cada energia significa, em 14 idiomas."""

DESC = {
 "pt": {1:"Lideranca e independencia",2:"Cooperacao e afeto",3:"Criatividade e alegria",
        4:"Lealdade e estrutura",5:"Liberdade e curiosidade",6:"Cuidado e vinculo familiar",
        7:"Intuicao e serenidade",8:"Forca e presenca",9:"Sociabilidade e docura"},
 "en": {1:"Leadership and independence",2:"Cooperation and affection",3:"Creativity and joy",
        4:"Loyalty and structure",5:"Freedom and curiosity",6:"Care and family bond",
        7:"Intuition and serenity",8:"Strength and presence",9:"Sociability and gentleness"},
 "es": {1:"Liderazgo e independencia",2:"Cooperacion y afecto",3:"Creatividad y alegria",
        4:"Lealtad y estructura",5:"Libertad y curiosidad",6:"Cuidado y vinculo familiar",
        7:"Intuicion y serenidad",8:"Fuerza y presencia",9:"Sociabilidad y dulzura"},
 "it": {1:"Leadership e indipendenza",2:"Cooperazione e affetto",3:"Creativita e gioia",
        4:"Lealta e struttura",5:"Liberta e curiosita",6:"Cura e legame familiare",
        7:"Intuito e serenita",8:"Forza e presenza",9:"Socievolezza e dolcezza"},
 "fr": {1:"Leadership et independance",2:"Cooperation et affection",3:"Creativite et joie",
        4:"Loyaute et structure",5:"Liberte et curiosite",6:"Soin et lien familial",
        7:"Intuition et serenite",8:"Force et presence",9:"Sociabilite et douceur"},
 "de": {1:"Fuehrung und Unabhaengigkeit",2:"Kooperation und Zuneigung",3:"Kreativitaet und Freude",
        4:"Loyalitaet und Struktur",5:"Freiheit und Neugier",6:"Fuersorge und Familienbindung",
        7:"Intuition und Gelassenheit",8:"Staerke und Praesenz",9:"Geselligkeit und Sanftheit"},
 "ja": {1:"指導力と自立",2:"協調と愛情",3:"創造性と喜び",4:"忠誠と安定",5:"自由と好奇心",
        6:"思いやりと家族の絆",7:"直感と穏やかさ",8:"力強さと存在感",9:"社交性と優しさ"},
 "zh": {1:"领导力与独立",2:"合作与亲情",3:"创造力与快乐",4:"忠诚与稳定",5:"自由与好奇",
        6:"关怀与家庭纽带",7:"直觉与平和",8:"力量与气场",9:"亲和与温柔"},
 "ru": {1:"Лидерство и независимость",2:"Сотрудничество и привязанность",3:"Творчество и радость",
        4:"Верность и устойчивость",5:"Свобода и любопытство",6:"Забота и семейная связь",
        7:"Интуиция и спокойствие",8:"Сила и присутствие",9:"Общительность и мягкость"},
 "id": {1:"Kepemimpinan dan kemandirian",2:"Kerja sama dan kasih sayang",3:"Kreativitas dan keceriaan",
        4:"Kesetiaan dan keteraturan",5:"Kebebasan dan rasa ingin tahu",6:"Kepedulian dan ikatan keluarga",
        7:"Intuisi dan ketenangan",8:"Kekuatan dan kehadiran",9:"Keramahan dan kelembutan"},
 "tr": {1:"Liderlik ve bagimsizlik",2:"Isbirligi ve sevgi",3:"Yaraticilik ve nese",
        4:"Sadakat ve duzen",5:"Ozgurluk ve merak",6:"Sefkat ve aile bagi",
        7:"Sezgi ve huzur",8:"Guc ve varlik",9:"Sosyallik ve yumusaklik"},
 "vi": {1:"Lanh dao va doc lap",2:"Hop tac va tinh cam",3:"Sang tao va niem vui",
        4:"Trung thanh va on dinh",5:"Tu do va to mo",6:"Cham soc va gan ket gia dinh",
        7:"Truc giac va thanh than",8:"Suc manh va hien dien",9:"Hoa dong va diu dang"},
 "he": {1:"מנהיגות ועצמאות",2:"שיתוף פעולה וחיבה",3:"יצירתיות ושמחה",4:"נאמנות ויציבות",
        5:"חופש וסקרנות",6:"אכפתיות וקשר משפחתי",7:"אינטואיציה ושלווה",8:"עוצמה ונוכחות",9:"חברותיות ועדינות"},
 "ar": {1:"القيادة والاستقلال",2:"التعاون والمودة",3:"الإبداع والفرح",4:"الوفاء والاستقرار",
        5:"الحرية والفضول",6:"الرعاية والرابط الأسري",7:"الحدس والسكينة",8:"القوة والحضور",9:"الاجتماعية واللطف"},
}


def descrever(energia, lang="pt"):
    try:
        n = int(energia)
    except Exception:
        return ""
    return (DESC.get(lang) or DESC["pt"]).get(n, "")
