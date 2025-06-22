const express = require('express');
const PDFDocument = require('pdfkit');
const ExcelJS = require('exceljs');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3300;

// Static data matching the screenshot fields
const staticData = {
  weekEnding: 'Date',
  today: 'Date',
  salesperson: 'Name',
  location: 'Location',
  days: [
    {
      name: 'Monday',
      values: [14, 23, 4, 45, 22, 2, 100, 0, 0, 0, 210],
    },
    {
      name: 'Tuesday',
      values: [23, 76, 10, 50, 54, 45, 80, 0, 0, 0, 338],
    },
    {
      name: 'Wednesday',
      values: [4, 130, 11, 33, 67, 65, 400, 0, 0, 0, 710],
    },
    {
      name: 'Thursday',
      values: [102, 40, 18, 0, 86, 82, 97, 0, 0, 0, 425],
    },
    {
      name: 'Friday',
      values: [33, 55, 22, 49, 143, 26, 50, 0, 0, 0, 378],
    },
    {
      name: 'Saturday',
      values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    },
    {
      name: 'Sunday',
      values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    },
  ],
  categories: [
    'IN SALES OFFICE',
    'OUTSIDE OFFICE',
    'IN OFFICE VISITS',
    'OUTSIDE CALLS',
    'FILE PHONE CALLS',
    'NEW ACCT. PHONE',
    'GUEST ROOMS',
    'FOOD & BEVERAGE',
    'MTG. ROOM RENTAL',
    'OTHER*',
    'TOTAL',
  ],
  totals: [176, 324, 65, 177, 372, 220, 727, 0, 0, 0, 2061],
  goal: [200, 400, 300, 65, 500, 300, 400, 600, 300, 300, 3365],
  variance: [-24, -76, -235, 112, -128, -80, 327, -600, -300, -300, -1304],
  explanation: '',
  items: [
    { name: 'Item 1', value: 100 },
    { name: 'Item 2', value: 200 },
    { name: 'Item 3', value: 300 },
  ],
};

const RTF_TEMPLATE_PATH = path.join(__dirname, 'template.rtf');

// Helper: Generate PDF Buffer
function generatePDF(data) {
  const doc = new PDFDocument({ margin: 30, size: 'A4', layout: 'landscape' });
  const buffers = [];
  doc.on('data', buffers.push.bind(buffers));
  doc.on('end', () => {});

  // Header
  doc.fontSize(22).fillColor('#222').font('Helvetica-Bold').text('WEEKLY ', { continued: true });
  doc.fillColor('#4CAF50').text('SALES ACTIVITY', { continued: false });
  doc.moveDown(0.5);
  doc.fontSize(10).fillColor('#222').font('Helvetica').text(`SALESPERSON  ${data.salesperson}`, { continued: true, align: 'left' });
  doc.text('WEEK ENDING  ' + data.weekEnding, { align: 'right' });
  doc.text(`LOCATION  ${data.location}`, { continued: true, align: 'left' });
  doc.text("TODAY'S DATE  " + data.today, { align: 'right' });
  doc.moveDown(1);

  // Table
  const tableTop = doc.y;
  const colWidths = [60, 65, 65, 65, 65, 65, 65, 65, 65, 65, 70];
  const startX = doc.x;

  // Draw header row
  doc.font('Helvetica-Bold').fontSize(9).fillColor('#B97A2A');
  doc.rect(startX, tableTop, colWidths.reduce((a, b) => a + b), 20).fillAndStroke('#fff3e0', '#fff3e0');
  doc.fillColor('#B97A2A').text('DAYS', startX + 2, tableTop + 5, { width: colWidths[0] - 4, align: 'left' });
  let x = startX + colWidths[0];
  data.categories.forEach((cat, i) => {
    doc.text(cat, x + 2, tableTop + 5, { width: colWidths[i + 1] - 4, align: 'center' });
    x += colWidths[i + 1];
  });

  // Draw day rows
  let y = tableTop + 20;
  data.days.forEach((day, rowIdx) => {
    doc.font('Helvetica').fontSize(9).fillColor('#222');
    doc.rect(startX, y, colWidths.reduce((a, b) => a + b), 20).fill(rowIdx % 2 === 0 ? '#fff' : '#f5f5f5');
    doc.fillColor('#222').text(day.name, startX + 2, y + 5, { width: colWidths[0] - 4, align: 'left' });
    x = startX + colWidths[0];
    day.values.forEach((val, i) => {
      doc.text(val === 0 ? '$0.00' : `$${val.toFixed(2)}`, x + 2, y + 5, { width: colWidths[i + 1] - 4, align: 'right' });
      x += colWidths[i + 1];
    });
    y += 20;
  });

  // Totals row
  doc.font('Helvetica-Bold').fillColor('#fff');
  doc.rect(startX, y, colWidths.reduce((a, b) => a + b), 20).fill('#21523B');
  doc.text('Totals', startX + 2, y + 5, { width: colWidths[0] - 4, align: 'left' });
  x = startX + colWidths[0];
  data.totals.forEach((val, i) => {
    doc.text(`$${val.toFixed(2)}`, x + 2, y + 5, { width: colWidths[i + 1] - 4, align: 'right' });
    x += colWidths[i + 1];
  });
  y += 20;

  // Goal row
  doc.font('Helvetica').fillColor('#B97A2A');
  doc.rect(startX, y, colWidths.reduce((a, b) => a + b), 20).fill('#fff3e0');
  doc.text('GOAL', startX + 2, y + 5, { width: colWidths[0] - 4, align: 'left' });
  x = startX + colWidths[0];
  data.goal.forEach((val, i) => {
    doc.text(`$${val.toFixed(2)}`, x + 2, y + 5, { width: colWidths[i + 1] - 4, align: 'right' });
    x += colWidths[i + 1];
  });
  y += 20;

  // Variance row
  doc.font('Helvetica').fillColor('#21523B');
  doc.rect(startX, y, colWidths.reduce((a, b) => a + b), 20).fill('#e0e0e0');
  doc.text('VARIANCE', startX + 2, y + 5, { width: colWidths[0] - 4, align: 'left' });
  x = startX + colWidths[0];
  data.variance.forEach((val, i) => {
    doc.text(val > 0 ? `$${val.toFixed(2)}` : `-$${Math.abs(val).toFixed(2)}`, x + 2, y + 5, { width: colWidths[i + 1] - 4, align: 'right' });
    x += colWidths[i + 1];
  });
  y += 30;

  // Explanation box
  doc.font('Helvetica').fontSize(10).fillColor('#222');
  doc.text('*EXPLANATION', startX, y);
  y += 15;
  doc.rect(startX, y, colWidths.reduce((a, b) => a + b), 30).stroke();
  y += 40;

  // Approval line
  doc.text('Approval', startX, y);
  y += 10;
  doc.moveTo(startX, y + 10).lineTo(startX + 200, y + 10).stroke();

  doc.end();
  return new Promise((resolve) => {
    doc.on('end', () => {
      const pdfBuffer = Buffer.concat(buffers);
      resolve(pdfBuffer);
    });
  });
}

