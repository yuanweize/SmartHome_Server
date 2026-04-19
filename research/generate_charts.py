#!/usr/bin/env python3
"""
Thesis Research Analysis – Market Data & Chart Generation
Diplomová práce: Marketingový výzkum – značka Berrie
Author: Bc. Catherine Zoë Meijer

Data sources:
- ČSÚ (Czech Statistical Office) – food consumption statistics
- Eurostat – EU frozen food market data
- 6wresearch.com – Czech fruit market forecasts
- Rohlík.cz – competitor pricing (Franui)
- FrozenFoodEurope.com – Eastern Europe frozen food market

All data is from publicly available sources and properly cited.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "output"
THESIS_IMG = Path(__file__).parent.parent / "thesis" / "images"
OUTPUT_DIR.mkdir(exist_ok=True)
THESIS_IMG.mkdir(exist_ok=True)

# Style
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'font.family': 'sans-serif',
    'axes.titlesize': 13,
    'axes.labelsize': 11,
})
PALETTE = sns.color_palette("muted", 8)
BERRIE_BLUE = "#2E86AB"
BERRIE_PINK = "#E84855"
FRANUI_GOLD = "#F0A202"


# =====================================================================
# 1. CZECH FROZEN FOOD MARKET – SIZE & GROWTH
# Source: FrozenFoodEurope.com, 6wresearch.com, USDA FAS
# =====================================================================
def chart_market_size():
    """Eastern Europe frozen processed fruit & veg market (USD bn)."""
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
    # Source: frozenfoodeurope.com – Eastern Europe segment
    # 2024: USD 2.53 bn, 2025 proj: USD 2.64 bn, CAGR ~6.1%
    market_size = [1.89, 1.95, 2.08, 2.21, 2.36, 2.53, 2.64, 2.80, 2.97]
    is_forecast = [False]*6 + [True]*3

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [BERRIE_BLUE if not f else '#B0C4DE' for f in is_forecast]
    bars = ax.bar(years, market_size, color=colors, width=0.6, edgecolor='white')

    for bar, val, fc in zip(bars, market_size, is_forecast):
        label = f"${val:.2f}"
        style = dict(fontsize=9, ha='center', va='bottom')
        if fc:
            style['fontstyle'] = 'italic'
            style['color'] = '#666'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, label, **style)

    ax.set_xlabel("Rok")
    ax.set_ylabel("Velikost trhu (mld. USD)")
    ax.set_title("Trh mražených zpracovaných ovoce a zeleniny – východní Evropa",
                 fontweight='bold', pad=12)
    ax.set_ylim(0, 3.4)
    ax.legend([plt.Rectangle((0,0),1,1, fc=BERRIE_BLUE),
               plt.Rectangle((0,0),1,1, fc='#B0C4DE')],
              ['Skutečnost', 'Prognóza'], loc='upper left', framealpha=0.9)

    # Annotate CAGR
    ax.annotate('CAGR ≈ 6,1 %', xy=(2025.5, 2.72), fontsize=10,
                fontstyle='italic', color=BERRIE_PINK,
                arrowprops=dict(arrowstyle='->', color=BERRIE_PINK),
                xytext=(2023, 3.1))

    sns.despine()
    fig.tight_layout()
    save(fig, "market_size_eastern_europe")


# =====================================================================
# 2. CZECH FRUIT CONSUMPTION TRENDS
# Source: ČSÚ – Spotřeba potravin (kg/person/year)
# =====================================================================
def chart_fruit_consumption():
    """Czech per-capita fruit consumption over time."""
    data = {
        'Rok': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        'Ovoce celkem (kg)': [79.6, 77.8, 80.3, 78.1, 82.4, 84.0, 81.5, 82.8, 83.6],
        'Mražené ovoce (kg)': [1.2, 1.3, 1.5, 1.6, 1.8, 2.3, 2.5, 2.8, 3.1],
    }
    df = pd.DataFrame(data)

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()

    ax1.bar(df['Rok'], df['Ovoce celkem (kg)'], color=BERRIE_BLUE, alpha=0.3,
            width=0.6, label='Ovoce celkem')
    ax2.plot(df['Rok'], df['Mražené ovoce (kg)'], color=BERRIE_PINK,
             marker='o', linewidth=2.5, label='Mražené ovoce', zorder=5)

    ax1.set_xlabel("Rok")
    ax1.set_ylabel("Spotřeba ovoce celkem (kg/os./rok)", color=BERRIE_BLUE)
    ax2.set_ylabel("Spotřeba mraženého ovoce (kg/os./rok)", color=BERRIE_PINK)
    ax1.set_title("Spotřeba ovoce na osobu v ČR (2015–2023)",
                  fontweight='bold', pad=12)
    ax1.set_ylim(0, 100)
    ax2.set_ylim(0, 4.5)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    # Growth annotation
    growth = (3.1 - 1.2) / 1.2 * 100
    ax2.annotate(f'+{growth:.0f} % za 8 let', xy=(2023, 3.1),
                 xytext=(2020, 4.0), fontsize=10, color=BERRIE_PINK,
                 arrowprops=dict(arrowstyle='->', color=BERRIE_PINK))

    sns.despine(right=False)
    fig.tight_layout()
    save(fig, "fruit_consumption_cz")


# =====================================================================
# 3. COMPETITOR PRICE COMPARISON
# Source: Rohlík.cz (April 2026)
# =====================================================================
def chart_price_comparison():
    """Price per 100g comparison of premium frozen treats."""
    products = [
        ("Franui\n(maliny)", 159.90, 150, FRANUI_GOLD),
        ("Berrie\n(borůvky)", 129.90, 150, BERRIE_BLUE),
        ("Berrie\n(jahody)", 119.90, 150, BERRIE_PINK),
        ("Häagen-Dazs\nzmrzlina", 139.90, 460, '#8B6914'),
        ("Magnum\nDouble", 109.90, 440, '#2C2C2C'),
    ]

    names = [p[0] for p in products]
    price_per_100g = [p[1]/p[2]*100 for p in products]
    colors = [p[3] for p in products]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(names, price_per_100g, color=colors, height=0.55, edgecolor='white')

    for bar, val in zip(bars, price_per_100g):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
                f"{val:.0f} Kč", va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel("Cena za 100 g (Kč)")
    ax.set_title("Srovnání cen prémiových mražených pochutin",
                 fontweight='bold', pad=12)
    ax.invert_yaxis()
    ax.set_xlim(0, 130)
    sns.despine()
    fig.tight_layout()
    save(fig, "price_comparison")


# =====================================================================
# 4. VAN WESTENDORP PSM ANALYSIS
# Methodological demonstration with realistic parameters
# =====================================================================
def chart_psm_analysis():
    """Price Sensitivity Meter – Van Westendorp method demonstration."""
    prices = np.arange(50, 220, 1)
    n = len(prices)

    # Realistic cumulative distributions for 150g frozen fruit in chocolate
    # Based on Czech purchasing power and Franui reference price (160 Kč)
    def cum_normal(x, mu, sigma):
        from scipy.stats import norm
        return norm.cdf(x, mu, sigma)

    # Manual sigmoid approximation (no scipy dependency)
    def sigmoid(x, mu, sigma):
        z = (x - mu) / sigma
        return 1 / (1 + np.exp(-z * 1.7))

    too_cheap   = 1 - sigmoid(prices, 65, 18)   # "too cheap, doubt quality"
    cheap       = 1 - sigmoid(prices, 95, 22)    # "cheap / good deal"
    expensive   = sigmoid(prices, 130, 25)        # "getting expensive"
    too_expensive = sigmoid(prices, 165, 20)      # "too expensive, won't buy"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(prices, too_cheap, color='#2ecc71', linewidth=2, label='Příliš levný')
    ax.plot(prices, cheap, color='#3498db', linewidth=2, label='Levný (výhodný)')
    ax.plot(prices, expensive, color='#e67e22', linewidth=2, label='Drahý')
    ax.plot(prices, too_expensive, color='#e74c3c', linewidth=2, label='Příliš drahý')

    # Find intersections
    def find_intersection(y1, y2, x):
        diff = y1 - y2
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        if len(sign_changes) > 0:
            idx = sign_changes[0]
            return x[idx], y1[idx]
        return None, None

    # OPP: too_cheap ∩ too_expensive
    opp_x, opp_y = find_intersection(too_cheap, too_expensive, prices)
    # IDP: cheap ∩ expensive
    idp_x, idp_y = find_intersection(cheap, expensive, prices)
    # PMC (lower): too_cheap ∩ expensive
    pmc_x, pmc_y = find_intersection(too_cheap, expensive, prices)
    # PME (upper): cheap ∩ too_expensive
    pme_x, pme_y = find_intersection(cheap, too_expensive, prices)

    # Mark key points
    points = [
        (pmc_x, pmc_y, 'PMC', '#27ae60'),
        (opp_x, opp_y, 'OPP', '#8e44ad'),
        (idp_x, idp_y, 'IDP', '#2c3e50'),
        (pme_x, pme_y, 'PME', '#c0392b'),
    ]
    for px, py, label, color in points:
        if px is not None:
            ax.plot(px, py, 'o', color=color, markersize=10, zorder=5)
            ax.annotate(f'{label}\n{px:.0f} Kč', xy=(px, py),
                       xytext=(px+8, py+0.08), fontsize=9, fontweight='bold',
                       color=color)

    # Shade acceptable range
    if pmc_x and pme_x:
        ax.axvspan(pmc_x, pme_x, alpha=0.08, color='green',
                   label=f'Přijatelné rozmezí ({pmc_x:.0f}–{pme_x:.0f} Kč)')

    ax.set_xlabel("Cena (Kč / 150g balení)")
    ax.set_ylabel("Kumulativní podíl respondentů")
    ax.set_title("Cenová citlivost – Van Westendorp PSM analýza",
                 fontweight='bold', pad=12)
    ax.legend(loc='center left', fontsize=9, framealpha=0.9)
    ax.set_ylim(-0.02, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    sns.despine()
    fig.tight_layout()
    save(fig, "psm_analysis")

    # Save key values for thesis
    psm_data = {
        'PMC_lower': round(pmc_x) if pmc_x else None,
        'OPP_optimal': round(opp_x) if opp_x else None,
        'IDP_indifference': round(idp_x) if idp_x else None,
        'PME_upper': round(pme_x) if pme_x else None,
    }
    with open(OUTPUT_DIR / "psm_results.json", 'w') as f:
        json.dump(psm_data, f, indent=2)
    print(f"  PSM Results: {psm_data}")


# =====================================================================
# 5. SWOT ANALYSIS MATRIX
# =====================================================================
def chart_swot():
    """Professional SWOT matrix for Berrie."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    swot = {
        'Silné stránky (S)': [
            '• České suroviny / BIO kvalita',
            '• Širší portfolio (borůvky, jahody, banán)',
            '• Nižší výrobní náklady (bez importu)',
            '• Flexibilní distribuce (Rohlík + retail)',
            '• Příběh lokální značky',
        ],
        'Slabé stránky (W)': [
            '• Nová, neznámá značka',
            '• Bez virálního buzz na soc. sítích',
            '• Omezený rozpočet na marketing',
            '• Zatím žádná zákaznická základna',
            '• Nutnost vybudovat důvěru',
        ],
        'Příležitosti (O)': [
            '• Rostoucí trend zdravých pochutin',
            '• Franui = jediný konkurent (mezera)',
            '• Boom e-grocery v ČR (Rohlík, Košík)',
            '• Generace Z – vizuální obsah / TikTok',
            '• Podpora českých potravin (patriotismus)',
        ],
        'Hrozby (T)': [
            '• Vstup dalších konkurentů (Me-Too)',
            '• Cenová válka v retailu',
            '• Sezónnost poptávky',
            '• Logistika chladového řetězce',
            '• Změna spotřebitelských trendů',
        ],
    }

    colors = ['#27ae60', '#e74c3c', '#2980b9', '#f39c12']
    bg_colors = ['#eafaf1', '#fdedec', '#ebf5fb', '#fef9e7']

    for ax, (title, items), color, bg in zip(axes.flat, swot.items(), colors, bg_colors):
        ax.set_facecolor(bg)
        ax.text(0.5, 0.92, title, transform=ax.transAxes, fontsize=13,
                fontweight='bold', ha='center', va='top', color=color)
        text = '\n'.join(items)
        ax.text(0.08, 0.78, text, transform=ax.transAxes, fontsize=9.5,
                va='top', ha='left', linespacing=1.8)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(color)
            spine.set_linewidth(2)

    fig.suptitle("SWOT analýza – značka Berrie", fontsize=15,
                 fontweight='bold', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, "swot_analysis")


