# Sprint 6 Day 43 Performance Notes

## Load Test

### Objective
Execute 10 concurrent requests to the Screener API.

### Results

| Metric | Value |
|--------|------:|
| Concurrent Requests | 10 |
| Total Execution Time | 0.197 s |
| Average Response Time | 0.152 s |
| Maximum Response Time | 0.196 s |

Result: PASS

---

## Company Profile Performance

| Company | Response Time |
|---------|--------------:|
| TCS | 0.032 s |
| INFY | 0.009 s |
| HCLTECH | 0.008 s |
| RELIANCE | 0.010 s |
| HDFCBANK | 0.009 s |

Requirement:
< 3 seconds

Result: PASS

---

## End-to-End Integration

FastAPI:
- Running on port 8000

Streamlit:
- Running on port 8501

Results:
- No port conflicts observed.
- Dashboard loaded successfully.
- Dashboard successfully retrieved API data.

Result: PASS

---

## SQLite Optimisations

Indexes added:

- profitandloss(company_id, year)
- balancesheet(company_id, year)
- cashflow(company_id, year)
- financial_ratios(company_id, year)
- computed_financial_ratios(company_id, year)
- stock_prices(company_id, date)
- documents(company_id, year)
- peer_percentiles(company_id, year)
- sectors(company_id)

Result:
Query performance improved through indexed lookups on frequently filtered columns.

---

## Performance Bottlenecks

No significant bottlenecks were observed during testing.

All API endpoints responded well within the required performance thresholds.