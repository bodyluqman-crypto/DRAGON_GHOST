import os
from datetime import datetime, timedelta

class Config:
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = False
    
    # مفاتيح التشفير
    AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    
    # إعدادات Free Fire
    FREEFIRE_VERSION = "OB51"
    REGION = "MENA"
    
    # الحساب الرئيسي
    MAIN_ACCOUNT_ID = "4315220774"
    MAIN_ACCOUNT_PASSWORD = "AF46CD1D09E6D361DB063261C79ED35AF2CF0196CC2A4E588BC25752931B552B"
    
    # مدة التشغيل
    API_DURATION = timedelta(days=30)
    START_TIME = datetime.now()