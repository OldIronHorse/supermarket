from collections import namedtuple
"""The namedtuple reprisentations of full priced and discounted shopping basket items"""

PricedItem = namedtuple('PricedItem', 'name price')
"""A named item and its associated full price"""

DiscountedItem = namedtuple('DiscountedItem', 'name full_price saving price')
"""An individual discounted item, the discount saving and the discounted price"""

MultiBuy = namedtuple('MultiBuy', 'type items saving price')
"""A discounted collection of items including the discount type, saving and total price"""

WeighedItem = namedtuple('WeighedItem', 'name weight')
"""A item sold by weight, unpriced"""

PricedWeighedItem = namedtuple('PricedWeighedItem', 'name weight price_per_kg price')
"""An item sold by weight, priced"""
