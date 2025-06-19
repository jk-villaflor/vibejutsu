import os
import bz2
from io import BytesIO

# Get all .md files in the current directory
md_files = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]

for md_file in md_files:
    with open(md_file, 'rb') as file:
        data = file.read()
        # Compress using bzip2
        compressed_data = bz2.compress(data)
        # Write compressed binary to .bin file
        bin_filename = md_file + '.bin'
        with open(bin_filename, 'wb') as bin_file:
            bin_file.write(compressed_data)
        print(f'Compressed binary written to: {bin_filename}') 