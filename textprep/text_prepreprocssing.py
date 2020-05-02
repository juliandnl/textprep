"""Preprocessing for natural language processing.

@date: 02.05.2020
@author: Julian Kortendieck
@email: julian@dnlab.de
"""
import re
import string
import numpy as np
import pandas as pd
import Levenshtein
import nltk
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize

# own modules
from helper import most_common

nltk.download("stopwords")
nltk.download("punkt")


def find_dates_in_df(df):
    df["date"] = df["text"].apply(
        lambda text: find_dates(text)
    )
    return df


def find_dates(text):
    # r = re.compile(DATE)
    m = regex_date.search(text)
    if m:
        return m[0]
    return None


def find_numbers(text):
    # r = re.compile(NUMBER)
    m = regex_number.match(text)
    if m:
        return m[0]
    return None


def find_numbers_in_df(df):
    df.loc[:, "number"] = df["text"][df["text"].str.match(NUMBER)]
    return df


def find_numbers_percentage_in_df(df):
    df.loc[:, "number_percentage"] = df["text"][df["text"].str.match(NUMBER_PERCENTAGE)]
    return df


def find_prev_year_in_df(df):
    df.loc[:, "prev_year"] = df["text"][df["text"].str.match(PREV_YEAR)]
    return df


def find_numbers_percentage(text):
    # r = re.compile(NUMBER_PERCENTAGE)
    m = regex_number_percentage.match(text)
    if m:
        return m[0]
    return None


def find_notes(text):
    """Regex for finding notes"""
    m = regex_notes.search(text)
    if m:
        return m[0]
    return None


def find_change(text):
    """Regex for finding change"""
    m = regex_change.search(text)
    if m:
        return m[0]
    return None


def find_currency(df):
    """find currency in the df, add column to df indicating which token contains currency
    and return the currency as string."""
    doc_currency = ""
    # euros = "Euro|€|EUR"
    # dollars = "Dollar|\$|USD|dols"
    # pounds = "£|GBP|BP"
    currencies = {"euro": EUROS, "dollar": DOLLARS, "pound": POUNDS}

    for key, value in currencies.items():
        if df.apply(lambda x: x.str.contains(value, case=False).any(), axis=1).any(
            axis=None
        ):
            # If doc_currency is set two times => set undefined
            if doc_currency:
                doc_currency = "euro"  # "undefined"
                break
            # Set doc currency
            else:
                doc_currency = key

    # Create column for unit in df marking the token which contains unit
    df.loc[:, "currency"] = False
    for key, value in currencies.items():
        df.loc[df["text"].str.contains(value, case=False), "currency"] = True
    # Set default unit to 1
    if not doc_currency:
        doc_currency = "euro"
    return doc_currency


def find_unit(df):
    """find unit in the df, add column to df indicating which token contains unit
    and return the unit as string."""
    doc_unit = ""
    # thousand = "(\$)(0){3}|thousand|€(\s*)thous|TEUR|T(\s*)€|Tsd|Tausend"
    # million = "millions|million|£(\s*)m|$(\s*)m|€(\s*)m|mn|mio(\s*)€|in(\s+)mio|MM|\d+(M){1}"
    # billion = "billion|Bn|Mrd|Md"
    units = {"thousand": THOUSAND, "million": MILLION, "billion": BILLION}

    for key, value in units.items():
        if df.apply(lambda x: x.str.contains(value, case=True).any(), axis=1).any(
            axis=None
        ):
            # If doc_unit is set two times => set undefined
            if doc_unit:
                doc_unit = "1"
                break
            # Set doc currency
            else:
                doc_unit = key
    # Create column for unit in df marking the token which contains unit
    df.loc[:, "unit"] = False
    for key, value in units.items():
        df.loc[df["text"].str.contains(value, case=True), "unit"] = True
    # Set default unit to 1
    if not doc_unit:
        doc_unit = "1"
    return doc_unit


