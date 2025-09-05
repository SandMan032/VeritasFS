from file_processor import FileProcessor
# Initialize processor: uses ./data and creates ./output
processor = FileProcessor(num_chunks=256)
# Step 1: Transmit all files (chunk them)
processor.transmit()
# Step 2: Reassemble all files into output folder
processor.reassemble()
