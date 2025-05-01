import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Generator functions
def generate_age(): return int(np.clip(np.random.normal(loc=58, scale=15), 18, 90))
def generate_gender(): return np.random.choice([0, 1, 2], p=[0.48, 0.48, 0.04])
def generate_ordinal(levels, probs): return np.random.choice(levels, p=probs)

# Probability distributions
education_probs = [0.10, 0.30, 0.35, 0.20, 0.05]
literacy_probs = [0.10, 0.20, 0.35, 0.25, 0.10]
tech_probs = [0.20, 0.30, 0.30, 0.15, 0.05]
language_probs = [0.10, 0.15, 0.30, 0.30, 0.15]
ses_probs = [0.15, 0.25, 0.35, 0.20, 0.05]
experience_probs = [0.10, 0.25, 0.35, 0.20, 0.10]
cognitive_probs = [0.10, 0.20, 0.30, 0.25, 0.15]

# Dynamic condition
def is_dynamic(row):
    return (
        row["f2: Urgency"] >= 7 or
        row["f4: Capacity"] <= 0.5 or
        row["h1: Age"] >= 71 or
        row["h6: Language / Culture"] <= 2 or
        row["h9: Cognitive/Mental State"] <= 3
    )

# f5: Human Factors computation
def compute_f5(row):
    normalized_age = (row['h1: Age'] - 18) / (90 - 18) * 5
    subfactors = [
        normalized_age, row['h2: Gender'], row['h3: Education Level'],
        row['h4: Health Literacy'], row['h5: Tech Proficiency'],
        row['h6: Language / Culture'], row['h7: Socioeconomic Status'],
        row['h8: Previous Experience'], row['h9: Cognitive/Mental State']
    ]
    return round(np.mean(subfactors), 2)

# Generate a single patient row
def generate_row(pid):
    h1 = generate_age()
    h2 = generate_gender()
    h3 = generate_ordinal([1, 2, 3, 4, 5], education_probs)
    h4 = generate_ordinal([1, 2, 3, 4, 5], literacy_probs)
    h5 = generate_ordinal([1, 2, 3, 4, 5], tech_probs)
    h6 = generate_ordinal([1, 2, 3, 4, 5], language_probs)
    h7 = generate_ordinal([1, 2, 3, 4, 5], ses_probs)
    h8 = generate_ordinal([1, 2, 3, 4, 5], experience_probs)
    h9 = generate_ordinal([1, 2, 3, 4, 5], cognitive_probs)
    f2 = np.random.randint(1, 11)
    f4 = round(np.random.choice([1.0, 0.75, 0.5, 0.25, 0.0], p=[0.2, 0.25, 0.3, 0.15, 0.1]), 2)
    return {
        "Patient Name": f"Patient_{pid:04d}",
        "f1: Frequency": np.random.randint(1, 11),
        "f2: Urgency": f2,
        "f3: Severity": np.random.randint(1, 11),
        "f4: Capacity": f4,
        "h1: Age": h1, "h2: Gender": h2, "h3: Education Level": h3,
        "h4: Health Literacy": h4, "h5: Tech Proficiency": h5,
        "h6: Language / Culture": h6, "h7: Socioeconomic Status": h7,
        "h8: Previous Experience": h8, "h9: Cognitive/Mental State": h9,
        "f6: Redundancy": np.random.randint(1, 6),
        "f7: Environment": np.random.randint(1, 11),
        "f8: Communication Quality": np.random.randint(1, 11),
        "f9: Consent Granularity": np.random.randint(1, 6),
        "f10: Cumulative Load": np.random.randint(1, 11)
    }

# Generate alternating dynamic/non-dynamic blocks
blocks = [(50, 30), (20, 40), (40, 20), (30, 50), (60, 20), (50, 40), (40, 40), (30, 30), (30, 30), (150, 200)]
dynamic_count = non_dynamic_count = 0
total_dynamic = total_non_dynamic = 500
final_data = []
pid = 1

