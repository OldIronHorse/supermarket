from collections import namedtuple
from functools import reduce
from .item import PricedItem

Receipt = namedtuple('Receipt', 'items total')

def price_items(basket, prices):
  return [PricedItem(item, prices[item]) for item in basket]

def make_receipt(basket, prices, rules=[]):
  priced = price_items(basket, prices)
  full_price, discounted = reduce(lambda items, rule: rule(items[0], items[1]),
                                  rules, 
                                  (priced, []))
  all_items = full_price + discounted
  total = sum(map(lambda priced_item: priced_item.price, all_items))
  return Receipt(all_items, total)
