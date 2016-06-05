import discord
from discord.ext import commands
from random import choice as rndchoice
from .utils.dataIO import fileIO
from .utils import checks
import os

defaults = [
    "an Ice Shard",
    "a USB Flash Drive",
    "a Ruler",
    "a Loaf Of Bread",
    "my 2048-bit biomechanical lifeform sensor arrays",
    "an Elite Task Force",
    "an Open-Source program",
    "a Wakizashi",
    "an Exodia Summon",
    "a Tantou"]

class poke:
    """poke command."""

    def __init__(self, bot):
        self.bot = bot
        self.items = fileIO("data/poke/items.json", "load")

    def save_items(self):
        fileIO("data/poke/items.json", 'save', self.items)

    @commands.group(pass_context=True, invoke_without_command=True)
    async def poke(self, ctx, *, user : discord.Member=None):
        """poke a user"""
        if ctx.invoked_subcommand is None:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                await self.bot.say("Dont make me poke you instead " + user.name)
                return
            await self.bot.say("-pokes " + user.name + " with " +
                               (rndchoice(self.items) + "-"))

    @poke.command()
    async def add(self, item):
        """Adds an item"""
        if item in self.items:
          await self.bot.say("That is already an item.")
        else:
          self.items.append(item)
          self.save_items()
          await self.bot.say("Item added.")

    @poke.command()
    @checks.is_owner()
    async def remove(self, item):
        """Removes item"""
        if item not in self.items:
          await self.bot.say("That is not an item")
        else:
            self.items.remove(item)
            self.save_items()
            await self.bot.say("item removed.")

def check_folders():
    if not os.path.exists("data/poke"):
        print("Creating data/poke folder...")
        os.makedirs("data/poke")

def check_files():
    f = "data/poke/items.json"
    if not fileIO(f, "check"):
        print("Creating empty items.json...")
        fileIO(f, "save", defaults)

def setup(bot):
    check_folders()
    check_files()
    n = poke(bot)
    bot.add_cog(n)