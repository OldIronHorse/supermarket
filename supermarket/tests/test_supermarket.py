from unittest import TestCase, main
from supermarket import make_receipt, PricedItem, Receipt, three_for_two, \
  DiscountedItem, price_items, two_for, MultiBuy, cheapest_free, freebies

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
                             PricedItem('toothpaste', 0.8),
                             MultiBuy('3 for 2',
                                      [PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0)],
                                      2.0, 4.0)]),
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
                                                 two_for('soap', 2.0)])
    self.assertEqual(sorted([PricedItem('shampoo', 2.0),
                             PricedItem('shampoo', 2.0),
                             PricedItem('toothpaste', 0.8),
                             MultiBuy('2 for',
                                      [PricedItem('soap', 1.5), 
                                       PricedItem('soap', 1.5)],
                                      1.0, 2.0),
                             MultiBuy('3 for 2',
                                      [PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0)],
                                      2.0, 4.0)]),
                     sorted(receipt.items))
    self.assertEqual(10.8, receipt.total)


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
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
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
    self.assertEqual(sorted([MultiBuy('3 for 2', 
                                      [PricedItem('soap', 1.5),
                                       PricedItem('soap', 1.5),
                                       PricedItem('soap', 1.5)],
                                      1.5, 3.0)]),
                     sorted(discounted))

  def test_simplest_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5), 
              PricedItem('soap', 1.5)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = three_for_two('soap')(basket, already_discounted)
    self.assertFalse(full_price)
    self.assertEqual(sorted([DiscountedItem('cheese', 1.0, 0.25, 0.75),
                             MultiBuy('3 for 2',
                                      [PricedItem('soap', 1.5), 
                                       PricedItem('soap', 1.5), 
                                       PricedItem('soap', 1.5)], 1.5, 3.0)]),
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
    self.assertEqual(sorted([MultiBuy('3 for 2', 
                                      [PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0)],
                                      2.0, 4.0)]),
                     sorted(discounted))

class Test2For(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = two_for('soap', 2.0)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_simplest(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('soap', 1.5)]
    full_price, discounted = two_for('soap', 2.0)(basket, [])
    self.assertFalse(full_price)
    self.assertEqual(sorted([MultiBuy('2 for',
                                      [PricedItem('soap', 1.5),
                                       PricedItem('soap', 1.5)],
                                      1.0, 2.0)]),
                     sorted(discounted))
    

class TestCheapestFree(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = \
        cheapest_free(['soap', 'toothpaste', 'conditioner'], 3)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_simplest_3(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = \
        cheapest_free(['soap', 'shampoo', 'toothpaste'], 3)(basket, already_discounted)
    self.assertEqual(sorted(discounted), 
                     sorted([DiscountedItem('cheese', 1.0, 0.25, 0.75),
                             MultiBuy('cheapest free',
                                      [PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0),
                                       PricedItem('toothpaste', 0.8)],
                                       0.8,
                                       4.0)]))
    self.assertEqual([PricedItem('soap', 1.5)], full_price)


class TestFreebies(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_triggered_not_fullfilled(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('conditioner', 2.5),
              PricedItem('conditioner', 2.5),
              PricedItem('conditioner', 2.5),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_triggered_partially_fullfilled(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('conditioner', 2.5),
              PricedItem('conditioner', 2.5),
              PricedItem('shampoo', 2.0),
              PricedItem('conditioner', 2.5),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(sorted(already_discounted +
                            [MultiBuy('freebies',
                                      [PricedItem('conditioner', 2.5),
                                       PricedItem('conditioner', 2.5),
                                       PricedItem('conditioner', 2.5),
                                       PricedItem('shampoo', 2.0)],
                                      2.0,
                                      7.5)]),
                     sorted(discounted)) 
    self.assertEqual(sorted([PricedItem('soap', 1.5),
                             PricedItem('toothpaste', 0.8)]),
                     sorted(full_price))

  def test_triggered_fullfilled(self):
    basket = [PricedItem('soap', 1.5),
              PricedItem('shampoo', 2.0),
              PricedItem('conditioner', 2.5),
              PricedItem('conditioner', 2.5),
              PricedItem('shampoo', 2.0),
              PricedItem('conditioner', 2.5),
              PricedItem('shampoo', 2.0),
              PricedItem('toothpaste', 0.8)]
    already_discounted = [DiscountedItem('cheese', 1.0, 0.25, 0.75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(sorted(discounted), 
                     sorted(already_discounted +
                            [MultiBuy('freebies',
                                      [PricedItem('conditioner', 2.5),
                                       PricedItem('conditioner', 2.5),
                                       PricedItem('conditioner', 2.5),
                                       PricedItem('shampoo', 2.0),
                                       PricedItem('shampoo', 2.0)],
                                      4.0,
                                      7.5)]))
    self.assertEqual(sorted([PricedItem('soap', 1.5),
                             PricedItem('shampoo', 2.0),
                             PricedItem('toothpaste', 0.8)]),
                    sorted(full_price))
    

if __name__ == '__main__':
  main()
