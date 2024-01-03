from tuya_iot import TuyaOpenAPI
from requests import get
import random
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import logging


ACCESS_ID = "suuarp4ndgpxunjs8u9v"
ACCESS_KEY = "dd981b503ff54aa882c13107403885c0"

USERNAME = "espana.dev.1@gmail.com"
PASSWORD = "Ariel0101"

ASSET_ID = "178810245"
DEVICE_ID = "bf8f2fa2152d25b65fs4f1"

ENDPOINT = "https://openapi.tuyaeu.com"


openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()