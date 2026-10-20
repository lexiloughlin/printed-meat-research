"""Illustrative annual plant-based food manufacturing model. Standard library only."""
import math

def validate(a):
    fractions = ['serviceable_fraction','capture_fraction','availability','performance','quality_yield']
    for key in fractions:
        if not 0 < a[key] <= 1: raise ValueError(f'{key} must be in (0,1]')
    if not 0 <= a['channel_deduction'] < 1: raise ValueError('invalid channel deduction')
    for key in ['accounts','kg_per_account_week','selling_weeks','rate_kg_hour','shifts','hours_per_shift','production_days','invoice_price_kg','input_conversion_cost_kg','pack_logistics_kg','fixed_cost_year','initial_capital','maintenance_capital_year','receivable_days','inventory_days','payable_days','discount_rate']:
        if not math.isfinite(a[key]) or a[key] < 0: raise ValueError(f'invalid {key}')
    if len(a['ramp']) != 5 or any(not 0 <= x <= 1 for x in a['ramp']): raise ValueError('five ramp fractions required')

def evaluate(a):
    validate(a)
    ceiling=a['accounts']*a['kg_per_account_week']*a['selling_weeks']
    serviceable=ceiling*a['serviceable_fraction']
    demand=serviceable*a['capture_fraction']
    capacity=a['rate_kg_hour']*a['shifts']*a['hours_per_shift']*a['production_days']*a['availability']*a['performance']*a['quality_yield']
    sold=min(demand,capacity)
    price=a['invoice_price_kg']*(1-a['channel_deduction'])
    unit_cost=a['input_conversion_cost_kg']/a['quality_yield']+a['pack_logistics_kg']
    contribution=price-unit_cost
    revenue=sold*price
    operating=sold*contribution-a['fixed_cost_year']
    be=a['fixed_cost_year']/contribution if contribution>0 else None
    working_capital=revenue*a['receivable_days']/365+sold*unit_cost*(a['inventory_days']-a['payable_days'])/365
    years=[];previous_wc=0;npv=-a['initial_capital'];cumulative=-a['initial_capital'];payback=None
    for year,ramp in enumerate(a['ramp'],1):
        wc=working_capital*ramp
        op=sold*ramp*contribution-a['fixed_cost_year']
        fcf=op-(wc-previous_wc)-a['maintenance_capital_year']
        if year==len(a['ramp']):fcf+=wc
        npv+=fcf/(1+a['discount_rate'])**year
        cumulative+=fcf
        if payback is None and cumulative>=0:payback=year
        years.append(dict(year=year,ramp=ramp,sold_kg=sold*ramp,revenue_usd=revenue*ramp,operating_contribution_usd=op,working_capital_usd=wc,free_cash_flow_usd=fcf,cumulative_cash_usd=cumulative))
        previous_wc=wc
    return dict(territory_ceiling_kg=ceiling,serviceable_demand_kg=serviceable,obtainable_demand_kg=demand,capacity_kg=capacity,sold_kg=sold,bottleneck='demand' if demand<=capacity else 'capacity',net_price_kg=price,variable_cost_kg=unit_cost,contribution_kg=contribution,revenue_usd=revenue,operating_contribution_usd=operating,break_even_kg=be,break_even_feasible=be is not None and be<=sold,working_capital_usd=working_capital,npv_5y_usd=npv,payback_year=payback,years=years)