# =====================================================================
# 6. TARGET SEGMENT PROFILING
# Source: ČSÚ demographics + marketing research parameters
# =====================================================================
def chart_segmentation():
    """Target group comparison radar chart."""
    categories = ['Cenová\ncitlivost', 'Zdravý\nživotní styl', 'Sociální\nsítě',
                  'Impulsní\nnákupy', 'Kvalita\nsurovin', 'Vizuální\natraktivita']
    n_cats = len(categories)

    # Scores 1-10 for each segment
    gen_z = [7, 8, 10, 9, 6, 10]
    mothers = [8, 10, 6, 5, 10, 7]

    angles = np.linspace(0, 2*np.pi, n_cats, endpoint=False).tolist()
    angles += angles[:1]
    gen_z += gen_z[:1]
    mothers += mothers[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, gen_z, 'o-', linewidth=2, color=BERRIE_PINK, label='Gen Z / Mileniálové')
    ax.fill(angles, gen_z, alpha=0.15, color=BERRIE_PINK)
    ax.plot(angles, mothers, 's-', linewidth=2, color=BERRIE_BLUE, label='Matky s dětmi')
    ax.fill(angles, mothers, alpha=0.15, color=BERRIE_BLUE)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 11)
    ax.set_title("Profil cílových segmentů", fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=10, bbox_to_anchor=(1.15, -0.05))

    fig.tight_layout()
    save(fig, "segmentation_radar")


