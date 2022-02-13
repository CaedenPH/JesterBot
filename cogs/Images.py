import disnake
import requests
import aiohttp
import PIL
import vacefron
import cv2 as cv

from disnake.ext import commands
from animals import Animals

from core.utils import get_colour
from core import Context


vace_api = vacefron.Client()


async def img(ctx, member, name):
    await ctx.trigger_typing()

    if member is None:
        member = ctx.author

    url = member.avatar.url

    if member.avatar.is_animated():
        url = member.avatar.url.replace(".gif", ".png")

    async with ctx.bot.client.get(str(url)) as r:
        f = open(f"./images/{name}.png", "wb")
        f.write(await r.read())
        f.close()

    return f"./images/{name}.png"


async def pilimg(ctx, member, name):
    await ctx.trigger_typing()

    if member is None:
        member = ctx.author

    url: str = member.avatar.url

    if member.avatar.is_animated():
        url: str = str(member.avatar.url).replace(".gif", ".webp")

    path = f"./images/{name}.png"
    async with ctx.bot.client.get(url) as r:
        f = open(path, "wb")
        f.write(await r.read())
        f.close()

    with PIL.Image.open(path) as im:
        return im, path


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sharp(self, ctx, sharpness: float = 10, member: disnake.Member = None):
        x = await pilimg(ctx, member, "sharp")
        enhancer = PIL.ImageEnhance.Sharpness(x[0])
        enhancer.enhance(sharpness)
        enhancer.image.save(x[1])
        await ctx.send(file=disnake.File(x[1]))

    @commands.command()
    async def enhance(self, ctx, factor: float, member: disnake.Member = None):
        x = await pilimg(ctx, member, "contrast")
        enhancer = PIL.ImageEnhance._Enhance()
        enhancer.enhance(factor)
        enhancer.image.save(x[1])
        await ctx.send(file=disnake.File(x[1]))

    @commands.command()
    async def contrast(self, ctx, factor: float, member: disnake.Member = None):
        x = await pilimg(ctx, member, "contrast")
        enhancer = PIL.ImageEnhance.Contrast(x[0])
        enhancer.enhance(factor)
        enhancer.image.save(x[1])
        await ctx.send(file=disnake.File(x[1]))

    @commands.command()
    async def brightness(self, ctx, factor: float, member: disnake.Member = None):
        x = await pilimg(ctx, member, "brightness")
        enhancer = PIL.ImageEnhance.factor(x[0])
        enhancer.enhance(factor)
        enhancer.image.save(x[1])
        await ctx.send(file=disnake.File(x[1]))

    @commands.command(aliases=["change", "changemind", "change_my_mind"])
    async def mindchange(self, ctx: Context, *, text: str = None):
        async with ctx.typing():
            embed = disnake.Embed(title="Change my mind...", colour=get_colour())
            x = await vace_api.change_my_mind(text)
            embed.set_image(url=x.url)

            await ctx.send(embed=embed)

    @commands.command()
    async def nasapic(self, ctx: Context):
        async with self.bot.client.get(
            url="https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=1"
        ) as response:
            up = await response.json()

        embed = disnake.Embed(
            title="Nasapic",
            description=f"""
        **date:** {up[0]['date']} │
        **explanation:** {up[0]['explanation']}
        """,
            colour=get_colour(),
        )
        embed.set_image(url=up[0]["hdurl"])
        await ctx.send(embed=embed)

    @commands.command()
    async def rover(self, ctx: Context):
        key2 = "dS9ecIIo07Q0gGLYXnCoJW6uCAKwDM9j0UnYbVre"
        async with self.bot.client.get(
            "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key={}".format(
                key2
            )
        ) as resp:
            response = await resp.json()
            await ctx.send(response)

    @commands.command(aliases=["rpic", "randpic"])
    async def randompicture(self, ctx: Context):
        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://source.unsplash.com/random"
            ) as response:
                my_file = open("./images/random.png", "wb")
                my_file.write(await response.read())
                my_file.close()

        await ctx.send(file=disnake.File("./images/random.png"))

    @commands.command(description="Covert Code Block to Snippet")
    async def code_snippet(self, ctx: commands.Context, *, code: str):
        if not code.startswith("```") and code.endswith("```"):
            return await ctx.em("Your code needs to be in a codeblock!")

        code_edited = disnake.utils.remove_markdown(code.strip()).strip()
        async with aiohttp.ClientSession(
            headers={"Content-Type": "application/json"},
        ) as ses:
            try:
                request = await ses.post(
                    f"https://carbonara-42.herokuapp.com/api/cook",
                    json={
                        "code": code_edited,
                    },
                )
            except Exception as e:
                print(f"Exception: {e}")
            resp = await request.read()

        with open("images/code_snippet.png", "wb") as f:
            f.write(resp)

        await ctx.send(file=disnake.File("./images/code_snippet.png"))

    @commands.command(description="""Sends a wasted filtered avatar""")
    async def wasted(self, ctx: Context, member: disnake.Member = None):

        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/wasted?avatar={avatar}"
            ) as response:

                file = open("./images/wasted.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/wasted.png"))

    @commands.command(description="""Sends a wasted filtered avatar""")
    async def threshold(self, ctx: Context, member: disnake.Member = None):

        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/threshold/?avatar={avatar}"
            ) as response:

                file = open("./images/threshold.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/threshold.png"))

    @commands.command(description="""Sends a fay filtered avatar""")
    async def gay(self, ctx: Context, member: disnake.Member = None):
        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/gay?avatar={avatar}"
            ) as response:

                file = open("./images/gay.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/gay.png"))

    @commands.command(description="""Sends a glass filtered avatar""")
    async def glass(self, ctx: Context, member: disnake.Member = None):
        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/glass?avatar={avatar}"
            ) as response:

                file = open("./images/glass.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/glass.png"))

    @commands.command(description="""Sends a triggered filtered avatar""")
    async def triggered(self, ctx: Context, member: disnake.Member = None):
        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/triggered?avatar={avatar}"
            ) as response:

                file = open("./images/triggered.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/triggered.png"))

    @commands.command(description="""Sends a bloody filtered avatar""")
    async def bloody(self, ctx: Context, member: disnake.Member = None):
        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/red?avatar={avatar}"
            ) as response:

                file = open("./images/bloody.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/bloody.png"))

    @commands.command(
        description="""Sends a YouTube comment with your custom comment"""
    )
    async def ytcomment(self, ctx: Context, *, comment):
        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar.with_format('png')}&comment={comment}&username={ctx.author.display_name}"
            ) as response:

                file = open("./images/yt-comment.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/yt-comment.png"))

    @commands.command(description="""Makes a bright filtered avatar""")
    async def bright(self, ctx: Context, member: disnake.Member = None):
        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/brightness?avatar={avatar}"
            ) as response:

                file = open("./images/brightness.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/brightness.png"))

    @commands.command(description="""Makes a bright filtered avatar""")
    async def invert(self, ctx: Context, member: disnake.Member = None):
        if member is None:
            avatar = ctx.author.avatar.with_format("png")
        else:
            avatar = member.avatar.with_format("png")

        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/invert?avatar={avatar}"
            ) as response:

                file = open("./images/invert.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/invert.png"))

    @commands.command(description="""Makes a bright filtered avatar""")
    async def viewcolor(self, ctx: Context, hexcolor):
        async with ctx.typing():
            async with self.bot.client.get(
                url=f"https://some-random-api.ml/canvas/colorviewer?hex={hexcolor}"
            ) as response:

                file = open("./images/color.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/color.png"))

    @commands.command(aliases=["pic", "imag", "images", "image"])
    async def picture(self, ctx: Context, *, pic):
        async with ctx.typing():
            async with self.bot.client.get(
                "https://source.unsplash.com/1600x900/?{}".format(pic)
            ) as response:

                my_file = open("./images/picture.png", "wb")
                my_file.write(await response.read())
                my_file.close()

        await ctx.send(file=disnake.File("./images/picture.png"))

    @commands.command(
        invoke_without_command=True,
        description="Sends certain images of animals such as `dog`, `fox`, `cat`, to get the full list type `j.image`",
        aliases=["animalpic", "animage"],
    )
    async def animalimage(self, ctx: Context, imag=""):

        if imag not in ["cat", "dog", "panda", "koala", "fox", "racoon", "kangaroo"]:
            embed = disnake.Embed(
                title=f"{imag} is not a valid option" if imag else "Options",
                description="Valid Options are `cat`, `dog`, `panda`, `koala`, `fox`, `racoon`, `kangaroo`",
                colour=get_colour(),
            )
            return await ctx.send(embed=embed)

        async with ctx.typing():

            animal = Animals(imag)

            embed = disnake.Embed(
                title=f"Here is your {imag}",
                description=f"**Fact:**\n{animal.fact()}",
                colour=get_colour(),
            )
            embed.set_image(url=animal.image())
        await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx, member: disnake.Member = None):
        x = await img(ctx, member, "flip")

        image = cv.imread(x)

        flip = cv.flip(image, 1)
        cv.imwrite(x, flip)
        await ctx.send(file=disnake.File(x))

    @commands.command()
    async def rotate(self, ctx, degrees: float = -180, member: disnake.Member = None):
        await img(ctx, member, "rotate")

        image = cv.imread("./images/rotate.png")
        h, w = image.shape[:2]

        rotation_matrix = cv.getRotationMatrix2D((w / 2, h / 2), degrees, 1)

        rotated_image = cv.warpAffine(image, rotation_matrix, (w, h))
        cv.imwrite("./images/rotate.png", rotated_image)
        await ctx.send(file=disnake.File("./images/rotate.png"))

    @commands.command(aliases=["pixel"])
    async def pixelate(self, ctx, member: disnake.Member = None):
        await img(ctx, member, "pixel")

        image = cv.imread("./images/pixel.png")
        image_scaled = cv.resize(image, None, fx=0.15, fy=0.15)
        image_scaled = cv.resize(image_scaled, (400, 400))
        cv.imwrite("./images/pixel.png", image_scaled)
        await ctx.send(file=disnake.File("./images/pixel.png"))

    @commands.command()
    async def bill(self, ctx: Context):
        async with ctx.typing():
            async with self.bot.client.get(
                "https://belikebill.ga/billgen-API.php?default=1", verify=False
            ) as response:

                file = open("./images/bill.png", "wb")
                file.write(await response.read())
                file.close()

        await ctx.send(file=disnake.File("./images/bill.png"))


def setup(bot):
    bot.add_cog(Images(bot))
