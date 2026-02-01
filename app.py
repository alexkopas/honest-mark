from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication
import traceback
import design
from pathlib import Path
from excel import Excel
from goods import Item
from xmlparser import XMLParser
import logging


logger = logging.getLogger(__name__)


class HonestMarkApp(QMainWindow, design.Ui_HonestMark):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnStart.clicked.connect(self.parse_files)
        self.tbBrowse.clicked.connect(self.select_directory)
        self.chbCreateExcel.setVisible(True)
        self.setFixedSize(867, 689)
        self.setStyleSheet("""QListWidget{
                    background: #f0f0f0;
                }
                """)
        self.xml_files = None
        self.folder = None
        self.clear_forms()

    def parse_files(self):
        try:
            parser = XMLParser()
            parser.parse(self.xml_files)
            if not parser.items:
                self.show_messagebox(icon=QMessageBox.Warning,
                                     text="В XML-файлах отсутствуют данные по КИЗ!",
                                     title="Нет данных",
                                     buttons=QMessageBox.Ok)
                return

            if self.chbCreateExcel.isChecked():
                self.create_excel(parser)

            self.clear_table()
            self.fill_table(parser)
        except Exception as e:
            self.show_messagebox(icon=QMessageBox.Critical,
                                 text="Возникла ошибка\n{}".format( traceback.format_exc()),
                                 title="Ошибка",
                                 buttons=QMessageBox.Ok)

    def fill_table(self, parser):
        table = self.table
        data = parser.to_list()
        table.setColumnCount(len(Item.attributes.keys()))
        table.setRowCount(len(data))

        table.setHorizontalHeaderLabels([v["column"] for k, v in Item.attributes.items()])

        i = 0
        for row in data:
            j = 0
            for col in row:
                table.setItem(i, j, QTableWidgetItem(str(col)))
                j += 1
            i += 1

        table.resizeColumnsToContents()

    def create_excel(self, parser: XMLParser):

        data = parser.to_list()
        logger.debug("Data: {}".format(data))
        wb = Excel()
        wb_name = wb.create_table(data=data, columns=Item.columns)

        self.show_messagebox(icon=QMessageBox.Information,
                             text="Создан файл \n{}".format(str(wb_name)),
                             title="Готово",
                             buttons=QMessageBox.Ok)

    def clear_table(self):
        self.table.clear()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)

    def clear_forms(self):
        self.lbFolder.setText("")
        self.listFiles.clear()
        self.xml_files = None
        self.folder = None
        self.btnStart.setEnabled(False)
        self.clear_table()

    @staticmethod
    def show_messagebox(icon, text, title, buttons, add_text=None):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setInformativeText(add_text)
        msg.setStandardButtons(buttons)
        msg.exec()

    def select_directory(self):
        self.clear_forms()

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        # dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)
        dialog.setDirectory(QCoreApplication.applicationDirPath())

        res = dialog.exec()
        if res != QFileDialog.Accepted:
            logger.debug("Folder dialog canceled")
            return

        directory = Path(dialog.directory().absolutePath())
        logger.debug(directory)

        if directory.is_dir():
            self.lbFolder.setText(str(directory))
            self.folder = directory
        else:
            self.show_messagebox(icon=QMessageBox.Critical,
                                 text="Каталог не существует\n{}".format(str(directory)),
                                 title="Ошибка",
                                 buttons=QMessageBox.Ok)
            return

        all_files = self.folder.glob("*.*")
        self.xml_files = [f for f in all_files if str(f).lower().endswith(".xml")]
        if self.xml_files:
            self.btnStart.setEnabled(True)
            [self.listFiles.addItem(f.name) for f in self.xml_files]
            self.xml_files = [Path(self.folder, f) for f in self.xml_files]

