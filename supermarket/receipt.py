from collections import namedtuple
from functools import reduce
from .item import PricedItem, PricedWeighedItem

Receipt = namedtuple('Receipt', 'items saving total')
"""A receipt as a list of item and a total"""

def price_items(basket, prices):
  """Function to apply a pricing table to a basket of items

  Args:
    basket (list of str): item names
    prices (dict of str to int): pricing table by item name

  Returns:
    list of PricedItem: items with prices

  Throws:
    KeyError: if item name does not exist in the pricing table"""
  return [price_item(item, prices) for item in basket]

def price_item(item, prices):
  """Function to price an individual item based in a pricing table
    Handles price per item and price per kilo.

  Args:
    item (str): item name
    prices (dict of str to int): price lookup table

  Returns:
    PricedItem|PricedWeigheditem: priced item

  Throws:
    KeyError: if item name is not in map"""
  try:
    return PricedItem(item, prices[item])
  except KeyError:
    per_kg = prices[item.name]
    return PricedWeighedItem(item.name, item.weight, per_kg, int(round(per_kg * item.weight)))

def make_receipt(basket, prices, rules=[]):
  """Function to make areciept from a list of items, a pricing table and a 
    list of discounting rules

  Args:
    basket (list of str|WeighedItem): the items in the basket
    prices (dict of string to int|float): prices by item name
    rules (list of fn(full_priced_items, discounted_items)): an ordered list 
      of discount rules to apply to the basket
    
  Returns:
    Receipt: namedtuple containg items, savings and total price"""
  priced = price_items(basket, prices)
  full_price, discounted = reduce(lambda items, rule: rule(items[0], items[1]),
                                  rules, 
                                  (priced, []))
  all_items = full_price + discounted
  total = sum(map(lambda priced_item: priced_item.price, all_items))
  saving = sum(map(lambda item: item.saving, discounted))
  return Receipt(all_items, saving, total)
