from CleanData.clean import *

class Cage:
    """"""
    @staticmethod
    def find_index_of_montly_weekly_daily_age(df, col):
        # find 
        dict_index = {"m":[], "w":[], "d":[]}
        for word in [ "month","week","day"]:
            dict_index[word[0]].append(list(df.index[df[col].astype(str).str.contains(word,  na=False)]))

        # flattening a two-dimensional list 
        for k, v  in dict_index.items():
            dict_index[k] = list(set([j for sub in v for j in sub]))
        return dict_index
    
    @staticmethod
    def from_montly_weekly_daily_to_num_age(df, col, dict_index): 
        date_dict = {"m":12, "w": 52, "d": 365}
        for k,v in dict_index.items():
            for i in v:
                integer = int([i for i in df.loc[i, col] if i.isdigit()][0])
                df.loc[i, col] = round(integer/date_dict[k], 2)
    
    
    @staticmethod
    def clean_age_col(df, col,  ls_contine_x_del):
        dict_index = Cage.find_index_of_montly_weekly_daily_age(df, col)
        Cage.from_montly_weekly_daily_to_num_age(df, col, dict_index)

        ls_contine_x_del += ["-", ">","<","+"]
        Clean.replace_value_by_contained_x(df, col, ls_contine_x_del, np.nan)

    
    
    #---------------------------------- age band -------------------------------------------
    
    @staticmethod
    def from_ranges_to_smaller_num(x):
        """ 75- => " "
        -7575- => " "
        80-89 75- => " "
        80-90 => 80
        70-90 =>np.nan"""
        # split - and del empty
        ls = x.split("-")
        ls_range = []

        for i in ls:
            if i.strip().isdigit() == True:
                ls_range.append(i)
 
        ls_range  = Clean.remove_from_ls(ls_range , "")
        ls_range = sorted(ls_range)
        
        # Age range difference 10 years
        if len(ls_range)>1 and (int(ls_range[0]) - int(ls_range[1]))**2 < 101 :
            return ls_range[0]
        
        # Age range difference more then 10 years of -60, 75-
        elif len(ls_range)< 2 or (int(ls_range[0]) - int(ls_range[1]))**2 > 101:
            return " "


    @staticmethod
    def to_age_band(df , col, ls_contine_x_del):
        """age_band from dirty age (range and more) """

        # values of months, weeks and days
        for word in ["month", "week","day"]:
            df.loc[df[col].astype(str).str.contains(word,  na=False), col] = 0
    
        # ranges to  smaller num
        df[col] = df[col].astype("str")
        df["n"] = df[col][df[col].str.contains("-",  na=False)].apply(lambda x :Cage.from_ranges_to_smaller_num(x))
        df[col].update(df["n"])
        df.drop(["n"],  axis= 1, inplace=True)
        
        # del value with ls_contine_x_del
        df[col] = df[col].astype("str")
        ls_contine_x_del += ["-", ">","<","+"]
        Clean.replace_value_by_contained_x(df, col, ls_contine_x_del, np.nan)
        df[col]= df[col][df[col].notnull()].apply(lambda x : np.nan if x== " " else x)
      
        #make num to 
        df[col] = df[col][df[col].notnull()].apply(lambda x : np.nan if x == "nan" else round(float(x)/10)*10)

        
    @staticmethod
    def v():
        print(17)