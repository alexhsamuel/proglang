extern crate datecalc;

use datecalc::*;

fn main() {
    for y in 1 .. 10000 {
        print!("{:04} {:1}\n", y, get_weekday(Date::new(y as Year, 1, 1)));
    }
}