def group_token_by_page(df):
    # combines all tokens on each page
    df_pages = (
        df.groupby("page")["token"]
        .apply(lambda t: [w for w in t if not pd.isnull(w)])  # w=word t=token
        .to_frame()
    )
    return df_pages


def df_dropna(df):
    return df[df["text"].notna()]


def check_distance(token, search_terms):
    distance = [Levenshtein.distance(token, s) for s in search_terms]
    return search_terms[np.argmin(distance)], np.min(distance)


def remove_punctuation(text):
    for p in string.punctuation:
        text = str(text).replace(p, "")
    return text


def remove_punctuation_pd(text):
    for p in string.punctuation:
        text = text.str.replace(p, "")
    return text


def remove_stopwords(text):
    if text in stopwords.words("english"):
        return pd.np.nan
    else:
        return text


class Detect_language:
    """"detects the language either of a string or a list of strings"""

    def __init__(self):
        self.short = {"english": "en", "german": "de", "french": "fr", "spanish": "es"}

    def detect_language(self, text):
        languages_ratios = {}
        tokens = wordpunct_tokenize(text)
        words = [clean_for_map(word) for word in tokens]
        languages = ["english", "german", "french", "spanish"]

        for language in languages:
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)
            languages_ratios[language] = len(common_elements)

        most_rated_language = max(languages_ratios, key=languages_ratios.get)

        try:
            short_lang = self.short[most_rated_language]
        except KeyError:
            short_lang = ""

        return short_lang

    def detect_language_loop(self, token_list):
        languages = []
        for token in token_list:
            languages.append(self.detect_language(token))
        return max(set(languages), key=languages.count)


def clean_for_map(token, min_len=2):
    """Clean token for mapping. Transforms it to lowercase, cleans punctuation,
    numbers, words with less then min_len characters."""
    t = token.translate(str.maketrans("", "", string.punctuation))
    t_clean = str(roman_to_int(t))
    t_clean = t_clean.lower()
    t_clean = re.sub("[^a-zA-Z]+", "", t_clean)
    if len(t_clean) < min_len:
        t_clean = ""

    return t_clean


def clean_list(input_labels):
    """Clean list of tokens, same methods as for token"""
    labels_tokenized = [nltk.word_tokenize(word) for word in input_labels]
    labels_cleaned = [[clean_for_map(word) for word in xbrl_token] for xbrl_token in labels_tokenized]
    labels = [str.join(" ", [x for x in i if len(x) > 0]) for i in labels_cleaned]
    return labels


def clean_token(token):
    """clean token, same methods as for list"""
    token_list = nltk.word_tokenize(token)
    token_list = [clean_for_map(i) for i in token_list]
    token = str.join(" ", [x for x in token_list if len(x) > 0])
    return token


def test_for_number(string):
    if re.search(r'\d', string) and not re.search("[a-zA-Z]", string):
        return True
    else:
        return False


def find_num_regex(string):
    for numerical_system, regex_list in num_regex.items():
        # test for date
        if date_regex.search(string):
            continue
        for regex in regex_list:
            m = regex.search(string)
            if m:
                return numerical_system


def test_for_numerical_system(string_list, default="us"):
    """ test string if numerical, then which numerical system it contains"""
    found_systems = []
    for _string in string_list:
        if test_for_number(_string):
            system = find_num_regex(_string)
            if system:
                found_systems.append(system)
    if found_systems:
        return most_common(found_systems)
    else:
        return default


def roman_to_int(s):
    try:
        # Excluded bigger roman numbers 'L': 50, 'C': 100, 'D': 500, 'M': 1000
        rom_val = {'I': 1, 'V': 5, 'X': 10}
        int_val = 0
        for i, item in enumerate(s):
            if i > 0 and rom_val[item] > rom_val[s[i - 1]]:
                int_val += rom_val[item] - 2 * rom_val[s[i - 1]]
            else:
                int_val += rom_val[item]
    except KeyError:
        int_val = s
    return int_val
