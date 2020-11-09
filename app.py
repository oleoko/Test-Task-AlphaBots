from config import API_TOKEN, WEBHOOK_HOST, WEBHOOK_URL_PATH
from aiogram import Bot, Dispatcher, types
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import urljoin
from aiogram.utils.executor import start_webhook
import os


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)


def getscreen(url):
    # Set options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')

    # Initialize webdriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)

    # Get screenshot
    widht = 1920
    height = 1080
    driver.set_window_size(widht, height)
    time.sleep(2)
    driver.save_screenshot('screenshot.png')
    driver.quit()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hello! \nIt is test task for Alpha bots")


@dp.message_handler(regexp='.')
async def send_welcome(message: types.Message):
    try:
        getscreen(f'https://{message.text}')
        print(message.text)
        with open('screenshot.png', 'rb') as photo:
            await message.answer_photo(photo)
    except:
        await message.answer('Invalid url')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_URL_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host='0.0.0.0', port=os.getenv('PORT'))
