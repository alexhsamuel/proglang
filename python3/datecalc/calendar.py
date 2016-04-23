import builtins
import datetime

from   . import parse_date

#-------------------------------------------------------------------------------

DAY = datetime.timedelta(1)

class Calendar:
    """
    Abstract calendar base class.  A calendar is semantically a set of days.

    A concrete calendar provides `__contains__()`, and optionally an override
    for `find()`.
    """

    def find(self, date, forward):
        """
        Finds the nearest next or previous date.

        If `forward` is true, returns the earliest day in the calendar on or
        after `date`; otherwise, the latest day in the calendar on or before
        `date`.
        """
        while date not in self:
            date += DAY if forward else -DAY
        return date



class AllCalendar(Calendar):

    def __contains__(self, date):
        return isinstance(date, datetime.date)



class WeekdayCalendar(Calendar):

    def __contains__(self, date):
        return isinstance(date, datetime.date) and date.weekday() < 5



#-------------------------------------------------------------------------------

class DatesCalendar(Calendar):
    """
    A calendar consisting of an explicit collection of dates.
    """

    def __init__(self, dates):
        self.__dates = frozenset(dates)
        assert all( isinstance(d, datetime.date) for d in self.__dates )


    def __contains__(self, date):
        return date in self.__dates



def load_calendar(path):
    with open(path, "r") as file:
        dates = ( parse_date(l.strip()) for l in file )
        return DatesCalendar(dates)


def get_calendar(name):
    if name == "all":
        return AllCalendar()
    elif name == "weekday":
        return WeekdayCalendar()
    else:
        return load_calendar(name)


#-------------------------------------------------------------------------------

def shift(calendar, date, offset):
    """
    Shifts a date forward or backward in a calendar.

    `date` must be in the calendar. 
    """
    if date not in calendar:
        raise ValueError("not in calendar: {}".format(date))

    if offset == 0:
        return date

    forward = offset > 0
    shift = DAY if forward else -DAY
    for _ in builtins.range(abs(offset)):
        date = calendar.find(date + shift, forward)
    return date
            

def range(calendar, date0, date1, inclusive=False):
    """
    Generates sequential dates in a calendar.

    Yields dates in `calendar` starting with `date0`, which must be in the
    calendar, and continuing as long as the date is less than `date1`, which
    must be not before `date0`.
    """
    if date0 not in calendar:
        raise ValueError("not in calendar: {}".format(date0))
    if date1 < date0:
        raise ValueError("dates out of order")

    date = date0
    while date < date1 or (inclusive and date == date1):
        yield date
        date = calendar.find(date + DAY, True)


def offset(calendar, date0, date1):
    """
    Returns the number of dates in a calendar between two days.  

    The return value is the offset such that `shift(calendar, date0, offset) ==
    date1`.  Both dates must be in the calendar.
    """
    for date in date0, date1:
        if date not in calendar:
            raise ValueError("not in calendar: {}".format(date))

    offset = 0
    delta = 1 if date1 > date0 else -1
    date = date0
    while date != date1:
        offset += delta
        date = shift(calendar, date, delta)
    return offset


