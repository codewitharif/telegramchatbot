"""
Telegram Customer Support Chatbot
----------------------------------
A practical chatbot for customer support on Telegram

Features:
- FAQ responses
- Order tracking
- Business hours info
- Contact support escalation
- Product information

Setup:
1. Install: pip install python-telegram-bot
2. Get bot token from @BotFather on Telegram
3. Replace 'YOUR_BOT_TOKEN_HERE' with your actual token
4. Run: python telegram_bot.py
"""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging
from datetime import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states
MAIN_MENU, ORDER_TRACKING, PRODUCT_INFO = range(3)

# FAQ Database
FAQS = {
    "business hours": "Business Hours:\n\nMonday-Friday: 9 AM - 6 PM\nSaturday: 10 AM - 4 PM\nSunday: Closed\n\nWe are available to serve you during these hours.",
    
    "return policy": "Return Policy:\n\n• 7 days return window\n• Product must be unused\n• Original packaging required\n• Refund processed in 5-7 business days\n\nPlease contact us if you have any issues.",
    
    "shipping": "Shipping Information:\n\n• Free shipping on orders above Rs. 500\n• Delivery: 3-5 business days\n• Metro cities: 2-3 days\n• Tracking details provided after order confirmation\n\nYou can track your order anytime.",
    
    "payment": "Payment Methods:\n\n• Credit/Debit Cards\n• UPI (GPay, PhonePe, Paytm)\n• Net Banking\n• Cash on Delivery (Rs. 50 extra)\n\nSecure payment gateway enabled.",
}

# Product catalog (sample)
PRODUCTS = {
    "1": {"name": "Wireless Headphones", "price": "Rs. 2,499", "stock": "In Stock"},
    "2": {"name": "Smart Watch", "price": "Rs. 3,999", "stock": "In Stock"},
    "3": {"name": "Power Bank 20000mAh", "price": "Rs. 1,299", "stock": "Limited Stock"},
    "4": {"name": "Bluetooth Speaker", "price": "Rs. 1,799", "stock": "In Stock"},
}

