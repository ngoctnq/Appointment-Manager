#!/usr/bin/env python

import Database as DB
from gui_search import *
from gui_list import *

#connecting with the database
db = DB.Database('cup.db')
new = gui_search(db)
