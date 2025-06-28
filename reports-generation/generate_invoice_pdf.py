import json
import re
import os
import tempfile

from pathlib import Path

try:
    import pypandoc
    HAS_PYPANDOC = True
except ImportError:
    HAS_PYPANDOC = False

try:
    from docx2pdf import convert as docx2pdf_convert
    HAS_DOCX2PDF = True
except ImportError:
    HAS_DOCX2PDF = False

from typing import Dict, Any

def load_json(path: str) -> Any:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_rtf(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def fill_placeholders(template: str, context: Dict[str, Any]) -> str:
    # Replace $placeholders in the template with context values
    def replacer(match):
        key = match.group(1)
        return str(context.get(key, match.group(0)))
    return re.sub(r'\$(\w+)', replacer, template)

def process_foreach(template: str) -> str:
    # Regex to match @foreach(collection as alias) ... @end-foreach
    foreach_regex = re.compile(r'@foreach\((\w+)(?:\s+as\s+(\w+))?\)([\s\S]*?)@end-foreach', re.MULTILINE)
    
    def foreach_replacer(match):
        collection_name = match.group(1)
        alias = match.group(2) or 'd'  # default alias is 'd' if not provided
        block = match.group(3)
        # Load data.json to get the collection
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Find the collection in the first invoice
        collection = data['invoices'][0].get(collection_name, [])
        rendered = ''
        for item in collection:
            # Support nested attribute access: ${alias.key} or ${alias.key.subkey}
            def item_replacer(m):
                expr = m.group(1)
                if not expr.startswith(alias + "."):
                    return m.group(0)
                keys = expr[len(alias)+1:].split('.')
                val = item
                for k in keys:
                    if isinstance(val, dict):
                        val = val.get(k, m.group(0))
                    else:
                        return m.group(0)
                return str(val)
            rendered += re.sub(r'\$\{(' + re.escape(alias) + r'(?:\.[^}]+)?)\}', item_replacer, block)
        return rendered
    # Replace all foreach blocks
    return foreach_regex.sub(foreach_replacer, template)

def rtf_to_pdf(rtf_content: str, output_pdf: str):
    # Save RTF to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.rtf', mode='w', encoding='utf-8') as tmp_rtf:
        tmp_rtf.write(rtf_content)
        tmp_rtf_path = tmp_rtf.name
    # Try pypandoc first
    if HAS_PYPANDOC:
        pypandoc.convert_file(tmp_rtf_path, 'pdf', outputfile=output_pdf)
    elif HAS_DOCX2PDF:
        # Convert RTF to DOCX using pypandoc, then DOCX to PDF
        tmp_docx = tmp_rtf_path.replace('.rtf', '.docx')
        pypandoc.convert_file(tmp_rtf_path, 'docx', outputfile=tmp_docx)
        docx2pdf_convert(tmp_docx, output_pdf)
        os.remove(tmp_docx)
    else:
        raise RuntimeError('No supported RTF to PDF converter found. Please install pypandoc or docx2pdf.')
    os.remove(tmp_rtf_path)

def main():
    data = load_json('data.json')
    template = load_rtf('template2.rtf')
    invoice = data['invoices'][0]  # Just use the first invoice for this example
    # Fill header placeholders
    context = invoice['header']
    filled = fill_placeholders(template, context)
    # Process @foreach for details and aliases
    filled = process_foreach(filled)
    # Output PDF
    output_pdf = 'invoice_output.pdf'
    rtf_to_pdf(filled, output_pdf)
    print(f'Generated PDF: {output_pdf}')

if __name__ == '__main__':
    main() 