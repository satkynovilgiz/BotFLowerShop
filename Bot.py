from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)

PRODUCTS = [
    {
        "name": "🌸 Цветок 1",
        "description": "Красивый цветок №1",
        "price": "$10",
        "photo_url": "https://i.pinimg.com/236x/6b/6d/c3/6b6dc3014162fc5cab8d73fb57fd4d9c.jpg",
        "buy_url": "https://example.com/order1"
    },
    {
        "name": "🌹 Цветок 2",
        "description": "Красивый цветок №2",
        "price": "$15",
        "photo_url": "https://www.povarenok.ru/data/cache/2017mar/16/22/1951015_46600-710x550.jpg",
        "buy_url": "https://example.com/order2"
    },
    {
        "name": "🌷 Цветок 3",
        "description": "Красивый цветок №3",
        "price": "$20",
        "photo_url": "https://kartin.papik.pro/uploads/posts/2023-06/thumbs/1686964607_kartin-papik-pro-p-kartinki-tsveti-dlya-svetika-s-nadpisyu-23.jpg",
        "buy_url": "https://example.com/order3"
    },
    {
        "name": "🌻 Цветок 4",
        "description": "Красивый цветок №4",
        "price": "$25",
        "photo_url": "https://kartin.papik.pro/uploads/posts/2023-06/1686851005_kartin-papik-pro-p-kartinki-tsveti-samie-krasivie-buketi-47.jpg",
        "buy_url": "https://example.com/order4"
    },
    # ... можно добавить до 10 товаров
]

# Стартовое приветствие с кнопкой показать товары
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать товары", callback_data="show_0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("HELLO welcome to our flower shop 🌸", reply_markup=reply_markup)

# Функция показа товара по индексу
async def send_product(update, context, product_index):
    product = PRODUCTS[product_index]
    caption = f"*{product['name']}*\n{product['description']}\nЦена: {product['price']}"

    buttons = [
        InlineKeyboardButton("🛒 Заказать", url=product['buy_url'])
    ]
    if product_index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"prev_{product_index}"))
    if product_index < len(PRODUCTS) - 1:
        buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"next_{product_index}"))

    keyboard = [buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Если это callback_query, редактируем сообщение с фото и подписью
    if update.callback_query:
        await update.callback_query.edit_message_media(
            media=InputMediaPhoto(media=product["photo_url"], caption=caption, parse_mode='Markdown'),
            reply_markup=reply_markup
        )
        await update.callback_query.answer()
    else:
        # Если вызвали напрямую (не из callback)
        await update.message.reply_photo(photo=product["photo_url"], caption=caption, parse_mode='Markdown', reply_markup=reply_markup)

# Обработчик кнопок
async def button(update, context):
    query = update.callback_query
    data = query.data  # например "next_0", "prev_1", "show_0"
    action, index_str = data.split('_')
    index = int(index_str)

    if action == "show":
        # Показываем товар с индексом 0 (первый)
        await send_product(update, context, index)
    elif action == "next":
        new_index = index + 1
        if new_index < len(PRODUCTS):
            await send_product(update, context, new_index)
    elif action == "prev":
        new_index = index - 1
        if new_index >= 0:
            await send_product(update, context, new_index)
    else:
        # На всякий случай - ответить, чтобы не "висел" запрос
        await query.answer()

def main():
    from telegram.ext import Application

    app = ApplicationBuilder().token("7859289535:AAGHHdzhp8LiFp-ZE0_AE4LRTzhLAnRyLT0").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Flower Shop Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
