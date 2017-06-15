# encoding:utf-8
import os

from modules.tables import OverviewTable

DATA_DIR = "tests/data/tables"



def test_parse_csv_file():
    FOREIGNBORN_FILES = [
        "foreignborn_201706.csv",
        "Manadsstatistik_ArbetssokandeRegArbetskraft_VW77FYJZZ5C3V15.csv",
        "foreignborn_old_format.csv"
        ]

    for file_name in FOREIGNBORN_FILES:
        file_path = os.path.join(DATA_DIR, file_name)
        table = OverviewTable()\
            .parse_downloaded_file(file_path)

        _validate_foreignborn_table(table)

    ALL_FILES = [
        "all_201706.csv",
        #"foreignborn_old_format.csv"
        ]

    for file_name in ALL_FILES:
        file_path = os.path.join(DATA_DIR, file_name)
        table = OverviewTable()\
            .parse_downloaded_file(file_path)

        _validate_all_table(table)


def _validate_foreignborn_table(table):
    for row in table:
        assert row["Region"] in ALLOWED_REGIONS
        assert row[u"Utrikesfödda"] == "Ja"
        assert row[u"Län"] == "Samtliga"
        assert row[u"Ålder"] == "16-64"
        assert row[u"Kön"] == u"Kvinnor och män"
    assert len(table) == 312

def _validate_all_table(table):
    for row in table:
        assert row["Region"] in ALLOWED_REGIONS
        assert row[u"Utrikesfödda"] == ""
        assert row[u"Län"] == "Samtliga"
        assert row[u"Ålder"] == "16-64"
        assert row[u"Kön"] == u"Kvinnor och män"
    assert len(table) == 312


