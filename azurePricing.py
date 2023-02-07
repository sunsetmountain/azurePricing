# Azure pricing overview - https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices


import requests
import json
import pandas as pd
import os
from pathlib import Path
import time
from datetime import datetime
import random

def main():
    startTime = datetime.today()
    print(f"Started at: {startTime}")

    num_skus = readPricingFile()

    print(f"Number of SKUs: {num_skus}")

    stopTime = datetime.today()

    print(f"Finished at: {stopTime}")
    print(f"Processing time: {stopTime - startTime}")

def readPricingFile():
    # Call the Azure Retail Prices API
    #response = requests.get("https://prices.azure.com/api/retail/prices?$filter= armRegionName eq 'southcentralus' and serviceName eq 'Virtual Machines'")
    response = requests.get("https://prices.azure.com/api/retail/prices")


    # Set your file location and filename to save your json and excel file
    filelocation = str(Path(__file__).parent) + "/"
    filename = 'azurePrices'

    # Create an array to store price list
    priceitems= []

    #Add the retail prices returned in the API response to a list
    for i in response.json()['Items']:
        priceitems.append(i)

    print(response.json()["NextPageLink"])

    # Retrieve price list from all available pages until there is a 'NextPageLink' available to retrieve prices
    while response.json()["NextPageLink"] != None:
        for i in response.json()['Items']:
            priceitems.append(i)
        response = requests.get(response.json()["NextPageLink"])
        print(response.json()["NextPageLink"])
        time.sleep(random.randint(2,7))

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
    #df.to_excel(os.path.join(filelocation,filename) + '.xlsx', sheet_name='azurePrices', index=False)

    # Save the data frame as a CSV file
    df.to_csv(os.path.join(filelocation,filename) + '.csv', index=False)

    return len(df.index)

if __name__ == "__main__":
    main()