// Helper: Generate XLS Buffer
async function generateXLS(data) {
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet('Weekly Report');

  // Header
  sheet.mergeCells('A1:K1');
  sheet.getCell('A1').value = 'WEEKLY SALES ACTIVITY';
  sheet.getCell('A1').font = { bold: true, size: 16 };
  sheet.getCell('A1').alignment = { horizontal: 'center' };

  sheet.getCell('A2').value = 'SALESPERSON';
  sheet.getCell('B2').value = data.salesperson;
  sheet.getCell('D2').value = 'WEEK ENDING';
  sheet.getCell('E2').value = data.weekEnding;
  sheet.getCell('G2').value = 'LOCATION';
  sheet.getCell('H2').value = data.location;
  sheet.getCell('J2').value = "TODAY'S DATE";
  sheet.getCell('K2').value = data.today;

  // Table header
  sheet.addRow([]);
  const headerRow = ['DAYS', ...data.categories];
  sheet.addRow(headerRow);
  const header = sheet.getRow(4);
  header.font = { bold: true, color: { argb: 'FFB97A2A' } };
  header.alignment = { horizontal: 'center' };
  header.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF3E0' } };

  // Day rows
  data.days.forEach((day) => {
    const row = [day.name, ...day.values.map((v) => v === 0 ? '$0.00' : `$${v.toFixed(2)}`)];
    sheet.addRow(row);
  });

  // Totals row
  const totalsRow = ['Totals', ...data.totals.map((v) => `$${v.toFixed(2)}`)];
  sheet.addRow(totalsRow);
  const totals = sheet.getRow(sheet.lastRow.number);
  totals.font = { bold: true, color: { argb: 'FFFFFFFF' } };
  totals.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF21523B' } };

  // Goal row
  const goalRow = ['GOAL', ...data.goal.map((v) => `$${v.toFixed(2)}`)];
  sheet.addRow(goalRow);
  const goal = sheet.getRow(sheet.lastRow.number);
  goal.font = { bold: true, color: { argb: 'FFB97A2A' } };
  goal.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF3E0' } };

  // Variance row
  const varianceRow = ['VARIANCE', ...data.variance.map((v) => v > 0 ? `$${v.toFixed(2)}` : `-$${Math.abs(v).toFixed(2)}`)];
  sheet.addRow(varianceRow);
  const variance = sheet.getRow(sheet.lastRow.number);
  variance.font = { bold: true, color: { argb: 'FF21523B' } };
  variance.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFE0E0E0' } };

  // Explanation box
  sheet.addRow([]);
  sheet.addRow(['*EXPLANATION']);
  sheet.addRow(['']);
  sheet.addRow(['Approval']);
  sheet.addRow(['']);

  // Set column widths
  [12, 14, 14, 14, 14, 14, 14, 14, 14, 14, 16].forEach((w, i) => {
    sheet.getColumn(i + 1).width = w;
  });

  const buffer = await workbook.xlsx.writeBuffer();
  return buffer;
}

