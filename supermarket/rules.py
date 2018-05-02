from functools import partial, reduce
from .item import MultiBuy

def cheapest_free(eligible_item_names, required_count):
  return partial(do_cheapest_free, eligible_item_names, required_count)

def do_cheapest_free(eligible_item_names, required_count, full_price_items, 
                     discounted_items):
  eligible_items = sorted([item for item in full_price_items 
                           if item.name in eligible_item_names],
                          key=lambda item: item.price,
                          reverse=True)
  ineligible_items = [item for item in full_price_items 
                      if item.name not in eligible_item_names]
  while(len(eligible_items) >= required_count):
    pay_for = eligible_items[:required_count - 1]
    get_free = eligible_items[-1]
    discounted_items = discounted_items + [MultiBuy('cheapest free', 
                                                   pay_for + [get_free],
                                                   get_free.price,
                                                   reduce(lambda total, i: total + i.price,
                                                          pay_for, 0))]
    eligible_items = eligible_items[required_count - 1:]
    eligible_items = eligible_items[:-1]
  return (ineligible_items + eligible_items, discounted_items)

def two_for(item_to_discount, discounted_price):
  return partial(do_two_for, item_to_discount, discounted_price)

def do_two_for(item_to_discount, discounted_price, full_price_items, 
               discounted_items):
  matching_items = [i for i in full_price_items if i.name == item_to_discount]
  non_matching_items = [i for i in full_price_items if i.name != item_to_discount]
  (discount_count, spare) = divmod(len(matching_items), 2)
  item = matching_items[0]
  return (non_matching_items + matching_items[:spare],
          discounted_items + [MultiBuy('2 for',
                                       matching_items[:2],
                                       item.price * 2 -discounted_price,
                                       discounted_price)] * discount_count)

def three_for_two(item_to_discount):
  return partial(do_three_for_two, item_to_discount)
    
def do_three_for_two(item_to_discount, full_price, discounted):
  matching_items = [i for i in full_price if i.name == item_to_discount]
  non_matching_items = [i for i in full_price if i.name != item_to_discount]
  (discount_count, spare) = divmod(len(matching_items), 3)
  new_discounts = [MultiBuy('3 for 2',
                            matching_items[:3],
                            matching_items[0].price, 
                            matching_items[0].price * 2)] * discount_count
  return (non_matching_items + matching_items[:spare], 
          discounted + new_discounts)
