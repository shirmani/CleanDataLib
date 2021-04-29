import pandas as pd


class JEngineer:
    @staticmethod
    def interval_date_datetime_col(df, col, date, new_col, time_format="day"):
        """
        interval date datetime col (date is earlyest)
        
        input:
        df: pd.df
        
        col:str
            name of col that 
            
        date:str
            "m%.d%.y%"

        new_col:str 
            name of col that contine the range 
        """
        if time_format == "day":
            df[new_col] = (df[col] - pd.to_datetime(date)) / pd.Timedelta(days=1)
        
        elif time_format == "year":
            df[new_col] = (df[col] - pd.to_datetime(date)) / pd.Timedelta(years=1)
            
            
    @staticmethod
    def interval_datatime_cols(df, col_a, col_b, new_col, time_format="day"):
        """
        input
        df: pd.df
        
        col_a:str
            name of col that contine time you want to compute a - b = range, a later from b
            
        col_b:str
            name of col that contine time you want to compute a - b = range, a later from b
            
        new_col:str 
            name of col that contine the range 
         
        """
        if time_format == "day":
            df[new_col] = (df[col_a] - df[col_b])/ pd.Timedelta(days=1)
        
        elif time_format == "year":
            df[new_col] = (df[col_a] - df[col_b])/ pd.Timedelta(years=1)
            
    
    @staticmethod
    def v():
        print(13)