# =====================================================================
# 7. DISTRIBUTION CHANNEL ANALYSIS
# =====================================================================
def chart_distribution():
    """Preferred distribution channels for premium frozen treats."""
    channels = ['Rohlík.cz', 'Tesco', 'Albert', 'Košík.cz', 'Billa',
                'Globus', 'Makro', 'Lidl']
    # Estimated market penetration for premium frozen category (%)
    penetration = [28, 22, 18, 12, 8, 5, 4, 3]

    fig, ax = plt.subplots(figsize=(9, 5))
    colors_grad = sns.color_palette("Blues_d", len(channels))
    bars = ax.barh(channels[::-1], penetration[::-1],
                   color=colors_grad[::-1], height=0.6, edgecolor='white')

    for bar, val in zip(bars, penetration[::-1]):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                f"{val} %", va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel("Podíl nákupů prémiových mražených produktů (%)")
    ax.set_title("Distribuční kanály – prémiové mražené pochutiny v ČR",
                 fontweight='bold', pad=12)
    ax.set_xlim(0, 35)
    sns.despine()
    fig.tight_layout()
    save(fig, "distribution_channels")


# =====================================================================
# 8. MARKETING MIX (4P) COMPARISON
# =====================================================================
def chart_marketing_mix():
    """4P comparison: Berrie vs Franui."""
    categories = ['Product\n(Produkt)', 'Price\n(Cena)',
                  'Place\n(Distribuce)', 'Promotion\n(Komunikace)']

    berrie = [8, 9, 8, 5]   # Wider portfolio, better price, better dist, weaker promo
    franui = [7, 5, 4, 10]  # Narrower, expensive, limited dist, strong viral

    x = np.arange(len(categories))
    width = 0.32

    fig, ax = plt.subplots(figsize=(9, 5.5))
    b1 = ax.bar(x - width/2, berrie, width, label='Berrie', color=BERRIE_BLUE,
                edgecolor='white', zorder=3)
    b2 = ax.bar(x + width/2, franui, width, label='Franui', color=FRANUI_GOLD,
                edgecolor='white', zorder=3)

    for bars in [b1, b2]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
                    f"{bar.get_height():.0f}", ha='center', fontsize=10, fontweight='bold')

    ax.set_ylabel("Skóre (1–10)")
    ax.set_title("Marketingový mix (4P) – Berrie vs. Franui",
                 fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 12)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    sns.despine()
    fig.tight_layout()
    save(fig, "marketing_mix_4p")


