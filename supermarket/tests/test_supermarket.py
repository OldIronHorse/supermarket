from unittest import TestCase
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
    self.maxDiff=None
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

  def test_3_for_2_not_triggered_no_triplets(self):
    basket = ['soap', 'shampoo', 'toothpaste']
    self.assertEqual(Receipt([PricedItem('soap', 1.5), 
                              PricedItem('shampoo', 2.0), 
                              PricedItem('toothpaste', 0.8)],
                             4.3),
                     make_receipt(basket, self.prices, [three_for_two('soap')]))

  def test_3_for_2_not_triggered_no_matching_triplets(self):
    basket = ['soap', 'shampoo', 'shampoo', 'shampoo', 'toothpaste']
    self.assertEqual(Receipt([PricedItem('soap', 1.5), 
                              PricedItem('shampoo', 2.0), 
                              PricedItem('shampoo', 2.0), 
                              PricedItem('shampoo', 2.0), 
                              PricedItem('toothpaste', 0.8)],
                             8.3),
                     make_receipt(basket, self.prices, [three_for_two('soap')]))

  def test_3_for_2_simplest(self):
    basket = ['soap', 'soap', 'soap']
    self.assertEqual(Receipt([PricedItem('soap', 1.5), 
                              PricedItem('soap', 1.5), 
                              DiscountedItem('soap', 1.5, 0.0)],
                             3.0),
                     make_receipt(basket, self.prices, [three_for_two('soap')]))

