import requests
import json
import pandas as pd
import os
from pathlib import Path
import time
import random

def main():
    # Set the file location and filename to save files
    filelocation = str(Path(__file__).parent.parent) + "/azurePricing/"
    filename = 'azurePrices'

    # Call the Azure Retail Prices API
    base_url = "https://prices.azure.com/api/retail/prices"
    #url_filters = "?$filter= armRegionName eq 'southcentralus' and serviceName eq 'Virtual Machines'" #filtered results are possible too
    url_filters = ""
    request_url = base_url + url_filters
    response = requests.get(request_url)

    # Create an array to store price list
    priceitems= []

    # Add the retail prices returned in the API response to a list
    for i in response.json()['Items']:
        priceitems.append(i)

    print(response.json()["NextPageLink"])

    # Retrieve price list from all available pages until there is a 'NextPageLink' available to retrieve prices
    while response.json()["NextPageLink"] != None:
        for i in response.json()['Items']:
            priceitems.append(i)
        response = requests.get(response.json()["NextPageLink"])
        print(response.json()["NextPageLink"])
        #time.sleep(random.randint(2,7)) #slow down API calls

    # Retrieve price list from the last page when there is no "NextPageLink" available to retrieve prices
    if response.json()["NextPageLink"] == None:
        for i in response.json()['Items']:
            priceitems.append(i)

    # Write the price list to a json file
    with open(os.path.join(filelocation,filename) + '.json', 'w') as f:
        json.dump(priceitems, f)

    # Open the price list json file and load into a variable
    with open(os.path.join(filelocation,filename) + '.json', encoding='utf-8') as f:
        raw = json.loads(f.read())

    # Convert the price list into a data frame
    df = pd.json_normalize(raw)

    ## Save the data frame as an excel file
    #df.to_excel(os.path.join(filelocation,filename) + '.xlsx', sheet_name='RetailPrices', index=False)

    # Save the data frame as a CSV file
    df.to_csv(os.path.join(filelocation,filename) + '.csv', index=False)

if __name__ == "__main__":
    main()
