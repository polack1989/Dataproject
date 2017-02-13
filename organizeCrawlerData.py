"""
This module provides tool to organize the data downloaded by the crawler.
the function create_full_clean_transports_json reads the jsons downloaded
by the crawler organized them and save the data in a pickle file named transferDataArray.p
"""
import json
import os
import cPickle as pickle
import math
import string
from const import *


def add_price(transfer):
    '''
    @param transfer: a dictionary represent a single transfer
    add to the dictionary transfer Type and transfer price (int)
    removes from the dictionary priceStatus
    '''
    price = transfer[price_Status_key]
    check_price = check_price_type(price)
    transfer[type_key] = check_price[0]
    transfer.pop("priceStatus")
    transfer[price_key] = check_price[1]


def check_price_type(price):
    '''
    @param price: string
    the transfer price (downloaded from the crawler) is a string , each price can be one of several formats.
    this function convert each price string to a number in Millions of Euros.
    @return: the type of the transaction, and the price as int in Millions of Euros.
    '''
    price_amount = ""
    type = ""

    if price == loan:
        type = loan
        price_amount = None

    elif undisclosed in price or swap in price or trade in price or na in price or fee in price:
        type = "Transfer NA"
        price_amount = None

    elif any(char.isdigit() for char in price):
        type = "Transfer"

        # in case there is extra data on the transfer in price status
        if "(" in price:
            price = price.split('(')[0]

        for char in price:
            if char.isdigit() or char == '.':
                price_amount += char

        if (price_amount.find(".") == -1) and (len(price_amount) > 3):
            price_amount = float(price_amount) / math.pow(10, 6)

        else:
            price_amount = float(price_amount)


    elif price.find(free) != -1:
        type = "Free"
        price_amount = 0

    return [type, price_amount]


def get_all_crawler_transfer():
    '''
    this function iterates all the json files downloaded by the crawler
    @return: it yields
    key - which is the player name for the current transfer json
    the current transfer json data
    and the year of the transfer
    '''
    for transfers_year_file_path in all_years_files_path:
        year, path = transfers_year_file_path
        with open(os.path.join(data_dir_path, path)) as file:
            all_transfer = json.load(file)
        for key in sorted(all_transfer):
            yield key, all_transfer[key], year


def add_player_name_and_year(transfer_tuple):
    '''
    @param transfer_tuple:  player_name, transfer, year
    @return: transfer dictionary
    '''
    player_name, transfer, year = transfer_tuple
    transfer["playerName"] = player_name
    transfer["year"] = year
    return transfer


def clean_string(transfer):
    '''
    @param transfer: a dictionary represent single transfer
    turn string to upper case, removes redundant character
    '''
    keys_of_string_value = [orig_Team_key, dest_Team_key, player_Name_key]
    for string_value_key in keys_of_string_value:

        str_value = transfer[string_value_key].upper()

        for c in string.punctuation:
            str_value = str_value.replace(c, "")


        if(str_value[0] == " "):
            str_value = str_value[1:]

        if str_value[(len(str_value)-1)] == " ":
            str_value = str_value[:len(str_value)-1]

        transfer[string_value_key] = str_value



def add_country_and_update_teams(transfer):
    '''
    @param transfer: a dictionary represent single transfer
    this function add to the transfer orig_country, dest_country
    and change the dest and orig team string to the unique team name
    as defined in the const page.
    '''
    transfer[orig_country_key] = teams_dic[transfer[orig_Team_key]][1]
    transfer[orig_Team_key] = teams_dic[transfer[orig_Team_key]][0]
    transfer[dest_country_key] = teams_dic[transfer[dest_Team_key]][1]
    transfer[dest_Team_key] = teams_dic[transfer[dest_Team_key]][0]



def create_full_clean_transports_json():
    '''
    create_full_clean_transports_json -
    organize json: adds year, player name field, cleans strings value, adds teams country info
    save all new organized data in a pickle named transferDataArray.p
    @return:
    '''
    transport_array = []
    for transfer_tuple in get_all_crawler_transfer():
        transfer = add_player_name_and_year(transfer_tuple)
        clean_string(transfer)
        add_price(transfer)
        add_country_and_update_teams(transfer)
        transport_array.append(transfer)

    # j = json.dumps(transport_array, indent=4)
    # f = open('sample.json', 'w')
    # print >> f, j
    # f.close()
    pickle.dump(transport_array, open("transferDataArray.p", "wb"))
    return transport_array

