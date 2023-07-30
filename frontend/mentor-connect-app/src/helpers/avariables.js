export const HOST_URL = "http://127.0.0.1:8000/";
export const FE_URL = "http://127.0.0.1:3000/";

export const WS_HOST_URL = "ws://127.0.0.1:8000/";

export const years = (s, e) => {
  return [Array.from({ length: e - s + 1 }, (_, index) => s + index)][0];
};

export const EDUCATION_LEVEL = [
  ["bachelors_degree", "תואר ראשון"],
  ["masters_degree", "תואר שני"],
  ["doctorate", "דוקטורט"],
  ["teaching_certificate", "תעודת הוראה"],
  ["diploma", "לימודי תעודה"],
  ["high_school", "תיכון"],
];

export const EXPERIENCE_WITH = [
  { value: "adhd", name: "קשב וריכוז" },
  { value: "teaching", name: "הוראה" },
];

export const CITIES_CHOICES = [
  { value: "Jerusalem", name: "ירושלים" },
  { value: "Tel Aviv-Yafo", name: "תל אביב-יפו" },
  { value: "Haifa", name: "חיפה" },
  { value: "Rishon LeZion", name: "ראשון לציון" },
  { value: "Petah Tikva", name: "פתח תקווה" },
  { value: "Ashdod", name: "אשדוד" },
  { value: "Netanya", name: "נתניה" },
  { value: "Be'er Sheva", name: "באר שבע" },
  { value: "Bnei Brak", name: "בני ברק" },
  { value: "Holon", name: "חולון" },
  { value: "Ramat Gan", name: "רמת גן" },
  { value: "Ashkelon", name: "אשקלון" },
  { value: "Rehovot", name: "רחובות" },
  { value: "Beit Shemesh", name: "בית שמש" },
  { value: "Bat Yam", name: "בת ים" },
  { value: "Kfar Saba", name: "כפר סבא" },
  { value: "Herzliya", name: "הרצליה" },
  { value: "Hadera", name: "חדרה" },
  { value: "Modi'in-Maccabim-Re'ut", name: "מודיעין- מכבים- רעות" },
  { value: "Lod", name: "לוד" },
  { value: "Modi'in Illit", name: "מודיעין עילית" },
  { value: "Nazareth", name: "נצרת" },
  { value: "Ramla", name: "רמלה" },
  { value: "Ra'anana", name: "רעננה" },
  { value: "Rahat", name: "רהט" },
  { value: "Rosh HaAyin", name: "ראש העין" },
  { value: "Hod HaSharon", name: "הוד השרון" },
  { value: "Beitar Illit", name: "ביתר עילית" },
  { value: "Givatayim", name: "גבעתיים" },
  { value: "Kiryat Ata", name: "קריית אתא" },
  { value: "Nahariya", name: "נהריה" },
  { value: "Kiryat Gat", name: "קריית גת" },
  { value: "Umm al-Fahm", name: "אום אל-פחם" },
  { value: "Afula", name: "עפולה" },
  { value: "Eilat", name: "אילת" },
  { value: "Nes Ziona", name: "נס ציונה" },
  { value: "Acre", name: "עכו" },
  { value: "Yavne", name: "יבנה" },
  { value: "El'ad", name: "אלעד" },
  { value: "Ramat HaSharon", name: "רמת השרון" },
  { value: "Karmiel", name: "כרמיאל" },
  { value: "Tiberias", name: "טבריה" },
  { value: "Kiryat Motzkin", name: "קריית מוצקין" },
  { value: "Tayibe", name: "טייבה" },
  { value: "Shefaram", name: "שפרעם" },
  { value: "Nof HaGalil", name: "נוף הגליל" },
  { value: "Kiryat Bialik", name: "קריית ביאליק" },
  { value: "Kiryat Ono", name: "קריית אונו" },
  { value: "Kiryat Yam", name: "קריית ים" },
  { value: "Netivot", name: "נתיבות" },
  { value: "Ma'ale Adumim", name: "מעלה אדומים" },
  { value: "Or Yehuda", name: "אור יהודה" },
  { value: "Zefat", name: "צפת" },
  { value: "Dimona", name: "דימונה" },
  { value: "Tamra", name: "טמרה" },
  { value: "Ofakim", name: "אופקים" },
  { value: "Sakhnin", name: "סח'נין" },
  { value: "Baqa al-Gharbiyye", name: "באקה אל-גרבייה" },
  { value: "Yehud-Monosson", name: "יהוד-מונוסון" },
  { value: "Sderot", name: "שדרות" },
  { value: "Be'er Ya'akov", name: "באר יעקב" },
  { value: "Giv'at Shmuel", name: "גבעת שמואל" },
  { value: "Arad", name: "ערד" },
  { value: "Tira", name: "טירה" },
  { value: "Arraba", name: "עראבה" },
  { value: "Kfar Yona", name: "כפר יונה" },
  { value: "Migdal HaEmek", name: "מגדל העמק" },
  { value: "Kiryat Malakhi", name: "קריית מלאכי" },
  { value: "Kafr Qasim", name: "כפר קאסם" },
  { value: "Tirat Carmel", name: "טירת כרמל" },
  { value: "Yokneam Illit", name: "יקנעם עילית" },
  { value: "Nesher", name: "נשר" },
  { value: "Qalansawe", name: "קלנסווה" },
  { value: "Kiryat Shmona", name: "קריית שמונה" },
  { value: "Ma'alot-Tarshiha", name: "מעלות- תרשיחא" },
  { value: "Ariel", name: "אריאל" },
  { value: "Or Akiva", name: "אור עקיבא" },
  { value: "Beit She'an", name: "בית שאן" },
];
