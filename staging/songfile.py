import xlrd
import xlwt
from xlutils.copy import copy
import datetime

class SongFile:
    FILE_NAME = "staged/song_cleaning.xls"
    SWAP_SHEET_NAME = 'swap_list'
    IGNORE_SHEET_NAME = 'ignore_list'
    RAW_SHEET_NAME = 'raw_%s'

    HEADER_ROW = ['artiest', 'song1', 'song2', 'year1', 'year2', 'ratio']

    FILE_ENCODING = 'UTF-8'

    swap_list = dict()
    ignore_list = dict()

    raw_data = [HEADER_ROW]

    def __init__(self):
        self.data = []
        try:
            self.workbook_reader = xlrd.open_workbook(self.FILE_NAME,
                                                      formatting_info=True,
                                                      encoding_override=self.FILE_ENCODING)
        except IOError:
            wt = xlwt.Workbook(encoding=self.FILE_ENCODING)
            wt.add_sheet(self.SWAP_SHEET_NAME)
            wt.add_sheet(self.IGNORE_SHEET_NAME)
            wt.save(self.filename)
            rd = xlrd.open_workbook(self.FILE_NAME, encoding_override=self.FILE_ENCODING)
        # read the swap list
        ws = self.workbook_reader.sheet_by_name(self.SWAP_SHEET_NAME)
        for row in range(ws.nrows):
            artist = ws.cell(row, 0).value
            current = ws.cell(row, 1).value
            changeto = ws.cell(row, 2).value
            current_name = "%s - %s" % (current, artist)
            self.swap_list[current_name] = changeto
        # read the ignore list
        ws = self.workbook_reader.sheet_by_name(self.IGNORE_SHEET_NAME)
        for row in range(ws.nrows):
            artist = ws.cell(row, 0).value
            current = ws.cell(row, 1).value
            changeto = ws.cell(row, 2).value
            current_name = "%s - %s" % (current, artist)
            self.ignore_list[current_name] = changeto

    def should_ignore_on_analyze(self, name1, name2):
        if not self.ignore_list.has_key(name1):
            return False
        return self.ignore_list[name1] == name2

    def clean_title(self, artist, title):
        title = title.strip()
        name = "%s - %s" % (title, artist)
        if self.swap_list.has_key(name):
            return self.swap_list[name]
        return title

    def append_raw_data(self, row):
        """"
        Voegt een nieuwe regel ruwe output toe
        """
        self.raw_data.append(row)

    def save(self):
        """"
        Slaat de wijzigingen in het Excel bestand op
        """
        print "START WRITING"
        wt = copy(self.workbook_reader)
        wt.encoding = self.FILE_ENCODING
        wt.__dict__['_Workbook__sst'].encoding = self.FILE_ENCODING
        sheet_name = self.RAW_SHEET_NAME % datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
        ws = wt.add_sheet(sheet_name)
        for row, value_array in enumerate(self.raw_data):
            for column, value in enumerate(value_array):
                cell_value = value
                if column < 2:
                    print repr(cell_value)
                ws.write(row, column, cell_value)
        wt.save(self.FILE_NAME)



