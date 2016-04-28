package date

import (
	"testing"
)

func TestIsLeapYear1(t *testing.T) {
	if   IsLeapYear(1999) ||
		!IsLeapYear(2000) ||
	 	 IsLeapYear(2001) ||
		 IsLeapYear(2002) ||
		!IsLeapYear(2004) ||
		!IsLeapYear(2040) ||
		 IsLeapYear(2100) {
		t.Fail()
	}
}

func TestValid(t *testing.T) {
	for _, d := range []Date{
		{   0,  1,  1},
		{  -1,  1,  1},
		{   1,  0,  1},
		{   1, 13,  1},
		{   1, 13,  1},
		{   1,  1,  0},
		{   1,  1, 32},
		{   1,  2, 29},
		{   1,  2, 30},
		{   1,  4, 31},
        {   1, 11, 31},
	} { if d.Valid() { t.Fail() } }

	for _, d := range []Date{
		{   1,  1,  1},
		{   1,  1, 31},
		{   1,  2, 28},
		{   1,  3,  1},
		{   1, 11, 30},
		{   1, 12, 31},
		{2000,  2, 28},
		{2000,  2, 29},
		{9999, 12, 31},
	} { if !d.Valid() { t.Fail() } }
}

func TestDaysInMonth(t *testing.T) {
	if DaysInMonth(1, 1) != 31 {
		t.Fail()
	}
}

func TestShift(t *testing.T) {
	if  (Date{   1,  1,  1}).Shift(  1) != (Date{   1,  1,  2}) ||
		(Date{   1,  1,  1}).Shift(  2) != (Date{   1,  1,  3}) ||
		(Date{   1,  1,  1}).Shift( 30) != (Date{   1,  1, 31}) ||
		(Date{   1,  1,  1}).Shift( 31) != (Date{   1,  2,  1}) ||
		(Date{   1,  1,  1}).Shift(365) != (Date{   2,  1,  1}) ||
		(Date{   1, 12, 31}).Shift(  1) != (Date{   2,  1,  1}) { 
		t.Fail() 
	}
}

func TestGetWeekday(t *testing.T) {
	if  GetWeekday(Date{1973, 12,  3}) != 0 ||
		GetWeekday(Date{2016,  4, 28}) != 3 ||
		GetWeekday(Date{2016,  5,  1}) != 6 {
		t.Fail()
	}
}
