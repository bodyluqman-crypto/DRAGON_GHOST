import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config import Config

def EnC_Vr(N):
    """ترميز Varint - من الملف الأصلي"""
    if N < 0: 
        return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N: 
            BesTo |= 0x80
        H.append(BesTo)
        if not N: 
            break
    return bytes(H)

def CrEaTe_VarianT(field_number, value):
    """إنشاء حقل varint - من الملف الأصلي"""
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    """إنشاء حقل length delimited - من الملف الأصلي"""
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    """إنشاء حزمة بروتوبوف - من الملف الأصلي"""
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet

def EnC_PacKeT(HeX, K, V):
    """تشفير الحزمة - من الملف الأصلي"""
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()

def ghost_pakcet(player_id, nm, secret_code, key, iv):
    """إنشاء حزمة الشبح الحقيقية - من الملف الأصلي"""
    fields = {
        1: 61,
        2: {
            1: int(player_id),  
            2: {
                1: int(player_id),  
                2: 1159,  
                3: f"[c]{nm}",  
                5: 12,  
                6: 15,
                7: 1,
                8: {2: 1, 3: 1},
                9: 3,
            },
            3: secret_code,
        }
    }
    packet_hex = CrEaTe_ProTo(fields).hex()
    return EnC_PacKeT(packet_hex, key, iv)

def GenJoinSquadsPacket(code, key, iv):
    """حزمة الانضمام للفريق - من الملف الأصلي"""
    fields = {}
    fields[1] = 4
    fields[2] = {}
    fields[2][4] = bytes.fromhex("01090a0b121920")
    fields[2][5] = str(code)
    fields[2][6] = 6
    fields[2][8] = 1
    fields[2][9] = {}
    fields[2][9][2] = 800
    fields[2][9][6] = 11
    fields[2][9][8] = "1.111.1"
    fields[2][9][9] = 5
    fields[2][9][10] = 1
    
    packet_hex = CrEaTe_ProTo(fields).hex()
    return EnC_PacKeT(packet_hex, key, iv)

def ExitBot(id, key, iv):
    """حزمة الخروج - من الملف الأصلي"""
    fields = {1: 7, 2: {1: int(11037044965)}}
    packet_hex = CrEaTe_ProTo(fields).hex()
    return EnC_PacKeT(packet_hex, key, iv)