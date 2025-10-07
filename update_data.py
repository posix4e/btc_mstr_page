#!/usr/bin/env python3
"""
Update script for MSTR Bitcoin Holdings and mNAV data
Usage: python3 update_data.py /path/to/excel_file.xlsx

The Excel file should have columns for:
- Period (Year and Month)
- Average BTC Price
- MSTR BTC Holdings
- MSTR Holdings Value
- BTC Closing Price

And optionally for mNAV calculation:
- MSTR Market Cap
- MSTR Share Price
- Shares Outstanding
- Total Debt
- Other Assets
"""

import sys
import json
import pandas as pd

def convert_excel_to_json(excel_path):
    """Convert Excel file to JSON format for the website with optional mNAV data"""

    # Read and clean the Excel file
    df = pd.read_excel(excel_path, skiprows=3)

    # Handle different possible column configurations
    if len(df.columns) >= 5:
        # Basic columns
        df.columns = ['Period', 'Avg_BTC_Price', 'MSTR_BTC_Holdings', 'MSTR_Holdings_Value', 'BTC_Closing_Price'] + list(df.columns[5:])

    # Check if mNAV columns exist
    has_mnav_data = False
    if len(df.columns) >= 10:
        # Rename additional columns for mNAV if they exist
        column_mapping = {
            df.columns[5]: 'MSTR_Market_Cap',
            df.columns[6]: 'MSTR_Share_Price',
            df.columns[7]: 'Shares_Outstanding',
            df.columns[8]: 'Total_Debt',
            df.columns[9]: 'Other_Assets'
        }
        df.rename(columns=column_mapping, inplace=True)
        has_mnav_data = True

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
                entry = {
                    'year': int(current_year),
                    'month': month,
                    'avg_btc_price': float(row['Avg_BTC_Price']) if pd.notna(row['Avg_BTC_Price']) else 0,
                    'mstr_btc_holdings': float(row['MSTR_BTC_Holdings']) if pd.notna(row['MSTR_BTC_Holdings']) else 0,
                    'mstr_holdings_value': float(row['MSTR_Holdings_Value']) if pd.notna(row['MSTR_Holdings_Value']) else 0,
                    'btc_closing_price': float(row['BTC_Closing_Price']) if pd.notna(row['BTC_Closing_Price']) else 0
                }

                # Add mNAV fields (either from data or as placeholders)
                if has_mnav_data:
                    entry.update({
                        'mstr_market_cap': float(row['MSTR_Market_Cap']) if pd.notna(row.get('MSTR_Market_Cap', 0)) else 0,
                        'mstr_share_price': float(row['MSTR_Share_Price']) if pd.notna(row.get('MSTR_Share_Price', 0)) else 0,
                        'shares_outstanding': float(row['Shares_Outstanding']) if pd.notna(row.get('Shares_Outstanding', 0)) else 0,
                        'total_debt': float(row['Total_Debt']) if pd.notna(row.get('Total_Debt', 0)) else 0,
                        'other_assets': float(row['Other_Assets']) if pd.notna(row.get('Other_Assets', 0)) else 0
                    })
                else:
                    # Add placeholder fields
                    entry.update({
                        'mstr_market_cap': 0,
                        'mstr_share_price': 0,
                        'shares_outstanding': 0,
                        'total_debt': 0,
                        'other_assets': 0
                    })

                data.append(entry)

    # Sort by year and month
    data.sort(key=lambda x: (x['year'], x['month']))

    return data, has_mnav_data

def calculate_mnav(btc_holdings_value, other_assets, total_debt, shares_outstanding):
    """Calculate mNAV per share"""
    if shares_outstanding == 0:
        return 0
    return (btc_holdings_value + other_assets - total_debt) / shares_outstanding

def calculate_premium_discount(share_price, mnav):
    """Calculate premium/discount percentage"""
    if mnav == 0:
        return 0
    return ((share_price - mnav) / mnav) * 100

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 update_data.py /path/to/excel_file.xlsx")
        print("\nExpected Excel columns:")
        print("1-5: Period, Avg BTC Price, MSTR BTC Holdings, Holdings Value, BTC Closing Price")
        print("6-10 (optional): Market Cap, Share Price, Shares Outstanding, Total Debt, Other Assets")
        sys.exit(1)

    excel_path = sys.argv[1]

    try:
        # Convert Excel to JSON
        data, has_mnav = convert_excel_to_json(excel_path)

        # Save to data.json
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Successfully updated data.json with {len(data)} monthly data points")

        # Show latest data point
        if data:
            latest = data[-1]
            print(f"\n📊 Latest data: {latest['year']}/{latest['month']:02d}")
            print(f"   BTC Holdings: {latest['mstr_btc_holdings']:,.0f} BTC")
            print(f"   Holdings Value: ${latest['mstr_holdings_value']/1e9:.2f}B")
            print(f"   BTC Price: ${latest['btc_closing_price']:,.0f}")

            # Show mNAV metrics if available
            if has_mnav and latest['shares_outstanding'] > 0:
                mnav = calculate_mnav(
                    latest['mstr_holdings_value'],
                    latest['other_assets'],
                    latest['total_debt'],
                    latest['shares_outstanding']
                )
                premium = calculate_premium_discount(latest['mstr_share_price'], mnav)

                print(f"\n💹 mNAV Metrics:")
                print(f"   MSTR Share Price: ${latest['mstr_share_price']:,.2f}")
                print(f"   mNAV per Share: ${mnav:,.2f}")
                print(f"   Premium/Discount: {premium:+.1f}%")
                print(f"   Market Cap: ${latest['mstr_market_cap']/1e9:.2f}B")
            elif not has_mnav:
                print("\n⚠️  No mNAV data found. Add columns 6-10 to Excel for mNAV calculations:")
                print("   - Column 6: MSTR Market Cap")
                print("   - Column 7: MSTR Share Price")
                print("   - Column 8: Shares Outstanding")
                print("   - Column 9: Total Debt")
                print("   - Column 10: Other Assets")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()