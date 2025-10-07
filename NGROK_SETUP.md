# 🌐 ngrok Setup - Make Your Server Globally Accessible

## What is ngrok?

**ngrok** creates a secure tunnel from the internet to your local server, giving you a public URL that anyone can access.

**Benefits:**
- ✅ Access server from anywhere
- ✅ Test with Flutter app on phone
- ✅ Share with team/clients
- ✅ No port forwarding needed
- ✅ HTTPS included for free

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install ngrok

**Option A: Download (Recommended)**
1. Visit: https://ngrok.com/download
2. Download for Windows
3. Extract `ngrok.exe` to a folder
4. Add to PATH or keep in project folder

**Option B: Using Chocolatey**
```bash
choco install ngrok
```

**Option C: Using pip**
```bash
pip install pyngrok
```

---

### Step 2: Get Auth Token (Free Account)

1. Sign up: https://dashboard.ngrok.com/signup
2. Get token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Authenticate ngrok:
```bash
ngrok authtoken YOUR_TOKEN_HERE
```

---

### Step 3: Start Server with ngrok

**Method 1: Automatic (Easiest)**
```bash
python setup_ngrok.py
```

**Method 2: Batch File**
```bash
start_with_ngrok.bat
```

**Method 3: Manual (2 Terminals)**

Terminal 1 (Server):
```bash
python server.py
```

Terminal 2 (ngrok):
```bash
ngrok http 3000
```

---

## 📱 What You'll Get

### Public URL:
```
https://1234-56-78-90-123.ngrok-free.app
```

### Features:
- ✅ Works from anywhere in the world
- ✅ HTTPS encryption included
- ✅ Inspect all requests at http://localhost:4040
- ✅ Free tier: 1 tunnel, 40 connections/min
- ✅ Reconnects automatically

---

## 🔗 How to Connect

### From test_client.py:
```python
# Change SERVER_URL to your ngrok URL
SERVER_URL = "https://1234-56-78-90-123.ngrok-free.app"
```

### From Flutter App:
```dart
import 'package:socket_io_client/socket_io_client.dart' as IO;

IO.Socket socket = IO.io(
  'https://1234-56-78-90-123.ngrok-free.app',
  <String, dynamic>{
    'transports': ['websocket'],
    'autoConnect': true,
  }
);
```

### From Web Browser (Test):
```
https://1234-56-78-90-123.ngrok-free.app
```

---

## 🖥️ ngrok Web Interface

**Access at: http://localhost:4040**

Features:
- 📊 View all HTTP requests
- 🔄 Replay requests
- 🔍 Inspect request/response details
- 📈 Traffic statistics
- 🐛 Debug issues

---

## 📋 Full Setup Example

### Terminal 1 (Server):
```bash
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python server.py
```

Output:
```
Loading YOLOv11x model...
✓ Model loaded successfully!
Configuration:
  Confidence threshold: 70%
Starting server on 0.0.0.0:3000
```

---

### Terminal 2 (ngrok):
```bash
ngrok http 3000
```

Output:
```
ngrok

Session Status                online
Account                       your@email.com (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:3000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

---

### Terminal 3 (Test Client):
```bash
# Update SERVER_URL in test_client.py first
python test_client.py
```

Or test from any device with internet:
```bash
curl https://abc123.ngrok-free.app
```

---

## 🎯 Testing with Phone

### Step 1: Get ngrok URL
From ngrok window, copy the HTTPS URL:
```
https://abc123.ngrok-free.app
```

### Step 2: Use in Flutter App
```dart
final socket = IO.io('https://abc123.ngrok-free.app', <String, dynamic>{
  'transports': ['websocket'],
  'autoConnect': true,
});

// Send frame
socket.emit('frame', {'image': base64Image});

// Receive detections
socket.on('detections', (data) {
  print('Detected ${data['count']} objects');
});
```

### Step 3: Test from Phone
Open Flutter app on phone, it will connect to your PC via ngrok!

---

## ⚙️ Configuration Options

### Custom Subdomain (Paid Plans)
```bash
ngrok http 3000 --subdomain=yolo-detection
# URL: https://yolo-detection.ngrok-free.app
```

### Custom Region
```bash
ngrok http 3000 --region=eu  # Europe
ngrok http 3000 --region=ap  # Asia Pacific
ngrok http 3000 --region=au  # Australia
ngrok http 3000 --region=sa  # South America
```

### Basic Auth Protection
```bash
ngrok http 3000 --basic-auth="username:password"
```

### Static Domain (Paid)
```bash
ngrok http 3000 --hostname=your-domain.com
```

---

## 🔐 Security Considerations

### Free Tier:
- ✅ HTTPS encryption
- ✅ Random URL each restart
- ⚠️ URL changes on restart
- ⚠️ Anyone with URL can access

### Best Practices:
1. **Don't share URL publicly**
2. **Add authentication** if needed
3. **Monitor access** via http://localhost:4040
4. **Use paid plan** for static URLs
5. **Close tunnel** when not in use

### Add Authentication (Optional):
Update `server.py`:
```python
@sio.event
async def connect(sid, environ):
    # Check for authentication token
    token = environ.get('HTTP_AUTHORIZATION')
    if token != 'YOUR_SECRET_TOKEN':
        raise ConnectionRefusedError('unauthorized')
    print(f"Client connected: {sid}")
