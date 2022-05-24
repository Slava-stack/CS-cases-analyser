import csv
import time

from website import site
import requests
from bs4 import BeautifulSoup
import schedule


def establish_connections():
    """
    \Tor Browser\Browser\TorBrowser\Tor\tor.exe  should be turned on.
    """
    headers = {
        'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    url = site
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    }
    resp = requests.get(url, headers=headers, proxies=proxies)
    return resp


def getting_cases(response):  # from 1 am till 3 am have some problems
    """
    parse html -> list of cases regarding list 'cases_names'
    """
    cases_names = ['Кейс «Змеиный укус»', 'Кейс «Решающий момент»',
                   'Кейс «Разлом»', 'Кейс «Грёзы и кошмары»', 'Кейс «Призма 2»']
    cases_drop_rate = []
    soup = BeautifulSoup(response.content, 'html.parser')
    cases = soup.find('tbody').find_all('tr')
    for link in cases:
        tds = link.find_all('td')
        try:
            td_first = tds[0].find('a').text
        except AttributeError:
            continue
        if td_first in cases_names:
            cases_drop_rate.append([td_first, tds[1].text])
    return sorted(cases_drop_rate)


def unzipping_lists_in_list_and_adding_datetime(lt):
    b = []
    """
    Unzips lists from the main list 'lt' to b and
    returns b list that contains data about cases and
    current datetime
    """
    curr_date = time.localtime(time.time())[1:3]  # date
    curr_date = curr_date[1], curr_date[0]
    curr_date = [i if len(str(i)) == 2 else '0' + str(i) for i in curr_date]
    curr_date = '.'.join(list(map(str, (list(curr_date)))))
    curr_time = time.localtime(time.time())[3:6]  # time
    curr_time = [i if len(str(i)) == 2 else '0' + str(i) for i in curr_time]
    curr_time = ':'.join(list(map(str, (list(curr_time)))))
    for i in lt:  # unzips lists from the main list 'lt'
        for j in i:
            b.append(j)
    b.append(curr_time)
    b.append(curr_date)
    return b


def writing_down_the_data(data):
    with open('rate_drop.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def reading_the_date_from_csv(csv_file):
    result = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            result.append(row)
    return result


def edit_the_csv_file(csv_file):
    result = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            result.append(row)
    while len(result) >= 21:
        result.pop(0)
    with open(csv_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for el in result:
            writer.writerow(el)


def send_email():
    pass


def drop_analyzer(csv_file='rate_drop.csv'):
    result = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            result.append(row)
    # first = [i for i in result[4][5:-2:2]]
    middle = [i for i in result[8][5:-2:2]]
    last = [i for i in result[-1][5:-2:2]]
    for j in range(0, len(last)):
        if last[j] == middle[j]:
            print("check cases")  # add time to the output
        # send e-mail


def job():
    result = establish_connections()
    data = getting_cases(result)
    unzipping = unzipping_lists_in_list_and_adding_datetime(data)
    writing_down_the_data(unzipping)
    reading_the_date_from_csv('rate_drop.csv')
    edit_the_csv_file('rate_drop.csv')
    drop_analyzer('rate_drop.csv')
    send_email()  # sending a message over email or telegram message
    #   server deployment


def main():
    schedule.every(15).minutes.do(job)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    # wrap the func to avoid errors
    main()
