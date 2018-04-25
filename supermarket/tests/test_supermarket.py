from unittest import TestCase
from supermarket import make_receipt, PricedItem, Receipt

class TestMakeReceipt(TestCase):
  def setUp(self):
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
