from unittest import TestCase
from supermarket import Receipt, PricedItem, make_receipt, three_for_two,\
  two_for, MultiBuy

class TestMakeReceipt(TestCase):
  def setUp(self):
    self.maxDiff = None
    self.prices = {
     'soap': 150,
     'shampoo': 200,
     'toothpaste': 80,
    }

  def test_no_rules_no_multiples(self):
    basket = ['soap', 'shampoo', 'toothpaste']
    self.assertEqual(Receipt([PricedItem('soap', 150),
                              PricedItem('shampoo', 200),
                              PricedItem('toothpaste', 80)],
                             430),
                     make_receipt(basket, self.prices))

  def test_3_for_2_1_and_bit_matches(self):
    basket = ['soap',
              'shampoo',
              'shampoo',
              'soap',
              'shampoo',
              'toothpaste',
              'shampoo',
              'shampoo']
    receipt = make_receipt(basket, self.prices, [three_for_two('shampoo')])
    self.assertEqual(1180, receipt.total)
    self.assertEqual(sorted([PricedItem('soap', 150),
                             PricedItem('shampoo', 200),
                             PricedItem('shampoo', 200),
                             PricedItem('soap', 150),
                             PricedItem('toothpaste', 80),
                             MultiBuy('3 for 2',
                                      [PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200)],
                                      200, 400)]),
                     sorted(receipt.items))

  def test_multiple_rules(self):
    basket = ['soap',
              'shampoo',
              'shampoo',
              'soap',
              'shampoo',
              'toothpaste',
              'shampoo',
              'shampoo']
    receipt = make_receipt(basket, self.prices, [three_for_two('shampoo'),
                                                 two_for('soap', 200)])
    self.assertEqual(sorted([PricedItem('shampoo', 200),
                             PricedItem('shampoo', 200),
                             PricedItem('toothpaste', 80),
                             MultiBuy('2 for',
                                      [PricedItem('soap', 150),
                                       PricedItem('soap', 150)],
                                      100, 200),
                             MultiBuy('3 for 2',
                                      [PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200)],
                                      200, 400)]),
                     sorted(receipt.items))
    self.assertEqual(1080, receipt.total)
