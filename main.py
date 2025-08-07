import requests
from bs4 import BeautifulSoup
import telebot
import time
from threading import Thread
from flask import Flask

# === CONFIG ===
BOT_TOKEN = "8255450631:AAEiziguyTTTkhUizga7lCP5k2klhLo-trs"
CHAT_ID = "6822525029"
bot = telebot.TeleBot(BOT_TOKEN)
headers = {"User-Agent": "Mozilla/5.0"}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def send_deal(title, price, link, site):
    msg = f"🔥 {site} Deal\n\n🛍️ {title}\n💰 {price}\n🔗 {link}"
    bot.send_message(CHAT_ID, msg)

def get_amazon_deals():
    url = "https://www.amazon.in/gp/goldbox"
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        deals = soup.select('.DealContent')[:5]
        for deal in deals:
            title = deal.select_one('.DealTitle').get_text(strip=True)
            price_tag = deal.select_one('.a-price .a-offscreen')
            link_tag = deal.find('a', href=True)
            if title and price_tag and link_tag:
                price = price_tag.get_text(strip=True)
                deal_link = "https://www.amazon.in" + link_tag['href']
                send_deal(title, price, deal_link, "Amazon")
    except Exception as e:
        print(f"Amazon error: {e}")

def get_flipkart_deals():
    url = "https://www.flipkart.com/offers-store"
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        deals = soup.select('a._1en9oG')[:5]
        for deal in deals:
            title = deal.get('title')
            deal_link = "https://www.flipkart.com" + deal.get('href')
            price = "Check on site"
            if title and deal_link:
                send_deal(title, price, deal_link, "Flipkart")
    except Exception as e:
        print(f"Flipkart error: {e}")

def bot_loop():
    while True:
        print("Checking deals...")
        get_amazon_deals()
        get_flipkart_deals()
        time.sleep(1800)  # 30 mins

def start_bot():
    Thread(target=bot_loop).start()

if __name__ == "__main__":
    start_bot()
    app.run(host="0.0.0.0", port=8000)
