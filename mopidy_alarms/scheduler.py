from __future__ import unicode_literals
import pykka
import logging
import schedule
import time

class AlarmsScheduler(pykka.ThreadingActor,):


    def __init__(self, alarmsactor=pykka.ThreadingActor ):
        super(AlarmsScheduler, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Background scheduler started")
        while True:
            self.logger.info("Run pending schedules:")
            alarmsactor.tell({'msg':'run_pending'})

            time.sleep(60)
