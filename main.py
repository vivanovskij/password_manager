#---------------------------------------------------
# Author: Vitalij Ivanovskij
# Date start: 2020-07-24
#
# Description: application for manage passwords
#---------------------------------------------------

import logging
import logging.config
from app_lib import log_config
from db.abstract_db import *

if __name__ == '__main__':
    logger = logging.config.dictConfig(log_config.LOGGING)
    logger = logging.getLogger(__name__)
    db = test_db('test.sqlite')
    query = "INSERT into switch values (?, ?, ?, ?)"
    params = ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
