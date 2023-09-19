import xlsxwriter
import datetime
import os
from pathlib import Path
from goods import Item


class Excel:

    def __init__(self):
        self.begin_column = 0
        self.begin_row = 0

    @staticmethod
    def _get_workbook_name(folder: Path):
        filename = f"HM_{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}.xlsx"
        if folder:
            filename = Path(folder, filename)

        return filename

    def create_table(self, data: list, columns: list, folder: Path = os.getcwd()) -> Path:
        workbook_name = self._get_workbook_name(folder)
        workbook = xlsxwriter.Workbook(workbook_name)
        worksheet = workbook.add_worksheet()
        row_nums = len(data)
        col_nums = len(data[0])

        worksheet.add_table(self.begin_row,
                            self.begin_column,
                            self.begin_row + row_nums,
                            self.begin_column + col_nums - 1,
                            {"data": data, "columns": columns, "style": "Table Style Medium 2"})

        i = 0
        for k, v in Item.attributes.items():
            width = v.get("width")
            worksheet.set_column(self.begin_column + i, self.begin_column + i, width)
            i += 1

        workbook.close()
        return workbook_name


