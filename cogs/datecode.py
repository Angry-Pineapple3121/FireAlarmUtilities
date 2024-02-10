import discord
import re

from datetime import datetime, timedelta
from discord.ext import commands
from discord.commands import Option

BOT_VERSION = open('version').read()

def convert_date_code(date_code):
    # Extract year and day components
    year = int(date_code[:2])
    day_of_year = int(date_code[2:])

    # Assuming all dates are in the 2000s, you can adjust this if necessary
    century = 2000

    # Calculate the date using datetime module
    manufacturing_date = datetime(century + year, 1, 1) + timedelta(days=day_of_year - 1)

    # Format the date as a string
    formatted_date = manufacturing_date.strftime('%B %d, %Y')

    return formatted_date

class SimplexDCD(commands.Cog):
    print('★ Loaded cog: Simplex Date Code Decoder')
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def simplexdcd(
        self,
        ctx,
        datecode: Option(str, 'The date code of the device you want to view. Should be in a format similar to "22 107 V".', required=True),
    ):
        """Checks when a Simplex device was manufactured based on its date code."""
        requestTime = datetime.now()
        print(f'[{requestTime}] [Simplex DCD] Requested by {ctx.author} (ID: {ctx.author.id}) with date code {datecode}')

        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
            
        if ctx.author.id in GLOBAL_BLACKLIST:
            await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
            print(f'[{datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
        else:
            try:
                embed = discord.Embed(
                    title=f"<:slash:1150933397179486339> Simplex Date Code Decoder",
                    description=f'Finished decoding date code **{datecode}**.',
                    color=discord.Colour.fuchsia(),
                )
    
                now = datetime.now()
                rtime = now.strftime("%B %d, %Y, %H:%M")
                embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")
    
                # regex for our date code
                code_regex = '[0-9]{2} [0-9]{3}'

                # check to see if we match the date code and throw error if we don't
                try:
                    if not re.match(code_regex, datecode).group():
                        return
                except:
                    await ctx.respond('<:warn:1105998033335898162> The date code you entered does not follow the standard (moden) date code format.', ephemeral=True)
                    return
                # if no error match again and do the stuff
                else:
                    date_code = re.match(code_regex, datecode).group()
                    
                    readable_date = convert_date_code(date_code)

                    embed.add_field(name=f":gear: Manufacturing Date", value=f'**```{readable_date}```**', inline=True)
                    await ctx.respond(embed=embed)
                

            except Exception as e:
                await ctx.respond('<:warn:1105998033335898162> An error occurred when processing your command. Please contact `Angry_Pineapple#6926` with what you were attempting to do, along with the date and time.', ephemeral=True)
                print(f'[{requestTime}] [*** BOT ERROR ***] {e}')
                pass

def setup(bot):
    bot.add_cog(SimplexDCD(bot))