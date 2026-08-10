# 📋 Order-to-Cash Process Improvement Analysis

**Type:** Business Analyst project · **Tools:** Excel, SQL, process mapping · **Status:** Complete

[🔗 Live interactive dashboard](#) · [🔗 GitHub repository](#) · [📄 Findings & Recommendation (PDF)](#) · [🗺️ Process maps](#)

---

### The problem
A B2B company's Order-to-Cash cycle is too slow, hurting cash flow — leadership wants to know where the delay actually comes from before proposing a fix.

### Business context
This is the project that connects most directly to real BD/account-management experience — closing B2B and B2G deals firsthand means already understanding *why* government contracts move slowly. This project formalizes that pattern recognition into a rigorous, quantified analysis.

### What I did
1. **Calculated DSO and stage cycle-times** (order-to-invoice, invoice-to-payment) by customer segment, in both Excel and SQL.
2. **Segmented by customer type** — Government stood out immediately in both cycle time and outstanding receivables value.
3. **Mapped the current process** end-to-end and identified the real bottleneck: a manual approval step exclusive to government contracts.
4. **Proposed a redesigned process** with an automation point, and modeled the exact cash-flow impact of the fix.

### 🔑 Key insight
> Government DSO (66.8 days) is more than double SME's (26.6 days) — but the gap doesn't start with government's payment behavior, which the company can't control. It starts with a **12.6-day order-to-invoice delay** (vs. 2.2 days for SME) caused by an *internal* manual approval step. €6.84M currently sits in outstanding Government receivables — over 90% of all outstanding AR, despite Government being only 15% of order volume.

### Recommendation
Automate invoice validation against the PO and contract terms for government orders, removing the manual approval step — without touching the external, unchangeable government payment-run timeline.

### Cash-flow impact
Reducing the order-to-invoice delay by 7 days frees an estimated **€1,103,172** in working capital.

### Business impact
The strongest project in this portfolio to link directly to existing BD experience — it shows I'm not starting from zero on business acumen, I'm formalizing skills I already have into rigorous BA methodology.

---

**CV / LinkedIn bullet:**
*Analyzed an Order-to-Cash cycle across 3 customer segments; identified that a government-specific manual approval step (not payment behavior) was the primary bottleneck, and proposed a redesign projected to reduce DSO by 7 days, freeing €1.1M in working capital.*

**Skills demonstrated:** DSO/cycle-time analysis · SQL · Excel (formula-driven dashboards) · Process/swimlane mapping · Root-cause bottleneck identification · Cash-flow impact modeling
