[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6f0b73cb31034c16b9da7789a7265703)](https://www.codacy.com/manual/4spb/weather?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=FloMko/weather&amp;utm_campaign=Badge_Grade)## Reference
Проект посвяшен получению информации с сайта infoeco суточных измерени качетсва воздуха
Реализовано получение данных о pm10 и pm2_5
Есть пробелы в данных, связанными с:
  - изменением формата данных (группировка измерений)
  - добавление в данные новых параметров (азот и тд)
  - изменение формата хранения за 2019 год
### Как запустить
необходимо иметь docker установленным на машине
необходимо установить используемые библиотеки python:
pip3 install -r requirements.txt
далее запускаем докер 'docker-compose up -d'
далее python3 pars.py
в виде артефакта работы вы получите файл dummy.csv с собранной статистикой
