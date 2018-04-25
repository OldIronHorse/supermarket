from collections import namedtuple
from .item import PricedItem

Receipt = namedtuple('Receipt', 'basket total')

def make_receipt(basket, prices):
  priced = list(map(lambda item: PricedItem(item, prices[item]), basket))
  total = sum(map(lambda priced_item: priced_item.price, priced))
  return Receipt(priced, total)
