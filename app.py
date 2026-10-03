import json
import requests
import time
import sys
import os
from flask import Flask, request, jsonify, Response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from urllib.parse import urlparse, parse_qs

# -------------------- Include protobuf generated code --------------------
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf.message import Message

_sym_db = _symbol_database.Default()

app = Flask(__name__)
app.json.sort_keys = False

# --- MajorLoginReq protobuf ---
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MajorLoginReq_pb2', _globals)

class ThunderFFMock:
    pass

thunderFF_pb2 = ThunderFFMock()
thunderFF_pb2.MajorLoginReq = _globals['MajorLogin']
thunderFF_pb2.GameSecurity = _globals['GameSecurity']

# --- MajorLoginRes protobuf ---
DESCRIPTOR2 = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"|\n\rMajorLoginRes\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0b\n\x03key\x18\x16 \x01(\x0c\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3')
_globals2 = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR2, _globals2)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR2, 'MajorLoginRes_pb2', _globals2)
thunderFF_pb2.MajorLoginRes = _globals2['MajorLoginRes']

# AES constants
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

async def aes_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data, AES.block_size))

import traceback
import ssl
import asyncio
from datetime import datetime
import aiohttp

async def build_majorlogin_payload(open_id, access_token, platform, client_version, device_info):
    try:
        proto = thunderFF_pb2.MajorLoginReq()
        proto.event_time = str(datetime.now())[:-7]
        proto.game_name = "free fire"
        proto.platform_id = int(platform)
        
        proto.client_version = "1.132.1"
        proto.client_version_code = "2019116753"
        proto.platform_sdk_id = 1
        proto.login_by = 3
        proto.login_open_id_type = int(platform)
        proto.open_id_type = str(platform)
        proto.origin_platform_type = str(platform)
        proto.primary_platform_type = str(platform)
        
        proto.system_software = str(device_info.get("system_software", "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"))
        proto.system_hardware = str(device_info.get("brand", "Handheld"))
        proto.device_type = str(device_info.get("model", "Handheld"))
        proto.screen_width = int(device_info.get("screen_width", 1920))
        proto.screen_height = int(device_info.get("screen_height", 1080))
        proto.screen_dpi = str(device_info.get("screen_dpi", "280"))
        proto.processor_details = str(device_info.get("processor_details", "ARM64 FP ASIMD AES VMH | 2865 | 4"))
        proto.memory = int(device_info.get("memory", 3003))
        proto.gpu_renderer = str(device_info.get("gpu_renderer", "Adreno (TM) 640"))
        proto.gpu_version = "OpenGL ES 3.1 v1.46"
        proto.unique_device_id = str(device_info.get("unique_device_id", "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"))
        proto.client_ip = str(device_info.get("client_ip", "223.191.51.89"))
        
        proto.telecom_operator = "Verizon"
        proto.network_operator_a = "Verizon"
        proto.network_type = "WIFI"
        proto.network_type_a = "WIFI"
        proto.cpu_type = 2
        proto.cpu_architecture = "64"
        proto.graphics_api = "OpenGLES2"
        proto.language = "en"
        proto.open_id = str(open_id)
        proto.access_token = str(access_token)
        proto.reg_avatar = 1
        proto.channel_type = 3
        
        if hasattr(proto, "memory_available"):
            proto.memory_available.version = 55
            proto.memory_available.hidden_value = 81
        
        proto.external_storage_total = 36235
        proto.external_storage_available = 31335
        proto.internal_storage_total = 2519
        proto.internal_storage_available = 703
        proto.game_disk_storage_total = 26628
        proto.game_disk_storage_available = 25010
        proto.external_sdcard_total_storage = 36235
        proto.external_sdcard_avail_storage = 32992
        
        proto.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
        proto.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
        proto.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        proto.supported_astc_bitset = 16383
        proto.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        proto.loading_time = 13564
        proto.release_channel = "android"
        proto.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        proto.android_engine_init_flag = 110009
        proto.if_push = 1
        proto.is_vpn = 1
        
        payload = proto.SerializeToString()
        return await aes_encrypt(payload, AES_KEY, AES_IV)
    except Exception as e:
        print(f"[-] Error building MajorLogin payload: {e}")
        traceback.print_exc()
        return None

