import fitz  # PyMuPDF
import base64
import math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
def save_reassembled_pdf(text_content, image_b64, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Add text
    text_object = c.beginText(50, height - 50)
    for line in text_content.splitlines():
        text_object.textLine(line)
    c.drawText(text_object)

    # Add image if present
    if image_b64.strip():
        image_bytes = base64.b64decode(image_b64)
        image_path = output_path.replace(".pdf", "_temp_image.png")
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        c.drawImage(image_path, 50, 100, width=400, preserveAspectRatio=True, mask='auto')

        # Clean up temp image file
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Temp image file deleted: {image_path}")

    c.save()
    print(f"Final PDF saved to: {output_path}")

def extract_pdf_content(pdf_path, image_output_path="extracted_image.png"):
    print("Extracting content from PDF...")
    doc = fitz.open(pdf_path)
    page = doc[0]

    # Extract text
    text = page.get_text()
    print(f"Extracted text length: {len(text)} characters")

    # Extract first image (if any)
    image_list = page.get_images(full=True)
    image_b64 = ""
    if image_list:
        xref = image_list[0][0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        print(f"Extracted image size: {len(image_b64)} base64 characters")

        # Save image locally
        #with open(image_output_path, "wb") as f:
         #   f.write(image_bytes)
        #print(f"Image saved to: {image_output_path}")
    else:
        print(" No image found on the page.")

    combined = text + "\n[IMAGE_DATA_START]\n" + image_b64
    print(f"Combined content length: {len(combined)} characters")
    return combined

def chunk_content(content, num_chunks=256):
    print(f"\nChunking content into {num_chunks} parts...")
    chunk_size = math.ceil(len(content) / num_chunks)
    print(f"Each chunk size (approx): {chunk_size} characters")

    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk_data = content[start:end]
        token = f"CHUNK_{i:03d}"
        chunks.append({"token": token, "data": chunk_data})
        print(f"Created {token} with {len(chunk_data)} characters")

    print(f"Total chunks created: {len(chunks)}")
    return chunks

def reassemble_chunks(chunks):
    print("\nReassembling chunks...")
    sorted_chunks = sorted(chunks, key=lambda x: x["token"])
    full_content = ''.join(chunk["data"] for chunk in sorted_chunks)
    print(f"Reassembled content length: {len(full_content)} characters")
    return full_content

pdf_path = r"C:\Users\Sapra\Downloads\sample.pdf"
image_output_path = r"C:\Users\Sapra\Downloads\extracted_image.png"

content = extract_pdf_content(pdf_path, image_output_path=image_output_path)
chunks = chunk_content(content, num_chunks=256)
reconstructed = reassemble_chunks(chunks)

# Optional: Verify reconstruction
if content == reconstructed:
    print("Reconstruction successful — content matches original!")
else:
    print("Reconstruction failed — content mismatch.")
# Split back into text and image
if "[IMAGE_DATA_START]" in reconstructed:
    text_part, image_b64 = reconstructed.split("[IMAGE_DATA_START]", 1)
else:
    text_part = reconstructed
    image_b64 = ""

# Save to PDF
output_path = r"C:\Users\Sapra\Downloads\reconstructed_output.pdf"
save_reassembled_pdf(text_part, image_b64, output_path)