import requests
from bs4 import BeautifulSoup
import json


def main():
    result_list = []
    count = 0
    games = 0
    for i in range(1, 11):
        url = f'https://kanobu.ru/games/popular/?page={i}'
        count += 1
        print(f'Парсим {i} страницу...')
        req = requests.get(url=url)
        soup = BeautifulSoup(req.text, 'lxml')

        games_names = soup.find_all('div', class_='BaseElementCard_body__fcrUh')
        names = [name.find('a').text.strip() for name in games_names]
        game_urls = soup.find_all('a', class_='knb-card--image style_wrap__t_NZD')

        for item in range(0, len(game_urls)):
            try:
                url = game_urls[item].get('href')
                game_dict = {}
                req = requests.get(url='https://kanobu.ru/' + url)
                soup = BeautifulSoup(req.text, 'lxml')

                games += 1
                game_dict['ID'] = games
                game_name = names[item]
                game_dict['Игра'] = game_name
                main_info = soup.find('div', class_='baseElementLayout_page_options__PknYS').find_all('div', class_='DatabaseElementOption_option__52an1')

                for j in main_info:
                    div = j.find_all('span')
                    game_dict[div[0].text.strip()] = div[1].text.strip()

                result_list.append(game_dict)
            except Exception as ex:
                print(ex)
                print('Упс, что-то пошло не так...')

    with open('game_list_result.json', 'a', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
    print(f"""
\nМы всё спарсили!
Всего игр: {games}.
Все данные записаны в файл 'game_list_result.json'.
""")


if __name__ == '__main__':
    main()
