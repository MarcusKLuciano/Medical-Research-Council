import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import requests
import json
import os
from p_tqdm import p_map
import argparse
from datetime import datetime
import random

parser = argparse.ArgumentParser(description='Find the the doctor Details from nmc for any given year/years')
parser.add_argument('--year',metavar='year',help='Enter the year in string, for a single year',type=str)
parser.add_argument('--years', action=argparse.BooleanOptionalAction, help='Set true to set a range of years with start year and end year both included')

args = parser.parse_args()

if args.years == True:
    start_year = input('Set the start year: ')
    end_year = input('Set the end year which is to be included: ')
    year_list = [str(x) for x in range(int(end_year),int(start_year)+1,-1)]
    print(year_list)
else:
    year_list = [args.year]
    # print(year_list)

ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43'
    ]
    
def get_doc_details(tup):
    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43'
    ]
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from tqdm import tqdm
    import requests
    import json
    import os
    import random

    url = "https://www.nmc.org.in/MCIRest/open/getDataFromService?service=getDoctorDetailsByIdImr"

    payload = json.dumps({
      "doctorId": str(tup[0]).replace(' ','%20'),
      "regdNoValue": str(tup[1]).replace(' ','%20')
    })
    headers = {
      'Accept': '*/*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json',
      'Cookie': 'JSESSIONID=mBhxeXmYueexqZ0jWSHL5newF9_Jys2kKf0Jxkdj.web3; PHPSESSID=8dn4rle6gsquead8r290ika3n2',
      'DNT': '1',
      'Origin': 'https://www.nmc.org.in',
      'Pragma': 'no-cache',
      'Referer': 'https://www.nmc.org.in/information-desk/indian-medical-register/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': random.choice(ua_list),
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:

        data = response.json()

        data['key']=tup

        return(data)
    
    except:
        return {}


def get_doc_list(year):
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from tqdm import tqdm
    import requests
    import json
    import os
    main = []
    header_list = ['sl_no','year_of_info','reg_no','state_med_councils','name','father_name','detail_keys']
    url = f"https://www.nmc.org.in/MCIRest/open/getPaginatedData?service=getPaginatedDoctor&draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=500&search%5Bvalue%5D=&search%5Bregex%5D=false&year={str(year)}&_=1679470517752"

    payload={}
    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'en-US,en;q=0.9',
      'Connection': 'keep-alive',
      'Cookie': 'JSESSIONID=syaLGf2DMSd46dybBNanH9tKzXkdqDKdHDa_5sPF.web3; PHPSESSID=9m16moe1m0871c0th6tp9glsq1; JSESSIONID=yLckDK8d14GxIpBa1F2UYSg8VbP_woph4mGlbd7R.web3',
      'DNT': '1',
      'Referer': 'https://www.nmc.org.in/information-desk/indian-medical-register/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': random.choice(ua_list),
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    pages = int(response.json()['recordsFiltered']/500)+1
    for i in tqdm(range(1,pages+1)):
        url = f"https://www.nmc.org.in/MCIRest/open/getPaginatedData?service=getPaginatedDoctor&draw={str(i)}&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start={(i-1)*500}&length=500&search%5Bvalue%5D=&search%5Bregex%5D=false&year={str(year)}&_=1679470517752"
        response = requests.request("GET", url, headers=headers, data=payload)
        docs = response.json()['data']
        for doc in docs:
            soup = bs(doc[-1],'lxml')
            try:
                tup = eval(soup.find('a')['onclick'].replace('openDoctorDetailsnew',''))
                doc[-1] = tup
            except:
                doc[-1] = (0,0)
            a = {header_list[i]: doc[i] for i in range(len(header_list))}
            main.append(a)
    pd.DataFrame(main).to_pickle(f'../data/doctor_list_{str(year)}.pkl')
    tup_list = pd.DataFrame(main)['detail_keys'].tolist()
    print(f'doc_list_for_{year}_done')
    res = p_map(get_doc_details,tup_list,num_cpus=8)
    pd.DataFrame(res).to_pickle(f'../data/doctor_details_{year}.pkl')
    main = []
    print(f'year {year}')

if args.years == True:
    for year in year_list:
        get_doc_list(year)

else:
    get_doc_list(year_list[0])

