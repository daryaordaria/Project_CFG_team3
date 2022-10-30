# address = "Warsaw, Poland"
import re

def extract_data(address):
    address_list = address.split(",")
    city = address_list[0].strip()
    country = address_list[1].strip()
    return city, country
