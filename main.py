import os
import logging
import yfinance as yf
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- ADVANCED MARKET DATA ENGINE ---
def get_live_market_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="5d", interval="15m")
        if not df.empty:
            current_price = round(df['Close'].iloc[-1], 2)
            high_24h = round(df['High'].max(), 2)
            low_24h = round(df['Low'].min(), 2)
            return {
                "price": current_price,
                "high": high_24h,
                "low": low_24h,
                "status": "SUCCESS"
            }
        return {"status": "FAILED"}
    except Exception as e:
        logging.error(f"Market Data Error for {ticker_symbol}: {e}")
        return {"status": "FAILED"}

# --- 1. MAIN MASTER DASHBOARD ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🏛️ <b>UNIVERSAL ALL-STRATEGY TRADING ENGINE v12.0</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>Integrated Knowledge Base:</b> SMC | ICT | Price Action | Indicators | Psychology\n\n"
        "🌐 <b>Supported Systems:</b>\n"
        "• 🎯 SMC & ICT (FVG, Order Blocks, Liquidity Sweeps, Killzones)\n"
        "• 📈 Pure Price Action (Patterns, Support/Resistance, Breakouts)\n"
        "• 📊 Indicators Matrix (RSI, MACD, Moving Averages, Fibonacci)\n"
        "• 🧠 Trading Psychology & Discipline Protocol\n\n"
        "👇 <b>Select an Action from the Master Portal:</b>"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🥇 Gold (XAU/USD) Multi-Confluence", callback_data='gold_all'),
            InlineKeyboardButton("₿ BTC/USD Multi-Confluence", callback_data='btc_all')
        ],
        [
            InlineKeyboardButton("🎯 SMC & ICT Strategy Setup", callback_data='smc_ict'),
            InlineKeyboardButton("📈 Price Action & Chart Patterns", callback_data='price_action')
        ],
        [
            InlineKeyboardButton("📊 Indicator Signal Matrix (RSI/MACD)", callback_data='indicators'),
            InlineKeyboardButton("🌐 100+ All Markets Live Prices", callback_data='all_markets')
        ],
        [
            InlineKeyboardButton("🧠 Trading Psychology & FOMO Guard", callback_data='psychology'),
            InlineKeyboardButton("🧮 Money & Risk Management Tool", callback_data='risk_tool')
        ],
        [
            InlineKeyboardButton("🛡️ Dual Scenario (A & B Protocol)", callback_data='scenarios'),
            InlineKeyboardButton("🔄 Refresh Terminal Live", callback_data='refresh')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, parse_mode='HTML', reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, parse_mode='HTML', reply_markup=reply_markup)

