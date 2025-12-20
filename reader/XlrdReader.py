import xlrd

class XlrdReader:

    def __init__(self, filename, edition, start_row=1, title_col=1, artist_col=2, year_col=3, position_col=0):
        self.edition = edition
        self.title_col = title_col
        self.artist_col = artist_col
        self.year_col = year_col
        self.position_col = position_col
        print ("Reading %s..." % filename)
        workbook = xlrd.open_workbook(filename, encoding_override='cp1252')
        self.current_row = start_row
        self.worksheet = workbook.sheet_by_index(0)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_row >=self.worksheet.nrows:
            raise StopIteration
        else:
            result = [self.worksheet.cell(self.current_row, self.title_col).value,
                      self.worksheet.cell(self.current_row, self.artist_col).value,
                      int(self.worksheet.cell(self.current_row, self.year_col).value),
                      self.edition,
                      int(self.worksheet.cell(self.current_row, self.position_col).value), ]
            self.current_row += 1
            return result
