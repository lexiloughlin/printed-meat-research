from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
def rows(name):
    with (ROOT/'results'/name).open() as f:return list(csv.DictReader(f))
def finish(fig,name):
    fig.text(.02,.01,'ILLUSTRATIVE | Source: data/assumptions.json; not observed results or forecasts.',fontsize=9,color='#555555')
    fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(ROOT/'charts'/name,dpi=160);plt.close(fig)
s=rows('scenarios.csv');fig,ax=plt.subplots(figsize=(9,4.8))
values=[float(x['operating_contribution_usd'])/1000 for x in s]
ax.bar([x['scenario'].title() for x in s],values,color=['#c38a46','#405f75','#405f75'])
for i,v in enumerate(values):ax.annotate(f'${v:,.0f}k',(i,v),xytext=(0,7 if v>=0 else -17),textcoords='offset points',ha='center')
ax.set_ylim(min(values)-180,max(values)+200);ax.axhline(0,color='#333',linewidth=.8);ax.set_ylabel('Annual operating contribution (USD thousands)');ax.set_title('Scenario economics depend on demand and unit contribution',loc='left',pad=20)
finish(fig,'scenario_operating_profit.png')
s=rows('price_utilization.csv');prices=sorted({float(x['invoice_price_kg']) for x in s});availability=sorted({float(x['availability']) for x in s})
matrix=[[next(float(x['operating_contribution_usd'])/1000 for x in s if float(x['availability'])==a and float(x['invoice_price_kg'])==p) for p in prices] for a in availability]
fig,ax=plt.subplots(figsize=(10,5.3));limit=max(abs(v) for row in matrix for v in row)
im=ax.imshow(matrix,cmap='PuOr',vmin=-limit,vmax=limit,aspect='auto',origin='lower')
for i,row in enumerate(matrix):
    for j,v in enumerate(row):ax.text(j,i,f'{v:,.0f}',ha='center',va='center',color='white' if abs(v)>limit*.6 else 'black',fontsize=9)
ax.set_xticks(range(len(prices)),[f'${p:.0f}' for p in prices]);ax.set_yticks(range(len(availability)),[f'{a:.0%}' for a in availability]);ax.set_xlabel('Invoice price (USD/kg), before channel deductions');ax.set_ylabel('Availability: running / scheduled time');ax.set_title('Price–availability sensitivity: annual operating contribution ($000)',loc='left',pad=15)
fig.colorbar(im,ax=ax,label='USD thousands');finish(fig,'price_utilization.png')
s=rows('simulation.csv');fig,ax=plt.subplots(figsize=(9,4.8));values=[float(x['operating_contribution_usd'])/1000 for x in s]
ax.hist(values,bins=45,color='#405f75',edgecolor='#faf9f5');ax.axvline(0,color='#a34e47',linestyle='--',label='Zero operating contribution');ax.set_xlabel('Annual operating contribution (USD thousands)');ax.set_ylabel('Number of illustrative draws');ax.set_title('10,000 draws from assumed independent input distributions',loc='left',pad=15);ax.legend(frameon=False);finish(fig,'simulated_profit.png')
