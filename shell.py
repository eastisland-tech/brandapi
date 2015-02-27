#!/usr/bin/env python

import os
import readline
from pprint import pprint
from datetime import datetime, timedelta
from flask import *

from brandapi import app


os.environ['PYTHONINSPECT'] = 'True'

ctx = app.test_request_context()
ctx.push()
app.preprocess_request()
