
import os
import math

class FileProcessor:
    def __init__(self, folder_name="data/input", num_chunks=256):
        self.folder_name = folder_name
        self.num_chunks = num_chunks
        self.file_chunks = {}

        # Use folder relative to script location
        self.projectroot= os.path.abspath(os.getcwd())
        self.input_folder = os.path.join(self.projectroot, self.folder_name)

        if not os.path.exists(self.input_folder):
            raise FileNotFoundError(f"❌ Folder '{folder_name}' not found next to script.")

        # Create output folder next to input
        self.output_folder = os.path.join(self.projectroot, "data/output")
        os.makedirs(self.output_folder, exist_ok=True)

        print(f"📂 Input folder: {self.input_folder}")
        print(f"📁 Output folder: {self.output_folder}")

    def read_file_bytes(self, file_path):
        with open(file_path, "rb") as f:
            return f.read()

    def chunk_bytes(self, data):
        chunk_size = math.ceil(len(data) / self.num_chunks)
        return [
            {"token": f"CHUNK_{i:03d}", "data": data[i * chunk_size : min((i + 1) * chunk_size, len(data))]}
            for i in range(self.num_chunks)
        ]

    def transmit(self):
        files = [f for f in os.listdir(self.input_folder) if os.path.isfile(os.path.join(self.input_folder, f))]
        if not files:
            print("⚠️ No files found in input folder.")
            return

        for filename in files:
            input_path = os.path.join(self.input_folder, filename)
            data = self.read_file_bytes(input_path)
            chunks = self.chunk_bytes(data)
            self.file_chunks[filename] = {"chunks": chunks, "original_data": data}
            print(f"📤 Transmitted '{filename}' into {len(chunks)} chunks.")

    def reassemble(self):
        for filename, info in self.file_chunks.items():
            sorted_chunks = sorted(info["chunks"], key=lambda x: x["token"])
            reconstructed_data = b''.join(chunk["data"] for chunk in sorted_chunks)

            output_path = os.path.join(self.output_folder, f"reconstructed_{filename}")
            with open(output_path, "wb") as f:
                f.write(reconstructed_data)

            if reconstructed_data == info["original_data"]:
                print(f"✅ '{filename}' reconstructed successfully ({len(reconstructed_data)} bytes)")
            else:
                print(f"⚠️ '{filename}' reconstruction mismatch!")