for d_block, nd_block in blocks:
    for _ in range(d_block):
        while True:
            row = generate_row(pid)
            if is_dynamic(row) and dynamic_count < total_dynamic:
                row["Trigger Type"] = "Dynamic"
                final_data.append(row)
                dynamic_count += 1
                pid += 1
                break
    for _ in range(nd_block):
        while True:
            row = generate_row(pid)
            if not is_dynamic(row) and non_dynamic_count < total_non_dynamic:
                row["Trigger Type"] = "Non-Dynamic"
                final_data.append(row)
                non_dynamic_count += 1
                pid += 1
                break
    if dynamic_count >= total_dynamic and non_dynamic_count >= total_non_dynamic:
        break

df = pd.DataFrame(final_data)

# === Apply Descriptive Labels ===
def map_range(val, mapping):
    for key, label in mapping.items():
        if isinstance(key, tuple):
            if key[0] <= val <= key[1]: return label
        elif val == key: return label
    return val

f1_map = {(1, 2): "Very Low", (3, 4): "Low to Moderate", (5, 6): "Moderate", (7, 8): "High", (9, 10): "Very High"}
f2_map = f3_map = f7_map = f8_map = f10_map = {(1, 2): "Very Low", (3, 4): "Low", (5, 6): "Moderate", (7, 8): "High", (9, 10): "Very High"}
f6_map = f9_map = {1: "Very Low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very High"}
f4_map = {1.0: "Full Capacity", 0.75: "Slightly Impaired", 0.5: "Moderately Impaired", 0.25: "Severely Impaired", 0.0: "No Capacity"}
h2_map = {0: "Male", 1: "Female", 2: "Other / Non-binary"}
h1_age_map = lambda age: "Young Adult" if age <= 35 else "Middle-Aged" if age <= 55 else "Older Adult" if age <= 70 else "Senior" if age <= 85 else "Elderly"
h3_map = {1: "No formal education / Primary only", 2: "Secondary (up to high school)", 3: "Some college / Vocational training", 4: "Bachelor’s degree", 5: "Graduate degree or higher"}
h4_h5_map = {1: "Very Low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very High"}
h6_map = {1: "Very Low Alignment", 2: "Low", 3: "Moderate", 4: "High", 5: "Very High"}
h7_map = h4_h5_map.copy()
h8_map = {1: "None", 2: "Minimal", 3: "Moderate", 4: "High", 5: "Very High"}
h9_map = {1: "Severely Impaired", 2: "Impaired", 3: "Fluctuating / Mixed", 4: "Clear but Stressed", 5: "Stable and Clear"}

# Apply mappings
df["f1: Frequency"] = df["f1: Frequency"].apply(lambda x: map_range(x, f1_map))
df["f2: Urgency"] = df["f2: Urgency"].apply(lambda x: map_range(x, f2_map))
df["f3: Severity"] = df["f3: Severity"].apply(lambda x: map_range(x, f3_map))
df["f4: Capacity"] = df["f4: Capacity"].apply(lambda x: f4_map.get(x, x))
df["f6: Redundancy"] = df["f6: Redundancy"].apply(lambda x: map_range(x, f6_map))
df["f7: Environment"] = df["f7: Environment"].apply(lambda x: map_range(x, f7_map))
df["f8: Communication Quality"] = df["f8: Communication Quality"].apply(lambda x: map_range(x, f8_map))
df["f9: Consent Granularity"] = df["f9: Consent Granularity"].apply(lambda x: map_range(x, f9_map))
df["f10: Cumulative Load"] = df["f10: Cumulative Load"].apply(lambda x: map_range(x, f10_map))
df["h1: Age"] = df["h1: Age"].apply(h1_age_map)
df["h2: Gender"] = df["h2: Gender"].map(h2_map)
df["h3: Education Level"] = df["h3: Education Level"].map(h3_map)
df["h4: Health Literacy"] = df["h4: Health Literacy"].map(h4_h5_map)
df["h5: Tech Proficiency"] = df["h5: Tech Proficiency"].map(h4_h5_map)
df["h6: Language / Culture"] = df["h6: Language / Culture"].map(h6_map)
df["h7: Socioeconomic Status"] = df["h7: Socioeconomic Status"].map(h7_map)
df["h8: Previous Experience"] = df["h8: Previous Experience"].map(h8_map)
df["h9: Cognitive/Mental State"] = df["h9: Cognitive/Mental State"].map(h9_map)

# Save to CSV
df.to_csv("descriptive_patient_dataset.csv", index=False)
print("✅ Descriptive dataset with alternating trigger types saved as 'descriptive_patient_dataset.csv'")
