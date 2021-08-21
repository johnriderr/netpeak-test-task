import os
import string
from random import randint, choices
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def select_random_selement_from_drop_down(elem_name):
    dropdown = driver.find_element_by_name(elem_name)
    elements_in_dropdown = dropdown.find_elements_by_tag_name('option')[1:]
    dropdown_select = Select(dropdown)
    dropdown_select.select_by_visible_text(
        elements_in_dropdown[randint(0, len(elements_in_dropdown) - 1)].text
    )


if __name__ == '__main__':
    TIMEOT_SEC = 10
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(TIMEOT_SEC)

    # 1. Перейти по ссылке на главную страницу сайта Netpeak. (https://netpeak.ua/)
    driver.get('https://netpeak.ua/')

    # 2. Перейдите на страницу "Работа в Netpeak", нажав на кнопку "Карьера"
    elem = driver.find_element_by_class_name('main-navigation')
    elem = elem.find_element_by_link_text('Карьера').click()
    old_tab = driver.current_window_handle
    all_tabs = driver.window_handles
    new_tab = [x for x in all_tabs if x != old_tab][0]
    driver.close()
    driver.switch_to.window(new_tab)

    # 3. Перейти на страницу заполнения анкеты, нажав кнопку - "Я хочу работать в Netpeak"
    driver.find_element_by_link_text('Я хочу работать в Netpeak').click()

    # 4. Загрузить файл с недопустимым форматом в блоке "Резюме", например png,
    # и проверить что на странице появилось сообщение, о том что формат изображения неверный.
    driver.find_element_by_css_selector('input[type=file]').send_keys(os.path.join(os.getcwd(), 'py-logo.jpg'))
    WebDriverWait(driver, TIMEOT_SEC).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#up_file_name .control-label'),
            'Ошибка: неверный формат файла (разрешённые форматы: doc, docx, pdf, txt, odt, rtf).')
    )

    # 5. Заполнить случайными данными блок "3. Личные данные"
    driver.find_element_by_id('inputName').send_keys(''.join(choices(string.ascii_lowercase, k=randint(5, 15))))
    driver.find_element_by_id('inputLastname').send_keys(''.join(choices(string.ascii_lowercase, k=randint(5, 15))))
    driver.find_element_by_id('inputEmail').send_keys(
        ''.join(choices(string.ascii_lowercase, k=randint(5, 15))) + '@gmail.com')
    driver.find_element_by_id('inputPhone').send_keys(''.join([str(randint(0, 9)) for x in range(0, 11)]))

    select_random_selement_from_drop_down('by')
    select_random_selement_from_drop_down('bm')
    select_random_selement_from_drop_down('bd')

    # 6. Нажать на кнопку отправить резюме
    driver.find_element_by_css_selector('[for="agree_rules"]').click()
    driver.find_element_by_id('submit').click()

    # 7. Проверить что сообщение на текущей странице - "Все поля
    # являются обязательными для заполнения" - подсветилось красным цветом
    assert driver.find_element_by_class_name('warning-fields').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'

    # 8. Перейти на страницу "Курсы" нажав соответствующую кнопку в меню и убедиться что открылась нужная страница.
    driver.find_element_by_link_text('Курсы').click()
    assert driver.current_url == 'https://school.netpeak.group/'

    driver.close()
