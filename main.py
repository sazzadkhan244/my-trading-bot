import os
import logging
import threading
from flask import Flask
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


# ==========================================
# ২. ফ্লাস্ক দিয়ে রেন্ডার পোর্ট ফিক্স (Web Service ফ্রি রাখার জন্য)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Mastermind Trading Bot Web Service is Active & Healthy!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ব্যাকগ্রাউন্ড থ্রেডে ফ্লাস্ক সার্ভার চালু করা যাতে টেলিগ্রাম বটের সাথে কোনো সমস্যা না হয়
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
            "এটি আপনার **Mastermind Trading Bot (Step 1 - Core & UI)**। "
            "এখানে কোনো কাল্পনিক বা ভুয়া সিগন্যাল দেখানো হয় না। ১০০% স্বচ্ছতা এবং প্রফেশনাল "
            "ইঞ্জিনিয়ারিং স্ট্যান্ডার্ড বজায় রেখে বট তৈরি করা হচ্ছে。\n\n"
            "নিচের প্রিমিয়াম মেনু থেকে আপনার কাঙ্ক্ষিত অপশনটি বেছে নিন:"
        )

        keyboard = [
            [InlineKeyboardButton("📊 মার্কেট ওয়াচলিস্ট (ক্যাটাগরি অনুযায়ী)", callback_data="show_watchlist")],
            [InlineKeyboardButton("⚙️ রিয়েল সিস্টেম হেলথ ও স্ট্যাটাস", callback_data="system_health")],
            [InlineKeyboardButton("💡 বটের গাইড ও স্টেজ ইনফো", callback_data="bot_guide")],
            [InlineKeyboardButton("💬 চ্যাট প্লেসহোল্ডার মোড", callback_data="chat_placeholder")]
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
                "📋 **প্রফেশনাল মার্কেট ওয়াচলিস্ট (Step 1B):**\n\n"
                "💱 **মেজর ফরেক্স পেয়ার:**\n"
                f"{forex_str}\n\n"
                "🪙 **মেটাল ও ক্রিপ্টো:**\n"
                f"{crypto_str}\n\n"
                "*(নোট: এগুলো বর্তমানে শুধু ওয়াচলিস্ট হিসেবে আছে। পরবর্তী ডেটা ইঞ্জিন ধাপে লাইভ প্রাইস যুক্ত হবে)*"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "system_health":
            response_msg = (
                "⚙️ **রিয়েল সিস্টেম হেলথ ও স্ট্যাটাস (Step 1):**\n\n"
                "• Telegram Core Engine: `ONLINE` (সচল)\n"
                "• UI & Navigation: `ACTIVE` (সচল)\n"
                "• Data Engine: `NOT CONNECTED` (অপেক্ষমাণ)\n"
                "• Market Analysis: `NOT ACTIVE`\n"
                "• Liquidity Detection: `NOT ACTIVE`\n"
                "• Paper Trading / Backtest: `PENDING`\n\n"
                "যাতে কোনো ভুল বা ফেক সিগন্যাল না আসে, সেজন্য প্রতিটা ধাপ যাচাই করে এগোচ্ছি।"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "bot_guide":
            response_msg = (
                "💡 **বটের গাইড ও বর্তমান স্টেজ:**\n\n"
                "• **বর্তমান স্টেজ:** Step 1 (Core Engine & Premium UI)\n"
                "• **উদ্দেশ্য:** একটি অত্যন্ত নিরাপদ, প্রিমিয়াম এবং গোছানো টেলিগ্রাম ইন্টারফেস তৈরি করা।\n"
                "• **পরবর্তী ধাপ:** Step 2-এ আমরা রিয়েল মার্কেট ডেটা ফেচিং ইঞ্জিন যুক্ত করব।"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "chat_placeholder":
            response_msg = (
                "💬 **চ্যাট প্লেসহোল্ডার মোড:**\n\n"
                "এটি একটি সাধারণ টেক্সট রিসিভার। এখানে কোনো রোবটিক মুখস্থ বুলি বা ফেক এআই প্রমিস নেই। "
                "আপনি সরাসরি যেকোনো কিছু লিখে টেস্ট করতে পারেন।"
            )
            await query.edit_message_text(text=response_msg, parse_mode="Markdown", reply_markup=back_keyboard)

        elif query.data == "back_to_home":
            welcome_text = (
                "🏠 **মূল মেনুতে স্বাগতম!**\n\n"
                "নিচের প্রিমিয়াম অপশনগুলো থেকে আপনার প্রয়োজনীয় সেকশনটি বেছে নিন:"
            )
            home_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📊 মার্কেট ওয়াচলিস্ট (ক্যাটাগরি অনুযায়ী)", callback_data="show_watchlist")],
                [InlineKeyboardButton("⚙️ রিয়েল সিস্টেম হেলথ ও স্ট্যাটাস", callback_data="system_health")],
                [InlineKeyboardButton("💡 বটের গাইড ও স্টেজ ইনফো", callback_data="bot_guide")],
                [InlineKeyboardButton("💬 চ্যাট প্লেসহোল্ডার মোড", callback_data="chat_placeholder")]
            ])
            await query.edit_message_text(text=welcome_text, parse_mode="Markdown", reply_markup=home_keyboard)

    except Exception as e:
        logger.error(f"বাটন হ্যান্ডেলিং করার সময় এরর হয়েছে: {e}")
        await query.edit_message_text(text="দুঃখিত, রিকোয়েস্ট প্রসেস করার সময় একটি টেকনিক্যাল সমস্যা হয়েছে।")


# ==========================================
# ৬. বেসিক টেক্সট মেসেজ হ্যান্ডলার
# ==========================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        reply_msg = f"আপনার কথাটি নোট করা হলো: \"{user_text}\". (এটি একটি বেসিক চ্যাট প্লেসহোল্ডার মোড)।"
        await update.message.reply_text(reply_msg)
    except Exception as e:
        logger.error(f"মেসেজ হ্যান্ডেল করতে গিয়ে সমস্যা হয়েছে: {e}")


# ==========================================
# ৭. গ্লোবাল এরর হ্যান্ডলার
# ==========================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"টেলিগ্রাম আপডেট প্রসেস করার সময় মারাত্মক এক্সেপশন ধরা পড়েছে: {context.error}")


# ==========================================
# ৮. মেইন রান ফাংশন
# ==========================================
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        logger.error("টেলিগ্রাম বট টোকেন পাওয়া যায়নি! দয়া করে .env ফাইলে টোকেন কনফিগার করুন।")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    application.add_error_handler(error_handler)

    logger.info("মাস্টারমাইন্ড ট্রেডিং বট সফলভাবে রান হচ্ছে...")
    application.run_polling()

if __name__ == '__main__':
    main()

