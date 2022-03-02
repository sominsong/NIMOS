import csv
import requests
from bs4 import BeautifulSoup

# for firewall pypass
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)\
     AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/55.0.2919.83 Safari/537.36'
}

url = "http://upstream.rosalinux.ru/tests/glibc/2.13/view_tests.html"
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, "html.parser")
# body > div:nth-child(1) > a:nth-child(6460) > span
# print(soup.find_all(attrs={"class":"int"}))
resultset = soup.select(".int")

funcList = []

for tag in resultset:   # type: element.Tag
    func = tag.get_text()
    funcList.append(func.split()[0])

with open("./API_Sanity_checker_funcion_list.csv","w", encoding='utf-8', newline='') as f:
    wr = csv.writer(f)
    wr.writerow(["function"])
    for func in funcList:
        wr.writerow([f"{func}"])