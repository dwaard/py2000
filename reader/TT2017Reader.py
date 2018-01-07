import xlrd


class TT2017Reader:
    FILE_NAME = 'raw/TOP-2000-2017.xls'
    FILE_ENCODING = 'ascii'

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
