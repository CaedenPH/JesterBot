import disnake
import math
import random
import io

from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands

from core.bot import JesterBot
from core.constants import THUMBS_UP
from core.utils.utils import get_colour


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot: JesterBot = bot

    async def find_or_insert_user(self, member: disnake.Member):
        result = await self.bot.db.fetchone(
            "Select * from users where user_id = ? and guild_id = ?",
            (
                member.id,
                member.guild.id,
            ),
        )
        if result is None:
            result = (member.id, member.guild.id, 0, 0, member.display_name)
            await self.bot.update("Insert into users values(?, ?, ?, ?, ?)", result)
        return result

    async def rankup(self, level, member):
        result = await self.bot.db.fetchone(
            "Select * from levels_config where guild_id = ?", (member.guild.id,)
        )

        chan, message = None, None
        if result is not None:
            guild, chan, ping = result
            if ping == "Yes":
                message = f"Well done {member.mention}! You ranked up to {level}"
            else:
                message = f"Well done {member}! You ranked up to {level}"
        return chan, message

    def calculate_xp(self, level):
        return 100 * (level ** 2)

    def calculate_level(self, xp):
        return round(0.1 * math.sqrt(xp))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot is True or message.guild is None:
            return

        result = await self.find_or_insert_user(message.author)
        user_id, guild_id, xp, level, name = result

        xp += random.randint(10, 40)

        if self.calculate_level(xp) > level:
            level += 1
            sendmessage = await self.rankup(level, message.author)
            if sendmessage[1] is not None:
                channel = self.bot.get_channel(sendmessage[0])
                await channel.send(sendmessage[1])

        await self.bot.db.update(
            "Update users set xp=?, level=? where user_id=? and guild_id=?",
            (xp, level, user_id, guild_id),
        )

    async def make_rank_image(self, member: disnake.Member, rank, level, xp, final_xp):
        user_avatar_image = str(member.avatar.with_format("png").with_size(512))
        async with self.bot.client.get(user_avatar_image) as resp:
            avatar_bytes = io.BytesIO(await resp.read())

        img = Image.new("RGB", (1000, 240))
        logo = Image.open(avatar_bytes).resize((200, 200))

        # Stack overflow helps :)
        bigsize = (logo.size[0] * 3, logo.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(logo.size, Image.ANTIALIAS)
        logo.putalpha(mask)
        ##############################
        img.paste(logo, (20, 20), mask=logo)

        # Black Circle
        draw = ImageDraw.Draw(img, "RGB")
        draw.ellipse((152, 152, 208, 208), fill="#000")

        # Placing offline or Online Status
        # Discord Colors (Online: '#43B581')
        draw.ellipse((155, 155, 205, 205), fill="#43B581")
        ##################################

        # Working with fonts
        big_font = ImageFont.FreeTypeFont("./core/utils/font/ABeeZee-Regular.otf", 60)
        medium_font = ImageFont.FreeTypeFont(
            "./core/utils/font/ABeeZee-Regular.otf", 40
        )
        small_font = ImageFont.FreeTypeFont("./core/utils/font/ABeeZee-Regular.otf", 30)

        # Placing Level text (right-upper part)
        text_size = draw.textsize(f"{level}", font=big_font)
        offset_x = 1000 - 15 - text_size[0]
        offset_y = 5
        draw.text((offset_x, offset_y), f"{level}", font=big_font, fill="#11ebf2")
        text_size = draw.textsize("LEVEL", font=small_font)

        offset_x -= 5 + text_size[0]
        offset_y = 35
        draw.text((offset_x, offset_y), "LEVEL", font=small_font, fill="#11ebf2")

        # Placing Rank Text (right upper part)
        text_size = draw.textsize(f"#{rank}", font=big_font)
        offset_x -= 15 + text_size[0]
        offset_y = 8
        draw.text((offset_x, offset_y), f"#{rank}", font=big_font, fill="#fff")

        text_size = draw.textsize("RANK", font=small_font)
        offset_x -= 5 + text_size[0]
        offset_y = 35
        draw.text((offset_x, offset_y), "RANK", font=small_font, fill="#fff")

        # Placing Progress Bar
        # Background Bar
        bar_offset_x = logo.size[0] + 20 + 100
        bar_offset_y = 160
        bar_offset_x_1 = 1000 - 50
        bar_offset_y_1 = 200
        circle_size = bar_offset_y_1 - bar_offset_y

        # Progress bar rect greyier one
        draw.rectangle(
            (bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175"
        )
        # Placing circle in progress bar

        # Left circle
        draw.ellipse(
            (
                bar_offset_x - circle_size // 2,
                bar_offset_y,
                bar_offset_x + circle_size // 2,
                bar_offset_y + circle_size,
            ),
            fill="#727175",
        )

        # Right Circle
        draw.ellipse(
            (
                bar_offset_x_1 - circle_size // 2,
                bar_offset_y,
                bar_offset_x_1 + circle_size // 2,
                bar_offset_y_1,
            ),
            fill="#727175",
        )

        # Filling Progress Bar

        bar_length = bar_offset_x_1 - bar_offset_x
        # Calculating of length
        # Bar Percentage (final_xp - current_xp)/final_xp

        # Some variables
        progress = (final_xp - xp) * 100 / final_xp
        progress = 100 - progress
        progress_bar_length = round(bar_length * progress / 100)
        pbar_offset_x_1 = bar_offset_x + progress_bar_length

        # Drawing Rectangle
        draw.rectangle(
            (bar_offset_x, bar_offset_y, pbar_offset_x_1, bar_offset_y_1),
            fill="#11ebf2",
        )
        # Left circle
        draw.ellipse(
            (
                bar_offset_x - circle_size // 2,
                bar_offset_y,
                bar_offset_x + circle_size // 2,
                bar_offset_y + circle_size,
            ),
            fill="#11ebf2",
        )
        # Right Circle
        draw.ellipse(
            (
                pbar_offset_x_1 - circle_size // 2,
                bar_offset_y,
                pbar_offset_x_1 + circle_size // 2,
                bar_offset_y_1,
            ),
            fill="#11ebf2",
        )

        def convert_int(integer):
            integer = round(integer / 1000, 2)
            return f"{integer}K"

        # Drawing Xp Text
        text = f"/ {convert_int(final_xp)} XP"
        xp_text_size = draw.textsize(text, font=small_font)
        xp_offset_x = bar_offset_x_1 - xp_text_size[0]
        xp_offset_y = bar_offset_y - xp_text_size[1] - 10
        draw.text((xp_offset_x, xp_offset_y), text, font=small_font, fill="#727175")

        text = f"{convert_int(xp)} "
        xp_text_size = draw.textsize(text, font=small_font)
        xp_offset_x -= xp_text_size[0]
        draw.text((xp_offset_x, xp_offset_y), text, font=small_font, fill="#fff")

        # Placing User Name
        text = member.display_name
        text_size = draw.textsize(text, font=medium_font)
        text_offset_x = bar_offset_x - 10
        text_offset_y = bar_offset_y - text_size[1] - 10
        draw.text((text_offset_x, text_offset_y), text, font=medium_font, fill="#fff")

        # Placing Discriminator
        text = f"#{member.discriminator}"
        text_offset_x += text_size[0] + 10
        text_size = draw.textsize(text, font=small_font)
        text_offset_y = bar_offset_y - text_size[1] - 10
        draw.text((text_offset_x, text_offset_y), text, font=small_font, fill="#727175")

        bytes = io.BytesIO()
        img.save(bytes, "PNG")
        bytes.seek(0)
        return bytes

    @commands.command()
    async def rank(self, ctx: commands.Context, member: disnake.Member = None):
        member = member or ctx.author
        user = await self.find_or_insert_user(member)
        user_id, guild_id, xp, level, name = user

        result = await self.bot.db.fetchone(
            "Select Count(*) from users where xp > ? and guild_id=?", (xp, guild_id)
        )
        rank = result[0] + 1
        final_xp = self.calculate_xp(level + 1)

        bytes = await self.make_rank_image(member, rank, level, xp, final_xp)
        await ctx.reply(file=disnake.File(bytes, "rank.png"))

    @commands.command(aliases=["conf"])
    async def levelsconfig(self, ctx: commands.Context):
        result = await self.bot.db.fetchone("Select * from levels_config where guild_id = ?", (ctx.guild.id,))

        if result is None:
            await ctx.reply(
                "What channel would you like the rankup messages to be in? Type No to not have a rankup message channel"
            )

            channel_msg = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )

            while not channel_msg.raw_channel_mentions and channel_msg.content != "No":

                await ctx.reply(
                    "Please ping the channel you would like to send the message in. An example is <#{}>".format(
                        ctx.channel.id
                    )
                )

                channel_msg = await self.bot.wait_for(
                    "message", check=lambda m: m.author == ctx.author
                )

            await channel_msg.add_reaction(THUMBS_UP)
            await ctx.reply(
                "Would you like the bot to ping after every rankup message? Type No to not ping on rankup, and Yes to ping."
            )

            ping = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )

            while ping.content not in ["No", "Yes"]:

                await ctx.reply("Type No to not ping on rankup, and Yes to ping.")
                ping = await self.bot.wait_for(
                    "message", check=lambda m: m.author == ctx.author
                )

            await ping.add_reaction(THUMBS_UP)

            result = (ctx.guild.id, channel_msg.raw_channel_mentions[0], ping.content)
            chan = self.bot.get_channel(channel_msg.raw_channel_mentions[0])

            embed = disnake.Embed(
                title=f"Config channel for {ctx.guild.name}"
            ).add_field(
                name="\u200b", value=f"**Channel:** {chan}\n**Ping:** {ping.content}"
            )

            await self.bot.db.update("Insert into levels_config values(?, ?, ?)", result)
            return await ctx.reply(embed=embed)

        await ctx.reply(
            embed=disnake.Embed(
                description="You already have a config!", colour=get_colour()
            ).set_author(name="Config", icon_url=ctx.author.avatar.url)
        )

    @commands.command(aliases=["vconf"])
    async def viewconfig(self, ctx: commands.Context):
        result = await self.bot.db.fetchone("Select * from levels_config where guild_id = ?", (ctx.guild.id,))

        if result is not None:
            config = f"""
**Server id:** `{result[0]}`,
**RankupChannel id:** `{result[1]}`,
**Ping:**`{result[2]}`
            """
        await ctx.reply(config if result is not None else "no config")

    @commands.command(aliases=["rconf"])
    async def removeconfig(self, ctx: commands.Context):
        await self.bot.db.execute("Delete from levels_config where guild_id = ?", (ctx.guild.id,))
        await ctx.reply("Deleted all rankup config messages")

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx: commands.Context):
        embed = disnake.Embed(colour=get_colour())
        embed.set_author(name="Leaderboard", icon_url=ctx.author.avatar.url)

        result = await self.bot.db.fetchall(
            "SELECT user_id, xp, level, name FROM users WHERE guild_id = ? ORDER BY xp ASC",
            (ctx.guild.id,),
        )

        desc = ""
        for k, value in enumerate(result[::-1], start=1):
            desc += f"\n**{k}.** {value[3]}: level **{value[2]}**"
            if k == 10:
                break

        embed.description = desc
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Levels(bot))
