import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, output_txt_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    with open(output_txt_path, "w") as f:
        f.write(full_text)
    print(f"✅ Extracted text saved to: {output_txt_path}")

# Example usage
extract_text_from_pdf("malawi_data_protection_act.pdf", "data_protection_malawi.txt")