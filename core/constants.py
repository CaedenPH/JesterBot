## environ

from asyncpraw import Reddit
from os import environ
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = environ["BOT_TOKEN"]
WEATHER_KEY = environ["WEATHER_KEY"]
COORDS_KEY = environ["COORDS_KEY"]
CHATBOT_KEY = environ["CHATBOT_KEY"]
RAPID_API_KEY = environ["RAPID_API_KEY"]
GOOGLE_KEY = environ["GOOGLE_KEY"]

CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
USERNAME = environ["REDDIT_USERNAME"]
PASSWORD = environ["PASSWORD"]
USER_AGENT = environ["USER_AGENT"]


## reddit

REDDIT = Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD,
)


## emojis

THUMBS_UP = "👍"
THUMBS_DOWN = "👎"
CONFETTI = "🎊"
CLOSED_LOCK = "🔐"
BOOM = "💥"
HANDSHAKE = "🤝"
BOMB = "💣"
BLUE_SQUARE = "🟦"
GOLF = "⛳"
RED_FLAG = "🚩"
SPOON = "🥄"

NUMBERS = {
    0: "0️⃣",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
}

## custom emojis

LOCATION_EMOJIS = {
    "fastbackwards": "<:fast_forward_left:870781340692402226>",
    "backwards": "<:left_arrow:870781340990197860>",
    "close": "<:Cross:863313854069997578>",
    "forwards": "<:right_arrow:870781340314898473>",
    "fastforwards": "<:fast_forward_right:870781340839202837>",
}
COG_EMOJIS = {
    "JesterInfo": 863075610048987166,
    "Feedback": 863075610851147777,
    "Music": 863075611320647719,
    "Snipe": 863075611269791794,
    "Fun": 863075609781075968,
    "Mod": 863075610784301068,
    "Games": 863075611329167380,
    "Utils": 863075611161788478,
    "Images": 863075611277656124,
    "Economy": 863075610913800233,
    "Misc": 863075610979729409,
    "Levels": 863075611182628895,
    "Config": 863075611169259550,
    "Love": 863075611374125056,
    "JesterJokes": 873327129016811528,
    "Countries": 872473402638762025,
    "ChatBot": 872473402693259324,
    "DiscordTogether": 872473402840076288,
    "UrbanDictionary": 924074967673503796,
    "Random": 924074967405051965,
    "Trivia": 924152372001910834,
    "Crime": 924411072729985046,
    "Docs": 925222917946605629,
}

CLOSE = "<:Cross:863313854069997578>"
HOME = "<:Arrow:863313854040506379>"
LINK = "<:links:870781340700782612>"
CATEGORIES = "<:menus:870781340746932225>"
TRASHCAN = "<:trashbin:873564727006089287>"
LOADING = "<a:loading_grey:942386360877219881>"

_J = "<:J_:863313855286607932>"
_E = "<:E_:863313854150606848>"
_S = "<:S:863313855061164062>"
_T = "<:T:863313855399329812>"
_R = "<:R_:863313855119360022>"


## game

CARD_SUITS = {
    "hearts": "♥️",
    "diamonds": "♦️",
    "clubs": "♣️",
    "spades": "♠️",
}
BLACKJACK_WELCOME = """```yaml
Welcome to the blackjack game. 
==============================

It is recommended that you research the rules to familiarize yourself how the game is played.```
"""
BLACKJACK_HOW_TO = """```yaml
How to play blackjack
=====================x

Start
-----
• When you play you will get a hand with 2 cards.
• If you get an ace you can choose it's value to be 1 or 11. 
• All face cards are equal to 10 this includes; King, Queen and Jack.

Game over
---------
• The player who's card's overall score is closer to 21 wins.
• The game ends when you stand.```
"""
HANGMAN = [
    "",
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
    """

  +---+   _   _  _____   ____   ___  _____  ____
  |   |  | | | || ____| |  _ \ |_ _|| ____||  _ \
  O   |  | |_| ||  _|   | | | | | | |  _|  | | | |
 /|\  |  |  _  || |___  | |_| | | | | |___ | |_| |
 / \  |  |_| |_||_____| |____/ |___||_____||____/
      |
=========""",
][::-1]
MINESWEEPER_MESSAGE = """
Board size : {board_size}x{board_size}
Bomb count : {bomb_count}
"""

