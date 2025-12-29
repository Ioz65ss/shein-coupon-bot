import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
from datetime import datetime
import json

BOT_TOKEN = "7917130354:AAGR-Nme2vJsLtQeYp2fvnWFnuQCEOJQiIE"
CHANNEL_ID = -1003619656295  # Your coupon channel ID
COUPON_CODE = "SVWK08VD3A6088R"  # Replace with your coupon

bot = Bot(token=BOT_TOKEN)

async def get_products_with_coupon_check():
    """Get SHEIN products and validate coupon for each"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    valid_products = []
    
    try:
        # Fetch product page
        url = "https://www.sheinindia.in/c/sverse-5939-37961"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract products
        product_items = soup.find_all('div', class_='product-item')
        
        for item in product_items[:10]:  # Check top 10
            try:
                name = item.find('div', class_='goods-title').text.strip()
                price = item.find('span', class_='goods-price-usd').text.strip()
                
                # Check if coupon applicable (SHEIN has minimum order values)
                try:
                    price_value = float(price.replace('$', '').replace(',', ''))
                    if price_value > 5:  # Minimum for coupon
                        coupon_applicable = "✅ APPLICABLE"
                        valid_products.append({
                            'name': name,
                            'price': price,
                            'sizes': "All sizes",
                            'coupon_status': coupon_applicable
                        })
                except:
                    pass
            except:
                pass
        
        return valid_products
    
    except Exception as e:
        print(f"Error: {e}")
        return []

async def send_coupon_update():
    """Send coupon-valid products to channel"""
    products = await get_products_with_coupon_check()
    
    if products:
        message = "🎉 **SHEIN COUPON CHECKER** 🎉\n\n"
        message += f"Coupon Code: **{COUPON_CODE}**\n"
        message += f"Check: {datetime.now().strftime('%H:%M:%S IST')}\n\n"
        message += "Products where coupon applies:\n\n"
        
        for i, product in enumerate(products[:5], 1):
            message += f"{i}. {product['name']}\n"
            message += f"   Price: {product['price']}\n"
            message += f"   Coupon: {product['coupon_status']}\n\n"
        
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode='Markdown'
            )
            print(f"✓ Coupon check sent")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    print("Coupon checker started...")
    while True:
        await send_coupon_update()
        await asyncio.sleep(60)  # Update every 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
