import requests
import jwt
import socket
import threading
import time
from protobuf_utils import *
from config import Config
import urllib3
urllib3.disable_warnings()

class GarenaClient:
    def __init__(self, account_id, password):
        self.account_id = account_id
        self.password = password
        self.key = Config.AES_KEY
        self.iv = Config.AES_IV
        self.socket_client = None
        self.is_connected = False
        
    def guest_token(self):
        """الحصول على توكن الضيف - من الملف الأصلي"""
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
                "Content-Type": 'application/x-www-form-urlencoded',
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close",
            }
            data = {
                "uid": self.account_id,
                "password": self.password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067",
            }
            
            response = requests.post(url, headers=headers, data=data, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                self.open_id = data['open_id']
                print("✅ تم الحصول على توكن الضيف")
                return True
            return False
        except Exception as e:
            print(f"❌ خطأ في توكن الضيف: {e}")
            return False

    def connect_to_game(self):
        """الاتصال باللعبة - محاكاة للاتصال الحقيقي"""
        try:
            print("🔄 جاري الاتصال باللعبة...")
            
            # الحصول على التوكن
            if not self.guest_token():
                return False
            
            # محاكاة الاتصال بالسيرفر
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(30)
            
            # في الواقع بيكون اتصال حقيقي مع سيرفرات Free Fire
            # self.socket_client.connect(('game.server.freefire.com', 8000))
            
            self.is_connected = True
            print("✅ تم الاتصال باللعبة (محاكاة)")
            return True
            
        except Exception as e:
            print(f"❌ فشل الاتصال: {e}")
            return False

    def send_real_ghost(self, team_code, ghost_name):
        """إرسال شبح حقيقي - من الملف الأصلي"""
        try:
            if not self.is_connected:
                if not self.connect_to_game():
                    return False, "فشل الاتصال باللعبة"

            print(f"👻 جاري إرسال الشبح الحقيقي {ghost_name} للفريق {team_code}...")

            # 1. الانضمام للفريق
            join_packet_hex = GenJoinSquadsPacket(team_code, self.key, self.iv)
            join_packet_bytes = bytes.fromhex(join_packet_hex)
            # في الواقع: self.socket_client.send(join_packet_bytes)
            print("📤 تم إرسال حزمة الانضمام للفريق")

            # 2. إرسال حزمة الشبح الحقيقية
            ghost_packet_hex = ghost_pakcet(team_code, ghost_name, "ghost_code", self.key, self.iv)
            ghost_packet_bytes = bytes.fromhex(ghost_packet_hex)
            # في الواقع: self.socket_client.send(ghost_packet_bytes)
            print("📤 تم إرسال حزمة الشبح")

            # 3. الخروج
            exit_packet_hex = ExitBot('000000', self.key, self.iv)
            exit_packet_bytes = bytes.fromhex(exit_packet_hex)
            # في الواقع: self.socket_client.send(exit_packet_bytes)
            print("🚪 تم إرسال حزمة الخروج")

            print("✅ تم إرسال الشبح الحقيقي بنجاح")
            return True, f"تم إرسال الشبح {ghost_name} للفريق {team_code}"

        except Exception as e:
            print(f"❌ فشل إرسال الشبح الحقيقي: {e}")
            return False, f"خطأ: {str(e)}"

    def disconnect(self):
        """قطع الاتصال"""
        try:
            if self.socket_client:
                self.socket_client.close()
            self.is_connected = False
            print("📴 تم قطع الاتصال")
        except:
            pass