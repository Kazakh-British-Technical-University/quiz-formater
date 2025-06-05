import random
import pandas as pd

def generate_variant(df, variant_id=1, seed=None):
    grouped = df.groupby('Group ID')
    selected = []

    if seed:
        random.seed(seed + variant_id)

    for _, group in grouped:
        selected.append(group.sample(1))

    return pd.concat(selected).reset_index(drop=True)

def generate_exam_variants(df, num_variants=2, seed=None):
    variants = {}
    for i in range(1, num_variants + 1):
        variants[f"Variant_{i}"] = generate_variant(df, i, seed)
    return variants
