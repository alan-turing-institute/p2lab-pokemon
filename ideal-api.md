# Ideal API

This is a document that describes the ideal API for working with teams, setting
up showdown bots that run using a specified configuration, and running genetic
algorithms to optimize teams.

```python3

team = generate_team(format='gen8randombattle', seed=1234)

# a team object contains a list of 6 pokemon objects with their moves, items, etc.
# it's also tracking the (normalised) number of wins/losses/ties for this team.
# (would be nice to hard-code an auto-tie at 100 moves or something, but that's not a priority)

# here's an example env file for running a showdown bot:
# BATTLE_BOT=safest
# WEBSOCKET_URI=sim.psim.us:8000
# PS_USERNAME=whimsicaldreams
# PS_PASSWORD=password
# BOT_MODE=CHALLENGE_USER
# POKEMON_MODE=gen3ou
# RUN_COUNT=1
# USER_TO_CHALLENGE=...
# SAVE_REPLAY=False
# TEAM_NAME=gen3/my_teams


# here's an idealised Bot class that uses these same env variables to run a showdown bot, but more cleanly:
bot_1 = Bot(
    team,
    strategy='safest',
    websocket_uri='sim.psim.us:8000',
    user='whimsicaldreams',
    password='password',
    bot_mode='CHALLENGE_USER',
    format='gen3ou',
    num_battles=1,
    save_replay=False,
)

# this will require hacking the bot code to remove dependence from environment variables, but it's doable
# note the absence of the user to challenge -- this is so we can be flexible about which bots are fighting at any given time (needs coding)
# the bot class will also need to be able to run a battle and return the results

# now we can run a battle between two bots:
bot_2 = Bot(
    team,
    strategy='safest',
    websocket_uri='sim.psim.us:8000',
    user='melonchomper',
    password='password',
    bot_mode='CHALLENGE_USER',
    format='gen3ou',
    num_battles=1,
    save_replay=False,
)

run_battle(bot_1, bot_2)

# within this function, we'll need to:
# - run the bot_1 and bot_2 showdown bots
# - parse the results of the battle
# - update the win/loss/tie counts for each team

# here's a more generic example, where we specify a number of battles for each team, and then run them all:
bots = {f'bot{i}':Bot(team, strategy='safest', websocket_uri='sim.psim.us:8000', user=f'bot{i}', password='password', bot_mode='CHALLENGE_USER', format='gen3ou', num_battles=10, save_replay=False) for i in range(10)}

# now we can run all of these battles in parallel using a while loop that ensures every bot has fought every other bot:
while not all([bot.remaining_battles == 0 for bot in bots.values()]):
    for bot_1 in bots:
        for bot_2 in bots:
            if bot_1 != bot_2 and bot_1.remaining_battles > 0 and bot_2.remaining_battles > 0:
                try:
                    run_battle(bot_1, bot_2)
                    bot_1.remaining_battles -= 1
                    bot_2.remaining_battles -= 1
                except Exception as e:
                    print(e)
                    print(f'Error running battle between {bot_1} and {bot_2}')

# now we can print out the results of each bot:
for bot in bots:
    print(bot.user, bot.team.wins, bot.team.losses, bot.team.ties)
```
