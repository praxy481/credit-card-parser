import re

def parse(text: str) -> dict:
    """
    Parses Chase credit card statement text.
    
    NOTE: These regex patterns are educated guesses and will
    need to be fine-tuned based on the *actual* statement text.
    """
    data = {
        'issuer': 'Chase',
        'last_4_digits': None,
        'due_date': None,
        'total_due': None,
        'statement_period': None
    }
    
    # --- REGEX PATTERNS: These will need to be adjusted ---

    try:
        # 1. Last 4 Digits
        # Look for "Account Number:" or "Account ending in"
        match = re.search(r'Account ending in.*?(\d{4})', text, re.IGNORECASE)
        if match:
            data['last_4_digits'] = match.group(1)

        # 2. Payment Due Date
        # US format is often Mmm dd, yyyy (e.g., Oct 25, 2024)
        match = re.search(r'Payment Due Date:.*?(\w{3}\s\d{1,2},\s\d{4})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['due_date'] = match.group(1)

        # 3. Total Amount Due
        # Look for "New Balance"
        match = re.search(r'New Balance.*?\$([\d,]+\.\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['total_due'] = match.group(1).replace(',', '')

        # 4. Statement Period
        # Look for "Opening/Closing Date"
        match = re.search(r'Opening/Closing Date.*?(\d{2}/\d{2}/\d{2})\s*-\s*(\d{2}/\d{2}/\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['statement_period'] = f"{match.group(1)} to {match.group(2)}"
            
    except Exception as e:
        print(f"Error parsing Chase statement: {e}")

    return data
