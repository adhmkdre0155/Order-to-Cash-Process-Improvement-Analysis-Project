"""
Generates a simulated Order-to-Cash dataset for a B2B company selling across
three customer segments: SME, Enterprise, and Government (B2G).

Built-in realistic pattern (to be discovered, not asserted): Government orders
have a genuine bottleneck at the order-to-invoice stage (manual approval before
invoicing is even possible), on top of slower payment terms — mirroring a
real B2G sales cycle.

Intentionally messy: ~2% duplicate Order IDs, a handful of negative amounts
(credit notes / data-entry errors), inconsistent Payment Terms formatting,
and some orders with no Payment Date yet (still outstanding — a real AR
snapshot, not something to "clean away").
"""
import random
import csv
from datetime import date, timedelta

random.seed(33)

SEGMENTS = {
    "SME": {
        "share": 0.50, "terms": "Net 30", "terms_days": 30,
        "order_to_invoice_mean": 2.2, "order_to_invoice_sd": 1.2,
        "invoice_to_payment_mean": 27, "invoice_to_payment_sd": 8,
        "amount_range": (1500, 18000),
    },
    "Enterprise": {
        "share": 0.35, "terms": "Net 30", "terms_days": 30,
        "order_to_invoice_mean": 4.0, "order_to_invoice_sd": 1.8,
        "invoice_to_payment_mean": 33, "invoice_to_payment_sd": 10,
        "amount_range": (15000, 120000),
    },
    "Government": {
        "share": 0.15, "terms": "Net 60", "terms_days": 60,
        "order_to_invoice_mean": 12.5, "order_to_invoice_sd": 4.5,   # manual approval bottleneck
        "invoice_to_payment_mean": 68, "invoice_to_payment_sd": 14,
        "amount_range": (25000, 320000),
    },
}

TERMS_CASING = lambda t: random.choice([t, t.lower(), t.upper(), t.replace(" ", "")])

PERIOD_START = date(2024, 1, 1)
PERIOD_END = date(2025, 10, 31)
SNAPSHOT_DATE = date(2025, 12, 9)  # "today" for the analysis — orders after this can't have paid yet

rows = []
order_id = 500000

N_ORDERS = 4200
for _ in range(N_ORDERS):
    order_id += 1
    seg_name = random.choices(list(SEGMENTS.keys()),
                                weights=[s["share"] for s in SEGMENTS.values()], k=1)[0]
    cfg = SEGMENTS[seg_name]

    order_date = PERIOD_START + timedelta(days=random.randint(0, (PERIOD_END - PERIOD_START).days))

    o2i_days = max(0, round(random.gauss(cfg["order_to_invoice_mean"], cfg["order_to_invoice_sd"])))
    invoice_date = order_date + timedelta(days=o2i_days)

    i2p_days = max(1, round(random.gauss(cfg["invoice_to_payment_mean"], cfg["invoice_to_payment_sd"])))
    payment_date = invoice_date + timedelta(days=i2p_days)

    amount = round(random.uniform(*cfg["amount_range"]), 2)

    # ~4% credit note / data-entry error (negative amount)
    if random.random() < 0.04:
        amount = -abs(round(amount * random.uniform(0.05, 0.3), 2))

    terms_raw = TERMS_CASING(cfg["terms"]) if random.random() < 0.2 else cfg["terms"]

    # Orders not yet paid by the snapshot date are genuinely still outstanding
    payment_date_val = payment_date.strftime("%Y-%m-%d") if payment_date <= SNAPSHOT_DATE else ""
    invoice_date_val = invoice_date.strftime("%Y-%m-%d") if invoice_date <= SNAPSHOT_DATE else ""

    rows.append([order_id, order_date.strftime("%Y-%m-%d"), invoice_date_val, payment_date_val,
                 seg_name, amount, terms_raw])

# Inject ~2% duplicate Order IDs (system export error)
dupes = random.sample(rows, int(N_ORDERS * 0.02))
rows.extend(dupes)
random.shuffle(rows)

header = ["OrderID", "OrderDate", "InvoiceDate", "PaymentDate", "CustomerSegment", "Amount", "PaymentTerms"]
with open("order_to_cash_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

print(f"Generated {len(rows)} raw order rows.")
