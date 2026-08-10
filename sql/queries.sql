-- ============================================================
-- Order-to-Cash Process Improvement Analysis — Queries
-- Table: orders (loaded from order_to_cash_clean.csv)
-- Excludes credit notes (IsCreditNote=0) from cycle-time analysis —
-- negative-amount rows are refunds, not sales orders, and would distort DSO.
-- ============================================================

-- 1. Cycle time per stage by customer segment (core diagnostic query)
SELECT
    CustomerSegment,
    COUNT(*) AS Orders,
    ROUND(AVG(OrderToInvoiceDays), 1) AS AvgOrderToInvoiceDays,
    ROUND(AVG(InvoiceToPaymentDays), 1) AS AvgInvoiceToPaymentDays,
    ROUND(AVG(OrderToPaymentDays), 1) AS AvgTotalCycleDays
FROM orders
WHERE IsCreditNote = 0 AND IsPaid = 1
GROUP BY CustomerSegment
ORDER BY AvgTotalCycleDays DESC;

-- 2. Days Sales Outstanding (DSO) by segment
--    DSO = (Total Accounts Receivable / Total Credit Sales) x Days in Period
--    Approximated here as average InvoiceToPaymentDays weighted by order value
SELECT
    CustomerSegment,
    ROUND(SUM(Amount * InvoiceToPaymentDays) / SUM(Amount), 1) AS DSO_ValueWeighted,
    ROUND(AVG(InvoiceToPaymentDays), 1) AS DSO_SimpleAverage
FROM orders
WHERE IsCreditNote = 0 AND IsPaid = 1
GROUP BY CustomerSegment
ORDER BY DSO_ValueWeighted DESC;

-- 3. Bottleneck identification: which stage contributes most to Government's
--    longer cycle, relative to the fastest segment (SME)?
WITH stage_avgs AS (
    SELECT
        CustomerSegment,
        AVG(OrderToInvoiceDays) AS AvgO2I,
        AVG(InvoiceToPaymentDays) AS AvgI2P
    FROM orders
    WHERE IsCreditNote = 0 AND IsPaid = 1
    GROUP BY CustomerSegment
)
SELECT
    CustomerSegment,
    ROUND(AvgO2I, 1) AS AvgOrderToInvoiceDays,
    ROUND(AvgO2I - (SELECT AvgO2I FROM stage_avgs WHERE CustomerSegment='SME'), 1) AS O2I_GapVsSME,
    ROUND(AvgI2P, 1) AS AvgInvoiceToPaymentDays,
    ROUND(AvgI2P - (SELECT AvgI2P FROM stage_avgs WHERE CustomerSegment='SME'), 1) AS I2P_GapVsSME
FROM stage_avgs
ORDER BY AvgO2I DESC;

-- 4. Outstanding (unpaid) receivables by segment, as of the snapshot date —
--    this is the actual cash currently tied up
SELECT
    CustomerSegment,
    COUNT(*) AS OpenOrders,
    ROUND(SUM(Amount), 0) AS OutstandingAR
FROM orders
WHERE IsCreditNote = 0 AND IsPaid = 0
GROUP BY CustomerSegment
ORDER BY OutstandingAR DESC;

-- 5. Cash-flow impact scenario: working capital freed by reducing Government's
--    order-to-invoice delay (the identified bottleneck) by 7 days
WITH gov AS (
    SELECT SUM(Amount) AS TotalGovRevenue, COUNT(*) AS GovOrders
    FROM orders WHERE CustomerSegment = 'Government' AND IsCreditNote = 0 AND IsPaid = 1
),
period AS (
    SELECT JULIANDAY(MAX(OrderDate)) - JULIANDAY(MIN(OrderDate)) AS PeriodDays
    FROM orders WHERE CustomerSegment = 'Government'
)
SELECT
    ROUND(gov.TotalGovRevenue, 0) AS TotalGovRevenueInPeriod,
    ROUND(period.PeriodDays, 0) AS PeriodDays,
    ROUND(gov.TotalGovRevenue / period.PeriodDays, 0) AS AvgDailyGovRevenue,
    ROUND((gov.TotalGovRevenue / period.PeriodDays) * 7, 0) AS WorkingCapitalFreed_7DayReduction
FROM gov, period;

-- 6. Overall company DSO (all segments blended) vs. Government-only, for the
--    executive summary comparison
SELECT
    'All Segments' AS Scope,
    ROUND(SUM(Amount * InvoiceToPaymentDays) / SUM(Amount), 1) AS DSO
FROM orders WHERE IsCreditNote = 0 AND IsPaid = 1
UNION ALL
SELECT
    'Government Only' AS Scope,
    ROUND(SUM(Amount * InvoiceToPaymentDays) / SUM(Amount), 1) AS DSO
FROM orders WHERE IsCreditNote = 0 AND IsPaid = 1 AND CustomerSegment = 'Government';
