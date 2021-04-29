import nltk
import pandas as pd
from CleanData.clean.clean import *
from CleanData.python_expansion import *


class TextAnalysis:
    """Converts free text column to a category or multicategories column by a root guide dictionary"""

    @staticmethod
    def from_col_text_to_root_str(df, col):
        """" text (include punctuation) -> "root root root" """
        Clean.clean_text_col_from_punctuation(df, col)
        ps = nltk.stem.SnowballStemmer('english')
        Clean.change_words_col_to_ls_word_col(df, col)
        df[col] = df[col].apply(lambda x: Pexpansion.from_word_ls_to_roots_str(x, ps) if x == x else " ")

    @staticmethod
    def guess_by_word(df_hotvec_phrase, bag_words):
        """get hotvec of Columns expressions
        return dict that classified if the column belonging to the category (keys)
        decide by bag_words (if root is in key point on category (value))
        input:
        df_hotvec_phrase:pd.df
        bag_words: dict
        return:
        dict_vote_words:dict
        """
        dict_vote_words = dict(zip(df_hotvec_phrase.columns,
                                   [[] for i in range(len(df_hotvec_phrase.columns))]))
        for j in df_hotvec_phrase.columns:
            for k, v in bag_words.items():
                if k in j:
                    dict_vote_words[j].append(v)
        return dict_vote_words

    @staticmethod
    def guess_by_sentence(df_hotvec_phrase, sentences_bag, num_decision):
        """get hotvec of Columns expressions
        rreturn dict that classified if the column belonging to the category (keys)
        decide by sentences_bag (if num_decision of root is in value list of key)"""
        dict_vote_sentences = dict(zip(df_hotvec_phrase.columns, [[] for i in range(len(df_hotvec_phrase.columns))]))
        for j in df_hotvec_phrase.columns:
            dict_vote = dict(zip(sentences_bag.keys(), [0 for i in range(len(sentences_bag.keys()))]))
            for k, v in sentences_bag.items():
                for i in v:
                    if i in j:
                        dict_vote[k] += 1

            for k, v in dict_vote.items():
                if v > num_decision - 1:
                    dict_vote_sentences[j].append(k)
        return dict_vote_sentences

    @staticmethod
    def clean_until_guess(df, input_col, bag_words, sentences_bag,
                          num_decision, input_col_is_dirty):

        if input_col_is_dirty == True:
            # clean the col 
            TextAnalysis.from_col_text_to_root_str(df, input_col)
            # print(df[input_col])

        # make hot vector - split to hotvec for vectorization of the code(improve performance)
        df_hotvec_phrase = pd.get_dummies(df[input_col])

        # make guess
        dict_vote_words = TextAnalysis.guess_by_word(df_hotvec_phrase, bag_words)
        dict_vote_sentences = TextAnalysis.guess_by_sentence(df_hotvec_phrase, sentences_bag,
                                                             num_decision)

        return df_hotvec_phrase, dict_vote_words, dict_vote_sentences

    @staticmethod
    def make_votevec_from_hotvec(df_hotvec_phrase, type_vote, dict_vote_cols):
        ls_categories = [j for i in dict_vote_cols.values() for j in i]
        for col in ls_categories:
            name_col_result = "result_" + type_vote + "|" + col
            df_hotvec_phrase[name_col_result] = 0

        for k, v in dict_vote_cols.items():
            for i in v:
                df_hotvec_phrase["result_" + type_vote + "|" + i] = df_hotvec_phrase["result_" + type_vote + "|" + i] + \
                                                                    df_hotvec_phrase[k]

        return ls_categories

    @staticmethod
    def del_unuseful_cols_to_get_resultvec_df(df_hotvec_phrase):
        """child func: TextAnalysis.analyze_text_for_category_col"""
        phrase_in_df = []
        for j in df_hotvec_phrase.columns:
            if "result_" not in j:
                phrase_in_df.append(j)
        df_resultvec = df_hotvec_phrase.drop(phrase_in_df, axis=1)
        return df_resultvec

    @staticmethod
    def supervision(combain_dict, num_decision_supervision):
        new_combain_dict = {}
        for k, v in combain_dict.items():
            if len(v) + num_decision_supervision < len(k.split(" ")):
                new_combain_dict.update({k: v})
        return new_combain_dict

    @staticmethod
    def make_resultcol_category_col(df, df_votevec, ls_categories, name_output_col):
        """Gives category 1 per row
            Prefers sentence analysis over word analysis
        
            child func: TextAnalysis.analyze_text_for_category_col"""
        ####TODO : Make a solution without the conditions
        category_ls = list(set(ls_categories))
        if len(df_votevec.columns) == 0:
            print("The result column is empty")

        else:
            for col in df_votevec.columns:
                ls_col_name = col.split("|")
                df_votevec.loc[df_votevec[col] == 1, name_output_col] = ls_col_name[1]

    @staticmethod
    def analyze_text_for_category_col(df, input_col, name_output_col, bag_words, sentences_bag,
                                      num_decision=2, supervision=False, input_col_is_dirty=True):
        # change the format of dict to key=root, value=category
        bag_words = Pexpansion.upside_down_dictionary(bag_words)  # O(1) for Key Search

        # clean data & change to hotvec & Prepare a dictionary of belonging
        df_hotvec_phrase, dict_vote_words, dict_vote_sentences = TextAnalysis.clean_until_guess(df, input_col,
                                                                                                bag_words,
                                                                                                sentences_bag,
                                                                                                num_decision=num_decision,
                                                                                                input_col_is_dirty=input_col_is_dirty)

        # if supervision mode end and return dict_vote_words, dict_vote_sentences
        if supervision == True:
            return dict_vote_words, dict_vote_sentences

        ls_categories1 = TextAnalysis.make_votevec_from_hotvec(df_hotvec_phrase, "word", dict_vote_words)
        ls_categories2 = TextAnalysis.make_votevec_from_hotvec(df_hotvec_phrase, "sentence", dict_vote_sentences)
        ls_categories = ls_categories1 + ls_categories2
        df_votevec = TextAnalysis.del_unuseful_cols_to_get_resultvec_df(df_hotvec_phrase)

        # output 
        TextAnalysis.make_resultcol_category_col(df, df_votevec, ls_categories, name_output_col)
        df[name_output_col] = df_votevec[name_output_col]
        Clean.replace_empty_value_to_npnan(df, name_output_col)

    @staticmethod
    def make_resultcol_multicategory_col(df, df_hotvec_phrase, combain_dict, name_output_col):
        for k in combain_dict.keys():
            value_text = ", ".join(sorted(combain_dict[k]))
            df_hotvec_phrase.loc[df_hotvec_phrase[k] == 1, name_output_col] = value_text
        return df

    @staticmethod
    def analyze_text_for_multicategory_col(df, input_col, name_output_col, bag_words, sentences_bag,
                                           num_decision=2, supervision=False, num_decision_supervision=2,
                                           input_col_is_dirty=True):
        """ 
        input:
        bag_words/sentences_bag: dict
            {"categty":["stem(word)","stem(word)", "stem(word)"],
            "critical":["critic", "intens", "sever"]}
            """
        if input_col in df.columns:
            print("{0}--------------------".format(input_col))


        bag_words = Pexpansion.upside_down_dictionary(bag_words)  # O(1) for Key Search

        # clean data & change to hotvec & Prepare a dictionary of belonging
        df_hotvec_phrase, dict_vote_words, dict_vote_sentences = TextAnalysis.clean_until_guess(df, input_col,
                                                                                                bag_words,
                                                                                                sentences_bag,
                                                                                                num_decision=num_decision,
                                                                                                input_col_is_dirty=input_col_is_dirty)

        combain_dict = Pexpansion.merge_dicts(dict_vote_words, dict_vote_sentences)

        # if supervision mode end and return dict_vote_words, dict_vote_sentences
        if supervision == True:
            return TextAnalysis.supervision(combain_dict, num_decision_supervision=num_decision_supervision)

        # output 
        TextAnalysis.make_resultcol_multicategory_col(df, df_hotvec_phrase, combain_dict, name_output_col)
        df[name_output_col] = df_hotvec_phrase[name_output_col]
        Clean.replace_empty_value_to_npnan(df, name_output_col)

    @staticmethod
    def v():
        print(73)
