const fs = require('fs');
const PDFDocument = require('pdfkit');

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

  console.log('context =>', context);

  // Support nested keys like $header.customer_name or $details[0].description
  return template.replace(/\$(\w+(?:\.[\w\d_]+)*)/g, (match, keyPath) => {
    console.log('match =>', match);
    // console.log('keyPath =>', keyPath);
    const keys = keyPath.split('.');
    console.log('keys =>', keys);
    let val = context;
    console.log('val =>', val && typeof val === 'object');
    for (const k of keys) {
      if (val && typeof val === 'object' && k in val) {
        val = val[k];
      // } else {
        // return match;
      }
    }
    return val;
  });
}

// Process @foreach(collection as alias) ... @end-foreach
function processForeach(template, context) {
  const foreachRegex = /@foreach\((\w+)(?:\s+as\s+(\w+))?\)([\s\S]*?)@end-foreach/gm;
  return template.replace(foreachRegex, (match, collectionName, alias, block) => {
    alias = alias || 'd';
    const collection = context[collectionName] || [];
    let rendered = '';
    for (const item of collection) {
      rendered += block.replace(new RegExp(`\$\{${alias}((?:\.[^}}]+)+)\}`, 'g'), (m, expr) => {
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

// Convert filled template content to PDF using pdfkit
function createPdfFromContent(content, pdfPath) {
  const doc = new PDFDocument({
    size: 'A4',
    margin: 50
  });

  // Pipe the PDF to a file
  const stream = fs.createWriteStream(pdfPath);
  doc.pipe(stream);

  // Parse the content and add to PDF
  const lines = content.split('\n');
  
  // Track current position and formatting
  let currentY = 50;
  let inTable = false;
  let tableData = [];
  
  for (const line of lines) {
    // Skip RTF control words and focus on actual content
    if (line.trim() && !line.startsWith('\\') && !line.startsWith('{') && !line.startsWith('}')) {
      // Clean up RTF formatting
      const cleanLine = line
        .replace(/\\[a-z0-9-]+/g, '') // Remove RTF control words
        .replace(/[{}]/g, '') // Remove RTF braces
        .trim();
      
      if (cleanLine) {
        // Check for specific patterns in the content
        if (cleanLine.toUpperCase() === 'INVOICE') {
          doc.fontSize(24).font('Helvetica-Bold').text(cleanLine, { align: 'center' });
          doc.moveDown(2);
        } else if (cleanLine.includes('Invoice Number:') || cleanLine.includes('Date:') || cleanLine.includes('Due Date:')) {
          doc.fontSize(12).font('Helvetica').text(cleanLine);
          doc.moveDown(0.5);
        } else if (cleanLine === 'From:' || cleanLine === 'To:') {
          doc.fontSize(14).font('Helvetica-Bold').text(cleanLine);
          doc.moveDown(0.5);
        } else if (cleanLine === 'Items:' || cleanLine.includes('Item') && cleanLine.includes('Qty') && cleanLine.includes('Price')) {
          // Start of items table
          doc.fontSize(14).font('Helvetica-Bold').text('Items:');
          doc.moveDown(0.5);
          inTable = true;
          tableData = [];
        } else if (inTable && (cleanLine.includes('$') || /^\d+/.test(cleanLine))) {
          // This looks like table data
          tableData.push(cleanLine);
        } else if (cleanLine.includes('Total:') || cleanLine.includes('Amount:')) {
          // End of table, render it
          if (tableData.length > 0) {
            renderTable(doc, tableData);
            tableData = [];
            inTable = false;
          }
          doc.fontSize(12).font('Helvetica-Bold').text(cleanLine, { align: 'right' });
          doc.moveDown();
        } else if (cleanLine === 'Notes:') {
          doc.fontSize(12).font('Helvetica-Bold').text(cleanLine);
          doc.moveDown(0.5);
        } else if (cleanLine.length > 0) {
          // Regular content
          if (cleanLine.toUpperCase() === cleanLine && cleanLine.length > 3) {
            doc.fontSize(14).font('Helvetica-Bold').text(cleanLine);
          } else {
            doc.fontSize(10).font('Helvetica').text(cleanLine);
          }
          doc.moveDown(0.5);
        }
      }
    }
  }

  // Render any remaining table data
  if (tableData.length > 0) {
    renderTable(doc, tableData);
  }

  // Footer
  doc.moveDown(3);
  doc.fontSize(10).font('Helvetica').text('Thank you for your business!', { align: 'center' });

  // Finalize the PDF
  doc.end();

  return new Promise((resolve, reject) => {
    stream.on('finish', () => {
      console.log('PDF created successfully');
      resolve();
    });
    stream.on('error', reject);
  });
}

// Helper function to render table data
function renderTable(doc, tableData) {
  const tableTop = doc.y;
  const itemX = 50;
  const qtyX = 250;
  const priceX = 350;
  const totalX = 450;

  // Table header
  doc.fontSize(10).font('Helvetica-Bold');
  doc.text('Item', itemX, tableTop);
  doc.text('Qty', qtyX, tableTop);
  doc.text('Price', priceX, tableTop);
  doc.text('Total', totalX, tableTop);

  let currentY = tableTop + 20;

  // Table rows
  doc.fontSize(10).font('Helvetica');
  for (const row of tableData) {
    // Parse the row data - this is a simplified parser
    const parts = row.split(/\s+/).filter(part => part.trim());
    if (parts.length >= 4) {
      const itemName = parts[0];
      const qty = parts[1];
      const price = parts[2];
      const total = parts[3];

      doc.text(itemName, itemX, currentY);
      doc.text(qty, qtyX, currentY);
      doc.text(price, priceX, currentY);
      doc.text(total, totalX, currentY);

      currentY += 20;
    }
  }

  doc.y = currentY + 10;
}

async function main() {
  try {
    console.log('Loading data and template...');
    const data = loadJson('data.json');
    const template = loadRtf('template2.rtf');
    const invoice = data.invoices[0]; // Just use the first invoice for this example

    // console.log(invoice);
    
    console.log('Processing template with data...');
    // Use the entire invoice object for placeholder replacement
    let filled = fillPlaceholders(template, invoice);
    filled = processForeach(filled, invoice);
    
    // // Write filled RTF to temp file for debugging
    // const tempRtf = 'filled_invoice.rtf';
    // fs.writeFileSync(tempRtf, filled, 'utf-8');
    // console.log('Filled template saved to:', tempRtf);
    
    // // Convert to PDF using pdfkit
    // const outputPdf = 'invoice_output.pdf';
    // console.log('Generating PDF...');
    // await createPdfFromContent(filled, outputPdf);
    
    // console.log('Successfully generated PDF:', outputPdf);
    // console.log('Files created:');
    // console.log('  -', tempRtf, '(filled template)');
    // console.log('  -', outputPdf, '(final PDF)');
    
  } catch (error) {
    console.error('Error generating PDF:', error.message);
    console.error('Stack trace:', error.stack);
  }
}

main(); 