import re

def parse(text: str) -> dict:
    """
    Parses American Express statement text.
    
    NOTE: These regex patterns are educated guesses and will
    need to be fine-tuned based on the *actual* statement text.
    """
    data = {
        'issuer': 'American Express',
        'last_4_digits': None,
        'due_date': None,
        'total_due': None,
        'statement_period': None
    }
    
    # --- REGEX PATTERNS: These will need to be adjusted ---
    
    try:
        # 1. Last 4 Digits
        # Amex often shows last 5, e.g., "Account #: XXXXX-XXXXX-X1234"
        match = re.search(r'Account.*?(\d{5})', text, re.IGNORECASE)
        if match:
            data['last_4_digits'] = match.group(1) # Could be 5 digits

        # 2. Payment Due Date
        # Look for "Please pay by"
        match = re.search(r'Please pay by.*?(\w{3}\s\d{1,2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['due_date'] = match.group(1) # Amex often omits the year

        # 3. Total Amount Due
        # Look for "Total Balance"
        match = re.search(r'Total Balance.*?\$([\d,]+\.\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['total_due'] = match.group(1).replace(',', '')

        # 4. Statement Period
        # Look for "Closing Date" and "Opening Date"
        closing_match = re.search(r'Closing Date.*?(\w{3}\s\d{1,2},\s\d{4})', text, re.IGNORECASE | re.DOTALL)
        opening_match = re.search(r'Opening Date.*?(\w{3}\s\d{1,2},\s\d{4})', text, re.IGNORECASE | re.DOTALL)
        if opening_match and closing_match:
            data['statement_period'] = f"{opening_match.group(1)} to {closing_match.group(1)}"
            
    except Exception as e:
        print(f"Error parsing Amex statement: {e}")

    return data
