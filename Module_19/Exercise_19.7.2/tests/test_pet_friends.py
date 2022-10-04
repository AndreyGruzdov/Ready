from api import PetFriends
from settings import valid_email, valid_password

import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Myny', animal_type='spanel',
                                     age='20', pet_photo='images/cote.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print( name)


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Miki", "mous", "3", "images/ims.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Mymy', animal_type='Spaniel', age='5'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


"""Дополнительные тест-кейсы"""


def test_get_api_key_for_not_valid_user(email = '1sas1@rusp.ru', password = '1EG24wLgtADBP2At1'):
    """ Тест с проверкой неверных значений email and password. """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert 'key' not in result


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос возвращает не пустой список .
    Получаем ключ запрашиваем список моих питомцев и проверяем что список не пустой
    значение параметра filter - 'my_pets' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Еслди список не пустой
    if len(result['pets']) > 0:
           # Проверяем что статус ответа = 200 и результат отличный от нуля
        assert status == 200
        assert len(result['pets']) > 0
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_get_all_pets_with_not_valid_key(filter=' '):
    """ Проверяем что запрос всех питомцев с неверным ключем возвращает пустой список.
    Получаем api ключ и сохраняем в переменную auth_key(или без этого). Далее меняем этот ключ,
    запрашиваем список всех питомцев, проверяем что статус ответа не равен 200 и список питомцев пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': 'ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200
    #assert 'pets' is not result


def test_get_all_pets_with_not_valid_filter_faild(filter='abc'):
    """Проверяем что запрос с некоректным значением filter выдает статус отличный от 200 и не выдает значений 'pets'
    Получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список питомцев с значением filter='123'."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'pets' not in result


def test_add_new_home_pet_without_photo(name='Mickey',
                                        animal_type='Mouse',
                                        age='1'):
    """Проверяем что можно добавить питомца без фото """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_add_pet_nofoto(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] == ''


def test_post_change_pet_foto(pet_photo='images/ims.jpg'):
    """Проверяем добавление нового фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового (БЕЗ ФОТО) и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_pet_nofoto(auth_key, "Mickey", "Mouse", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Добавляем фото
    status, result = pf.post_add_pet_photo(auth_key, pet_id, pet_photo)
    print(result )
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''


def test_add_new_pet_with_valid_special_characters_data(name='!"№;%:?*()_+@#$%^&*_+',
                                                        animal_type='!"№;%:?*()_+@#$%^&*_+',
                                                        age='11',
                                                        pet_photo='images/ims.jpg'):
    """ Проверяем что можно добавить питомца с спецсимволами в разделах name и animal_type """

       # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type


def test_post_changes_foto_and_update_self_pet_info(name='Мурзик',
                                                    animal_type='Котэ',
                                                    age='9',
                                                    pet_photo='images/cote.jpeg'):
    """Тестируем изменение фото питомца с заменой name and animal_type предыдущего теста"""
      # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

     # Значение картинки1:
    value_image1 = my_pets['pets'][0]['pet_photo']

    #Если список не пустой, то пробуем обновить его имя, тип, возраст и фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        status, result = pf.post_add_pet_photo(auth_key, pet_id, pet_photo)
        # Значение картинки2:
        value_image2 = result.get('pet_photo')
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        # Если полученное значение ключа одной картинки не равно значению ключа другой картинки - PASSED:
        assert value_image1 != value_image2
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_with_not_valid_data_faild(name='', animal_type='',
                                     age='', pet_photo='images/cote.jpeg'):
    """Тест создание питомца с пустыми значениями в разделах name, animal_type,age """

     # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == ''
    assert result['name'] == ''
    assert result['animal_type'] == ''


def test_delete_self_pet_without_id():
    """Удаление питомца без указания id."""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    #Значение списка
    listPets1 = my_pets['pets']#[0]['id']

    pet_id = ""
    status, result = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    #Значение списка
    listPets2 = my_pets['pets']#[0]['id']

    # Проверяем что статус ответа равен 404 и списки равны

    assert status == 404
    assert listPets1 == listPets2
