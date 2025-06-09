import random
import pandas as pd

def generate_variant(df, variant_id=1, seed=None, max_questions=None):
    grouped = df.groupby('Group ID')
    selected = []

    if seed:
        random.seed(seed + variant_id)

    for _, group in grouped:
        selected.append(group.sample(1))
    
    result = pd.concat(selected).reset_index(drop=True)
    
    if max_questions and len(result) > max_questions:
        result = result.sample(max_questions, random_state=seed + variant_id if seed else None)
    
    return result

def generate_exam_variants(df, num_variants=2, max_questions=None, seed=None):
    variants = {}
    for i in range(1, num_variants + 1):
        variants[i] = generate_variant(df, i, seed, max_questions)
    return variants
