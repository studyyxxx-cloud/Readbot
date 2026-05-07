import json
import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8543992455:AAE9PqF1ND9JTtTPwdARHEcm5Iqa5nXkMlQ"
DATA_FILE = "data.json"

logging.basicConfig(level=logging.INFO)

BOOKS = [
    {"id":1,  "cat":"mind",      "title":"Znaju, ponimaju, upravljaju soboj",                 "author":"God lichnoj effektivnosti",    "p":True},
    {"id":2,  "cat":"mind",      "title":"Emocionalnyj intellekt. V ljubvi",                   "author":"Gottman, Silfer",              "p":True},
    {"id":3,  "cat":"mind",      "title":"Ljubit jego, ne terjaja sebja",                      "author":"Beveri Engl",                  "p":True},
    {"id":4,  "cat":"mind",      "title":"Byt, a ne styditsja",                                "author":"Tatjana Fisher"},
    {"id":5,  "cat":"mind",      "title":"Bez ogljadki na mamu",                               "author":"Tursheva, Rempel"},
    {"id":6,  "cat":"mind",      "title":"Tancujte svoju zhizn",                               "author":"Lilja Grad"},
    {"id":7,  "cat":"mind",      "title":"Ja - hozjain svoih emocij",                         "author":"Viktorija Shimanskaja"},
    {"id":8,  "cat":"mind",      "title":"Psihologija leni",                                   "author":"Svetlana Pisareva"},
    {"id":9,  "cat":"mind",      "title":"Kniga assertivnosti",                                "author":"Alberti, Emmons"},
    {"id":10, "cat":"mind",      "title":"Razreshi sebe sebja",                                "author":"Albert Safin"},
    {"id":11, "cat":"mind",      "title":"Zachem byt schastlivoj esli mozhno byt normalnoj",   "author":"Dzhanet Uinterson"},
    {"id":12, "cat":"mind",      "title":"Kak byt schastlivym vsegda",                        "author":"M.K. Gupta"},
    {"id":13, "cat":"mind",      "title":"Dao zhizni",                                        "author":"Irina Hakamada"},
    {"id":14, "cat":"mind",      "title":"Derzhis voin",                                       "author":"Glennon Dojl"},
    {"id":15, "cat":"mind",      "title":"Motivacija dlja tvorcheskih ljudej",                 "author":"Mark Makginness"},
    {"id":16, "cat":"health",    "title":"Sila cikla",                                        "author":"Mejsi Hill",                   "p":True},
    {"id":17, "cat":"health",    "title":"Zhenshina ves gormony",                              "author":"Elizabet Li Vliet",            "p":True},
    {"id":18, "cat":"health",    "title":"Myshcy tazovogo dna",                               "author":"Marina Osokina"},
    {"id":19, "cat":"health",    "title":"Begi mozg begi",                                    "author":"Anders Hansen"},
    {"id":20, "cat":"health",    "title":"Strannaja devochka vljubivshajasja v mozg",          "author":"Vendi Suzuki"},
    {"id":21, "cat":"health",    "title":"Privychki medlennogo starenija",                     "author":"Hevon Chon"},
    {"id":22, "cat":"health",    "title":"Japonskaja sistema omolozhenija 114 lajfhakov",      "author":"Savako Hibino"},
    {"id":23, "cat":"health",    "title":"Hranitel mozga",                                    "author":"Entoni Uiljam"},
    {"id":24, "cat":"health",    "title":"Spasenie pecheni",                                  "author":"Entoni Uiljam"},
    {"id":25, "cat":"health",    "title":"Koleni",                                            "author":"Manuel Kjone"},
    {"id":26, "cat":"health",    "title":"Mikroby vnutri nas",                                "author":"Blanka Garsija-Orea Aro"},
    {"id":27, "cat":"health",    "title":"Vdohnovljajushaja joga",                            "author":"Nensi Gershteijn"},
    {"id":28, "cat":"health",    "title":"Risknte stat zeljonoj vedmoj",                      "author":"Eris Urban"},
    {"id":29, "cat":"health",    "title":"Istochnik molodosti",                               "author":"Rouz En Kenni"},
    {"id":30, "cat":"health",    "title":"Ja ne umeju spat",                                  "author":"Hans-Gjunter Ves"},
    {"id":31, "cat":"health",    "title":"Mikroflora",                                        "author":"Zhan-Mark Bobo"},
    {"id":32, "cat":"health",    "title":"Kak ponjat svoj ZhKT",                              "author":"Daniela Purgina"},
    {"id":33, "cat":"health",    "title":"Pjatyj element zdorovja",                           "author":"Liza Hendrikson-Dzhek"},
    {"id":34, "cat":"health",    "title":"Women Hormones and the Menstrual Cycle",            "author":"Ruth Trickey"},
    {"id":35, "cat":"health",    "title":"Kak sozdat svojo novoje telo",                      "author":"Alberto Villoldo"},
    {"id":36, "cat":"health",    "title":"Mudrost tela",                                      "author":"Hillari Makbrajd"},
    {"id":37, "cat":"food",      "title":"Umnye kalorii",                                     "author":"Dzhonatan Bejlor",             "p":True},
    {"id":38, "cat":"food",      "title":"Eda i mozg",                                        "author":"Devid Perlmutter",             "p":True},
    {"id":39, "cat":"food",      "title":"Sol sahar i zhir",                                  "author":"Majkl Moss"},
    {"id":40, "cat":"food",      "title":"Golodnyj mozg",                                     "author":"Stefan Dj. Gijane"},
    {"id":41, "cat":"food",      "title":"Delo ne v kalorijah",                               "author":"Dzhonatan Bejlor"},
    {"id":42, "cat":"food",      "title":"Kompas pitanija",                                   "author":"Bas Kast"},
    {"id":43, "cat":"food",      "title":"Pochemu my edim to chto edim",                      "author":"Rejchel Herz"},
    {"id":44, "cat":"food",      "title":"Osoznannoe pitanije osoznannaja zhizn",             "author":"Tik Nat Han"},
    {"id":45, "cat":"food",      "title":"Netrevozhnye otnoshenija s edoj",                   "author":"Marija Kardakova"},
    {"id":46, "cat":"food",      "title":"Pishevoj monstr",                                   "author":"Zhenya Donova"},
    {"id":47, "cat":"food",      "title":"Appetit na povodke",                                "author":"Zhan-Filipp Zermati"},
    {"id":48, "cat":"food",      "title":"Kak my edim",                                       "author":"Bi Uilson"},
    {"id":49, "cat":"food",      "title":"Zamenit himiju na edu",                             "author":"Julita Bator"},
    {"id":50, "cat":"food",      "title":"Eda i mikrobiom",                                   "author":"Ketrin Harmon"},
    {"id":51, "cat":"food",      "title":"Zdorovyj kishechnik",                               "author":"Dzhastin Zonnenburg"},
    {"id":52, "cat":"food",      "title":"Eda dlja energii",                                  "author":"Ari Uitten"},
    {"id":53, "cat":"food",      "title":"Perezagruzka pitanija",                             "author":"Mark Sisson"},
    {"id":54, "cat":"food",      "title":"Fletcherizm",                                       "author":"Goracio Fletcher"},
    {"id":55, "cat":"food",      "title":"Pustye kalorii",                                    "author":"Kris Van Tulleken"},
    {"id":56, "cat":"food",      "title":"Vremena goda v moej tarelke",                       "author":"Kristina Chernyahovskaja"},
    {"id":57, "cat":"food",      "title":"Ljogkaja kuhnja",                                   "author":"Mari-Lor Tombini"},
    {"id":58, "cat":"food",      "title":"Zhenshina novogo vremeni",                          "author":"Ella Li"},
    {"id":59, "cat":"food",      "title":"Eda i mozg na praktike",                            "author":"Devid Perlmutter"},
    {"id":60, "cat":"money",     "title":"Bablospsobnost",                                    "author":"Svetlana Patrusheva",          "p":True},
    {"id":61, "cat":"money",     "title":"Sovety bogatoj mamy",                               "author":"Pak Sojon",                   "p":True},
    {"id":62, "cat":"money",     "title":"Horoshie devochki ne stanovjatsja bogatymi",        "author":"Lois P. Frankel"},
    {"id":63, "cat":"money",     "title":"Dengi idut zhenshhinam na polzu",                   "author":"Bodo Shefer"},
    {"id":64, "cat":"money",     "title":"Umnaja devushka stanovitsja bogatoj",               "author":"Elena Feoktistova"},
    {"id":65, "cat":"money",     "title":"Passivnyj dohod Rannjaja pensija",                  "author":"Rejchel Richards"},
    {"id":66, "cat":"money",     "title":"Blagodari i bogatej",                               "author":"Pem Grout"},
    {"id":67, "cat":"money",     "title":"Neskuchnye finansy",                                "author":"Afanasev Bodrejshij Krasnov"},
    {"id":68, "cat":"money",     "title":"Iskusstvo stilnoj bednosti",                        "author":"Aleksandr fon Shonburg"},
    {"id":69, "cat":"money",     "title":"Snachala zaplati sebe",                             "author":"Majk Mikalovic"},
    {"id":70, "cat":"money",     "title":"Dajte deneg rabotu ne predlagat",                   "author":"Marina Gogujeva"},
    {"id":71, "cat":"money",     "title":"Deti dengi ne zarabatyvajut",                       "author":"Irina Marjevich"},
    {"id":72, "cat":"money",     "title":"Schastlivyj karman polnyj deneg",                   "author":"Devid Kameron Dzhikandi"},
    {"id":73, "cat":"self",      "title":"Igra vdolguju",                                     "author":"Dori Klark",                  "p":True},
    {"id":74, "cat":"self",      "title":"365 dnej samodiscipliny",                           "author":"Martin Medouz",               "p":True},
    {"id":75, "cat":"self",      "title":"Net opravdanij",                                    "author":"Brajan Trejsi"},
    {"id":76, "cat":"self",      "title":"Cifrovoj minimalizm",                               "author":"Kel Njuport"},
    {"id":77, "cat":"self",      "title":"Magija vychitanija lishnego",                       "author":"Lejdi Kloti"},
    {"id":78, "cat":"self",      "title":"Superobuchenie",                                    "author":"Skott Jung"},
    {"id":79, "cat":"self",      "title":"Vsegda eshte levoj rukoj",                          "author":"Rohit Bhargava"},
    {"id":80, "cat":"self",      "title":"Ja ne lenjus ja na podzarjadke",                    "author":"Densing Snejl"},
    {"id":81, "cat":"self",      "title":"Zakonchi to chto nachal",                           "author":"Dzhon Ejkaf"},
    {"id":82, "cat":"self",      "title":"Peresebrat zhizn za 30 dnej",                      "author":"Vera Dejnogalerijan"},
    {"id":83, "cat":"self",      "title":"Vazhnye 30",                                        "author":"Kim He Nam"},
    {"id":84, "cat":"self",      "title":"Cepkaja cennaja celnaja",                           "author":"Marija Komkova"},
    {"id":85, "cat":"self",      "title":"Ne ischite apelsiny v chernichnom pole",            "author":"Dzhon Streleki"},
    {"id":86, "cat":"self",      "title":"Paradoks energii",                                  "author":"Stiven Gandri"},
    {"id":87, "cat":"self",      "title":"Kak silno ty etogo hochesh",                        "author":"Met Fitzgerald"},
    {"id":88, "cat":"relations", "title":"Nenasilvstvennoe obshenie dlja par",                "author":"Dzhonatant Robinson",         "p":True},
    {"id":89, "cat":"relations", "title":"Vmeste a ne prosto rjadom",                        "author":"Marina Majorova"},
    {"id":90, "cat":"relations", "title":"Netrevozhnye otnoshenija",                          "author":"Kniga ob otnoshenijah"},
    {"id":91, "cat":"relations", "title":"Prinjatie otca muzha i vsego muzhskogo mira",       "author":"Liana Dimitroshkina"},
    {"id":92, "cat":"relations", "title":"Seks v chelovecheskoj ljubvi",                      "author":"Erik Bern"},
    {"id":93, "cat":"relations", "title":"Zdorovye otnoshenija",                              "author":"Olga Dulepina"},
    {"id":94, "cat":"mom",       "title":"Lenivaja genialnaja mama",                          "author":"Kendra Adachi",               "p":True},
    {"id":95, "cat":"mom",       "title":"Horoshaja mama vs Plohaja mama",                    "author":"Minna Dubin",                 "p":True},
    {"id":96, "cat":"mom",       "title":"Mama kotoroj ja hochu byt",                        "author":"Daniela Gajgg"},
    {"id":97, "cat":"mom",       "title":"Pravila spokojnyh roditelej",                       "author":"Lora Markhem"},
    {"id":98, "cat":"mom",       "title":"Minimum vospitanija",                               "author":"Kim Dzhon Pejn"},
    {"id":99, "cat":"mom",       "title":"Kak mama",                                         "author":"Elli Kasacca"},
    {"id":100,"cat":"mom",       "title":"Doma posle roddoma",                                "author":"Julija Ismailova"},
    {"id":101,"cat":"mom",       "title":"Tajnaja opora",                                     "author":"L. Petranovskaja"},
    {"id":102,"cat":"mom",       "title":"Kogda ty budesh gotova",                            "author":"E.P. Berezovskaja"},
    {"id":103,"cat":"mom",       "title":"Osoznannoe roditelstvo",                            "author":"Sjuzen Stifelman"},
    {"id":104,"cat":"mom",       "title":"Kak govorit chtoby deti slushali",                  "author":"Adel Faber"},
    {"id":105,"cat":"mom",       "title":"Ja uchus byt mamoj",                                "author":"Lena Nikitina"},
    {"id":106,"cat":"mom",       "title":"Sozdan dlja menja kniga dlja otcov",                "author":"Zak Bush"},
    {"id":107,"cat":"biz",       "title":"Personalizacija prodazh",                           "author":"Aleksandr Derevickij",        "p":True},
    {"id":108,"cat":"biz",       "title":"Upravlenije proektami ot A do Ja",                 "author":"Richard Njuton"},
    {"id":109,"cat":"biz",       "title":"Biznes na podpiske",                                "author":"Ten Cuo"},
    {"id":110,"cat":"biz",       "title":"Vovlechjonnyje sotrudniki",                         "author":"Anna Jegorova"},
    {"id":111,"cat":"biz",       "title":"Ot klijenta k fanatu",                              "author":"Donna Katting"},
    {"id":112,"cat":"biz",       "title":"Upakuj i prodaj",                                   "author":"Temsen Vebster"},
    {"id":113,"cat":"biz",       "title":"Uchites videt biznes-processy",                     "author":"Majk Rother"},
    {"id":114,"cat":"biz",       "title":"God prozhityj pravilno",                            "author":"Brett Bljumentalj"},
    {"id":115,"cat":"biz",       "title":"Bez bjudzheta",                                     "author":"Igor Mann"},
    {"id":116,"cat":"biz",       "title":"Slozhnye podchinenye",                              "author":"Maksim Batyrev"},
    {"id":117,"cat":"biz",       "title":"Ekstremalnaja volja",                               "author":"Dzhoko Villink"},
    {"id":118,"cat":"biz",       "title":"Bolshaja kniga o socsetjah",                        "author":"Maksim Iljahov"},
    {"id":119,"cat":"biz",       "title":"Aktiviruyte svoj personalnyj brend",                "author":"Marija Azarenok"},
    {"id":120,"cat":"biz",       "title":"Hochu svoj biznes",                                 "author":"Artem Vahrushev"},
    {"id":121,"cat":"other",     "title":"52 upryamye zhenshiny",                             "author":"Rejchel Svejbi"},
    {"id":122,"cat":"other",     "title":"Suchki",                                            "author":"Ljusi Kok"},
    {"id":123,"cat":"other",     "title":"Magija mjagkoj bani",                               "author":"Marija Vojevodina"},
    {"id":124,"cat":"other",     "title":"Ogorod kruglyj god",                                "author":"Tjerri Enink"},
    {"id":125,"cat":"other",     "title":"Iskusstvo bega pod dozhdyom",                       "author":"Gart Sztajn"},
    {"id":126,"cat":"other",     "title":"Govorit pravdu o samom sebe",                       "author":"Mishel Fuko"},
    {"id":127,"cat":"other",     "title":"100 velichajshih huliganok v istorii",              "author":"Hanna Dzhevell"},
]

