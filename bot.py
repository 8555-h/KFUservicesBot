from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# القنوات
CATEGORIES = {
    "📚 قروبات الدبلوم": [
        {"name": "مستوى أول دبلوم", "url": "https://t.me/+98Ow9FOSDsY4ZjA0"},
        {"name": "دبلوم إدارة أعمال", "url": "https://t.me/+UwyZYbgCSR0yZDJk"}
    ]
}

# القائمة الرئيسية
def main_menu() -> InlineKeyboardMarkup:
    keyboard = []
    for category in CATEGORIES.keys():
        keyboard.append([InlineKeyboardButton(category, callback_data=f"cat::{category}")])
    return InlineKeyboardMarkup(keyboard)

# قائمة العناصر داخل القسم
def category_menu(title: str) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(item["name"], url=item["url"])] for item in CATEGORIES.get(title, [])]
    rows.append([InlineKeyboardButton("↩️ رجوع", callback_data="back::main")])
    return InlineKeyboardMarkup(rows)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً 👋\nاختر القسم من القروبات المتاحة:",
        reply_markup=main_menu()
    )

# التعامل مع الضغط على الأزرار
async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data or ""
    if data.startswith("cat::"):
        title = data.split("::", 1)[1]
        await q.edit_message_text(f"📚 {title}", reply_markup=category_menu(title))
    elif data == "back::main":
        await q.edit_message_text("اختر القسم من القروبات المتاحة:", reply_markup=main_menu())

# تشغيل البوت
def run():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_click))
    app.run_polling()

if __name__ == "__main__":
    run()
