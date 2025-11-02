import re

def parse(text: str) -> dict:
    """
    Parses ICICI credit card statement text.
    
    NOTE: These regex patterns are educated guesses and will
    need to be fine-tuned based on the *actual* statement text.
    """
    data = {
        'issuer': 'ICICI',
        'last_4_digits': None,
        'due_date': None,
        'total_due': None,
        'statement_period': None
    }
    
    # --- REGEX PATTERNS: These will need to be adjusted ---

    try:
        # 1. Last 4 Digits (ICICI might just show it)
        # Look for a 16-digit number format or card number ending in
        match = re.search(r'Card Number.*?(\d{4})', text, re.IGNORECASE)
        if match:
            data['last_4_digits'] = match.group(1)

        # 2. Payment Due Date
        match = re.search(r'Payment Due Date.*?([\d]{2}/[\d]{2}/[\d]{4})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['due_date'] = match.group(1)

        # 3. Total Amount Due
        # ICICI might call it "Total Dues"
        match = re.search(r'Total Dues.*?([\d,]+\.\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['total_due'] = match.group(1).replace(',', '')

        # 4. Statement Period
        match = re.search(r'Statement Period.*?(\d{2}/\d{2}/\d{4})\s*to\s*(\d{2}/\d{2}/\d{4})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['statement_period'] = f"{match.group(1)} to {match.group(2)}"
            
    except Exception as e:
        print(f"Error parsing ICICI statement: {e}")

    return data
