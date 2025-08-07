import requests
import pandas as pd
import pandas_ta as ta
import time
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime
import os # Required for environment variables

# --- CONFIGURATION ---
# Securely reads your secret keys from Render's environment variables.
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- YOUR CUSTOM MACD SETTINGS ---
# Settings from your screenshot: 4, 10, 9
FAST_SETTING = 4
SLOW_SETTING = 10
SIGNAL_SETTING = 9


# The list of symbols for the AUTOMATED reports
SYMBOLS_TO_WATCH = [
    "1000000BOBUSDT.P", "1000000MOGUSDT.P", "1000BONKUSDT.P", "1000CATUSDT.P", "1000CHEEMSUSDT.P", "1000FLOKIUSDT.P", "1000LUNCUSDT.P", "1000PEPEUSDT.P",
    "1000RATSUSDT.P", "1000SATSUSDT.P", "1000SHIBUSDT.P", "1000WHYUSDT.P", "1000XECUSDT.P", "1000XUSDT.P", "1INCHUSDT.P", "1MBABYDOGEUSDT.P",
    "A2ZUSDT.P", "AAVEUSDT.P", "ACXUSDT.P", "ACTUSDT.P", "ADAUSDT.P", "AERGOUSDT.P", "AEROUSDT.P", "AEVOUSDT.P", "AGLDUSDT.P", "AGTUSDT.P", "AI16ZUSDT.P", "AINUSDT.P",
    "AIOTUSDT.P", "AIUSDT.P", "AIXBTUSDT.P", "AKTUSDT.P", "ALCHUSDT.P", "ALGOUSDT.P", "ALICEUSDT.P", "ALPINEUSDT.P", "ALPHAUSDT.P", "ALTUSDT.P", "ANKRUSDT.P",
    "APEUSDT.P", "API3USDT.P", "APTUSDT.P", "ARCUSDT.P", "ARBUSDT.P", "ARKMUSDT.P", "ARKUSDT.P", "ARUSDT.P", "ASRUSDT.P", "ASTRUSDT.P", "ATAUSDT.P", "ATHUSDT.P",
    "ATOMUSDT.P", "AUCTIONUSDT.P", "AUSDT.P", "AVAAIUSDT.P", "AVAUSDT.P", "AVAXUSDT.P", "AWEUSDT.P", "AXLUSDT.P", "AXSUSDT.P",
    "B2USDT.P", "B3USDT.P", "BABYUSDT.P", "BAKEUSDT.P", "BANANAUSDT.P", "BANANAS31USDT.P", "BANDUSDT.P", "BANKUSDT.P", "BANUSDT.P", "BATUSDT.P", "BBUSDT.P", "BCHUSDT.P", "BDXNUSDT.P", "BEAMXUSDT.P",
    "BELUSDT.P", "BERAUSDT.P", "BICOUSDT.P", "BIDUSDT.P", "BIGTIMEUSDT.P", "BIOUSDT.P", "BMTUSDT.P", "BNBUSDT.P", "BNTUSDT.P", "BOMEUSDT.P", "BRETTUSDT.P", "BROCCOLI714USDT.P",
    "BROCCOLIF3BUSDT.P", "BRUSDT.P", "BSVUSDT.P", "BSWUSDT.P", "BTCDOMUSDT.P", "BTCUSDT.P", "BULLAUSDT.P", "BUSDT.P",
    "C98USDT.P", "CAKEUSDT.P", "CELOUSDT.P", "CELRUSDT.P", "CETUSUSDT.P", "CFXUSDT.P", "CGPTUSDT.P", "CHESSUSDT.P", "CHILLGUYUSDT.P", "CHRUSDT.P", "CHZUSDT.P", "CKBUSDT.P", "COMPUSDT.P", "COSUSDT.P", "COTIUSDT.P",
    "COWUSDT.P", "CROSSUSDT.P", "CRVUSDT.P", "CTKUSDT.P", "CTSIUSDT.P", "CUSDT.P", "CVCUSDT.P", "CVXUSDT.P", "CYBERUSDT.P",
    "DASHUSDT.P", "DEEPUSDT.P", "DEFIUSDT.P", "DEGENUSDT.P", "DEGOUSDT.P", "DENTUSDT.P", "DEXEUSDT.P", "DFUSDT.P", "DIAUSDT.P", "DMCUSDT.P", "DOGEUSDT.P", "DOGSUSDT.P", "DOLOUSDT.P", "DOODUSDT.P",
    "DOTUSDT.P", "DRIFTUSDT.P", "DUSDT.P", "DUSKUSDT.P", "DYDXUSDT.P",
    "EDUUSDT.P", "EGLDUSDT.P", "EIGENUSDT.P", "ENAUSDT.P", "ENJUSDT.P", "ENSUSDT.P", "EPICUSDT.P", "EPTUSDT.P", "ERAUSDT.P", "ESPORTSUSDT.P", "ETCUSDT.P", "ETHFIUSDT.P", "ETHUSDT.P", "ETHWUSDT.P",
    "FARTCOINUSDT.P", "FETUSDT.P", "FHEUSDT.P", "FIDAUSDT.P", "FILUSDT.P", "FIOUSDT.P", "FISUSDT.P", "FLOWUSDT.P", "FLUXUSDT.P", "FLMUSDT.P", "FORMUSDT.P", "FORTHUSDT.P", "FUNUSDT.P", "FUSDT.P", "FXSUSDT.P",
    "GALAUSDT.P", "GASUSDT.P", "GHSTUSDT.P", "GLMUSDT.P", "GMTUSDT.P", "GMXUSDT.P", "GOATUSDT.P", "GPSUSDT.P", "GRASSUSDT.P", "GRIFFAINUSDT.P", "GRTUSDT.P", "GTCUSDT.P", "GUNUSDT.P",
    "GUSDT.P",
    "HAEDALUSDT.P", "HBARUSDT.P", "HEIUSDT.P", "HIFIUSDT.P", "HIGHUSDT.P", "HIPPOUSDT.P", "HIVEUSDT.P", "HMSTRUSDT.P", "HFTUSDT.P", "HOMEUSDT.P", "HOOKUSDT.P",
    "HOTUSDT.P", "HUMAUSDT.P", "HUSDT.P", "HYPEUSDT.P", "HYPERUSDT.P",
    "ICPUSDT.P", "ICNTUSDT.P", "ICXUSDT.P", "IDOLUSDT.P", "IDUSDT.P", "ILVUSDT.P", "IMXUSDT.P", "INITUSDT.P", "INJUSDT.P", "IOSTUSDT.P", "IOTAUSDT.P", "IOTXUSDT.P", "IOUSDT.P", "IPUSDT.P",
    "JASMYUSDT.P", "JELLYJELLYUSDT.P", "JOEUSDT.P", "JSTUSDT.P", "JTOUSDT.P", "JUPUSDT.P",
    "KAIAUSDT.P", "KAITOUSDT.P", "KASUSDT.P", "KAVAUSDT.P", "KDAUSDT.P", "KERNELUSDT.P", "KMNOUSDT.P", "KNCUSDT.P", "KOMAUSDT.P", "KSMUSDT.P",
    "LAYERUSDT.P", "LAUSDT.P", "LDOUSDT.P", "LEVERUSDT.P", "LINKUSDT.P", "LISTAUSDT.P", "LPTUSDT.P", "LQTYUSDT.P", "LRCUSDT.P", "LSKUSDT.P", "LTCUSDT.P", "LUNA2USDT.P", "LUMIAUSDT.P",
    "MAGICUSDT.P", "MANAUSDT.P", "MANTAUSDT.P", "MASKUSDT.P", "MAVUSDT.P", "MAVIAUSDT.P", "MBOXUSDT.P", "MELANIAUSDT.P", "MEMEFIUSDT.P", "MEMEUSDT.P", "MERLUSDT.P", "METISUSDT.P", "MEUSDT.P",
    "MEWUSDT.P", "MILKUSDT.P", "MKRUSDT.P", "MLNUSDT.P", "MOCAUSDT.P", "MOODENGUSDT.P", "MORPHOUSDT.P", "MOVRUSDT.P", "MOVEUSDT.P", "MTLUSDT.P", "MUBARAKUSDT.P", "MYROUSDT.P",
    "MYXUSDT.P",
    "NAORISUSDT.P", "NEARUSDT.P", "NEIROETHUSDT.P", "NEIROUSDT.P", "NEOUSDT.P", "NEWTUSDT.P", "NFPUSDT.P", "NILUSDT.P", "NKNUSDT.P", "NMRUSDT.P", "NOTUSDT.P",
    "NTRNUSDT.P",
    "OBOLUSDT.P", "OGNUSDT.P", "OGUSDT.P", "OLUSDT.P", "OMNIUSDT.P", "OMUSDT.P", "ONDOUSDT.P", "ONEUSDT.P", "ONGUSDT.P", "ONTUSDT.P", "OPUSDT.P", "ORCAUSDT.P",
    "ORDIUSDT.P", "OXTUSDT.P",
    "PARTIUSDT.P", "PAXGUSDT.P", "PENDLEUSDT.P", "PENGUUSDT.P", "PEOPLEUSDT.P", "PERPUSDT.P", "PHAUSDT.P", "PHBUSDT.P", "PIPPINUSDT.P", "PIXELUSDT.P",
    "PLAYUSDT.P", "PLUMEUSDT.P", "PNUTUSDT.P", "POLUSDT.P", "POLYXUSDT.P", "PONKEUSDT.P", "POPCATUSDT.P", "PORT3USDT.P", "PORTALUSDT.P", "POWRUSDT.P", "PROMUSDT.P",
    "PROMPTUSDT.P", "PUFFERUSDT.P", "PUMPBTCUSDT.P", "PUMPUSDT.P", "PUNDIXUSDT.P", "PYTHUSDT.P",
    "QNTUSDT.P", "QTUMUSDT.P", "QUICKUSDT.P",
    "RAREUSDT.P", "RAYSOLUSDT.P", "RDNTUSDT.P", "REDUSDT.P", "REIUSDT.P", "RESOLVUSDT.P", "REZUSDT.P", "RIFUSDT.P", "RLCUSDT.P", "RONINUSDT.P", "ROSEUSDT.P", "RPLUSDT.P", "RSRUSDT.P", "RUNEUSDT.P", "RVNUSDT.P",
    "SAFEUSDT.P", "SAGAUSDT.P", "SAHARAUSDT.P", "SANDUSDT.P", "SANTOSUSDT.P", "SCRTUSDT.P", "SCRUSDT.P", "SEIUSDT.P", "SFPUSDT.P", "SHELLUSDT.P", "SIGNUSDT.P", "SIRENUSDT.P",
    "SKATEUSDT.P", "SKLUSDT.P", "SKYAIUSDT.P", "SLERFUSDT.P", "SLPUSDT.P", "SNXUSDT.P", "SOLUSDT.P", "SOLVUSDT.P", "SONICUSDT.P", "SOONUSDT.P", "SOPHUSDT.P", "SPKUSDT.P",
    "SPXUSDT.P", "SQDUSDT.P", "SSVUSDT.P", "STEEMUSDT.P", "STGUSDT.P", "STORJUSDT.P", "STOUSDT.P", "STRKUSDT.P", "STXUSDT.P", "SUIUSDT.P", "SUNUSDT.P", "SUPERUSDT.P",
    "SUSDT.P", "SUSHIUSDT.P", "SWARMSUSDT.P", "SWELLUSDT.P", "SXTUSDT.P", "SXPUSDT.P", "SYNUSDT.P", "SYRUPUSDT.P", "SYSUSDT.P",
    "TAGUSDT.P", "TAIKOUSDT.P", "TANSSIUSDT.P", "TAOUSDT.P", "TAUSDT.P", "TACUSDT.P", "THEUSDT.P", "THETAUSDT.P", "TIAUSDT.P", "TLMUSDT.P", "TNSRUSDT.P", "TOKENUSDT.P", "TONUSDT.P", "TRBUSDT.P", "TREEUSDT.P", "TRUUSDT.P",
    "TRUMPUSDT.P", "TRXUSDT.P", "TSTUSDT.P", "TUSDT.P", "TUTUSDT.P", "TURBOUSDT.P", "TWTUSDT.P",
    "UMAUSDT.P", "UNIUSDT.P", "USDCUSDT.P", "USUALUSDT.P", "USTCUSDT.P", "UXLINKUSDT.P",
    "VANAUSDT.P", "VANRYUSDT.P", "VELODROMEUSDT.P", "VELVETUSDT.P", "VETUSDT.P", "VICUSDT.P", "VINEUSDT.P", "VIRTUALUSDT.P", "VOXELUSDT.P", "VTHOUSDT.P", "VVVUSDT.P",
    "WALUSDT.P", "WAXPUSDT.P", "WCTUSDT.P", "WIFUSDT.P", "WLDUSDT.P", "WOOUSDT.P", "WUSDT.P", "XAIUSDT.P", "XCNUSDT.P", "XLMUSDT.P", "XMRUSDT.P", "XRPUSDT.P", "XVSUSDT.P", "XTZUSDT.P",
    "YFIUSDT.P", "YGGUSDT.P",
    "ZECUSDT.P", "ZENUSDT.P", "ZEREBROUSDT.P", "ZETAUSDT.P", "ZILUSDT.P", "ZKUSDT.P", "ZKJUSDT.P", "ZORAUSDT.P", "ZROUSDT.P", "ZRXUSDT.P", "ZRCUSDT.P"
]

