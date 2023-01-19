import requests #1 шаг работы
from bs4 import BeautifulSoup
import json
import csv

url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie" #2 шаг работы

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0"
}

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w", encoding="utf-8") as file: #3 шаг работы
    file.write(src)

with open("index.html", encoding="utf-8") as file:
    src1 = file.read()

soup = BeautifulSoup(src1, "lxml")
all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

all_categories_dict = {}
for item in all_products_hrefs:
    item_text = item.text
    item_href = "https://health-diet.ru" + item.get("href")

    all_categories_dict[item_text] = item_href

with open("all_categories_dict.json", "w", encoding="utf-8") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", encoding="utf-8") as file:
   all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():

    req = requests.get(url=category_href, headers=headers)
    src2 = req.text

    with open(f"product/{count}_{category_name}.html", "w", encoding="utf-8") as file:
        file.write(src2)

    with open(f"product/{count}_{category_name}.html", encoding="utf-8") as file:
        src2 = file.read()

    soup1 = BeautifulSoup(src2, "lxml")

    #проверка страницы на наличие таблицы!
    alert = soup1.find(class_="uk-alert-danger")
    if alert is not None:
        continue

    table_head = soup1.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"product/{count}_{category_name}.csv", "w", encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    product_data = soup1.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    for item in product_data:
        product_tds = item.find_all("td")

        title = product_tds[0].find("a").text
        product = product_tds[0].text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        with open(f'product/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    count += 1
    print(f" Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print ("Работа закончена")
        break

    print(f" ОСталось итераций: {iteration_count}")

