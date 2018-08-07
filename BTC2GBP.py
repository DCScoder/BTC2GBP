#################################################################################
#   Copyright © 2017 DCScoder
#
#                                    ~ BTC2GBP ~
#
#   Description:  BTC2GBP is a Bitcoin (BTC) to British Pound Sterling (GBP)
#                 currency converter. The script will process in bulk a .txt file
#                 containing 1 x BTC value on each line and output an .xlsx report.
#
#   Usage:        python BTC2GBP.py <InputFilePath> <OutputFilePath>
#
#################################################################################

import requests
import sys
import os
import time
import xlsxwriter

__version__ = 'v1.0'
__author__ = 'DCScoder'
__email__ = 'dcscoder@gmail.com'

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~ BTC2GBP " + __version__ + " developed by",__author__, "~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

print("Powered by CoinDesk\n")

source = sys.argv[1]
output_dir = sys.argv[2]

# Utilises Coindesk Bitcoin Price Index API to determine valuation of BTC
try:
    rate = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
    lutime = (rate['time']['updatedISO'])
    print("Currency Rates Last Updated:", lutime, "\n")
except:
    sys.exit("Error obtaining currency rates, ensure internet connection is active...")


def main():
    # Create .xlsx report and format
    workbook = xlsxwriter.Workbook(os.path.join(output_dir, "BTC2GBP" + time.strftime("-%d%m%Y-%H%M%S") + ".xlsx"))
    worksheet = workbook.add_worksheet("BTC2GBP")
    row = 2
    col1 = 1
    col2 = 2
    format1 = workbook.add_format()
    format1.set_font_size(18)
    format1.set_bold()
    format1.set_align('center')
    format2 = workbook.add_format()
    format2.set_align('center')
    worksheet.set_column('B:B', 20) + worksheet.set_column('C:C', 20)
    worksheet.write("B2", "BTC", format1) + worksheet.write("C2", "GBP", format1)

    # Process each BTC value and convert to GBP value
    data = open(source)
    total_lines = 0
    for each_value in data:
        total_lines += 1
        gbp_rate = (rate['bpi']['GBP']['rate_float']) * float(each_value)
        gbp_c = str(round(gbp_rate, 2))
        worksheet.write(row, col1, str(each_value), format2) + worksheet.write(row, col2, round(gbp_rate, 2), format2)
        row += 1

    workbook.close()

    print(total_lines, "BTC values processed.")

if __name__ == "__main__":
    main()