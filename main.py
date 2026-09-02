import os
import logging
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv

# ==========================================
# ১. এনভায়রনমেন্ট ও লগিং সেটআপ
# ==========================================
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# জেমিনি এআই কনফিগারেশন
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    generation_config = {
        "temperature": 0.7,
    }
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        system_instruction="You are Mastermind, an elite, professional Forex and Smart Money Concepts (SMC) trading assistant. Provide clear, risk-aware, and precise trading insights in a supportive tone."
    )
    logger.info("Gemini AI সফলভাবে কনফিগার করা হয়েছে।")
else:
    model = None
    logger.warning("GEMINI_API_KEY পাওয়া যায়নি! এআই চ্যাট ফিচারটি অফ থাকবে।")


# ==========================================
# ২. ফ্লাস্ক দিয়ে রেন্ডার পোর্ট ফিক্স
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Mastermind AI Trading Bot Web Service is Active & Healthy!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()


# ==========================================
# ৩. ডেটা স্ট্রাকচার ও মার্কেট ওয়াচলিস্ট
# ==========================================
FOREX_MAJORS = [
    "1. EUR/USD [Watchlist]",
    "2. GBP/USD [Watchlist]",
    "3. USD/JPY [Watchlist]",
    "4. AUD/USD [Watchlist]",
    "5. USD/CAD [Watchlist]",
    "6. NZD/USD [Watchlist]",
    "7. GBP/JPY [Watchlist]"
]

METALS_AND_CRYPTO = [
    "8. Gold (XAUUSD) [Ref: GC=F Watchlist]",
    "9. Bitcoin (BTCUSD) [Watchlist]",
    "10. Ethereum (ETHUSD) [Watchlist]"
]


# ==========================================
# ৪. কোর টেলিগ্রাম ইঞ্জিন: /start কমান্ড হ্যান্ডলার
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_name = update.effective_user.first_name
        
        welcome_text = (
            f"স্বাগতম ভাই, **{user_name}**! 🚀\n\n"
            "এটি আপনার **Mastermind AI Trading Bot**। এখন এটি সরাসরি জেমিনি এআই দ্বারা চালিত! "
            "ফরেক্স, এসএমসি (SMC) বা মার্কেট নিয়ে যেকোনো কিছু সরাসরি চ্যাটে জিজ্ঞেস করতে পারেন।\n\n"
            "নিচের প্রিমিয়াম মেনু থেকে আপনার কাঙ্ক্ষিত অপশনটি বেছে নিন:"
        )

        keyboard = [
            [InlineKeyboardButton("📊 মার্কেট ওয়াচলিস্ট (ক্যাটাগরি অনুযায়ী)", callback_data="show_watchlist")],
            [InlineKeyboardButton("⚙️ রিয়েল সিস্টেম হেলথ ও স্ট্যাটাস", callback_data="system_health")],
            [InlineKeyboardButton("💡 বটের গাইড ও স্টেজ ইনফো", callback_data="bot_guide")],
            [InlineKeyboardButton("💬 এআই চ্যাট মোড", callback_data="chat_placeholder")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
    
    except Exception as e:
        logger.error(f"start কমান্ড এক্সিকিউট করতে গিয়ে এরর হয়েছে: {e}")
        await update.message.reply_text("দুঃখিত, সিস্টেমে সাময়িক সমস্যা হয়েছে। একটু পর আবার চেষ্টা করুন।")


# ==========================================
# ৫. ইনলাইন বাটন ক্লিক ও নেভিগেশন হ্যান্ডলার
# ==========================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="back_to_home")]
        ])

        if query.data == "show_watchlist":
            forex_str = "\n".join(FOREX_MAJORS)
            crypto_str = "\n".join(METALS_AND_CRYPTO)
            
            response_msg = (
                "📋 **প্রফেশনাল মার্কেট ওয়াচলিস্ট:**\n\n"
                "💱 **মেজর ফরেক্স পেয়ার:**\n"
                f"{forex_str}\n\n"
                "🪙 **মেটাল ও ক্রিপ্টো:**\n"
                f"{crypto_str}\n\n"
                "*(নোট: পরবর্তী ধাপে লাইভ প্রাইস ইঞ্জিন যুক্ত হবে)*"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "system_health":
            ai_status = "ONLINE (Active)" if model else "NOT CONNECTED"
            response_msg = (
                "⚙️ **রিয়েল সিস্টেম হেলথ ও স্ট্যাটাস:**\n\n"
                "• Telegram Core Engine: `ONLINE` (সচল)\n"
                "• UI & Navigation: `ACTIVE` (সচল)\n"
                f"• Gemini AI Assistant: `{ai_status}`\n"
                "• Data Engine: `PENDING`"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "bot_guide":
            response_msg = (
                "💡 **বটের গাইড ও বর্তমান স্টেজ:**\n\n"
                "• **বর্তমান স্টেজ:** Gemini AI Integration Enabled\n"
                "• **উদ্দেশ্য:** ইউজারের সাথে ন্যাচারাল চ্যাট এবং ট্রেডিং বিষয়ে রিয়েল-টাইম এআই গাইডেন্স প্রদান করা।"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "chat_placeholder":
            response_msg = (
                "💬 **এআই চ্যাট মোড সক্রিয়:**\n\n"
                "এখন আপনি যেকোনো টেক্সট বা প্রশ্ন সরাসরি চ্যাটে পাঠাতে পারেন। জেমিনি এআই সরাসরি তার উত্তর দেবে!"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "back_to_home":
            welcome_text = "🏠 **মূল মেনুতে স্বাগতম!** অপশন বেছে নিন:"
            home_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 মার্কেট ওয়াচলিস্ট (ক্যাটাগরি অনুযায়ী)", callback_data="show_watchlist")],
                [InlineKeyboardButton("⚙️ রিয়েল সিস্টেম হেলথ ও স্ট্যাটাস", callback_data="system_health")],
                [InlineKeyboardButton("💡 বটের গাইড ও স্টেজ ইনফো", callback_data="bot_guide")],
                [InlineKeyboardButton("💬 এআই চ্যাট মোড", callback_data="chat_placeholder")]
            ])
            await query.edit_message_text(text=welcome_text, parse_mode="Markdown", reply_markup=home_keyboard)

    except Exception as e:
        logger.error(f"বাটন হ্যান্ডেল করতে গিয়ে এরর: {e}")


# ==========================================
# ৬. জেমিনি এআই টেক্সট মেসেজ হ্যান্ডলার
# ==========================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        
        if not model:
            await update.message.reply_text("এআই মডেল কনফিগার করা নেই। দয়া করে GEMINI_API_KEY চেক করুন।")
            return

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        response = model.generate_content(user_text)
        ai_reply = response.text

        await update.message.reply_text(ai_reply)

    except Exception as e:
        logger.error(f"এআই মেসেজ প্রসেস করতে গিয়ে সমস্যা হয়েছে: {e}")
        await update.message.reply_text("দুঃখিত, এআই থেকে উত্তর আনতে সমস্যা হয়েছে। একটু পরে আবার চেষ্টা করুন।")


# ==========================================
# ۷. গ্লোবাল এরর হ্যান্ডলার
# ==========================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"টেলিগ্রাম আপডেট এরর: {context.error}")


# ==========================================
# ৮. মেইন রান ফাংশন
# ==========================================
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        logger.error("টেলিগ্রাম বট টোকেন পাওয়া যায়নি!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.add_error_handler(error_handler)

    logger.info("মাস্টারমাইন্ড এআই ট্রেডিং বট সফলভাবে রান হচ্ছে...")
    application.run_polling()

if __name__ == '__main__':
    main()

