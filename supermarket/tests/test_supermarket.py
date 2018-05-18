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


class TestRule3For2(TestCase):
  def test_not_triggered_no_triplets(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    full_price, discounted = three_for_two('soap')(basket, [])
    self.assertFalse(discounted)
    self.assertEqual(sorted([PricedItem('soap', 150),
                             PricedItem('shampoo', 200),
                             PricedItem('toothpaste', 80)]),
                     sorted(full_price))

  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = three_for_two('soap')(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted([PricedItem('soap', 150),
                             PricedItem('shampoo', 200),
                             PricedItem('toothpaste', 80)]),
                     sorted(full_price))


  def test_not_triggered_no_matching_triplets(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    full_price, discounted = three_for_two('soap')(basket, [])
    self.assertFalse(discounted)
    self.assertEqual(sorted([PricedItem('soap', 150),
                      PricedItem('shampoo', 200),
                      PricedItem('shampoo', 200),
                      PricedItem('shampoo', 200),
                      PricedItem('toothpaste', 80)]),
                     sorted(full_price))

  def test_simplest(self):
    basket = [PricedItem('soap', 150),
              PricedItem('soap', 150),
              PricedItem('soap', 150)]
    full_price, discounted = three_for_two('soap')(basket, [])
    self.assertFalse(full_price)
    self.assertEqual(sorted([MultiBuy('3 for 2', 
                                      [PricedItem('soap', 150),
                                       PricedItem('soap', 150),
                                       PricedItem('soap', 150)],
                                      150, 300)]),
                     sorted(discounted))

  def test_simplest_preserve_discounts(self):
    basket = [PricedItem('soap', 150),
              PricedItem('soap', 150),
              PricedItem('soap', 150)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = three_for_two('soap')(basket, already_discounted)
    self.assertFalse(full_price)
    self.assertEqual(sorted([DiscountedItem('cheese', 100, 25, 75),
                             MultiBuy('3 for 2',
                                      [PricedItem('soap', 150),
                                       PricedItem('soap', 150),
                                       PricedItem('soap', 150)], 150, 300)]),
                     sorted(discounted))

  def test_1_and_a_bit_matches(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200)]
    full_price, discounted = three_for_two('shampoo')(basket, [])
    self.assertEqual(sorted([PricedItem('soap', 150),
                             PricedItem('soap', 150),
                             PricedItem('toothpaste', 80),
                             PricedItem('shampoo', 200),
                             PricedItem('shampoo', 200)]),
                     sorted(full_price))
    self.assertEqual(sorted([MultiBuy('3 for 2', 
                                      [PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200)],
                                      200, 400)]),
                     sorted(discounted))

class Test2For(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = two_for('soap', 200)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_simplest(self):
    basket = [PricedItem('soap', 150),
              PricedItem('soap', 150)]
    full_price, discounted = two_for('soap', 200)(basket, [])
    self.assertFalse(full_price)
    self.assertEqual(sorted([MultiBuy('2 for',
                                      [PricedItem('soap', 150),
                                       PricedItem('soap', 150)],
                                      100, 200)]),
                     sorted(discounted))
    

class TestCheapestFree(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = \
        cheapest_free(['soap', 'toothpaste', 'conditioner'], 3)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_simplest_3(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = \
        cheapest_free(['soap', 'shampoo', 'toothpaste'], 3)(basket, already_discounted)
    self.assertEqual(sorted(discounted), 
                     sorted([DiscountedItem('cheese', 100, 25, 75),
                             MultiBuy('cheapest free',
                                      [PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200),
                                       PricedItem('toothpaste', 80)],
                                       80,
                                       400)]))
    self.assertEqual([PricedItem('soap', 150)], full_price)


class TestFreebies(TestCase):
  def test_not_triggered_preserve_discounts(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_triggered_not_fullfilled(self):
    basket = [PricedItem('soap', 150),
              PricedItem('conditioner', 250),
              PricedItem('conditioner', 250),
              PricedItem('conditioner', 250),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(discounted, already_discounted)
    self.assertEqual(sorted(basket), sorted(full_price))

  def test_triggered_partially_fullfilled(self):
    basket = [PricedItem('soap', 150),
              PricedItem('conditioner', 250),
              PricedItem('conditioner', 250),
              PricedItem('shampoo', 200),
              PricedItem('conditioner', 250),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(sorted(already_discounted +
                            [MultiBuy('freebies',
                                      [PricedItem('conditioner', 250),
                                       PricedItem('conditioner', 250),
                                       PricedItem('conditioner', 250),
                                       PricedItem('shampoo', 200)],
                                      200,
                                      750)]),
                     sorted(discounted)) 
    self.assertEqual(sorted([PricedItem('soap', 150),
                             PricedItem('toothpaste', 80)]),
                     sorted(full_price))

  def test_triggered_fullfilled(self):
    basket = [PricedItem('soap', 150),
              PricedItem('shampoo', 200),
              PricedItem('conditioner', 250),
              PricedItem('conditioner', 250),
              PricedItem('shampoo', 200),
              PricedItem('conditioner', 250),
              PricedItem('shampoo', 200),
              PricedItem('toothpaste', 80)]
    already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
    full_price, discounted = \
        freebies('conditioner', 3, 'shampoo', 2)(basket, already_discounted)
    self.assertEqual(sorted(discounted), 
                     sorted(already_discounted +
                            [MultiBuy('freebies',
                                      [PricedItem('conditioner', 250),
                                       PricedItem('conditioner', 250),
                                       PricedItem('conditioner', 250),
                                       PricedItem('shampoo', 200),
                                       PricedItem('shampoo', 200)],
                                      400,
                                      750)]))
    self.assertEqual(sorted([PricedItem('soap', 150),
                             PricedItem('shampoo', 200),
                             PricedItem('toothpaste', 80)]),
                    sorted(full_price))

class TestSpendXOnYGetXPrecentOff(TestCase):
    def test_not_triggered_spend_too_low(self):
        basket = [PricedItem('soap', 150),
                  PricedItem('shampoo', 200),
                  PricedItem('conditioner', 250),
                  PricedItem('conditioner', 250),
                  PricedItem('shampoo', 200),
                  PricedWeighedItem('banana', 0.454, 80, 36),
                  PricedItem('apples', 155),
                  PricedItem('toothpaste', 80)]
        fruit = ['banana', 'apples', 'grapes', 'oranges']
        already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
        full_price, discounted = \
            spend_x_on_y_get_zpc_off(fruit, 500, 0.1)(basket, already_discounted)
        self.assertEqual(sorted(already_discounted),sorted(discounted))
        self.assertEqual(sorted(basket),sorted(full_price))

    def test_triggered(self):
        basket = [PricedItem('soap', 150),
                  PricedItem('apples', 155),
                  PricedItem('apples', 155),
                  PricedItem('apples', 155),
                  PricedItem('apples', 155),
                  PricedItem('shampoo', 200),
                  PricedWeighedItem('banana', 0.454, 80, 36),
                  PricedItem('apples', 155),
                  PricedItem('toothpaste', 80)]
        fruit = ['banana', 'apples', 'grapes', 'oranges']
        already_discounted = [DiscountedItem('cheese', 100, 25, 75)]
        full_price, discounted = \
            spend_x_on_y_get_zpc_off(fruit, 50, 0.1)(basket, already_discounted)
        self.assertEqual(sorted(already_discounted + \
                                [MultiBuy('spend X on Y get Z% off',
                                         [PricedItem('apples', 155),
                                          PricedItem('apples', 155),
                                          PricedItem('apples', 155),
                                          PricedItem('apples', 155),
                                          PricedItem('apples', 155),
                                          PricedWeighedItem('banana', 0.454, 80, 36)],
                                         (155 * 5 + 36) * 0.1,
                                         (155 * 5 + 36) * 0.9
                                         )]
                                ),sorted(discounted))
        self.assertEqual(sorted([PricedItem('soap', 150),
                                 PricedItem('shampoo', 200),
                                 PricedItem('toothpaste', 80)]),
                         sorted(full_price))


if __name__ == '__main__':
  main()
