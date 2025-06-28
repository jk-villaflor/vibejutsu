const fs = require('fs');
const PDFDocument = require('pdfkit');

// Helper to load JSON
function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

// Create a properly formatted invoice PDF
function createInvoicePdf(invoice, pdfPath) {
  const doc = new PDFDocument({
    size: 'A4',
    margin: 50
  });

  // Pipe the PDF to a file
  const stream = fs.createWriteStream(pdfPath);
  doc.pipe(stream);

  // Header
  doc.fontSize(24).font('Helvetica-Bold').text('INVOICE', { align: 'center' });
  doc.moveDown();

  // Invoice details
  doc.fontSize(12).font('Helvetica');
  doc.text(`Invoice Number: ${invoice.header.invoiceNumber || 'N/A'}`);
  doc.text(`Date: ${invoice.header.date || 'N/A'}`);
  doc.text(`Due Date: ${invoice.header.dueDate || 'N/A'}`);
  doc.moveDown();

  // Company and client info
  if (invoice.header.companyName) {
    doc.fontSize(14).font('Helvetica-Bold').text('From:');
    doc.fontSize(12).font('Helvetica').text(invoice.header.companyName);
    if (invoice.header.companyAddress) {
      doc.text(invoice.header.companyAddress);
    }
    doc.moveDown();
  }

  if (invoice.header.clientName) {
    doc.fontSize(14).font('Helvetica-Bold').text('To:');
    doc.fontSize(12).font('Helvetica').text(invoice.header.clientName);
    if (invoice.header.clientAddress) {
      doc.text(invoice.header.clientAddress);
    }
    doc.moveDown(2);
  }

  // Items table
  if (invoice.items && invoice.items.length > 0) {
    doc.fontSize(14).font('Helvetica-Bold').text('Items:');
    doc.moveDown(0.5);

    // Table header
    const tableTop = doc.y;
    const itemX = 50;
    const qtyX = 250;
    const priceX = 350;
    const totalX = 450;

    doc.fontSize(10).font('Helvetica-Bold');
    doc.text('Item', itemX, tableTop);
    doc.text('Qty', qtyX, tableTop);
    doc.text('Price', priceX, tableTop);
    doc.text('Total', totalX, tableTop);

    let currentY = tableTop + 20;
    let grandTotal = 0;

    // Table rows
    doc.fontSize(10).font('Helvetica');
    for (const item of invoice.items) {
      const itemTotal = (item.quantity || 0) * (item.price || 0);
      grandTotal += itemTotal;

      doc.text(item.name || 'N/A', itemX, currentY);
      doc.text((item.quantity || 0).toString(), qtyX, currentY);
      doc.text(`$${(item.price || 0).toFixed(2)}`, priceX, currentY);
      doc.text(`$${itemTotal.toFixed(2)}`, totalX, currentY);

      currentY += 20;
    }

    // Total line
    doc.moveDown();
    doc.fontSize(12).font('Helvetica-Bold');
    doc.text(`Total: $${grandTotal.toFixed(2)}`, { align: 'right' });
  }

  // Additional notes
  if (invoice.header.notes) {
    doc.moveDown(2);
    doc.fontSize(12).font('Helvetica-Bold').text('Notes:');
    doc.fontSize(10).font('Helvetica').text(invoice.header.notes);
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

async function main() {
  try {
    const data = loadJson('data.json');
    const invoice = data.invoices[0]; // Just use the first invoice for this example
    
    // Create PDF directly
    const outputPdf = 'invoice_output_direct.pdf';
    await createInvoicePdf(invoice, outputPdf);
    
    console.log('Generated PDF:', outputPdf);
  } catch (error) {
    console.error('Error generating PDF:', error.message);
  }
}

main(); 