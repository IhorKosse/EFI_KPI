

DEBUG = True
if DEBUG:
    from settings_dev import *
else:
    from settings_prod import *