ALLOWED_REGIONS = [
u"Riket",
u"Stockholms län",
u"Upplands Väsby",
u"Vallentuna",
u"Österåker",
u"Värmdö",
u"Järfälla",
u"Ekerö",
u"Huddinge",
u"Botkyrka",
u"Salem",
u"Haninge",
u"Tyresö",
u"Upplands-Bro",
u"Nykvarn",
u"Täby",
u"Danderyd",
u"Sollentuna",
u"Stockholm",
u"Södertälje",
u"Nacka",
u"Sundbyberg",
u"Solna",
u"Lidingö",
u"Vaxholm",
u"Norrtälje",
u"Sigtuna",
u"Nynäshamn",
u"Uppsala län",
u"Håbo",
u"Älvkarleby",
u"Knivsta",
u"Heby",
u"Tierp",
u"Uppsala",
u"Enköping",
u"Östhammar",
u"Södermanlands län",
u"Vingåker",
u"Gnesta",
u"Nyköping",
u"Oxelösund",
u"Flen",
u"Katrineholm",
u"Eskilstuna",
u"Strängnäs",
u"Trosa",
u"Östergötlands län",
u"Ödeshög",
u"Ydre",
u"Kinda",
u"Boxholm",
u"Åtvidaberg",
u"Finspång",
u"Valdemarsvik",
u"Linköping",
u"Norrköping",
u"Söderköping",
u"Motala",
u"Vadstena",
u"Mjölby",
u"Jönköpings län",
u"Aneby",
u"Gnosjö",
u"Mullsjö",
u"Habo",
u"Gislaved",
u"Vaggeryd",
u"Jönköping",
u"Nässjö",
u"Värnamo",
u"Sävsjö",
u"Vetlanda",
u"Eksjö",
u"Tranås",
u"Kronobergs län",
u"Uppvidinge",
u"Lessebo",
u"Tingsryd",
u"Alvesta",
u"Älmhult",
u"Markaryd",
u"Växjö",
u"Ljungby",
u"Kalmar län",
u"Högsby",
u"Torsås",
u"Mörbylånga",
u"Hultsfred",
u"Mönsterås",
u"Emmaboda",
u"Kalmar",
u"Nybro",
u"Oskarshamn",
u"Västervik",
u"Vimmerby",
u"Borgholm",
u"Gotlands län",
u"Gotland",
u"Blekinge län",
u"Olofström",
u"Karlskrona",
u"Ronneby",
u"Karlshamn",
u"Sölvesborg",
u"Skåne län",
u"Svalöv",
u"Staffanstorp",
u"Burlöv",
u"Vellinge",
u"Östra Göinge",
u"Örkelljunga",
u"Bjuv",
u"Kävlinge",
u"Lomma",
u"Svedala",
u"Skurup",
u"Sjöbo",
u"Hörby",
u"Höör",
u"Tomelilla",
u"Bromölla",
u"Osby",
u"Perstorp",
u"Klippan",
u"Åstorp",
u"Båstad",
u"Malmö",
u"Lund",
u"Landskrona",
u"Helsingborg",
u"Höganäs",
u"Eslöv",
u"Ystad",
u"Trelleborg",
u"Kristianstad",
u"Simrishamn",
u"Ängelholm",
u"Hässleholm",
u"Hallands län",
u"Hylte",
u"Halmstad",
u"Laholm",
u"Falkenberg",
u"Varberg",
u"Kungsbacka",
u"Västra Götalands län",
u"Härryda",
u"Partille",
u"Öckerö",
u"Stenungsund",
u"Tjörn",
u"Orust",
u"Sotenäs",
u"Munkedal",
u"Tanum",
u"Dals-Ed",
u"Färgelanda",
u"Ale",
u"Lerum",
u"Vårgårda",
u"Bollebygd",
u"Grästorp",
u"Essunga",
u"Karlsborg",
u"Gullspång",
u"Tranemo",
u"Bengtsfors",
u"Mellerud",
u"Lilla Edet",
u"Mark",
u"Svenljunga",
u"Herrljunga",
u"Vara",
u"Götene",
u"Tibro",
u"Töreboda",
u"Göteborg",
u"Mölndal",
u"Kungälv",
u"Lysekil",
u"Uddevalla",
u"Strömstad",
u"Vänersborg",
u"Trollhättan",
u"Alingsås",
u"Borås",
u"Ulricehamn",
u"Åmål",
u"Mariestad",
u"Lidköping",
u"Skara",
u"Skövde",
u"Hjo",
u"Tidaholm",
u"Falköping",
u"Värmlands län",
u"Kil",
u"Eda",
u"Torsby",
u"Storfors",
u"Hammarö",
u"Munkfors",
u"Forshaga",
u"Grums",
u"Årjäng",
u"Sunne",
u"Karlstad",
u"Kristinehamn",
u"Filipstad",
u"Hagfors",
u"Arvika",
u"Säffle",
u"Örebro län",
u"Lekeberg",
u"Laxå",
u"Hallsberg",
u"Degerfors",
u"Hällefors",
u"Ljusnarsberg",
u"Örebro",
u"Kumla",
u"Askersund",
u"Karlskoga",
u"Nora",
u"Lindesberg",
u"Västmanlands län",
u"Skinnskatteberg",
u"Surahammar",
u"Kungsör",
u"Hallstahammar",
u"Norberg",
u"Västerås",
u"Sala",
u"Fagersta",
u"Köping",
u"Arboga",
u"Dalarnas län",
u"Vansbro",
u"Malung-Sälen",
u"Gagnef",
u"Leksand",
u"Rättvik",
u"Orsa",
u"Älvdalen",
u"Smedjebacken",
u"Mora",
u"Falun",
u"Borlänge",
u"Säter",
u"Hedemora",
u"Avesta",
u"Ludvika",
u"Gävleborgs län",
u"Ockelbo",
u"Hofors",
u"Ovanåker",
u"Nordanstig",
u"Ljusdal",
u"Gävle",
u"Sandviken",
u"Söderhamn",
u"Bollnäs",
u"Hudiksvall",
u"Västernorrlands län",
u"Ånge",
u"Timrå",
u"Härnösand",
u"Sundsvall",
u"Kramfors",
u"Sollefteå",
u"Örnsköldsvik",
u"Jämtlands län",
u"Ragunda",
u"Bräcke",
u"Krokom",
u"Strömsund",
u"Åre",
u"Berg",
u"Härjedalen",
u"Östersund",
u"Västerbottens län",
u"Nordmaling",
u"Bjurholm",
u"Vindeln",
u"Robertsfors",
u"Norsjö",
u"Malå",
u"Storuman",
u"Sorsele",
u"Dorotea",
u"Vännäs",
u"Vilhelmina",
u"Åsele",
u"Umeå",
u"Lycksele",
u"Skellefteå",
u"Norrbottens län",
u"Arvidsjaur",
u"Arjeplog",
u"Jokkmokk",
u"Överkalix",
u"Kalix",
u"Övertorneå",
u"Pajala",
u"Gällivare",
u"Älvsbyn",
u"Luleå",
u"Piteå",
u"Boden",
u"Haparanda",
u"Kiruna",
]
