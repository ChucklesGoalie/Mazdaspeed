import discord
from discord.ext import commands
from discord.ui import Select, View
from discord import app_commands, Colour
import time
import json
import os
import io
import math
import socket
import pandas as pd
import aiohttp
import re
import asyncio
from collections import Counter
import numpy as np
from client_run import NORMAL_BOT_KEY, DEV_BOT_KEY
cogs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')

GUILD_ID = 462106215007256576 

class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_file_path = None
        self.cog_folder = None
    async def on_ready(self):
        print(f'Logged on as {self.user} \n{time.strftime(("[%d/%m/%Y, %I:%M:%S %p ET]"))}')
        print("Version 0.4")
        await self.tree.sync()
        try:
            guild = discord.Object(id=GUILD_ID)
            sync = await self.tree.sync(guild=guild)
            print(f'Synced {len(sync)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing command: {e}')
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Zoom Zoom Boom Forums"))
    async def on_command_error(self, ctx, error):
        user = ctx.message.author
        await ctx.send(error)
        print(f'[{user.guild}]', f'{time.strftime(("[%d/%m/%Y, %I:%M:%S %p ET]"))}', error)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  
intents.members = True
client = Client(command_prefix="!", intents=intents)
guild = discord.Object(id=GUILD_ID)

@client.tree.command(name='hello', description='Says Hello', guild=guild)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello There!")

@client.tree.command(name='exhaust', description='Shows the stock exhaust system', guild=guild)
async def exhaust(interaction: discord.Interaction):
        with open('ms3exhaust.jpg', 'rb') as f:
            picture = discord.File(f)
        await interaction.response.send_message(f"Heres photo of exhaust - ")
        await interaction.followup.send(file=discord.File('ms3exhaust.jpg'))

@client.tree.command(name='suspension', description='Asks what suspension you should use', guild=guild)
async def suspension(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="What's the best suspension for Mazdaspeed!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Best for Lowering and bad road performance", value="Raceland, Godspeed, Maxspeedingrods", inline=True)
    embed.add_field(name="Decent Suspension:", value="Graveyard Performance, BC Racing, Tein, Scale \nShocks: Koni, KYB, Bilstein \nCoils: H&R, Eibach, Corksport, Tein, Swift Sport Spec-R,", inline=True)
    embed.add_field(name="Good Coilovers:", value="Fortune Auto, KW", inline=True)
    embed.add_field(name="Suspension forum:", value="https://mazdaspeeds.org/index.php?threads/the-official-ms3-suspension-thread.15531/", inline=False)
    embed.set_footer(text="These are based off of previous people's feels to each suspension setup, and overall build quality. Less quality will always result in lower street and track performance and better suspension will always have superior adjustability. Please visit forum for more info")
    await interaction.followup.send(embed=embed)

@client.tree.command(name='turbos', description='Asks what turbo you should use and for what application', guild=guild)
async def turbos(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="What's the best turbo for Mazdaspeed!",
        color=discord.Color.red()
    )
    embed.add_field(name="Stock type performance", value="K04 - OEM \nBNR S1 - OEM equivelent \nBNR S2 - Almost OEM replacement, slightly bigger and better flow", inline=False)
    embed.add_field(name="Slightly bigger", value="BNR S3 - Higher flow rate, better design and power until redline \nCTS4 - Same type as BNR, But takes slightly longer to spool", inline=False)
    embed.add_field(name="Bigger", value="CTS5 - Not recommended, anything higher than BNR S4 or CTS4 it's better to go to Garrett or other turbos", inline=False)
    embed.set_footer(text="Note: BNR S4 will be better in saving your engine if you do not have port injection as the torque will be applied around 1000rpm later, therefore saving your rods.")
    await interaction.followup.send(embed=embed)

