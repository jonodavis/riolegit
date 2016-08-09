from bs4 import BeautifulSoup
import requests
from django.core.exceptions import ObjectDoesNotExist

from olympics import models

RESULTS_URL = 'http://www.espn.com/olympics/summer/2016/results/_/date/201608%02d'


def get_results():
    for day in range(3, 21):
        page = requests.get(RESULTS_URL % day).content
        soup = BeautifulSoup(page, 'html.parser')
        tables = soup('table', class_='olympics results')
        print('Parsing %d tables.' % len(tables))
        for table in tables:
            # Event name is up to the first comma.
            event_name = str(table.find('th').text).split(',')[0].strip()
            discipline = str(table.find_parent('div', class_='discipline-container').find('h2', class_='table-caption')
                             .text).strip()
            rows = table('tr', class_='home')
            if len(rows) == 0:
                continue

            first_medal = rows[0].find('span', class_='olympics-medal')
            if not first_medal:
                continue

            if 'gold' in first_medal['class']:
                gold_winner = find_country(str(rows[0].find('img', class_='team-logo')['src']))
                silver_winner = find_country(str(rows[1].find('img', class_='team-logo')['src']))
                bronze_winner = None
                fourth_place = None
                if len(rows) > 2:
                    bronze_winner = find_country(str(rows[2].find('img', class_='team-logo')['src']))
                if len(rows) > 3:
                    fourth_place = find_country(str(rows[3].find('img', class_='team-logo')['src']))

                try:
                    model = models.Event.objects.get(name=event_name, discipline=discipline)
                except ObjectDoesNotExist:
                    model = models.Event()
                    model.name = event_name
                    model.discipline = discipline
                model.gold_winner = gold_winner
                model.silver_winner = silver_winner
                model.bronze_winner = bronze_winner
                model.fourth_place = fourth_place
                print('Loading event %s: %s: Gold - %s, Silver: %s, Bronze: %s, 4th: %s'
                      % (discipline, event_name, gold_winner.name, silver_winner.name,
                         'Unknown' if bronze_winner is None else bronze_winner.name,
                         'Unknown' if fourth_place is None else fourth_place.name))
                model.save()
            elif 'bronze' in first_medal['class']:
                bronze_winner = find_country(str(rows[0].find('img', class_='team-logo')['src']))
                fourth_place = find_country(str(rows[1].find('img', class_='team-logo')['src']))
                try:
                    model = models.Event.objects.get(name=event_name, discipline=discipline)
                except ObjectDoesNotExist:
                    model = models.Event()
                    model.name = event_name
                    model.discipline = discipline
                model.bronze_winner = bronze_winner
                model.fourth_place = fourth_place
                print('Loading event %s: %s: Bronze: %s, 4th: %s'
                      % (discipline, event_name, bronze_winner.name,
                         fourth_place.name))
                model.save()


def find_country(img: str):
    code = img[-12:-9]
    return models.Country.objects.get_or_create(code=code)[0]


if __name__ == '__main__':
    get_results()
