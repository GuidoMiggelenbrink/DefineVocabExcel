import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from dictionary_fetcher import CambridgeDictionaryFetcher
from ExcelFile import ExcelFile
import requests
import signal
import sys

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)

        # slots 
        self.browse_in.clicked.connect(self.browseFiles_in)
        self.browse_out.clicked.connect(self.browseFiles_out)
        self.start.clicked.connect(self.startProgram)

        self.filename_in.setText(r"vocab_in.xlsx")
        self.filename_out.setText(r"vocab_out.xlsx")

        self.plainTextEdit.setPlainText('Select an Excel file of which the first column contains words and the column name is "Word". \n')

    def browseFiles_in(self):
        fname = QFileDialog.getOpenFileName(
            self, "Open Excel file", "", "Excel Files (*.xlsx)"
        )
        self.filename_in.setText(fname[0])

    def browseFiles_out(self):
        fname = QFileDialog.getSaveFileName(
            self, "Save as Excel file", "", "Excel Files (*.xlsx)"
        )
        self.filename_out.setText(fname[0])

    def startProgram(self):
        # try:
            #self.filename_in.setText(r"C:\Users\guido\Desktop\DefineVocabExcel\Vocab test.xlsx")
            #self.filename_out.setText(r"C:\Users\guido\Desktop\DefineVocabExcel\hallo.xlsx")

            # check if browse file input fields are not empty
            if self.filename_in.text() and self.filename_out.text():
                print(self.filename_in.text())
                print(self.filename_out.text())
                
                # Create dictionary
                CamDict = CambridgeDictionaryFetcher() 

                # Open excel file
                xlsx_in = ExcelFile()
                xlsx_in.open(str(self.filename_in.text()))

                # get word list  
                word_list = xlsx_in.read_column()

                # close excel file
                xlsx_in.close()

                # check if word list is empty 
                if not word_list or (all(i != i for i in word_list)):  # code after or checks if all items in the list are 'nan'.
                    self.plainTextEdit.appendPlainText("No words found in the Excel file or column name 'Word' is missing. Try again. \n")
                    return False
                
                # create excel file and save
                xlsx_out = ExcelFile()
                xlsx_out.create()
                xlsx_out.save(str(self.filename_out.text()))

                # create rows 
                row_1 = ["Word"]
                rows = []
                
                # fetch word and parse into a row
                for i, word in enumerate(word_list):

                    def_blocks = CamDict.fetch_enLearner_dictionary(word)

                    row = [word]
                    for j, block in enumerate(def_blocks[:3]):
                        # update first row
                        if f"Definition{j}" not in row_1:
                            row_1 += [f"Definition{j}", f"Example{j}" ]                  
                        # append new rows
                        row += [str(block["Definitions"]), str(block["Examples"])]
                    rows.append(row)

                    # save intermediate results 
                    if ((i+1) % 10) == 0:
                        xlsx_out.write_row(row_1)
                        xlsx_out.append_rows(rows) 
                        xlsx_out.save(str(self.filename_out.text())) 
                        rows = []

                    print(f"- {i}. {word}")

                # save results and close file
                xlsx_out.write_row(row_1)
                xlsx_out.append_rows(rows)    
                re = xlsx_out.save(str(self.filename_out.text()))
                xlsx_out.close()
                self.plainTextEdit.appendPlainText("Succesfully saved .xlsx and .csv files. \n")
                print("end")
                
            else:
                self.plainTextEdit.appendPlainText("No file selected. \n")
                return False            
        
        # except Exception as e:
        #     print(f"Error Startprogram(): {e}")

def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setWindowTitle("Dictionary Fetcher")
    widget.show()
    sys.exit(app.exec_())

main()