def get_main_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [KeyboardButton("Track Order"), KeyboardButton("View Products")],
        [KeyboardButton("FAQs"), KeyboardButton("Contact Support")],
        [KeyboardButton("Business Hours"), KeyboardButton("Store Location")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_faq_keyboard():
    """FAQ keyboard"""
    keyboard = [
        [KeyboardButton("Return Policy"), KeyboardButton("Shipping Info")],
        [KeyboardButton("Payment Methods"), KeyboardButton("Business Hours")],
        [KeyboardButton("Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    welcome_msg = f"""
Hello {user.first_name},

I am your customer support assistant. How can I help you today?

Please select an option:
"""
    await update.message.reply_text(welcome_msg, reply_markup=get_main_keyboard())
    return MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu selections"""
    text = update.message.text
    
    if text == "Track Order":
        await update.message.reply_text(
            "Please enter your order number:\n\n(Format: ORD12345)",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Main Menu")]], resize_keyboard=True)
        )
        return ORDER_TRACKING
    
    elif text == "View Products":
        products_msg = "Our Products:\n\n"
        for pid, product in PRODUCTS.items():
            products_msg += f"{pid}. {product['name']}\n"
            products_msg += f"   Price: {product['price']}\n"
            products_msg += f"   Status: {product['stock']}\n\n"
        products_msg += "To learn more about a product, please send the product number (1-4)"
        
        await update.message.reply_text(
            products_msg,
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Main Menu")]], resize_keyboard=True)
        )
        return PRODUCT_INFO
    
    elif text == "FAQs":
        await update.message.reply_text(
            "Frequently Asked Questions\n\nPlease select a topic:",
            reply_markup=get_faq_keyboard()
        )
        return MAIN_MENU
    
    elif text == "Contact Support":
        support_msg = """
Customer Support

Contact our support team:

Email: support@example.com
Phone: +91-9876543210
WhatsApp: +91-9876543210

Support Hours: Monday-Saturday, 9 AM - 6 PM

We will respond within 24 hours.
"""
        await update.message.reply_text(support_msg, reply_markup=get_main_keyboard())
        return MAIN_MENU
    
    elif text == "Business Hours":
        await update.message.reply_text(FAQS["business hours"], reply_markup=get_main_keyboard())
        return MAIN_MENU
    
    elif text == "Store Location":
        location_msg = """
Store Location

Head Office:
123, MG Road, Connaught Place
New Delhi - 110001

Landmark: Near Metro Station

Store Timings:
Monday-Saturday: 10 AM - 8 PM
Sunday: 11 AM - 6 PM

Google Maps: [Location Link]
"""
        await update.message.reply_text(location_msg, reply_markup=get_main_keyboard())
        return MAIN_MENU
    
    # FAQ responses
    elif text.lower() in ["return policy", "shipping info", "payment methods", "business hours"]:
        key = text.lower().replace("info", "").replace("methods", "").strip()
        if key == "shipping":
            key = "shipping"
        elif key == "payment":
            key = "payment"
        
        response = FAQS.get(key, "Sorry, information on this topic is not available.")
        await update.message.reply_text(response, reply_markup=get_faq_keyboard())
        return MAIN_MENU
    
    elif text == "Main Menu":
        await update.message.reply_text("Main Menu:", reply_markup=get_main_keyboard())
        return MAIN_MENU
    
    else:
        await update.message.reply_text(
            "Sorry, I did not understand. Please select an option:",
            reply_markup=get_main_keyboard()
        )
        return MAIN_MENU

async def order_tracking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle order tracking"""
    text = update.message.text
    
    if text == "Main Menu":
        await update.message.reply_text("Main Menu:", reply_markup=get_main_keyboard())
        return MAIN_MENU
    
    # Simulate order lookup
    if text.upper().startswith("ORD"):
        order_status = f"""
Order Status

Order ID: {text.upper()}
Status: Out for Delivery

Timeline:
• Order Placed: 12 Jan 2026
• Shipped: 13 Jan 2026
• Out for Delivery: 14 Jan 2026
• Expected Delivery: Today by 6 PM

Tracking Link: [Track Order]

Delivery Partner: BlueDart
Contact: 1800-123-4567
"""
        await update.message.reply_text(order_status, reply_markup=get_main_keyboard())
        return MAIN_MENU
    else:
        await update.message.reply_text(
            "Invalid order number format.\n\nPlease enter order number in format: ORD12345",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Main Menu")]], resize_keyboard=True)
        )
        return ORDER_TRACKING

async def product_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle product information requests"""
    text = update.message.text
    
    if text == "Main Menu":
        await update.message.reply_text("Main Menu:", reply_markup=get_main_keyboard())
        return MAIN_MENU
    
    if text in PRODUCTS:
        product = PRODUCTS[text]
        product_detail = f"""
{product['name']}

Price: {product['price']}
Availability: {product['stock']}

Features:
• High quality product
• 1 year warranty
• Free shipping on orders above Rs. 500

To place an order:
Phone/WhatsApp: +91-9876543210
Website: www.example.com

Would you like to know anything else?
"""
        await update.message.reply_text(product_detail, reply_markup=get_main_keyboard())
        return MAIN_MENU
    else:
        await update.message.reply_text(
            "Invalid product number. Please select 1-4:",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Main Menu")]], resize_keyboard=True)
        )
        return PRODUCT_INFO

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text(
        "Thank you! Feel free to message us if you need any assistance.",
        reply_markup=get_main_keyboard()
    )
    return MAIN_MENU

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    # Replace with your bot token from @BotFather
    TOKEN = "8335737411:AAEVZ-eWF_iG_zepAo5SRhFYZfnJlQ-OXmE"
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            ORDER_TRACKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_tracking_handler)],
            PRODUCT_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_info_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    app.add_handler(conv_handler)
    app.add_error_handler(error_handler)
    
    # Start bot
    print("Bot is running...")
    print("Press Ctrl+C to stop")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()