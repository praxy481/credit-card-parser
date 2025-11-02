import os
import json
import glob
import re
import sys
from extract import extract_text

# --- Import all available parser modules ---
# UPDATED: Changed imports to match your filenames (e.g., hdfc_parser)
from hdfc_parser import parse as parse_hdfc
from icici_parser import parse as parse_icici
from chase_parser import parse as parse_chase
from amex_parser import parse as parse_amex
from citi_parser import parse as parse_citi

# --- Define the Parser "Strategy" Map ---
# NOTE: The keys here are used for *identification*
# They must match the text found in the PDF.
PARSER_MAP = {
    'HDFC Bank': parse_hdfc,
    'ICICI Bank': parse_icici,
    'Chase': parse_chase,
    'American Express': parse_amex,
    'Citi': parse_citi,
}

def identify_issuer_and_parse(text: str, file_name: str) -> dict:
    """
    Identifies the issuer from text and calls the correct parser.
    """
    
    # Check for keywords from our map
    for issuer_keyword, parser_func in PARSER_MAP.items():
        # Check if the keyword (e.g., "HDFC Bank") is in the extracted text
        if re.search(issuer_keyword, text, re.IGNORECASE):
            print(f"  -> Identified as {issuer_keyword}. Parsing...")
            return parser_func(text)
            
    # If no parser is found
    print(f"  -> Error: Unknown issuer for file {file_name}. No parser found.")
    return {
        'issuer': 'Unknown',
        'error': 'No matching parser found for this statement.'
    }

def main():
    """
    Main function to orchestrate the parsing.
    - Finds all .pdf files in ../samples/
    - Extracts text from each
    - Identifies the issuer
    - Calls the specific parser
    - Saves all results to ../output/results.json
    """
    
    # Use os.path.join for better cross-platform compatibility
    script_dir = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(script_dir, '..'))
    sample_dir = os.path.join(base_dir, 'samples')
    output_dir = os.path.join(base_dir, 'output')
    output_file = os.path.join(output_dir, 'results.json')
    
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    # --- Find only .pdf files ---
    print(f"Scanning {sample_dir} for .pdf files...")
    
    # Search recursively (**) inside the samples directory
    search_pattern = os.path.join(sample_dir, '**', '*.pdf')
    all_files = glob.glob(search_pattern, recursive=True)
    
    if not all_files:
        print(f"No .pdf files found in {sample_dir}.")
        print("Please add your sample PDF statements to that directory to proceed.")
        return

    print(f"Found {len(all_files)} file(s). Starting parsing...")
    
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        print(f"\nProcessing {file_name}...")
        
        # 1. Extract Text
        full_text = extract_text(file_path)
        
        if not full_text:
            print(f"  -> Error: Could not extract text from {file_name}. Skipping.")
            results.append({
                'file': file_name,
                'error': 'Failed to extract text. File might be image-based or corrupt.'
            })
            continue
            
        # 2. Identify and Parse
        data = identify_issuer_and_parse(full_text, file_name)
        
        # 3. Store Result
        data['file'] = file_name
        results.append(data)
        
    # 4. Write all results to the JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"\nError writing to {output_file}: {e}", file=sys.stderr)
        
    print(f"\n--- Parsing complete. ---")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Ensure src directory is in path if running directly
    sys.path.append(os.path.dirname(__file__))
    main()

