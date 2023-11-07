# DefineVocabExcel

## install
Create a virtual environment:  
1. ```pip install virtualenv```  
2. ```py -m venv env```  
3. ```.\env\Scripts\activate```  

Install the required packages:  
1. ```pip install -r requirements.txt```  

Create executable:  
1. ```pyinstaller --onefile --add-data="gui.ui;." qt_main.py```  

pyinstaller packages source files and not data files such as gui.ui. Therefore, the gui.ui is not packed into the .exe and the .exe and gui.ui file must be distributed togehter (in the same folder). 

## Future work: 
Make use of an installer instead of packager(pyinstaller). 

