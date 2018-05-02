from collections import namedtuple

#TODO: add saving to discounted items?

PricedItem = namedtuple('PricedItem', 'name price')
DiscountedItem = namedtuple('DiscountedItem', 'name full_price saving price')
MultiBuy = namedtuple('MultiBuy', 'type items saving price')
