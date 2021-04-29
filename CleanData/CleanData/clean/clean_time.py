from CleanData.clean import *
from CleanData.python_expansion import *
import numpy as np
import pandas as pd

class CTime:

    @staticmethod
    def make_ls_of_str_to_datatime(ls):
        for i in range(len(ls)):
            ls[i] = pd.to_datetime(ls[i], dayfirst=True, errors='ignore').date() # optim?
        return ls

    @staticmethod
    def time_range_extremity(ls, earliest=False):
        """
        return the latest / earliest date from a date list
        
        input:
        ls: list
         list of pd.datatime
         
        earliest: True/Fasle
            True :return the earliest date
            False :return the latest date
        
        return:
            pd.datetime
        
        """
        df = pd.DataFrame({"series":ls})  # optim
        if earliest == True:
            value = df.series.max() # optim
        else:
            value = df.series.min() # optim
        return value

    @staticmethod
    def exceptional_time_range(x, character_separator, earliest=False):
        """
        Handle date column exceptions (before becoming pd.datetime)      
        
        input:
        df:pd.df
        
        input_col:str
            name of col
            
        output_col:str
            name of col
        
        indx:int 
            index of row 
            
        character_separator: list
            List of characters separating dates
            
        earliest: False \ True
        """
        ls = x.split(character_separator)

        ls = Pexpansion.remove_from_ls(ls , "")

        ls = CTime.make_ls_of_str_to_datatime(ls)

        return CTime.time_range_extremity(ls, earliest=False)


    @staticmethod
    def stipulation_len_str(x):
        """
        Checks if the date is correct by the length of the string
 
        input:
        df:pd.df
        
        input_col:str
            name of col
        
        indx:int 
            index of row 
        """
        if 10< len(x)<12:
            print(x)
            return np.nan


    
    @staticmethod
    def updat_s_time(df, col, character_separator, earliest=False):

        # Identify exceptions
        error = []

        exceptional_df = df[df[col].str.contains(character_separator, na=False)]
        exceptional_dictionary = exceptional_df[col].to_dict()
        for k,v in exceptional_dictionary.items():
            df.loc[k, col] = CTime.exceptional_time_range(v, character_separator, earliest=False)

        CTime.updat_s_time_basic_multi_df([df], col, True)
        return error      

    @staticmethod
    def updat_s_time_basic_multi_df(dfs, col, format_):
        """
        Makes series pd.datetime
        Unthinkable exceptionally (needs to be addressed before)
        input:
        dfs : list
            list of pd.dataframe 
        """
        for df in dfs:
            print("----------------------------------")
            if col in df.columns:
                print(col)
            df.loc[df[col] == " ", col] = np.nan
            df[col] = df[col].fillna(np.nan)

            if type(format_) == str:
                df[col] = pd.to_datetime(df[col], format= format_)
            else:  
                df[col] = pd.to_datetime(df[col], dayfirst=True)

    @staticmethod
    def exceptional_ranges(x):

        # split - and del empty
        ls_range = x.split("-")
        ls_range =  Clean.remove_from_ls(ls_range , "")

        # if len(ls_range) == 1 handle "-75" or "75 -"
        if len(ls_range) == 1:
            return x 

        else:
            ls_range  = Clean.decade_of_range(ls_range)

            if ls_range[0][0] == ls_range[1][0]:
                df.loc[indx, col_band]  = int(ls_range[0][0])*10
                df.loc[indx, col]  = np.nan

            else:
                df.loc[indx, col]  = np.nan
    
    
    @staticmethod
    def v():
        print(14)