#__________________________________________________________________________________________________________________________________________________________________________

## Method 1. Traditional Scraping: Example with Yahoo Finance API

#__________________________________________________________________________________________________________________________________________________________________________

# Step 1: imports
from requests import get
from bs4 import BeautifulSoup
import os
import requests
import json
from typing import Dict, List, Optional, Union, cast
import time
import pandas as pd
from datetime import date

# Step 2: Create the pbjects to use later on:

url = 'https://finance.yahoo.com/'
endpoints = ['quote/ABNB?p=ABNB', 'quote/TSLA?p=TSLA', 'quote/CRWD?p=CRWD', 'quote/PANW?p=PANW', 'quote/CRM?p=CRM']
# b. headers may or may not be required
headers = {'User-Agent': 'Codeup Data Science'}

# Step 3: bits and pieces test:
# a. set out the basic elements for the scraper to access
baseUrl = 'https://finance.yahoo.com/'
# b. add in the endpoints for the various stocks you want to check
endpoint = 'quote/ABNB?p=ABNB'
actual = 'https://finance.yahoo.com/quote/ABNB?p=ABNB'
# c. headers will be generic unless a custom is key is required for the yfinance API
#headers = {'User-Agent': 'Codeup Data Science'}
url = f'{baseUrl}{endpoint}'
response = get(url)
# d. create the scraper
soup = BeautifulSoup(response.text, 'html.parser')
# e. test the response
response.text[:50]

# Step 3: Now the tricky part...may need to use attributes or other Soup item types

# BS4 custom tags
# used an atttribute to tell BS that we want to use for ID
# beatiful soup custom tags for more info
# Selenium for site interaction, but can be a little slow
# read in the old CSV, then add in the new, then overwrite
openingPrice = soup.find(attrs = {"data-test":"OPEN-value"}).text
ticker = soup.find(class_="D(ib) Fz(18px)").text
dailyRange = soup.find(attrs = {"data-test":"DAYS_RANGE-value"}).text
closingPrice = soup.find(attrs = {"data-test":"qsp-price", "data-field":"regularMarketPrice"}).text
openingPrice, ticker, dailyRange, closingPrice

# Step 4: Wrap it all up in a fucntion:

# I want date, open, high, close, stock name
def get_prices():
    # set out the basic elements for the scraper to access
    baseUrl = 'https://finance.yahoo.com/'
    # add in the endpoints for the various stocks you want to check
    endpoints = ['quote/ABNB?p=ABNB', 'quote/TSLA?p=TSLA', 'quote/CRWD?p=CRWD', 'quote/PANW?p=PANW', 'quote/CRM?p=CRM']
    # headers will be generic unless a custom is key is required for the yfinance API
    headers = {'User-Agent': 'Codeup Data Science'}

    #create an empty list to store the dictionary of daily values
    dailyOverview = []

    # make a for loop to iterate through the URL and endpoints
    for endpoint in endpoints:
        url = f'{baseUrl}{endpoint}'
        headers = {'User-Agent': 'Codeup Data Science'}
        while True:
            response = get(url, headers=headers)
            if response.ok:
                break
            else:
                time.sleep(15)

        # create the scraper
        soup = BeautifulSoup(response.text, 'html.parser')

        # list the variables to scrape

        day = date.today()

        ticker = soup.find(class_="D(ib) Fz(18px)").text

        openingPrice = soup.find(attrs = {"data-test":"OPEN-value"}).text

        dailyRange = soup.find(attrs = {"data-test":"DAYS_RANGE-value"}).text

        closingPrice = soup.find(attrs = {"data-test":"qsp-price", "data-field":"regularMarketPrice"}).text

        # create a dictionary to store the variables
        all_prices = {'Day': day,
            'Stock': ticker,
            'Open': openingPrice,
            'Range': dailyRange,
           'Close': closingPrice}

        # add a check statement to display the progress
        print(f'\rFetching page {endpoint}', end='')

        # append the iterated stock dictionary to the master list
        dailyOverview.append(all_prices)

    # convert the list to a DataFrame
    dailyOverview = pd.DataFrame(dailyOverview)

    # return the DataFrame
    return dailyOverview

#__________________________________________________________________________________________________________________________________________________________________________

## Method 2. Scraping made quick, with multi-page sources:

#__________________________________________________________________________________________________________________________________________________________________________

### Always Check for the Hidden API When Web Scraping - Youtube Video by John Watson Rooney

### Using REI's site as an example, under section camp electronics

# 1. navigate to site, inspect page elements
# 2. in the inspect page elements box, click the network tab in the toolbar at top, and check the box for 'Fetch/XHR' to retrieve the full web request
# 3. navigate to the bottom of the target page, click on 'more' or 'page 2', which will generate more search results
# 4. select the request that contains all of the web page info (page size/items). This result is the body of the scrpaing file we will build.
# 5. Copy the appropriate result with a right click "copy cURL"
# 6. Paste into Insomnia (API tool), and attempt to edit the item counts per page, to reduce aggregate page requests during scraping.
# 7. Once complete with parameter adjustment, click the drop down arrow to the right of the GET request, select 'generate code'
# 8. Select 'Python', copy to clipboard, paste in IDE
# 9. Note: common issues with generated dict:
#     a. quotes: 2x double quotes. fix by replacing the outer double quotes with single quotes
#     b. clean up the code by removing the empty payload varaible, then from the response variable equation

