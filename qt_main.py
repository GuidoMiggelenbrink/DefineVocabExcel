import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from dictionary_fetcher import CambridgeDictionaryFetcher
from excel_editor import ExcelVocabEditor
import os


class MainWindow(QDialog):
    def __init__(self):
        # GUI stuff
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.browse_in.clicked.connect(self.browseFiles_in)
        self.browse_out.clicked.connect(self.browseFiles_out)
        self.start.clicked.connect(self.startProgram)
        self.plainTextEdit.setPlainText(
            'Select an Excel file of which the first column contains words and the column name is "Word". \n'
        )

        # program logic stuff
        self.C_dict = CambridgeDictionaryFetcher()  # create dictionary object
        self.vocab_list = ExcelVocabEditor()  # create vocab list

    def browseFiles_in(self):
        fname = QFileDialog.getOpenFileName(
            self, "Open Excel file", "", "Excel Files (*.xlsx)"
        )
        self.filename_in.setText(fname[0])
        # pass

    def browseFiles_out(self):
        fname = QFileDialog.getSaveFileName(
            self, "Save as Excel file", "", "Excel Files (*.xlsx)"
        )
        self.filename_out.setText(fname[0])
        # pass

    def startProgram(self):
        try:
            # self.filename_out.setText(r"C:\Users\guido\Desktop\translator\env\hallo.xlsx")
            # self.filename_in.setText(r"C:\Users\guido\Desktop\translator\env\Vocab test.xlsx")

            if self.filename_in.text() and self.filename_out.text():
                print(self.filename_in.text())
                print(self.filename_out.text())

                # Open word list
                self.vocab_list.read_excel(str(self.filename_in.text()))
                word_list = self.vocab_list.get_word_list()

                if not word_list or (
                    all(i != i for i in word_list)
                ):  # code after or checks if all items in the list are 'nan'.
                    self.plainTextEdit.appendPlainText(
                        "No words found in the Excel file or column name 'Word' is missing. Try again. \n"
                    )
                    return False

                # append word list with defintions and examples from Cambridge Dictionary
                for i, word in enumerate(word_list):
                    def_blocks = self.C_dict.fetch_enLearner_dictionary(word)
                    col_s = 1
                    for j, block in enumerate(def_blocks):
                        self.vocab_list.add_columns(
                            [f"Translation{j}", f"Definition{j}", f"Example{j}"]
                        )
                        col_e = col_s + 3
                        self.vocab_list.write_df_row(
                            i,
                            col_s,
                            col_e,
                            block["Translations"],
                            block["Definitions"],
                            block["Examples"],
                        )
                        col_s = col_e

                # print table
                self.plainTextEdit.appendPlainText(str(self.vocab_list.get_df()))

                # save as .xlsx and .csv
                re_xlsx = self.vocab_list.save_as_xlsx(str(self.filename_out.text()))
                re_csv = self.vocab_list.save_as_csv(
                    f"{os.path.splitext(str(self.filename_out.text()))[0]}.csv"
                )

                if re_xlsx and re_csv:
                    self.plainTextEdit.appendPlainText(
                        "Succesfully saved .xlsx and .csv files. \n"
                    )
                else:
                    self.plainTextEdit.appendPlainText(
                        "Failed to save .xlsx or .csv. \n"
                    )

                return True

            else:
                self.plainTextEdit.appendPlainText("No file selected. \n")
                return False
        except Exception as e:
            print(f"An error in Startprogram() occurred: {e}")
            self.plainTextEdit.appendPlainText(
                f"An error in Startprogram() occurred: {e}. \n"
            )
            return False


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setWindowTitle("Dictionary Fetcher")
    widget.show()
    sys.exit(app.exec_())


main()

# ---------------------------------------------------------------------------
