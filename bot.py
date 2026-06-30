import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Add it in Railway Variables.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

STORE_NAME = "Next Gen AI Shop"
SUPPORT = "@digitalproduct786"
BINANCE_PAY_ID = "486825563"
BKASH = "01619431937"
NAGAD = "01619431937"
products = {   
"p1": {
    "name": "ChatGPT K12 - 2 Years",
    "bdt": "1650",
    "usdt": "$14",
    "stock": 20,
    "image": "https://raw.githubusercontent.com/nextgenaishop/next-gen-ai-shop/main/IMG_20260628_103606_618.jpg",
    "desc": """🤖 CDK (K12) FOR SINGLE
━━━━━━━━━━━━━━

💵 Price: $14.00
➕ Stock: 20 accounts
↗️ Sold: 350 accounts

Description:

✅ ChatGPT K12 Edu 2-year package.
Full of latest languages like Plus.

✅ Can activate any account owner.

⚠️ Applies to Gmail ONLY.
(We are not responsible if you use other emails.)

✅ After ordering, you will receive a code.

✅ Account is on free plan.

✅ Recommended to use an account without an active subscription or a newly created account to register.

🌐 Web upgrade CDK:
https://oaiteam.azx.us/

Step 1:
Get https://chatgpt.com/api/auth/session
Paste into JSON.

Step 2:
Paste the CDK.

Step 3:
Upgrade.

⚠️ NOTE:
This product is sold with NO WARRANTY."""
},
    "p2": {
        "name": "Canva Pro - 1 Month",
        "bdt": "500",
        "usdt": "$4",
        "stock": 20,
        "desc": "Canva Pro access. Instant delivery after payment verification.",
        "image": ""
    },

    "p3": {
        "name": "Super Grok - 3 Month Full Warranty",
        "bdt": "2280",
        "usdt": "$18",
        "stock": "10",
        "desc": "Super Grok subscription. Instant delivery after payment verification.",
        "image": ""
    },

    "p4": {
        "name": "ChatGPT Plus Official - 1 Month",
        "bdt": "530",
        "usdt": "4.5",
        "stock": "10",
        "desc": "ChatGPT Plus official subscription. Instant delivery after payment verification.",
        "image": "https://raw.githubusercontent.com/nextgenaishop/next-gen-ai-shop/main/IMG_20260628_103606_618.jpg"
    },
    "p5": {
        "name": "Capcut Pro 28 Days- Full warranty",
        "bdt": "420",
        "usdt": "$3.00",
        "stock": "70",
        "desc": "Capcut Pro subscription. Instant delivery after payment verification.",
        "image": ""
    },

    "p6": {
        "name": "ElevenLabs - 1 Month + 15 Days Warranty",
        "bdt": "1250",
        "usdt": "10",
        "stock": "5",
        "desc": "ElevenLabs subscription with 15 days warranty. Instant delivery after payment verification.",
        "image": ""
    }
}

user_orders = {}
user_wallets = {}

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Products"), KeyboardButton(text="🎧 Support")],
            [KeyboardButton(text="💰 Wallet"), KeyboardButton(text="🎁 Share & Earn")],
            [KeyboardButton(text="🌐 Language")],
        ],
        resize_keyboard=True,
    )


def products_keyboard():
    rows = []
    for pid, p in products.items():
        rows.append([InlineKeyboardButton(text=f"{p['name']} | ৳{p['bdt']} / {p['usdt']} USDT", callback_data=f"product:{pid}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def buy_keyboard(pid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buy Now", callback_data=f"buy:{pid}")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="products")],
    ])


@dp.message(CommandStart())
async def start(message: Message):
    if message.from_user.id not in user_wallets:
        user_wallets[message.from_user.id] = 0.0

    await message.answer(
        f"🤖 Welcome to {STORE_NAME}\n\n"
        f"Premium AI tools & online subscriptions are available here.\n\n"
        f"Please choose an option from the menu below 👇",
        reply_markup=main_menu(),
    )
    
@dp.message(F.text == "🛍 Products")
async def show_products_message(message: Message):
    await message.answer("🛍 Available Products\n\nSelect a product:", reply_markup=products_keyboard())

