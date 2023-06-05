AGE_CHOICES = [(str(year), str(year)) for year in range(1933, 2007)]

EDUCATION_START = [(str(year), str(year)) for year in range(1983, 2024)]
EDUCATION_COMPLETE = [(str(year), str(year)) for year in range(1984, 2031)]

CITIES_CHOICES = [("Jerusalem", "ירושלים"),
          ("Tel Aviv-Yafo", "תל אביב-יפו"),
          ("Haifa", "חיפה"),
          ("Rishon LeZion", "ראשון לציון"),
          ("Petah Tikva", "פתח תקווה"),
          ("Ashdod", "אשדוד"),
          ("Netanya", "נתניה"),
          ("Be'er Sheva", "באר שבע"),
          ("Bnei Brak", "בני ברק"),
          ("Holon", "חולון"),
          ("Ramat Gan", "רמת גן"),
          ("Ashkelon", "אשקלון"),
          ("Rehovot", "רחובות"),
          ("Beit Shemesh", "בית שמש"),
          ("Bat Yam", "בת ים"),
          ("Kfar Saba", "כפר סבא"),
          ("Herzliya", "הרצליה"),
          ("Hadera", "חדרה"),
          ("Modi'in-Maccabim-Re'ut", "מודיעין- מכבים- רעות"),
          ("Lod", "לוד"),
          ("Modi'in Illit", "מודיעין עילית"),
          ("Nazareth", "נצרת"),
          ("Ramla", "רמלה"),
          ("Ra'anana", "רעננה"),
          ("Rahat", "רהט"),
          ("Rosh HaAyin", "ראש העין"),
          ("Hod HaSharon", "הוד השרון"),
          ("Beitar Illit", "ביתר עילית"),
          ("Givatayim", "גבעתיים"),
          ("Kiryat Ata", "קריית אתא"),
          ("Nahariya", "נהריה"),
          ("Kiryat Gat", "קריית גת"),
          ("Umm al-Fahm", "אום אל-פחם"),
          ("Afula", "עפולה"),
          ("Eilat", "אילת"),
          ("Nes Ziona", "נס ציונה"),
          ("Acre", "עכו"),
          ("Yavne", "יבנה"),
          ("El'ad", "אלעד"),
          ("Ramat HaSharon", "רמת השרון"),
          ("Karmiel", "כרמיאל"),
          ("Tiberias", "טבריה"),
          ("Kiryat Motzkin", "קריית מוצקין"),
          ("Tayibe", "טייבה"),
          ("Shefaram", "שפרעם"),
          ("Nof HaGalil", "נוף הגליל"),
          ("Kiryat Bialik", "קריית ביאליק"),
          ("Kiryat Ono", "קריית אונו"),
          ("Kiryat Yam", "קריית ים"),
          ("Netivot", "נתיבות"),
          ("Ma'ale Adumim", "מעלה אדומים"),
          ("Or Yehuda", "אור יהודה"),
          ("Zefat", "צפת"),
          ("Dimona", "דימונה"),
          ("Tamra", "טמרה"),
          ("Ofakim", "אופקים"),
          ("Sakhnin", "סח'נין"),
          ("Baqa al-Gharbiyye", "באקה אל-גרבייה"),
          ("Yehud-Monosson", "יהוד-מונוסון"),
          ("Sderot", "שדרות"),
          ("Be'er Ya'akov", "באר יעקב"),
          ("Giv'at Shmuel", "גבעת שמואל"),
          ("Arad", "ערד"),
          ("Tira", "טירה"),
          ("Arraba", "עראבה"),
          ("Kfar Yona", "כפר יונה"),
          ("Migdal HaEmek", "מגדל העמק"),
          ("Kiryat Malakhi", "קריית מלאכי"),
          ("Kafr Qasim", "כפר קאסם"),
          ("Tirat Carmel", "טירת כרמל"),
          ("Yokneam Illit", "יקנעם עילית"),
          ("Nesher", "נשר"),
          ("Qalansawe", "קלנסווה"),
          ("Kiryat Shmona", "קריית שמונה"),
          ("Ma'alot-Tarshiha", "מעלות- תרשיחא"),
          ("Ariel", "אריאל"),
          ("Or Akiva", "אור עקיבא"),
          ("Beit She'an", "בית שאן")]


EDUCATION_LEVEL = [
    ('bachelors_degree', 'תואר ראשון'),
    ('masters_degree', 'תואר שני'),
    ('doctorate', 'דוקטורט'),
    ('teaching_certificate', 'תעודת הוראה'),
    ('diploma', 'לימודי תעודה'),
    ('high_school', 'תיכון'),
]

TEACH_OPTIONS = [
    ('online', 'online'),
    ('mentor_place', 'mentor_place'),
    ('student_place', 'student_place'),
]






# api for mentor
# {
#     "user": {
#         "email": "test18@gmail.com",
#         "password": "123"
#     },
#     "gender": "female",
#     "first_name": "אורי",
#     "last_name": "גשר",
#     "phone_num": "0553001034",
#     "education": "bachelors_degree",
#     "education_start_year": "2010",
#     "education_completion_year": "2014",
#     "year_of_birth": "1987",
#     "address_city": "Jerusalem",
#     "study_cities": "Jerusalem",
#     "short_description": "מסביר נהדר",
#     "long_description": "מלמד פייתון וכו",
#     "cost_hour_min": 150,
#     "cost_hour_max": 201,
#     "teach_in": "online", // Provide
# teach_in as a
# string
# with comma - separated values
# "experience_with": "",
# "group_teaching": true,
# "sub_topics": [4],
# "students": [4]
# }


