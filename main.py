import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import pandas as pd

# Function to perform OCR on a PDF and extract text
def ocr_pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text_from_all_pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        image_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        page_text = pytesseract.image_to_string(image_data)
        text_from_all_pages.append(page_text)
    doc.close()
    return ' '.join(text_from_all_pages)

# Function to perform OCR on an image and extract text
def ocr_image_to_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

# Function to extract key-value pairs from OCR text

def extract_key_value_pairs(text):
    key_value_data = {}
    # Define your patterns here based on the provided invoice structure
    patterns = {
        'Invoice Number': r'Invoice no\.\s*([A-Z0-9-]+)',
        'Payment Date': r'Payment date\:\s*(\d{2}/\d{2}/\d{4})',
        'Total': r'Total CHF\s*([0-9,.]+)',
        'Customer Name': r'Payment\:\nMr\.\s(.+?)\n',  # Extract customer name
        'Customer Address': r'\nMr\. .+?\n(.+?)\nCredit Card',  # Extract customer address
        
        
        
        
    
        # Add more patterns as needed
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            key_value_data[key] = match.group(1).strip()  # Strip to remove leading/trailing whitespace
    return key_value_data


# Main execution
def main():
    # List to hold all the extracted data
    all_data = []
    # Get a list of all files in the current directory
   
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.lower().endswith('.pdf'):
            try:
                ocr_text = ocr_pdf_to_text(file)
                extracted_data = extract_key_value_pairs(ocr_text)
                extracted_data['Filename'] = file  # Add the filename to the data
                all_data.append(extracted_data)
            except Exception as e:
                print(f"An error occurred with file {file}: {e}")
        elif file.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                ocr_text = ocr_image_to_text(file)
                extracted_data = extract_key_value_pairs(ocr_text)
                extracted_data['Filename'] = file  # Add the filename to the data
                all_data.append(extracted_data)
            except Exception as e:
                print(f"An error occurred with file {file}: {e}")

    # Convert all data to a DataFrame and save as a CSV file
    df = pd.DataFrame(all_data)
    df.to_csv('extracted_data.csv', index=False)

if __name__ == "__main__":
    main()
