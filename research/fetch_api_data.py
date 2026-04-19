#!/usr/bin/env python3
"""
fetch_api_data.py — Fetch real data from free public APIs

APIs used (all free, no authentication required):
  1. Eurostat (JSON-stat) — CZ food price index (HICP)
  2. Czech National Bank (ČNB) — EUR/CZK exchange rates
  3. World Bank — GDP per capita PPP for Czech Republic

Each API call saves raw data to research/data/ as CSV.
Only data RELEVANT to the thesis is fetched:
  - Food CPI → pricing context for Berrie
  - EUR/CZK → import cost pressure on Franui (supports local production argument)
  - GDP PPP → purchasing power context for price sensitivity analysis
"""

import requests
import csv
import json
import sys
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TIMEOUT = 30  # seconds


def fetch_eurostat_food_cpi():
    """
    Eurostat HICP (Harmonised Index of Consumer Prices) for food in CZ.
    Dataset: prc_hicp_aind (annual average index, 2015=100)
    Coicop: CP0112 (Meat), CP0116 (Fruit), CP0118 (Sugar/chocolate/confectionery)
    
    WHY: Shows food price inflation trends — directly relevant for:
    - Justifying Berrie's pricing strategy
    - Understanding consumer price sensitivity context
    """
    print("  Fetching Eurostat HICP food prices for CZ...")
    
    # Annual average rate of change, CZ, food sub-categories
    # prc_hicp_ainr replaced discontinued prc_hicp_aind
    url = (
        "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
        "prc_hicp_ainr?"
        "geo=CZ&"
        "coicop=CP0116,CP0118,CP011&"  # Fruit, Sugar/choc/confect, Food
        "unit=RCH_A_AVG&"  # Annual rate of change
        "sinceTimePeriod=2018&"
        "untilTimePeriod=2024"
    )
    
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        
        # Parse JSON-stat format
        time_labels = data['dimension']['time']['category']['label']
        coicop_labels = data['dimension']['coicop']['category']['label']
        coicop_index = data['dimension']['coicop']['category']['index']
        time_index = data['dimension']['time']['category']['index']
        values = data['value']
        
        n_coicop = len(coicop_index)
        n_time = len(time_index)
        
        rows = []
        for coicop_code, coicop_label in coicop_labels.items():
            ci = coicop_index[coicop_code]
            for time_code, time_label in time_labels.items():
                ti = time_index[time_code]
                # JSON-stat flat index
                flat_idx = str(ci * n_time + ti)
                val = values.get(flat_idx, None)
                rows.append({
                    'year': time_code,
                    'category_code': coicop_code,
                    'category': coicop_label,
                    'index_2015_100': val,
                    'source': 'Eurostat prc_hicp_aind'
                })
        
        outpath = DATA_DIR / "eurostat_food_cpi.csv"
        with open(outpath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['year', 'category_code', 'category', 'index_2015_100', 'source'])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"    ✅ Saved {len(rows)} rows → {outpath.name}")
        return True
        
    except Exception as e:
        print(f"    ❌ Eurostat HICP failed: {e}")
        return False


def fetch_cnb_exchange_rates():
    """
    Czech National Bank — annual average EUR/CZK exchange rate.
    
    WHY: Franui is imported from Spain (EUR zone). A weakening CZK makes
    imports more expensive → strengthens the argument for a locally
    produced alternative (Berrie). Directly relevant for pricing chapter.
    """
    print("  Fetching ČNB EUR/CZK exchange rates...")
    
    # ČNB provides a simple text API for daily rates
    # We'll fetch annual averages by querying the yearly average endpoint
    url = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/prumerne_rok.txt?rok={year}"
    
    rows = []
    for year in range(2018, 2026):
        try:
            resp = requests.get(url.format(year=year), timeout=TIMEOUT)
            resp.raise_for_status()
            text = resp.text
            
            for line in text.split('\n'):
                if 'EUR' in line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        rate = float(parts[4].replace(',', '.').strip())
                        rows.append({
                            'year': year,
                            'currency_pair': 'EUR/CZK',
                            'avg_rate': rate,
                            'source': 'CNB'
                        })
                        break
        except Exception as e:
            print(f"    ⚠ ČNB {year}: {e}")
    
    if rows:
        outpath = DATA_DIR / "cnb_eur_czk.csv"
        with open(outpath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['year', 'currency_pair', 'avg_rate', 'source'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"    ✅ Saved {len(rows)} rows → {outpath.name}")
        return True
    else:
        print("    ❌ No ČNB data retrieved")
        return False


def fetch_worldbank_gdp():
    """
    World Bank — GDP per capita (PPP, current international $) for CZ.
    
    WHY: Purchasing power context for PSM analysis. If GDP PPP is growing,
    consumers can afford premium products → supports market entry thesis.
    """
    print("  Fetching World Bank GDP PPP per capita for CZ...")
    
    url = (
        "https://api.worldbank.org/v2/country/CZE/indicator/"
        "NY.GDP.PCAP.PP.CD?format=json&date=2018:2024&per_page=10"
    )
    
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        
        if len(data) < 2 or not data[1]:
            print("    ❌ World Bank returned no data")
            return False
        
        rows = []
        for entry in data[1]:
            if entry['value'] is not None:
                rows.append({
                    'year': entry['date'],
                    'gdp_ppp_per_capita_usd': round(entry['value'], 2),
                    'country': 'CZ',
                    'source': 'World Bank NY.GDP.PCAP.PP.CD'
                })
        
        rows.sort(key=lambda x: x['year'])
        
        outpath = DATA_DIR / "worldbank_gdp_ppp.csv"
        with open(outpath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['year', 'gdp_ppp_per_capita_usd', 'country', 'source'])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"    ✅ Saved {len(rows)} rows → {outpath.name}")
        return True
        
    except Exception as e:
        print(f"    ❌ World Bank failed: {e}")
        return False