CATS = {
    "mind":"🧠 Psihologija","health":"💪 Zdorovje","food":"🥗 Pitanije",
    "money":"💰 Finansy","self":"🚀 Samorazvitije","relations":"💑 Otnoshenija",
    "mom":"👩 Materinstvo","biz":"💼 Biznes","other":"🌿 Raznoye"
}

INDEX = {str(b["id"]): b for b in BOOKS}

def load(uid):
    try:
        data = json.load(open(DATA_FILE, encoding="utf-8")) if os.path.exists(DATA_FILE) else {}
    except Exception:
        data = {}
    uid = str(uid)
    if uid not in data:
        data[uid] = {"done": [], "notes": {}, "pages": {}}
        json.dump(data, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return data[uid]

def save(uid, profile):
    try:
        data = json.load(open(DATA_FILE, encoding="utf-8")) if os.path.exists(DATA_FILE) else {}
    except Exception:
        data = {}
    data[str(uid)] = profile
    json.dump(data, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def main_menu():
    buttons = [[InlineKeyboardButton(name, callback_data=f"cat:{cat}")] for cat, name in CATS.items()]
    buttons.append([InlineKeyboardButton("⭐ S chego nachat", callback_data="priority")])
    buttons.append([InlineKeyboardButton("📊 Progress", callback_data="progress")])
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Privet {update.effective_user.first_name}! Vyberi kategoriju:",
        reply_markup=main_menu()
    )

async def progress_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = load(update.effective_user.id)
    done = len(p["done"])
    total = len(BOOKS)
    pct = int(done / total * 100)
    bar = "🟩" * (pct // 10) + "⬜" * (10 - pct // 10)
    await update.message.reply_text(f"📊 Progress:\n{bar} {pct}%\nProchitano: {done} iz {total}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    uid = q.from_user.id
    p = load(uid)

    if d == "main":
        await q.edit_message_text("Vyberi kategoriju:", reply_markup=main_menu())

    elif d == "progress":
        done = len(p["done"])
        total = len(BOOKS)
        pct = int(done / total * 100)
        bar = "🟩" * (pct // 10) + "⬜" * (10 - pct // 10)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Nazad", callback_data="main")]])
        await q.edit_message_text(f"📊 {done}/{total}\n{bar} {pct}%", reply_markup=kb)

    elif d == "priority":
        books = [b for b in BOOKS if b.get("p") and b["id"] not in p["done"]]
        if not books:
            await q.edit_message_text("Vse prioritetnye knigi prochitany!")
            return
        buttons = [[InlineKeyboardButton(f"⭐ {b['title'][:38]}", callback_data=f"book:{b['id']}")] for b in books[:10]]
        buttons.append([InlineKeyboardButton("Nazad", callback_data="main")])
        await q.edit_message_text("S chego nachat:", reply_markup=InlineKeyboardMarkup(buttons))

    elif d.startswith("cat:"):
        cat = d.split(":")[1]
        books = [b for b in BOOKS if b["cat"] == cat]
        buttons = []
        for b in books:
            tick = "✅" if b["id"] in p["done"] else "📖"
            star = "⭐" if b.get("p") else ""
            buttons.append([InlineKeyboardButton(f"{tick}{star} {b['title'][:36]}", callback_data=f"book:{b['id']}")])
        buttons.append([InlineKeyboardButton("Nazad", callback_data="main")])
        await q.edit_message_text(CATS[cat], reply_markup=InlineKeyboardMarkup(buttons))

    elif d.startswith("book:"):
        bid = int(d.split(":")[1])
        b = INDEX.get(str(bid))
        if not b:
            return
        is_done = bid in p["done"]
        note = p["notes"].get(str(bid), "")
        pages = p["pages"].get(str(bid), 0)
        tick = "✅" if is_done else "📖"
        text = f"{tick} {b['title']}\n{b['author']}"
        if b.get("p") and not is_done:
            text += "\n⭐ Prioritet"
        if pages:
            text += f"\nStranic: {pages}"
        if note:
            text += f"\nZametka: {note}"
        buttons = [
            [InlineKeyboardButton("↩️ Ubrat otmetku" if is_done else "✅ Prochitala!", callback_data=f"toggle:{bid}")],
            [InlineKeyboardButton("📝 Zametka", callback_data=f"note:{bid}"), InlineKeyboardButton("📄 Stranicy", callback_data=f"pages:{bid}")],
            [InlineKeyboardButton("Nazad", callback_data=f"cat:{b['cat']}")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif d.startswith("toggle:"):
        bid = int(d.split(":")[1])
        if bid in p["done"]:
            p["done"].remove(bid)
            msg = "Otmetka udalena"
        else:
            p["done"].append(bid)
            msg = "Prochitala! Molodec!"
        save(uid, p)
        b = INDEX.get(str(bid))
        is_done = bid in p["done"]
        text = f"{msg}\n\n{'✅' if is_done else '📖'} {b['title']}"
        buttons = [
            [InlineKeyboardButton("↩️ Ubrat otmetku" if is_done else "✅ Prochitala!", callback_data=f"toggle:{bid}")],
            [InlineKeyboardButton("📝 Zametka", callback_data=f"note:{bid}"), InlineKeyboardButton("📄 Stranicy", callback_data=f"pages:{bid}")],
            [InlineKeyboardButton("Nazad", callback_data=f"cat:{b['cat']}")],
        ]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

    elif d.startswith("note:"):
        bid = int(d.split(":")[1])
        context.user_data["note_for"] = bid
        b = INDEX.get(str(bid))
        await q.edit_message_text(f"Napishi zametku dlja:\n{b['title']}")

    elif d.startswith("pages:"):
        bid = int(d.split(":")[1])
        context.user_data["pages_for"] = bid
        b = INDEX.get(str(bid))
        cur = p["pages"].get(str(bid), 0)
        await q.edit_message_text(f"Stranicy dlja:\n{b['title']}\nSejchas: {cur}\nNapishi chislo:")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    p = load(uid)
    text = update.message.text.strip()

    if "note_for" in context.user_data:
        bid = context.user_data.pop("note_for")
        p["notes"][str(bid)] = text
        save(uid, p)
        await update.message.reply_text(f"Zametka sohranena!")
        return

    if "pages_for" in context.user_data:
        bid = context.user_data.pop("pages_for")
        if text.isdigit():
            p["pages"][str(bid)] = int(text)
            save(uid, p)
            await update.message.reply_text(f"Zapisano {text} stranic!")
        else:
            await update.message.reply_text("Nuzhno napisat chislo!")
        return

    found = [b for b in BOOKS if text.lower() in b["title"].lower() or text.lower() in b["author"].lower()]
    if found:
        buttons = [[InlineKeyboardButton(f"{'✅ ' if b['id'] in p['done'] else ''}{b['title'][:40]}", callback_data=f"book:{b['id']}")] for b in found[:6]]
        buttons.append([InlineKeyboardButton("Menju", callback_data="main")])
        await update.message.reply_text(f"Najdeno {len(found)}:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await update.message.reply_text("Ne nashla. Ispolzuj /start")

async def run():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("progress", progress_cmd))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Bot running!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(run())
