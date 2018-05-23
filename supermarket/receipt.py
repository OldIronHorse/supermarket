from collections import namedtuple
from functools import reduce
from .item import PricedItem, PricedWeighedItem

Receipt = namedtuple('Receipt', 'items saving total')
"""A receipt as a list of item and a total"""

def price_items(basket, prices):
  return [price_item(item, prices) for item in basket]

def price_item(item, prices):
  try:
    return PricedItem(item, prices[item])
  except KeyError:
    per_kg = prices[item.name]
    return PricedWeighedItem(item.name, item.weight, per_kg, int(round(per_kg * item.weight)))

def make_receipt(basket, prices, rules=[]):
  priced = price_items(basket, prices)
  full_price, discounted = reduce(lambda items, rule: rule(items[0], items[1]),
                                  rules, 
                                  (priced, []))
  all_items = full_price + discounted
  total = sum(map(lambda priced_item: priced_item.price, all_items))
  saving = sum(map(lambda item: item.saving, discounted))
  return Receipt(all_items, saving, total)
