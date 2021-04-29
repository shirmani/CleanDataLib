from CleanData.python_expansion import *

class StoreDF:
    def __init__(self, dfs, dfs_names):
        self.dfs = dfs
        self.dfs_names = dfs_names
    
    def remove(self, df_names):
        df_names = Pexpansion.if_x_not_ls_make_x_ls(df_names)
        for df_name in df_names:
            print(type(self.dfs_names[0]))
            index_df = self.dfs_names.index(df_name)
            del self.dfs_names[index_df]
            del self.dfs[index_df]

    def add(self, df_name, df):
        self.dfs_names.append(df_name)
        self.dfs.append(df)

    def get_df_by_name(self, df_name):
        index_df = self.dfs_names.index(df_name)
        return self.dfs[index_df]

