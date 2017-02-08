import xlsxwriter
from organizeCrawlerData import *

transport_array = create_full_clean_transports_json()

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('try.xlsx')

def create_transaction_table():
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Player Name', bold)
    worksheet.write('B1', 'Year', bold)
    worksheet.write('C1', 'Original Team', bold)
    worksheet.write('D1', 'Original Country', bold)
    worksheet.write('E1', 'Destination Team', bold)
    worksheet.write('F1', 'Destination Country', bold)
    worksheet.write('G1', 'Transaction Type', bold)
    worksheet.write('H1', 'Price', bold)

    transport_keys_sort_bt_col = [player_Name_key,
                                  year_key,
                                  orig_Team_key,
                                  orig_country_key,
                                  dest_Team_key,
                                  dest_country_key,
                                  type_key,
                                  price_key]
    row = 1
    for transport in transport_array:
        for col in range(len(transport_keys_sort_bt_col)):
            worksheet.write(row, col, transport[transport_keys_sort_bt_col[col]])
        row += 1

if __name__ == "__main__":
    create_transaction_table()
    workbook.close()