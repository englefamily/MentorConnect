




# Code to return list  of Cities in a Country
# Also found this: https://github.com/Moshe0027/israel-cities-1 which can be useful

# import geonamescache
#
# # Initialize a GeonamesCache object
# gc = geonamescache.GeonamesCache()
#
# # Get a list of all cities
# cities = gc.get_cities()
#
# # Find the desired country code based on the country name
# country_name = "Israel"
# country_code = [code for code, data in gc.get_countries().items() if data['name'] == country_name][0]
#
# # Filter the list of cities based on the desired country code
# cities_in_country = [data for data in cities.values() if data['countrycode'] == country_code]
#
# # Print the list of cities for the specified country
# for city_data in cities_in_country:
#     print(city_data['name'])

# # In this version tried to get the names converted to Hebrew:
#
# import geonamescache
# import pycountry
#
# # Initialize a GeonamesCache object
# gc = geonamescache.GeonamesCache()
#
# # Get a list of all cities and countries
# cities = gc.get_cities()
# countries = gc.get_countries()
#
# # Find the desired country code based on the country name
# country_name = "Israel"
# country_code = [code for code, data in countries.items() if data['name'] == country_name][0]
#
# # Define the language code for Hebrew
# language_code = "he"
#
# # Filter the list of cities for the country code
# cities_in_country = [data for data in cities.values() if data['countrycode'] == country_code]
#
# def get_city_name_in_language(city_data, language_code):
#     if 'alternateNames' in city_data:
#         for alternate_name in city_data['alternateNames']:
#             if alternate_name['lang'].lower() == language_code.lower():
#                 return alternate_name['name']
#     return city_data['name']
#
# # Print the list of cities in Hebrew for Israel
# for city_data in cities_in_country:
#     city_name_in_language = get_city_name_in_language(city_data, language_code)
#     print(city_name_in_language)