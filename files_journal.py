import sys
import os
import stat
import datetime

date = datetime.date.today()
home = sys.argv[1]
journaldir = os.path.join(home, "journal")
yeardir = os.path.join(journaldir, str(date.year))
monthdir = os.path.join(yeardir, str(date.month))
entry = os.path.join(monthdir, date.isoformat())
if not os.path.exists(home):
    print "Home %s not found" % home
    sys.exit(1)

for i in [journaldir, yeardir, monthdir]:
    if not os.path.exists(i):
        os.mkdir(i)
if not os.path.exists(entry):
    with open(entry, 'w') as f:
        f.write("")
print entry
