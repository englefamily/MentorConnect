<<<<<<< HEAD
# Generated by Django 4.2.1 on 2023-06-01 22:30
=======
# Generated by Django 4.2.1 on 2023-05-30 23:22
>>>>>>> d53a25a (models base)

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mentorconnect.models
<<<<<<< HEAD
import multiselectfield.db.fields
=======
>>>>>>> d53a25a (models base)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', mentorconnect.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='Topic',
=======
            name='LearningSubTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_topic_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'sub_topic',
            },
        ),
        migrations.CreateModel(
            name='LearningTopic',
>>>>>>> d53a25a (models base)
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'topic',
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='SubTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_topic_name', models.CharField(max_length=50)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='courses', to='mentorconnect.topic')),
            ],
            options={
                'db_table': 'sub_topic',
            },
        ),
        migrations.CreateModel(
=======
>>>>>>> d53a25a (models base)
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
<<<<<<< HEAD
                ('phone_num', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('year_of_birth', models.CharField(choices=[('1933', '1933'), ('1934', '1934'), ('1935', '1935'), ('1936', '1936'), ('1937', '1937'), ('1938', '1938'), ('1939', '1939'), ('1940', '1940'), ('1941', '1941'), ('1942', '1942'), ('1943', '1943'), ('1944', '1944'), ('1945', '1945'), ('1946', '1946'), ('1947', '1947'), ('1948', '1948'), ('1949', '1949'), ('1950', '1950'), ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'), ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'), ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'), ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006')], max_length=4)),
                ('short_description', models.CharField(max_length=256)),
                ('sub_topics', models.ManyToManyField(blank=True, related_name='students', to='mentorconnect.subtopic')),
=======
                ('year_of_birth', models.CharField(choices=[('1933', '1933'), ('1934', '1934'), ('1935', '1935'), ('1936', '1936'), ('1937', '1937'), ('1938', '1938'), ('1939', '1939'), ('1940', '1940'), ('1941', '1941'), ('1942', '1942'), ('1943', '1943'), ('1944', '1944'), ('1945', '1945'), ('1946', '1946'), ('1947', '1947'), ('1948', '1948'), ('1949', '1949'), ('1950', '1950'), ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'), ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'), ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'), ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006')], max_length=4)),
                ('address_city', models.CharField(choices=[('Jerusalem', 'ירושלים'), ('Tel Aviv-Yafo', 'תל אביב-יפו'), ('Haifa', 'חיפה'), ('Rishon LeZion', 'ראשון לציון'), ('Petah Tikva', 'פתח תקווה'), ('Ashdod', 'אשדוד'), ('Netanya', 'נתניה'), ("Be'er Sheva", 'באר שבע'), ('Bnei Brak', 'בני ברק'), ('Holon', 'חולון'), ('Ramat Gan', 'רמת גן'), ('Ashkelon', 'אשקלון'), ('Rehovot', 'רחובות'), ('Beit Shemesh', 'בית שמש'), ('Bat Yam', 'בת ים'), ('Kfar Saba', 'כפר סבא'), ('Herzliya', 'הרצליה'), ('Hadera', 'חדרה'), ("Modi'in-Maccabim-Re'ut", 'מודיעין- מכבים- רעות'), ('Lod', 'לוד'), ("Modi'in Illit", 'מודיעין עילית'), ('Nazareth', 'נצרת'), ('Ramla', 'רמלה'), ("Ra'anana", 'רעננה'), ('Rahat', 'רהט'), ('Rosh HaAyin', 'ראש העין'), ('Hod HaSharon', 'הוד השרון'), ('Beitar Illit', 'ביתר עילית'), ('Givatayim', 'גבעתיים'), ('Kiryat Ata', 'קריית אתא'), ('Nahariya', 'נהריה'), ('Kiryat Gat', 'קריית גת'), ('Umm al-Fahm', 'אום אל-פחם'), ('Afula', 'עפולה'), ('Eilat', 'אילת'), ('Nes Ziona', 'נס ציונה'), ('Acre', 'עכו'), ('Yavne', 'יבנה'), ("El'ad", 'אלעד'), ('Ramat HaSharon', 'רמת השרון'), ('Karmiel', 'כרמיאל'), ('Tiberias', 'טבריה'), ('Kiryat Motzkin', 'קריית מוצקין'), ('Tayibe', 'טייבה'), ('Shefaram', 'שפרעם'), ('Nof HaGalil', 'נוף הגליל'), ('Kiryat Bialik', 'קריית ביאליק'), ('Kiryat Ono', 'קריית אונו'), ('Kiryat Yam', 'קריית ים'), ('Netivot', 'נתיבות'), ("Ma'ale Adumim", 'מעלה אדומים'), ('Or Yehuda', 'אור יהודה'), ('Zefat', 'צפת'), ('Dimona', 'דימונה'), ('Tamra', 'טמרה'), ('Ofakim', 'אופקים'), ('Sakhnin', "סח'נין"), ('Baqa al-Gharbiyye', 'באקה אל-גרבייה'), ('Yehud-Monosson', 'יהוד-מונוסון'), ('Sderot', 'שדרות'), ("Be'er Ya'akov", 'באר יעקב'), ("Giv'at Shmuel", 'גבעת שמואל'), ('Arad', 'ערד'), ('Tira', 'טירה'), ('Arraba', 'עראבה'), ('Kfar Yona', 'כפר יונה'), ('Migdal HaEmek', 'מגדל העמק'), ('Kiryat Malakhi', 'קריית מלאכי'), ('Kafr Qasim', 'כפר קאסם'), ('Tirat Carmel', 'טירת כרמל'), ('Yokneam Illit', 'יקנעם עילית'), ('Nesher', 'נשר'), ('Qalansawe', 'קלנסווה'), ('Kiryat Shmona', 'קריית שמונה'), ("Ma'alot-Tarshiha", 'מעלות- תרשיחא'), ('Ariel', 'אריאל'), ('Or Akiva', 'אור עקיבא'), ("Beit She'an", 'בית שאן')], max_length=128)),
                ('short_description', models.CharField(max_length=256)),
                ('sub_topics', models.ManyToManyField(blank=True, related_name='students', to='mentorconnect.learningsubtopic')),
