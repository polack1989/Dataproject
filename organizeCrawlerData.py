import json
import os
import re
import math
import string

orig_Team_key = "OrigTeam"
player_Name_key = "playerName"
year_key = "year"
price_Status_key = "priceStatus" # this key will be remove
dest_Team_key = "DestTeam"
price_key = "price"
type_key = "type"
dest_country_key = "DestCountry"
orig_country_key = "OrigCountry"

start_year = 2007
number_of_seasons = 9

# array of tuples each tuple is : (int: year , string: json file path contains all transferd for this year)
all_years_files_path = []
[all_years_files_path.append((start_year+i, "Transfers_"+str(start_year+i)+"_"+str(start_year+i+1)+".json")) for i in range(number_of_seasons)]


data_dir_path = "crawlerData"


def add_price(transfer):
    price = transfer["priceStatus"]

    check_price = check_price_type(price)
    transfer[type_key] = check_price[0]
    transfer.pop("priceStatus")
    transfer[price_key] = check_price[1]

def check_price_type(price):
    price_amount = ""
    type = ""

    swap = "swap"
    trade = "trade"
    undisclosed = "undis"
    na = "n/a"
    fee = "fee"
    free = "Free"
    loan = "Loan"

    if price == loan:
        type = loan
        price_amount = None

    elif any(char.isdigit() for char in price):
        type = "Transfer"
        for char in price :
            if char.isdigit() or char == '.':
                price_amount += char
        if (price_amount.find(".") == -1) and (len(price_amount) > 3):
            price_amount = float(price_amount) / math.pow(10, 6)

        else:
            price_amount = float(price_amount)

    elif undisclosed in price or swap in price or trade in price or na in price or fee in price:
        type = "Transfer NA"
        price_amount = None

    elif price.find(free) != -1:
        type = "Free"
        price_amount = 0

    return [type, price_amount]




def get_all_crawler_transfer():
    for transfers_year_file_path in all_years_files_path:
        year, path = transfers_year_file_path
        with open(os.path.join(data_dir_path, path)) as file:
            all_transfer = json.load(file)
        for key in sorted(all_transfer):
            yield key, all_transfer[key], year

def add_player_name_and_year(key_transfer):
    player_name, transfer, year = key_transfer
    transfer["playerName"] = player_name
    transfer["year"] = year
    return transfer




def clean_string(transfer):
    keys_of_string_value = [orig_Team_key, dest_Team_key, player_Name_key]
    for string_value_key in keys_of_string_value:

        str_value = transfer[string_value_key].upper()

        for c in string.punctuation:
            str_value = str_value.replace(c, "")


        if(str_value[0] == " "):
            str_value = str_value[1:]

        if str_value[(len(str_value)-1)] == " ":
            str_value = str_value[:len(str_value)-1]

        #private cases
        if "Marcelo Filho" in str_value:
            if len(str_value) == 14:
                print "_"+str_value+"_"
                print(str_value[13]== " ")
                str_value = str_value[:len(str_value) - 1]
                print "_"+str_value+"_"

        if "Edin Dzeko" in str_value:
            if len(str_value) == 11:
                print "_"+str_value+"_"
                print(str_value[10] == " ")
                str_value = str_value[:len(str_value) - 1]
                print "_"+str_value+"_"

        transfer[string_value_key] = str_value


def add_country(transfer):
    transfer[orig_country_key] = None
    transfer[dest_country_key] = None



def create_full_clean_transports_json():
    transport_array = []
    for key_transfer in get_all_crawler_transfer():
        transfer = add_player_name_and_year(key_transfer)
        clean_string(transfer)
        add_price(transfer)
        add_country(transfer)
        transport_array.append(transfer)

    j = json.dumps(transport_array, indent=4)
    f = open('sample.json', 'w')
    print >> f, j
    f.close()
    return transport_array


def get_all_lists(transfer_array):
    players = set()
    teams = set()
    countries = set()
    for transfer in transfer_array:
        players.add(transfer[player_Name_key])
        teams.add(transfer[orig_Team_key])
        teams.add(transfer[dest_Team_key])

    print(len(transfer_array))
    print(len(players))
    print(len(teams))
    #
    # print(players)
    for team in sorted(teams):
         print team

    # for plaer in sorted(players):
    #     print plaer

if __name__ == "__main__":
    get_all_lists(create_full_clean_transports_json())