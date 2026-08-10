"""
Cleaning step for the Order-to-Cash Process Improvement Analysis project.
  1. Standardize PaymentTerms formatting
  2. Remove duplicate OrderIDs
  3. Flag credit notes (negative amounts) separately from genuine sales orders
  4. Compute stage durations: OrderToInvoiceDays, InvoiceToPaymentDays, OrderToPaymentDays
Note: orders with no InvoiceDate or PaymentDate yet are NOT dropped — they are
genuinely still open (still awaiting invoicing or payment as of the snapshot
date), which is exactly the population a real AR/DSO analysis needs to include.
"""
import pandas as pd

df = pd.read_csv("order_to_cash_raw.csv", parse_dates=["OrderDate", "InvoiceDate", "PaymentDate"])
raw_rows = len(df)

# 1) Standardize payment terms
df["PaymentTerms"] = df["PaymentTerms"].astype(str).str.strip().str.title()
df["PaymentTerms"] = df["PaymentTerms"].str.replace(r"^Net(\d)", r"Net \1", regex=True)
df["PaymentTerms"] = df["PaymentTerms"].replace({"Net30": "Net 30", "Net60": "Net 60"})

# 2) Remove duplicate OrderIDs
df = df.drop_duplicates(subset="OrderID", keep="first")
after_dedupe = len(df)

# 3) Flag credit notes
df["IsCreditNote"] = df["Amount"] < 0
credit_notes = df["IsCreditNote"].sum()

# 4) Stage durations (NaT-safe: only computed where the relevant date exists)
df["OrderToInvoiceDays"] = (df["InvoiceDate"] - df["OrderDate"]).dt.days
df["InvoiceToPaymentDays"] = (df["PaymentDate"] - df["InvoiceDate"]).dt.days
df["OrderToPaymentDays"] = (df["PaymentDate"] - df["OrderDate"]).dt.days
df["IsPaid"] = df["PaymentDate"].notna()
df["IsInvoiced"] = df["InvoiceDate"].notna()

df = df.sort_values("OrderDate").reset_index(drop=True)
df.to_csv("order_to_cash_clean.csv", index=False)

print(f"Raw rows:            {raw_rows}")
print(f"After dedupe:        {after_dedupe}  ({raw_rows - after_dedupe} duplicates removed)")
print(f"Credit notes flagged: {credit_notes} (kept, flagged, not deleted)")
print(f"Final rows:          {len(df)}")
print(f"Orders invoiced:     {df['IsInvoiced'].sum()} / {len(df)}")
print(f"Orders paid:         {df['IsPaid'].sum()} / {len(df)}")
print(f"Segments: {sorted(df['CustomerSegment'].unique())}")