@client.tree.command(name='buy_turbos', description='Purchasing turbos', guild=guild)
async def buyturbos(interaction: discord.Interaction):
    BNR_website = "https://bnrturbos.com/collections/mazdaspeed-3-6"
    CS_website = "https://corksport.com/mazdaspeed-3/2010-2013-mazdaspeed-3/2010ms3-power/turbo-system-parts/page-2/"
    await interaction.response.send_message(f"BNR's Website: <{BNR_website}>, \nCorksport's Website: <{CS_website}>")

@client.tree.command(name="vendors", description='Vendors to use when buying parts for Mazdaspeed components', guild=guild)
async def vendors(interaction: discord.Interaction):
    CW_Turbo = "https://www.cwturbochargers.com/"
    Graveyard = "https://www.graveyardperformance.com/"
    DamondMT = "https://damondmotorsports.com/"
    CS = "https://corksport.com/"
    #forte = discord.Member.id(267147762615713793)
    embed = discord.Embed(
        title="Vendors for Mazdaspeed's",
        color=discord.Color.blue()
    )
    embed.add_field(name="Graveyard Performance", value=f"Contact Forte or their website: {Graveyard}", inline=False)
    embed.add_field(name="CW Turbochargers", value=f"Canadian Company, website is: {CW_Turbo}", inline=False)
    embed.add_field(name="Corksport", value=f"Website is: {CS}", inline=False)
    embed.add_field(name="Damond Motorsport", value=f"Website is: {DamondMT}", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="manuals", description="Manual for Mazdaspeeds", guild=guild)
async def manuals(interaction=discord.Interaction):
    embed = discord.Embed(
        title="Manuals for Mazdaspeeds",
        color=discord.Color.blue()
    )
    ms6 = "https://www.mazdausa.com/siteassets/pdf/owners-optimized/2006/mazdaspeed6/2006-mazdaspeed6-owners-manual.pdf?msockid=3f96a76bfb4167592defb12ffa6e66a0"
    m307 = "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2007_mazdaspeed3_manual_en_optimized.pdf" 
    m308= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2008_mazdaspeed3_manual_en_optimized.pdf"
    m309= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2009_mazdaspeed3_manual_en_optimized.pdf"
    m3010= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2010_mazdaspeed3_manual_en_optimized.pdf"
    m3011= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2011_mazdaspeed3_manual_en_optimized.pdf"
    m3012= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2012_mazdaspeed3_manual_en_optimized.pdf"
    m3013= "https://www.mazda.ca/globalassets/mazda-canada/en/pdf/manuals/vehicles/mazdaspeed3/2013_mazdaspeed3_manual_en_optimized.pdf"
    embed.add_field(name="Mazdaspeed 6", value=ms6, inline=False)
    embed.add_field(name="Mazdaspeed 3", value=f"2007:{m307} \n2008: {m308} \n2009: {m309} \n2010: {m3010} \n2011: {m3011} \n2012: {m3012} \n2013: {m3013}", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="maintenance", description="Recommended Maintenance Schedule", guild=guild)
async def maintenance(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Maintenance Schedule for Mazdaspeeds",
        color=discord.Color.blue()
    )
    embed.add_field(name="3,000 Miles (5,000km)", value="Oil Change \nInspect Fluids \nLook for Leaks", inline=False)
    embed.add_field(name="15,000 miles (25,000km)", value="Change / Clean air filters \nchange brake fluid", inline=False)
    embed.add_field(name="30,000 Miles (50,000km)", value="Check / Replace Spark Plugs (Do Compression test since you are there) \nDrain and Fill Transmission Fluid \n Coolant flush", inline=False)
    embed.add_field(name="50,000 Miles (80,000km) and or\n100,000 Miles (160,000km)", value="Valve Cleaning \nInjector Cleaning / Flow Test \nVVT Inspection / Replacement (IMPORTANT FOR 07-11 MODEL YEARS)", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="tunefreemods", description="Modifications that do not require a tune on the vehicle", guild=guild)
