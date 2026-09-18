from flask import Flask, request, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import base64
import json
from datetime import datetime, timezone, timedelta
import time
import my_pb2
import output_pb2
from google.protobuf import json_format
import FreeFire_pb2

app = Flask(__name__)
SESSION = requests.Session()
KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

LOGIN_URL = "https://loginbp.ppmainecoonghj.com/"
CLIENT_URL = "https://clientbp.ppmainecoonghj.com/"
RELEASEVERSION = "OB55"
USERAGENT = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"

PLATFORM_MAP = {
    3: "Facebook",
    4: "Guest",
    5: "VK",
    8: "Google",
    10: "AppleId",
    11: "X (Twitter)"
}

def log_debug(message):
    print(f"[DEBUG] {message}")

def log_error(message):
    print(f"[ERROR] {message}")

def log_info(message):
    print(f"[INFO] {message}")

def convert_timestamp_to_human_readable(timestamp_seconds: int):
    try:
        utc_time = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
        ist_offset = timedelta(hours=5, minutes=30)
        ist_time = utc_time + ist_offset
        
        current_time = int(time.time())
        time_remaining = timestamp_seconds - current_time
        
        days = time_remaining // (24 * 3600)
        hours = (time_remaining % (24 * 3600)) // 3600
        minutes = (time_remaining % 3600) // 60
        seconds = time_remaining % 60
        is_expired = time_remaining <= 0
        
        return {
            "timestamp": timestamp_seconds,
            "utc_time": utc_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "ist_time": ist_time.strftime("%Y-%m-%d %H:%M:%S IST"),
            "time_remaining_seconds": time_remaining,
            "time_remaining_human": f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds" if time_remaining > 0 else "Expired",
            "is_expired": is_expired,
            "days_remaining": days if not is_expired else 0,
            "hours_remaining": hours if not is_expired else 0,
            "minutes_remaining": minutes if not is_expired else 0,
            "seconds_remaining": seconds if not is_expired else 0
        }
    except Exception as e:
        log_error(f"Error converting timestamp: {e}")
        return {
            "timestamp": timestamp_seconds,
            "utc_time": "Invalid timestamp",
            "ist_time": "Invalid timestamp",
            "time_remaining_seconds": 0,
            "time_remaining_human": "Invalid timestamp",
            "is_expired": True,
            "error": str(e)
        }

def get_token_inspect_data(access_token: str):
    try:
        resp = SESSION.get(
            f"https://ffmconnect.live.gop.garenanow.com/oauth/token/inspect?token={access_token}",
            timeout=15,
            verify=False
        )
        data = resp.json()
        
        if 'open_id' in data and 'platform' in data and 'uid' in data:
            if 'expiry_time' in data:
                data['expiry_info'] = convert_timestamp_to_human_readable(data['expiry_time'])
            elif 'expires_in' in data:
                expires_at = int(time.time()) + data['expires_in']
                data['expiry_info'] = convert_timestamp_to_human_readable(expires_at)
            return data
    except Exception as e:
        log_error(f"Error inspecting token: {e}")
    return None

def decode_jwt_token(jwt_token: str):
    try:
        parts = jwt_token.split('.')
        if len(parts) != 3:
            return None
        
        payload = parts[1]
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += '=' * padding
        
        decoded_bytes = base64.urlsafe_b64decode(payload)
        payload_data = json.loads(decoded_bytes.decode('utf-8'))
        
        if 'exp' in payload_data:
            payload_data['expiry_info'] = convert_timestamp_to_human_readable(payload_data['exp'])
        if 'iat' in payload_data:
            payload_data['issued_at_info'] = convert_timestamp_to_human_readable(payload_data['iat'])
        
        return payload_data
    except Exception as e:
        log_error(f"Error decoding JWT token: {e}")
        return None

def find_protobuf_start(data: bytes) -> int:
    """Find where valid protobuf starts in the response"""
    idx = data.find(b'\x12\x03IND')
    if idx != -1:
        for i in range(idx - 1, max(idx - 20, -1), -1):
            if data[i] == 0x08:
                return i

    jwt_marker = data.find(b'B\xe7\x05eyJ')
    if jwt_marker != -1:
        for i in range(jwt_marker - 1, max(jwt_marker - 200, -1), -1):
            if data[i] == 0x08:
                return i

    return data.find(b'\x08')

