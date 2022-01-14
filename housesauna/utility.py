import telepot

my_token = None
with open('./housesauna/token.txt') as f:
    my_token = f.read().strip()

my_chat_id = None
with open('./housesauna/chat.txt') as f:
    my_chat_id = f.read().strip()


def send_telegram(msg) -> None:
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    print(msg)
    bot = telepot.Bot(my_token)
    bot.sendMessage(chat_id=my_chat_id, text=msg)