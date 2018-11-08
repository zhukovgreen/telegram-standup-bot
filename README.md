# Telegram Standup Bot
**!!! Pls note: the bot is in experimental condition !!!**

Bot address:
[@standup_tbe_remak_bot](https://telegram.me/standup_tbe_remak_bot)

Support group:
https://t.me/joinchat/EiE7ykcEzD3-3DfvxzdSow

It is inspired by a `geekbot` which exists only for
slack.

The bot has basic functionality:
- Add to standup group
- When a new member joins the group the bot sends an 
invitation to join the standup
- After that upon running `/report` command
the bot starts the standup by asking questions
- After the answer to the last question the bot
publishes the report to the standup channel
- Each 24 h the bot sends a reminder to submit the report.
- Reminders could be turned on/of via `/settings` command

# List of commands
1. `/help` - Get a help
1. `/start` - Start a bot
1. `/add_me` - Add a user to the standup (Only for standup group)
1. `/remove_me` - Remove a user from the standup (Only for standup group)
1. `/settings` - Bot settings
1. `/report` - Submit a report
1. `/stop_report` - Stop report right now


# Deployment
If you want to deploy own version of the bot
then:

1. Create your bot at [@BotFather](https://telegram.me/BotFather)
1. `git clone https://github.com/ZhukovGreen/telegram-standup-bot.git`
1. Create `.env` file with:
    * BOT_TOKEN="your bot token"
    * LOGGING_LEVEL="INFO"
    
1. `docker-compose -f docker-compose.deploy.yml build`
1. `docker swarm init`
1. `docker stack deploy -c docker-compose.deploy.yml
standup-bot`
