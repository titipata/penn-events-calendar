import os
import sys
from crontab import CronTab

cron = CronTab(user='')  # put your user name here
cron.remove_all()
print('Len of crontab =', len(cron))

command = sys.executable + ' ' + os.path.join(os.getcwd(), 'fetch_events.py')
job = cron.new(command=command)
# job.minute.every(1) # for testing
job.day.every(1)
cron.write()
