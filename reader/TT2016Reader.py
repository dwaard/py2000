import xlrd

class TT2016Reader:
    filename = 'raw/TOP-2000-2016.xls'

    def __init__(self):
        print "Reading %s..." % self.filename
        workbook = xlrd.open_workbook(self.filename, encoding_override='cp1252')
        self.current_row = 1
        self.worksheet = workbook.sheet_by_index(0)

    def __iter__(self):
        return self

    def next(self):
        if self.current_row >=self.worksheet.nrows:
            raise StopIteration
        else:
            result = [self.worksheet.cell(self.current_row, 1).value,
                      self.worksheet.cell(self.current_row, 2).value,
                      self.worksheet.cell(self.current_row, 3).value,
                        2016,
                      self.worksheet.cell(self.current_row, 0).value, ]
            self.current_row += 1
            return result
