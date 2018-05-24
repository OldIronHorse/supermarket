from functools import partial, reduce
from .item import MultiBuy

def spend_x_on_y_get_zpc_off(eligible_item_names, required_spend, discount):
    return partial(do_spend_x_on_y_get_zpc_off, eligible_item_names,
                   required_spend, discount)

def do_spend_x_on_y_get_zpc_off(eligible_item_names, required_spend, discount,
                               full_price_items, discounted_items):
    eligible_items = [item for item in full_price_items
                       if item.name in eligible_item_names]
    ineligilble_items = [item for item in full_price_items
                         if item.name not in eligible_item_names]
    eligible_spend = reduce(lambda total, i: total + i.price, eligible_items, 0)
    if eligible_spend < required_spend:
        return (full_price_items, discounted_items)
    else:
        return (ineligilble_items,
                discounted_items +
                [MultiBuy('spend X on Y get Z% off',
                          sorted(eligible_items),
                          eligible_spend * discount,
                          eligible_spend * (1 - discount))])

def freebies(paid_item_name, paid_item_count, free_item_name, free_item_count):
  """Factory function for "buy X of item A get Y of item B free rule
    You only get the freebies if they are in the basket, they are not added 
    automatically. It returns a function that implements the rule with the 
    supplied parameters.

  Args:
    paid_item_name (str): the name of the eligilbe item, A
    paid_item_count (int): the number of items A required to get a freebie, X
    freee_item_name (str): the name of the (potentially) free item, B
    free_item_count (int): the number of free items to be granted, Y

  Returns:
    fn(full_price_items, discounted_items): a function that will apply the 
      freebies rule to a list of priced items and return a tuple of 
      (full_priced_items, discounted_items)"""
  return partial(do_freebies, paid_item_name, paid_item_count, free_item_name,
                 free_item_count)

def do_freebies(paid_item_name, paid_item_count, free_item_name, free_item_count,
                full_price_items, discounted_items):
  paid_items = [item for item in full_price_items
                if item.name == paid_item_name]
  free_items = [item for item in full_price_items
                if item.name == free_item_name]
  other_items = [item for item in full_price_items 
                 if item.name not in [free_item_name, paid_item_name]]
  while free_items and len(paid_items) >= paid_item_count:
    paid = paid_items[:paid_item_count] 
    free = free_items[:free_item_count]
    paid_items = paid_items[paid_item_count:]
    free_items = free_items[free_item_count:]
    discounted_items = discounted_items + [MultiBuy('freebies',
                                                    paid + free,
                                                    reduce(lambda total, i: total + i.price,
                                                           free, 0),
                                                    reduce(lambda total, i: total + i.price,
                                                           paid, 0))]
  return (other_items + paid_items + free_items, discounted_items)

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
  while len(eligible_items) >= required_count:
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
