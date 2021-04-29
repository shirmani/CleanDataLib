import pytest
from clean import *
import numpy as np
from CleanData.tool_for_test import *


class TestClean:

    def test_replace_value_by_comparison_value_replace_value(self):
        df = pd.DataFrame({"a": ["x", "ax", np.nan]})
        Clean.replace_value_by_comparison(df, "a", {"v": ["x"]})
        target = pd.DataFrame({"a": ["v", "ax", np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_value_by_comparison_npnan_replace_value(self):
        df = pd.DataFrame({"a": ["x", "ax", np.nan]})
        Clean.replace_value_by_comparison(df, "a", {np.nan: ["x"]})
        target = pd.DataFrame({"a": [np.nan, "ax", np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_value_by_comparison_int_col(self):
        df = pd.DataFrame({"a": [1, 2, np.nan]})
        Clean.replace_value_by_comparison(df, "a", {np.nan: ["x"]})
        target = pd.DataFrame({"a": [1, 2, np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_value_by_comparison_different_output_col(self):
        df = pd.DataFrame({"a": ["x", "ax", np.nan]})
        Clean.replace_value_by_comparison(df, "a", {np.nan: ["x"]}, name_output_col="b")
        target = pd.DataFrame({"a": ["x", "ax", np.nan],
                               "b": [np.nan, "ax", np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_value_by_contained_x(self):
        df = pd.DataFrame({"a": ["x", "ax", np.nan]})
        Clean.replace_value_by_contained_x(df, "a", {"v": ["x"]})
        target = pd.DataFrame({"a": ["v", "v", np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_value_by_contained_x_npnan_replace_value(self):
        df = pd.DataFrame({"a": ["x", "ax", np.nan]})
        Clean.replace_value_by_contained_x(df, "a", {np.nan: ["x"]})
        target = pd.DataFrame({"a": [np.nan, np.nan, np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_value_by_contained_x_int_col(self):
        df = pd.DataFrame({"a": [1, 2, np.nan]})
        Clean.replace_value_by_contained_x(df, "a", {np.nan: ["x"]})
        target = pd.DataFrame({"a": [1, 2, np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_replace_empty_value_to_npnan(self):
        df = pd.DataFrame({"a": [None, "nan", " ", "s", "na", np.nan]})
        Clean.replace_empty_value_to_npnan(df, "a")
        target = pd.DataFrame({"a": [np.nan, np.nan, np.nan, "s", "na", np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_add_comma_to_notnull_value_in_col(self):
        df = pd.DataFrame({"a": [None, "nan", " ", "s", "na", np.nan]})
        Clean.add_comma_to_notnull_value_in_col(df, "a")
        target = pd.DataFrame({"a": [np.nan, np.nan, np.nan, "s,", "na,", np.nan]})
        assert Tool.compare_dfs(df, target)

    def test_clean_text_col_from_punctuation(self):
        df = pd.DataFrame({"a": [None, "    ", "ee,ee", "tt-ss", "sff!", 2, np.nan]})
        Clean.clean_text_col_from_punctuation(df, "a")
        target = pd.DataFrame({"a": [None, "    ", "ee ee", "tt ss", "sff ", 2, np.nan]})
        assert Tool.compare_dfs(df, target)

    """problem: ["22","22"] == "22 22" => True """
    def test_change_words_col_to_ls_word_col(self):
        pass
        # df = pd.DataFrame({"a": ["woer swsw", None, " ", "ee,ee",
        #                          "tt-ss", "sff!", 2, np.nan, "22 22"]})
        # # Clean.change_words_col_to_ls_word_col(df, "a")
        # target = pd.DataFrame({"a": [["woer", "swsw"], np.nan, np.nan, ["ee" "ee"],
        #                              ["tt", "ss"], ["sff"], 2, np.nan, "22 22"]})
        # assert Tool.compare_dfs(df, target)


if __name__ == "__main__":
    pytest.main()
