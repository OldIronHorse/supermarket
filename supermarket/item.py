from collections import namedtuple

PricedItem = namedtuple('PricedItem', 'name price')
DiscountedItem = namedtuple('DiscountedItem', 'name full_price price')