async def tunefreemods(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Tune Free Mods",
        color=discord.Colour.green()
    )
    embed.add_field(name="Catch Can / PCV Plate", value="", inline=False)
    embed.add_field(name="BPV / Dual Port BPV / BOV", value="A Blow Off Valve will cause your car to run rich when decelerating or shifting, tuners are unable to tune for BOV's", inline=False)    
    embed.add_field(name="Motor Mounts", value="These are highly recommended. Damond or Corksport are good, but Damond has less NVH and may ride better", inline=False)
    embed.add_field(name="Catback / Axleback exhaust system", value="", inline=False)
    embed.add_field(name="Short Throw Shifter / Short Shift Plate", value="Short Shift Plate is not recommended as it can possibly strecth the shifting cables", inline=False)
    embed.add_field(name="Drop in Air Filter", value="", inline=False)
    await interaction.response.send_message(embed=embed)
    # embed.add_field(name="", value="", inline=False)

@client.tree.command(name="turboflow", description="Turbo Flow Rate for most common Turbo's within Mazdaspeed platform", guild=guild)
async def turboflow(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Turbo Flow Rates",
        description="Here are the Flow Rates for the common turbos",
        color=discord.Colour.green()
    )
    embed.add_field(name="K04", value="~35lbs/min", inline=False)
    embed.add_field(name="BNR S1 / S2", value="40lbs/min", inline=False)    
    embed.add_field(name="BNR S3", value="46lbs/min", inline=False)
    embed.add_field(name="BNR S4 V4", value="53lbs/min", inline=False)
    embed.add_field(name="BNR S4 V5", value="66lbs/min", inline=False)
    embed.add_field(name="CTS4", value="50lbs/min", inline=False)
    embed.add_field(name="CTS5", value="56lbs/min", inline=False)
    embed.add_field(name="CTS6", value="64lbs/min", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="tuners", description="List of Tuners who know the platform", guild=guild)
async def tuners(interaction: discord.Interaction):
    speedwiz = 744994903611670538
    embed = discord.Embed(
        title="List of Tuners",
        description="Please use these tuners because the mentioned are knowledgeable with the platform. You can NOT tune these yourself with EcuTek but you can with Versatune. If you are looking to tune your Mazdaspeed, the available tuning options are COBB Accessport, Versatune, and ECUTEK which is no longer supported.",
        colour= discord.Colour.magenta(),
        url="https://mazdaspeeds.org/index.php"
    )
    embed.add_field(name="FreekTune", value="https://www.freektune.com/collections/mazdaspeed/e-tune", inline=False)
    embed.add_field(name="PD Tuning", value="https://www.pd-tuning.com/tuning-request/", inline=False)
    embed.add_field(name="Damond Motorsport", value="https://damondmotorsports.com/collections/tuning", inline=False)
    embed.add_field(name="Stratified Tuning", value="https://www.stratifiedauto.com/index.php?main_page=index&cPath=87", inline=False)
    embed.add_field(name="Edge Autosport", value="https://edgeautosport.com/edge-autosport-etune-mazdaspeed-3-2007-2013-mazdaspeed-6-2006-2007/", inline=False)
    embed.add_field(name="Tuned by Nishan", value="https://www.tunedbynishan.com/support.html", inline=False)
    embed.add_field(name="Versatuner - Self tune or E-Tune", value="https://www.versatuner.com/", inline=False)
    embed.set_footer(text="If you need more information, or have questions, dont hesitate to ping the Speed Wizard's, or Zenith")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="horsepower_goals", description="What are your horsepower goals? Please view this to see what is needed for your goals", guild=guild)
async def horsepower_goals(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Video of Horsepower goals",
        description="Please view the video linked in the title to watch PD Tuning explain what is all needed for certain Horsepower goals",
        colour= discord.Colour.green(),
        url="https://www.dropbox.com/scl/fi/8dak78nwex3rj8m31bsqf/1548027956239.mp4?rlkey=zctnuhk8owo2xl2mi4b883lzu&e=1&dl=0"
    )
    embed.add_field(name="275-325", value="HPFP, Intake", inline=False)
    embed.add_field(name="330-370", value='Previous + 3" intake, Optional Turbo upgrade', inline=False)
    embed.add_field(name="375-475", value='Previous + 3.5-4" intake, Catted or Catless DP, FMIC, Turbo upgrade, clutch and flywheel, Intake Manifold, Port Injection, Optional Meth, Optional Forged Rotating assembly', inline=False)
    embed.add_field(name="500+", value="Previous + Catless DP, Forged Rotating assembly", inline=False)
    embed.add_field(name="600+", value="Previous + ...", inline=False)
    embed.add_field(name="700-1,000", value="Get a different Car", inline=False)
    embed.set_footer(text="If you need more information, or have questions, dont hesitate to ping Zenith")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="faq", description="FAQ", guild=guild)
