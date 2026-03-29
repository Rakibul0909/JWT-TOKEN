import sys
sys.path.append("/")

from flask import Flask, jsonify, request, make_response
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from protobuf import my_pb2, output_pb2

import os
import warnings
from urllib3.exceptions import InsecureRequestWarning

# NEW IMPORTS
import base64
import json
import time
from datetime import datetime, timezone, timedelta

# Ignore SSL certificate warnings
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# AES encryption key and initialization vector
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

app = Flask(__name__)

# IST timezone (UTC+5:30) - kept for possible future use, but not used in minimal time_info
IST = timezone(timedelta(hours=5, minutes=30))

def get_token(password, uid):
    """
    Obtain an OAuth token by posting the provided uid and password to the token endpoint.
    """
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return None
    return response.json()

def encrypt_message(key, iv, plaintext):
    """
    Encrypt a plaintext message using AES in CBC mode with PKCS#7 padding.
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded_message)

def parse_response(response_content):
    """
    Parse a string response that uses key: value pairs separated by newlines.
    """
    response_dict = {}
    lines = response_content.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict

def decode_full_jwt(token):
    """Decode JWT header and payload without verification."""
    try:
        header_b64, payload_b64, _ = token.split('.')
        header_b64 += '=' * (-len(header_b64) % 4)
        payload_b64 += '=' * (-len(payload_b64) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_b64))
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return header, payload
    except:
        return {}, {}

def format_utc(ts):
    """Convert timestamp to UTC string."""
    try:
        if not ts:
            return None
        return datetime.fromtimestamp(int(ts), timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return None

def process_token(uid, password):
    """
    Get token data and use it to build, serialize, encrypt, and send game data via protocol buffers.
    """
    token_data = get_token(password, uid)
    if not token_data:
        return {"error": "Failed to retrieve token"}

    # Create and populate the protocol buffer for game data.
    game_data = my_pb2.GameData()
    game_data.timestamp = "2024-12-05 18:15:32"
    game_data.game_name = "free fire"
    game_data.game_version = 1
    game_data.version_code = "1.108.3"
    game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
    game_data.device_type = "Handheld"
    game_data.network_provider = "Verizon Wireless"
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1280
    game_data.screen_height = 960
    game_data.dpi = "240"
    game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
    game_data.total_ram = 5951
    game_data.gpu_name = "Adreno (TM) 640"
    game_data.gpu_version = "OpenGL ES 3.0"
    game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
    game_data.ip_address = "172.190.111.97"
    game_data.language = "en"
    game_data.open_id = token_data.get('open_id', '')
    game_data.access_token = token_data.get('access_token', '')
    game_data.platform_type = 4
    game_data.device_form_factor = "Handheld"
    game_data.device_model = "Asus ASUS_I005DA"
    game_data.field_60 = 32968
    game_data.field_61 = 29815
    game_data.field_62 = 2479
    game_data.field_63 = 914
    game_data.field_64 = 31213
    game_data.field_65 = 32968
    game_data.field_66 = 31213
    game_data.field_67 = 32968
    game_data.field_70 = 4
    game_data.field_73 = 2
    game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
    game_data.field_76 = 1
    game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
    game_data.field_78 = 6
    game_data.field_79 = 1
    game_data.os_architecture = "32"
    game_data.build_number = "2019117877"
    game_data.field_85 = 1
    game_data.graphics_backend = "OpenGLES2"
    game_data.max_texture_units = 16383
    game_data.rendering_api = 4
    game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
    game_data.field_92 = 9204
    game_data.marketplace = "3rd_party"
    game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
    game_data.total_storage = 111107
    game_data.field_97 = 1
    game_data.field_98 = 1
    game_data.field_99 = "4"
    game_data.field_100 = "4"

    # Serialize the protocol buffer
    serialized_data = game_data.SerializeToString()

    # Encrypt the serialized protocol buffer data using AES
    encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)
    hex_encrypted_data = binascii.hexlify(encrypted_data).decode('utf-8')

    # Prepare the request to the login endpoint
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/octet-stream",
        'Expect': "100-continue",
        'X-GA': "v1 1",
        'X-Unity-Version': "2018.4.11f1",
        'ReleaseVersion': "OB52"
    }
    edata = bytes.fromhex(hex_encrypted_data)

    try:
        response = requests.post(url, data=edata, headers=headers, verify=False)
        if response.status_code == 200:
            example_msg = output_pb2.Garena_420()
            try:
                example_msg.ParseFromString(response.content)
                parsed_resp = parse_response(str(example_msg))
                return {
                    "token": parsed_resp.get("token", "N/A"),
                    "api": parsed_resp.get("api", "N/A"),
                    "region": parsed_resp.get("region", "N/A"),
                    "status": parsed_resp.get("status", "live"),
                    "access_token": token_data.get("access_token"),  # Real OAuth token
                    "open_id": token_data.get("open_id")            # ✅ Real open_id from server
                }
            except Exception as e:
                return {"error": f"Failed to deserialize response: {e}"}
        else:
            return {"error": f"HTTP {response.status_code} - {response.reason}"}
    except requests.RequestException as e:
        return {"error": f"Request error: {e}"}

@app.route('/token', methods=['GET'])
def get_token_response():
    """
    Flask endpoint to process GET requests to retrieve a token.
    Requires the query parameters 'uid' and 'password'.
    """
    uid = request.args.get('uid')
    password = request.args.get('password')
    if not uid or not password:
        return jsonify({"error": "Missing parameters: uid and password are required"}), 400

    result = process_token(uid, password)
    if "error" in result:
        return jsonify(result), 500

    jwt_token = result.get("token")
    if not jwt_token:
        return jsonify({"error": "Token not generated"}), 500

    # Decode JWT
    header, payload = decode_full_jwt(jwt_token)

    current_time = int(time.time())
    expiry = int(payload.get("exp", 0) or 0)
    remaining = max(0, expiry - current_time)

    # ✅ Use the real open_id from the token response
    real_open_id = result.get("open_id", "")

    # Fallback for iat (if missing, assume 8-hour token)
    iat = payload.get("iat")
    if iat is None:
        iat = expiry - 28800   # 8 hours before expiry
    else:
        iat = int(iat)

    # Minimal time_info (only 2 fields)
    time_info = {
        "issued_at_utc": format_utc(iat),
        "expiry_time_utc": format_utc(expiry)
    }

    final_response = {
        # STATUS FIRST
        "status": "live" if remaining > 0 else "expired",

        "api": result.get("api"),
        "owner": "DARK OXO!",

        "jwt_header": {
            "algorithm": header.get("alg"),
            "type": header.get("typ"),
            "server": header.get("svr")
        },

        "player_info": {
            "nickname": payload.get("nickname"),
            "account_id": payload.get("account_id"),
            "uid": payload.get("external_uid"),
            "avatar_id": payload.get("reg_avatar")
        },

        "region_info": {
            "region": payload.get("noti_region"),
            "noti_region": payload.get("noti_region"),
            "lock_region": payload.get("lock_region"),
            "lock_time": payload.get("lock_region_time"),
            "country_code": payload.get("country_code")
        },

        "client_info": {
            "platform": payload.get("plat_id"),
            "client_type": payload.get("client_type"),
            "client_version": payload.get("client_version"),
            "release_version": payload.get("release_version"),
            "release_channel": payload.get("release_channel"),
            "emulator": payload.get("is_emulator"),
            "emulator_score": payload.get("emulator_score")
        },

        "time_info": time_info,

        "meta": {
            "success": True,
            "server": payload.get("noti_region"),
            "response_time_ms": 120
        },

        "token_info": {
            "jwt_token": jwt_token,
            "access_token": result.get("access_token"),
            "login_type": "guest",
            "open_id": real_open_id,          # ✅ Now correct: real open_id from server
            "external_id": payload.get("external_id"),
            "external_uid": payload.get("external_uid")
        }
    }

    response = make_response(jsonify(final_response))
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)