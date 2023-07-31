import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email = "test@gmail.com"     # Логин показан в качестве образца, используйте актуальные данные
password = "password"        # Пароль показан в качестве образца, используйте актуальные данные

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    '''Переходим на страницу авторизации'''
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )

    yield

    pytest.driver.quit()


def test_show_my_pets():
    '''Вводим email'''
    pytest.driver.find_element(By.ID, 'email').send_keys(email)
    '''Вводим пароль'''
    pytest.driver.find_element(By.ID, 'pass').send_keys(password)
    '''Проверяем, что мы оказались на главной странице'''
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    '''Нажимаем кнопку "Войти"'''
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    '''Нажимаем кнопку мои питомцы'''
    pytest.driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    '''Проверяем, что мы оказались на главной странице пользователя'''
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "guest.sf"
    '''Количество питомцев пользователя из таблицы'''
    tabl_pets_number = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    '''В статистике пользователя берем строку и разделяем ее для получения количества питомцев'''
    pytest.driver.implicitly_wait(10)
    my_pets = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(":")[1]
    '''Объявляем переменную и записываем в нее найденные картинки питомцев'''
    pytest.driver.implicitly_wait(10)
    my_images = pytest.driver.find_elements(By.XPATH, '//tbody//img')
    '''Из таблицы найдем и запишем имя, породу и возраст питомцев'''
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(By.XPATH, '//tbody//td')

    '''Проверим, что количество питомцев на странице равно количеству питомцев указанных в статистике'''
    assert len(tabl_pets_number) == int(my_pets)

    '''Посчитаем сколько питомцев имеют фото'''
    count = 0
    for i in range(len(my_images)):
        if my_images[i].get_attribute('src') != '':
            count += 1
    '''Проверим, что у половины или более питомцев присутствует фото'''
    print('\n', count, '>=', len(tabl_pets_number) / 2)
    assert count >= len(tabl_pets_number) / 2

    '''Проверим, что у всех питомцев есть имя, возраст и порода'''
    for index in range(0, len(names), 4):
        assert names[index].text != '',     'проверка наличия имени питомца'
        assert names[index + 1].text != '', 'проверка наличия породы питомца'
        assert names[index + 2].text != '', 'проверка наличия возраста питомца'

    '''Проверим, что в списке нет питомцев у которых одновременно одинаковое имя, порода и возраст'''
    pets_data = [index.text for index in tabl_pets_number]
    print('Повторяющиеся питомцы', set([index.text for index in tabl_pets_number if pets_data.count(index.text) > 1]))
    assert len(pets_data) == len(set(pets_data))
