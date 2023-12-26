import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
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

req = Request()
scraper = Scraper()


'''
Messages
'''
def get_start_message():
  return "Zincatz's M.League Infoboard\nKindly wait a few seconds for responses."

def get_help_message():
  return "\n".join([
      "Available commands:",
      "/help - Display this help message",
      "/start - Return to start menu"
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
Command handlers
'''
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(get_start_message(), reply_markup=await menu_keyboard())


'''
Callback query handler for menu
'''
def get_menu_callback_query_handler(message:str):
  async def menu_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=message, reply_markup=await menu_keyboard())
  return menu_handler

def start_menu():
  message = get_start_message()
  return get_menu_callback_query_handler(message)

def help_menu():
  message = get_help_message()
  return get_menu_callback_query_handler(message)

def opponent_menu():
  message = get_opponent_message()
  return get_menu_callback_query_handler(message)

def regular_menu():
  message = get_regular_team_rank_message()
  return get_menu_callback_query_handler(message)

def personal_score_menu():
  message = get_personal_score_message()
  return get_menu_callback_query_handler(message)

def personal_highest_menu():
  message = get_personal_highest_message()
  return get_menu_callback_query_handler(message)

def last_avoid_rate_menu():
  message = get_last_avoid_rate_message()
  return get_menu_callback_query_handler(message)


'''
Keyboard
'''
async def menu_keyboard():
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


def add_command_handler(application:Application, handle_name: str, handler):
  application.add_handler(CommandHandler(handle_name, handler))


if __name__ == '__main__':
  dotenv.load_dotenv("./.env")
  TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
  
  application = ApplicationBuilder().token(TOKEN).build()
  
  application.add_handler(CommandHandler('start', menu_handler))
  application.add_handler(CallbackQueryHandler(help_menu(), pattern='help'))
  application.add_handler(CallbackQueryHandler(start_menu(), pattern='start'))
  application.add_handler(CallbackQueryHandler(opponent_menu(), pattern='opponent'))
  application.add_handler(CallbackQueryHandler(regular_menu(), pattern='regular'))
  application.add_handler(CallbackQueryHandler(personal_score_menu(), pattern='personal_score'))
  application.add_handler(CallbackQueryHandler(personal_highest_menu(), pattern='personal_highest'))
  application.add_handler(CallbackQueryHandler(last_avoid_rate_menu(), pattern='last_avoid_rate'))

  application.run_polling()
  
