from unittest import TestCase, main
from supermarket import make_receipt, PricedItem, Receipt, three_for_two, \
  DiscountedItem, price_items, two_for

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
    self.assertEqual(11.8, receipt.total)
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                             PricedItem('shampoo', 2.0),
                             PricedItem('shampoo', 2.0),
                             PricedItem('soap', 1.5),
                             PricedItem('shampoo', 2.0),
                             PricedItem('toothpaste', 0.8),
                             PricedItem('shampoo', 2.0),
                             DiscountedItem('shampoo', 2.0, 0)]),
                     sorted(receipt.items))


class TestRule3For2(TestCase):
  def test_not_triggered_no_triplets(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    full_price, discounted = three_for_two('soap')(basket, [])
    self.assertFalse(discounted)
    self.assertEqual(sorted([PricedItem('soap', 1.5),
                             PricedItem('shampoo', 2.0),
                             PricedItem('toothpaste', 0.8)]),
                     sorted(full_price))

  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.75)]
    full_price, discounted = three_for_two('soap')(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted([PricedItem('soap', 1.5),
                             PricedItem('shampoo', 2.0),
                             PricedItem('toothpaste', 0.8)]),
                     sorted(full_price))


  def test_not_triggered_no_matching_triplets(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    full_price, discounted = three_for_two('soap')(basket, [])
    self.assertFalse(discounted)
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('shampoo', 2.0), 
                      PricedItem('toothpaste', 0.8)]),
                     sorted(full_price))

  def test_simplest(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5)]
    full_price, discounted = three_for_two('soap')(basket, [])
    self.assertFalse(full_price)
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                             PricedItem('soap', 1.5), 
                             DiscountedItem('soap', 1.5, 0.0)]),
                     sorted(discounted))

  def test_simplest_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.75)]
    full_price, discounted = three_for_two('soap')(basket, already_discounted)
    self.assertFalse(full_price)
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                             PricedItem('soap', 1.5), 
                             DiscountedItem('cheese', 1.0, 0.75),
                             DiscountedItem('soap', 1.5, 0.0)]),
                     sorted(discounted))

  def test_1_and_a_bit_matches(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0)]
    full_price, discounted = three_for_two('shampoo')(basket, [])
    self.assertEqual(sorted([PricedItem('soap', 1.5), 
                             PricedItem('soap', 1.5),
                             PricedItem('toothpaste', 0.8),
                             PricedItem('shampoo', 2.0),
                             PricedItem('shampoo', 2.0)]),
                     sorted(full_price))
    self.assertEqual(sorted([DiscountedItem('shampoo', 2.0, 0.0),
                             PricedItem('shampoo', 2.0),
                             PricedItem('shampoo', 2.0)]),
                     sorted(discounted))

class Test2For(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.75)]
    full_price, discounted = two_for('soap', 2.0)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_simplest(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('soap', 1.5)]
    full_price, discounted = two_for('soap', 2.0)(basket, [])
    self.assertFalse(full_price)
    self.assertEqual(sorted([DiscountedItem('soap', 1.5, 2.0),
                             DiscountedItem('soap', 1.5, 0)]),
                     sorted(discounted))
    

if __name__ == '__main__':
  main()