##REI v3

import requests
import pandas as pd
import time


def scrapeREIv3(n):

    url = "https://www.rei.com/c/climbing"

    results = []

    for x in range(1, n):


        start = time.time() # gives time now, of execution

        querystring = {"json":"true","page":f"{x}"}


        headers = {
            "cookie": "akamai_session=23.52.43.86.70651662741090785; EdgeLocation=29.4697,-98.5294; akacd_RWASP-default-phased-release=3840193891~rv=80~id=941d429870c021c9033359324d9773d7; check=true; AMCVS_F0A65E09512D2C440A490D4D%40AdobeOrg=1; REI_DEVICE_ID=fd1d0f997da4885f1d275d8a20cbb01c|8f1cf5e0faeec48e3dd528b1e5231521ce2a9219f7a40598e8a910f3557d3a60; crl8.fpcuid=9bfce551-4b69-460d-90fe-597d603a6cdd; s_ecid=MCMID%7C55821625543482899773563706189799122325; qualtricsSwimlaneCookie=32; s_cc=true; _gcl_au=1.1.902870909.1662741095; _caid=fbf485f2-5979-4f9e-94ce-5667d0358698; _mibhv=anon-1653182539798-780448828_5274; _scid=8b3c9aa1-5ca6-4797-aa0e-14786fdac9ca; AAM=AAM%3D17802662%2C17811395; aam_uuid=55574878270270512063540718926528616682; BVBRANDID=690d975f-34b0-4e5e-a4e3-dc4e889fbcbc; sessionPageViews=2; emailAcqModalSeen=true; QSI_SI_6Ll4zMEOB0C74vs_intercept=true; m_pages=30; AWSALB=nZwvAaQ5s/hKxES7HiZzMH45gSuQpx7b+TwIesO2JyVojtlF+mKyFHc3j2iu4GBXrHKNQ2WWM3yzIaI3sFLWxupojD9s7lV+jFXGKpgm6b7LsS+NfT1pzhzV6NvO; AWSALBCORS=nZwvAaQ5s/hKxES7HiZzMH45gSuQpx7b+TwIesO2JyVojtlF+mKyFHc3j2iu4GBXrHKNQ2WWM3yzIaI3sFLWxupojD9s7lV+jFXGKpgm6b7LsS+NfT1pzhzV6NvO; bm_sz=C937791453F2F41A8FD852BA988051DC~YAAQLDovFxfyCCKDAQAAvKFQJBE37hr0ITriSECzyJhp/ftHZfy2QTHY/GW3Ta6O+KiqyVskgcVug1O/tsCKCjdOX0izGTyYpnbTkXOTJ6VUJVeiP+Y3DmP+jit3cARWyjfyHTsRjoYPAoWkv4KtvvHoumy+WFIrbXPr5lBBQKtELzOJnNwycZEOHgX+k4pDSpmLaDETHH4TQ0lCrZTNP8E57Ebo+cZYOGII5F6kbu6ehAgJ+bM0trIC5xt9kpB1cL1QCCAX3iMIvHUbPMcZTs3FyBXfbHPsRrHVjf+uhhg=~3683649~3748674; ak_bmsc=CD11438E72B95A3F42C153F81D60CB59~000000000000000000000000000000~YAAQGmzNF0hYgR+DAQAA0KtQJBGO9+EoWMJjutdfVkqYfhrARrvK9jtjKphmJZmM9Cej6kMSNDcnrUw2u7QX4yoRrbJyl9y2nONHnJKmF4OdFgB27l7Q7UKMofCDhSgMUMi6nAkXrpD4AW1muHHf1w8ZMhNvIx+UmEfqKG1/lCiGIRMBD+nx5iUzYJgRhaYO+uP7NbIjAJ9dQ467j8+ynykBU/JcG5oxsSFhGB1fbG40FBG7DcjuA4SB0gfWEqzp2xDbvfePB/EYLtYmkvNFSj3iYhs0gfQszrRvgZdFIULDOirNeYr6lCq7eAGOYlGcUukl4UWauwYvnuki3nMd/Qcvon+/5R69lngZrjkBuMX3kyvq7EjvMJTLFzD5IjZYGss4xRgsZJ0FZoabCcTXQWB+3SRm17nmCSEA5Flu5Z1U2615zSF9Gf3ybWVYFUBHGAiDonzf+QUuePcdZpXWQO8O9nmtT1+lbQEDxZBF5yY+vrJDXdQCyQ==; AMCV_F0A65E09512D2C440A490D4D%40AdobeOrg=1585540135%7CMCIDTS%7C19245%7CMCMID%7C55821625543482899773563706189799122325%7CMCAAMLH-1663366410%7C9%7CMCAAMB-1663366410%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1662768810s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0%7CMCCIDH%7C1508253309; mboxEdgeCluster=35; _abck=A0E62878B22673980A5584D96EA26BC9~0~YAAQGmzNF3tYgR+DAQAAF6xQJAjMUC/1CGF7hJ3Jh12xfDQHkmaJ+Jt2XSjnYx3flhfb8eb8Pkw00iVErOiw6me08d7w3G7OO+7ZIStg+U985vV3V17Hd3svILqlkUArcZnrn+Eir1fQ+0DijrWUP4pPV2sYuPb+ydNgu6VsXe9w0D24lr24Bg2Ws66RSTUVhg7tkNZ1FKkNpzy+MLJaqoOQkgsbKRp/m7se5Hi+v2GUxb5Z/QleXE9R5Rz967bwCsFhqJEYuFaMOCw4jxfEIyrElKTdANKihyWGuQy57HPI1A/AZJr2uZX2kjKQmpXWztan8HdLX1xnmTtFWId4BBxmsybYBsiJuePAzuXDEds/KhPjbO6OQLDh5nd6CYUzTOd1xe0CPBpafyWDD9TsgTrM~-1~-1~1662765196; s_vnum=1820421094297%26vn%3D4; s_invisit=true; rr_rcs=eF5jYSlN9rAwMEhNMzM00TVJMTLWNTFISdRNtjQ11jVPNDNItkg2TTVPTuPKLSvJTBEwNDQ31jXUNQQAk0QOYQ; _cavisit=1832450b3ed|; akaas_CategoryHubCategoryTest=1667945627~rv=85~id=541438077a40a645455cd29b27be3db3~rn=; mbox=PC#04ef44a6e310423580a32637bed70cf4.35_0#1726006434|session#e05c6449c84a4704b9d719893a77a00a#1662763470; searchURL=/c/climbing; s_nr=1662761637852-Repeat; mp_rei_us_mixpanel=%7B%22distinct_id%22%3A%20%22180e95ba7b720-0429f33168a454-34736704-1aeaa0-180e95ba7b813ea%22%2C%22bc_persist_updated%22%3A%201662741094706%7D; s_ips=2222.3333740234375; avmws=1.1969075358631b6a677133b436426135.46539221.1662761612.1662761638.3.2973257633; QSI_HistorySession=https%3A%2F%2Fwww.rei.com%2Fc%2Fmens-clothing%3Fpage%3D2~1662746035535%7Chttps%3A%2F%2Fwww.rei.com%2Fc%2Fmens-clothing%3Fpage%3D3~1662750259114%7Chttps%3A%2F%2Fwww.rei.com%2F~1662761614807%7Chttps%3A%2F%2Fwww.rei.com%2Fh%2Fclimbing~1662761631057%7Chttps%3A%2F%2Fwww.rei.com%2Fc%2Fclimbing~1662761639447; akaas_Search=1665353649~rv=19~id=f9b8e6a519a06ad7bf24b4f8dca25903~rn=; bm_sv=25285EB4F65436874CF18D7F19D67B0D~YAAQGmzNF1nPgR+DAQAAs0ZRJBEqGTv2rpT/3e/5ljPmfK6AN532Uvhm/hFVqK0PMZ7BMXlzOJNM9OK21lsVLgN1ZeGSEzg7V4/19MmwR6rb0/jWsDfaaVapc8YpXFJvDo1rg9s1HJaoz66VYLqH5pUhXPWuJ3D2/OWkhUeaZmPvha820RGwmhuxsczY8s+RXnwE05DI/vXx0lEzDPnu2N88d6EPYZQ0f2ewyCLDPSPrdK+uImu9R3Pwrzbi~1; s_tp=10462; s_ppv=rei%253Anav_search%253Aclimbing%2C90%2C21%2C9381.22265625%2C8%2C9; utag_main=v_id:018323179e5b001eb83fc90f5e6905075001406d00ac8$_sn:5$_ss:0$_st:1662763458352$vapi_domain:rei.com$ses_id:1662761611222%3Bexp-session$_pn:3%3Bexp-session$_prevpage:rei%3Anav_search%3Aclimbing%3Bexp-1662765258354$_prevtemp:nav_search%3Bexp-1662765237850; s_sq=%5B%5BB%5D%5D",
            "authority": "www.rei.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "referer": "https://www.rei.com/c/climbing?page=2",
            "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
                }

        while True:
            try:
                response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
                break
            except:
                print("Response unsuccessful")
                time.sleep(15)

        time_taken = time.time() - start

        #make this the sleep timer interval, beacuse its the difference in allowed access

        #print(response.json())

        #print(response.ok)

        print(f"\rFetching page {x} of {n-1} at {url}, time per query is {time_taken}", end="")

        data = response.json()
        # access the data on the page by using the key, then the list indices location
        for p in data['searchResults']['results']:
            results.append(p)

    results_df = pd.json_normalize(results)
    results_df.to_csv('REIscrape.csv')
    return results_df