"""Run from any directory; all inputs/outputs resolve relative to the repository."""
from pathlib import Path
import csv,json,random
from model import evaluate
ROOT=Path(__file__).resolve().parents[1]

def save_csv(path,rows):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator="\n");writer.writeheader();writer.writerows(rows)

def run():
    config=json.loads((ROOT/'data/assumptions.json').read_text())
    out=ROOT/'results';out.mkdir(exist_ok=True)
    cases=[];annual=[]
    for name,inputs in config['cases'].items():
        result=evaluate(inputs);years=result.pop('years');cases.append(dict(scenario=name,**result))
        annual.extend(dict(scenario=name,**year) for year in years)
    save_csv(out/'scenarios.csv',cases);save_csv(out/'annual_cashflows.csv',annual)
    base=config['cases']['base'];sensitivity=[]
    for availability in [.4,.5,.6,.7,.8,.9]:
        for price in [18,20,22,24,26,28,30]:
            result=evaluate(dict(base,availability=availability,invoice_price_kg=price))
            sensitivity.append(dict(availability=availability,invoice_price_kg=price,sold_kg=result['sold_kg'],operating_contribution_usd=result['operating_contribution_usd']))
    save_csv(out/'price_utilization.csv',sensitivity)
    sim=config['simulation'];rng=random.Random(sim['seed']);draws=[]
    for draw in range(sim['draws']):
        params={k:rng.triangular(v[0],v[2],v[1]) for k,v in sim['triangular_min_mode_max'].items()}
        res=evaluate(dict(base,**params))
        draws.append(dict(draw=draw,**params,operating_contribution_usd=res['operating_contribution_usd'],npv_5y_usd=res['npv_5y_usd']))
    save_csv(out/'simulation.csv',draws)
    profits=sorted(x['operating_contribution_usd'] for x in draws)
    def quantile(p):
        position=(len(profits)-1)*p;lo=int(position);hi=min(lo+1,len(profits)-1)
        return profits[lo]+(position-lo)*(profits[hi]-profits[lo])
    summary=dict(label='Illustrative independent triangular input draws; not calibrated commercial probabilities',seed=sim['seed'],draws=len(draws),operating_profit_p10_usd=quantile(.1),operating_profit_p50_usd=quantile(.5),operating_profit_p90_usd=quantile(.9),fraction_positive_operating=sum(v>0 for v in profits)/len(profits),fraction_positive_npv=sum(d['npv_5y_usd']>0 for d in draws)/len(draws))
    (out/'simulation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# Illustrative model results','', 'Generated from `data/assumptions.json`. These are hypothetical scenarios, not observed company performance or forecasts.','', '| Case | Sold kg/year | Binding constraint | Unit contribution | Annual operating contribution | Five-year NPV | Break-even feasible |','|---|---:|---|---:|---:|---:|---|']
    for x in cases:
        lines.append(f"| {x['scenario']} | {x['sold_kg']:,.0f} | {x['bottleneck']} | ${x['contribution_kg']:,.2f}/kg | ${x['operating_contribution_usd']:,.0f} | ${x['npv_5y_usd']:,.0f} | {x['break_even_feasible']} |")
    lines+=['','## Interpreting the scenarios','', 'Changes across cases reflect multiple assumptions together; this is not a causal decomposition. NPV includes initial and maintenance capital, the five-year ramp, working-capital changes and final recovery, with no terminal business value.','',f"Simulation operating contribution p10 / median / p90: ${quantile(.1):,.0f} / ${quantile(.5):,.0f} / ${quantile(.9):,.0f}. Positive operating contribution occurs in {summary['fraction_positive_operating']:.1%} of illustrative draws. This frequency depends on the chosen independent distributions; it is not a validated probability of success."]
    (out/'summary.md').write_text('\n'.join(lines)+'\n')
    print('Generated scenarios, annual cashflows, sensitivity, simulation and summary.')
if __name__=='__main__':run()
