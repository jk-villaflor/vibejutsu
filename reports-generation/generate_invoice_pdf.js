const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Helper to load JSON
function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

// Helper to load RTF
function loadRtf(filePath) {
  return fs.readFileSync(filePath, 'utf-8');
}

// Fill $placeholders in the template with context values
function fillPlaceholders(template, context) {
  return template.replace(/\$(\w+)/g, (match, key) =>
    context[key] !== undefined ? context[key] : match
  );
}

// Process @foreach(collection as alias) ... @end-foreach
function processForeach(template, invoice) {
  const foreachRegex = /@foreach\((\w+)(?:\s+as\s+(\w+))?\)([\s\S]*?)@end-foreach/gm;
  return template.replace(foreachRegex, (match, collectionName, alias, block) => {
    alias = alias || 'd';
    const collection = invoice[collectionName] || [];
    let rendered = '';
    for (const item of collection) {
      rendered += block.replace(new RegExp(`\\$\\{${alias}((?:\\.[^}}]+)+)\\}`, 'g'), (m, expr) => {
        // expr is like .key or .key.subkey
        const keys = expr.slice(1).split('.');
        let val = item;
        for (const k of keys) {
          if (val && typeof val === 'object' && k in val) {
            val = val[k];
          } else {
            return m;
          }
        }
        return val;
      });
    }
    return rendered;
  });
}

// Convert RTF to PDF using LibreOffice (needs to be installed)
function rtfToPdf(rtfPath, pdfPath) {
  // LibreOffice must be installed and in PATH
  try {
    execSync(`soffice --headless --convert-to pdf --outdir "${path.dirname(pdfPath)}" "${rtfPath}"`);
    // Move the generated PDF to the desired path if needed
    const generatedPdf = path.join(path.dirname(rtfPath), path.basename(rtfPath, '.rtf') + '.pdf');
    if (generatedPdf !== pdfPath) {
      fs.renameSync(generatedPdf, pdfPath);
    }
  } catch (err) {
    throw new Error('LibreOffice conversion failed: ' + err.message);
  }
}

function main() {
  const data = loadJson('data.json');
  const template = loadRtf('template2.rtf');
  const invoice = data.invoices[0]; // Just use the first invoice for this example
  let filled = fillPlaceholders(template, invoice.header);
  filled = processForeach(filled, invoice);
  // Write filled RTF to temp file
  const tempRtf = 'filled_invoice.rtf';
  fs.writeFileSync(tempRtf, filled, 'utf-8');
  // Convert to PDF
  const outputPdf = 'invoice_output.pdf';
  rtfToPdf(tempRtf, outputPdf);
  console.log('Generated PDF:', outputPdf);
}

main(); 