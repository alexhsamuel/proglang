from   cron import *

holidays = (
    ("New Year's Day", 2016/Jan/1),
    ("Martin Luther King, Jr. Day", 2016/Jan/18),
    ("Presidents' Day", 2016/Feb/15),
    ("Good Friday", 2016/Mar/25),
    ("Memorial Day", 2016/May/30),
    ("Independence Day", 2016/Jul/4),
    ("Labor Day", 2016/Sep/5),
    ("Thanksgiving Day", 2016/Nov/24),
    ("Christmas (Observed)", 2016/Dec/26),
    ("New Year's Day", 2015/Jan/1),
    ("Martin Luther King, Jr. Day", 2015/Jan/19),
    ("Presidents' Day", 2015/Feb/16),
    ("Good Friday", 2015/Apr/3),
    ("Memorial Day", 2015/May/25),
    ("Independence Day", 2015/Jul/3),
    ("Labor Day", 2015/Sep/7),
    ("Thanksgiving Day", 2015/Nov/26),
    ("Christmas", 2015/Dec/25),
    ("New Year's Day", 2014/Jan/1),
    ("Martin Luther King, Jr. Day", 2014/Jan/20),
    ("Presidents' Day", 2014/Feb/17),
    ("Good Friday", 2014/Apr/18),
    ("Memorial Day", 2014/May/26),
    ("Independence Day", 2014/Jul/4),
    ("Labor Day", 2014/Sep/1),
    ("Thanksgiving Day", 2014/Nov/27),
    ("Christmas", 2014/Dec/25),
    ("New Year's Day", 2013/Jan/1),
    ("Martin Luther King, Jr. Day", 2013/Jan/21),
    ("Presidents' Day", 2013/Feb/18),
    ("Good Friday", 2013/Mar/29),
    ("Memorial Day", 2013/May/27),
    ("Independence Day", 2013/Jul/4),
    ("Labor Day", 2013/Sep/2),
    ("Thanksgiving Day", 2013/Nov/28),
    ("Christmas", 2013/Dec/25),
    ("New Year's Day", 2012/Jan/2),
    ("Martin Luther King, Jr. Day", 2012/Jan/16),
    ("Presidents' Day", 2012/Feb/20),
    ("Good Friday", 2012/Apr/6),
    ("Memorial Day", 2012/May/28),
    ("Independence Day", 2012/Jul/4),
    ("Labor Day", 2012/Sep/3),
    ("Thanksgiving Day", 2012/Nov/22),
    ("Christmas", 2012/Dec/25),
    )

half_days = (
    2016/Nov/25,
    2015/Nov/27,
    2015/Dec/24,
    2014/Jul/3,
    2014/Nov/28,
    2014/Dec/24,
    2013/Jul/3,
    2013/Nov/29,
    2013/Dec/24,
    2012/Jul/3,
    2012/Nov/23,
    2012/Dec/24,
    )

holiday_dates = tuple( d for _, d in holidays )

d = 2012/Jan/1
while d < 2017/Jan/1:
    if d.weekday not in (Sat, Sun) and d not in holiday_dates:
        print(d)
    d += 1

