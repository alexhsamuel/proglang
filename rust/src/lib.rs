/// Gregorican year.
///
/// Years 1 through 9999 are supported.
pub type Year = u16;

/// Month of the year, January=1 through December=12.
pub type Month = u8;

/// Day of the month, 1 through the number of days in the month.
pub type Day = u8;

/// Day of the week, Monday=0 through Sunday=6.
pub type Weekday = u8; 

pub fn is_leap_year(year: Year) -> bool {
    return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

pub fn days_in_month(year: Year, month: Month) -> Day {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => if is_leap_year(year) { 29 } else { 28 }, 
        _ => panic!("invalid month: {}", month),
    }
}

//------------------------------------------------------------------------------

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Date {
    year: Year,
    month: Month,
    day: Day,
}
    
fn between<T: std::cmp::PartialOrd>(min: T, value: T, max: T) -> bool {
    min <= value && value <= max
}

impl Date {
    pub fn new(year: Year, month: Month, day: Day) -> Date {
        let date = Date{ year: year, month: month, day: day };
        assert!(date.valid());
        date
    }

    pub fn valid(&self) -> bool {
        between(1, self.year, 9999)
            && between(1, self.month, 12)
            && between(1, self.day, days_in_month(self.year, self.month))
    }

    pub fn next(&self) -> Date {
        let mut date = *self;
        date.day += 1;
        if date.day > days_in_month(date.year, date.month) {
            date.day = 1;
            date.month += 1;
            if date.month > 12 {
                date.month = 1;
                date.year += 1;
            }
        }
        date
    }

    pub fn prev(&self) -> Date {
        let mut date = *self;
        date.day -= 1;
        if date.day < 1 {
            date.month -= 1;
            if date.month < 1 {
                date.year -= 1;
                date.month = 12;
            }
            date.day = days_in_month(date.year, date.month);
        }
        date
    }

    pub fn shift(self, count: i32) -> Date {
        if count > 0 {
            (0 .. count).fold(self, |d, _| d.next())
        }
        else if count < 0 {
            (0 .. -count).fold(self, |d, _| d.prev())
        }
        else {
            self
        }
    }

}

const M_TABLE: [u8; 12] = [1, 4, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5];
const C_TABLE: [u8;  4] = [0, 5, 3, 1];

pub fn get_weekday(date: Date) -> Weekday {
    // See https://en.wikipedia.org/wiki/Determination_of_the_day_of_the_week#Kraitchik.27s_variation.
    let y = if date.month < 3 { date.year - 1 } else { date.year };
    let s = (y % 100) as u8;
    ((  C_TABLE[(y / 100 % 4) as usize]     // century leap years
      + s / 4                               // leap years
      + s                                   // years
      + M_TABLE[(date.month - 1) as usize]  // months
      + date.day                            // days
      + 5                                   // start on Monday
        ) % 7) as Weekday
      
}

//------------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_leap_year_test() {
        assert!(!is_leap_year(1999));
        assert!( is_leap_year(2000));
        assert!(!is_leap_year(2001));
        assert!(!is_leap_year(2002));
        assert!( is_leap_year(2004));
        assert!( is_leap_year(2040));
        assert!(!is_leap_year(2100));
    }

    #[test]
    fn shift_test() {
        let first = Date::new(1, 1, 1);
        assert_eq!(first.shift(  0), Date::new(1,  1,  1));
        assert_eq!(first.shift(  1), Date::new(1,  1,  2));
        assert_eq!(first.shift(  2), Date::new(1,  1,  3));
        assert_eq!(first.shift( 30), Date::new(1,  1, 31));
        assert_eq!(first.shift( 31), Date::new(1,  2,  1));
        assert_eq!(first.shift(365), Date::new(2,  1,  1));
        assert_eq!(Date::new(1, 12, 31).shift(1), Date::new(2, 1, 1));
    }

    #[test]
    fn get_weekday_test() {
        assert_eq!(get_weekday(Date::new(   1,  1,  1)), 0);
        assert_eq!(get_weekday(Date::new(1973, 12,  3)), 0);
        assert_eq!(get_weekday(Date::new(2016,  1,  1)), 4);
        assert_eq!(get_weekday(Date::new(2016,  4, 28)), 3);
        assert_eq!(get_weekday(Date::new(2016,  5,  1)), 6);
        assert_eq!(get_weekday(Date::new(9600,  1,  1)), 5);
        assert_eq!(get_weekday(Date::new(9900,  1,  1)), 0);
        assert_eq!(get_weekday(Date::new(9999, 12, 31)), 4);
    }

}