>>>>>>> d53a25a (models base)
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=128)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
<<<<<<< HEAD
                ('phone_num', models.CharField(max_length=10, unique=True)),
                ('education', models.CharField(choices=[('bachelors_degree', 'תואר ראשון'), ('masters_degree', 'תואר שני'), ('doctorate', 'דוקטורט'), ('teaching_certificate', 'תעודת הוראה'), ('diploma', 'לימודי תעודה'), ('high_school', 'תיכון')], max_length=30)),
                ('education_start_year', models.CharField(choices=[('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023')], max_length=4)),
                ('education_completion_year', models.CharField(choices=[('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], max_length=4)),
                ('year_of_birth', models.CharField(choices=[('1933', '1933'), ('1934', '1934'), ('1935', '1935'), ('1936', '1936'), ('1937', '1937'), ('1938', '1938'), ('1939', '1939'), ('1940', '1940'), ('1941', '1941'), ('1942', '1942'), ('1943', '1943'), ('1944', '1944'), ('1945', '1945'), ('1946', '1946'), ('1947', '1947'), ('1948', '1948'), ('1949', '1949'), ('1950', '1950'), ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'), ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'), ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'), ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006')], max_length=4)),
                ('address_city', models.CharField(choices=[('Jerusalem', 'ירושלים'), ('Tel Aviv-Yafo', 'תל אביב-יפו'), ('Haifa', 'חיפה'), ('Rishon LeZion', 'ראשון לציון'), ('Petah Tikva', 'פתח תקווה'), ('Ashdod', 'אשדוד'), ('Netanya', 'נתניה'), ("Be'er Sheva", 'באר שבע'), ('Bnei Brak', 'בני ברק'), ('Holon', 'חולון'), ('Ramat Gan', 'רמת גן'), ('Ashkelon', 'אשקלון'), ('Rehovot', 'רחובות'), ('Beit Shemesh', 'בית שמש'), ('Bat Yam', 'בת ים'), ('Kfar Saba', 'כפר סבא'), ('Herzliya', 'הרצליה'), ('Hadera', 'חדרה'), ("Modi'in-Maccabim-Re'ut", 'מודיעין- מכבים- רעות'), ('Lod', 'לוד'), ("Modi'in Illit", 'מודיעין עילית'), ('Nazareth', 'נצרת'), ('Ramla', 'רמלה'), ("Ra'anana", 'רעננה'), ('Rahat', 'רהט'), ('Rosh HaAyin', 'ראש העין'), ('Hod HaSharon', 'הוד השרון'), ('Beitar Illit', 'ביתר עילית'), ('Givatayim', 'גבעתיים'), ('Kiryat Ata', 'קריית אתא'), ('Nahariya', 'נהריה'), ('Kiryat Gat', 'קריית גת'), ('Umm al-Fahm', 'אום אל-פחם'), ('Afula', 'עפולה'), ('Eilat', 'אילת'), ('Nes Ziona', 'נס ציונה'), ('Acre', 'עכו'), ('Yavne', 'יבנה'), ("El'ad", 'אלעד'), ('Ramat HaSharon', 'רמת השרון'), ('Karmiel', 'כרמיאל'), ('Tiberias', 'טבריה'), ('Kiryat Motzkin', 'קריית מוצקין'), ('Tayibe', 'טייבה'), ('Shefaram', 'שפרעם'), ('Nof HaGalil', 'נוף הגליל'), ('Kiryat Bialik', 'קריית ביאליק'), ('Kiryat Ono', 'קריית אונו'), ('Kiryat Yam', 'קריית ים'), ('Netivot', 'נתיבות'), ("Ma'ale Adumim", 'מעלה אדומים'), ('Or Yehuda', 'אור יהודה'), ('Zefat', 'צפת'), ('Dimona', 'דימונה'), ('Tamra', 'טמרה'), ('Ofakim', 'אופקים'), ('Sakhnin', "סח'נין"), ('Baqa al-Gharbiyye', 'באקה אל-גרבייה'), ('Yehud-Monosson', 'יהוד-מונוסון'), ('Sderot', 'שדרות'), ("Be'er Ya'akov", 'באר יעקב'), ("Giv'at Shmuel", 'גבעת שמואל'), ('Arad', 'ערד'), ('Tira', 'טירה'), ('Arraba', 'עראבה'), ('Kfar Yona', 'כפר יונה'), ('Migdal HaEmek', 'מגדל העמק'), ('Kiryat Malakhi', 'קריית מלאכי'), ('Kafr Qasim', 'כפר קאסם'), ('Tirat Carmel', 'טירת כרמל'), ('Yokneam Illit', 'יקנעם עילית'), ('Nesher', 'נשר'), ('Qalansawe', 'קלנסווה'), ('Kiryat Shmona', 'קריית שמונה'), ("Ma'alot-Tarshiha", 'מעלות- תרשיחא'), ('Ariel', 'אריאל'), ('Or Akiva', 'אור עקיבא'), ("Beit She'an", 'בית שאן')], max_length=128)),
                ('study_cities', multiselectfield.db.fields.MultiSelectField(choices=[('Jerusalem', 'ירושלים'), ('Tel Aviv-Yafo', 'תל אביב-יפו'), ('Haifa', 'חיפה'), ('Rishon LeZion', 'ראשון לציון'), ('Petah Tikva', 'פתח תקווה'), ('Ashdod', 'אשדוד'), ('Netanya', 'נתניה'), ("Be'er Sheva", 'באר שבע'), ('Bnei Brak', 'בני ברק'), ('Holon', 'חולון'), ('Ramat Gan', 'רמת גן'), ('Ashkelon', 'אשקלון'), ('Rehovot', 'רחובות'), ('Beit Shemesh', 'בית שמש'), ('Bat Yam', 'בת ים'), ('Kfar Saba', 'כפר סבא'), ('Herzliya', 'הרצליה'), ('Hadera', 'חדרה'), ("Modi'in-Maccabim-Re'ut", 'מודיעין- מכבים- רעות'), ('Lod', 'לוד'), ("Modi'in Illit", 'מודיעין עילית'), ('Nazareth', 'נצרת'), ('Ramla', 'רמלה'), ("Ra'anana", 'רעננה'), ('Rahat', 'רהט'), ('Rosh HaAyin', 'ראש העין'), ('Hod HaSharon', 'הוד השרון'), ('Beitar Illit', 'ביתר עילית'), ('Givatayim', 'גבעתיים'), ('Kiryat Ata', 'קריית אתא'), ('Nahariya', 'נהריה'), ('Kiryat Gat', 'קריית גת'), ('Umm al-Fahm', 'אום אל-פחם'), ('Afula', 'עפולה'), ('Eilat', 'אילת'), ('Nes Ziona', 'נס ציונה'), ('Acre', 'עכו'), ('Yavne', 'יבנה'), ("El'ad", 'אלעד'), ('Ramat HaSharon', 'רמת השרון'), ('Karmiel', 'כרמיאל'), ('Tiberias', 'טבריה'), ('Kiryat Motzkin', 'קריית מוצקין'), ('Tayibe', 'טייבה'), ('Shefaram', 'שפרעם'), ('Nof HaGalil', 'נוף הגליל'), ('Kiryat Bialik', 'קריית ביאליק'), ('Kiryat Ono', 'קריית אונו'), ('Kiryat Yam', 'קריית ים'), ('Netivot', 'נתיבות'), ("Ma'ale Adumim", 'מעלה אדומים'), ('Or Yehuda', 'אור יהודה'), ('Zefat', 'צפת'), ('Dimona', 'דימונה'), ('Tamra', 'טמרה'), ('Ofakim', 'אופקים'), ('Sakhnin', "סח'נין"), ('Baqa al-Gharbiyye', 'באקה אל-גרבייה'), ('Yehud-Monosson', 'יהוד-מונוסון'), ('Sderot', 'שדרות'), ("Be'er Ya'akov", 'באר יעקב'), ("Giv'at Shmuel", 'גבעת שמואל'), ('Arad', 'ערד'), ('Tira', 'טירה'), ('Arraba', 'עראבה'), ('Kfar Yona', 'כפר יונה'), ('Migdal HaEmek', 'מגדל העמק'), ('Kiryat Malakhi', 'קריית מלאכי'), ('Kafr Qasim', 'כפר קאסם'), ('Tirat Carmel', 'טירת כרמל'), ('Yokneam Illit', 'יקנעם עילית'), ('Nesher', 'נשר'), ('Qalansawe', 'קלנסווה'), ('Kiryat Shmona', 'קריית שמונה'), ("Ma'alot-Tarshiha", 'מעלות- תרשיחא'), ('Ariel', 'אריאל'), ('Or Akiva', 'אור עקיבא'), ("Beit She'an", 'בית שאן')], max_length=128)),
                ('short_description', models.CharField(max_length=256)),
                ('long_description', models.CharField(max_length=700)),
                ('cost_hour_min', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(300)])),
                ('cost_hour_max', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(300)])),
                ('teach_in', multiselectfield.db.fields.MultiSelectField(choices=[('online', 'online'), ('mentor_place', 'mentor_place'), ('student_place', 'student_place')], max_length=30)),
                ('experience_with', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('adhd', 'adhd'), ('teaching', 'teaching')], max_length=30, null=True)),
                ('group_teaching', models.BooleanField(default=False)),
                ('students', models.ManyToManyField(blank=True, related_name='mentors', to='mentorconnect.student')),
                ('sub_topics', models.ManyToManyField(related_name='mentors', to='mentorconnect.subtopic')),
