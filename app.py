"""
Simple WhatsApp AI Chatbot
Multi-language support via Twilio + Gemini AI
"""
from fastapi import FastAPI, Form
from fastapi.responses import Response
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Validate config
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    raise ValueError("Twilio credentials not found in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Multi-language system instruction (from backend)
SYSTEM_INSTRUCTION = """You are a helpful AI assistant with multi-language support.

CRITICAL RULES:
- ALWAYS respond in the SAME LANGUAGE as the user's message
- Support: English, Hindi, Marathi, Spanish, French, German, Arabic, and more
- Be concise, friendly, and helpful
- Keep responses brief for WhatsApp (2-3 sentences for simple questions)
- Be conversational and natural

EXAMPLES:
- User: "Hello, how are you?" → Respond in English
- User: "नमस्ते, आप कैसे हैं?" → Respond in Hindi  
- User: "नमस्कार, तुम्ही कसे आहात?" → Respond in Marathi
- User: "Hola, ¿cómo estás?" → Respond in Spanish

Match the user's language and be helpful!"""

# Initialize app
app = FastAPI(title="WhatsApp AI Chatbot")

# Store chat sessions
chat_sessions = {}

@app.get("/")
def home():
    """Health check"""
    return {
        "status": "✅ Running",
        "service": "WhatsApp AI Chatbot",
        "features": ["Multi-language", "Gemini AI", "Twilio WhatsApp"]
    }

@app.get("/webhook")
async def webhook_validation():
    """Twilio webhook validation"""
    return {"status": "Webhook is ready!", "service": "WhatsApp AI Chatbot"}

@app.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    """
    Twilio webhook - receives WhatsApp messages
    """
    print(f"\n{'='*50}")
    print(f"📱 Message from: {From}")
    print(f"💬 Text: {Body}")
    
    try:
        # Get or create chat session for this user
        if From not in chat_sessions:
            model = genai.GenerativeModel('gemini-2.5-flash')
            chat_sessions[From] = model.start_chat(history=[])
        
        # Get AI response with system instruction in the message
        chat = chat_sessions[From]
        full_message = f"{SYSTEM_INSTRUCTION}\n\nUser: {Body}\nAssistant:"
        response = chat.send_message(full_message)
        ai_response = response.text
        
        print(f"🤖 Response: {ai_response}")
        print(f"{'='*50}\n")
        
        # Create TwiML response using Twilio library
        twiml_response = MessagingResponse()
        twiml_response.message(ai_response)
        
        return Response(content=str(twiml_response), media_type="application/xml")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        twiml_response = MessagingResponse()
        twiml_response.message("Sorry, I encountered an error. Please try again.")
        return Response(content=str(twiml_response), media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*60}")
    print(f"🚀 WhatsApp AI Chatbot Starting...")
    print(f"{'='*60}")
    print(f"📡 Server: http://0.0.0.0:8000")
    print(f"🤖 AI Model: gemini-2.5-flash")
    print(f"📱 Twilio Number: {TWILIO_WHATSAPP_NUMBER}")
    print(f"{'='*60}")
    print(f"\n⚠️  Configure Twilio Webhook:")
    print(f"   URL: http://YOUR_PUBLIC_URL/webhook")
    print(f"   Method: POST")
    print(f"{'='*60}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