def fetch_eurostat_fruit_trade():
    """
    Eurostat — CZ imports of frozen fruit (HS 0811) from SDMX API.
    Dataset: ext_st_28msbgn2 (EU trade since 2002 by HS2-HS4)
    
    WHY: Proves that CZ imports substantial volumes of frozen fruit,
    demonstrating domestic demand that a local producer could capture.
    """
    print("  Fetching Eurostat CZ frozen fruit imports (HS 0811)...")
    
    # Try the main Eurostat statistics API with trade dataset
    url = (
        "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
        "DS-045409?"
        "REPORTER=CZ&"
        "PARTNER=WORLD&"
        "PRODUCT=0811&"
        "FLOW=1&"
        "INDICATORS=VALUE_IN_EUROS&"
        "freq=A&"
        "sinceTimePeriod=2018&"
        "untilTimePeriod=2024"
    )
    
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        
        time_labels = data['dimension']['time']['category']['label']
        time_index = data['dimension']['time']['category']['index']
        values = data['value']
        
        rows = []
        for time_code, time_label in time_labels.items():
            ti = time_index[time_code]
            val = values.get(str(ti), None)
            if val is not None:
                rows.append({
                    'year': time_code,
                    'product': 'HS 0811 (frozen fruit)',
                    'flow': 'import',
                    'value_eur': val,
                    'reporter': 'CZ',
                    'partner': 'WORLD',
                    'source': 'Eurostat DS-045409'
                })
        
        rows.sort(key=lambda x: x['year'])
        
        outpath = DATA_DIR / "eurostat_cz_frozen_fruit_imports.csv"
        with open(outpath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['year', 'product', 'flow', 'value_eur', 'reporter', 'partner', 'source'])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"    ✅ Saved {len(rows)} rows → {outpath.name}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"    ⚠ Eurostat trade API returned {e.response.status_code}, trying alternative...")
    except Exception as e:
        print(f"    ⚠ Eurostat trade: {e}")
    
    # If the specific trade dataset fails, note it
    print("    ℹ Eurostat Comext trade data requires specific DS- dataset codes.")
    print("      Manual download available at: https://ec.europa.eu/eurostat/databrowser")
    return False


if __name__ == "__main__":
    print("=" * 60)
    print("  API DATA FETCHER — Thesis Research")
    print(f"  Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    results = {}
    
    print("\n[1/4] Eurostat — Food CPI (HICP)")
    results['eurostat_cpi'] = fetch_eurostat_food_cpi()
    
    print("\n[2/4] ČNB — EUR/CZK Exchange Rate")
    results['cnb_fx'] = fetch_cnb_exchange_rates()
    
    print("\n[3/4] World Bank — GDP PPP per capita")
    results['worldbank_gdp'] = fetch_worldbank_gdp()
    
    print("\n[4/4] Eurostat — Frozen fruit imports (HS 0811)")
    results['eurostat_trade'] = fetch_eurostat_fruit_trade()
    
    print("\n" + "=" * 60)
    print("  RESULTS:")
    for name, ok in results.items():
        status = "✅ OK" if ok else "❌ FAILED"
        print(f"    {name}: {status}")
    
    successful = sum(1 for v in results.values() if v)
    print(f"\n  {successful}/{len(results)} APIs fetched successfully")
    print("  Data saved to:", DATA_DIR)
    print("=" * 60)
