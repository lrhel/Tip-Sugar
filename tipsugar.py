#!/usr/bin/env python3

import traceback

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import config
import utility
import user_db

COMMANDS = [
    'info',
    'help',
    'balance',
    'deposit',
    'tip',
    'withdraw',
    'withdrawall'
]

class TipSugar(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        for cog in COMMANDS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("Successful login.") # notify login completion on terminal
        print("Name: " + str(self.user.name))
        print("ID: " + str(self.user.id))
        print("----------------------")

        await self.change_presence(activity=discord.Game(name=f'{config.prefix}help') if not config.status else config.status) # change game playing

if __name__ == "__main__":
    user_db.db_init()

    bot = TipSugar(command_prefix=utility.prefix)
    bot.run(config.token)

    @bot.check
    def add_to_db():
        if not user_db.check_user(user_id):
            user_db.add_user(user_id, user_name)
        return True