async def faq(interaction : discord.Interaction):
    embed = discord.Embed(
        title="FAQ",
        description="",
        colour= discord.Colour.green(),
        url=""
    )
    with open('HPFP type.jpg', 'rb') as f:
        hpfp = discord.File(f)
    embed.add_field(name="what oil to run?", value="Oil brand doesn't matter too much some are subjectively better than others you can check out this link for all the specifics, mazdaspeeds.org \nhttps://mazdaspeeds.org/index.php?threads/best-engine-oil-all-mod-levels.7931/ \nMost of the time penz plat 5w30 is the best along with Royal purple 5w-30! Please see link for a complete breakdown!", inline=False)
    embed.add_field(name="How do I know if I have hpfp internals already/what company to buy from.", value="you have to take apart the hpfp and look at the valve itself The tip of the valve has different shapes as shown: \nThe best company to buy hpfp internals is usually whatever is one sale at the time as they are all basically the same thing. Company doesn't matter at all through testing just get them upgraded asap!", inline=False)
    await interaction.response.send_message(embed=embed)
    await interaction.followup.send(file=discord.File('HPFP type.jpg'))

@client.tree.command(name="corn", description="Ethanol Fuel", guild=guild)
async def corn(interaction : discord.Interaction):
    await interaction.response.send_message("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHhjNG9kZjl6dGdsdXcwb2FlOHFjeG0yeGtsbmZhNGlwbDNuOXU2diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yUZvqAk6pjIYNlpEdc/giphy.gif")

@client.tree.command(name="newspeed", description="So you bought a new to you Mazdaspeed... heres a quick guide on the mazdaspeed forum")
async def newspeed(interaction : discord.Interaction):
    await interaction.response.send_message("https://www.mazdaspeeds.org/threads/congratulations-you-bought-your-mazdaspeed-now-what.16270/")