def get_binance_klines(symbol, interval, limit=100):
    """Fetches historical data, supporting both Spot and Futures."""
    is_futures = symbol.upper().endswith('.P')
    api_symbol = symbol.upper().replace('.P', '')
    url = f"https://fapi.binance.com/fapi/v1/klines" if is_futures else f"https://api.binance.com/api/v3/klines"
    
    params = {'symbol': api_symbol, 'interval': interval, 'limit': limit}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'])
        df = df[['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume']]
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col])
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# --- ON-DEMAND /macd command ---
async def macd_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        symbol = context.args[0].upper()
        timeframe = context.args[1].lower()
    except IndexError:
        await update.message.reply_text("<b>Usage:</b> <code>/macd SYMBOL TIMEFRAME</code>\n\n<b>Example:</b> <code>/macd BTCUSDT.P 1d</code>", parse_mode='HTML')
        return

    await update.message.reply_text(f"⏳ Analyzing MACD for {symbol} on the {timeframe} timeframe...")
    df = get_binance_klines(symbol=symbol, interval=timeframe)
    if df is not None and len(df) > 35:
        df.ta.macd(fast=FAST_SETTING, slow=SLOW_SETTING, signal=SIGNAL_SETTING, append=True)
        
        macd_col = f'MACD_{FAST_SETTING}_{SLOW_SETTING}_{SIGNAL_SETTING}'
        hist_col = f'MACDh_{FAST_SETTING}_{SLOW_SETTING}_{SIGNAL_SETTING}'
        signal_col = f'MACDs_{FAST_SETTING}_{SLOW_SETTING}_{SIGNAL_SETTING}'

        current_hist = df[hist_col].iloc[-1]
        previous_hist = df[hist_col].iloc[-2]

        signal_status = "⚪️ Neutral"
        if previous_hist <= 0 and current_hist > 0:
            signal_status = "📈 UP Signal (Bullish Crossover)"
        elif previous_hist >= 0 and current_hist < 0:
            signal_status = "📉 DOWN Signal (Bearish Crossover)"
        elif current_hist > 0:
            signal_status = "👍 Bullish (Histogram is positive)"
        elif current_hist < 0:
            signal_status = "👎 Bearish (Histogram is negative)"
        
        message = (f"<b>MACD Signal for {symbol} ({timeframe})</b>\n\n"
                   f"<b>Settings:</b> fast={FAST_SETTING}, slow={SLOW_SETTING}, signal={SIGNAL_SETTING}\n"
                   f"<b>Status:</b> {signal_status}\n\n"
                   f"<b>MACD Line:</b> <code>{df[macd_col].iloc[-1]:.4f}</code>\n"
                   f"<b>Signal Line:</b> <code>{df[signal_col].iloc[-1]:.4f}</code>\n"
                   f"<b>Histogram:</b> <code>{current_hist:.4f}</code>")
        await update.message.reply_html(message)
    else:
        await update.message.reply_text(f"Sorry, I couldn't get enough data for {symbol}.")

