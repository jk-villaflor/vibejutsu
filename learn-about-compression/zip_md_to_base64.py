import os
import zipfile
import base64
import bz2
from io import BytesIO

# Get all .md files in the current directory
md_files = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]

# Create a zipfile in memory
zip_buffer = BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for md_file in md_files:
        zipf.write(md_file)
zip_data = zip_buffer.getvalue()

# Compress the zipfile using bzip2
compressed_zip = bz2.compress(zip_data)

# Encode to base64
encoded = base64.b64encode(compressed_zip).decode('utf-8')

print(f'Base64 Length: {len(encoded)}')
print(f'Base64 String:\n{encoded}\n') 