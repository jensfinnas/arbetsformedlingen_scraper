from modules.ams import AMS
from modules.tables import OverviewTable
from modules.utils import file_exists, merge_csv_files
from modules.interface import Interface

from dateutil import rrule
from datetime import datetime, timedelta

cmd_args = [
    {
        'short': "-d", "long": "--dest",
        'dest': "folder",
        'type': str,
        'help': """path to output folder if you want to store results""",
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

if not ui.args.folder:
    folder = ""
else:
    folder = ui.args.folder
    if folder[-1] is not "/":
        folder += "/"

scraper = AMS(sleep=sleep)

date_start = datetime.strptime(ui.args.date_start, "%Y-%m-%d")
if ui.args.date_end:
    date_end = datetime.strptime(ui.args.date_end, "%Y-%m-%d")
else:
    date_end = datetime.now()


for dt in rrule.rrule(rrule.MONTHLY, dtstart=date_start, until=date_end):
    file_base = folder + "ams-%s-%02d" % (dt.year, dt.month)

    # Get all
    file_name = file_base + "-all.csv"
    if file_exists(file_name):
        print "%s already exists" % file_name
    else: 
        data = scraper.get_overview(year=dt.year, month=dt.month)
        data.save_as(file_name)
    
    # Get foreign born
    file_name = file_base + "-foreignborn.csv"
    if file_exists(file_name):
        print "%s already exists" % file_name
    else: 
        data = scraper.get_overview(year=dt.year, month=dt.month, foreign_only=True)
        data.save_as(file_name)

    # Get youth
    file_name = file_base + "-youth.csv"
    if file_exists(file_name):
        print "%s already exists" % file_name
    else: 
        data = scraper.get_overview(year=dt.year, month=dt.month, youth_only=True)
        data.save_as(file_name)

scraper.driver.close()
