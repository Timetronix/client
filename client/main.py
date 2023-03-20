import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import requests

i2c = busio.I2C(board.SCL, board.SDA)

reset_pin = DigitalInOut(board.D6)

req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version

pn532.SAM_configuration()

def wait_for_card_scan():
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is None:
            continue
        current_work_state = _get_current_work_state(uid)
        
        # Is currently not working
        if current_work_state == 0:
            pass
        
        # Is currently working
        elif current_work_state == 1:
            pass
    
def _get_current_work_state(uid):
    return requests.post(f'https://127.0.0.1:7091/employee/work-state/{uid}')

if __name__ == "__main__":
    wait_for_card_scan()