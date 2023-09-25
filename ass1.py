import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# get the htlm
resp = requests.get('https://ca.trustpilot.com/review/equitablebank.ca')

print(resp.text)
# This is the html source
html_code = resp.text


soup = BeautifulSoup(html_code, 'html.parser')
item = soup.find(
name='p',
attrs={'class':'typography_body-l__KUYFJ typography_appearance-default__AAY17'}
)
N = int(item.contents[0].replace(',',''))
print(N)

data_para = []
data_time = []
data_ratingvalue=[]
review_count = 0 
current = 'https://ca.trustpilot.com/review/equitablebank.ca'
page = 'https://ca.trustpilot.com'
All_page=[current]
while current:
    response = requests.get(current)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.find_all(name="a", string='Next page')
        review = soup.find_all(
            name='div',
            attrs={
              'class':'styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ'
            }
        )
        for section in review:
            para = section.find(
                              name = 'p',
                              class_ = "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"
        )
            time_tag = section.find(
                  name = 'time'
            )
            ratingvalue = section.find(
                  class_="styles_reviewHeader__iU9Px"
            )
            if review_count >= 10:
                 current = False
                 break
            elif para:
                  paras = para.text
                  data_time.append(time_tag['datetime'])
                  data_para.append(paras)
                  data_ratingvalue.append(ratingvalue['data-service-review-rating'])
                  review_count += 1
            else:
                  paras = None
                  data_time.append(time_tag['datetime'])
                  data_para.append(paras)
                  data_ratingvalue.append(ratingvalue['data-service-review-rating'])
                  review_count += 1

        if next_page[0].get('href', ''):
            next_url = page + next_page[0]['href']
            current = next_url
            print(current)
        else:
            current = False
    else:
        current = False



df = pd.DataFrame({'Text': data_para, 'Time':data_time, 'Rating':data_ratingvalue, 'Name': 'Equitable Bank'})

df