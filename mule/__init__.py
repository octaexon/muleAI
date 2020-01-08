import os

# store project root
ROOT = os.path.dirname(os.path.abspath(__file__))

# logging
LOG = os.path.join(ROOT, 'logging')
LOG_CFG = os.path.join(LOG, 'config')
LOG_DAT = os.path.join(LOG, 'data')

LOG_CFG_REF = 'default'

# drive
DRV = os.path.join(ROOT, 'drive')
DRV_CFG = os.path.join(DRV, 'config')
DRV_DAT = os.path.join(DRV, 'data')

DRV_CFG_REF = 'default'

# calibration
CAL = os.path.join(ROOT, 'calibrate')
CAL_DAT = os.path.join(CAL, 'data')

CAL_JOY = os.path.join(CAL, 'keymaps')
