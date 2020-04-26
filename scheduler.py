'''
main scheduler of bots
running bots according of random deterministic
'''

import time
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def tick1():
    '''
    test function - make tick
    '''
    print('1 Tick! The time is: %s' % datetime.now())

def tick2():
    '''
    test function - make tick
    '''
    print('2 Tick! The time is: %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    #scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.add_job(tick1, 'date', run_date=datetime(2020, 4, 26, 17, 17))
    scheduler.add_job(tick2, 'date', run_date=datetime(2020, 4, 26, 17, 16))
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
            print(scheduler.get_jobs())
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
