from facebookChatbot.database.sampledata                               import Sampledata
from facebookChatbot.database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re
import logging, sys

class MultipleChoiceResponseBuilder:

    def __init__(self):
        print 'init MultipleChoiceResponseBuilder'
