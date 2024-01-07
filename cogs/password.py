import discord
import datetime
import uuid
import re

from discord.ext import commands
from discord.commands import Option

BOT_VERSION = open('version').read()

GLOBAL_CHART_1 = {
    '000': '00',
    '008': '01',
    '010': '02',
    '018': '03',
    '020': '04',
    '028': '05',
    '030': '06',
    '038': '07',
    '040': '08',
    '048': '09',
    '080': '10',
    '088': '11',
    '090': '12',
    '098': '13',
    '0A0': '14',
    '0A8': '15',
    '0B0': '16',
    '0B8': '17',
    '0C0': '18',
    '0C8': '19',
    '11D': '20',
    '115': '21',
    '10D': '22',
    '105': '23',
    '13D': '24',
    '135': '25',
    '12D': '26',
    '125': '27',
    '15D': '28',
    '155': '29',
    '19D': '30',
    '195': '31',
    '18D': '32',
    '185': '33',
    '1BD': '34',
    '1B5': '35',
    '1AD': '36',
    '1A5': '37',
    '1DD': '38',
    '1D5': '39',
    '23A': '40',
    '232': '41',
    '22A': '42',
    '222': '43',
    '21A': '44',
    '212': '45',
    '20A': '46',
    '202': '47',
    '27A': '48',
    '272': '49',
    '2BA': '50',
    '2B2': '51',
    '2AA': '52',
    '2A2': '53',
    '29A': '54',
    '292': '55',
    '28A': '56',
    '282': '57',
    '2FA': '58',
    '2F2': '59',
    '327': '60',
    '32F': '61',
    '337': '62',
    '33F': '63',
    '307': '64',
    '30F': '65',
    '317': '66',
    '31F': '67',
    '367': '68',
    '36F': '69',
    '3A7': '70',
    '3AF': '71',
    '3B7': '72',
    '3BF': '73',
    '387': '74',
    '38F': '75',
    '397': '76',
    '39F': '77',
    '3E7': '78',
    '3EF': '79',
    '474': '80',
    '47C': '81',
    '464': '82',
    '46C': '83',
    '454': '84',
    '45C': '85',
    '444': '86',
    '44C': '87',
    '434': '88',
    '43C': '89',
    '4F4': '90',
    '4FC': '91',
    '4E4': '92',
    '4EC': '93',
    '4D4': '94',
    '4DC': '95',
    '4C4': '96',
    '4CC': '97',
    '4B4': '98',
    '4BC': '99'
}

GLOBAL_CHART_2 = {
    '00': '0', 
    '08': '1', 
    '10': '2',
    '18': '3',
    '20': '4',
    '28': '5',
    '30': '6',
    '38': '7',
    '40': '8',
    '48': '9'
}

def decode_pw(encoded_pw):
    # step one already done since its encoded_pw
    # Step 2
    first_two_digits_decode = GLOBAL_CHART_1[encoded_pw[:3]]

    # Step 3
    next_two_digits_decode = hex(min(range(0, 49, 8), key=lambda x: abs(int(encoded_pw[3:5], 16) - x)))[2:]
    if len(next_two_digits_decode) == 1:
        next_two_digits_decode = '0' + next_two_digits_decode

    final_two_digits = GLOBAL_CHART_2[str(next_two_digits_decode)]

    # Step 4
    rounded_value = (int(encoded_pw[3:5], 16) // 8) * 8
    step_4_code = int(hex(rounded_value)[2:] + '00')

    # Step 5
    last_four_digits = int(encoded_pw[3:], 16)
    new_step4 = int(str(step_4_code), 16)

    step_5_result = hex(last_four_digits - new_step4)[2:]
    if len(step_5_result) == 2:
        step_5_result = '0' + step_5_result

    # Step 6
    step_6_result = GLOBAL_CHART_1[step_5_result.upper()]

    # Step 7
    final_decoded_pass = first_two_digits_decode + final_two_digits + step_6_result

    return final_decoded_pass

class Password(commands.Cog):
    print('★ Loaded cog: Notifier Password Decoder [EXPERIMENT]')
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def password(
        self,
        ctx,
        password: Option(str, 'The password you want to decode.', required=True),
    ):
        """Decodes an encrypted Level 1 or Level 2 password for use with specific Notifier panels."""
        requestTime = datetime.datetime.now()
        print(f'[{requestTime}] [Simplex MNC] Requested by {ctx.author} (ID: {ctx.author.id}) with encoded password {password}')

        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
            
        if ctx.author.id in GLOBAL_BLACKLIST:
            await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
            print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
            
        else:
            with open ('enrolled', 'r') as file:
                ENROLLED_USERS = [int(line.strip()) for line in file if line.strip()]
            
            if ctx.author.id not in ENROLLED_USERS:
                embed = discord.Embed(
                    title=f"",
                    description=f'<:warn:1105998033335898162> You\'re not enrolled in the Experimental Features program yet! To enroll, run the `/enroll` command.',
                    color=discord.Colour.yellow(),
                )

                await ctx.respond(embed=embed, ephemeral=True)
                return
            
            else:
                try:
                    # regex for possible password formats
                    pwRegex = '^[0-9A-F]{7}$'

                    # we want to check if the password is a valid 'pwRegex' password
                    if not re.match(pwRegex, password):
                        await ctx.respond('<:warn:1105998033335898162> The password you entered does not follow the standard encrypted password format.', ephemeral=True)
                        return 
                    else:
                        embed = discord.Embed(
                            title=f"<:slash:1150933397179486339> Notifier Password Decoder",
                            description=f'Designed for use with the Notifier `AM-2020`, `AFP-1010` and `AFP-200` series panels. **This command is experimental and may not work as intended.**',
                            color=discord.Colour.red(),
                        )

                        now = datetime.datetime.now()
                        rtime = now.strftime("%B %d, %Y, %H:%M")
                        embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")

                        # decode the password
                        decoded_password = decode_pw(password)

                        embed.add_field(name='🔑 Decoded Password', value=f'```{decoded_password}```', inline=False)

                        await ctx.respond(embed=embed)

                except Exception as e:
                    error_id = uuid.uuid4()
                    await ctx.respond(f'<:warn:1105998033335898162> An error occurred when processing this experimental command. Let <@304054669372817419> know and provide the following error code: `{error_id}`', ephemeral=True)
                    print(f'[Experimental Command Error] Error ID: {error_id}')
                    print(f'[{requestTime}] [*** BOT ERROR ***] {e}')
                    pass

def setup(bot):
    bot.add_cog(Password(bot))