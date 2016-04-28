package calendar

import (
	"date"
)

type Calendar interface {
	contains(date date.Date) bool
}

func find(cal Calendar, date date.Date, forward bool) date.Date {
	for !cal.contains(date) {
		date = date.Shift(forward)
	}
	return date
}

type AllCalendar struct {
}

func (cal AllCalendar) contains(date.Date) bool {
	return true
}

type WeekdayCalendar struct {
}

func (cal WeekdayCalendar) contains(d date.Date) bool {
	return date.GetWeekday(d) < 5
}

func abs(val int) int {
	if (val < 0) {
		return -val
	} else {
		return val
	}
}

func Shift(cal Calendar, d date.Date, offset int) date.Date {
	if !cal.contains(d) {
		panic("date not in calendar")
	}

	if (offset == 0) {
		return d
	}

	forward := offset > 0
	for i := 0; i < abs(offset); i += 1 {
		d = find(cal, d.Shift(forward), forward)
	}
	return d
}

func Range(cal Calendar, date0 date.Date, date1 date.Date, inclusive bool) []date.Date {
	if !cal.contains(date0) {
		panic("date0 not in calendar")
	}
	if date.Less(date1, date0) {
		panic("dates out of order")
	}

	d := date0
	dates := make([]date.Date, 0)
	for date.Less(d, date1) || (inclusive && d == date1) {
		dates = append(dates, d)
		d = find(cal, d, true)
	}
	return dates
}

func Offset(cal Calendar, date0 date.Date, date1 date.Date) int {
	if !cal.contains(date0) {
		panic("date0 not in calendar")
	}
	if !cal.contains(date1) {
		panic("date1 not in calendar")
	}

	offset := 0
	var delta int
	if date.Less(date0, date1) {
		delta = 1
	} else {
		delta = -1
	}
	date := date0
	for date != date1 {
		offset += delta
		date = Shift(cal, date, delta)
	}
	return offset
}

