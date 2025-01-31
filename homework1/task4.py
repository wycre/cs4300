def calculate_discount(price, discount):
    if not (discount > 0 and discount < 1):
        discount = discount / 100
    return price * discount
