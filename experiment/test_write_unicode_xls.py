import xlwt, xlrd
from xlutils.copy import copy

class TT2017Reader:
    FILE_NAME = 'TOP-2000-2017.xls'
    FILE_ENCODING = 'UTF-8'

    YEAR = 2017

    def __init__(self):
        print "Reading %s..." % self.FILE_NAME
        try:
            workbook = xlrd.open_workbook(self.FILE_NAME, encoding_override=self.FILE_ENCODING)
            self.current_row = 1
            self.worksheet = workbook.sheet_by_index(0)
        except IOError:
            self.current_row = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current_row == 0 or self.current_row >=self.worksheet.nrows:
            raise StopIteration
        else:
            while (self.worksheet.cell(self.current_row, 0).value == ''):
                self.current_row += 1
            result = [self.worksheet.cell(self.current_row, 1).value,
                      self.worksheet.cell(self.current_row, 2).value,
                      1800,
                      self.YEAR,
                      self.worksheet.cell(self.current_row, 0).value, ]
            self.current_row += 1
            return result


FILE_NAME = 'artist_cleaning.xls'
FILE_ENCODING = 'UTF-8'

r = TT2017Reader()
data = []
for index, row in enumerate(r):
    if index == 19:
        print row
        data = row


wb = xlrd.open_workbook(FILE_NAME,
                        formatting_info=True,
                        encoding_override=FILE_ENCODING)
wb = copy(wb)
wb.encoding = FILE_ENCODING
wb.__dict__['_Workbook__sst'].encoding = FILE_ENCODING
uc = u"".join(unichr(0x0410 + i) for i in xrange(32)) # some Cyrillic characters
uc = data[1].encode('UTF-8')
u8 = uc.decode(FILE_ENCODING)
ws = wb.add_sheet("demo")
ws.write(0, 0, uc)
ws.write(1, 0, u8)
ws.write(2, 0, xlwt.Formula("A1=A2"))
ws.write(3, 0, "ASCII is a subset of UTF-8")
wb.save("xlwt_write_utf8.xls")