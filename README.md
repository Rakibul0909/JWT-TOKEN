🔐 Token Generation API

A lightweight Flask-based API to generate and decode authentication tokens using UID and password.

---

🚀 Endpoint
```
http://127.0.0.1:5000/token?uid={uid}&password={password}
```
---

📌 Example Request
```
/token?uid=4644343519&password=866D6D72
```
---

📥 Query Parameters

Parameter| Type| Required| Description
uid| string| ✅ Yes| User ID
password| string| ✅ Yes| Account password

---

✅ Successful Response
```
{
  "status": "live",
  "api": "example_api",
  "owner": "DARK OXO!",
  
  "jwt_header": {
    "algorithm": "HS256",
    "type": "JWT",
    "server": "example"
  },

  "player_info": {
    "nickname": "PlayerName",
    "account_id": "123456",
    "uid": "4644343519",
    "avatar_id": "102"
  },

  "region_info": {
    "region": "IND",
    "noti_region": "IND",
    "lock_region": "IND",
    "lock_time": "0",
    "country_code": "IN"
  },

  "client_info": {
    "platform": "4",
    "client_type": "2",
    "client_version": "1.108.3",
    "release_version": "OB52",
    "release_channel": "3rd_party",
    "emulator": false,
    "emulator_score": "0"
  },

  "time_info": {
    "issued_at_utc": "2026-03-29 13:05:07 UTC",
    "expiry_time_utc": "2026-03-29 21:05:07 UTC"
  },

  "meta": {
    "success": true,
    "server": "IND",
    "response_time_ms": 120
  },

  "token_info": {
    "jwt_token": "your_jwt_token_here",
    "access_token": "your_access_token_here",
    "login_type": "guest",
    "open_id": "hashed_open_id",
    "external_id": "external_id_value",
    "external_uid": "4644343519"
  }
}
```
---

❌ Error Response

Missing Parameters

{
  "error": "Missing parameters: uid and password are required"
}

Token Failure

{
  "error": "Failed to retrieve token"
}

---

⚙️ Features

- 🔑 Generates JWT token using UID & password
- 🔍 Decodes JWT header and payload
- 🕒 Provides issued and expiry time (UTC)
- 📊 Structured response with player & client info
- 🔐 Secure AES + Protobuf communication

---

🧠 Notes

- Token validity is typically 8 hours
- "issued_at_utc" is derived from JWT ("iat")
- If missing, fallback = "expiry - 8 hours"
- Always rely on server-provided "exp" for accuracy

---

🛠️ Tech Stack

- Python (Flask)
- Requests
- Protobuf
- AES Encryption (PyCryptodome)

---

📡 Deployment

Default port:

5000

Run server:

python app.py

---

👤 Author

DARK OXO!

---