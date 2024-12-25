import xlrd

class XlrdReader:
    filename = 'raw/TOP-2000-2016.xls'

    YEAR = 2016

    def __init__(self, filename, edition):
        self.edition = edition
        print ("Reading %s..." % filename)
        workbook = xlrd.open_workbook(filename, encoding_override='cp1252')
        self.current_row = 1
        self.worksheet = workbook.sheet_by_index(0)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_row >=self.worksheet.nrows:
            raise StopIteration
        else:
            result = [self.worksheet.cell(self.current_row, 1).value,
                      self.worksheet.cell(self.current_row, 2).value,
                      int(self.worksheet.cell(self.current_row, 3).value),
                        2016,
                      int(self.worksheet.cell(self.current_row, 0).value), ]
            self.current_row += 1
            return result
