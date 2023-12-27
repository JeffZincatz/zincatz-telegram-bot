import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from request import Request
from scrape_bs import Scraper

# Load environment variables
import dotenv

# Keep alive for deployment
# from keep_alive import keep_alive

# keep_alive()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

req = Request()
scraper = Scraper()


'''
Messages
'''
def get_start_message():
  return f"Zincatz's M.League Infoboard\nKindly wait a few seconds for responses."

def get_help_message():
  return "\n".join([
      "Available commands:",
      "/start - Display start menu"
  ])

def get_opponent_message():
  return '\n'.join(scraper.get_match_info())

def get_regular_team_rank_message():
  return '\n'.join(scraper.get_regualr_team_rank())

def get_personal_score_message():
  return '\n'.join(scraper.get_personal_score())

def get_personal_highest_message():
  return '\n'.join(scraper.get_personal_highest())

def get_last_avoid_rate_message():
  return '\n'.join(scraper.get_last_avoid_rate())


'''
Keyboard
'''
def menu_keyboard():
  keyboard = [
    [InlineKeyboardButton('Start', callback_data='start'),
     InlineKeyboardButton('Help', callback_data='help')],
    [InlineKeyboardButton('Upcoming Opponents', callback_data='opponent')],
    [InlineKeyboardButton('Team Ranking (regular season)', callback_data='regular')],
    [InlineKeyboardButton('Personal Score Ranking', callback_data='personal_score')],
    [InlineKeyboardButton('Personal Highest Ranking', callback_data='personal_highest')],
    [InlineKeyboardButton('Last Avoid Rate Ranking', callback_data='last_avoid_rate')]
    ]
  return InlineKeyboardMarkup(keyboard)


'''
Command handlers
'''
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(get_start_message(), reply_markup=menu_keyboard())


'''
Callback query handlers for menu
'''
async def help_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  
  await query.answer()
  try:
    await query.edit_message_text(text=get_help_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")


async def start_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  
  await query.answer()
  try:
    await query.edit_message_text(text=get_start_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")

async def opponent_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  try:
    await query.edit_message_text(text=get_opponent_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")

async def regular_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  try:
    await query.edit_message_text(text=get_regular_team_rank_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")
  
async def personal_score_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  try:
    await query.edit_message_text(text=get_personal_score_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")

async def personal_highest_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  try:
    await query.edit_message_text(text=get_personal_highest_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")

async def last_avoid_rate_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  try:
    await query.edit_message_text(text=get_last_avoid_rate_message(), reply_markup=menu_keyboard())
  except error.BadRequest as e:
    logging.info(f"{e}")


if __name__ == '__main__':
  dotenv.load_dotenv("./.env")
  TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
  
  application = ApplicationBuilder().token(TOKEN).build()
  
  application.add_handler(CommandHandler('start', callback=start_handler))
  application.add_handler(CallbackQueryHandler(help_menu_handler, pattern='help'))
  application.add_handler(CallbackQueryHandler(start_menu_handler, pattern='start'))
  application.add_handler(CallbackQueryHandler(opponent_menu_handler, pattern='opponent'))
  application.add_handler(CallbackQueryHandler(regular_menu_handler, pattern='regular'))
  application.add_handler(CallbackQueryHandler(personal_score_menu_handler, pattern='personal_score'))
  application.add_handler(CallbackQueryHandler(personal_highest_menu_handler, pattern='personal_highest'))
  application.add_handler(CallbackQueryHandler(last_avoid_rate_menu_handler, pattern='last_avoid_rate'))
  
  application.run_polling()
  
