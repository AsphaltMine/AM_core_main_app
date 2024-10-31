""" Utilities for dictionaries
"""


def get_dict_keys(dictionary):
    """Retrieve all keys in a nested dictionary.

    Args:
        dictionary (dict): The dictionary to retrieve the keys from.

    Returns:
        set: The keys located in the dictionary.
    """
    keys = set()

    for key, value in dictionary.items():
        keys.add(key)
        if isinstance(value, dict):
            keys.update(get_dict_keys(value))

    return keys


def get_dict_text(dictionary):
    """Flatten a nested dictionary into a single string holding every element
    name and every leaf value it contains. Numbers are rendered as text so that
    they can be searched like any other value, and duplicates are dropped to
    keep the result small on records with many repeated elements.

    Args:
        dictionary (dict): The dictionary to flatten.

    Returns:
        str: Space separated element names and values.
    """
    tokens = []

    def collect(value, key=None):
        """Append the element name, then walk down to the leaf values."""
        if key:
            # "@attribute" and "#text" are xmltodict markers, not element names
            tokens.append(str(key).lstrip("@#"))

        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                collect(sub_value, sub_key)
        elif isinstance(value, (list, tuple)):
            for item in value:
                collect(item)
        elif value is not None:
            tokens.append(str(value))

    collect(dictionary)
    return " ".join(dict.fromkeys(tokens))
