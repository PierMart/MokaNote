import discord  # Librairie principale pour interagir avec l'API Discord
from discord.ext import commands  # Extension pour créer des bots plus facilement
import sys
import os
from utils import process_url  # Fonction utilitaire pour traiter les URLs
import json
import logging

# --------------------
# CONFIGURATION LOGGING
# --------------------
# Permet de logger à la fois dans un fichier log dédié et dans la console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'log', 'bot.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ResuPhyBot")
# Active les logs détaillés de la librairie discord.py
logging.getLogger('discord').setLevel(logging.INFO)

# --------------------
# CHARGEMENT DE LA CONFIGURATION
# --------------------
# On charge le token Discord depuis le fichier config.json
with open('config.json') as f:
    config = json.load(f)

TOKEN = config.get('DISCORD_TOKEN')  # Token d'authentification du bot

# --------------------
# CONFIGURATION DES INTENTS
# --------------------
# Les intents définissent les types d'événements que le bot peut recevoir
intents = discord.Intents.default()
intents.message_content = True  # Permet de lire le contenu des messages
intents.messages = True

def get_hello_message():
    """Fonction utilitaire pour retourner un message de bienvenue."""
    return "Hello!"

# --------------------
# INITIALISATION DU BOT
# --------------------
# On crée une instance du bot avec le préfixe '$' pour les commandes
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

# --------------------
# EVENEMENT : Bot prêt
# --------------------
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    # Bot prêt
    # (Logique de reboot supprimée)

# --------------------
# COMMANDE : $url <lien>
# --------------------
@bot.command()
async def url(ctx, url: str):
    """Commande pour traiter une URL (YouTube, TikTok, etc.) et renvoyer le résultat."""
    result = process_url(url)
    # Discord limite les messages à 2000 caractères, on découpe si besoin
    async def send_long_message(ctx, message):
        for i in range(0, len(message), 2000):
            await ctx.send(message[i:i+2000])
    await send_long_message(ctx, result)

# --------------------
# COMMANDE : $hello
# --------------------

@bot.command(aliases=["h"])
async def help(ctx):
    """Affiche la liste des commandes disponibles."""
    help_message = (
        "**Commandes disponibles :**\n"
        "`$hello` : Vérifie que le bot est en ligne.\n"
        "`$url <lien>` : Traite une URL (YouTube, TikTok, Instagram) et renvoie le résultat.\n"
        "`$reboot` : Redémarre le bot (propriétaire uniquement).\n"
        "`$help` ou `$h` : Affiche cette aide."
    )
    await ctx.send(help_message)

@bot.command()
async def hello(ctx):
    """Commande simple pour vérifier que le bot est en ligne."""
    await ctx.send("Hello! Je suis en ligne grâce à OVH.")

# --------------------
# COMMANDE : $reboot (propriétaire uniquement)
# --------------------
@bot.command()
@commands.is_owner()
async def reboot(ctx):
    """Commande pour redémarrer le bot à distance. Seul le propriétaire peut l'utiliser."""
    await ctx.send("♻️ Redémarrage du bot en cours...")
    await bot.close()
    # Relance le script principal avec les mêmes arguments
    os.execv(sys.executable, [sys.executable] + sys.argv)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Supprime un certain nombre de messages dans le canal. Non disponible en DM."""
    if ctx.guild is None:
        await ctx.send("❌ Cette commande ne peut être utilisée qu'en salon de serveur, pas en message privé.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande elle-même
    confirmation = await ctx.send(f"{len(deleted)-1} messages supprimés.", delete_after=3)

# --------------------
# LANCEMENT DU BOT
# --------------------
if __name__ == '__main__':
    if not TOKEN:
        logger.error('Please add your Discord API token to config.json (key: DISCORD_TOKEN)')
    else:
        logger.info('Starting the bot...')
        bot.run(TOKEN)
