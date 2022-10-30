# misc/common_functions.py

import logging  # noqa


# find value in a list of similar dicts
def dict_list_search(dict_list,
                     key_to_find_dict,
                     val_to_find_dict,
                     key_for_search):
    return list(filter(
        None,
        [
            the_dict
            if the_dict[key_to_find_dict] == val_to_find_dict else None
            for the_dict in dict_list
        ]
    ))[0][key_for_search]

