import math
import os

def read_pdf_as_bytes(pdf_path):
    with open(pdf_path, "rb") as f:
        data = f.read()
    print(f"Read {len(data)} bytes from {pdf_path}")
    return data

def chunk_raw_bytes(data, num_chunks=256):
    print(f"\nChunking PDF into {num_chunks} parts...")
    chunk_size = math.ceil(len(data) / num_chunks)
    print(f"Each chunk size (approx): {chunk_size} bytes")

    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, len(data))
        chunk_data = data[start:end]
        token = f"CHUNK_{i:03d}"
        chunks.append({
            "token": token,
            "data": chunk_data
        })
        print(f"Created {token} with {len(chunk_data)} bytes")

    print(f"Total chunks created: {len(chunks)}")
    return chunks

def reassemble_chunks(chunks):
    print("\nReassembling chunks back into raw PDF...")
    sorted_chunks = sorted(chunks, key=lambda x: x["token"])
    reconstructed_data = b''.join(chunk["data"] for chunk in sorted_chunks)
    print(f"Reassembled PDF size: {len(reconstructed_data)} bytes")
    return reconstructed_data

def save_pdf_from_bytes(data, output_path):
    with open(output_path, "wb") as f:
        f.write(data)
    print(f"Final reconstructed PDF saved to: {output_path}")

pdf_path = r"./data/sample.pdf"
output_path = r"./data/reconstructed_output.pdf"

pdf_bytes = read_pdf_as_bytes(pdf_path)
chunks = chunk_raw_bytes(pdf_bytes, num_chunks=256)
reconstructed_bytes = reassemble_chunks(chunks)

if pdf_bytes == reconstructed_bytes:
    print("Reconstruction successful — bytes match original perfectly!")
else:
    print("Reconstruction failed — mismatch detected!")

save_pdf_from_bytes(reconstructed_bytes, output_path)