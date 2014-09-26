from __future__ import unicode_literals
import pykka
import logging
import schedule
import time

class AlarmsScheduler(pykka.ThreadingActor,):


    def __init__(self, alarmsactor):
        super(AlarmsScheduler, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Background scheduler started")
        self.proxy= alarmsactor.proxy()
        self.wait()


    def wait (self):
        time.sleep(60)
        self.logger.debug("One Minute gone.. call run_pending in foreground:")
        # Run pending shedules
        self.proxy.run_pending()

