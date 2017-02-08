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
number_of_seasons = 10

# array of tuples each tuple is : (int: year , string: json file path contains all transferd for this year)
all_years_files_path = []
[all_years_files_path.append((start_year+i, "Transfers_"+str(start_year+i)+"_"+str(start_year+i+1)+".json")) for i in range(number_of_seasons)]
for y in all_years_files_path:
    print y

data_dir_path = "crawlerData"