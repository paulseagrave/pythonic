'''
Clock module
This is largely copied from another submission. Although
the previous iteration was valid and working this is much more
elegant.
'''
class Clock:
    def __init__(self, hours, minutes):
        self._hours = hours
        self._minutes = minutes
        self.fix()

    def __repr__(self):
        return 'Clock({!r}, {!r})'.format(self._hours, self._minutes)

    def __str__(self):
        return '{:02d}:{:02d}'.format(self._hours, self._minutes)

    def __eq__(self, other):
        if self.hours == other.hours and self.minutes == other.minutes:
            return True
        return False

    @property
    def minutes(self):
        return self._minutes

    @property
    def hours(self):
        return self._hours

    def fix_hours(self):
        self._hours = self._hours % 24

    def fix_mins(self):
        self._hours += self._minutes // 60
        self._minutes = self._minutes % 60

    def fix(self):
        self.fix_mins()
        self.fix_hours()

    def add(self, more):
        self._minutes += more
        self.fix()
        return self
