import pandas as pd
import requests as rq

url='https://www.sec.gov/cgi-bin/viewer?action=view&cik=1288776&accession_number=0001288776-15-000046&xbrl_type=v'
resp=rq.get(url)
dfs=pd.read_html(resp.text)
for df in dfs:
    print(df)