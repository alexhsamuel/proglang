package date

type Year int
type Month int
type Day int
type Weekday int

func IsLeapYear(year Year) bool {
	return year%4 == 0 && (year%100 != 0 || year%400 == 0)
}

func DaysInMonth(year Year, month Month) Day {
	switch month {
	case 1, 3, 5, 7, 8, 10, 12:
		return 31
	case 4, 6, 9, 11:
		return 30
	case 2:
		if IsLeapYear(year) {
			return 29
		} else {
			return 28
		}
	default:
		panic("invalid month")
	}
}

type Date struct {
	Year  Year
	Month Month
	Day   Day
}

func (date Date) valid() bool {
	return 1 <= date.Year && date.Year <= 9999 &&
		1 <= date.Month && date.Month <= 12 &&
		1 <= date.Day && date.Day <= DaysInMonth(date.Year, date.Month)
}

func Less(date0 Date, date1 Date) bool {
	return date0.Year < date1.Year || 
		(date0.Year == date1.Year && (date0.Month < date0.Month ||
		(date0.Month == date1.Month && date0.Day < date1.Day)))
}

func (date Date) next() Date {
	date.Day += 1
	if date.Day > DaysInMonth(date.Year, date.Month) {
		date.Day = 1
		date.Month += 1
		if date.Month > 12 {
			date.Month = 1
			date.Year += 1
		}
	}
	return date
}

func (date Date) prev() Date {
	date.Day -= 1
	if date.Day == 0 {
		date.Month -= 1
		if date.Month == 0 {
			date.Year -= 1
			date.Month = 12
		}
		date.Day = DaysInMonth(date.Year, date.Month)
	}
	return date
}

func (date Date) Shift(forward bool) Date {
	if (forward) {
		return date.next()
	} else {
		return date.prev()
	}
}

var mTable = []int{1, 4, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5}
var cTable = []int{0, 5, 3, 1}

func GetWeekday(date Date) Weekday {
	// See https://en.wikipedia.org/wiki/Determination_of_the_day_of_the_week#Kraitchik.27s_variation
	m := mTable[date.Month - 1]
	s := int(date.Year) % 100
	y := (s + s / 4) % 7
	c := cTable[date.Year / 100 % 4]
	return Weekday((int(date.Day) + m + c + y + 5) % 7)
}