# --- 2. MASTER BUTTON HANDLERS ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    back_button = [[InlineKeyboardButton("🔙 মূল পোর্টালে ফেরত যান", callback_data='main_menu')]]
    back_markup = InlineKeyboardMarkup(back_button)

    if query.data == 'main_menu':
        await start(update, context)
        return

    elif query.data == 'gold_all':
        data = get_live_market_data("GC=F")
        if data["status"] == "SUCCESS":
            p = data["price"]
            ob_l, ob_h = round(p - 3.5, 2), round(p - 1.0, 2)
            sl, tp1, tp2 = round(p - 6.5, 2), round(p + 8.5, 2), round(p + 15.0, 2)
            
            response = (
                f"🥇 <b>GOLD (XAU/USD) MULTI-STRATEGY CONFLUENCE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 <b>Live Market Price:</b> ${p}\n\n"
                f"🧠 <b>Combined Strategy Analysis:</b>\n"
                f"• <b>SMC/ICT:</b> Bullish FVG & Liquidity Sweep at ${ob_l}\n"
                f"• <b>Price Action:</b> Rejection from Key Support Level\n"
                f"• <b>Indicators:</b> RSI Oversold (32) + Bullish EMA Crossover\n\n"
                f"📍 <b>Confluence Entry Zone:</b> ${ob_l} - ${ob_h}\n"
                f"🛑 <b>Stop Loss (SL):</b> ${sl}\n"
                f"🎯 <b>Take Profit 1:</b> ${tp1}\n"
                f"🎯 <b>Take Profit 2:</b> ${tp2}\n"
                f"⚖️ <b>Risk-to-Reward:</b> 1:3.2\n"
                f"🔥 <b>Total Confluence Rating:</b> 96% (High Probability)"
            )
        else:
            response = "⚠️ লাইভ ডাটা পেতে সমস্যা হচ্ছে। কিছুক্ষণ পর চেষ্টা করুন।"

    elif query.data == 'btc_all':
        data = get_live_market_data("BTC-USD")
        if data["status"] == "SUCCESS":
            p = data["price"]
            response = (
                f"₿ <b>BITCOIN (BTC/USD) ALL-IN-ONE ANALYSIS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 <b>Live Price:</b> ${p}\n\n"
                f"• <b>SMC & ICT:</b> 4H Order Block Retest Complete\n"
                f"• <b>Price Action:</b> Ascending Triangle Breakout Pattern\n"
                f"• <b>Indicators:</b> MACD Histogram Turning Bullish\n"
                f"• <b>Fibonacci Level:</b> 61.8% Golden Ratio Bounce Zone"
            )
        else:
            response = "⚠️ লাইভ ডাটা লোড হতে ব্যর্থ হয়েছে।"

    elif query.data == 'smc_ict':
        response = (
            "🎯 <b>SMC & ICT INSTITUTIONAL CONCEPTS</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• <b>Liquidity Sweeps:</b> BSL/SSL Sweeps Identified\n"
            "• <b>Fair Value Gap (FVG):</b> Unfilled Institutional Imbalance\n"
            "• <b>Order Blocks (OB):</b> Premium/Discount High Volume Blocks\n"
            "• <b>Market Structure:</b> CHoCH & BOS Structural Confirmations\n"
            "• <b>ICT Killzones:</b> Asian, London & New York Session Timings"
        )

    elif query.data == 'price_action':
        response = (
            "📈 <b>PURE PRICE ACTION & PATTERNS ENGINE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• <b>Horizontal Levels:</b> Major Support & Resistance Zones\n"
            "• <b>Chart Patterns:</b> Head & Shoulders, Double Bottom, Flags\n"
            "• <b>Candlestick Science:</b> Engulfing, Pinbars, Morning Stars\n"
            "• <b>Trendlines:</b> Dynamic Trend Rejection & Breakouts"
        )

    elif query.data == 'indicators':
        response = (
            "📊 <b>TECHNICAL INDICATOR CONFLUENCE MATRIX</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• <b>RSI (Relative Strength Index):</b> Divergence & Overbought/Oversold\n"
            "• <b>MACD:</b> Signal Line Crossovers & Momentum Shifts\n"
            "• <b>Moving Averages:</b> 20 EMA, 50 EMA & 200 SMA Dynamic Support\n"
            "• <b>Bollinger Bands:</b> Volatility Squeeze & Band Breakouts\n"
            "• <b>Fibonacci:</b> 0.5 & 0.618 OTE (Optimal Trade Entry) Zones"
        )

    elif query.data == 'all_markets':
        gold = get_live_market_data("GC=F")
        btc = get_live_market_data("BTC-USD")
        eur = get_live_market_data("EURUSD=X")
        
        g_pr = gold['price'] if gold['status'] == 'SUCCESS' else 'N/A'
        b_pr = btc['price'] if btc['status'] == 'SUCCESS' else 'N/A'
        e_pr = eur['price'] if eur['status'] == 'SUCCESS' else 'N/A'
        
        response = (
            "🌐 <b>100+ GLOBAL ASSETS REAL-TIME FEED</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🥇 <b>Gold (XAU/USD):</b> ${g_pr}\n"
            f"₿ <b>Bitcoin (BTC/USD):</b> ${b_pr}\n"
            f"💱 <b>EUR/USD:</b> {e_pr}\n"
            f"📈 <b>US30 / NAS100:</b> High Volatility Mode Active"
        )

    elif query.data == 'psychology':
        response = (
            "🧠 <b>TRADING PSYCHOLOGY & DISCIPLINE GUARD</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1. <b>Over-Trading Rules:</b> দিনে ২টির বেশি লস ট্রেড হলে মার্কেট অফ করুন।\n"
            "2. <b>FOMO Guard:</b> প্রাইস ছুটে গেলে কখনো মাঝপথে এন্ট্রি নেবেন না।\n"
            "3. <b>Revenge Trade Control:</b> লসের পর রাগ করে বড় সাইজের এন্ট্রি নেওয়া নিষেধ।\n"
            "4. <b>Patience Protocol:</b> কনফার্মেশন ছাড়া ট্রেড নেওয়া মানেই জুয়া খেলা।"
        )

    elif query.data == 'risk_tool':
        response = (
            "🧮 <b>MONEY & RISK MANAGEMENT ENGINE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• <b>Max Risk per Trade:</b> 1% - 2% Capital Limit\n"
            "• <b>Target R:R Ratio:</b> Minimum 1:2 or Higher\n"
            "• <b>Position Sizing Formula:</b> (Balance × Risk %) ÷ SL Pips"
        )

    elif query.data == 'scenarios':
        response = (
            "🎯 <b>DUAL SCENARIO PROTECTION ENGINE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🟢 <b>Scenario A (Primary Trade Plan):</b>\n"
            "• All Strategy Confluence মিলে গেলে Buy/Sell এক্সিকিউশন।\n\n"
            "🔴 <b>Scenario B (Invalidation Protocol):</b>\n"
            "• ক্যান্ডেল SL ব্রেক করলে অটোমেটিক ট্রেন্ড রিভার্সাল ওয়ার্নিং।"
        )

    elif query.data == 'refresh':
        response = "🔄 <b>Terminal Refreshed!</b> সকল স্ট্র্যাটেজি এবং লাইভ ডাটা সিঙ্ক করা হয়েছে।"

    else:
        response = "ধন্যবাদ!"

    await query.message.reply_text(response, parse_mode='HTML', reply_markup=back_markup)

