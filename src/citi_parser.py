import re

def parse(text: str) -> dict:
    """
    Parses Citi credit card statement text.
    
    NOTE: These regex patterns are educated guesses and will
    need to be fine-tuned based on the *actual* statement text.
    """
    data = {
        'issuer': 'Citi',
        'last_4_digits': None,
        'due_date': None,
        'total_due': None,
        'statement_period': None
    }
    
    # --- REGEX PATTERNS: These will need to be adjusted ---

    try:
        # 1. Last 4 Digits
        match = re.search(r'Account Number.*?(\d{4})', text, re.IGNORECASE)
        if match:
            data['last_4_digits'] = match.group(1)

        # 2. Payment Due Date
        match = re.search(r'Payment Due Date.*?(\d{2}/\d{2}/\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['due_date'] = match.group(1)

        # 3. Total Amount Due
        # Look for "Total Balance Due"
        match = re.search(r'Total Balance Due.*?\$([\d,]+\.\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['total_due'] = match.group(1).replace(',', '')

        # 4. Statement Period
        # Look for "Statement Period"
        match = re.search(r'Statement Period.*?(\d{2}/\d{2}/\d{2})\s*-\s*(\d{2}/\d{2}/\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['statement_period'] = f"{match.group(1)} to {match.group(2)}"
            
    except Exception as e:
        print(f"Error parsing Citi statement: {e}")

    return data
