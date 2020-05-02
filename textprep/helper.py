def most_common(lst):
    """find most common value in list"""
    return max(set(lst), key=lst.count)


def create_today_as_string():
    """Use datetime date, isoformat with YYYYMMDD as string."""
    d = date.today().isoformat()
    date_string = d.replace("-", "")
    return date_string
