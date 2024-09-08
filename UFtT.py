import feedparser
import time
import telegram
from apscheduler.schedulers.blocking import BlockingScheduler

TELEGRAM_BOT_TOKEN = 'bot_token'
TELEGRAM_CHANNEL_ID = '@channel_id'

RSS_FEED_URL = 'https://forum.ubuntu-ir.org/index.php?action=.xml;type=rss'

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

sent_posts = set()

def check_feed():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        post_title = entry.title
        post_link = entry.link
        post_content = entry.description

        message = f'<a href="{post_link}">{post_title}</a>\n\n{post_content}'

        if post_link not in sent_posts:
            bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode=telegram.ParseMode.HTML)
            sent_posts.add(post_link)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(check_feed, 'interval', minutes=10)
    scheduler.start()