=======
                ('year_of_birth', models.CharField(choices=[('1933', '1933'), ('1934', '1934'), ('1935', '1935'), ('1936', '1936'), ('1937', '1937'), ('1938', '1938'), ('1939', '1939'), ('1940', '1940'), ('1941', '1941'), ('1942', '1942'), ('1943', '1943'), ('1944', '1944'), ('1945', '1945'), ('1946', '1946'), ('1947', '1947'), ('1948', '1948'), ('1949', '1949'), ('1950', '1950'), ('1951', '1951'), ('1952', '1952'), ('1953', '1953'), ('1954', '1954'), ('1955', '1955'), ('1956', '1956'), ('1957', '1957'), ('1958', '1958'), ('1959', '1959'), ('1960', '1960'), ('1961', '1961'), ('1962', '1962'), ('1963', '1963'), ('1964', '1964'), ('1965', '1965'), ('1966', '1966'), ('1967', '1967'), ('1968', '1968'), ('1969', '1969'), ('1970', '1970'), ('1971', '1971'), ('1972', '1972'), ('1973', '1973'), ('1974', '1974'), ('1975', '1975'), ('1976', '1976'), ('1977', '1977'), ('1978', '1978'), ('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006')], max_length=4)),
                ('address_city', models.CharField(choices=[('Jerusalem', 'ירושלים'), ('Tel Aviv-Yafo', 'תל אביב-יפו'), ('Haifa', 'חיפה'), ('Rishon LeZion', 'ראשון לציון'), ('Petah Tikva', 'פתח תקווה'), ('Ashdod', 'אשדוד'), ('Netanya', 'נתניה'), ("Be'er Sheva", 'באר שבע'), ('Bnei Brak', 'בני ברק'), ('Holon', 'חולון'), ('Ramat Gan', 'רמת גן'), ('Ashkelon', 'אשקלון'), ('Rehovot', 'רחובות'), ('Beit Shemesh', 'בית שמש'), ('Bat Yam', 'בת ים'), ('Kfar Saba', 'כפר סבא'), ('Herzliya', 'הרצליה'), ('Hadera', 'חדרה'), ("Modi'in-Maccabim-Re'ut", 'מודיעין- מכבים- רעות'), ('Lod', 'לוד'), ("Modi'in Illit", 'מודיעין עילית'), ('Nazareth', 'נצרת'), ('Ramla', 'רמלה'), ("Ra'anana", 'רעננה'), ('Rahat', 'רהט'), ('Rosh HaAyin', 'ראש העין'), ('Hod HaSharon', 'הוד השרון'), ('Beitar Illit', 'ביתר עילית'), ('Givatayim', 'גבעתיים'), ('Kiryat Ata', 'קריית אתא'), ('Nahariya', 'נהריה'), ('Kiryat Gat', 'קריית גת'), ('Umm al-Fahm', 'אום אל-פחם'), ('Afula', 'עפולה'), ('Eilat', 'אילת'), ('Nes Ziona', 'נס ציונה'), ('Acre', 'עכו'), ('Yavne', 'יבנה'), ("El'ad", 'אלעד'), ('Ramat HaSharon', 'רמת השרון'), ('Karmiel', 'כרמיאל'), ('Tiberias', 'טבריה'), ('Kiryat Motzkin', 'קריית מוצקין'), ('Tayibe', 'טייבה'), ('Shefaram', 'שפרעם'), ('Nof HaGalil', 'נוף הגליל'), ('Kiryat Bialik', 'קריית ביאליק'), ('Kiryat Ono', 'קריית אונו'), ('Kiryat Yam', 'קריית ים'), ('Netivot', 'נתיבות'), ("Ma'ale Adumim", 'מעלה אדומים'), ('Or Yehuda', 'אור יהודה'), ('Zefat', 'צפת'), ('Dimona', 'דימונה'), ('Tamra', 'טמרה'), ('Ofakim', 'אופקים'), ('Sakhnin', "סח'נין"), ('Baqa al-Gharbiyye', 'באקה אל-גרבייה'), ('Yehud-Monosson', 'יהוד-מונוסון'), ('Sderot', 'שדרות'), ("Be'er Ya'akov", 'באר יעקב'), ("Giv'at Shmuel", 'גבעת שמואל'), ('Arad', 'ערד'), ('Tira', 'טירה'), ('Arraba', 'עראבה'), ('Kfar Yona', 'כפר יונה'), ('Migdal HaEmek', 'מגדל העמק'), ('Kiryat Malakhi', 'קריית מלאכי'), ('Kafr Qasim', 'כפר קאסם'), ('Tirat Carmel', 'טירת כרמל'), ('Yokneam Illit', 'יקנעם עילית'), ('Nesher', 'נשר'), ('Qalansawe', 'קלנסווה'), ('Kiryat Shmona', 'קריית שמונה'), ("Ma'alot-Tarshiha", 'מעלות- תרשיחא'), ('Ariel', 'אריאל'), ('Or Akiva', 'אור עקיבא'), ("Beit She'an", 'בית שאן')], max_length=128)),
                ('short_description', models.CharField(max_length=256)),
                ('long_description', models.CharField(max_length=700)),
                ('teach_online', models.BooleanField(default=False)),
                ('students', models.ManyToManyField(related_name='mentors', to='mentorconnect.student')),
                ('sub_topics', models.ManyToManyField(related_name='mentors', to='mentorconnect.learningsubtopic')),
>>>>>>> d53a25a (models base)
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='mentor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mentor',
            },
        ),
<<<<<<< HEAD
=======
        migrations.AddField(
            model_name='learningsubtopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='courses', to='mentorconnect.learningtopic'),
        ),
>>>>>>> d53a25a (models base)
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_content', models.CharField(max_length=228)),
                ('fb_stars', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
<<<<<<< HEAD
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='mentorconnect.mentor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='mentorconnect.student')),
                ('sub_topic', models.ManyToManyField(blank=True, related_name='feedbacks', to='mentorconnect.subtopic')),
=======
                ('sub_topic', models.CharField(blank=True, choices=[], max_length=100, null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='mentorconnect.mentor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='mentorconnect.student')),
>>>>>>> d53a25a (models base)
            ],
            options={
                'db_table': 'feedback',
            },
        ),
    ]