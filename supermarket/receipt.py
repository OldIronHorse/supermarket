from collections import namedtuple
from .item import PricedItem

Receipt = namedtuple('Receipt', 'basket total')

def price_items(basket, prices):
  return [PricedItem(item, prices[item]) for item in basket]

def make_receipt(basket, prices, rules=[]):
  priced = price_items(basket, prices)
  discounted = [] 
  for rule in rules:
    (priced, discounted_this_rule) = rule(priced)
    discounted += discounted_this_rule
  all_items = priced + discounted
  total = sum(map(lambda priced_item: priced_item.price, all_items))
  return Receipt(all_items, total)