@client.tree.command(name="motormounts", description="Ever wonder what motor mounts you need for your Mazdaspeed?", guild=guild)
async def motormounts(interaction : discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="Motor Mounts",
        description="Motor mounts are what keep your engine from moving within the engine bay. They are meant to take the vibration of the engine. OEM motor mounts are original Mazda 3 mounts that are not meant to handle enormous mounts of torque like the L3-DISI engines. Here are a list of all part numbers and replacements.",
        colour=discord.Colour.darker_grey()
    )
    embed.add_field(name="Mazdaspeed 3's", value="All Mazdaspeed 3's Mounts are the same. You have the option of Race and Street bushings for the Polyurathane mount. Street is 70a and Race is 88a stiffness. The stiffer the mount is, the more Noise, Vibrations, and Harshness (NVH) you will feel. If you are daily driving the Speed, it is recommended that you get Street bushings. It is also recommended to replace the sides at the same time because the stiffness of one bushing will put more pressure and weight on the other side, therefore wearing out the weaker bushing faster. Rear Motor Mount does not have any choices for bushings, it is just the Race Bushing.", inline=False)
    embed.add_field(name="Transmission Motor Mount (TMM)", value="OEM Part #:BBR3-39-070A \n[TMM From CW(Canadian)](https://www.cwturbochargers.com/products/mazdaspeed3-damond-motorsports-transmission-motor-mount?_pos=14&_sid=92c49384d&_ss=r)\n[TMM From Damond](https://damondmotorsports.com/collections/mazdaspeed-3/products/transmission-motor-mount)\n[TMM From CS](https://corksport.com/mazdaspeed-3-performance-transmission-mount.html)", inline=True)
    embed.add_field(name="Rear Motor Mount (RMM)", value="OEM Part #:BBN5-39-040A \n[RMM From CW(Canadian)](https://www.cwturbochargers.com/products/damond-motorsports-rear-motor-mount?_pos=13&_sid=92c49384d&_ss=r)\n[RMM From Damond](https://damondmotorsports.com/collections/mazdaspeed-3/products/mazdaspeed3-rear-motor-mount-newly-revised)\n[RMM From CS](https://corksport.com/corksport-mazdaspeed-3-mazda-3-race-rear-motor-mount.html)", inline=True)
    embed.add_field(name="Passenger Motor Mount (PMM)", value="OEM Part #:BBN5-39-060 \n[PMM From CW(Canadian)](https://www.cwturbochargers.com/products/mazdaspeed-3-damond-passenger-side-motor-mount?_pos=1&_sid=92c49384d&_ss=r)\n[PMM From Damond](https://damondmotorsports.com/collections/mazdaspeed-3/products/passenger-side-motor-mount-mazdaspeed3)\n[PMM From CS](https://corksport.com/corksport-mazdaspeed-3-passenger-side-motor-mount.html)", inline=True)
    embed.add_field(name="Mazdaspeed 6", value="The bushings are the same stiffness as the Mazdaspeed 3's but bolt up differently to the 6's body.", inline=False)
    embed.add_field(name="Transmission Motor Mount (TMM)", value="OEM Part #:GK2A-39-070D \n[TMM From CW(Canadian)](https://www.cwturbochargers.com/products/damond-motorsports-mazdaspeed6-transmission-mount?variant=43449915703511)\n[TMM From AWR/Graveyard Performance](https://www.graveyardperformance.com/products/awr-mazdaspeed-6-passenger-side-mount?_pos=1&_sid=feeb27596&_ss=r)\n", inline=True)
    embed.add_field(name="Rear Motor Mount (RMM)", value="OEM Part #: DISCONTINUED \n[RMM From CW(Canadian)](https://www.cwturbochargers.com/products/mazdaspeed6-damond-motorsports-rear-motor-mount?variant=43443331825879)\n[RMM From Damond](https://damondmotorsports.com/products/rear-motor-mount-mazdaspeed6?_pos=24&_sid=26846115c&_ss=r)", inline=True)
    embed.add_field(name="Passenger Motor Mount (PMM)", value="OEM Part #:GP9A-39-060D \n[PMM From CW(Canadian)](https://www.cwturbochargers.com/products/damond-motorsports-mazdaspeed6-passenger-side-motor-mount?variant=43449902399703)\n[PMM From Damond](https://damondmotorsports.com/products/passenger-side-motor-mount-mazdaspeed6?_pos=9&_sid=26846115c&_ss=r)", inline=True)
    await interaction.followup.send(embed=embed)

@client.tree.command(name="bumpersag", description="Want to fix your bumper sag? ", guild=guild)
async def bumpersag(interaction : discord.Interaction):
    await interaction.response.defer()
    embed= discord.Embed(
        title="Raiderfab's Website",
        description="Ever needed better fitment or a quick release bumper? Raiderfab has made a nice and easy solution to said issue!",
        url="https://raiderfab.myshopify.com/",
        colour=discord.Colour.dark_magenta()
    )
    embed.add_field(name="Mazdaspeed 3 Gen 1", value="[Fenderwell area](https://raiderfab.myshopify.com/products/2007-2009-mazdaspeed-3-bumper-fitment-solution-fenderwell-only)\n[Full Kit](https://raiderfab.myshopify.com/products/2007-2009-mazdaspeed-3-bumper-fitment-solution-full-kit)", inline=True)
    embed.add_field(name="Mazdaspeed 3 Gen 2", value="[Fitment Kit](https://raiderfab.myshopify.com/products/2010-2013-mazdaspeed-3-bumper-fitment-solution)", inline=True)
    embed.add_field(name="Mazdaspeed 6", value="[Lower area](https://raiderfab.myshopify.com/products/mazda-6-mazdaspeed-6-bumper-fitment-kit)\n[Fenderwell area](https://raiderfab.myshopify.com/products/mazda-6-mazdaspeed-6-bumper-fitment-kit-fenderwell-area)\n[Headlight area](https://raiderfab.myshopify.com/products/mazda-6-mazdaspeed-6-bumper-fitment-kit-headlight-area)\n[Full Kit](https://raiderfab.myshopify.com/products/mazda-6-mazdaspeed-6-bumper-fitment-full-kit)", inline=False)
    embed.set_author(name=f"Thanks to Raiderfab for making this easy solution!", url=f"{embed.url}")
    await interaction.followup.send(embed=embed)

