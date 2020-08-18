# ArkhamPlayer extension for Discord
### PREAMBLE ##################################################################
import copy
import re

import discord
import requests
import random
from discord.ext import commands
from unidecode import unidecode

class ArkhamPlayer(commands.Cog):
    """Arkham Horror Player handler"""

    def __init__(self, bot):
        self.bot = bot
        ah_api = []
        self.Player1 = []
        self.Player2 = []
        self.Player3 = []
        self.Player4 = []
        self.init_api = False
        
    def numbers_to_strings(self,argument):
        switcher = {
            0: "Investigator",
            1: "Health",
            2: "Sanity",
            3: "IMG URL",
           }
        return switcher.get(argument, "nothing")
    
    def refresh_ah_api(self):
        self.ah_api = sorted([c for c in requests.get('https://arkhamdb.com/api/public/cards?encounter=1').json()],
                             key=lambda card: card['name'])

        # only player cards
        self.ah_api_p = [c for c in self.ah_api if "spoiler" not in c]
        self.init_api = True

    @commands.command(aliases=['arkhamplayerhelp'])
    async def aphelp(self, ctx):
        m_response = "Hi! I'm your discord's arkham player bot. Here's what I can do:\n"
        m_response += "!apadd1 [Investigator] - Add player 1 investigator \n"
        m_response += "!apadd2 [Investigator] - Add player 2 investigator \n"
        m_response += "!apadd3 [Investigator] - Add player 3 investigator \n"
        m_response += "!apadd4 [Investigator] - Add player 4 investigator \n"
        m_response += "!aph1 [Number] - Add/Remove health from investigator 1 \n"
        m_response += "!aph2 [Number] - Add/Remove health from investigator 2 \n"
        m_response += "!aph3 [Number] - Add/Remove health from investigator 3 \n"
        m_response += "!aph4 [Number] - Add/Remove health from investigator 4 \n"
        m_response += "!aps1 [Number] - Add/Remove sanity from investigator 1 \n"
        m_response += "!aps2 [Number] - Add/Remove sanity from investigator 2 \n"
        m_response += "!aps3 [Number] - Add/Remove sanity from investigator 3 \n"
        m_response += "!aps4 [Number] - Add/Remove sanity from investigator 4 \n"
        await ctx.send(m_response[:2000])

    ## PLAYER 1 ##
    @commands.command(aliases=['addplayer1'], pass_context=True)
    async def apadd1(self, ctx):
        """Add player 1"""
        subexists = False
        # Auto-link some images instead of other users' names
        query_redirects = {
            }
        if not self.init_api:
            self.refresh_ah_api()
        self.Player1.clear()
        self.Player1.append("None")
        self.Player1.append(0)
        self.Player1.append(0)
        self.Player1.append("")
        m_query = ' '.join(ctx.message.content.split()[1:]).lower()
        img = 'imagesrc'
        if m_query.find("~") >= 0:
            m_query,m_subquery = m_query.split("~",1)
            subexists = True
        m_response = ""
        if m_query in query_redirects.keys():
            m_response = query_redirects[m_query]
        elif not m_query:
            # post help text if no query
            m_response = "!apadd1 [Investigator name] - Add player 1 investigator \n"
        else:
            # Otherwise find and handle card names
            if not self.init_api:
                self.refresh_ah_api()
            else:
                # search player cards
                m_cards = [c for c in self.ah_api_p if c['name'].lower().__contains__(m_query)]
            if subexists:
                m_check = [c for c in m_cards if c['subname'].lower().__contains__(m_subquery)]
                if m_check:
                    m_cards = m_check
            for c in m_cards:
                if m_query == c['name'].lower():
                    # if exact name match, post only the one card
                    m_cards = [c]
                    break
            if len(m_cards) == 1:
                try:
                    self.Player1[0] = m_cards[0]['name']
                    self.Player1[1] = m_cards[0]['health']
                    self.Player1[2] = m_cards[0]['sanity']
                    self.Player1[3] = "http://arkhamdb.com" + m_cards[0][img]
                    m_response += "Player 1 added with investigator: "
                    m_response += self.Player1[0] + ", "
                    m_response += "health: " + str(self.Player1[1]) + ", "
                    m_response += "sanity: " + str(self.Player1[2]) + "."
                    
                except KeyError as e:
                    if e.args[0] == "imagesrc":
                        # if no image on ArkhamDB
                        m_response = "'{}' has no image on ArkhamDB:\n".format(m_cards[0]['name'])
                        m_response += "https://arkhamdb.com/card/" + m_cards[0]["code"]
            elif len(m_cards) == 0:
                m_response += "Sorry, I cannot seem to find any card with these parameters:\n"
                m_response += "http://arkhamdb.com/find/?q=" + m_query.replace(" ", "+")

        await ctx.send(m_response[:2000])

    @commands.command(aliases=['playerhealth1'], pass_context=True)
    async def aph1(self, ctx):
        """Modify player 1 health"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player1[1] += int(modifier)
        m_response = "Investigator " + self.Player1[0] + " has " + str(self.Player1[1]) + " health left."
        await ctx.send(m_response[:2000])
 
    @commands.command(aliases=['playersanity1'], pass_context=True)
    async def aps1(self, ctx):
        """Modify player 1 sanity"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player1[2] += int(modifier)
        m_response = "Investigator " + self.Player1[0] + " has " + str(self.Player1[2]) + " sanity left."
        await ctx.send(m_response[:2000])
 
     ## PLAYER 2 ##
    @commands.command(aliases=['addplayer2'], pass_context=True)
    async def apadd2(self, ctx):
        """Add player 2"""
        subexists = False
        # Auto-link some images instead of other users' names
        query_redirects = {
            }
        if not self.init_api:
            self.refresh_ah_api()
        self.Player2.clear()
        self.Player2.append("None")
        self.Player2.append(0)
        self.Player2.append(0)
        self.Player2.append("")
        m_query = ' '.join(ctx.message.content.split()[1:]).lower()
        img = 'imagesrc'
        if m_query.find("~") >= 0:
            m_query,m_subquery = m_query.split("~",1)
            subexists = True
        m_response = ""
        if m_query in query_redirects.keys():
            m_response = query_redirects[m_query]
        elif not m_query:
            # post help text if no query
            m_response = "!apadd2 [Investigator name] - Add player 2 investigator \n"
        else:
            # Otherwise find and handle card names
            if not self.init_api:
                self.refresh_ah_api()
            else:
                # search player cards
                m_cards = [c for c in self.ah_api_p if c['name'].lower().__contains__(m_query)]
            if subexists:
                m_check = [c for c in m_cards if c['subname'].lower().__contains__(m_subquery)]
                if m_check:
                    m_cards = m_check
            for c in m_cards:
                if m_query == c['name'].lower():
                    # if exact name match, post only the one card
                    m_cards = [c]
                    break
            if len(m_cards) == 1:
                try:
                    self.Player2[0] = m_cards[0]['name']
                    self.Player2[1] = m_cards[0]['health']
                    self.Player2[2] = m_cards[0]['sanity']
                    self.Player2[3] = "http://arkhamdb.com" + m_cards[0][img]
                    m_response += "Player 2 added with investigator: "
                    m_response += self.Player2[0] + ", "
                    m_response += "health: " + str(self.Player2[1]) + ", "
                    m_response += "sanity: " + str(self.Player2[2]) + "."
                    
                except KeyError as e:
                    if e.args[0] == "imagesrc":
                        # if no image on ArkhamDB
                        m_response = "'{}' has no image on ArkhamDB:\n".format(m_cards[0]['name'])
                        m_response += "https://arkhamdb.com/card/" + m_cards[0]["code"]
            elif len(m_cards) == 0:
                m_response += "Sorry, I cannot seem to find any card with these parameters:\n"
                m_response += "http://arkhamdb.com/find/?q=" + m_query.replace(" ", "+")

        await ctx.send(m_response[:2000])

    @commands.command(aliases=['playerhealth2'], pass_context=True)
    async def aph2(self, ctx):
        """Modify player 2 health"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player2[1] += int(modifier)
        m_response = "Investigator " + self.Player2[0] + " has " + str(self.Player2[1]) + " health left."
        await ctx.send(m_response[:2000])
 
    @commands.command(aliases=['playersanity2'], pass_context=True)
    async def aps2(self, ctx):
        """Modify player 2 sanity"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player2[2] += int(modifier)
        m_response = "Investigator " + self.Player2[0] + " has " + str(self.Player2[2]) + " sanity left."
        await ctx.send(m_response[:2000])
        
    ## PLAYER 3 ##
    @commands.command(aliases=['addplayer3'], pass_context=True)
    async def apadd3(self, ctx):
        """Add player 3"""
        subexists = False
        # Auto-link some images instead of other users' names
        query_redirects = {
            }
        if not self.init_api:
            self.refresh_ah_api()
        self.Player3.clear()
        self.Player3.append("None")
        self.Player3.append(0)
        self.Player3.append(0)
        self.Player3.append("")
        m_query = ' '.join(ctx.message.content.split()[1:]).lower()
        img = 'imagesrc'
        if m_query.find("~") >= 0:
            m_query,m_subquery = m_query.split("~",1)
            subexists = True
        m_response = ""
        if m_query in query_redirects.keys():
            m_response = query_redirects[m_query]
        elif not m_query:
            # post help text if no query
            m_response = "!apadd3 [Investigator name] - Add player 3 investigator \n"
        else:
            # Otherwise find and handle card names
            if not self.init_api:
                self.refresh_ah_api()
            else:
                # search player cards
                m_cards = [c for c in self.ah_api_p if c['name'].lower().__contains__(m_query)]
            if subexists:
                m_check = [c for c in m_cards if c['subname'].lower().__contains__(m_subquery)]
                if m_check:
                    m_cards = m_check
            for c in m_cards:
                if m_query == c['name'].lower():
                    # if exact name match, post only the one card
                    m_cards = [c]
                    break
            if len(m_cards) == 1:
                try:
                    self.Player3[0] = m_cards[0]['name']
                    self.Player3[1] = m_cards[0]['health']
                    self.Player3[2] = m_cards[0]['sanity']
                    self.Player3[3] = "http://arkhamdb.com" + m_cards[0][img]
                    m_response += "Player 3 added with investigator: "
                    m_response += self.Player3[0] + ", "
                    m_response += "health: " + str(self.Player3[1]) + ", "
                    m_response += "sanity: " + str(self.Player3[2]) + "."
                    
                except KeyError as e:
                    if e.args[0] == "imagesrc":
                        # if no image on ArkhamDB
                        m_response = "'{}' has no image on ArkhamDB:\n".format(m_cards[0]['name'])
                        m_response += "https://arkhamdb.com/card/" + m_cards[0]["code"]
            elif len(m_cards) == 0:
                m_response += "Sorry, I cannot seem to find any card with these parameters:\n"
                m_response += "http://arkhamdb.com/find/?q=" + m_query.replace(" ", "+")

        await ctx.send(m_response[:2000])

    @commands.command(aliases=['playerhealth3'], pass_context=True)
    async def aph3(self, ctx):
        """Modify player 3 health"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player3[1] += int(modifier)
        m_response = "Investigator " + self.Player3[0] + " has " + str(self.Player3[1]) + " health left."
        await ctx.send(m_response[:2000])
 
    @commands.command(aliases=['playersanity3'], pass_context=True)
    async def aps3(self, ctx):
        """Modify player 3 sanity"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player3[2] += int(modifier)
        m_response = "Investigator " + self.Player3[0] + " has " + str(self.Player3[2]) + " sanity left."
        await ctx.send(m_response[:2000])

    ## PLAYER 4 ##
    @commands.command(aliases=['addplayer4'], pass_context=True)
    async def apadd4(self, ctx):
        """Add player 4"""
        subexists = False
        # Auto-link some images instead of other users' names
        query_redirects = {
            }
        if not self.init_api:
            self.refresh_ah_api()
        self.Player4.clear()
        self.Player4.append("None")
        self.Player4.append(0)
        self.Player4.append(0)
        self.Player4.append("")
        m_query = ' '.join(ctx.message.content.split()[1:]).lower()
        img = 'imagesrc'
        if m_query.find("~") >= 0:
            m_query,m_subquery = m_query.split("~",1)
            subexists = True
        m_response = ""
        if m_query in query_redirects.keys():
            m_response = query_redirects[m_query]
        elif not m_query:
            # post help text if no query
            m_response = "!apadd4 [Investigator name] - Add player 1 investigator \n"
        else:
            # Otherwise find and handle card names
            if not self.init_api:
                self.refresh_ah_api()
            else:
                # search player cards
                m_cards = [c for c in self.ah_api_p if c['name'].lower().__contains__(m_query)]
            if subexists:
                m_check = [c for c in m_cards if c['subname'].lower().__contains__(m_subquery)]
                if m_check:
                    m_cards = m_check
            for c in m_cards:
                if m_query == c['name'].lower():
                    # if exact name match, post only the one card
                    m_cards = [c]
                    break
            if len(m_cards) == 1:
                try:
                    self.Player4[0] = m_cards[0]['name']
                    self.Player4[1] = m_cards[0]['health']
                    self.Player4[2] = m_cards[0]['sanity']
                    self.Player4[3] = "http://arkhamdb.com" + m_cards[0][img]
                    m_response += "Player 4 added with investigator: "
                    m_response += self.Player4[0] + ", "
                    m_response += "health: " + str(self.Player4[1]) + ", "
                    m_response += "sanity: " + str(self.Player4[2]) + "."
                    
                except KeyError as e:
                    if e.args[0] == "imagesrc":
                        # if no image on ArkhamDB
                        m_response = "'{}' has no image on ArkhamDB:\n".format(m_cards[0]['name'])
                        m_response += "https://arkhamdb.com/card/" + m_cards[0]["code"]
            elif len(m_cards) == 0:
                m_response += "Sorry, I cannot seem to find any card with these parameters:\n"
                m_response += "http://arkhamdb.com/find/?q=" + m_query.replace(" ", "+")

        await ctx.send(m_response[:2000])

    @commands.command(aliases=['playerhealth4'], pass_context=True)
    async def aph4(self, ctx):
        """Modify player 4 health"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player4[1] += int(modifier)
        m_response = "Investigator " + self.Player4[0] + " has " + str(self.Player4[1]) + " health left."
        await ctx.send(m_response[:2000])
 
    @commands.command(aliases=['playersanity4'], pass_context=True)
    async def aps1(self, ctx):
        """Modify player 4 sanity"""
        modifier = ' '.join(ctx.message.content.split()[1:])
        self.Player4[2] += int(modifier)
        m_response = "Investigator " + self.Player4[0] + " has " + str(self.Player4[2]) + " sanity left."
        await ctx.send(m_response[:2000])        
 
def setup(bot):
    bot.add_cog(ArkhamPlayer(bot))