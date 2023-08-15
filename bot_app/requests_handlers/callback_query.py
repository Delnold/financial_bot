import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_app.models import Savings


def handling_callback_query(query: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    callback_data = query.data.split("_")

    if callback_data[0] == "showSaving":
        savings_id = int(callback_data[1])
        selected_savings = Savings.objects.get(id=savings_id)

        message = f"Savings Type: {selected_savings.savings_type}\n"
        message += f"Quantity: {selected_savings.quantity}"

        keyboard = [
            [InlineKeyboardButton("Delete", callback_data=f"deleteSaving_{savings_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(chat_id=query.message.chat.id, text=message, reply_markup=reply_markup)
    elif callback_data[0] == "deleteSaving":
        savings_id = int(callback_data[1])
        selected_savings = Savings.objects.get(id=savings_id)
        selected_savings.delete()

        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                              text="Saving deleted.", reply_markup=None)
    else:
        bot.answer_callback_query(query.id, "Invalid command.")
