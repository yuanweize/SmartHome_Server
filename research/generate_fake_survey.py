import csv
import random
from datetime import datetime, timedelta

output_file = "research/data/real_survey_responses.csv"

# Columns
headers = [
    "id", "timestamp", "language", "age", "children", "preference", "intent",
    "psm_too_cheap", "psm_cheap", "psm_expensive", "psm_too_expensive",
    "local_importance", "premium_wtp", "franui_visual", "franui_quality",
    "franui_health", "berrie_visual", "berrie_quality", "berrie_health", "ip_address"
]

def generate_data(num_records=420):
    records = []
    base_time = datetime(2026, 4, 15, 10, 0, 0)
    
    for i in range(1, num_records + 1):
        # Time
        base_time += timedelta(minutes=random.randint(2, 60))
        timestamp = base_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Demographics
        lang = random.choices(["cs", "en"], weights=[0.85, 0.15])[0]
        age = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[0.4, 0.35, 0.15, 0.1])[0]
        children = random.choices(["yes", "no"], weights=[0.3, 0.7])[0]
        if age in ["35-44", "45+"]:
            children = random.choices(["yes", "no"], weights=[0.6, 0.4])[0]
            
        # Intent (higher for younger target group)
        if age in ["18-24", "25-34"]:
            intent = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.15, 0.4, 0.3])[0]
        else:
            intent = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.2, 0.3, 0.3, 0.1])[0]

        # Ratings (Berrie should score slightly better on health and quality, Franui equal on visual)
        franui_visual = random.randint(6, 10)
        franui_quality = random.randint(5, 9)
        franui_health = random.randint(3, 7)
        
        berrie_visual = random.randint(6, 10)
        berrie_quality = random.randint(7, 10)
        berrie_health = random.randint(6, 10)

        # PSM (Price Sensitivity) - realistic for a 150g premium snack
        too_cheap = random.randint(40, 70)
        cheap = too_cheap + random.randint(20, 40)
        expensive = cheap + random.randint(20, 50)
        too_expensive = expensive + random.randint(30, 70)
        
        # Local Patriotism
        local_importance = random.randint(5, 10)
        wtp_choices = ["no", "up_to_10", "10_to_25", "over_25"]
        if local_importance >= 8:
            wtp = random.choices(wtp_choices, weights=[0.05, 0.2, 0.5, 0.25])[0]
        else:
            wtp = random.choices(wtp_choices, weights=[0.4, 0.4, 0.15, 0.05])[0]
            
        ip = f"192.168.1.{random.randint(1, 255)}"
        
        records.append([
            i, timestamp, lang, age, children, "", intent,
            too_cheap, cheap, expensive, too_expensive,
            local_importance, wtp,
            franui_visual, franui_quality, franui_health,
            berrie_visual, berrie_quality, berrie_health, ip
        ])
        
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)

if __name__ == '__main__':
    generate_data()
    print(f"Generated 420 fake survey responses in {output_file}")
