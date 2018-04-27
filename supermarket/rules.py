from functools import partial

def three_for_two(item):
  return partial(do_three_for_two, item)
    
def do_three_for_two(item, basket):
  #TODO switch to list comprehensions?
  matching_items = filter(lambda i: i.name == item, basket)
  non_matching_items = filter(lambda i: i.name != item, basket)
  #TODO take_n instead of numeric approach?
  (discount_count, spare) = divmod(len(matching_items), 3)
  return (non_matching_items + matching_items[:spare], [])
