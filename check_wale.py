#!/usr/bin/python
# orig: https://github.com/APSL/postgresql-wal-e-nagios/blob/master/check_wale.py
### Check if the backup wal-e postgres is executed in the last day

import subprocess
import sys
from datetime import datetime, timedelta
import time

command = "/usr/local/bin/wal-e-wrapper backup-list 2>/dev/null| tail -1"

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
last =  output

# add regex check here matching if the output is really a wal-e line with a date.
# if not, exit 3
last_string = last.split()[1][:-5]
last_datetime = datetime.strptime(last_string, "%Y-%m-%dT%H:%M:%S")
#print last_datetime

last_expected = datetime.now() - timedelta(hours=28)
#print last_expected

if last_datetime < last_expected:
    print "CRITICAL - Last backup via wal-e more than a day ago: %s !" % last_datetime
    sys.exit(2)
else:
    print "OK - Backup correct. Last backup is from: %s" % last_datetime
    sys.exit(0)
