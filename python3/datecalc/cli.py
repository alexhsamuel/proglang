import argparse
import datetime

from   .calendar import get_calendar
from   . import expr

#-------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--calendar", metavar="CALENDAR", default="all",
        help="name of calendar to use [default: all]")
    parser.add_argument(
        "expression", metavar="EXPRESSION",
        help="expression to evaluate")
    args = parser.parse_args()

    calendar = get_calendar(args.calendar)
    result = expr.evaluate(args.expression, calendar=calendar)

    if isinstance(result, int):
        print(result)
    elif isinstance(result, datetime.date):
        print(result)
    else:
        for res in result:
            print(res)


if __name__ == "__main__":
    main()


