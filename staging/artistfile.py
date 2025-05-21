import xlrd
import xlwt
from xlutils.copy import copy
import datetime

class ArtistFile:
    """"
    Repository klasse naar het artst cleaning Excel bestand
    """

    FILE_NAME = "staged/artist_cleaning.xls"
    SWAP_SHEET_NAME = 'swap_list'
    IGNORE_SHEET_NAME = 'ignore_list'
    RAW_SHEET_NAME = 'raw_%s'

    HEADER_ROW = ['name1', 'name2', 'artist', 'songs', 'adv', 'stem1', 'stem2']

    FILE_ENCODING = 'UTF-8'

    swap_list = dict()
    ignore_list = dict()

    raw_data = [HEADER_ROW]

    def __init__(self):
        try:
            self.workbook_reader = xlrd.open_workbook(self.FILE_NAME,
                                                      formatting_info=True,
                                                      encoding_override=self.FILE_ENCODING)
            pass
        except IOError:
            wt = xlwt.Workbook(encoding=self.FILE_ENCODING)
            wt.add_sheet(self.SWAP_SHEET_NAME)
            wt.add_sheet(self.IGNORE_SHEET_NAME)
            wt.save(self.FILE_NAME)
            self.workbook_reader = xlrd.open_workbook(self.FILE_NAME, encoding_override=self.FILE_ENCODING)
        # read the swap list
        ws = self.workbook_reader.sheet_by_name(self.SWAP_SHEET_NAME)
        for row in range(ws.nrows):
            current = ws.cell(row, 0).value
            change_to = ws.cell(row, 1).value
            self.swap_list[current] = change_to
        # read the ignore list
        ws = self.workbook_reader.sheet_by_name(self.IGNORE_SHEET_NAME)
        for row in range(ws.nrows):
            current = ws.cell(row, 0).value
            change_to = ws.cell(row, 1).value
            self.ignore_list[current] = change_to

    def should_ignore_on_analyze(self, name1, name2):
        """"
        Retourneert True als de combinatie name1, name2 voorkomt in de ignore lijst
        """
        if not self.ignore_list.has_key(name1):
            return False
        return self.ignore_list[name1] == name2

    def clean(self, name):
        """"
        Cleant de meegegeven artiestennaam 
        """
        name = name.strip()
        if self.swap_list.has_key(name):
            return self.swap_list[name]
        return name


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

