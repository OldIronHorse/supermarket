from functools import partial
from .item import DiscountedItem

def three_for_two(item):
  return partial(do_three_for_two, item)
    
def do_three_for_two(item, basket):
  print(basket)
  full_price, discounted = basket
  matching_items = [i for i in full_price if i.name == item]
  non_matching_items = [i for i in full_price if i.name != item]
  (discount_count, spare) = divmod(len(matching_items), 3)
  new_discounts = [DiscountedItem(matching_items[0].name,
                                  matching_items[0].price, 
                                  0)] * discount_count
  return (non_matching_items + matching_items[:spare], 
          discounted + [matching_items[0]] * (discount_count * 2) + new_discounts)