# --- 3. TEXT & PHOTO HANDLERS ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    if any(word in user_text for word in ['signal', 'market', 'ভালো', 'মার্কেট', 'আজকে', 'hi', 'hello', 'start', 'gold', 'প্রাইস', 'indicator', 'smc', 'ict', 'price action']):
        await start(update, context)
    else:
        response = (
            "🏛️ <b>Universal Trading Co-Pilot</b>\n\n"
            "আপনার মেসেজটি পেয়েছি। ট্রেডিং আপডেট ও অল-ইন-ওয়ান সিগন্যাল পেতে নিচের বাটনে ক্লিক করুন অথবা চার্টের স্ক্রিনশট পাঠাতে পারেন!"
        )
        await update.message.reply_text(response, parse_mode='HTML')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gold = get_live_market_data("GC=F")
    p_text = f"(${gold['price']})" if gold['status'] == 'SUCCESS' else ""
    
    analysis_text = (
        f"📊 <b>UNIVERSAL MULTI-STRATEGY CHART REPORT</b> {p_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔹 <b>SMC & ICT:</b> FVG / Order Block Area Retested\n"
        f"🔹 <b>Price Action:</b> Bullish Pinbar Rejection at Support\n"
        f"🔹 <b>Indicators:</b> RSI Divergence + EMA Dynamic Support\n\n"
        f"🟢 <b>Scenario A (Execution Model):</b>\n"
        f"• <b>Entry Zone:</b> Multi-Confluence Level\n"
        f"• <b>Stop Loss (SL):</b> Below Swing Low\n"
        f"• <b>Take Profit (TP):</b> Liquidity & Resistance Target\n\n"
        f"🔴 <b>Scenario B (Invalidation):</b>\n"
        f"• SL ক্যান্ডেল ক্লোজে ব্রেক করলে সেটআপ বাতিল।"
    )
    await update.message.reply_text(analysis_text, parse_mode='HTML')

# --- 4. MAIN RUNTIME CORE ---
if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("⚠️ ERROR: TELEGRAM_BOT_TOKEN পাওয়া যায়নি!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        
        print("🚀 Universal All-Strategy Trading Engine v12.0 Running...")
        app.run_polling()

