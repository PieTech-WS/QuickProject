import os

import datetime
import sys


class LogFile:
    def __init__(self, module: str, main_path: str):
        self.logFileObj = None
        self.module = module
        self.main_path = main_path
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.logFileName = "{}-{}.log".format(self.module, self.date)
        if self.logFileName not in os.listdir(main_path):
            sys.stdout = self.generate_new_logfile()
        else:
            sys.stdout = self.get_existed_log()

    def process(self, content: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(":: [{}][PROC]{}".format(time, content))

    def child_process(self, content: str):
        print("=> {}".format(content))

    def tip(self, content: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(":: [{}][TIP]{}".format(time, content))

    def warn(self, content: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(":: [{}][WARN] {}".format(time, content))

    def error(self, content: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(":: [{}][ERROR] {}".format(time, content))

    def generate_new_logfile(self):
        log_file_obj = open(
            "{}/{}"
            .format(
                self.main_path, self.logFileName
            ),
            "a+",
            encoding="utf-8"
        )
        log_file_obj.write("------log file beginning------\n")
        return log_file_obj

    def get_existed_log(self):
        log_file_obj = open(
            "{}/{}"
            .format(
                self.main_path, self.logFileName
            ),
            "a+",
            encoding="utf-8"
        )
        return log_file_obj