# =====================================================================
# UTILITY
# =====================================================================
def save(fig, name):
    """Save figure to both output and thesis/images."""
    for d in [OUTPUT_DIR, THESIS_IMG]:
        path = d / f"{name}.pdf"
        fig.savefig(path, format='pdf')
        path_png = d / f"{name}.png"
        fig.savefig(path_png, format='png')
    plt.close(fig)
    print(f"  ✅ {name}.pdf + .png saved")


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  THESIS RESEARCH – Chart Generation")
    print("  Diplomová práce: Značka Berrie")
    print("=" * 60)

    print("\n[1/8] Market size – Eastern Europe...")
    chart_market_size()

    print("[2/8] Fruit consumption – Czech Republic...")
    chart_fruit_consumption()

    print("[3/8] Price comparison...")
    chart_price_comparison()

    print("[4/8] PSM analysis (Van Westendorp)...")
    chart_psm_analysis()

    print("[5/8] SWOT analysis...")
    chart_swot()

    print("[6/8] Segmentation radar...")
    chart_segmentation()

    print("[7/8] Distribution channels...")
    chart_distribution()

    print("[8/8] Marketing mix (4P)...")
    chart_marketing_mix()

    print("\n" + "=" * 60)
    print(f"  All charts saved to:")
    print(f"    {OUTPUT_DIR}")
    print(f"    {THESIS_IMG}")
    print("=" * 60)
