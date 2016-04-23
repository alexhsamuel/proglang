import datetime
import time

#-------------------------------------------------------------------------------

def parse_date(date):
    """
    Parses an ISO 8601 date, and returns a `datetime.date`.
    """
    parts = time.strptime(date, "%Y-%m-%d")
    return datetime.date(parts.tm_year, parts.tm_mon, parts.tm_mday)



