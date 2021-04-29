import pytest
from python_expansion import *


class TestPexpansion:

    def test_if_x_not_ls_make_x_ls_str(self):
        x = "[ss]"
        result = Pexpansion.if_x_not_ls_make_x_ls(x)
        target = ["[ss]"]
        assert target == result

    def test_if_x_not_ls_make_x_ls_float(self):
        x = 1.0
        result = Pexpansion.if_x_not_ls_make_x_ls(x)
        target = [1.0]
        assert target == result

    def test_if_x_not_ls_make_x_ls_int(self):
        x = 1
        result = Pexpansion.if_x_not_ls_make_x_ls(x)
        target = [1]
        assert target == result

    def test_if_x_not_ls_make_x_ls_bool(self):
        x = True
        result = Pexpansion.if_x_not_ls_make_x_ls(x)
        target = [True]
        assert target == result

    def test_flatten_ls(self):
        ls = [None, [444, 'lfggfg', [['l']], 'r'], 'ldededw', 333, 111,
              11, 1, 3, 3, 4343, 34, (4.21232, 45, 34343), 55, 5, 4343, 5,
              3, 3, 3, 33, 4343, 3, [[3, True], 23], 2, 2, 22, 12, 1]

        result = Pexpansion.flatten_ls(ls)

        target = [None, 444, 'lfggfg', 'l', 'r', 'ldededw', 333, 111,
                  11, 1, 3, 3, 4343, 34, 4.21232, 45, 34343, 55, 5, 4343, 5,
                  3, 3, 3, 33, 4343, 3, 3, True, 23, 2, 2, 22, 12, 1]
        assert target == result

    def test_flatten_ls_with_dict(self):
        ls = [None, 444, {"s": [1, 22, 23, 3], 122: ["wqw", "dwdw"]},
              'lfggfg', 'l', 'r', ('ldededw', 333), 111,
              11, [[1, 3, [3, 4343, [[[34]]], 4.21232]], 45, 34343, 55, 5], 4343, 5,
              3, 3, 3, 33, 4343, 3, 3, True, 23, 2, 2, 22, 12, 1]

        result = Pexpansion.flatten_ls(ls)

        target = [None, 444, {"s": [1, 22, 23, 3], 122: ["wqw", "dwdw"]},
                  'lfggfg', 'l', 'r', 'ldededw', 333, 111,
                  11, 1, 3, 3, 4343, 34, 4.21232, 45, 34343, 55, 5, 4343, 5,
                  3, 3, 3, 33, 4343, 3, 3, True, 23, 2, 2, 22, 12, 1]
        assert target == result

    def test_get_key_from_dict_by_value(self):
        dictionary = {"k": [1,2,"a"],
                      "v": "2132"}
        result = Pexpansion.get_key_from_dict_by_value(dictionary, "2132")
        target = "v"
        assert target == result

    def test_get_key_from_dict_by_value_x_not_exist(self):
        dictionary = {"k": [1, 2, "ax"],
                      "v": "2132"}
        result = Pexpansion.get_key_from_dict_by_value(dictionary, "45")
        target = None
        assert target == result

    def test_get_key_from_dict_by_value_ls(self):
        dictionary = {"k": [1, 2, "a"],
                      "v": "2132"}
        result = Pexpansion.get_key_from_dict_by_value(dictionary, "a")
        target = "k"
        assert target == result

    def test_get_key_from_dict_by_value_contain_x(self):
        dictionary = {"k": [1, 2, "ax"],
                      "v": "2132"}
        result = Pexpansion.get_key_from_dict_by_value(dictionary, "a")
        target = "k"
        assert target != result

    # def test_merge_dicts(self):
    #     dict1 = {"k": [1, 2, "ax"],
    #          "v": "2132",
    #          "s": 54}
    #     dict2 = {"ak": [1, 2, "ax"],
    #          "v": ["2132", "eee"],
    #          "s": 223}
    #     result = Pexpansion.merge_dicts(dict1, dict2)
    #     target = {"k": [1, 2, "ax"],
    #           "ak": [1, 2, "ax"],
    #           "v": ["2132", "eee"],
    #           "s": [223, 54]}
    #     assert target == result

    def test_upside_down_dictionary(self):
        dictionary = {"k": [1],
                      "v": "2132",
                      "l": ["ww", 3]}
        result = Pexpansion.upside_down_dictionary(dictionary)
        target = {1: "k",
                  "2132": "v",
                  "ww": "l",
                  3: "l"}
        assert target == result

    def test_replace_str_by_comparison(self):
        string = "polpmn  , 880b, g "
        result = Pexpansion.replace_str_by_comparison(string,
                                                      {"": ["p", "8", " "],
                                                       "*": ["m", "n", "k"]})
        target = "ol**,0b,g"
        assert target == result


    # def test_remove_from_ls(self):
    #     ls = [3.4, True, ["r","g",4], "trr", ]
    #     result = Pexpansion.remove_from_ls(ls, ["r", True, None])
    #     target = [3.4, ["g",4], "trr", ]
    #     assert target == result

    # def test_from_ls_to_str_comma_separated(self):
    #     ls = [False, None, "", "abc", 123, 34.5, "   ", ["rrr", "  ", 443],]
    #     result = Pexpansion.from_ls_to_str_comma_separated(ls)
    #
    #     assert target == result


    def test_del_duplicate_categories_in_multicategories_str(self):
        string = "aa,23212,U H,U h,^^$,aa,U H,true, aa"
        result = Pexpansion.del_duplicate_categories_in_multicategories_str(string)
        target = " aa,23212,U H,U h,^^$,aa,true"
        assert target == result

    def test_str_of_dicts_keys(self):
        dict_a = {"k": [1],
                  "v": "2132",
                  "l": ["ww", 3]}

        dict_b = {1: "k",
                  "2132": "v",
                  True: "l",
                  "k": "l"}
        result = Pexpansion.str_of_dicts_keys([dict_b,  dict_a])
        target = "[1, '2132', 'k'], ['k', 'v', 'l']"
        assert target == result





if __name__ == "__main__":
    pytest.main()
