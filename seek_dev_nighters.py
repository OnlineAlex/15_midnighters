import requests
from pytz import timezone
from datetime import datetime

SOLUTION_ATTEMPTS_URL = 'http://devman.org/api/challenges/solution_attempts/'


def get_number_pages():
    response = requests.get(SOLUTION_ATTEMPTS_URL)
    pages = response.json()['number_of_pages']
    return pages


def load_attempts(pages):
    for page in range(1, pages+1):
        response = requests.get('{}?page={}'.format(SOLUTION_ATTEMPTS_URL, page))
        solution_attempts_on_page = response.json()['records']

        for attempt in solution_attempts_on_page:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }


def get_midnighters(today_attempts):
    midnighters_users = []
    for attempt in today_attempts:
        user_time = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=timezone(attempt['timezone'])
        )
        if user_time.hour < 5:
            midnighters_users.append(attempt['username'])

    return set(midnighters_users)


if __name__ == '__main__':
    try:
        number_pages = get_number_pages()
        solution_attempts = load_attempts(number_pages)
    except requests.ConnectionError:
        exit('Не удалось подключиться к серверу'
             'Проверьте интернет соеденние')

    devman_midnighters = get_midnighters(solution_attempts)
    print('Сов на davman.org — {}'.format(len(devman_midnighters)))
    for index, devman_midnighter in enumerate(devman_midnighters, start=1):
        print('{:>3}: {}'.format(index, devman_midnighter))
