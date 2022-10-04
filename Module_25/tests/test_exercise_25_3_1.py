#pytest --driver Firefox --driver-path geckodriver.exe test_exercise_25_3_1.py
#pytest -v --driver Chrome --driver-path chromedriver.exe test_exercise_25_3_1.py

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_all_pets(my_open_pets):
   '''Присутствуют все питомцы'''

   WebDriverWait(pytest.driver, 5).until(
      EC.presence_of_element_located((By.XPATH, '/ html / body / div[1] / div / div[1]')))
   WebDriverWait(pytest.driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

   #Элементы статистики пользователя
   statistic = pytest.driver.find_element_by_xpath('/ html / body / div[1] / div / div[1]')
   number = int(statistic.text.split('\n')[1].split(':')[1].strip())

   #Kоличество карточек питомцев
   pets_card = len(pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr'))

   #Kоличество питомцев из статистики совпадает с количеством карточек питомцев
   assert number == pets_card

def test_have_photo(my_open_pets):
   '''На странице со списком моих питомцев у половины питомцев есть фото'''

   #Элементы статистики пользователя
   statistic = pytest.driver.find_element_by_xpath('/ html / body / div[1] / div / div[1]')
   number = int(statistic.text.split('\n')[1].split(':')[1].strip())
   # Сохраняем в переменную images элементы с атрибутом img
   images = pytest.driver.find_elements_by_css_selector('.table.table-hover img')

   mid = number // 2 #Половина количества питомцев пользователя

   # Находим количество питомцев с фотографией
   number_а_photos = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         number_а_photos += 1

   # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
   assert number_а_photos >= mid

def test_pets_have_all_parameters(my_open_pets):
   '''Ищем на странице пользователя что у всех питомцев есть имя, возраст и порода:'''

   # Настраиваем неявные ожидания:
   pytest.driver.implicitly_wait(10)

   names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')#Сохраняем имена питомцев в переменную
   breed = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')#Сохраняем породу питомцев в переменную
   age = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')#Сохраняем возраст питомцев в переменную

   #Проверка во всех случаях наличее или отсутствие текста
   for i in range (len(names)):
      assert names[i].text != ''
      assert breed[i].text != ''
      assert   age[i].text != ''

def test_all_pets_have_different_names(my_open_pets):
   '''Поверяем что на странице со списком моих питомцев, у всех питомцев разные имена'''

   name_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
   # Проверяем, что у всех питомцев разные имена:
   list_name_my_pets = []
   for i in range(len(name_my_pets)):
      list_name_my_pets.append(name_my_pets[i].text)
   set_name_my_pets = set(list_name_my_pets) # преобразовываем список в множество
   assert len(list_name_my_pets) == len(set_name_my_pets) # сравниваем длину списка и множества: без повторов должны совпасть

def test_no_duplicate_pets(my_open_pets):
   '''Поверяем что на странице со списком моих питомцев нет повторяющихся питомцев'''

   data_my_pets = pytest.driver.find_elements_by_css_selector('tbody>tr')
   # Проверяем, что в списке нет повторяющихся питомцев:
   list_data_my_pets = []
   for i in range(len(data_my_pets)):
      list_data = data_my_pets[i].text.split("\n") # отделяем от данных питомца "х" удаления питомца
      list_data_my_pets.append(list_data[0]) # выбираем элемент с данными питомца и добавляем его в список
   set_data_my_pets = set(list_data_my_pets) # преобразовываем список в множество
   assert len(list_data_my_pets) == len(set_data_my_pets) # сравниваем длину списка и множества: без повторов должны совпасть


