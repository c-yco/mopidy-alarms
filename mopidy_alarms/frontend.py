from __future__ import unicode_literals
import pykka
import logging
import schedule
import time
import json
from os.path import isfile, exists, split
from os import mkdir

from mopidy import core


class AlarmsFrontend(pykka.ThreadingActor, core.CoreListener):

    scheduler = schedule
    def __init__(self, config, core):
        super(AlarmsFrontend, self).__init__()
        self.core = core
        self.config = config
        
        # Start logger
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Mopidy Alarms loaded")
        # Load alarms from disk
        self.scheduler.jobs = self.load_alarms(self.config['alarms']['jobsfile'])
        self.test_alarm()
        # Enter loop
        self.run_pending()


    def run_pending(self):
        while True:
            schedule.run_pending()
            self.logger.debug("Run pending schedules:")
            time.sleep(60)

    def load_alarms(self,jobs_file):
        if not isfile(jobs_file):
            self.logger.info(
            'No jobs file found, starting with no jobs!',jobs_file)
        return {}
        try:
            with gzip.open(jobs_file, 'rb') as fp:
                return json.load(fp)
        except (IOError, ValueError) as error:
            logger.warning(
            'Loading JSON jobs file failed: %s',
            encoding.locale_decode(error))
        return {}


    def save_alarms(self,data):


        # check if path exists, if not create folder first
        jobsfile_ = self.config['alarms']['jobsfile']
        path = split(jobsfile_)[0]
        if exists(path):
            self.logger.debug("Path found, writing jobs file to %s" % jobsfile_)
            filehandle = open(jobsfile_,'w+')
            json.dump(
                self.scheduler.jobs,
                filehandle
            )
        else:
            self.logger.warn("%s Directory not found, will try to create it " % path)
            try:
                mkdir (path)
            except  IOError:
                self.logger.error("Error creating %s" % path)
            self.save_alarms()

    def add_alarm(self):
        #ToDO neuen Job anlegen
        None

    def play_alarm(self):
        # ToDo implement alarm playback
        self.logger.info('Playing alarm:')
        core.PlaybackController.play()


    def test_alarm(self):
        self.scheduler.every(10).minutes.do(self.play_alarm)
        self.save_alarms(self.scheduler.jobs)