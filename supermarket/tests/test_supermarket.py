from unittest import TestCase, main
from supermarket import make_receipt, PricedItem, Receipt, three_for_two, \
  DiscountedItem, price_items

class TestPriceItems(TestCase):
  def setUp(self):
    self.prices = {
     'soap': 1.5,
     'shampoo': 2.0,
     'toothpaste': 0.8,
    }

  def test_prices_for_all_items(self):
    basket = ['soap', 'shampoo', 'toothpaste']
    self.assertEqual([PricedItem('soap', 1.5), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('toothpaste', 0.8)],
                     list(price_items(basket, self.prices)))
    
  

class TestMakeReceipt(TestCase):
  def setUp(self):
    self.maxDiff = None
    self.prices = {
     'soap': 1.5,
     'shampoo': 2.0,
     'toothpaste': 0.8,
    }

  def test_no_rules_no_multiples(self):
    basket = ['soap', 'shampoo', 'toothpaste']
    self.assertEqual(Receipt([PricedItem('soap', 1.5), 
                              PricedItem('shampoo', 2.0), 
                              PricedItem('toothpaste', 0.8)],
                             4.3),
                     make_receipt(basket, self.prices))

class TestRule3For2(TestCase):
  def test_3_for_2_not_triggered_no_triplets(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    full_price, discounted = three_for_two('soap')((basket, []))
    self.assertFalse(discounted)
    self.assertEqual(sorted([PricedItem('soap', 1.5),
                             PricedItem('shampoo', 2.0),
                             PricedItem('toothpaste', 0.8)]),
                     sorted(full_price))

  def test_3_for_2_not_triggered_no_matching_triplets(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    full_price, discounted = three_for_two('soap')((basket, []))
    self.assertFalse(discounted)
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('toothpaste', 0.8)]),
                     sorted(full_price))

  def test_3_for_2_simplest(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5)]
    full_price, discounted = three_for_two('soap')((basket, []))
    self.assertFalse(full_price)
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                             PricedItem('soap', 1.5), 
                             DiscountedItem('soap', 1.5, 0.0)]),
                     sorted(discounted))

if __name__ == '__main__':
  main()