## utils

TEXT_TO_MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ",": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
    ":": "---...",
    "'": ".----.",
    "’": ".----.",
    '"': ".-..-.",
    " ": ".......",
    "!": "-.-.--",
    "@": ".--.-.",
    "$": "...-..-",
    "&": ".-...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "_": "..--.-",
}

MORSE_TO_TEXT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
    "--..--": ",",
    ".-.-.-": ".",
    "..--..": "?",
    "-..-.": "/",
    "-....-": "-",
    "-.--.": "(",
    "-.--.-": ")",
    "---...": ":",
    ".----.": "'",
    ".-..-.": '"',
    ".......": " ",
    "-.-.--": "!",
    ".--.-.": "@",
    "...-..-": "$",
    ".-...": "&",
    "-.-.-.": ";",
    "-...-": "=",
    ".-.-.": "+",
    "..--.-": "_",
}
ASCII_DESCRIPTION = """ASCII was developed from telegraph code. Work on the ASCII standard began in May 1961. The first edition of the standard was published in 1963. Compared to earlier telegraph codes, the proposed Bell code and ASCII were both ordered for more convenient sorting (i.e., alphabetization) of lists.

The use of ASCII format for Network Interchange was described in 1969. That document was formally elevated to an Internet Standard in 2015.

Originally based on the English alphabet, ASCII encodes 128 specified characters into seven-bit integers as shown by the ASCII chart above. Ninety-five of the encoded characters are printable: these include the digits 0 to 9, lowercase letters a to z, uppercase letters A to Z, and punctuation symbols. 

For example, lowercase i would be represented in the ASCII encoding by binary 1101001 = hexadecimal 69 (i is the ninth letter) = decimal 105.
To get the ascii table type j.ascii

Source: [Website](https://en.wikipedia.org/wiki/ASCII)
    """


## docs

ZEN_OF_PYTHON = """\
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""

# cog

COG_DESCRIPTIONS = {
    "Fun": "Fun commands which have no purpose nor goal other than to be fun! You can even hack your friends!",
    "Games": "Play fun games with the bot or with other members, who doesnt love a game of blackjack against an ai?",
    "Mod": "A moderators dream, useful commands that no other bots offer - God in the palm of your hand",
    "Misc": "Random commands that cannot be categorized, not 'useless' commands, but like... hint is in the name",
    "JesterInfo": "Information about JesterBot, for example - do you want to see the most popular commands?",
    "Economy": "Interact with JesterBot's economy...With commands such as beg and bet you can become a rich person",
    "Utils": "Utility commands which may have a use; such as timezone - google has it but wheres the fun in that?",
    "Images": "All image commands, such as cute pictures of cats and dogs and more! Type ^help image for more info",
    "Config": "Configure your server with jester commands such as welcome and auto-verification",
    "JesterJokes": "JesterBot is truly a comedian, ask him about his latest joke hand?",
    "Love": "Want to make a family? Want to test the compatability? JesterLove has all the commands!",
    "Music": "Got a song in your head that you need to listen to? JesterBot's music category has all the musical needs",
    "Snipe": "Snipe messages or edited messages with JesterBot snipe commands!",
    "Levels": "Beat all of your friends in a race to activiness on your server, because, well, flexing rights!",
    "Feedback": "Send feedback to the developer",
    "Countries": "Get information about every country in the world!",
    "DiscordTogether": "PLay an amazing game night on a call with all your friends!",
    "UrbanDictionary": "Want to look up that kink you've been wondering about? Do it with urbandictionary!",
    "Random": "Just a selection of commands that implement randomness - a bunch of random apis",
    "Trivia": "Test your knowledge in specific commands or just general commands",
    "Crime": "Get information about all the latest criminal activities - all fact-checked through official apis like the fbi",
    "ChatBot": "Are you sad and lonely? Talk to the bot and get a wonderful insight of how a bot thinks!",
    "Docs": "Read up on the latest python documentation and rtfm commands. Great for helping people and quick searches",
}
