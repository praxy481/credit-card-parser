import pdfplumber
import sys
import os

def extract_text(file_path: str) -> str:
    """
    Extracts all text from a .pdf file.

    Args:
        file_path: The file path to the PDF.

    Returns:
        A single string containing all text.
        Returns None if extraction fails or file is not a .pdf.
    """
    
    # Get the file extension
    _, extension = os.path.splitext(file_path)
    
    if extension.lower() != '.pdf':
        print(f"Skipping non-PDF file: {file_path}", file=sys.stderr)
        return None
        
    # --- PDF Extraction Logic ---
    full_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + f"\n--- Page {i+1} ---\n"
            
            if not full_text and len(pdf.pages) > 0:
                print(f"Warning: No text extracted from {file_path}. It might be an image-based PDF (scanned).", file=sys.stderr)
                return None
        return full_text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}", file=sys.stderr)
        return None


if __name__ == '__main__':
    # A simple test to run this file directly
    # Make sure to place a real PDF in ../samples/
    
    print("--- Testing PDF Extraction ---")
    # You can change this to one of your actual PDF filenames to test
    sample_pdf = '../samples/HDFC Bank Monthly Statement.pdf'
    
    if os.path.exists(sample_pdf):
        print(f"Testing text extraction on {sample_pdf}...")
        text = extract_text(sample_pdf)
        if text:
            print("--- EXTRACTION SUCCESSFUL ---")
            print(text[:500] + "\n...")
        else:
            print("--- EXTRACTION FAILED ---")
    else:
        print(f"Test PDF not found: {sample_pdf}. Make sure it exists to test extract.py")

