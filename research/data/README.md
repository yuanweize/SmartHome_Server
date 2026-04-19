# Research Data — Raw Datasets

This directory contains all raw data used in the thesis charts and analysis.
Every data point is stored here for reproducibility and academic transparency.

## Files

### Manually Curated
| File | Description | Source | Status |
|---|---|---|---|
| `czso_food_consumption.csv` | Czech food consumption per capita (2018–2023) | ČSÚ – Spotřeba potravin | ✅ Verified |
| `ee_frozen_market.csv` | Eastern Europe frozen F&V market size | FrozenFoodEurope.com (2025) | ✅ Verified (2023–2025), estimated (2020–2022) |
| `pricing_comparison.csv` | Product pricing: Franui vs Berrie | Rohlík.cz / proposed | ✅ Franui verified, Berrie proposed |
| `percapita_spending.csv` | Per capita frozen F&V spending (EE vs WE) | FrozenFoodEurope.com (2025) | ✅ Verified |

### Fetched from APIs (via `fetch_api_data.py`)
| File | Description | API Source | Status |
|---|---|---|---|
| `cnb_eur_czk.csv` | EUR/CZK annual average exchange rate (2018–2025) | ČNB API | ✅ Verified (live API) |
| `worldbank_gdp_ppp.csv` | GDP per capita PPP for CZ (2018–2024) | World Bank API | ✅ Verified (live API) |

## Data Provenance

### ČSÚ (Czech Statistical Office)
- **Website:** https://czso.cz
- **Publication:** Spotřeba potravin – 2023
- **Method:** Balance method (bilanční metoda)
- **Notes:** Fruit = "v hodnotě čerstvého"; ČSÚ does NOT publish "frozen fruit" as a separate category; Chocolate = "čokoláda a čokoládové cukrovinky"; Ice cream estimated from Eurostat production data

### FrozenFoodEurope.com
- **Report:** Eastern Europe Frozen Processed Fruits & Vegetables Market
- **Verified data points:** 2023 (USD 2.36 bn), 2024 (USD 2.53 bn), 2025 forecast (USD 2.64 bn)
- **Per capita:** EE = USD 8.10, WE = USD 24.00 (2024)

### Rohlík.cz
- **Product:** Franuí – Mražené maliny v čokoládě 150g
- **Price:** 159.99 Kč (verified April 19, 2026)

### Czech National Bank (ČNB)
- **Endpoint:** `https://www.cnb.cz/.../prumerne_rok.txt?rok={year}`
- **Data:** Annual average EUR/CZK exchange rates
- **Fetched programmatically:** 2026-04-19 via `fetch_api_data.py`

### World Bank Open Data
- **Endpoint:** `https://api.worldbank.org/v2/country/CZE/indicator/NY.GDP.PCAP.PP.CD`
- **Data:** GDP per capita, PPP (current international $)
- **Fetched programmatically:** 2026-04-19 via `fetch_api_data.py`

## How to Update Data
1. **API data:** Run `python3 fetch_api_data.py` (fetches fresh data from ČNB + World Bank)
2. **Manual data:** Update the CSV, add `source_status` = `verified`, note the date
3. **Regenerate charts:** Run `python3 generate_charts.py`
