from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_folder):
    reader = PdfReader(input_pdf_path)

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = f"{output_folder}/page_{i+1}.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"Saved: {output_path}")

# 예시 사용
split_pdf("sample.pdf", "output_pages")


# import fitz  # PyMuPDF
# import os

# def split_pdf_with_pymupdf(input_pdf_path, output_folder):
#     os.makedirs(output_folder, exist_ok=True)
#     doc = fitz.open(input_pdf_path)

#     for i in range(len(doc)):
#         single_page = fitz.open()
#         single_page.insert_pdf(doc, from_page=i, to_page=i)

#         output_path = os.path.join(output_folder, f"page_{i+1}.pdf")
#         single_page.save(output_path)
#         print(f"Saved: {output_path}")

# # 예시 사용
# split_pdf_with_pymupdf("sample.pdf", "output_pages")