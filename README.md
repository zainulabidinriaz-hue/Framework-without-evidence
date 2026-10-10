# Frameworks Without Evidence? — Supplementary Material

Code and data for the article *"Frameworks Without Evidence? A Validation Audit of Agentic AI Security Frameworks and a Formal Analysis of Runtime Trust Scoring"* by Zain Ul Abidin Riaz et al.

## Files

| File | What it contains |
| --- | --- |
| `trust_sim.py` | Simulation script that produces every number in Tables 4 and 5 and in Figure 1 of the article. |
| `results.json` | The exact output of `trust_sim.py`, so results can be checked without running the code. |
| `audit_coding_sheet.csv` | The validation audit (Table 2): each of the 50 framework–criterion scores (Y / P / N) with the supporting quotation or note from the audited paper. |

## Reproducing the results

Requirements: Python 3.9 or later and NumPy.

```bash
pip install numpy
python trust_sim.py
```

The script uses a fixed random seed (20261010), so it writes a `results.json` identical to the one in this repository. It takes a few minutes on an ordinary laptop.

## Citation

If you use this material, please cite the article (citation details will be added on publication).