```

---

## 📊 Free vs Paid Plans

### Free Tier:
- ✅ 1 ngrok process
- ✅ 40 connections/minute
- ✅ HTTPS
- ⚠️ Random URL (changes on restart)
- ⚠️ ngrok branding page

### Paid Plans ($8+/month):
- ✅ Custom subdomain
- ✅ Static domain
- ✅ More connections
- ✅ No branding page
- ✅ Multiple tunnels
- ✅ Reserved domains

---

## 🐛 Troubleshooting

### Issue: "command not found: ngrok"
**Solution:** Add ngrok to PATH or run from ngrok folder
```bash
# Windows: Add to PATH
# Or run from folder
cd C:\path\to\ngrok
ngrok http 3000
```

### Issue: "authentication required"
**Solution:** Run auth token command
```bash
ngrok authtoken YOUR_TOKEN
```

### Issue: "tunnel not found"
**Solution:** Make sure server is running first
```bash
# Terminal 1: Start server first
python server.py

# Terminal 2: Then start ngrok
ngrok http 3000
```

### Issue: "ERR_NGROK_108"
**Solution:** Check your internet connection and firewall

### Issue: Can't see public URL
**Solution:** Visit http://localhost:4040 to see tunnel info

---

## 💡 Usage Tips

### 1. Keep ngrok Running
Leave both server and ngrok running while testing

### 2. Use Web Interface
Monitor all requests at http://localhost:4040

### 3. Save Your URL
Copy ngrok URL immediately (it changes on restart)

### 4. Test Locally First
Make sure server works locally before using ngrok

### 5. Monitor Performance
Check latency in ngrok dashboard

---

## 📱 Example: Full Workflow

### PC (Server):
```bash
# Terminal 1: Start server
cd C:\Users\SANJAI\Desktop\AI\YOLO\yolov11x-backend
python server.py

# Terminal 2: Start ngrok
ngrok http 3000

# Note the URL: https://abc123.ngrok-free.app
```

### Phone (Flutter App):
```dart
// Update connection URL
final socket = IO.io(
  'https://abc123.ngrok-free.app',
  <String, dynamic>{'transports': ['websocket']},
);

// Capture and send frame
final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
final base64 = base64Encode(bytes.buffer.asUint8List());
socket.emit('frame', {'image': base64});

// Receive detections
socket.on('detections', (data) {
  setState(() {
    detections = data['detections'];
  });
});
```

### Result:
Phone camera → ngrok → Your PC → YOLO detection → ngrok → Phone display

---

## ✅ Verification Checklist

Test your setup:
- [ ] ngrok installed and authenticated
- [ ] Server starts successfully
- [ ] ngrok tunnel created
- [ ] Public URL accessible
- [ ] Web interface works (http://localhost:4040)
- [ ] test_client.py connects with public URL
- [ ] Detections working over public URL

---

## 🎉 Summary

### Setup Commands:
```bash
# Install and authenticate
ngrok authtoken YOUR_TOKEN

# Start server
python server.py

# Start tunnel (new terminal)
ngrok http 3000

# Get URL from ngrok output or visit:
http://localhost:4040
```

### Your Server is Now:
- ✅ Accessible from anywhere
- ✅ Secure (HTTPS)
- ✅ Ready for mobile testing
- ✅ Shareable with team
- ✅ Monitorable via web interface

---

## 📚 Resources

- **ngrok Dashboard:** https://dashboard.ngrok.com
- **Documentation:** https://ngrok.com/docs
- **Pricing:** https://ngrok.com/pricing
- **Support:** https://ngrok.com/support

---

## 🚀 Next Steps

After ngrok is working:
1. Test with local client
2. Test from phone/tablet
3. Share with team
4. Deploy Flutter app
5. Consider paid plan for production

Your YOLOv11x server is now globally accessible! 🌍

