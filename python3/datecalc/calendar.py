import datetime

from   . import parse_date

#-------------------------------------------------------------------------------

DAY = datetime.timedelta(1)

class Calendar:

    def _check(self, date):
        if date not in self:
            raise ValueError("date not in calendar: {}".format(date))


    def to(self, date, forward):
        while date not in self:
            date += DAY if forward else -DAY
        return date


    def add(self, date, count):
        self._check(date)

        if count == 0:
            return date

        shift = DAY if count > 0 else -DAY
        for _ in range(abs(count)):
            date = self.to(date + shift, count > 0)
        return date
            


class AllCalendar(Calendar):

    def __contains__(self, date):
        return isinstance(date, datetime.date)



class WeekdayCalendar(Calendar):

    def __contains__(self, date):
        return isinstance(date, datetime.date) and date.weekday() < 5



#-------------------------------------------------------------------------------

class DatesCalendar(Calendar):

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



