# 🚀 ngrok Quick Start - 3 Minutes to Global Access

## ⚡ Super Fast Setup

### 1️⃣ Install ngrok (1 minute)
```bash
# Download from: https://ngrok.com/download
# Extract and double-click ngrok.exe
```

### 2️⃣ Get Free Account (1 minute)
```bash
# Sign up: https://dashboard.ngrok.com/signup
# Get token: https://dashboard.ngrok.com/get-started/your-authtoken

ngrok authtoken YOUR_TOKEN_HERE
```

### 3️⃣ Start Everything (1 minute)
```bash
# Option A: Double-click
start_with_ngrok.bat

# Option B: Manual
# Terminal 1:
python server.py

# Terminal 2:
ngrok http 3000
```

---

## 📋 What You Get

### Your Public URL:
```
https://abc123-45-67-89.ngrok-free.app
```

**Share this URL to:**
- Test from phone ✅
- Share with team ✅
- Deploy Flutter app ✅
- Access anywhere ✅

---

## 🔗 Update Your Client

### test_client.py:
```python
SERVER_URL = "https://your-url.ngrok-free.app"
```

### Flutter App:
```dart
socket.connect('https://your-url.ngrok-free.app');
```

---

## 🖥️ Monitor Requests

Visit: **http://localhost:4040**

See all requests, responses, and debug issues!

---

## 🎯 Common Commands

```bash
# Start tunnel
ngrok http 3000

# View tunnel info
curl http://localhost:4040/api/tunnels

# Stop tunnel
Ctrl+C
```

---

## ✅ Verify It Works

```bash
# From anywhere (even phone):
curl https://your-url.ngrok-free.app

# Should see server response
```

---

## 📱 Test from Phone

1. Copy your ngrok URL
2. Open Flutter app
3. Update socket URL
4. Test detection with phone camera!

---

## 💡 Pro Tips

- ⭐ URL changes each restart (free tier)
- ⭐ Keep both server and ngrok running
- ⭐ Check http://localhost:4040 for URL
- ⭐ Free tier: 40 connections/min
- ⭐ Close tunnel when not in use

---

## 🐛 Quick Fixes

**Can't find ngrok?**
→ Add to PATH or run from ngrok folder

**"authentication required"?**
→ Run: `ngrok authtoken YOUR_TOKEN`

**Tunnel not working?**
→ Start server first, then ngrok

**Need help?**
→ See NGROK_SETUP.md for full guide

---

## 🎉 You're Done!

Your server is now accessible from anywhere in the world!

```
Local:  http://localhost:3000
Public: https://your-url.ngrok-free.app
```

Test it now! 🚀

