import requests
from pytz import timezone
from datetime import datetime


def load_attempts(api_upl):
    page_number = 1

    while True:
        response = requests.get(api_upl, params={'page': page_number})
        if response.status_code == 404:
            break
        solution_attempts_on_page = response.json()['records']
        for attempt in solution_attempts_on_page:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }
        page_number += 1


def get_midnighters(all_attempts):
    midnighters_users = []
    for attempt in all_attempts:
        user_time = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=timezone(attempt['timezone'])
        )
        if user_time.hour < 5:
            midnighters_users.append(attempt['username'])

    return set(midnighters_users)


if __name__ == '__main__':
    solution_attempts_url = 'http://devman.org/api/challenges/solution_attempts/'
    try:
        solution_attempts = load_attempts(solution_attempts_url)
    except requests.ConnectionError:
        exit('Не удалось подключиться к серверу'
             'Проверьте интернет соеденние')

    devman_midnighters = get_midnighters(solution_attempts)
    print('Сов на davman.org — {}'.format(len(devman_midnighters)))
    for index, devman_midnighter in enumerate(devman_midnighters, start=1):
        print('{:>3}: {}'.format(index, devman_midnighter))
