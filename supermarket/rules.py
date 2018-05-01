from functools import partial
from .item import DiscountedItem

def two_for(item_to_discount, discounted_price):
  return partial(do_two_for, item_to_discount, discounted_price)

def do_two_for(item_to_discount, discounted_price, full_price_items, 
               discounted_items):
  matching_items = [i for i in full_price_items if i.name == item_to_discount]
  non_matching_items = [i for i in full_price_items if i.name != item_to_discount]
  (discount_count, spare) = divmod(len(matching_items), 2)
  item = matching_items[0]
  return (non_matching_items + matching_items[:spare],
          discounted_items + [DiscountedItem(item.name, item.price, 0),
                              DiscountedItem(item.name, 
                                             item.price, 
                                             discounted_price)] 
                           * discount_count)

def three_for_two(item_to_discount):
  return partial(do_three_for_two, item_to_discount)
    
def do_three_for_two(item_to_discount, full_price, discounted):
  matching_items = [i for i in full_price if i.name == item_to_discount]
  non_matching_items = [i for i in full_price if i.name != item_to_discount]
  (discount_count, spare) = divmod(len(matching_items), 3)
  new_discounts = [DiscountedItem(matching_items[0].name,
                                  matching_items[0].price, 
                                  0)] * discount_count
  return (non_matching_items + matching_items[:spare], 
          discounted + [matching_items[0]] * (discount_count * 2) + new_discounts)
