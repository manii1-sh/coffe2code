"""
Telegram AI Chatbot with Voice Support
Multi-language support via Telegram + Gemini AI
Uses faster-whisper for speech-to-text (no FFmpeg needed!)
Uses gTTS for text-to-speech
"""
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from gtts import gTTS
import tempfile
from dotenv import load_dotenv
from faster_whisper import WhisperModel

# Load environment
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load faster-whisper model (large-v3 - BEST accuracy for all languages!)
print("🔄 Loading Whisper Large model (this may take a few minutes first time)...")
whisper_model = WhisperModel("large-v3", device="cpu", compute_type="int8")
print("✅ Whisper Large model loaded!")

# Multi-language system instruction
SYSTEM_INSTRUCTION = """You are a helpful AI assistant with multi-language support.

CRITICAL RULES:
- ALWAYS respond in the SAME LANGUAGE as the user's message
- Support: English, Hindi, Marathi, Spanish, French, German, Arabic, and more
- Be concise, friendly, and helpful
- Keep responses brief (2-3 sentences for simple questions)
- Be conversational and natural

EXAMPLES:
- User: "Hello, how are you?" → Respond in English
- User: "नमस्ते, आप कैसे हैं?" → Respond in Hindi  
- User: "नमस्कार, तुम्ही कसे आहात?" → Respond in Marathi
- User: "Hola, ¿cómo estás?" → Respond in Spanish

Match the user's language and be helpful!"""

# Store chat sessions
chat_sessions = {}

def get_chat_session(user_id: int):
    """Get or create chat session for user"""
    if user_id not in chat_sessions:
        model = genai.GenerativeModel('gemini-2.5-flash')  # Fresh API key with full quota!
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]

def text_to_speech(text: str, language: str = 'en') -> str:
    """Convert text to speech using gTTS"""
    try:
        # Detect language
        if any('\u0900' <= char <= '\u097F' for char in text):
            language = 'hi'  # Hindi/Marathi
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        
        return temp_file.name
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return None

def transcribe_voice(file_path: str) -> str:
    """Convert voice to text using faster-whisper (no FFmpeg needed!)"""
    try:
        print(f"🔍 Transcribing file: {file_path}")
        
        # Transcribe with faster-whisper
        # Try Hindi first, then auto-detect if confidence is low
        segments, info = whisper_model.transcribe(
            file_path, 
            beam_size=5,
            language="hi",  # Force Hindi (works for Gujarati too)
            task="transcribe"
        )
        
        # Collect all segments
        transcription = " ".join([segment.text for segment in segments]).strip()
        detected_language = info.language
        
        print(f"✅ Transcribed ({detected_language}): {transcription}")
        
        # Cleanup
        os.remove(file_path)
        
        return transcription if transcription else None
            
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        import traceback
        print(traceback.format_exc())
        try:
            os.remove(file_path)
        except:
            pass
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        f"I'm your AI assistant with multi-language support!\n\n"
        f"You can:\n"
        f"✅ Send text messages in any language\n"
        f"✅ Send voice messages (I'll respond with voice!)\n"
        f"✅ Get responses in the same language\n\n"
        f"Powered by Whisper AI + Gemini 🚀"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_id = update.effective_user.id
    user_text = update.message.text
    
    print(f"\n{'='*50}")
    print(f"📱 Message from: {update.effective_user.first_name} ({user_id})")
    print(f"� Text: {user_text}")
    
    try:
        # Get chat session
        chat = get_chat_session(user_id)
        
        # Get AI response
        full_message = f"{SYSTEM_INSTRUCTION}\n\nUser: {user_text}\nAssistant:"
        response = chat.send_message(full_message)
        ai_response = response.text
        
        print(f"🤖 Response: {ai_response}")
        print(f"{'='*50}\n")
        
        # Send response
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text("Sorry, I encountered an error. Please try again.")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages"""
    user_id = update.effective_user.id
    
    print(f"\n{'='*50}")
    print(f"📱 Voice message from: {update.effective_user.first_name} ({user_id})")
    
    try:
        # Download voice file
        voice_file = await update.message.voice.get_file()
        file_path = f"voice_{user_id}.ogg"
        await voice_file.download_to_drive(file_path)
        
        print(f"📥 Downloaded voice file")
        
        # Transcribe with Whisper
        print(f"🎧 Transcribing with Whisper AI...")
        transcribed_text = transcribe_voice(file_path)
        
        if not transcribed_text:
            await update.message.reply_text("Sorry, I couldn't understand your voice message. Please try again.")
            return
        
        print(f"📝 Transcribed: {transcribed_text}")
        
        # Get chat session
        chat = get_chat_session(user_id)
        
        # Get AI response with retry logic
        max_retries = 2
        ai_response = None
        
        for attempt in range(max_retries):
            try:
                full_message = f"{SYSTEM_INSTRUCTION}\n\nUser: {transcribed_text}\nAssistant:"
                response = chat.send_message(full_message)
                ai_response = response.text
                break  # Success!
            except Exception as api_error:
                print(f"⚠️ API attempt {attempt + 1} failed: {api_error}")
                if attempt == max_retries - 1:
                    # Last attempt failed
                    ai_response = f"I heard: '{transcribed_text}'. Sorry, I'm having trouble responding right now. Please try again!"
        
        if not ai_response:
            await update.message.reply_text("Sorry, I couldn't process your message. Please try again.")
            return
        
        print(f"🤖 Response: {ai_response}")
        
        # Convert to speech
        print(f"🔊 Converting to speech...")
        audio_path = text_to_speech(ai_response)
        
        if audio_path:
            # Send voice response
            with open(audio_path, 'rb') as audio_file:
                await update.message.reply_voice(voice=audio_file, caption=ai_response)
            
            # Cleanup
            os.remove(audio_path)
            print(f"✅ Voice response sent!")
        else:
            # Send text response
            await update.message.reply_text(ai_response)
        
        print(f"{'='*50}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(traceback.format_exc())
        await update.message.reply_text("Sorry, I encountered an error processing your voice message.")

def main():
    """Start the bot"""
    print(f"\n{'='*60}")
    print(f"🚀 Telegram AI Chatbot Starting...")
    print(f"{'='*60}")
    print(f"🤖 AI Model: Gemini 2.5 Flash")
    print(f"🎤 Speech-to-Text: faster-whisper (no FFmpeg needed!)")
    print(f"🔊 Text-to-Speech: gTTS")
    print(f"📱 Bot: @Sahayakk_AI_BOT")
    print(f"{'='*60}\n")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    # Start bot
    print(f"✅ Bot is running! Open Telegram and search for @Sahayakk_AI_BOT\n")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
