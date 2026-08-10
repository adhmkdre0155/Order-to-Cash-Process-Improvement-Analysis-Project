# Order-to-Cash Process Improvement Analysis

**Business Analyst portfolio project — Adham AlHers**
[Live interactive dashboard](/dashboard/index.html) · [LinkedIn](https://www.linkedin.com/in/adhamalhers/) · [Portfolio home](#)

## Problem statement
A B2B company's Order-to-Cash cycle (order → invoice → payment) is too slow, hurting cash flow — and leadership wants to know where the delay actually comes from before proposing a fix.

## Business context
Directly builds on real B2B deal-closing and account-management experience — this project reframes hands-on B2B/B2G sales-cycle experience (including closing government-sector deals) into a formal Business Analyst case study.

## Dataset
A simulated Order-to-Cash dataset (4,200 cleaned orders, 2024–2025) across three customer segments — **SME**, **Enterprise**, and **Government** — with Order/Invoice/Payment dates, Amount, and Payment Terms. Generated with a genuine, discoverable bottleneck (a manual approval step specific to government contracts) rather than a scripted conclusion — see `data/generate_data.py`.

## Tools
Excel (openpyxl, formula-driven) · SQL (SQLite) · Python (matplotlib) for the process swimlane diagrams · Chart.js for the interactive dashboard.

## Repository structure
```
├── data/
│   ├── generate_data.py               # Generates the raw simulated dataset
│   ├── clean_data.py                  # Standardizes terms, dedupes, flags credit notes, computes stage durations
│   ├── order_to_cash_raw.csv
│   └── order_to_cash_clean.csv
├── sql/
│   └── queries.sql                    # DSO by segment, stage bottleneck analysis, cash-flow scenario
├── excel/
│   └── Order_to_Cash_Dashboard.xlsx   # Formula-driven KPI dashboard with charts
├── dashboard/
│   └── index.html                     # Self-contained interactive web dashboard
├── diagrams/
│   ├── process_current_state.png      # Current Government O2C process, bottleneck highlighted
│   └── process_future_state.png       # Proposed automated-validation process
└── docs/
    └── findings_recommendation.docx/.pdf
```

## Step-by-step approach
1. **Calculated DSO and stage cycle-times** in both Excel (formula-driven, SUMIFS/AVERAGEIFS) and SQL — order-to-invoice and invoice-to-payment, split by customer segment.
2. **Segmented by customer type** to isolate which segment drives the longest delays — Government stood out immediately, both in cycle time and in the value of outstanding receivables.
3. **Mapped the current process** as a swimlane diagram, and identified the highest-friction handoff: a manual approval step exclusive to government contracts, adding 10.4 days *before the invoice is even issued* — separate from and in addition to government's inherently slower payment cycle.
4. **Proposed a redesigned process** [Future state process map](/diagrams/process_future_state.png) with an automated validation point replacing the manual approval step, and modeled the cash-flow impact of the resulting DSO reduction.

## Key insight
Government segment DSO (66.8 days) is more than double SME's (26.6 days) — but the gap doesn't start with government's payment behavior, which the company can't control. It starts with a 12.6-day order-to-invoice delay (vs. 2.2 days for SME) caused by an internal manual approval step — something the company fully controls. €6.84M currently sits in outstanding Government receivables, over 90% of all outstanding AR company-wide, despite Government being only 15% of order volume.

## Recommendation
Automate invoice validation against the PO and contract terms for government orders, removing the manual approval step and targeting invoice issuance in under 3 days — without touching the external, unchangeable government payment-run timeline.

## Cash-flow impact
Reducing the Government segment's order-to-invoice delay by just 7 days frees an estimated **€1,103,172** in working capital, based on Government's average daily revenue over the analysis period (~€157,000/day) — a concrete, quantified number tied to a specific, internally-controllable process fix.

## Business impact
The strongest project in this portfolio to link directly to existing BD/account-management experience — it demonstrates the ability to formalize real commercial pattern-recognition (knowing government deals move slowly) into a rigorous, quantified process analysis with a specific, implementable fix.

---
*Dataset is simulated for portfolio purposes. The bottleneck and cash-flow figures are computed directly from the simulation, not scripted into the summary — see the SQL queries and Excel workbook for full reproducibility.*
