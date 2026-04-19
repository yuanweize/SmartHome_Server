import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set global matplotlib styles to match academic LaTeX fonts (Computer Modern if possible, else standard)
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'font.family': 'sans-serif',
    'figure.autolayout': True
})

data_file = 'research/data/real_survey_responses.csv'
out_dir = 'research/charts'
os.makedirs(out_dir, exist_ok=True)

df = pd.read_csv(data_file)

# 1. Demographics Chart
def plot_demographics():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    
    # Age
    age_counts = df['age'].value_counts().sort_index()
    sns.barplot(x=age_counts.index, y=age_counts.values, ax=ax1, palette="Purples_d")
    ax1.set_title("Age Distribution")
    ax1.set_ylabel("Count")
    ax1.set_xlabel("Age Group")
    
    # Intent by Age
    intent_means = df.groupby('age')['intent'].mean()
    sns.lineplot(x=intent_means.index, y=intent_means.values, ax=ax2, marker='o', color='purple', linewidth=2)
    ax2.set_title("Purchase Intent by Age")
    ax2.set_ylabel("Avg Intent (1-5)")
    ax2.set_xlabel("Age Group")
    ax2.set_ylim(1, 5)
    
    plt.savefig(f'{out_dir}/survey_demographics.pdf')
    plt.close()

# 2. 4P Product Comparison
def plot_4p_comparison():
    params = ['Visual Appeal', 'Perceived Quality', 'Health Perception']
    franui_means = [df['franui_visual'].mean(), df['franui_quality'].mean(), df['franui_health'].mean()]
    berrie_means = [df['berrie_visual'].mean(), df['berrie_quality'].mean(), df['berrie_health'].mean()]
    
    x = np.arange(len(params))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, franui_means, width, label='Franui (Arg)', color='#E91E63') # Pink
    rects2 = ax.bar(x + width/2, berrie_means, width, label='Berrie (CZ)', color='#5A2B81')  # Purple
    
    ax.set_ylabel('Average Rating (0-10)')
    ax.set_title('Product Perception: Franui vs. Berrie')
    ax.set_xticks(x)
    ax.set_xticklabels(params)
    ax.legend(loc='lower right')
    ax.set_ylim(0, 10)
    
    # Add values on top
    for rects in [rects1, rects2]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
                        
    plt.savefig(f'{out_dir}/survey_4p_comparison.pdf')
    plt.close()

# 3. PSM (Price Sensitivity Meter)
def plot_psm():
    # Sort prices
    prices = np.sort(np.unique(df[['psm_too_cheap', 'psm_cheap', 'psm_expensive', 'psm_too_expensive']].values.flatten()))
    
    tc_pct = [ (df['psm_too_cheap'] >= p).mean() * 100 for p in prices ]
    c_pct = [ (df['psm_cheap'] >= p).mean() * 100 for p in prices ]
    e_pct = [ (df['psm_expensive'] <= p).mean() * 100 for p in prices ]
    te_pct = [ (df['psm_too_expensive'] <= p).mean() * 100 for p in prices ]
    
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(prices, tc_pct, label='Too Cheap', color='darkblue', linestyle='--')
    ax.plot(prices, c_pct, label='Cheap / Good Value', color='green')
    ax.plot(prices, e_pct, label='Expensive', color='orange')
    ax.plot(prices, te_pct, label='Too Expensive', color='red', linestyle='--')
    
    ax.set_xlabel('Price (CZK)')
    ax.set_ylabel('Cumulative Percentage of Respondents (%)')
    ax.set_title('Van Westendorp Price Sensitivity Meter (PSM)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(30, 200)
    
    plt.savefig(f'{out_dir}/survey_psm.pdf')
    plt.close()

# 4. Local Patriotism Premium
def plot_local_premium():
    fig, ax = plt.subplots(figsize=(8, 5))
    wtp_counts = df['premium_wtp'].value_counts()
    
    # Reorder
    order = ['no', 'up_to_10', '10_to_25', 'over_25']
    labels = ['No premium', 'Up to +10%', '+10% to +25%', 'Over +25%']
    values = [wtp_counts.get(o, 0) for o in order]
    
    colors = ['#cccccc', '#a0c4ff', '#9bf6ff', '#fdffb6']
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', 
                                     colors=colors, startangle=90, textprops=dict(color="black"))
    
    ax.set_title('Willingness to Pay Premium for Local Origin')
    plt.savefig(f'{out_dir}/survey_local_premium.pdf')
    plt.close()

if __name__ == "__main__":
    plot_demographics()
    plot_4p_comparison()
    plot_psm()
    plot_local_premium()
    print("Charts generated successfully in research/charts/")
