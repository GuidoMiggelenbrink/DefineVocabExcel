# DefineVocabExcel

pyinstaller packages source files and not data files such as gui.ui. Therefore, the gui.ui is not packed into the .exe and the .exe and gui.ui file must be distributed togehter (in the same folder). 

#### Future work: 
Make use of an installer instead of packager(pyinstaller). 

#### Commands:
Create executable: `pyinstaller --onefile --add-data="gui.ui;." qt_main.py`