@dp.callback_query(F.data.startswith("product:"))
async def show_product(callback: CallbackQuery):
    pid = callback.data.split(":", 1)[1]
    p = products[pid]

    text = (
        f"📦 {p['name']}\n\n"
        f"💰 Price: ৳{p['bdt']} / {p['usdt']} USDT\n"
        f"🎁 Stock: {p['stock']}\n\n"
        f"ℹ️ {p['desc']}"
    )

    if p.get("image"):
        await callback.message.answer_photo(
            photo=p["image"],
            caption=text,
            reply_markup=buy_keyboard(pid)
        )
    else:
        await callback.message.answer(
            text,
            reply_markup=buy_keyboard(pid)
        )

    await callback.answer()

@dp.callback_query(F.data.startswith("buy:"))
async def buy_product(callback: CallbackQuery):
    pid = callback.data.split(":", 1)[1]

    user_orders[callback.from_user.id] = {
        "product": pid,
        "step": "quantity"
    }

    await callback.message.answer(
        f"✏️ Enter quantity to buy (1-{products[pid]['stock']}):"
    )

    await callback.answer()

@dp.message(F.text.regexp(r"^\d+$"))
async def process_quantity(message: Message):

    if message.from_user.id not in user_orders:
        return

    if user_orders[message.from_user.id].get("step") != "quantity":
        return

    if not message.text.isdigit():
        await message.answer("❌ Please enter a valid number.")
        return

    qty = int(message.text)

    pid = user_orders[message.from_user.id]["product"]
    p = products[pid]

    if qty < 1 or qty > int(p["stock"]):
        await message.answer(f"❌ Quantity must be between 1 and {p['stock']}.")
        return

total_bdt = qty * int(p["bdt"])
total_usdt = qty * float(str(p["usdt"]).replace("$", ""))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟡 Binance Pay", callback_data="pay_binance")],
        [InlineKeyboardButton(text="💳 Wallet", callback_data="pay_wallet")],
        [InlineKeyboardButton(text="💵 USDT (BEP20)", callback_data="pay_usdt")],
        [InlineKeyboardButton(text="📱 bKash", callback_data="pay_bkash")],
        [InlineKeyboardButton(text="📱 Nagad", callback_data="pay_nagad")]
    ])

    await message.answer(
        f"📦 Order Summary\n\n"
        f"Product: {p['name']}\n"
        f"Quantity: {qty}\n\n"
        f"💰 Total: ৳{total_bdt}\n"
        f"💵 Total USDT: ${total_usdt}\n\n"
        f"Choose payment method:",
        reply_markup=kb
    )

@dp.callback_query(F.data == "pay_binance")
async def pay_binance(callback: CallbackQuery):
    pid = user_orders.get(callback.from_user.id, {}).get("product")
    qty = user_orders.get(callback.from_user.id, {}).get("qty", 1)

    if pid and pid in products:
        usdt = float(str(products[pid]["usdt"]).replace("$", "")) * qty
    else:
        usdt = 0

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ I Have Paid",
                    callback_data="paid_binance"
                )
            ]
        ]
    )

    text = (
        f"🟡 Binance Pay\n\n"
        f"🆔 Binance Pay ID:\n"
        f"{BINANCE_PAY_ID}\n\n"
        f"💵 Amount to Pay: ${usdt:.2f} USDT\n\n"
        f"⚠️ Send the exact payment amount."
    )

    await callback.message.answer(text, reply_markup=kb)
    await callback.answer()

@dp.callback_query(F.data == "paid_binance")
async def paid_binance(callback: CallbackQuery):
    await callback.message.answer(
        f"📸 Please send your payment screenshot or Transaction ID.\n\n"
        f"👤 Admin: {SUPPORT}\n\n"
        f"⚠️ Send your payment proof directly to the admin above.\n"
        f"After verification, your order will be processed ."
    )
    await callback.answer()

@dp.message(F.text == "🎧 Support")
async def support(message: Message):
    await message.answer(f"🎧 Support\n\nযেকোনো order, payment বা delivery সমস্যা হলে যোগাযোগ করুন:\n\n{SUPPORT}")


