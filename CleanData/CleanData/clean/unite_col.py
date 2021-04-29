from CleanData.clean.clean import *

class Unite:
    # U
    @staticmethod
    def unite_multicategries_columns(df, cols, delete=True):
        """Vector connection of text columns
        with a separation of "," between the connections"""
        # Preparation for vector connection
        for col in cols:
            Clean.add_comma_to_notnull_value_in_col(df, col)
            df[col] = df[col].fillna("")

        # vector connection
        for i in range(1, len(cols)):
            df[cols[0]] = df[cols[0]] + df[cols[i]]

        # Preparation connected col
        df[col] = df[col].apply(lambda x: Pexpansion.del_duplicate_categories_in_multicategories_str(x))
        Clean.replace_empty_value_to_npnan(df, cols[0])
        df[cols[0]] = df[cols[0]][df[cols[0]].notnull()].apply(lambda x: x[2::])

        # Delete unnecessary columns
        if delete:
            cols.pop(0)
            df.drop(cols, axis=1, inplace=True)

    # U
    @staticmethod
    def unite_categories_columns(df, cols, dictionary_importance):
        """
        input:
        dictionary_importance:dict
            {"deceased":0,"cured":0, "critical":1, "good":2, "asymptomatic":3}
            the smaller the number is the more important it is
            and will choose over others
        *If two keys of the same value are in the string
        the first one in the string will be selected"""
        # make hotvec of combinations
        name_of_first_col = cols[0]
        Clean.unite_multicategries_columns(df, cols)
        df_hotvec_phrase = pd.get_dummies(df[name_of_first_col])

        # Insert the most important category into the output column
        df_hotvec_phrase[name_of_first_col] = np.nan
        df_hotvec_phrase_cols_without_output_col = list(df_hotvec_phrase.columns)[0:-1]

        for col in df_hotvec_phrase_cols_without_output_col:
            category = Pexpansion.select_category_by_importance(col, dictionary_importance)
            df_hotvec_phrase.loc[df_hotvec_phrase[col] == 1, name_of_first_col] = category

        Clean.concat_resultcol_to_df(df, df_hotvec_phrase, name_of_first_col)
        del df_hotvec_phrase


    # M ????
    @staticmethod
    def update_by_index(df, col, indexs, data):
        """
        Value change according index

        df: pd.df

        col : str
            name of col you want to change

        indexs: pd.index

        data: int/ str/ float
            data you want to into

        """
        for indx in indexs:
            df.loc[indx, col] = data
