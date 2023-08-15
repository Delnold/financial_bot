import telebot
from telebot.types import Message
from bot_app.models import User, Savings, UserState
from bot_app.requests_handlers.commands import add_savings_command


def handling_messages(message: Message, bot: telebot.TeleBot):
    user_id = message.from_user.id
    try:
        user = User.objects.filter(user_id=user_id).first()
        current_state = UserState.objects.get_state(user=user)
        if current_state.command == "/add_savings":
            add_savings_command(message, bot)
        else:
            bot.reply_to(message, "There is no ongoing commands!")
    except User.DoesNotExist:
        bot.reply_to(message, "Please use the /register command first to record your credentials and use the bot.")