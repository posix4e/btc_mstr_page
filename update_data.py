#!/usr/bin/env python3
"""
Update script for MSTR Bitcoin Holdings data
Usage: python3 update_data.py /path/to/excel_file.xlsx
"""

import sys
import json
import pandas as pd

def convert_excel_to_json(excel_path):
    """Convert Excel file to JSON format for the website"""

    # Read and clean the Excel file
    df = pd.read_excel(excel_path, skiprows=3)
    df.columns = ['Period', 'Avg_BTC_Price', 'MSTR_BTC_Holdings', 'MSTR_Holdings_Value', 'BTC_Closing_Price']

    # Filter out summary rows
    df = df[~df['Period'].astype(str).str.contains('Grand Total|Row Labels', na=False)]

    # Parse year and month data
    data = []
    current_year = ''

    for _, row in df.iterrows():
        period = str(row['Period'])

        # Check if it's a year row
        if period.replace('.', '').isdigit() and len(period) == 4:
            current_year = period
        # Otherwise it's a month
        elif period.replace('.', '').isdigit() and current_year:
            month = int(float(period))
            # Skip year summary rows
            if month <= 12:
                data.append({
                    'year': int(current_year),
                    'month': month,
                    'avg_btc_price': float(row['Avg_BTC_Price']) if pd.notna(row['Avg_BTC_Price']) else 0,
                    'mstr_btc_holdings': float(row['MSTR_BTC_Holdings']) if pd.notna(row['MSTR_BTC_Holdings']) else 0,
                    'mstr_holdings_value': float(row['MSTR_Holdings_Value']) if pd.notna(row['MSTR_Holdings_Value']) else 0,
                    'btc_closing_price': float(row['BTC_Closing_Price']) if pd.notna(row['BTC_Closing_Price']) else 0
                })

    # Sort by year and month
    data.sort(key=lambda x: (x['year'], x['month']))

    return data

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 update_data.py /path/to/excel_file.xlsx")
        sys.exit(1)

    excel_path = sys.argv[1]

    try:
        # Convert Excel to JSON
        data = convert_excel_to_json(excel_path)

        # Save to data.json
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Successfully updated data.json with {len(data)} monthly data points")

        # Show latest data point
        if data:
            latest = data[-1]
            print(f"📊 Latest data: {latest['year']}/{latest['month']:02d}")
            print(f"   BTC Holdings: {latest['mstr_btc_holdings']:,.0f} BTC")
            print(f"   Holdings Value: ${latest['mstr_holdings_value']/1e9:.2f}B")
            print(f"   BTC Price: ${latest['btc_closing_price']:,.0f}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()