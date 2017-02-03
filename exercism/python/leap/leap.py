import calendar

def is_leap_year_library(year):
    '''
    Use pythons built in calendar module to check for leap year
    '''
    return calendar.isleap(year)

def is_leap_year(year):
    '''
    Calculate whether a year is a leap year
    '''
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        else:
            return False
    elif year % 4 == 0:
        return True
    else:
        return False