# --- AUTOMATED hourly report function ---
async def hourly_report(context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Running hourly MACD check...")
    bullish_signals, bearish_signals = [], []
    chat_id = context.job.chat_id
    hist_col = f'MACDh_{FAST_SETTING}_{SLOW_SETTING}_{SIGNAL_SETTING}'

    for symbol in SYMBOLS_TO_WATCH:
        df = get_binance_klines(symbol, interval='1h')
        if df is not None and len(df) > 35:
            df.ta.macd(fast=FAST_SETTING, slow=SLOW_SETTING, signal=SIGNAL_SETTING, append=True)
            
            current_hist = df[hist_col].iloc[-2]
            previous_hist = df[hist_col].iloc[-3]
            
            if previous_hist <= 0 and current_hist > 0:
                bullish_signals.append(symbol.replace('.P', ''))
            elif previous_hist >= 0 and current_hist < 0:
                bearish_signals.append(symbol.replace('.P', ''))
        else:
            print(f"Could not get enough data for {symbol} on 1h timeframe. Skipping.")
        await asyncio.sleep(0.5) 

    if not bullish_signals and not bearish_signals:
        print("No hourly MACD crossovers found in the last hour.")
        return

    message = f"<b> Hourly MACD Crossover Report ({FAST_SETTING},{SLOW_SETTING},{SIGNAL_SETTING}) </b>\n\n"
    if bullish_signals:
        message += "<b>✅ Bullish Crossovers (UP):</b>\n<code>" + ", ".join(bullish_signals) + "</code>\n\n"
    if bearish_signals:
        message += "<b>❌ Bearish Crossovers (DOWN):</b>\n<code>" + ", ".join(bearish_signals) + "</code>\n\n"
    message += "<pre>Checked on 1H Timeframe.</pre>"
    
    await context.bot.send_message(chat_id, text=message, parse_mode='HTML')
    print("Hourly report sent to Telegram.")


# --- AUTOMATED daily report function ---
async def daily_report(context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Running daily MACD check...")
    bullish_signals, bearish_signals = [], []
    chat_id = context.job.chat_id
    hist_col = f'MACDh_{FAST_SETTING}_{SLOW_SETTING}_{SIGNAL_SETTING}'

    for symbol in SYMBOLS_TO_WATCH:
        df = get_binance_klines(symbol, interval='1d')
        if df is not None and len(df) > 35:
            df.ta.macd(fast=FAST_SETTING, slow=SLOW_SETTING, signal=SIGNAL_SETTING, append=True)

            current_hist = df[hist_col].iloc[-2]
            previous_hist = df[hist_col].iloc[-3]

            if previous_hist <= 0 and current_hist > 0:
                bullish_signals.append(symbol.replace('.P', ''))
            elif previous_hist >= 0 and current_hist < 0:
                bearish_signals.append(symbol.replace('.P', ''))
        else:
            print(f"Could not get enough data for {symbol}. Skipping.")
        await asyncio.sleep(0.5)

    if not bullish_signals and not bearish_signals:
        print("No daily MACD crossovers found.")
        await context.bot.send_message(chat_id, text=f"No new daily MACD crossovers found today with settings {FAST_SETTING},{SLOW_SETTING},{SIGNAL_SETTING}.")
        return

    message = f"<b> Daily MACD Crossover Report ({FAST_SETTING},{SLOW_SETTING},{SIGNAL_SETTING}) </b>\n\n"
    if bullish_signals:
        message += "<b>✅ Bullish Crossovers (UP):</b>\n<code>" + ", ".join(bullish_signals) + "</code>\n\n"
    if bearish_signals:
        message += "<b>❌ Bearish Crossovers (DOWN):</b>\n<code>" + ", ".join(bearish_signals) + "</code>\n\n"
    message += "<pre>Checked on Daily Timeframe.</pre>"
    
    await context.bot.send_message(chat_id, text=message, parse_mode='HTML')
    print("Daily report sent to Telegram.")

# --- Bot Setup ---
def main() -> None:
    if not BOT_TOKEN or not CHAT_ID:
        print("🔴 ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
        return

    print(f"Bot is starting with custom MACD settings (Fast: {FAST_SETTING}, Slow: {SLOW_SETTING}, Signal: {SIGNAL_SETTING})...")
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("macd", macd_command))

    job_queue = application.job_queue
    
    job_queue.run_repeating(hourly_report, interval=3600, first=10, chat_id=CHAT_ID)
    
    colombo_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    job_queue.run_daily(daily_report, time=datetime.time(hour=5, minute=35, tzinfo=colombo_tz), chat_id=CHAT_ID)
    
    print("Bot is polling for commands.")
    print("Hourly job is scheduled to run every hour.")
    print("Daily job is scheduled for 05:35 Colombo time.")
    
    application.run_polling()

if __name__ == "__main__":
    main()
