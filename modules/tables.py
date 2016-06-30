# encoding: utf-8
from utils import partition
import csvkit as csv
import codecs
from itertools import islice
from errors import DataValidationError, EmptyFileError
import pdb

class DictList(list):
    def save_as(self, file_name):
        headers = self[0].keys()
        with open(file_name, 'wb') as output_file:
            print "Write %s row to %s" % (len(self), file_name)
            dict_writer = csv.DictWriter(output_file, headers)
            dict_writer.writeheader()
            dict_writer.writerows(self)
  
    def _csv_lines_to_dict_list(self, csv_lines, delimiter=";", headers=[]):
        first = True
        data = []
        for line in csv_lines:
            if first:
                if not headers:
                    headers = line.split(delimiter)
                first = False
            else:
                values = line.split(delimiter)
                values = [v.strip() for v in values]
                row = dict(zip(headers, values))
                data.append(row)
        return data

class DetailedTable(DictList):
    def parse_downloaded_file(self, file_path):
        print "Parse %s" % file_path
        with codecs.open(file_path, "r", "utf-8") as f:
            lines = [line for line in f]
            splits = [i for i,line in enumerate(lines) if len(line.strip()) == 0]
            tables = partition(lines, splits)
            data = self._csv_lines_to_dict_list(tables[0], headers=["group", "value", "last_year", "change"])
            params = {}
            for row in tables[2][2:]:
                x = row.split(";")
                key = x[0].replace(":","")
                value = x[1].strip()
                params[key] = value

            for data_row in data:
                row = merge_dicts(params, data_row)

                self.append(row)

            return self

class OverviewTable(DictList):
    def parse_downloaded_file(self, file_path):
        print "Parse %s" % file_path
        with open(file_path,'rb') as f:
            all_rows = list(csv.reader(f, delimiter=";"))
            if len(all_rows) == 0:
                print "%s is empty." % file_path
                raise EmptyFileError("In file {}".format(file_path))

            param_rows = all_rows[-5:]
            param_headers = [x[0].replace(":","").strip() for x in param_rows]
            param_values = [x[1].strip() for x in param_rows]

            data_rows = all_rows[6:-7]
            data_headers = [x.replace("\n","") for x in data_rows[0]]
            data_headers[0] = "Region"
            headers = param_headers + data_headers
            for row in data_rows[1:]:
                values = param_values + row
                self.append(dict(zip(headers, values)))

            return self

    def verify(self, year=None, month=None, youth_only=False, foreign_only=False):
        """ Validate that the downloaded file matches the current query
        """
        print "Verify data"

        # Validate month column
        for row in self:
            year_month = "%s-%02d" % (year, month)
            if row[u"Månad"] != year_month:
                pdb.set_trace()
                raise DataValidationError(u"Column 'Månad' should be '{}', but is '{}'".format(year_month, row[u"Månad"]) )

        # Validate youth_only column
        if youth_only:
            for row in self:
                if row[u"Ålder"] != u"18-24":
                    raise DataValidationError(u"Column 'Ålder' should be '18-24', but is '{}'".format(row[u"Ålder"]) )

        # Validate foreign_only column
        if foreign_only:
            for row in self:
                if row[u"Utrikesfödda"] != u"Ja":
                    raise DataValidationError(u"Column 'Utrikesfödda' should be 'Ja', but is '{}'".format(row[u"Utrikesfödda"]) )

