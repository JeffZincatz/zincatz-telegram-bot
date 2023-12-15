import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from request import get_match_info

# Load environment variables
import dotenv

dotenv.load_dotenv("./env")

# Keep alive for deployment
# from keep_alive import keep_alive

# keep_alive()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=
      "Welcome to the Zincatz's M.League opponent info Bot!\nt.me/zincatz_bot\nUse /help to view all available commands."
  )


async def mleague(update: Update, context: ContextTypes.DEFAULT_TYPE):
  match_info = get_match_info()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(match_info))


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  help_message = "Available commands:\n" +\
      "/help - Display this help message\n"+\
      "/mleague - Display the latest M.League opponent information"

  # Send the help message to the user
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=help_message)


def add_command_handler(handle_name: str, handler):
  application.add_handler(CommandHandler(handle_name, handler))


if __name__ == '__main__':
  application = ApplicationBuilder().token(TOKEN).build()

  add_command_handler('start', start)
  add_command_handler('help', help)
  add_command_handler('mleague', mleague)

  application.run_polling()
