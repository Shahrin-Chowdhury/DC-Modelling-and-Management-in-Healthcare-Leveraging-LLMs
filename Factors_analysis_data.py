import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Helper functions
def generate_age():
    return int(np.clip(np.random.normal(loc=58, scale=15), 18, 90))

def generate_gender():
    return np.random.choice([0, 1, 2], p=[0.48, 0.48, 0.04])

def generate_ordinal(levels, probs):
    return np.random.choice(levels, p=probs)

# Distributions
education_probs = [0.10, 0.30, 0.35, 0.20, 0.05]
literacy_probs = [0.10, 0.20, 0.35, 0.25, 0.10]
tech_probs = [0.20, 0.30, 0.30, 0.15, 0.05]
language_probs = [0.10, 0.15, 0.30, 0.30, 0.15]
ses_probs = [0.15, 0.25, 0.35, 0.20, 0.05]
experience_probs = [0.10, 0.25, 0.35, 0.20, 0.10]
cognitive_probs = [0.10, 0.20, 0.30, 0.25, 0.15]

# Dynamic trigger condition
def is_dynamic_any(row):
    return (
        row["f2: Urgency"] >= 7 or
        row["f4: Capacity"] <= 0.5 or
        row["h1: Age"] >= 71 or
        row["h6: Language / Culture"] <= 2 or
        row["h9: Cognitive/Mental State"] <= 3
    )

# Generate 10,000 patients: 5,000 dynamic, 5,000 non-dynamic
data = []
dynamic_count = 0
non_dynamic_count = 0
target_each = 5000
patient_id = 1

while dynamic_count < target_each or non_dynamic_count < target_each:
    f1 = np.random.randint(1, 11)
    f2 = np.random.randint(1, 11)
    f3 = np.random.randint(1, 11)
    f4 = round(np.random.choice([1.0, 0.75, 0.5, 0.25, 0.0], p=[0.2, 0.25, 0.3, 0.15, 0.1]), 2)
    h1 = generate_age()
    h2 = generate_gender()
    h3 = generate_ordinal([1, 2, 3, 4, 5], education_probs)
    h4 = generate_ordinal([1, 2, 3, 4, 5], literacy_probs)
    h5 = generate_ordinal([1, 2, 3, 4, 5], tech_probs)
    h6 = generate_ordinal([1, 2, 3, 4, 5], language_probs)
    h7 = generate_ordinal([1, 2, 3, 4, 5], ses_probs)
    h8 = generate_ordinal([1, 2, 3, 4, 5], experience_probs)
    h9 = generate_ordinal([1, 2, 3, 4, 5], cognitive_probs)
    f6 = np.random.randint(1, 6)
    f7 = np.random.randint(1, 11)
    f8 = np.random.randint(1, 11)
    f9 = np.random.randint(1, 6)
    f10 = np.random.randint(1, 11)

    row = {
        "Patient Name": f"Patient_{patient_id:05d}",
        "f1: Frequency": f1, "f2: Urgency": f2, "f3: Severity": f3, "f4: Capacity": f4,
        "h1: Age": h1, "h2: Gender": h2, "h3: Education Level": h3, "h4: Health Literacy": h4,
        "h5: Tech Proficiency": h5, "h6: Language / Culture": h6, "h7: Socioeconomic Status": h7,
        "h8: Previous Experience": h8, "h9: Cognitive/Mental State": h9,
        "f6: Redundancy": f6, "f7: Environment": f7, "f8: Communication Quality": f8,
        "f9: Consent Granularity": f9, "f10: Cumulative Load": f10
    }

    if is_dynamic_any(row) and dynamic_count < target_each:
        row["Trigger Type"] = "Dynamic"
        data.append(row)
        dynamic_count += 1
        patient_id += 1
    elif not is_dynamic_any(row) and non_dynamic_count < target_each:
        row["Trigger Type"] = "Non-Dynamic"
        data.append(row)
        non_dynamic_count += 1
        patient_id += 1

# Create and save CSV
df = pd.DataFrame(data)

# Ensure Patient Name is the first column
columns = ["Patient Name"] + [col for col in df.columns if col != "Patient Name"]
df = df[columns]

df.to_csv("Patient_dataset.csv", index=False)
print("✅ File 'Patient_dataset.csv' saved with Patient Name as the first column.")
