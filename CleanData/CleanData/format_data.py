import numpy as np 
import pandas as pd


class Format:
    
    @staticmethod
    def get_name_of_categorized_value(df, input_col):
        """
        df: pd.dataframe
        
        input_col:str
        """
        value_list = [c for c in df[input_col][df[input_col].notnull()]]
        clean_value_list = list(dict.fromkeys(value_list))

        name_col = []
        for x in clean_value_list:
            i = x.split(",")
            for t in i:
                t = t.strip()
                name_col.append(t)

        clean_name_col = list(dict.fromkeys(name_col))
        return clean_name_col
    
    
    @staticmethod
    def category_col_to_num_col(df, col):
        """
        df: pd.dataframe
        
        col:str
        """
        keys = Format.get_name_of_categorized_value(df, col)
        value = range(len(keys))

        dictionary = dict(zip(keys, value))
        print(dictionary)
        df[col] = df[col].replace(dictionary)
        
        return dictionary
    
    
    @staticmethod
    def turn_hotvec(df, input_col, min_num):
        """
        df: pd.dataframe
        
        input_col:str
        """
        name_col = Format.get_name_of_categorized_value(df, input_col)
        for j in name_col:
            name = j.replace(" ", "_")
            df[input_col + "_"+ name] = df[input_col][df[input_col].notnull()].apply(lambda i: 1 if j in i else 0)
            print(df[input_col + "_"+ name].value_counts())
            
        # delete all columns that the frequency of a particular option 0 \ 1
        # is less than min_num
            for cat, frequency in dict(df[input_col + "_"+ name].value_counts()).items():
                if frequency < min_num:
                    print("--del " + input_col + "_"+ name + "---"+ "\n")
                    df.drop([input_col + "_"+ name], axis=1, inplace=True )
                    pass
            
    @staticmethod
    def v():
        print(8)
            
            