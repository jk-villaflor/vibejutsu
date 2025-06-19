import os
import base64

# Get all .bin files in the current directory
bin_files = [f for f in os.listdir('.') if f.endswith('.bin') and os.path.isfile(f)]

for bin_file in bin_files:
    with open(bin_file, 'rb') as file:
        data = file.read()
        # Encode to base64
        encoded = base64.b64encode(data).decode('utf-8')
        print(f'File: {bin_file}')
        print(f'Base64 Length: {len(encoded)}')
        print(f'Base64 String:\n{encoded}\n') 