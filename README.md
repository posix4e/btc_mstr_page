# MSTR Bitcoin Holdings Rainbow Chart 🌈

Interactive visualization of MicroStrategy's Bitcoin holdings over time with rainbow gradient charts.

## 🚀 Live Demo

Visit: `https://[your-username].github.io/btc_mstr_page/`

## 📊 Features

- **Rainbow Gradient Charts**: Beautiful gradient visualizations that change colors across the timeline
- **Dual Axis Display**: Shows both BTC holdings quantity and USD value
- **Bitcoin Price Tracking**: Displays BTC price movements alongside holdings
- **Real-time Statistics**: Key metrics including total holdings, value, and growth percentage
- **Responsive Design**: Works on desktop and mobile devices

## 🔄 Updating the Data

### Method 1: Using the Update Script

1. Install required Python packages:
   ```bash
   pip install pandas openpyxl
   ```

2. Run the update script with your Excel file:
   ```bash
   python3 update_data.py /path/to/BTC_MSTR.xlsx
   ```

### Method 2: Manual Update

Edit `data.json` directly with the following format:

```json
{
  "year": 2025,
  "month": 10,
  "avg_btc_price": 100000.0,
  "mstr_btc_holdings": 650000.0,
  "mstr_holdings_value": 65000000000.0,
  "btc_closing_price": 100000.0
}
```

## 🚀 Deployment to GitHub Pages

1. Create a new GitHub repository

2. Push the code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/[your-username]/btc_mstr_page.git
   git push -u origin main
   ```

3. Enable GitHub Pages:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)
   - Save

4. Your site will be available at: `https://[your-username].github.io/btc_mstr_page/`

## 📁 Project Structure

```
btc_mstr_page/
├── index.html          # Main webpage with charts
├── data.json          # Data file (easily editable)
├── update_data.py     # Script to convert Excel to JSON
└── README.md         # This file
```

## 📈 Data Source

Data tracks MicroStrategy's Bitcoin accumulation strategy including:
- Monthly average BTC prices
- MSTR's total BTC holdings
- USD value of holdings
- BTC closing prices

## 🎨 Customization

The rainbow gradient can be customized in `index.html` by modifying the `createRainbowGradient` function colors:

```javascript
gradient.addColorStop(0, '#FF6B6B');     // Red
gradient.addColorStop(0.17, '#FFB56B');  // Orange
gradient.addColorStop(0.33, '#FFEB6B');  // Yellow
gradient.addColorStop(0.5, '#95E77E');   // Green
gradient.addColorStop(0.67, '#6BDFFF');  // Light Blue
gradient.addColorStop(0.83, '#6B8BFF');  // Blue
gradient.addColorStop(1, '#B56BFF');     // Purple
```

## 📝 License

MIT License - Feel free to use and modify as needed!