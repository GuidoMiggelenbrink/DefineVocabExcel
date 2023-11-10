import pandas as pd

class ExcelVocabEditor:
    def __init__(self):
        self.df_table = None
        self.df_word_list = None

    def read_excel(self, path):
        try:
            self.df_table = pd.read_excel(path, engine='openpyxl')
            return self.df_table
          
        except Exception as e:
            print(f"An error in read_excel() occurred: {e}")
    
    def print(self):
        print(self.df_table)
    
    def get_df_table(self):
        return self.df_table
    
    def get_word(self, index):
        self.df_word_list = self.df_table['word'][index] 
        return self.df_word_list

    def get_word_list(self):
        try:
            for word in self.df_table['Word']:
                self.df_word_list.append(word)
            
            return self.df_word_list
        
        except Exception as e:
            print(f"An error in get_word_list() occurred, error code: {e}")  
            return False          
            
    def write_df_table_row(self, row_i, col_s, col_e, translations, defintions, examples):
        """
        row_i : row index
        col_s : column start index  
        col_e : column end_index
        """
        try:
            self.df_table.iloc[row_i, col_s:col_e] = [translations, defintions, examples]
   
        except Exception as e:
            print(f"An error in write_df_table_row() occurred: {e}")

    def add_columns(self, new_columns: list):
        """append columns, without replacing existing ones. If column name already exist, skip."""
        for column_name in new_columns:
            if column_name not in self.df_table.columns:
                self.df_table[column_name] = ''

    def save_as_xlsx(self, path): 
        try:
            self.df_table.to_excel(path,index=False)
            return True
        except Exception as e:
            print(f"An error in save_as_xlsx() occurred: {e}")
            return False
        
    def save_as_csv(self, path):
        try:    
            self.df_table.to_csv(path,index=False)
            return True
        except Exception as e:
            print(f"An error in save_as_csv() occurred: {e}")
            return False
        
    def append_xlsx(self):
        """Write dataframe to xlsx file in append mode"""
        pass

    def append_csv(self):
        pass

    def clear_df_table(self):
        """Clear the dataframe/reset to initial state"""
        self.df_table = None