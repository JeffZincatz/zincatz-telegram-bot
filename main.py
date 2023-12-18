import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from request import get_match_info, get_regualr_team_rank, get_personal_score

# Load environment variables
import dotenv

# Keep alive for deployment
# from keep_alive import keep_alive

# keep_alive()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text=
      "Welcome to the Zincatz's M.League info Bot!\nt.me/zincatz_bot\nUse /help to view all available commands."
  )


async def opponent(update: Update, context: ContextTypes.DEFAULT_TYPE):
  match_info = get_match_info()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(match_info))


async def team_ranking_regular(update: Update, context: ContextTypes.DEFAULT_TYPE):
  team_ranking = get_regualr_team_rank()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(team_ranking))

async def personal_score_regular(update: Update, context: ContextTypes.DEFAULT_TYPE):
  personal_score = get_personal_score()
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\n".join(personal_score))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  help_message = "\n".join(
    [
      "Available commands:",
      "/help - Display this help message",
      "/opponent - Display the latest opponent information",
      "/regular - Display the latest regular season team ranking",
      "/personal_score - Display personal score ranking"
      ]
    )

  # Send the help message to the user
  await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=help_message)


def add_command_handler(handle_name: str, handler):
  application.add_handler(CommandHandler(handle_name, handler))


if __name__ == '__main__':
  dotenv.load_dotenv("./.env")
  TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
  
  application = ApplicationBuilder().token(TOKEN).build()

  add_command_handler('start', start)
  add_command_handler('help', help)
  add_command_handler('opponent', opponent)
  add_command_handler('regular', team_ranking_regular)
  add_command_handler('personal_score', personal_score_regular)

  application.run_polling()
  
