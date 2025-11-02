import re

def parse(text: str) -> dict:
    """
    Parses HDFC credit card statement text to extract key data.
    
    NOTE: These regex patterns are educated guesses and will
    need to be fine-tuned based on the *actual* statement text.
    
    Args:
        text: The full text extracted from the PDF.
        
    Returns:
        A dictionary containing the extracted data.
    """
    data = {
        'issuer': 'HDFC',
        'last_4_digits': None,
        'due_date': None,
        'total_due': None,
        'statement_period': None
    }
    
    # --- REGEX PATTERNS: These will need to be adjusted ---
    
    try:
        # 1. Last 4 Digits
        # Look for "Card No." followed by XXXX XXXX XXXX 1234
        match = re.search(r'Card No\..*?(\d{4})', text, re.IGNORECASE)
        if match:
            data['last_4_digits'] = match.group(1)

        # 2. Payment Due Date
        # Look for "Payment Due Date" followed by dd/mm/yyyy or dd-mmm-yy
        match = re.search(r'Payment Due Date.*?([\d]{2}/[\d]{2}/[\d]{4})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['due_date'] = match.group(1)

        # 3. Total Amount Due
        # Look for "Total Amount Due" followed by a currency symbol and amount
        match = re.search(r'Total Amount Due.*?([\d,]+\.\d{2})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['total_due'] = match.group(1).replace(',', '') # Clean the amount

        # 4. Statement Period
        # Look for "Statement Period" followed by two dates
        match = re.search(r'Statement Period.*?(\d{2}/\d{2}/\d{4})\s*to\s*(\d{2}/\d{2}/\d{4})', text, re.IGNORECASE | re.DOTALL)
        if match:
            data['statement_period'] = f"{match.group(1)} to {match.group(2)}"
            
    except Exception as e:
        print(f"Error parsing HDFC statement: {e}")
        
    return data
