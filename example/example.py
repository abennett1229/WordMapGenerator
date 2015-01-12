from GetWordMap import get_region_word_clouds,get_word_map

#Define map country
my_country = 'US'

#Define map colors
hex_code_list = ["B8DB70","FF9494","A3E0E0","E066E0","A3E085","85E0FF","FFA366","FFE066","FF85C2","C2A3E0","FFC2E0","A3FFE0","4DB894","7094FF","B280B2","E06685","372AFF"]

#Define map regions
if my_country == "US":
	region_list = [ "AL","AZ","AR","CA","CO","CT","DE","DC","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
if my_country == "GB":
	region_list = ["east-england","east-midlands","london","north-east","north-west","northern-ireland","scotland","south-east","south-west","wales","west-midlands","yorkshire-and-humber"]
if my_country == "LATAM":
    region_list = ["AR","BO","BR","CL","CO","CR","DO","EC","SV","GT","HN","MX","NI","PA","PY","PE","UY","VE","PR"]

get_region_word_clouds(my_country,region_list,hex_code_list)
get_word_map(my_country,region_list)
