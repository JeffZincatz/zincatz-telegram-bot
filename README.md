# M.League Opponent Information Bot

## About
A simple telegram bot here at [M.League Opponent Info Bot](https://t.me/zincatz_bot) that allows you to get information about M.League's daily opponent information. Built for fun and personal use only.

## Built With
- Python
  - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
  - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Development

Developed locally and can be hosted locally in terminal or Docker.

Currently deployed using school server (lol). Previous deployment using Replit and UptimeRobot seized functioning.

Telegram bot token needs to be set up in environment configuration.

## Roadmap
- Initally planned to utilize Twitter's Developer API. However, since Twitter updated its terms of service, it is no longer free to use for such purposes.
- All game opponent information is requested from the official [M.League website](https://m-league.jp/).
- Barebone functionality of retrieving the upcoming game opponent information is implemented.
- Added regular season team ranking.
- Added regular season personal rankings.
- Some optimisation to cache page data for 1 minute (this duration is adjustable).
- Use [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) for more robust scraping.
- Build button keyboards instead of pure commands to reduce spamming.
  - Side note, abstracting callback handlers affected message text updates, thus was not implemented (werid...).
- Potential features:
  - Personal & team statistics
    - [Stats Overview](https://m-league.jp/stats)
    - [Team Points](https://m-league.jp/points)
  - Schedule to run requesting opponent cards on game days repeatedly.
    - Users can subscribe/unsubscribe opponent card updates by using commands/buttons.
    - On every Monday, Tuesday, Thursday, Friday, in game season period (the dates might have to be hard-coded), start requesting cards from, say 14:00 (GMT +8) every, say 5mins, until opponent cards are updated, or until 18:00 (which means the day should have no game for reasons such as holidays).
    - If an updated non-empty opponent card is found, send a notification to all subscribed users by id.
    - The list of subscribed user ids must become **persistent**, meaning that some form of persitent database is required.
    
- Currently I don't see the point to respond with icons and images. Reducing payload is prefereable since it is just utilizing free service.
- No plan to use any paid hosting services, since this is just a hobby project.