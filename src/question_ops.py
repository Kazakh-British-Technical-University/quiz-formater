import random
import pandas as pd

def generate_variant(df, variant_id=1, randomize_order=False, seed=None, max_questions=None, start_index=0, end_index=None):
    grouped = df.groupby('Group ID')
    selected = []

    print(grouped.head(10))

    # Something wrong here
    for _, group in grouped:
        selected.append(group.iat[(variant_id - 1) % len(group)])

    if end_index is None or end_index==start_index:
        end_index = len(result) - 1
    
    result = pd.concat(selected).reset_index(drop=True).iloc[start_index:end_index]
    
    max_questions = min(max_questions, len(result))

    if randomize_order:
        result = result.sample(max_questions, random_state=seed + variant_id if seed else None)
    else:
        result = result.head(max_questions % len(result))
    
    # Add answer information
    result['answer'] = result['Answer']
    
    return result

def generate_exam_variants(df, num_variants=2, max_questions=None, randomize_order=False, seed=None, start_index=0, end_index=None):
    variants = {}
    for i in range(1, num_variants + 1):
        variants[i] = generate_variant(df, i, randomize_order, seed, max_questions, start_index, end_index)
    return variants
