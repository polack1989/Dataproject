"""
createXls
this module creates an Xls file named project_data.xls which contains tables of the data.
"""
import xlsxwriter
from organizeCrawlerData import create_full_clean_transports_json
from const import *


def get_all_lists(transfer_array):
    '''
    @param transfer_array:
    iterates all transfers and creates sets of: players names, teams name, countries
    @return: tuple of three values
    set of all players name,
    set of all teams name,
    set of all countries
    '''
    players = set()
    teams = set()
    countries = set()
    for transfer in transfer_array:
        players.add(transfer[player_Name_key])
        if transfer[orig_Team_key] in teams_dic.keys():
            teams.add(transfer[orig_Team_key])
        if transfer[dest_Team_key] in teams_dic.keys():
            teams.add(transfer[dest_Team_key])
        countries.add(transfer[orig_country_key])
        countries.add(transfer[dest_country_key])
    return players, teams, countries


def create_transaction_table():
    '''
    create an xls shit contains a single table,
    a record in the table represent a single transfer.
    '''
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

    transport_keys_sort_by_col = [player_Name_key,
                                  year_key,
                                  orig_Team_key,
                                  orig_country_key,
                                  dest_Team_key,
                                  dest_country_key,
                                  type_key,
                                  price_key]
    row = 1
    for transport in transport_array:
        for col in range(len(transport_keys_sort_by_col)):
            worksheet.write(row, col, transport[transport_keys_sort_by_col[col]])
        row += 1


def create_all_separates_tables():
    '''
    create an xls shit contains 3 tables,
    players name table,
    teams table (each record is team name, team country),
    countries table.
    '''
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'All Players', bold)

    worksheet.write('C1', 'Team', bold)
    worksheet.write('D1', 'Country', bold)

    worksheet.write('F1', 'All Countries', bold)

    players, teams, countries = get_all_lists(transport_array)

    row = 1
    for player in sorted(players):
        worksheet.write(row, 0, player)
        row += 1

    row = 1
    for team in sorted(teams):
        worksheet.write(row, 2, team)
        worksheet.write(row, 3, teams_dic[team][1])
        row += 1

    row = 1
    for country in sorted(countries):
        worksheet.write(row, 5, country)
        row += 1



if __name__ == "__main__":
    transport_array = create_full_clean_transports_json()
    workbook = xlsxwriter.Workbook('project_data.xlsx')
    create_transaction_table()
    create_all_separates_tables()
    workbook.close()