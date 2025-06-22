# Sales Activity Report Generator

## Project Overview
This is an Express.js web application that generates a weekly sales activity report using static data. The report can be exported in PDF and XLS formats.

## Features
- Express.js backend
- Static data modeling (matching screenshot fields)
- PDF generation (using pdfkit)
- XLS generation (using exceljs)
- API endpoints for triggering report generation and download

## Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the server:
   ```bash
   node index.js
   ```
3. Open your browser and go to [http://localhost:3000](http://localhost:3000)

## API Endpoints
- `/report/pdf` - Download the weekly sales activity report as a PDF file
- `/report/xls` - Download the weekly sales activity report as an XLSX file

## Project Structure
- `index.js` - Main server file
- `package.json` - Project metadata and dependencies

## Libraries Used
- [express](https://www.npmjs.com/package/express)
- [pdfkit](https://www.npmjs.com/package/pdfkit)
- [exceljs](https://www.npmjs.com/package/exceljs)

## Future Improvements
- Integrate with dynamic data sources
- Add user authentication
- Enhance report layout and formatting
- Add frontend UI for custom report generation 