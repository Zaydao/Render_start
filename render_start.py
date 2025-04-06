from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import telegram.error

TOKEN = '7600663477:AAG8Fd5FmLJ8XkQg-MWED4q-hvJLTR-m2os'

# Linkuri PayPal și imagini pentru fiecare plan
PLAN_DETAILS = {
    "1️⃣ Rezervă locul – 9€": {
        "link": "https://www.paypal.com/",  # Înlocuiește cu linkul corect pentru plata
        "image": "https://media.designcafe.com/wp-content/uploads/2022/07/29185240/industrial-rustic-living-room-in-earthy-tones.jpg",
        "desc": "Plătește acum doar 9€ ca să îți rezervi locul la curs.\nAchitarea integrală o poți face până la 1 mai 2025."
    },
    "2️⃣ 3ds Max Integral – 175€": {
        "link": "https://www.paypal.com/",  # Înlocuiește cu linkul corect pentru plata
        "image": "https://media.designcafe.com/wp-content/uploads/2022/07/29185240/industrial-rustic-living-room-in-earthy-tones.jpg",
        "desc": "Dedicat celor care vor să aprofundeze partea tehnică și randările fotorealiste.\n\n✅ Acces Modul 5 – 3ds Max + Corona Render\n✅ Chat de suport pe durata cursului\n❌ Fără diplomă\n❌ Fără acces la celelalte module"
    },
    "3️⃣ Tarif Expert – 450€": {
        "link": "https://www.paypal.com/",  # Înlocuiește cu linkul corect pentru plata
        "image": "https://media.designcafe.com/wp-content/uploads/2022/07/29185240/industrial-rustic-living-room-in-earthy-tones.jpg",
        "desc": "Parcurs complet de la zero la designer cu clienți.\n\n✅ Acces la Modulele 1–6\n✅ Diplomă de absolvire\n✅ Suport în timpul cursului\n❌ Fără Modul 7 (strategie personalizată)\n❌ Fără apeluri 1:1\n❌ Fără suport după finalizare"
    },
    "4️⃣ Tarif Antreprenor – 600€": {
        "link": "https://www.paypal.com/",  # Înlocuiește cu linkul corect pentru plata
        "image": "https://media.designcafe.com/wp-content/uploads/2022/07/29185240/industrial-rustic-living-room-in-earthy-tones.jpg",
        "desc": "Experiență premium cu suport extins și dezvoltare de brand personal.\n\n✅ Acces la toate cele 7 module\n✅ 3 apeluri 1:1 cu Gabriela\n✅ Strategie personală & portofoliu\n✅ Lecții AI + animații cu Rayon\n✅ Diplomă de absolvire\n✅ Suport 3 luni după curs"
    },
    "5️⃣ Vreau să achit în rate": {
        "link": "https://t.me/NumeleTău",  # Înlocuiește cu linkul corect pentru contact
        "image": "https://media.designcafe.com/wp-content/uploads/2022/07/29185240/industrial-rustic-living-room-in-earthy-tones.jpg",
        "desc": "Scrie-mi direct aici: telegram.me/NumeleTău\nVom stabili împreună metoda de plată. (Voi avea nevoie de IDNP-ul tău)"
    },
}

# Mesajul de bun venit
WELCOME_MESSAGE = (
    "Salut!\n"
    "Mă bucur sincer că ai rezonat cu programul și că ești interesată să mergi mai departe.🤍\n\n"
    "Rezervă locul pentru curs, cu doar 9€ sau achită integral, cu o reducere de 15%. ⬇️"
)

# Funcție reutilizabilă pentru afișarea planurilor
async def show_plans(update_or_query, context):
    keyboard = [
        [InlineKeyboardButton(plan, callback_data=plan)]
        for plan in PLAN_DETAILS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(update_or_query, Update):
        # Trimite doar lista de planuri fără mesaj suplimentar aici
        await update_or_query.message.reply_text(
            "Alege planul dorit:",
            reply_markup=reply_markup
        )
    else:  # CallbackQuery (din „Înapoi”)
        await update_or_query.message.reply_text(
            "Alege planul dorit:",
            reply_markup=reply_markup
        )

# /start – mesaj de salut și afișarea planurilor
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Trimite mesajul de bun venit
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode='Markdown'
    )
    # Apoi trimite lista de planuri
    await show_plans(update, context)

# Când se apasă pe un plan sau butonul „Înapoi”
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    plan = query.data

    if plan == "back_to_plans":
        # Revine la lista de planuri cu un mesaj nou
        await show_plans(query, context)
        return

    details = PLAN_DETAILS[plan]

    # Trimite imaginea fără text
    await query.message.reply_photo(
        photo=details["image"]
    )

    # Trimite detaliile cursului cu butoanele „Înapoi” și „Contact Suport”
    keyboard = [
        [InlineKeyboardButton("🔙 Înapoi", callback_data="back_to_plans"),
         InlineKeyboardButton("📞 Contact Suport", url="https://t.me/SupportTeam")]  # Înlocuiește cu link-ul real de suport
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        text=f"{details['desc']}\n\n💳 Plătește aici:\n{details['link']}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Configurare aplicație
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()