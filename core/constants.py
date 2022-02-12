from os import environ
from dotenv import load_dotenv

load_dotenv()

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

_J = "<:J_:863313855286607932>"
_E = "<:E_:863313854150606848>"
_S = "<:S:863313855061164062>"
_T = "<:T:863313855399329812>"
_R = "<:R_:863313855119360022>"

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

BOT_TOKEN = environ["BOT_TOKEN"]
WEATHER_KEY = environ["WEATHER_KEY"]
POLICE_KEY = environ["POLICE_KEY"]
COORDS_KEY = environ["COORDS_KEY"]
CHATBOT_KEY = environ["CHATBOT_KEY"]
RAPID_API_KEY = environ["RAPID_API_KEY"]

CARD_SUITS = {
  'hearts': '♥️',
  'diamonds': '♦️',
  'clubs': '♣️',
  'spades': '♠️',
}
BLACKJACK_WELCOME = """```yaml
Welcome to the blackjack game. 
==============================

It is recommended that you research the rules to familiarize yourself how the game is played. 
Stay safe and happy betting!```
""",
