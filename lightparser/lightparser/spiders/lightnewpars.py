import scrapy
import csv
import os

class LightnewparsSpider(scrapy.Spider):
    name = "lightnewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/torshery"]

    def __init__(self):
        # Открываем файл с кодировкой utf-8-sig
        self.file_path = "lights.csv"
        self.file = open(self.file_path, "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.file)

        # Добавляем заголовки
        self.writer.writerow(["Название товара", "Цена", "Ссылка на товар"])

    def parse(self, response):
        lights = response.css('div.LlPhw')
        for light in lights:
            name = light.css('div.lsooF span::text').get()
            price = light.css('div.pY3d2 span::text').get()
            url = response.urljoin(light.css('a').attrib['href'])

            # Проверяем, что данные не пустые
            if name and price and url:
                self.writer.writerow([name, price, url])
                yield {
                    "Название товара": name,
                    "Цена": price,
                    "Ссылка на товар": url
                }

    def closed(self, reason):
        self.file.close()
