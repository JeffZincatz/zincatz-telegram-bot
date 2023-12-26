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
Handlers
'''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=
      "Welcome to the Zincatz's M.League info Bot!\nt.me/zincatz_bot\nUse /help to view all available commands."
  )


async def opponent(update: Update, context: ContextTypes.DEFAULT_TYPE):
  match_info = scraper.get_match_info()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(match_info))


async def team_ranking_regular(update: Update, context: ContextTypes.DEFAULT_TYPE):
  team_ranking = scraper.get_regualr_team_rank()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(team_ranking))

async def personal_score_regular(update: Update, context: ContextTypes.DEFAULT_TYPE):
  personal_score = scraper.get_personal_score()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(personal_score))

async def personal_highest_regular(update: Update, context: ContextTypes.DEFAULT_TYPE):
  personal_highest = scraper.get_personal_highest()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(personal_highest))

async def last_avoid_rate_regular(update: Update, context: ContextTypes.DEFAULT_TYPE):
  last_avoid_rate = scraper.get_last_avoid_rate()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(last_avoid_rate))

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Zincatz's M.League Infoboard", reply_markup=await menu_keyboard())

def menu_handler_builder(message:str):
  async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(message, reply_markup=await menu_keyboard())
  return menu_handler

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  help_message = "\n".join([
      "Available commands:", "/help - Display this help message",
      "/opponent - Display the latest opponent information",
      "/regular - Display the latest regular season team ranking",
      "/personal_score - Display personal score ranking",
      "/personal_highest - Display personal highest ranking",
      "/last_avoid_rate - Display the last avoid rate ranking"
  ])

  # Send the help message to the user
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=help_message)

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message = "\n".join([
      "Available commands:", "/help - Display this help message",
      "/opponent - Display the latest opponent information",
      "/regular - Display the latest regular season team ranking",
      "/personal_score - Display personal score ranking",
      "/personal_highest - Display personal highest ranking",
      "/last_avoid_rate - Display the last avoid rate ranking"
  ])
  
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(text=message, reply_markup=await menu_keyboard())

async def default_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message = "Zincatz's M.League Infoboard"
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(text=message, reply_markup=await menu_keyboard())

'''
Keyboards
'''
async def menu_keyboard():
  keyboard = [
    [InlineKeyboardButton('Help', callback_data='help'),
     InlineKeyboardButton('Menu', callback_data='menu')],
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

  add_command_handler(application, 'start', start)
  add_command_handler(application, 'help', help)
  add_command_handler(application, 'opponent', opponent)
  add_command_handler(application, 'regular', team_ranking_regular)
  add_command_handler(application, 'personal_score', personal_score_regular)
  add_command_handler(application, 'personal_highest', personal_highest_regular)
  add_command_handler(application, 'last_avoid_rate', last_avoid_rate_regular)
  
  add_command_handler(application, 'menu', menu_handler)
  application.add_handler(CallbackQueryHandler(help_menu, pattern='help'))
  application.add_handler(CallbackQueryHandler(default_menu, pattern='menu'))

  application.run_polling()
  
