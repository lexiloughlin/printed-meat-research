# Edit, reproduce, and extend

Open this repository folder in VS Code. Use Python 3.12, create a virtual environment, and install `requirements.txt` as shown in the README. The financial runner requires no third-party packages.

1. Change assumptions in `data/assumptions.json`, retaining explicit status and units. Replace illustrative inputs only with dated evidence and a documented scope.
2. Run `python analysis/run_analysis.py` to regenerate tables and the summary.
3. Run `python analysis/plot_commercial.py` to regenerate the three financial exhibits.
4. Run `python -m unittest discover -s tests -v`.
5. Open and run `notebooks/commercial-analysis.ipynb` top-to-bottom; save outputs.
6. For historical charts, run `python analysis/make_charts.py` and review their evidence warnings.
7. Commit inputs, scripts, narrative changes, and regenerated results together. Never manually edit a generated result to fit a conclusion.

`data/evidence_ledger.csv` is the reviewed-source register. Legacy CSVs preserve historical claims and are not all freshly verified. Add source IDs and review dates to research updates. Record failed access, contrary evidence, changing product definitions, and plan/actual distinctions.

The GitHub Pages file in `docs/index.html` is the inherited presentation, with a prominent notice linking to the expanded research. The new analytical content is designed first for GitHub Markdown and VS Code notebooks. It is not a newly deployed web dashboard.

## Suggested GitHub workflow

Create a feature branch, review the changes and generated output, commit, and open a pull request against `main`. The included workflow reruns financial tests and checks that committed tabular outputs reproduce. Reproduce plots locally and inspect them before presenting.
