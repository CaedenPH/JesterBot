import json

import disnake
from disnake.ext.commands import Cog, command, has_permissions

from core import Context, JesterBot
from core.utils import get_colour, send_embed, update_json


class Config(Cog):
    def __init__(self, bot):
        self.bot: JesterBot = bot

    async def insert_values(self, channel_id: int, channel_type: str) -> None:
        result = await self.bot.db.fetchone(
            "SELECT channel_types FROM channels_config WHERE channel_id = ?",
            (channel_id,),
        )

        if not result:
            return await self.bot.db.update(
                "INSERT INTO channels_config VALUES (?, ?)", (channel_id, channel_type)
            )

        channel_types = result[0].split(" | ")
        if channel_type in channel_types:
            return

        await self.bot.db.update(
            "UPDATE channels_config SET channel_types = ? where channel_id = ?",
            (result[0] + " | " + channel_type, channel_id),
        )

    @command()
    @has_permissions(manage_channels=True)
    async def pickupchannel(self, ctx: Context, channel: disnake.TextChannel = None):
        if not channel:
            channel = await ctx.guild.create_text_channel(name="Joke Channel")

        await self.insert_values(channel.id, "pickup")
        await send_embed(
            ctx, None, channel.mention + " now sends pickup lines on the hour!"
        )

    @command()
    @has_permissions(manage_channels=True)
    async def jokechannel(self, ctx: Context, channel: disnake.TextChannel = None):
        if not channel:
            channel = await ctx.guild.create_text_channel(name="Joke Channel")

        await self.insert_values(channel.id, "joke")
        await send_embed(ctx, None, channel.mention + " now sends jokes on the hour!")

    @command()
    @has_permissions(manage_channels=True)
    async def quotechannel(self, ctx: Context, channel: disnake.TextChannel = None):
        if not channel:
            channel = await ctx.guild.create_text_channel(name="Joke Channel")

        await self.insert_values(channel.id, "quote")
        await send_embed(ctx, None, channel.mention + " now sends quotes on the hour!")

    @command()
    @has_permissions(manage_channels=True)
    async def factchannel(self, ctx: Context, channel: disnake.TextChannel = None):
        if not channel:
            channel = await ctx.guild.create_text_channel(name="Joke Channel")

        await self.insert_values(channel.id, "fact")
        await send_embed(ctx, None, channel.mention + " now sends facts on the hour!")

    @command(
        aliases=["Welcomer", "welcome"],
        description="Adds a welcome feature into the current channel (everytime someone joins the server it says welcome) - `[message]` is a good welcome message",
    )
    @has_permissions(administrator=True)
    async def welcomechannel(
        self, ctx: Context, role: disnake.Role = "", *, message: str = ""
    ):
        with open("./dicts/Welcome.json", "r+") as f:
            data = json.load(f)
            if not role:
                data[str(ctx.guild.id)] = {
                    "message": message,
                    "name": ctx.guild.name,
                    "channel_id": ctx.channel.id,
                    "Welcome": True,
                }
                update_json(f, data)
                embed = disnake.Embed(title="Added!", colour=get_colour())
                return await ctx.reply(embed=embed)

            data[str(ctx.guild.id)] = {
                "message": message,
                "name": ctx.guild.name,
                "channel_id": ctx.channel.id,
                "role": role.id,
                "Welcome": True,
            }

            update_json(f, data)
            embed = disnake.Embed(title="Added!", colour=get_colour())
            await ctx.reply(embed=embed)

    @command(
        aliases=["Unwelcome", "Stop_Welcome"],
        description="Removes the j.welcome command",
    )
    async def remove_welcome(self, ctx: Context):
        with open("./dicts/Welcome.json", "r+") as f:
            data = json.load(f)

            if str(ctx.guild.id) in data:
                data[str(ctx.guild.id)]["Welcome"] = False
                update_json(f, data)
                embed = disnake.Embed(title="Re`moved!", colour=get_colour())
                await ctx.reply(embed=embed)

    @command(
        description="Makes the channel specified a suggestion channel - members can only type j.suggest or their message gets deleted. Nice and orderly"
    )
    @has_permissions(manage_channels=True)
    async def suggestchannel(self, ctx: Context, channel: disnake.TextChannel):
        with open("./dicts/Suggest.json", "r+") as k:
            data = json.load(k)
            if str(channel.id) not in data:
                data[str(channel.id)] = {"Yes": True}
                update_json(k, data)
                if channel.id != ctx.channel.id:
                    embed = disnake.Embed(title="Applied", colour=get_colour())
                    await ctx.reply(embed=embed)
                await channel.purge(limit=10000)
                embed1 = disnake.Embed(
                    title="Suggest",
                    description="""
                This channel is now a suggestion only channel.
                This means that you can only type `suggest`, which will formally create a ticket that only you can reply to. After giving a title and a description, your suggestion will be sent.
                Any messages that aren't `suggest` are automatically deleted
                """,
                    colour=get_colour(),
                )
                x = await channel.send(embed=embed1)
                await x.pin()
                return await channel.purge(limit=1)

            if not data[str(channel.id)]["Yes"]:
                data[str(channel.id)]["Yes"] = True
                update_json(k, data)
                embed = disnake.Embed(title="Applied", colour=get_colour())
                await ctx.reply(embed=embed)
            else:
                embed = disnake.Embed(title="Already applied", colour=get_colour())
                await ctx.reply(embed=embed)

    @command(
        aliases=["verify"],
        description="""
    Creates a channel/uses an existing channel to make the server be secure by adding the need to say `verify` to access the server...Remove with `j.removeverify`
    1. If channel is not given, this command will create a role called `⚘ Member ⚘` and a role called `⚘ Unverified ⚘`
    2. It will create a channel called `⚘ verify ⚘`
    3. When a new member joins they will only see the channel `⚘ verify ⚘`, and if they write `verify` they can text in and see all other channels""",
    )
    @has_permissions(administrator=True)
    async def verifychannel(
        self, ctx: Context, channel: disnake.TextChannel = None, role: disnake.Role = ""
    ):
        embed = disnake.Embed(
            title="Warning",
            description="While this command can help your server by adding a verification, it can also add roles and channels you may not like the look of. To get more information type `j.help verifychannel`. To proceed type y",
            colour=get_colour(),
        )
        await ctx.reply(embed=embed)
        received_msg = str(
            (
                await self.bot.wait_for(
                    "message",
                    timeout=60.0,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                )
            ).content
        ).lower()
        if received_msg != "y":
            embed = disnake.Embed(title="Goodbye!", colour=get_colour())
            return await ctx.reply(embed=embed)

        with open("./dicts/VerifyChannel.json") as k:
            data = json.load(k)

            for key in data:
                if "Yes" in data[key]:
                    if data[key]["Yes"]:
                        if data[key]["Guild"] == ctx.guild.id:
                            return await ctx.reply("There is already a verify here!")
        if not channel:
            channel = await ctx.guild.create_text_channel(name="⚘ verify ⚘")
        with open("./dicts/VerifyChannel.json", "r+") as k:
            if role is None:
                await ctx.guild.create_role(
                    name="⚘ Member ⚘",
                    permissions=disnake.Permissions(send_messages=True),
                )
            membrole = disnake.utils.get(ctx.guild.roles, name="⚘ Member ⚘")
            await ctx.guild.create_role(
                name="⚘ Unverified ⚘",
                permissions=disnake.Permissions(send_messages=False),
            )
            Urole = disnake.utils.get(ctx.guild.roles, name="⚘ Unverified ⚘")
            for x in ctx.guild.channels:
                if x.id == channel.id:
                    await x.set_permissions(
                        membrole,
                        send_messages=False,
                        read_message_history=False,
                        read_messages=False,
                    )
                else:
                    await x.set_permissions(
                        membrole,
                        speak=True,
                        send_messages=True,
                        read_message_history=True,
                        read_messages=True,
                    )
                if x.id != channel.id:
                    await x.set_permissions(
                        Urole,
                        send_messages=False,
                        read_message_history=False,
                        read_messages=False,
                    )
                else:
                    await x.set_permissions(
                        Urole,
                        speak=True,
                        send_messages=True,
                        read_message_history=True,
                        read_messages=True,
                    )

            every = disnake.utils.get(ctx.guild.roles, name="@everyone")
            for y in ctx.guild.channels:
                await y.set_permissions(
                    every,
                    speak=True,
                    send_messages=True,
                    read_message_history=True,
                    read_messages=True,
                )
            with open("./dicts/Welcome.json") as w:
                weldata = json.load(w)
                if str(ctx.guild.id) in weldata:
                    g = disnake.utils.get(
                        ctx.guild.roles, id=weldata[str(ctx.guild.id)]["role"]
                    )
                    for z in ctx.guild.channels:
                        if z.id == channel.id:
                            await z.set_permissions(
                                g,
                                send_messages=False,
                                read_message_history=False,
                                read_messages=False,
                            )
                        else:
                            await z.set_permissions(
                                g,
                                speak=True,
                                send_messages=True,
                                read_message_history=True,
                                read_messages=True,
                            )

            data = json.load(k)
            if str(channel.id) in data:
                embed = disnake.Embed(title="Already applied!")
            else:
                data[str(channel.id)] = {
                    "Yes": True,
                    "MRole id": membrole.id,
                    "URole id": Urole.id,
                    "Guild": ctx.guild.id,
                }

            update_json(k, data)

            await channel.purge(limit=10000)
            embed1 = disnake.Embed(
                title="Verify",
                description="""
            This channel is a verify channel.
            Type `verify` to get acess to the server!
            Have fun and make sure to follow the rules.
            """,
                colour=get_colour(),
            )
            x = await channel.send(embed=embed1)
            await x.pin()
            embed = disnake.Embed(title="Applied!")
            await ctx.reply(embed=embed)
            await channel.purge(limit=1)

    @command(aliases=["remverify"], description="removes the need for a verification")
    @has_permissions(administrator=True)
    async def removeverify(self, ctx: Context):
        with open("./dicts/VerifyChannel.json", "r+") as k:
            data = json.load(k)
            for key in data:
                if data[key]["Guild"] == ctx.guild.id:
                    del data[key]
                    update_json(k, data)
                    embed = disnake.Embed(title="Removed!", colour=get_colour())
                    return await ctx.reply(embed=embed)

            await send_embed(ctx, "There was never a verify!")

    @command()
    async def leavechannel(self, ctx: Context, channel: disnake.TextChannel = None):
        with open("./dicts/LeaveChannel.json", "r+") as k:
            data = json.load(k)
            if str(ctx.guild.id) in data:
                return await send_embed(
                    ctx, "Leaving", "This server is already registered!"
                )
            else:
                if not channel:
                    channel = await ctx.guild.create_text_channel(
                        name="Leaving Channel"
                    )
                data[str(ctx.guild.id)] = {"id": channel.id}
                update_json(k, data)
        await send_embed(
            channel,
            "This is a leaving channel, everyone who leaves will be announced here...",
        )

    @command()
    async def removeleavechannel(self, ctx: Context, channel: disnake.TextChannel):
        with open("./dicts/LeaveChannel.json", "r+") as k:
            data = json.load(k)
            if str(ctx.guild.id) not in data:
                return await send_embed(
                    ctx, "Leaving", "There was never a leaving channel here!"
                )
            del data[str(ctx.guild.id)]
            await send_embed(ctx, "Done!")

    @Cog.listener()
    async def on_member_remove(self, memb):
        with open("./dicts/LeaveChannel.json", "r+") as k:
            data = json.load(k)

            if str(memb.guild.id) in data:
                channel = self.bot.get_channel(data[str(memb.guild.id)]["id"])
                await send_embed(
                    channel, "Goodbye", f"You wil be missed *{memb.name}*..."
                )


def setup(bot):
    bot.add_cog(Config(bot))
