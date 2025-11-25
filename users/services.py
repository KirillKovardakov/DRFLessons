import stripe
from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_API_KEY


def corvert_rub_to_dollars(amount: float) -> int:
    """Конвертирует рубли в доллар"""
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(float(amount) * rate)


def create_stripe_price(amount: float) -> stripe.Price:
    """Создаёт ценну в Stripe"""
    price = stripe.Price.create(
        currency="usd",
        unit_amount=corvert_rub_to_dollars(amount) * 100,
        product_data={"name": "Payment"},
    )
    return price


def create_stripe_session(price: dict) -> (str, str):
    """Создаёт сессию оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def create_stripe_product(product_name: str) -> stripe.Product:
    """Создаёт продукт для оплаты Stripe"""
    product = stripe.Product.create(name=product_name)
    return product
