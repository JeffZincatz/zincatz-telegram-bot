# M.League Opponent Information Bot

## About
A simple telegram bot here at [M.League Opponent Info Bot](https://t.me/zincatz_bot) that allows you to get information about M.League's daily opponent information. Built for fun and personal use only.

## Built With
- Python
  - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Development

Developed locally and can be hosted on local machine.

Currently deployed on free tier Replit and kept running alive with UptimeRobot.

Replit manages Telegram Bot API key using its Secret Environment Variable. Locally, environment variable configuration is needed using python-dotenv.

## Roadmap
- Initally planned to utilize Twitter's Developer API. However, since Twitter updated its terms of service, it is no longer free to use for such purposes.
- All game opponent information is requested from the official [M.League website](https://m-league.jp/).
- Barebone functionality of retrieving the upcoming game opponent information is implemented.
- There is no plan to add any new features.
- Potential new features include adding current team ranking scoreboards, individual ranking scoreboards etc.
- Currently I don't see the point to use images in bot resposnes. Not sending images can reduce payload since it is just utilizing free service.
- No plan to upgrade to any paid hosting services, since this is just a hobby project.