import disnake
import re
import os
import io
import zlib

from . import fuzzy


class Colours:
    white = 0xFFFFFF
    blue = 0x0279FD
    bright_green = 0x01D277
    dark_green = 0x1F8B4C
    orange = 0xE67E22
    pink = 0xCF84E0
    purple = 0xB734EB
    soft_green = 0x68C290
    soft_orange = 0xF9CB54
    soft_red = 0xCD6D6D
    yellow = 0xF9F586
    python_blue = 0x4B8BBE
    python_yellow = 0xFFD43B
    grass_green = 0x66FF00
    gold = 0xE6C200


class SphinxObjectFileReader:
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode("utf-8")

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b""
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b"\n")
            while pos != -1:
                yield buf[:pos].decode("utf-8")
                buf = buf[pos + 1 :]
                pos = buf.find(b"\n")


class RTFM:
    def parse_object_inv(self, stream, url):
        result = {}
        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]  # noqa

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError("Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            (name, directive, prio, location, dispname) = match.groups()
            (domain, _, subdirective) = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            if projname == "disnake":
                key = key.replace("disnake.ext.commands.", "").replace("disnake.", "")

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for (key, page) in page_types.items():
            cache[key] = {}
            async with self.bot.client.get(page + "/objects.inv") as resp:
                if resp.status != 200:
                    raise RuntimeError("Cannot build rtfm lookup table, try again later.")

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._rtfm_cache = cache

    async def do_rtfm(self, ctx, key, obj):
        page_types = {
            "latest": "https://disnake.readthedocs.io/en/latest",
            "python": "https://docs.python.org/3",
        }

        if not hasattr(self, "_rtfm_cache"):
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r"^(?:disnake\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)

        if key.startswith("latest"):
            q = obj.lower()
            for name in dir(disnake.abc.Messageable):
                if name[0] == "_":
                    continue
                if q == name:
                    obj = f"abc.Messageable.{name}"
                    break

        cache = list(self._rtfm_cache[key].items())
        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        e = disnake.Embed(colour=disnake.Colour.blurple())
        if len(matches) == 0:
            return await ctx.em("Could not find anything. Sorry.")

        e.description = "\n".join(f"[`{key}`]({url})" for key, url in matches)
        await ctx.reply(embed=e)
