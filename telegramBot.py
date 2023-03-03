import random
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, filters, MessageHandler, Updater


class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_callback))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.echo))

    def start(self, update, context):
        user = update.message.from_user
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {user.first_name}! Что ты хочешь?")
        button_list = [
            InlineKeyboardButton("Случайное сообщение", callback_data="random_message"),
            InlineKeyboardButton("Случайная картинка", callback_data="random_picture")
        ]
        reply_markup = InlineKeyboardMarkup(self.build_menu(button_list, n_cols=1))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите действие:", reply_markup=reply_markup)

    def button_callback(self, update, context):
        query = update.callback_query
        if 'last_message' in context.chat_data:
            context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.chat_data['last_message'])
        if 'last_photo' in context.chat_data:
            context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.chat_data['last_photo'])
        if query.data == "random_message":
            messages = ["Сегодня прекрасный день!", "Солнце светит ярко.", "Сегодня я чувствую себя хорошо."]
            message = context.bot.send_message(chat_id=query.message.chat_id, text=random.choice(messages))
            context.chat_data['last_message'] = message.message_id
        elif query.data == "random_picture":
            url = "https://source.unsplash.com/featured/600x400/?anime,love"
            photo = context.bot.send_photo(chat_id=query.message.chat_id, photo=url)
            context.chat_data['last_photo'] = photo.message_id

    def echo(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()


def main():
    token = '6175911864:AAGXL9jIZzBYWtQ5i-oB8rsLNpy1SCW0r84'
    bot = TelegramBot(token)
    bot.start_polling()


if __name__ == '__main__':
    main()
