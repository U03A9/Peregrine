import discord
import re
import subprocess
import sys
import time
import json
import sys
from io import StringIO

from colorama import init
from termcolor import colored

from ESSENTIALS import *
from TOKEN import TOKEN
from URL_ANALYSIS import submit_URL


class Peregrine(discord.Client):

    # Display logo and basic information on successfull login

    async def on_ready(self):
        with open('resources/logo.txt', 'r') as mylogo:
                logo = mylogo.read()
        print(colored(logo, 'red'))
        print(colored(self.user.id, 'red'))

    async def on_message(self, message):

        BOT_MESSAGE = ""
        ANALYSIS_MESSAGE = ""
        ANALYSIS_FULL = ""


        if message.content.startswith('!peregrine'):
            channel = message.channel
            return

            if message.content.endswith('status'):
                await channel.send('Status: Logged In')
                return

        # Check message for urls

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content.lower())

        if urls:

            try:

                with open('resources/quote_Message.txt', 'r') as quote_File:
                        quote_Message = quote_File.read()
                await message.delete()

                BOT_MESSAGE = await message.channel.send('Peregrine Discord Malware Protection :bird:\n\n```Do not panic, {}!\nYour URL has been submitted to Hybrid-Analysis for evaluation.\nOnce this process is completed this message will update.\n\n\nAwaiting report.```'.format(message.author))


                for url in urls:
                    print("URL detected in message ID: ", message.id)
                    print("Initiating scan on URL: ", url)
                    ANALYSIS_MESSAGE = await submit_URL(url, message)
                    ANALYSIS_FULL = ANALYSIS_FULL + ANALYSIS_MESSAGE + "\n"
                    fullMessage = "```" + ANALYSIS_FULL + "```" + "\n" + quote_Message.format(message.content, message.author)

                await BOT_MESSAGE.edit(content = fullMessage)

            except Exception as e:

                print("Exception throwin is: {}".format(e))
                await BOT_MESSAGE.edit(content = 'Could not process url.')

                time.sleep(1)


client = Peregrine()
client.run(TOKEN)
