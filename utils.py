import datetime
import requests
import urllib
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")

def extract_job_title(div):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['title'].casefold())
    return('NOT_FOUND')

def extract_company(div): 
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
        for b in company:
            return (b.text.strip())
    else:
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
            return (span.text.strip())
    return 'NOT_FOUND'

def extract_location(div):
    for span in div.findAll('span', attrs={'class': 'location'}):
        return (span.text)
    return 'NOT_FOUND'

def extract_link(div): 
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['href'])
    return('NOT_FOUND')

def extract_date(div):
    try:
        spans = div.findAll('span', attrs={'class': 'date'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'

# extract full job description from link
"""def extract_fulltext(url):
    try:
        page = requests.get('http://www.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        spans = soup.findAll('div', attrs={'class': 'jobsearch-jobDescriptionText'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'"""



def summary(div):
    for a in div.find_all('span', {'id': 'job_summary'}):
        return a.text

def get_past_date(str_days_ago):
    TODAY = datetime.date.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].casefold() == 'today':
        return str(TODAY.isoformat())
    elif len(splitted) == 1 and splitted[0].casefold() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return str(date.isoformat())
    elif len(splitted) > 1 and splitted[1].casefold() in ['hour', 'hours', 'hr', 'hrs', 'h','uur', 'Stunden','horas','or\u0103','ore','godz.','timmar','\u0447\u0430\u0441\u0430']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif len(splitted) > 1 and splitted[1].casefold() in ['day', 'days', 'd','dagar','dag','dagen','Tag','Tagen','d\u00edas','dni','\u0434\u043d\u044f','\u0434\u043d\u0435\u0439','\u0434\u043d\u044f','giorni']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    elif len(splitted) > 1 and splitted[1].casefold() in ['mon', 'mons', 'month', 'months', 'm','maanden','mesi','mies.','m\u00e5nader','\u043c\u0435\u0441\u044f\u0446\u0435\u0432']:
        date = TODAY - relativedelta(months=int(splitted[0]))
        return str(date.isoformat())
    elif len(splitted) > 1 and splitted[2].casefold() in ['stunden','horas','or\u0103','ore']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[1]))
        return str(date.date().isoformat())
    elif len(splitted) > 1 and splitted[2].casefold() in ['tag','tagen','d\u00edas','zile']:
        date = TODAY - relativedelta(days=int(splitted[1]))
        return str(date.isoformat())
    elif len(splitted) > 1 and splitted[2].casefold() in ['monaten','meses','luni']:
        date = TODAY - relativedelta(months=int(splitted[1]))
        return str(date.isoformat())
    elif len(splitted) > 1 and splitted[4].casefold() in ["heures"]:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[3]))
        return str(date.date().isoformat())
    elif len(splitted) > 1 and splitted[4].casefold() in ["jours"]:
        date = TODAY - relativedelta(days=int(splitted[3]))
        return str(date.isoformat())
    elif len(splitted) > 1 and splitted[4].casefold() in ["mois"]:
        date = TODAY - relativedelta(months=int(splitted[3]))
        return str(date.isoformat())
    else:
        return "Wrong Argument format"

def get_timestamp(str_days_ago):
    try:
        TODAY = datetime.datetime.today()
        splitted = str_days_ago.split()
        if len(splitted) == 1 and splitted[0].casefold() in ['today','oggi','heute','aujourd\u2019hui','dnes','idag','dzisiaj','azi']:
            return int(datetime.datetime.timestamp(TODAY))
        elif len(splitted) == 1 and splitted[0].casefold() == 'yesterday':
            date = TODAY - relativedelta(days=1)
            return int(datetime.datetime.timestamp(TODAY))
        elif len(splitted) > 1 and splitted[1].casefold() in ['hour', 'hours', 'hr', 'hrs', 'h','uur', 'Stunden','horas','or\u0103','ore','godz.','timmar','\u0447\u0430\u0441\u0430','\u0447\u0430\u0441\u043e\u0432']:
            date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[1].casefold() in ['day', 'days', 'd','dagar','dag','dagen','Tag','Tagen','d\u00edas','dni','\u0434\u043d\u044f','\u0434\u043d\u0435\u0439','giorni']:
            date = TODAY - relativedelta(days=int(splitted[0]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[1].casefold() in ['mon', 'mons', 'month', 'months', 'm','maanden','mesi','mies.','m\u00e5nader','\u043c\u0435\u0441\u044f\u0446\u0430']:
            date = TODAY - relativedelta(months=int(splitted[0]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[2].casefold() in ['stunden','horas','or\u0103','ore','hodinami','hora']:
            date = datetime.datetime.now() - relativedelta(hours=int(splitted[1]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[2].casefold() in ['tag','tagen','d\u00edas','zile','zi','dny']:
            date = TODAY - relativedelta(days=int(splitted[1]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[2].casefold() in ['monaten','meses','luni','měsíci']:
            date = TODAY - relativedelta(months=int(splitted[1]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[4].casefold() in ["heures"]:
            date = datetime.datetime.now() - relativedelta(hours=int(splitted[3]))
            return int(datetime.datetime.timestamp(date))
        elif len(splitted) > 1 and splitted[4].casefold() in ["jours","jour"]:
            date = TODAY - relativedelta(days=int(splitted[3]))
            return str(date.isoformat())
        elif len(splitted) > 1 and splitted[4].casefold() in ["mois"]:
            date = TODAY - relativedelta(months=int(splitted[3]))
            return int(datetime.datetime.timestamp(date))
        else:
            return "Wrong Argument format"
    except Exception as e:
        pass
        
def extract_fulltext(job_id):
    ajax_url = 'https://www.indeed.com/rpc/jobdescs?jks=' + urllib.parse.quote(job_id.encode('utf-8'))
    ajax_content = requests.get(ajax_url).json()
    soup = BeautifulSoup(ajax_content[job_id],"lxml")
    text = soup.get_text().casefold().replace('\t', '').replace('\n', '')
    return text

def check(string, forbidden, skills):
    match = []
    if any(s_prefix in string for s_prefix in forbidden): return match
    match = [skill for skill in skills if skill in string]
    return match

def unique(data):
    result = {}
    for key, value in data.items():
        new_list = []
        url_list = []
        for item in value:
            if item['url'] not in url_list:
                new_list.append(item)
                url_list.append(item['url'])
        result[key] = new_list
        return result