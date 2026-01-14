import re
import numpy as np
import pandas as pd

def find_brand(text):
    text_lower = str(text).lower()
    
    # 1. The "Elite" List (Your known giants)
    # (Keep your existing list here)
    known_brands = [
        'mccormick', 'rani', 'goya', 'frontier', 'betty', 'starbucks', 
        'badia', 'amoretti', 'bob\'s', 'campbell\'s', 'kraft', 
        'gerber', 'eden', 'lorann', 'kirkland', 'bigelow', 'knorr', 
        'kellogg\'s', 'morton', 'twinings', 'hershey\'s', 'heinz', 
        'torani', 'celestial', 'quaker', 'apple', 'samsung', 'sony', 
        'nike', 'adidas', 'lego', 'funko', 'disney'
    ]
    
    # Check for known brands first (High Confidence)
    for brand in known_brands:
        if brand in text_lower: 
            return brand.title() # Return capitalized (e.g. "Nike")
            
    # 2. The "Smart Fallback" (Low Confidence)
    # If we didn't find a known brand, let's guess the first word.
    
    # A. Clean the text (Remove "Item Name:", "Product:", etc.)
    import re
    cleaned_text = re.sub(r'^(item\s*name|item|product\s*name|description)[:\s-]*', '', text_lower)
    
    # B. Get the first word
    words = cleaned_text.split()
    if not words:
        return 'Unknown'
        
    candidate_brand = words[0]
    
    # C. "Junk Word" Filter
    # If the first word is one of these, it's NOT a brand.
    junk_words = [
        'the', 'a', 'new', 'pack', 'set', 'lot', 'case', 'box', 'of', 'for', 
        'premium', 'organic', 'fresh', 'natural', 'large', 'small', 'blue', 
        'red', 'black', 'white', 'green', 'gold', 'silver', 'combo', 'pair',
        'food', 'item', 'generic', 'unbranded'
    ]
    
    if candidate_brand in junk_words or len(candidate_brand) < 2:
        return 'Unknown'
        
    # If it passed the filter, assume it's a brand!
    return candidate_brand.title()

def check_for_bulk(text):
    text = str(text).lower()
    bulk_keywords = ['kit', 'pallet', 'case', 'bucket', 'pack', 'bulk', 'servings', 'supply', 'bottles']
    for keyword in bulk_keywords:
        if keyword in text: return 1
    return 0

def extract_ipq(text):
    match = re.search(r'(?:IPQ|Pack of|Count)[\s:]*(\d+)', str(text), re.IGNORECASE)
    return int(match.group(1)) if match else 1

def process_text_features(text_series):
    """
    Takes a pandas Series of text and returns a DataFrame of parsed features.
    """
    df = pd.DataFrame()
    df['brand'] = text_series.apply(find_brand)
    df['is_bulk'] = text_series.apply(check_for_bulk)
    df['item_quantity'] = text_series.apply(extract_ipq)
    
    # Simple One-Hot Encoding for Brand (Hardcoded columns for production safety)
    # In a real system, you'd save the OneHotEncoder object, but this is robust for now.
    known_brands = ['apple', 'samsung', 'sony', 'nike', 'dell', 'hp', 'lego', 'adidas']
    for b in known_brands:
        df[f'brand_{b}'] = (df['brand'] == b).astype(int)
        
    # Drop the raw 'brand' column as models need numbers
    
    return df