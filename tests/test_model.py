import sys,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from model import evaluate
class EconomicsTests(unittest.TestCase):
    def setUp(self):self.a=json.loads((ROOT/'data/assumptions.json').read_text())['cases']['base']
    def test_demand_and_capacity_bounds(self):
        x=evaluate(self.a)
        self.assertLessEqual(x['sold_kg'],x['capacity_kg']);self.assertLessEqual(x['sold_kg'],x['obtainable_demand_kg'])
        self.assertAlmostEqual(x['sold_kg'],86400)
    def test_cash_reconciles_with_recovered_working_capital(self):
        x=evaluate(self.a)
        expected=sum(y['operating_contribution_usd'] for y in x['years'])-5*self.a['maintenance_capital_year']
        self.assertAlmostEqual(sum(y['free_cash_flow_usd'] for y in x['years']),expected)
    def test_negative_unit_margin_has_no_break_even(self):
        x=evaluate(dict(self.a,invoice_price_kg=1))
        self.assertIsNone(x['break_even_kg']);self.assertFalse(x['break_even_feasible'])
    def test_yield_loss_reduces_output_and_increases_cost(self):
        high=evaluate(self.a);low=evaluate(dict(self.a,quality_yield=.5))
        self.assertLess(low['capacity_kg'],high['capacity_kg']);self.assertGreater(low['variable_cost_kg'],high['variable_cost_kg'])
    def test_demand_bound_higher_availability_cannot_add_sales(self):
        self.assertAlmostEqual(evaluate(self.a)['sold_kg'],evaluate(dict(self.a,availability=.9))['sold_kg'])
    def test_npv_matches_explicit_discount(self):
        x=evaluate(self.a)
        expected=-self.a['initial_capital']+sum(y['free_cash_flow_usd']/(1+self.a['discount_rate'])**y['year'] for y in x['years'])
        self.assertAlmostEqual(x['npv_5y_usd'],expected)
    def test_invalid_fraction_rejected(self):
        with self.assertRaises(ValueError):evaluate(dict(self.a,quality_yield=0))
    def test_changing_price_preserves_physical_capacity(self):
        self.assertEqual(evaluate(self.a)['capacity_kg'],evaluate(dict(self.a,invoice_price_kg=30))['capacity_kg'])
if __name__=='__main__':unittest.main()
