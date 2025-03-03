import requests
from time import sleep

requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "BLEED_APU_FAULT"}) #A
sleep(1)
requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "PRESS_CABIN_ALT_TOO_HI"}) #R
sleep(1)
requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "HUMID_FAULT"}) #W

# sleep(5)

# requests.get("http://127.0.0.1:8881/api/remove_message", json = {"message": "BLEED_APU_FAULT"})

# sleep(1)

# requests.get("http://127.0.0.1:8881/api/remove_all_messages")
# sleep(1)

# requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "BLEED_APU_FAULT"}) #A
# sleep(1)
# requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "PRESS_CABIN_ALT_TOO_HI"}) #R
# sleep(1)
# requests.get("http://127.0.0.1:8881/api/show_message", json = {"message": "HUMID_FAULT"}) #W

# sleep(1)

requests.get("http://127.0.0.1:8881/api/read_message")
sleep(1)

# add_mssg("IRS 1+2+3 NO POS ENTRY") #W  cruise = True
# add_mssg("AVC: AGM #+#+# FAIL") #A  cruise = True
# add_mssg("90 PRESS: CABIN ALT TOO HI") #R cruise = True
# add_mssg("AVC: ASCB FAULT") #A cruise = False
# add_mssg("AVC: APM 1+2+3+4 FAIL") #A cruise = False
# add_mssg("15 COND: AFT FCS BOX OVHT") #R cruise = True
# add_mssg("AVC AURAL WARN 1+2 INHIBIT") #W cruise = True
# add_mssg("30 ELEC: BAT 1 OVHT") #R cruise = True
# add_mssg("AVC: VALIDATE CONFIG") #W cruise = True
# add_mssg("AVC: GEN IO 1+2+3+4+5 FAIL") #A cruise = True
# add_mssg("AVC: MAU 1A+1B HI TEMP") #A cruise = True
# add_mssg("HUMID: FAULT") #"W"
# add_mssg("31 ELEC: BAT 2 OVHT") #R
# add_mssg("32 ELEC: BAT 1+2 OVHT") #R
# add_mssg("BLEED: APU FAULT") #A
# add_mssg("WATER: AFT HEATER HI TEMP") #A
# add_mssg("APU: AUTO SHUTDOWN")#A
# add_mssg("DOOR: EMERG NOT SECURED") #A