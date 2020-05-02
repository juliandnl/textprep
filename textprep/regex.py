DATE = "|".join([str(y) for y in range(2000, datetime.now().year, 1)])
regex_date = re.compile(DATE)
# NUMBER = "^((?:[\-\(]{0,1}[\ ]{0,1})(?:[0-9]{1,3}){1}(?:\,[0-9]{3}){0,}(?:\.[0-9]{1,}){0,1}(?:[\ ]{0,1}[\)]{0,1}[\,]{0,1}))$"
NUMBER = "^((?:[\-\(]{0,1}[\ ]{0,1})(?:[0-9]{1,3}){1}(?:(\.|\,)[0-9]{3}){0,}(?:(\.|\,)[0-9]{1,}){0,1}(?:[\ ]{0,1}[\)]{0,1}[(\.|\,)]{0,1}))$"
regex_number = re.compile(NUMBER)
NUMBER_PERCENTAGE = "^((?:[\-\(]{0,1}[\ ]{0,1})(?:[0-9]{1,3}){1}(?:\,[0-9]{3}){0,}(?:\.[0-9]{1,}){0,1}(?:[\%]{1}[\)]{0,1}|[p]{2}[\)]{0,1}))$"
regex_number_percentage = re.compile(NUMBER_PERCENTAGE)
NOTES = "(Notes|Note|notes|note|Anhang|anhang)"
regex_notes = re.compile(NOTES)
CHANGE = "(Change|change|in %)"
regex_change = re.compile(CHANGE)
PREV_YEAR = "(Vorjahr)"

# CURRENCY REGEX
EUROS = "Euro|€|EUR"
DOLLARS = "Dollar|\$|USD|dols"
POUNDS = "£|GBP|BP"
CURRENCY = EUROS + DOLLARS + POUNDS
regex_currency = re.compile(CURRENCY, re.IGNORECASE)

# UNIT REGEX
# €000, thousand, Tsd, tausend, Eur thous, T Eur
THOUSAND = "(€|\$|£)(0){3}|(t|T){1}housand|Tsd|(t|T){1}ausend|(EUR|Eur|eur|€|\$|£)(\s*)thous|T(\s*)(EUR|Eur|eur|€|\$|£)"
# Million(s), € M, M €, Mio €, in Mio, 3 M
MILLION = "(m|M){1}illion(s){0,1}|(M){1}ILLION(S){0,1}|(£|\$|€)(\s*)(m|M)|(m|M)(\s*)(£|\$|€)|(m|M)io(\s*)(£|\$|€)|in(\s+)(m|M)io|\d+(M){1}"
# Billion(s), Bn, Mrd, Md
BILLION = "(b|B){1}illion(s){0,1}|Bn|(m|M){1}rd|Md"
UNIT = THOUSAND + MILLION + BILLION
regex_unit = re.compile(UNIT)


# numerical regex
us_thousand = re.compile("\,[0-9]{3}")
us_decimal = re.compile("\.[0-9]{1,2}(?![0-9])")
de_thousand = re.compile("\.[0-9]{3}")
de_decimal = re.compile("\,[0-9]{1,2}(?![0-9])")
num_regex = defaultdict(list)
num_regex["us"].append(us_thousand)
num_regex["us"].append(us_decimal)
num_regex["de"].append(de_thousand)
num_regex["de"].append(de_decimal)


# date regex
DATE = "|".join([str(y) for y in range(2000, datetime.now().year, 1)])
date_regex = re.compile(DATE)
