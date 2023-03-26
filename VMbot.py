#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

Formato del mensaje qeu envia Telegram al bot (Update):
Update(
	message=Message(
		channel_chat_created=False, 
		chat=Chat(
			first_name='Jo', 
			id=6213587610, 
			last_name='Loto', 
			type=<ChatType.PRIVATE>
			), 
		date=datetime.datetime(2023, 3, 24, 22, 39, 39, tzinfo=datetime.timezone.utc), 
		delete_chat_photo=False, 
		entities=(
			MessageEntity(
				length=5, 
				offset=0, 
				type=<MessageEntityType.BOT_COMMAND>
				),
			), 
		from_user=User(
			first_name='Jo', 
			last_name='Loto'
			id=6213587610, 
			is_bot=False, 
			language_code='es', 
			), 
		group_chat_created=False, 
		message_id=69, 
		supergroup_chat_created=False, 
		text='/test 2'
		), 
	update_id=960652557
	)
"""
import requests
import logging
import subprocess

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


ORDEN_ESTADO = 'estado'
PARAMETROS_ESTADO = 1
ORDEN_PARA = 'para'
PARAMETROS_PARA = 1
ORDEN_ARRANCA = 'arranca'
PARAMETROS_ARRANCA = 1

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    ayuda  = "Te puedo responder a estas preguntas:\n"
    ayuda += "--estado <id_maquina>\n     -->Devuelve el estado actual de la maquina\n"
    ayuda += "--arranca <id_maquina>\n     -->Arranca la maquina indicada en el id_maquina\n"
    ayuda += "--para <id_maquina>\n     -->Para la maquina indicada en el id_maquina\n"
    ayuda += "\n<id_maquina> corresponde con el numero de la maquina Win10_<id_maquina>"
    user = update.effective_user
    await update.message.reply_text(ayuda)


async def test_command (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
    print("entrada: ")
    print(update)


async def canal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
    print("Voy a por el canal")
    r = requests.post('https://api.telegram.org/bot' + BOT_ID + '/sendMessage',
              data={'chat_id': '@TotemVM', 'text': update.message.text})
    print(r.text)


async def ordenes (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    comando=update.message.text.split()
    print(comando)
    orden=comando[0].lower()
    print(orden)

    nParametros=len(comando)-1
    print("parametros= " + str(nParametros))
    parametros=[]
    if(nParametros>0):
        parametros=comando[1:nParametros+1]
        for i in range(len(parametros)):
           print("parametro[" + str(i) + "]: " + parametros[i])

    if (orden == ORDEN_ESTADO):
        if(len(parametros)<PARAMETROS_ESTADO):
           await update.message.reply_text("Prametros insuficientes")
        else:
           await update.message.reply_text(estado(parametros))
    elif (orden == ORDEN_ARRANCA):
        if(len(parametros)<PARAMETROS_ARRANCA):
           await update.message.reply_text("Prametros insuficientes")
        else:
           await update.message.reply_text(arranca(parametros))
    elif (orden == ORDEN_PARA):
        if(len(parametros)<PARAMETROS_PARA):
           await update.message.reply_text("Prametros insuficientes")
        else:
           await update.message.reply_text(para(parametros))
    else:
        await update.message.reply_text("Orden incorrecta")

def estado(parametros) -> None:
    if(len(parametros)<PARAMETROS_ESTADO):
        return("Faltan parametros")

    #compruebo el estado la maquina 1
    id_maquina=parametros[0]
    maquina="Win10_0"+id_maquina
    print("Maquina: " + maquina)
    p = subprocess.run(["/home/VMmanager/maquinas/estado.sh", maquina], stdout=subprocess.PIPE)

    #repondo con el estado
    if(p.returncode!=0):
        return ("Error en la llamada:" + p.stderr.decode('utf-8'))
    return p.stdout.decode('utf-8')
    #await update.message.reply_text(p.stdout.decode('utf-8'))


def para(parametros) -> None:
    if(len(parametros)<PARAMETROS_PARA):
        return("Faltan parametros")

    #compruebo el estado la maquina 1
    id_maquina=parametros[0]
    maquina="Win10_0"+id_maquina
    print("Maquina: " + maquina)
    p = subprocess.run(["/home/VMmanager/maquinas/paraVM.sh", maquina], stdout=subprocess.PIPE)

    #repondo con el estado
    if(p.returncode!=0):
        return ("Error en la llamada:" + p.stderr.decode('utf-8'))
    return "Maquina parando..." #p.stdout.decode('utf-8')
    #await update.message.reply_text(p.stdout.decode('utf-8'))


def arranca(parametros) -> None:
    if(len(parametros)<PARAMETROS_ARRANCA):
        return("Faltan parametros")

    #compruebo el estado la maquina 1
    id_maquina=parametros[0]
    maquina="Win10_0"+id_maquina
    print("Maquina: " + maquina)
    p = subprocess.run(["/home/VMmanager/maquinas/arranca.sh", maquina], stdout=subprocess.PIPE)
    print("Orden de arranque enviada a la maquina " + maquina)

    #repondo con el estado
    if(p.returncode!=0):
        return ("Error en la llamada:" + p.stderr.decode('utf-8'))
    return p.stdout.decode('utf-8')
    #await update.message.reply_text(p.stdout.decode('utf-8'))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("estado", estado))
    #application.add_handler(CommandHandler("arranca", arranca))
    #application.add_handler(CommandHandler("para", para))

    # on non command i.e message - echo the message on Telegram
    ####application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ordenes))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