@client.tree.command(name="indepthmaintenance", description="Here is an in depth maintenance record of what your vehicle should look like")
async def indepthmaintenance(interaction :discord.Interaction):
    embed= discord.Embed(
        title="",
        description="",
        colour= discord.Colour.random()
    )
    return
@client.tree.command(name="doanddonts", description="Do's and Don'ts with your Mazdaspeed", guild=guild)
async def doanddonts(interaction:discord.Interaction):    
    embed=discord.Embed(
        title="Do's and Dont's of Mazdaspeeds",
        colour=discord.Colour.random()
    )
    embed.add_field(name="Do's", value="Let car warm up for 15~60 seconds before moving \n", inline=True)
    embed.add_field(name="Dont's", value="Try to keep RPM under 3000RPM while car is warming up \nDont go full boost until operating temp. Recommended to wait around 5-10 minutes after coolant is at operating temperature because oil warms up slower than coolant \nDont go full throttle (WOT) under 3k rpm \no not go WOT in 6th gear", inline=True)


    await interaction.response.send_message(embed=embed)

def oil_from_coolant(Tc):
    if Tc < -5 or Tc > 125:
        raise ValueError("Proper Coolant tempurature is between -5c and 125c")
    if Tc < 75:
        return Tc - 20
    progress = min(1.0, (Tc - 75) / 15)
    return (Tc - 20) * (1 - progress) + 110 * progress
def get_colour_from_coolant(coolant):
    if coolant < 75:
        return discord.Colour.blue()
    elif coolant <= 100:
        return discord.Colour.green()
    else:
        return discord.Colour.red()
@client.tree.command(name="tempurature_calculator", description="This provides a rough calculation of where you oil tempurature is related to coolant tempurature")
async def temps(interaction: discord.Interaction, coolant: float):
    try:
        oil = oil_from_coolant(coolant)
    except ValueError as e:
        await interaction.response.send_message(str(e))
        return
    await interaction.response.defer()
    embed = discord.Embed(
        title="Engine Temperatures",
        colour=get_colour_from_coolant(coolant)
    )
    embed.add_field(
        name="Coolant Temperature",
        value=f"{coolant:.1f} °C",
        inline=False
    )
    embed.add_field(
        name="Estimated Oil Temperature",
        value=f"{oil:.1f} °C",
        inline=False
    )
    if coolant < 75:
        embed.set_footer(text="Warm-up phase: oil ≈ 20°C cooler than coolant")
    elif coolant < 89:
        embed.set_footer(text="Oil warming faster as coolant reaches operating temp")
    elif coolant <110:
        embed.set_footer(text="Coolant at temp — oil approaching ~120°C")
    else:
        embed.set_footer(text="Coolant is getting hot, suggested to flush coolant or look for issues")

    await interaction.followup.send(embed=embed)


@client.event
async def on_member_remove(member):
    channel = member.guild.get_channel(706661568091389973)
    year_left = time.strftime('%d-%m-%Y')
    time_left = time.strftime('%H:%M')
    if channel:
        await channel.send(f'{year_left}\n{time_left}\n{member.name}') 
    else:
        print(f'{year_left}\n{time_left}\n{member.name}')



client.run(DEV_BOT_KEY)