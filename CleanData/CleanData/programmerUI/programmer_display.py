import pandas as pd
import sys


class Display:
    def __init__(self, class_store):
        self.class_store = class_store
        self.dfs = class_store.dfs
        self.dfs_names = class_store.dfs_names

    @staticmethod
    def num_of_line():
        print()
        print()
        print(str(sys._getframe(2).f_lineno) + "-----------------------------")

    def print_df_by_name(self, df_name, num_rows=5):
        df = self.class_store.get_df_by_name(df_name)
        pd.set_option('expand_frame_repr', True,
                      "display.max_rows", num_rows,
                      "display.max_columns", len(df),
                      'display.width', len(df) * 50)
        print(df)
        pd.reset_option("display.max_rows")
        pd.reset_option("display.max_columns")
        pd.reset_option('display.width')

    def print_all_dfs(self):
        for df_name in self.dfs_names:
            print(df_name)
            Display.print_df_by_name(df_name)
            print("-------------------------------")

    def print_col_values_by_dfs(self, col):
        Display.num_of_line()
        print("--" + col + "--")
        for i in range(len(self.dfs)):
            print("\n" + self.dfs_names[i])
            if col in self.dfs[i].columns:
                print(self.dfs[i][col].value_counts())

    def print_shape_dfs(self):
        Display.num_of_line()
        print("Shape of Dfs")
        shapes = []
        for i in range(len(self.dfs_names)):
            print(self.dfs_names[i], self.dfs[i].shape)
            shapes.append(self.dfs[i].shape[0])
        print("\nsum " + str(sum(shapes)))

    def print_cols_by_df(self):
        Display.num_of_line()
        for i in range(len(self.dfs_names)):
            print(self.dfs_names[i] + " " + str(self.dfs[i].columns))
            print()

    def print_cols_values_by_dfs(self):
        Display.num_of_line()
        for i in range(len(self.dfs_names)):
            for col in self.dfs[i].columns:
                print(self.dfs_names[i] + " " + col)
                print(self.dfs[i][col].value_counts())
                print()