// Helper: Fill RTF template with data
function fillRtfTemplate(template, data) {
  let flat = {
    salesperson: data.salesperson,
    weekEnding: data.weekEnding,
    today: data.today,
    location: data.location,
  };
  let result = template;
  // Handle iteration blocks: ${#items}...${/items}
  result = result.replace(/\$\{#(\w+)\}([\s\S]*?)\$\{\/\1\}/g, (match, arrName, block) => {
    if (!Array.isArray(data[arrName])) return '';
    return data[arrName].map(item => {
      let itemBlock = block;
      Object.keys(item).forEach(key => {
        itemBlock = itemBlock.replace(new RegExp(`\\$\{${key}\}`, 'g'), item[key]);
      });
      return itemBlock;
    }).join('');
  });
  // Flat replacements
  Object.keys(flat).forEach(key => {
    result = result.replace(new RegExp(`\\$\{${key}\}`, 'g'), flat[key]);
  });
  data.categories.forEach((cat, i) => {
    result = result.replace(new RegExp(`\\$\{totals_${cat.replace(/[^A-Za-z0-9]/g, '')}\}`, 'g'), data.totals[i]);
    result = result.replace(new RegExp(`\\$\{goal_${cat.replace(/[^A-Za-z0-9]/g, '')}\}`, 'g'), data.goal[i]);
    result = result.replace(new RegExp(`\\$\{variance_${cat.replace(/[^A-Za-z0-9]/g, '')}\}`, 'g'), data.variance[i]);
  });
  data.days.forEach(day => {
    data.categories.forEach((cat, i) => {
      result = result.replace(new RegExp(`\\$\{day_${day.name}_${cat.replace(/[^A-Za-z0-9]/g, '')}\}`, 'g'), day.values[i]);
    });
  });
  return result;
}

// Endpoint: Download PDF
app.get('/report/pdf', async (req, res) => {
  const pdfBuffer = await generatePDF(staticData);
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', 'attachment; filename="sales-activity-report.pdf"');
  res.send(pdfBuffer);
});

// Endpoint: Download XLS
app.get('/report/xls', async (req, res) => {
  const xlsBuffer = await generateXLS(staticData);
  res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
  res.setHeader('Content-Disposition', 'attachment; filename="sales-activity-report.xlsx"');
  res.send(xlsBuffer);
});

// Route: Download filled RTF report as PDF
app.get('/report/rtf', (req, res) => {
  fs.readFile(RTF_TEMPLATE_PATH, 'utf8', (err, template) => {
    if (err) {
      res.status(500).send('RTF template not found.');
      return;
    }
    const filled = fillRtfTemplate(template, staticData);
    // Simple RTF to plain text for demo: remove RTF commands, keep text and line breaks
    let plain = filled
      .replace(/\\par/g, '\n')
      .replace(/\\tab/g, '\t')
      .replace(/\{\\[^}]+\}/g, '') // remove fonttbl and other RTF groups
      .replace(/\\[a-z]+[0-9]*/g, '') // remove other RTF commands
      .replace(/\{\}|\}/g, '') // remove leftover braces
      .replace(/\n/g, '\n');
    // Generate PDF from plain text
    const doc = new PDFDocument({ margin: 30, size: 'A4', layout: 'portrait' });
    const buffers = [];
    doc.on('data', buffers.push.bind(buffers));
    doc.on('end', () => {});
    doc.fontSize(12).text(plain, { lineGap: 4 });
    doc.end();
    doc.on('end', () => {
      const pdfBuffer = Buffer.concat(buffers);
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', 'attachment; filename="sales-activity-report-from-template.pdf"');
      res.send(pdfBuffer);
    });
  });
});

// Route: Display filled RTF report as HTML
app.get('/report/rtf/html', (req, res) => {
  fs.readFile(RTF_TEMPLATE_PATH, 'utf8', (err, template) => {
    if (err) {
      res.status(500).send('RTF template not found.');
      return;
    }
    const filled = fillRtfTemplate(template, staticData);
    // Simple RTF to HTML conversion for demo: replace \par with <br> and \tab with &emsp;
    let html = filled
      .replace(/\\par/g, '<br>')
      .replace(/\\tab/g, '&emsp;')
      .replace(/\{\\[^}]+\}/g, '') // remove fonttbl and other RTF groups
      .replace(/\\[a-z]+[0-9]*/g, '') // remove other RTF commands
      .replace(/\{\}|\}/g, '') // remove leftover braces
      .replace(/\n/g, '');
    res.send(`<!DOCTYPE html><html><head><meta charset='utf-8'><title>RTF Report Preview</title></head><body>${html}</body></html>`);
  });
});

// Basic home route
app.get('/', (req, res) => {
  res.send('<h2>Sales Activity Report Generator</h2><ul>' +
    '<li><a href="/report/pdf">Download PDF Report</a></li>' +
    '<li><a href="/report/xls">Download XLS Report</a></li>' +
    '<li><a href="/report/rtf">Download RTF Report (from template)</a></li>' +
    '<li><a href="/report/rtf/html">Preview RTF Report as HTML</a></li>' +
    '</ul>');
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
}); 