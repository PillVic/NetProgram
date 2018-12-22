rom urllib.request import urlopen
from bs4 import BeautifulSoup

city = dict()
with open('dict.txt') as f:
    lines = f.readlines()
    for line in lines:
        cityName, cityCode = line.split(':')
        city[cityName] = cityCode.rstrip(' \n')

def getWeather(cityName):
    cityCode = city.get(cityName)
    if cityCode == None:
        return '[Error]: City Not Found'
    print(cityCode)
    resp=urlopen('http://www.weather.com.cn/weather/'+str(cityCode)+'.shtml')
    soup=BeautifulSoup(resp,'html.parser')

    today = soup.find('p', class_='tem')
    date=soup.find('ul',class_="t clearfix").h1.string
    weather=soup.find('p', class_="wea").string
    wind=soup.find('p',class_='win').i.string
    low=today.i.string
    high=today.find_next('p', class_="tem").span.string
    ray=soup.find('li',class_='li1').p.string
    sport=soup.find('li',class_='li2 hot').p.string
    bloodsugar=soup.find('li',class_='li5').p.string
    wear=soup.find('li',class_='li3 hot').p.string
    washcar=soup.find('li',class_='li4').p.string
    pollute=soup.find('li',class_='li6').p.string

    info = '''
    天气:%s
    风级:%s
    最低气温:%s
    最高气温:%s
    紫外线指数:%s
    减肥指数:%s
    血糖指数:%s
    穿衣指数:%s
    洗车指数:%s
    空气污染指数:%s
    ''' %(weather, wind, low, high, ray, sport, bloodsugar, wear, washcar, pollute)
    return info





if __name__ == '__main__':
    while True:
        cityName = input('Please input the cityName: ')
        print(getWeather(cityName))

