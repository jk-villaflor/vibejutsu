import os
import base64
import bz2
from io import BytesIO

# Get all .md files in the current directory
md_files = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]

for md_file in md_files:
    with open(md_file, 'rb') as file:
        data = file.read()
        # Compress using bzip2
        compressed_data = bz2.compress(data)
        # Encode to base64
        encoded = base64.b64encode(compressed_data).decode('utf-8')
        print(f'File: {md_file}')
        print(f'Base64 Length: {len(encoded)}')
        print(f'Base64 String:\n{encoded}\n') 