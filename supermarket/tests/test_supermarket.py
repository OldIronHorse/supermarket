from unittest import TestCase, main
from supermarket import make_receipt, PricedItem, Receipt, three_for_two, \
  DiscountedItem, price_items, two_for, MultiBuy, cheapest_free, freebies, \
  WeighedItem, PricedWeighedItem, spend_x_on_y_get_zpc_off

class TestPriceItems(TestCase):
  def setUp(self):
    self.prices = {
     'soap': 150,
     'shampoo': 200,
     'toothpaste': 80,
     'banana': 80,
    }

  def test_prices_for_all_items(self):
    basket = ['soap', 'shampoo', 'toothpaste']
    self.assertEqual([PricedItem('soap', 150),
                      PricedItem('shampoo', 200),
                      PricedItem('toothpaste', 80)],
                     list(price_items(basket, self.prices)))
    
  def test_weighed_item(self):
    basket = [WeighedItem('banana', 0.454)]
    self.assertEqual([PricedWeighedItem('banana', 0.454, 80, 36)],
                     list(price_items(basket, self.prices)))
  





if __name__ == '__main__':
  main()