@dp.message(F.text == "💰 Wallet")
async def wallet(message: Message):

    balance = user_wallets.get(message.from_user.id, 0.0)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="➕ Deposit USDT",
                callback_data="deposit_usdt"
            )]
        ]
    )

    await message.answer(
        f"💰 Wallet\n\n"
        f"💵 USDT Balance: ${balance:.2f}\n\n"
        f"🟡 Recharge your wallet using Binance Pay.\n"
        f"📷 After payment, send the payment screenshot to admin.\n\n"
        f"🆔 Binance Pay ID: {BINANCE_PAY_ID}",
        reply_markup=kb
    )

@dp.message(F.text == "🎁 Share & Earn")
async def share(message: Message):
    await message.answer(f"🎁 Share & Earn\n\nআপনার referral link share করুন।\n\nhttps://t.me/next_gen_ai_shop_bot?start={message.from_user.id}\n\nআপনার link থেকে কেউ order করলে আপনি commission পাবেন।\nReferral system manually admin verify করবে।")


@dp.message(F.text == "🌐 Language")
async def language(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇧🇩 বাংলা", callback_data="lang:bn")],
    ])
    await message.answer("🌐 Select Language", reply_markup=kb)


@dp.callback_query(F.data.startswith("lang:"))
async def set_lang(callback: CallbackQuery):
    lang = callback.data.split(":", 1)[1]
    if lang == "bn":
        await callback.message.answer("✅ ভাষা বাংলা সিলেক্ট করা হয়েছে।")
    else:
        await callback.message.answer("✅ English language selected.")
    await callback.answer()


@dp.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Access denied.")
        return
    await message.answer("👨‍💼 Admin Panel\n\nCommands:\n/stock - Send stock alerts\n/admin - Show this menu")


@dp.message(Command("stock"))
async def stock(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    for p in products.values():
        await message.answer(f"🚨 Stock Alert!\n━━━━━━━━━━━━━━\n\n🔥 New keys have been added for: {p['name']}\n\n🎁 Available Stock: {p['stock']}\n⚡ Hurry up and grab yours now before it runs out!", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Now", callback_data="products")]]))


@dp.message(F.photo)
async def receive_payment_info(message: Message):
    pid = user_orders.get(message.from_user.id)
    if pid:
        p = products[pid]
        await message.answer("✅ Transaction ID / Screenshot received.\n\nAdmin verify করার পর order delivery করা হবে।")
        if ADMIN_ID:
            await bot.send_message(ADMIN_ID, f"💳 Payment Submitted\n\nUser ID: {message.from_user.id}\nUsername: @{message.from_user.username}\nProduct: {p['name']}\nMessage: {message.text or 'Attachment/Screenshot'}")
    else:
        await message.answer("Please choose an option from the menu.", reply_markup=main_menu())

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class AddProduct(StatesGroup):
    id = State()
    name = State()
    bdt = State()
    usdt = State()
    stock = State()
    desc = State()

@dp.message(Command("addproduct"))
async def add_product(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(AddProduct.id)
    await message.answer("Product ID লিখুন (যেমন: p6)")
    
@dp.message(AddProduct.id)
async def add_product_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await state.set_state(AddProduct.name)
    await message.answer("Product Name লিখুন:")
    
@dp.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.bdt)
    await message.answer("BDT Price লিখুন:")

@dp.message(AddProduct.bdt)
async def add_product_bdt(message: Message, state: FSMContext):
    await state.update_data(bdt=message.text)
    await state.set_state(AddProduct.usdt)
    await message.answer("USDT Price লিখুন:")

@dp.message(AddProduct.usdt)
async def add_product_usdt(message: Message, state: FSMContext):
    await state.update_data(usdt=message.text)
    await state.set_state(AddProduct.stock)
    await message.answer("Stock লিখুন:")

@dp.message(AddProduct.stock)
async def add_product_stock(message: Message, state: FSMContext):
    await state.update_data(stock=message.text)
    await state.set_state(AddProduct.desc)
    await message.answer("Description লিখুন:")

@dp.message(AddProduct.desc)
async def add_product_desc(message: Message, state: FSMContext):
    data = await state.get_data()

    products[data["id"]] = {
        "name": data["name"],
        "bdt": data["bdt"],
        "usdt": data["usdt"],
        "stock": data["stock"],
        "desc": message.text,
    }

    await state.clear()
    await message.answer("✅ Product Successfully Added!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
