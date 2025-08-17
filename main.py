
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import threading
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token - using the new token provided
BOT_TOKEN = "YOUR_BOT_TOLEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("🍽️ Ուտել", callback_data='eat'),
            InlineKeyboardButton("❌ Չուտել", callback_data='not_eat')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '🍇 Բարև՜ կեր, ամենահամեղ դոլմաները DolmaTopUtelBot ում 🍇',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'eat':
        keyboard = [
            [
                InlineKeyboardButton("✅ Այո", callback_data='yes_hungry'),
                InlineKeyboardButton("❌ Ոչ", callback_data='no_hungry')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            '🍴 Բարիօր ախպեր, սոված ես՞ 🤤',
            reply_markup=reply_markup
        )
    
    elif query.data == 'not_eat':
        await query.edit_message_text(
            '😤 Քու հետ մի պյան էն չի, ջիգ տեղերը խառնել ես 😤'
        )
    
    elif query.data == 'yes_hungry':
        keyboard = [
            [InlineKeyboardButton("🔥 Սարքել", callback_data='make_dolma')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            '🍇 Մեր տոլմից լավը չկա ջիգյար, արի սարքենք 🍇',
            reply_markup=reply_markup
        )
    
    elif query.data == 'no_hungry':
        await query.edit_message_text(
            '😒 Դե գնա ախպեր, հետո կկյաս որ սոված լես 😒'
        )
    
    elif query.data == 'make_dolma':
        keyboard = [
            [InlineKeyboardButton("⏭️ Շարունակեցինք", callback_data='continue')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            '⚠️ Բռատ զգուշ կլես, տոլմեն չեն խառնմ ⚠️',
            reply_markup=reply_markup
        )
    
    elif query.data == 'continue':
        keyboard = [
            [
                InlineKeyboardButton("🌿 Թփով տոլմա", callback_data='grape_dolma'),
                InlineKeyboardButton("🥬 Քյալամով տոլմա", callback_data='cabbage_dolma')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            '🍇 Ընտրիր տոլմայի տեսակը 🥬',
            reply_markup=reply_markup
        )
    
    elif query.data in ['grape_dolma', 'cabbage_dolma']:
        keyboard = [
            [InlineKeyboardButton("🚀 Սկսիր սարքել", callback_data='start_cooking')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            '👍 Լավ ճաշակ ունես, դե արի փորձենք 👨‍🍳',
            reply_markup=reply_markup
        )
    
    elif query.data == 'start_cooking':
        # Start countdown
        await countdown_animation(query, context)

async def countdown_animation(query, context):
    """Handle countdown animation from 1 to 10."""
    import asyncio
    
    for count in range(1, 11):
        if count == 10:
            keyboard = [
                [InlineKeyboardButton("🍽️ Փորձել", callback_data='try_dolma')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f'🔥 {count} 🔥\n\n✨ Փորձի դե, լա 😋',
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(f'⏱️ {count} ⏱️')
            await asyncio.sleep(2)

async def try_dolma_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle try dolma callback."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'try_dolma':
        keyboard = [
            [
                InlineKeyboardButton("😍 Այո", callback_data='liked'),
                InlineKeyboardButton("😕 Ոչ", callback_data='not_liked')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            '🤔 Հն՜, հավանեցիր՞ 🍽️',
            reply_markup=reply_markup
        )
    
    elif query.data == 'liked':
        await query.edit_message_text(
            '🎉 Մալադեց՜ Համեցեք երբ ուզմեք 🥳'
        )
    
    elif query.data == 'not_liked':
        await query.edit_message_text(
            '😠 Աչքիս քու հետ մի պան էն չի 😤'
        )

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        print("❌ Error: Bot token not found!")
        return
    
    print("🤖 Starting Telegram Bot...")
    
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler, pattern='^(eat|not_eat|yes_hungry|no_hungry|make_dolma|continue|grape_dolma|cabbage_dolma|start_cooking)$'))
        application.add_handler(CallbackQueryHandler(try_dolma_handler, pattern='^(try_dolma|liked|not_liked)$'))

        # Start the bot with polling
        print("🚀 Bot is starting...")
        application.run_polling(drop_pending_updates=True, allowed_updates=['message', 'callback_query'])
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("🔄 Restarting in 5 seconds...")
        time.sleep(5)
        main()

if __name__ == '__main__':
    main()
