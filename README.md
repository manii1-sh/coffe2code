# WhatsApp AI Chatbot 🤖

Simple multi-language WhatsApp chatbot using Twilio and Gemini AI.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Server
```bash
python app.py
```

Server starts on `http://0.0.0.0:8000`

### 3. Expose to Internet (for Twilio)
Use ngrok to make your local server public:
```bash
ngrok http 8000
```

You'll get a URL like: `https://abc123.ngrok.io`

### 4. Configure Twilio
1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to: Messaging → Try it out → Send a WhatsApp message
3. Set webhook:
   - **URL**: `https://abc123.ngrok.io/webhook`
   - **Method**: POST

### 5. Test!
Send a message to your Twilio WhatsApp number and get AI responses!

## 💬 Example Conversations

**English:**
```
You: Hello, how are you?
Bot: Hello! I'm doing great, thank you! How can I help you today?
```

**Hindi:**
```
You: नमस्ते, आप कैसे हैं?
Bot: नमस्ते! मैं बहुत अच्छा हूं, धन्यवाद! मैं आपकी कैसे मदद कर सकता हूं?
```

**Marathi:**
```
You: नमस्कार, तुम्ही कसे आहात?
Bot: नमस्कार! मी छान आहे, धन्यवाद! मी तुम्हाला कशी मदत करू शकतो?
```

## 📁 Files

- `app.py` - Main FastAPI server
- `.env` - Configuration (API keys)
- `requirements.txt` - Python dependencies

## 🔧 How It Works

1. User sends WhatsApp message
2. Twilio receives it → forwards to your webhook
3. Your server processes with Gemini AI
4. AI detects language and responds
5. Response sent back to WhatsApp

## ✅ Features

- Multi-language support (50+ languages)
- Session management (remembers conversation)
- Simple, clean code
- Easy to deploy

---

Made with ❤️ using Twilio + Gemini AI
