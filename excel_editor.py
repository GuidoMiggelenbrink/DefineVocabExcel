import pandas as pd

class ExcelVocabEditor:
    def __init__(self):
        self.df = None

    def read_excel(self, path):
        try:
            self.df = pd.read_excel(path, engine='openpyxl')
            return self.df
          
        except Exception as e:
            print(f"An error in read_excel() occurred: {e}")
    
    def print(self):
        print(self.df)
    
    def get_df(self):
        return self.df
    
    def get_word(self, index):
        self.df['word'][index]

    def get_word_list(self):
        try:
            word_list = []

            for word in self.df['Word']:
                word_list.append(word)
            
            return word_list
        
        except Exception as e:
            print(f"An error in get_word_list() occurred, error code: {e}")  
            return False          
            
    def write_df_row(self, row_i, col_s, col_e, translations, defintions, examples):
        """
        row_i : row index
        col_s : column start index  
        col_e : column end_index
        """
        try:
            self.df.iloc[row_i, col_s:col_e] = [translations, defintions, examples]
   
        except Exception as e:
            print(f"An error in write_df_row() occurred: {e}")

    def add_columns(self, new_columns: list):
        """append columns, without replacing existing ones. If column name already exist, skip."""
        for column_name in new_columns:
            if column_name not in self.df.columns:
                self.df[column_name] = ''

    def save_as_xlsx(self, path): 
        try:
            self.df.to_excel(path,index=False)
            return True
        except Exception as e:
            print(f"An error in save_as_xlsx() occurred: {e}")
            return False
        
    def save_as_csv(self, path):
        try:    
            self.df.to_csv(path,index=False)
            return True
        except Exception as e:
            print(f"An error in save_as_csv() occurred: {e}")
            return False