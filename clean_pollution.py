import pandas as pd
from difflib import get_close_matches

# load the england pollution CSV 
england = pd.read_csv("CSVs/popwmpm252023byEnglandregionanduppertierlocalauthority.csv", skiprows=2)
england.columns = ["Area Name", "PM2.5 Total", "PM2.5 Non-Anthropogenic", "PM2.5 Anthropogenic", "Region"]

# add england data to dictionary 
pollution_data = england.set_index("Region")["PM2.5 Total"].to_dict()

# add scotland data to dictionary 
scotland = pd.read_csv("CSVs/scotland_pm25.csv")
pollution_data.update(scotland.set_index("Region")['PM2.5'].to_dict())

# add wales data to dictionary
wales = pd.read_csv("CSVs/wales_pm25.csv")
pollution_data.update(wales.set_index("Region")["PM2.5"].to_dict())

# add northern ireland data to dictionary 
northern_ireland = pd.read_csv("CSVs/NI_pm25.csv")
pollution_data.update(northern_ireland.set_index("Region")["PM2.5"].to_dict())

# all 108 counties
county_list = [
    "Bedfordshire", "Berkshire", "Bristol", "Buckinghamshire", "Cambridgeshire", "Cheshire", "City of London",
    "Cornwall", "Cumbria", "Derbyshire", "Devon", "Dorset", "County Durham", "East Riding of Yorkshire",
    "East Sussex", "Essex", "Gloucestershire", "Greater London", "Greater Manchester", "Hampshire", "Herefordshire",
    "Hertfordshire", "Isle of Wight", "Kent", "Lancashire", "Leicestershire", "Lincolnshire", "Merseyside",
    "Norfolk", "Northamptonshire", "Northumberland", "North Yorkshire", "Nottinghamshire", "Oxfordshire",
    "Rutland", "Shropshire", "Somerset", "South Yorkshire", "Staffordshire", "Suffolk", "Surrey", "Tyne and Wear",
    "Warwickshire", "West Midlands", "West Sussex", "West Yorkshire", "Wiltshire", "Worcestershire",
    "Aberdeen City", "Aberdeenshire", "Angus", "Argyll and Bute", "Clackmannanshire", "Dumfries and Galloway",
    "Dundee City", "East Ayrshire", "East Dunbartonshire", "East Lothian", "East Renfrewshire",
    "Edinburgh (City of Edinburgh)", "Falkirk", "Fife", "Glasgow (City of Glasgow)", "Highland", "Inverclyde",
    "Midlothian", "Moray", "Na h-Eileanan Siar (Western Isles)", "North Ayrshire", "North Lanarkshire",
    "Orkney Islands", "Perth and Kinross", "Renfrewshire", "Scottish Borders", "Shetland Islands",
    "South Ayrshire", "South Lanarkshire", "Stirling", "West Dunbartonshire", "West Lothian",
    "Blaenau Gwent", "Bridgend", "Caerphilly", "Cardiff", "Carmarthenshire", "Ceredigion", "Conwy",
    "Denbighshire", "Flintshire", "Gwynedd", "Isle of Anglesey", "Merthyr Tydfil", "Monmouthshire",
    "Neath Port Talbot", "Newport", "Pembrokeshire", "Powys", "Rhondda Cynon Taf", "Swansea", "Torfaen",
    "Vale of Glamorgan", "Wrexham", "Antrim", "Armagh", "Down", "Fermanagh", "Londonderry", "Tyrone"
]

# map for counties missed due to city names etc used 
county_map = {
    "Bedfordshire": "Central Bedfordshire",
    "Berkshire": "West Berkshire",
    "Bristol": "Bristol, City of",
    "Cornwall": "Cornwall and Isles of Scilly",
    "Cumbria": "Carlisle",
    "Derbyshire": "Derby",
    "Devon": "Exeter",
    "Dorset": "Bournemouth",
    "County Durham": "Durham",
    "Gloucestershire": "Gloucester",
    "Greater London": "London",
    "Greater Manchester": "Manchester",
    "Herefordshire": "County of Herefordshire",
    "Merseyside": "Liverpool",
    "Northamptonshire": "Northampton",
    "Nottinghamshire": "Nottingham",
    "Shropshire": "Shrewsbury",
    "Somerset": "Taunton",
    "South Yorkshire": "Sheffield",
    "Staffordshire": "Stafford",
    "Tyne and Wear": "Newcastle upon Tyne",
    "West Midlands": "Birmingham",
    "West Yorkshire": "Leeds",
    "Wiltshire": "Salisbury",
    "Worcestershire": "Worcester",
    "Cheshire": "Cheshire West and Chester",
    "Glasgow (City of Glasgow)": "City of Glasgow",
    "Dundee City": "City of Dundee",
    "Edinburgh (City of Edinburgh)": "City of Edinburgh",
    "Aberdeen City": "City of Aberdeen"
}

# match counties to pollution data using map or similar names
output_rows = []
for county in county_list:
    value = pollution_data.get(county, "")
    if not value:
        city = county_map.get(county)
        if city:
            value = pollution_data.get(city)
            if value is None:
                match = get_close_matches(city, pollution_data.keys(), n=1, cutoff=0.8)
                value = pollution_data.get(match[0]) if match else ""
    output_rows.append((county, value))

# save final output
final_df = pd.DataFrame(output_rows, columns=["county_name", "pollution"])
final_df.to_csv("CSVs/clean_pollution.csv", index=False)
print("Cleaned pollution data saved")