async def send_majorlogin(data, release_version, access_token, server_url):
    try:
        url = f"{server_url}MajorLogin"
        req_headers = {
            'User-Agent': "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            'Accept': "*/*",
            'Accept-Encoding': "deflate, gzip",
            'X-Ga-Sv': "1789534056",
            'Authorization': f"Bearer {access_token}",
            'X-Ga': "v1 1",
            'Releaseversion': str(release_version),
            'Content-Type': "application/octet-stream",
            'X-Unity-Version': "2018.4.12f1",
            'PlAy_VeR': "1.132.1",
            'Ob_VeR': str(release_version),
            'LoGiN_UrL': url
        }
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=req_headers, data=data, ssl=ssl_context) as response:
                if response.status != 200:
                    return None
                    
                response_content = await response.read()
                if not response_content or len(response_content) < 20:
                    return None

                try:
                    res_proto = thunderFF_pb2.MajorLoginRes()
                    res_proto.ParseFromString(response_content)
                    if getattr(res_proto, "region", None) and getattr(res_proto, "token", None):
                        return res_proto
                except Exception:
                    pass

                if len(response_content) > 64:
                    try:
                        res_proto = thunderFF_pb2.MajorLoginRes()
                        res_proto.ParseFromString(response_content[64:])
                        if getattr(res_proto, "region", None) and getattr(res_proto, "token", None):
                            return res_proto
                    except Exception:
                        pass

                for offset in range(min(128, len(response_content))):
                    try:
                        candidate = thunderFF_pb2.MajorLoginRes()
                        candidate.ParseFromString(response_content[offset:])
                        if getattr(candidate, "region", None) and getattr(candidate, "token", None):
                            return candidate
                    except Exception:
                        continue

                fallback_proto = thunderFF_pb2.MajorLoginRes()
                fallback_proto.ParseFromString(response_content)
                return fallback_proto
                
    except Exception as e:
        return None

def format_login_result(res_proto):
    if not res_proto:
        return None
    try:
        token = getattr(res_proto, "token", "")
        if not token:
            return None
        return {
            "account_uid": str(getattr(res_proto, "account_uid", "")),
            "region": getattr(res_proto, "region", ""),
            "token": token,
            "url": getattr(res_proto, "url", ""),
            "timestamp": getattr(res_proto, "timestamp", 0),
            "key": getattr(res_proto, "key", b"").hex(),
            "iv": getattr(res_proto, "iv", b"").hex()
        }
    except Exception:
        return None

def try_major_login(open_id: str, access_token: str, platform_type: int):
    async def _wrapper():
        device_info = {}
        payload = await build_majorlogin_payload(open_id, access_token, platform_type, "1.132.1", device_info)
        if not payload:
            return None
        res_proto = await send_majorlogin(payload, "OB55", access_token, "https://loginbp.ppmainecoonghj.com/")
        return format_login_result(res_proto)
    
    try:
        return asyncio.run(_wrapper())
    except Exception as e:
        return None

def get_garena_data(eat_token):
    try:
        callback_url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
        response = requests.get(callback_url, allow_redirects=False, timeout=10)

        if 300 <= response.status_code < 400 and "Location" in response.headers:
            redirect_url = response.headers["Location"]
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)

            return {
                "status": "success",
                "access_token": query_params.get("access_token", [None])[0],
                "account_id": query_params.get("account_id", [None])[0],
                "nickname": query_params.get("nickname", [None])[0],
                "region": query_params.get("region", [None])[0]
            }
        return {"error": "Invalid access token or session expired"}
    except Exception as e:
        return {"error": "Server error", "details": str(e)}

def get_token(uid, password):
    try:
        url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
        payload = (
            f"uid={uid}&password={password}"
            "&response_type=token&client_type=2"
            "&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
            "&client_id=100067"
        )
        headers = {
            "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        res = requests.post(url, data=payload, headers=headers, timeout=10)
        return res.json() if res.status_code == 200 else {"error": "Login failed", "status": res.status_code}
    except Exception as e:
        return {"error": str(e)}
        
@app.route("/access-to-jwt", methods=["GET"])
def rizer_endpoint():
  access_token = request.args.get("access_token")
  if not access_token:
    return jsonify({"error": "Missing 'access_token' parameter"}), 400

  inspect_url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
  try:
    insp_resp = requests.get(inspect_url, timeout=10)
    open_id = insp_resp.json().get("open_id") if insp_resp.status_code == 200 else None
    if not open_id:
      return jsonify({"error": "open_id not found"}), 400
  except Exception as e:
    return jsonify({"error": str(e)}), 500

  for pt in [3, 8, 11, 5, 10, 2, 4, 6, 12]:
    result = try_major_login(open_id, access_token, pt)
    if result:
      custom_response = {
          "Success": True,
          "account_uid": result["account_uid"],
          "region": result["region"],
          "jwt_Token": result["token"],
          "login_url": result["url"],
          "timestamp": result["timestamp"],
          "Platform_type_used": pt,
          "Ob_version": "OB55",
          "Client_Version": "1.132.1",
          "Develover": "@XEROX_MODS",
          "Telegram": "@SEXTYMODS",
          "Status_Code": 200,
      }
      return Response(
          json.dumps(custom_response, ensure_ascii=False, separators=(",", ":")),
          status=200,
          content_type="application/json; charset=utf-8",
      )

  return jsonify({"success": False, "error": "All platform login failed"}), 401




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
