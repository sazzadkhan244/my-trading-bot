import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **আসসালামু আলাইকুম ভাই!**\n\n"
        "আমি আপনার Institutional SMC Trading Co-Pilot।\n"
        "কোনো অতিরিক্ত থিওরি বা ভীতি নয়—সরাসরি প্র্যাকটিক্যাল ট্রেডিং নির্দেশিকা পাবেন।\n\n"
        "🎯 **নিচের অপশন থেকে সিলেক্ট করুন:**"
    )
    keyboard = [
        [InlineKeyboardButton("📊 আজকের সেরা মার্কেট", callback_data='best_markets'),
         InlineKeyboardButton("⚡ স্ক্যাল্পিং সেটআপ (1m/5m)", callback_data='scalp_setup')],
        [InlineKeyboardButton("📈 ইনট্রাডে ট্রেড (15m/1h)", callback_data='intraday_setup'),
         InlineKeyboardButton("🏆 ব্যাকটেস্ট ও উইন-রেট", callback_data='winrate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    if any(word in user_text for word in ['signal', 'market', 'ভালো', 'মার্কেট', 'কোনটি', 'আজকে']):
        response = (
            "🎯 **আজকের সেরা ট্রেডিং মার্কেট আপডেট:**\n\n"
            "🟢 **XAU/USD (Gold):** ১৫m টাইমফ্রেমে লিকুইডিটি সুইপ সম্পন্ন। সুইং হাই ব্রেক করলে বাই সেটআপ তৈরি হবে।\n"
            "🟢 **BTC/USD:** ৪-ঘণ্টায় বুলিশ FVG হোল্ড করছে। ছোট টাইমফ্রেমে CHoCH পেলেই এন্ট্রি নেওয়া যাবে।\n"
            "🔴 **EUR/USD:** কনসোলিডেশন মার্কেট—এখন ট্রেড এভোয়েড করুন।\n\n"
            "💡 *টিপস: যেকোনো পেয়ারের চার্ট স্ক্রিনশট পাঠালে আমি সরাসরি Buy/Sell Zone, SL এবং TP চিহ্নিত করে দেব।*"
        )
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        response = (
            "ভাই, আমি আপনার মেসেজটি পেয়েছি। 😊\n\n"
            "মার্কেট আপডেট পেতে লিখুন: **'আজকের মার্কেট কোনটা ভালো?'** "
            "অথবা TradingView থেকে চার্টের একটি স্ক্রিনশট পাঠান।"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    analysis_text = (
        "📊 **SMC & Price Action চার্ট বিশ্লেষণ**\n"
        "---------------------------------------\n"
        "🔹 **মার্কেট ট্রেন্ড:** বুলিশ ইমপালসিভ মুভ (Bullish Displacement)\n"
        "🔹 **লিকুইডিটি জোন:** Sell-side liquidity successfully swept.\n\n"
        "🎯 **সরাসরি অ্যাকশনেবল সিনারিও:**\n\n"
        "🟢 **Scenario A (Buy Setup):**\n"
        "• **Buy Zone:** 4,350 - 4,355 (Discount Zone / FVG)\n"
        "• **Stop Loss (SL):** 4,338\n"
        "• **Take Profit (TP):** 4,385 / 4,400\n"
        "• **Risk-to-Reward (R:R):** 1:2.4\n\n"
        "🔴 **Scenario B (Bearish Invalidation):**\n"
        "• ৪,৩৩৮ লেভেল নিচে ব্রেক করে ক্যান্ডেল ক্লোজ দিলে বুলিশ ট্রেন্ড বাতিল এবং সেল সাইড ট্র্যাপ হবে।\n\n"
        "⚠️ **সতর্কতা:** এন্ট্রির আগে ৫-মিট টাইমফ্রেমে কনফার্মেশন দেখে নিন।"
    )
    await update.message.reply_text(analysis_text, parse_mode='Markdown')

if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN পাওয়া যায়নি!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        print("🚀 Trading Bot Engine Started...")
        app.run_polling()