def login(uid, access_token, open_id, platform_type):
    """Login and get JWT token using updated URL and headers"""
    log_debug(f"Starting login for UID {uid} with platform_type {platform_type}")
    
    url = f"{LOGIN_URL}MajorLogin"
    
    game_data = my_pb2.GameData()
    game_data.timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    game_data.game_name = "Free Fire"
    game_data.game_version = 1
    game_data.version_code = "1.126.2"
    game_data.os_info = "iOS 18.4"
    game_data.device_type = "Handheld"
    game_data.network_provider = "Verizon Wireless"
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1170
    game_data.screen_height = 2532
    game_data.dpi = "460"
    game_data.cpu_info = "Apple A15 Bionic"
    game_data.total_ram = 6144
    game_data.gpu_name = "Apple GPU (5-core)"
    game_data.gpu_version = "Metal 3"
    game_data.user_id = str(uid)
    game_data.ip_address = "172.190.111.97"
    game_data.language = "en"
    game_data.open_id = str(open_id)
    game_data.access_token = str(access_token)
    game_data.platform_type = int(platform_type)
    game_data.field_99 = str(platform_type)
    game_data.field_100 = str(platform_type)
    
    serialized_data = game_data.SerializeToString()
    padded_data = pad(serialized_data, AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(padded_data)
    
    headers = {
        'User-Agent': USERAGENT,
        'Accept': "*/*",
        'Accept-Encoding': "deflate, gzip",
        'X-Ga-Sv': "1789534056",
        'Authorization': "Bearer",
        'X-Ga': "v1 1",
        'Releaseversion': RELEASEVERSION,
        'Content-Type': "application/x-www-form-urlencoded",
        'X-Unity-Version': "2018.4.12f1",
        'PlAy_VeR': "1.132.1",
        'Ob_VeR': RELEASEVERSION
    }
    
    try:
        response = SESSION.post(url, data=encrypted_data, headers=headers, timeout=30, verify=False)
        
        if response.status_code == 200:
            start_idx = find_protobuf_start(response.content)
            
            if start_idx == -1:
                log_error(f"Protobuf start not found. Raw: {response.content[:300]}")
                return None
            
            proto_data = response.content[start_idx:]
            log_debug(f"Protobuf starts at index {start_idx}")
            
            jwt_msg = output_pb2.Garena_420()
            try:
                jwt_msg.ParseFromString(proto_data)
                if jwt_msg.token:
                    log_debug(f"Login successful for UID {uid}")
                    return jwt_msg.token
            except Exception as parse_err:
                log_error(f"Failed to parse protobuf: {parse_err}")
                return None
        else:
            error_text = response.content.decode().strip()
            log_debug(f"API MajorLogin returned status {response.status_code}: {error_text}")
            
            if error_text == "BR_PLATFORM_INVALID_PLATFORM":
                return {"error": "INVALID_PLATFORM", "message": "this account is registered on another platform"}
            elif error_text == "BR_GOP_TOKEN_AUTH_FAILED":
                return {"error": "INVALID_TOKEN", "message": "AccessToken invalid."}
            elif error_text == "BR_PLATFORM_INVALID_OPENID":
                return {"error": "INVALID_OPENID", "message": "OpenID invalid."}
                
    except Exception as e:
        log_error(f"UID {uid}: Error in JWT request - {e}")
    
    return None

# ============ /token endpoint functions ============

def get_access_token(account: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = account + "&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
    headers = {
        'User-Agent': USERAGENT,
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    with requests.Session() as client:
        resp = client.post(url, data=payload, headers=headers, verify=False)
        data = resp.json()
        return data.get("access_token", "0"), data.get("open_id", "0")

def generate_jwt_token_with_uid_password(uid: str, password: str):
    account = f"uid={uid}&password={password}"

    token_val, open_id = get_access_token(account)

    if token_val == "0" or open_id == "0":
        raise Exception("Invalid UID or Password — access token not received")

    body = json.dumps({
        "open_id": open_id,
        "open_id_type": "4",
        "login_token": token_val,
        "orign_platform_type": "4"
    })

    proto_bytes = json_to_proto(body, FreeFire_pb2.LoginReq())
    encrypted_payload = aes_cbc_encrypt(KEY, IV, proto_bytes)

    url = f"{LOGIN_URL}MajorLogin"
    headers = {
        'User-Agent': USERAGENT,
        'Accept': "*/*",
        'Accept-Encoding': "deflate, gzip",
        'X-Ga-Sv': "1789534056",
        'Authorization': "Bearer",
        'X-Ga': "v1 1",
        'Releaseversion': RELEASEVERSION,
        'Content-Type': "application/x-www-form-urlencoded",
        'X-Unity-Version': "2018.4.12f1",
        'PlAy_VeR': "1.132.1",
        'Ob_VeR': RELEASEVERSION
    }

    with requests.Session() as client:
        resp = client.post(url, data=encrypted_payload, headers=headers, verify=False)

        print(f"=== HTTP {resp.status_code} | Content-Length: {len(resp.content)} ===")

        start_idx = find_protobuf_start(resp.content)

        if start_idx == -1:
            raise Exception(f"Protobuf start not found. Raw: {resp.content[:300]}")

        proto_data = resp.content[start_idx:]
        print(f"=== Protobuf starts at index {start_idx} ===")

        try:
            msg = json.loads(json_format.MessageToJson(
                decode_protobuf(proto_data, FreeFire_pb2.LoginRes)
            ))
        except Exception as parse_err:
            raise Exception(
                f"Failed to parse LoginRes from index {start_idx}. "
                f"Raw (from start): {resp.content[start_idx:start_idx+300]}. "
                f"Error: {parse_err}"
            )

        response_data = {
            "account_Id": msg.get("accountId", ""),
            "agoraEnvironment": msg.get("agoraEnvironment", "live"),
            "ipRegion": msg.get("ipRegion", ""),
            "lockRegion": msg.get("lockRegion", ""),
            "region": msg.get("notiRegion", ""),
            "serverUrl": msg.get("serverUrl", ""),
            "token": f"{msg.get('token', '')}"
        }

        return response_data

def decode_protobuf(encoded_data: bytes, message_type):
    instance = message_type()
    instance.ParseFromString(encoded_data)
    return instance

def json_to_proto(json_data: str, proto_message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()

def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    padded = pad(plaintext, AES.block_size)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(padded)

# ============ Routes ============

@app.route('/access-to-jwt', methods=['GET'])
def access_to_jwt():
    """Convert access_token to JWT token"""
    access_token = request.args.get('access_token')
    
    if not access_token:
        return jsonify({
            "success": False,
            "error": "MISSING_PARAMETER",
            "message": "access_token parameter is required"
        }), 400
    
    token_data = get_token_inspect_data(access_token)
    
    if not token_data:
        return jsonify({
            "success": False,
            "error": "INVALID_TOKEN",
            "message": "AccessToken is invalid or expired"
        }), 400
    
    open_id = token_data.get('open_id')
    platform_type = token_data.get('platform', 4)
    uid = token_data.get('uid')
    
    uid_str = str(uid) if uid else ""
    platform_type_int = int(platform_type) if platform_type else 4
    open_id_str = str(open_id) if open_id else ""
    
    if not open_id_str:
        return jsonify({
            "success": False,
            "error": "MISSING_DATA",
            "message": "Could not extract open_id from access_token"
        }), 400
    
    jwt_token = login(uid_str, access_token, open_id_str, platform_type_int)
    
    if isinstance(jwt_token, dict) and 'error' in jwt_token:
        return jsonify({
            "success": False,
            "error": jwt_token.get("error"),
            "message": jwt_token.get("message")
        }), 400
    
    if not jwt_token:
        return jsonify({
            "success": False,
            "error": "JWT_GENERATION_FAILED",
            "message": "Failed to generate JWT token. Account may be unregistered or banned."
        }), 500
    
    decoded_token = decode_jwt_token(jwt_token)
    platform_name = PLATFORM_MAP.get(platform_type_int, "Unknown")
    
    current_time = datetime.now(timezone.utc)
    current_ist = current_time + timedelta(hours=5, minutes=30)
    
    response_data = {
        "success": True,
        "access_token": access_token,
        "jwt_token": jwt_token,
        "decoded_jwt": decoded_token if decoded_token else {},
        "user_info": {
            "uid": uid_str,
            "open_id": open_id_str,
            "platform_type": platform_type_int,
            "platform_name": platform_name,
        },
        "current_time": {
            "utc": current_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "ist": current_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
            "timestamp": int(time.time())
        },
        "credits": {
            "developer": "@UditGaming45",
            "main_channel": "@UDITGAM1NG45",
            "apis_channel": "@UDITGAM1NG455"
        }
    }
    
    if 'expiry_info' in token_data:
        response_data['access_token_expiry'] = token_data['expiry_info']
    
    return jsonify(response_data)

@app.route('/token', methods=['GET'])
def get_jwt_token():
    """Generate JWT token from UID and password"""
    uid = request.args.get('uid')
    password = request.args.get('password')

    if not uid or not password:
        return jsonify({
            "success": False,
            "error": "MISSING_PARAMETER",
            "message": "Both uid and password parameters are required"
        }), 400

    try:
        token_data = generate_jwt_token_with_uid_password(uid, password)
        
        token_data['success'] = True
        token_data['credits'] = {
            "developer": "@UditGaming45",
            "main_channel": "@UDITGAM1NG45",
            "apis_channel": "@UDITGAM1NG455"
        }
        
        return jsonify(token_data), 200
    except Exception as e:
        log_error(f"Failed to generate token: {str(e)}")
        return jsonify({
            "success": False,
            "error": "TOKEN_GENERATION_FAILED",
            "message": f"Failed to generate token: {str(e)}"
        }), 500

@app.route('/')
def index():
    return jsonify({
        "success": True,
        "message": "Free Fire Token Converter API",
        "endpoints": {
            "/access-to-jwt": "Convert access_token to JWT token",
            "/token": "Generate JWT token using UID and password"
        },
        "credits": {
            "developer": "@UditGaming45",
            "main_channel": "@UDITGAM1NG45",
            "apis_channel": "@UDITGAM1NG455"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    log_info(f'Starting API server on port {port}')
    app.run(host='0.0.0.0', port=port, debug=True)