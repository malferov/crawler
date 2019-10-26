#!/bin/env python3.6
import sys
import time
import json
import codecs
import psutil
from crawler import Co
from pdb import set_trace as bp
from pprint import pprint

HOME = './'
URL  = "https://careers.fourthline.com"

class Runner(Co):
    def __init__(self, home, url):
        super().__init__(url)
        self.h = home
        self.data = dict()
        for var in ['status']:
            self.data.update({var: {'file': 'dat/{}.json'.format(var), 'value': ''}})
            self.data_load(var)
        if len(sys.argv) > 1 and sys.argv[1] == '-d':
            self.debug = True
        else:
            self.debug = False
        self.lock()
        self.log(time.strftime("%Y-%m-%d %H:%M:%S"), "init")

    def data_sync(self, varname):
        j = json.dumps(self.data[varname]["value"], sort_keys=True, indent=4)#separators=(',',':')
        open(self.h + self.data[varname]["file"], 'w').write(j)

    def data_load(self, varname):
        self.data[varname]["value"] = json.loads(open(self.h + self.data[varname]["file"]).read())

    def lock(self):
        if self.data["status"]["value"]["lock"] == 1:
            self.log(time.strftime("%Y-%m-%d %H:%M:%S"), "system is locked")
            sys.exit("system is locked")
        else:
            self.data["status"]["value"]["lock"] = 1
            self.data_sync("status")

    def ulock(self):
        self.data["status"]["value"]["lock"] = 0
        self.data_sync("status")

r = Runner(HOME, URL)
try:
    r.logIn()
    pprint(r.getJobs())
    r.data_sync("status")
finally:
    r.Quit()
    r.ulock()
