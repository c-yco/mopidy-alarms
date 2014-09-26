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
        proxy= alarmsactor.proxy()
        while True:
            self.logger.debug("One Minute gone.. call run_pending in foreground:")
            proxy.run_pending()

