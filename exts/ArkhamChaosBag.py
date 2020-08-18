# ArkhamChaosBag extension for Discord
### PREAMBLE ##################################################################
import copy
import re

import discord
import requests
import random
from discord.ext import commands
from unidecode import unidecode

class ArkhamChaosBag(commands.Cog):
    """Arkham Horror related commands"""

    def __init__(self, bot):
        self.bot = bot
        self.ChaosBag = []
        self.init_api = False
        
    def numbers_to_strings(self,argument):
        switcher = {
            0: "+1",
            1: "0",
            2: "-1",
            3: "-2",
            4: "-3",
            5: "-4",
            6: "-5",
            7: "-6",
            8: "-7",
            9: "-8",
            10: "Skull",
            11: "Cultist",
            12: "Broken tablet",
            13: "Monster",
            14: "Auto-fail",
            15: "Elder sign",
           }
        return switcher.get(argument, "nothing")
    
    def numbers_to_imgurl(self,argument):
        switcher = {
            0: "http://chaos.chrisputnam.info/assets/tokens/plus1.png",
            1: "http://chaos.chrisputnam.info/assets/tokens/zero.png",
            2: "http://chaos.chrisputnam.info/assets/tokens/minus1.png",
            3: "http://chaos.chrisputnam.info/assets/tokens/minus2.png",
            4: "http://chaos.chrisputnam.info/assets/tokens/minus3.png",
            5: "http://chaos.chrisputnam.info/assets/tokens/minus4.png",
            6: "http://chaos.chrisputnam.info/assets/tokens/minus5.png",
            7: "http://chaos.chrisputnam.info/assets/tokens/minus6.png",
            8: "http://chaos.chrisputnam.info/assets/tokens/minus7.png",
            9: "http://chaos.chrisputnam.info/assets/tokens/minus8.png",
            10: "http://chaos.chrisputnam.info/assets/tokens/skull.png",
            11: "http://chaos.chrisputnam.info/assets/tokens/cultist.png",
            12: "http://chaos.chrisputnam.info/assets/tokens/gravestone.png",
            13: "http://chaos.chrisputnam.info/assets/tokens/elderone.png",
            14: "http://chaos.chrisputnam.info/assets/tokens/terror.png",
            15: "http://chaos.chrisputnam.info/assets/tokens/eldersign.png",
           }
        return switcher.get(argument, "nothing")

    @commands.command(aliases=['chaosbaghelp'])
    async def cbhelp(self, ctx):
        m_response = "Hi! I'm your discord's Chaos bag bot. Here's what I can do:\n"
        m_response += "!cbsetup [X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X] - +1,0,-1,-2,-3,-4,-5,-6,-7,-8, Skull, Cultist, Tablet, Monster, Auto-fail, Eldersign \n"
        m_response += "!cbpull - pulls a token from the bag \n"
        await ctx.send(m_response[:2000])

    @commands.command(aliases=['chaosbagsetup'], pass_context=True)
    async def cbsetup(self, ctx):
        """Setup chaos bag"""
        m_response = ""
        TempChaosBag = [{}]
        pos = 0
        chaostoken = 0
        self.ChaosBag.clear()
        #channelid = ctx.message.channel.id
        rawcontents = ' '.join(ctx.message.content.split()[1:])
        TempChaosBag = rawcontents.split(",")
        for amount in TempChaosBag:
            i = 0
            while i < int(amount):
                self.ChaosBag.append(chaostoken)
                i += 1
            chaostoken = chaostoken + 1
        m_response = "the Chaos bag currently contains: \n"
        for t in self.ChaosBag:
            m_response += self.numbers_to_strings(t) + ", "
        #m_response += "Channel Id = " + str(channelid)
        await ctx.send(m_response[:2000])

    @commands.command(aliases=['chaosbagadd'], pass_context=True)
    async def cbadd(self, ctx):
        """add token to chaos bag"""
        m_response = ""
        chaostoken = ' '.join(ctx.message.content.split()[1:])
        if int(chaostoken) >= 0 and int(chaostoken) <= 15:
            self.ChaosBag.append(int(chaostoken))
            m_response = self.numbers_to_strings(int(chaostoken)) + " added \n"
        else:
            m_response = "Must be a value between 0-15 \n"
        await ctx.send(m_response[:2000])

    @commands.command(aliases=['chaosbagremoove', 'cbremove'], pass_context=True)
    async def cbrem(self, ctx):
        """remove token from chaos bag"""
        m_response = ""
        chaostoken = ' '.join(ctx.message.content.split()[1:])
        if int(chaostoken) >= 0 and int(chaostoken) <= 15:
            try:
                self.ChaosBag.remove(int(chaostoken))
                m_response = self.numbers_to_strings(int(chaostoken)) + " removed \n"
            except ValueError:
                m_response = "No matching tokens in the bag \n"    
        else:
            m_response = "Must be a value between 0-15 \n"
        await ctx.send(m_response[:2000])

    @commands.command(aliases=['chaosbagpull', 'cb'])
    async def cbpull(self, ctx):
        """Pull a token from chaos bag"""
        #m_response = self.numbers_to_imgurl(random.choice(self.ChaosBag))
        #await ctx.send(m_response[:2000])
        e = discord.Embed()
        e.set_image(url=self.numbers_to_imgurl(random.choice(self.ChaosBag)))
        await ctx.send(embed=e)

    @commands.command(aliases=['chaosbaglist'])
    async def cblist(self, ctx):
        """List tokens in the chaos bag"""
        m_response = "the Chaos bag currently contains: \n"
        for t in self.ChaosBag:
            m_response += self.numbers_to_strings(t) + ", "
        await ctx.send(m_response[:2000])

def setup(bot):
    bot.add_cog(ArkhamChaosBag(bot))