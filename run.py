from modules.ams import AMS
from modules.tables import OverviewTable
from modules.utils import file_exists, merge_csv_files
from modules.interface import Interface

from dateutil import rrule
from datetime import datetime, timedelta

cmd_args = [
    {
        'short': "-o", "long": "--output",
        'dest': "output",
        'type': str,
        'help': """path to output file (csv) if you want to store results""",
        'required': False
    },
    {
        'short': "-f", "long": "--from",
        'dest': "date_start",
        'type': str,
        'help': """start date (2016-01-01)""",
        'required': True
    },
    {
        'short': "-t", "long": "--to",
        'dest': "date_end",
        'type': str,
        'help': """end date (2016-01-01)""",
        'required': False
    },
    {
        'short': "-s", "long": "--slow",
        'dest': "slow",
        'type': str,
        'help': """use the --slow flag if connection is slow, adds extra sleep time""",
        'required': False
    },

]
ui = Interface("AMS Scraper",
               "For getting data from AMS website",
               commandline_args=cmd_args)

if ui.args.slow:
    sleep = 3
else:
    sleep = 1.5

scraper = AMS(sleep=sleep)

date_start = datetime.strptime(ui.args.date_start, "%Y-%m-%d")
if ui.args.date_end:
    date_end = datetime.strptime(ui.args.date_end, "%Y-%m-%d")
else:
    date_end = datetime.now()


#data = scraper.get_overview(month=4,year=2016)
#data = OverviewTable().parse_downloaded_file("tmp/Manadsstatistik_ArbetssokandeBefolkning_4TK9XC05T43FI4G.csv")
#data.save_as("data/overview-2016-04.csv")

files = []

for dt in rrule.rrule(rrule.MONTHLY, dtstart=date_start, until=date_end):
    file_name = "tmp/raw-%s-%02d.csv" % (dt.year, dt.month)

    if file_exists(file_name):
        print "%s already exists" % file_name
    else: 
        data = scraper.get_overview(year=dt.year, month=dt.month)
        data += scraper.get_overview(year=dt.year, month=dt.month, youth_only=True)
        data += scraper.get_overview(year=dt.year, month=dt.month, foreign_only=True)
        data += scraper.get_overview(year=dt.year, month=dt.month, foreign_only=True, youth_only=True)
        data.save_as(file_name)

    files.append(file_name)

if ui.args.output:
    merge_csv_files(files).save_as(ui.args.output)
