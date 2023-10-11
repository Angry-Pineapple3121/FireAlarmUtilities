import discord
import datetime
import requests
import re
from parsel import Selector

from discord.ext import commands
from discord.commands import Option

BOT_VERSION = open('version').read()

def parse_item(sel: Selector):
    # parsing shortcuts to avoid repetition:
    css_join = lambda css: "".join(sel.css(css).getall()).strip()  # join all selected elements
    css = lambda css: sel.css(css).get("").strip()  # take first selected element and strip of leading/trailing spaces

    item = {}
    item["url"] = css('link[rel="canonical"]::attr(href)')
    item["id"] = item["url"].split("/itm/")[1].split("?")[0]  # we can take ID from the URL
    item["price"] = css('.x-price-primary span.ux-textspans ::text')
    item["shipping"] = css(".ux-labels-values__values-content span.ux-textspans::text")  # ebay automatically converts price for some regions

    item["name"] = css_join("h1 span::text")
    item["seller_name"] = css_join(".ux-seller-section__item--seller span.ux-textspans ::text")
    item["photos"] = sel.css('.ux-image-filmstrip-carousel-item.image img::attr("src")').getall()  # carousel images
    item["photos"].extend(sel.css('.ux-image-carousel-item.image img::attr("src")').getall())  # main image
    return item

class AucLink(discord.ui.View):
    def __init__(self, auclink: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="View Auction", url=auclink, emoji="<:ebay:1153523851016278046>"))


class AucPreview(commands.Cog):
    print('★ Loaded cog: eBay Auction Prettifier')
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def aucpreview(
        self,
        ctx,
        url: Option(str, 'The listing link you\'d like to preview.', required=True),
        anon: Option(str, 'Hides the slash command execution. Good for showcasing in for-sale channels.', required=False, choices=['True', 'False'], default='False')
    ):
        """Makes an eBay Auction much easier to read and understand via Discord."""
        requestTime = datetime.datetime.now()
        print(f'[{requestTime}] [Auction Beautifier] Requested by {ctx.author} (ID: {ctx.author.id}) with auction {url}')

        with open('blacklist', 'r') as file:
            GLOBAL_BLACKLIST = [int(line.strip()) for line in file if line.strip()]
            
        if ctx.author.id in GLOBAL_BLACKLIST:
            await ctx.respond('<:X_:1152069831638650890> Your account is currently **blacklisted** from all features in Fire Alarm Utilities.')
            print(f'[{datetime.datetime.now()}] [Blacklisted] {ctx.author} (ID: {ctx.author.id}) attempted to use a command they are blacklisted from using.')
        
        else:
            validation = re.search("http?(s)://www.ebay.com/itm/[0-9]+", url)
            if validation:
                try:
                    dirtyurl = url
                    aucurl = re.search("http?(s)://www.ebay.com/itm/[0-9]+", dirtyurl)
                    #aucurl[0]
                    embed = discord.Embed(
                        title=f"<:slash:1150933397179486339> eBay Auction Previewer",
                        description=f'Showing data for auction **{aucurl[0]}**.',
                        color=discord.Colour.blurple(),
                    )
    
                    now = datetime.datetime.now()
                    rtime = now.strftime("%B %d, %Y, %H:%M")
                    embed.set_footer(text=f"Requested by {ctx.author.display_name} » {rtime} | {BOT_VERSION}")
    
                    # handle logic for dealing with the auction shit and stuff
                    response = requests.get(aucurl[0])
                    selector = Selector(response.text)
                    item = parse_item(selector)
    
                    #print(item)
    
                    embed.add_field(name=f"📚 Auction Name", value=f'```{item["name"]}```', inline=False)
                    embed.add_field(name=f"💵 Price", value=f'**```{item["price"]}```**', inline=True)
                    embed.add_field(name=f"📦 Shipping", value=f'```{item["shipping"]}```', inline=True)
                    embed.add_field(name=f"🪝 Seller", value=f'```{item["seller_name"]}```', inline=True)
    
                    embed.set_image(url=item["photos"][-1])
                        
                    if anon == 'False':
                        await ctx.respond(embed=embed, view=AucLink(aucurl[0]))
                    else:
                        await ctx.send(embed=embed, view=AucLink(aucurl[0]))
                        await ctx.respond("<:check:1081988275851513919> Successfully processed your request.", ephemeral=True)
    
    
                except Exception as e:
                    await ctx.respond('<:warn:1105998033335898162> An error occurred when processing your command. Please contact `Angry_Pineapple#6926` with what you were attempting to do, along with the date and time.', ephemeral=True)
                    print(f'[{requestTime}] [*** BOT ERROR ***] {e}')
                    pass
            else:
                await ctx.respond('<:warn:1105998033335898162> That eBay link doesn\'t appear to be valid. Please try a different link.', ephemeral=True)

def setup(bot):
    bot.add_cog(AucPreview(bot))