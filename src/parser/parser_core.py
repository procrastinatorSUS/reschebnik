from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
import os
import re


def open_page(driver: webdriver.Chrome, example_id: int) -> None: 
    driver.get("https://kompege.ru/task")
    search_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/p[2]/input')
    select_tab = driver.find_element(By.TAG_NAME, 'select')
    # TskNames = select_tab.text.split('\n')
    TaskElements = select_tab.find_elements(By.TAG_NAME, 'option')
    TaskElements[example_id].click()
    search_button.click()
    print('страница открыта')
    sleep(2)

def define_level(text: str) -> str|None:
    levels = {"Базовый": 0, "Средний": 1, "Сложный": 2, "Гроб": 3}
    for level in levels.keys():
        if level in text:
            print()
            return levels[level]
    return None
    
def find_answer(driver: webdriver.Chrome, example: WebElement, ex_type: int) -> str|Tuple[str, str]:
    example.find_element(By.CLASS_NAME, 'link').click() 
    try:
        answer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "answerWrap")))
    except Exception:
        return None
    finally:
        ans_text = answer.find_element(By.TAG_NAME, 'p').text if ex_type != 19 else ' '.join(map(lambda x: x.text, answer.find_elements(By.TAG_NAME, 'p')))
        example.find_element(By.CLASS_NAME, 'link').click()
        return ans_text
    

def example_info(driver:webdriver.Chrome, example:WebElement, ex_type: int) -> Tuple[int|str]:
    headers = example.find_element(By.CLASS_NAME, 'details').text
    files = list(x.get_attribute('href') for x in example.find_elements(By.CSS_SELECTOR,'[download]'))
    answer = find_answer(driver, example, ex_type)
    number = re.search(r'\d+', headers).group()
    hazard = define_level(headers)
    link = os.path.abspath("src\\common\\entities\\photos")
    body = example.find_element(By.CLASS_NAME, 'task-text')\
        .screenshot(link + f"\\{number}.png")
    if body:
        print('задание спаршено')
        return ex_type, number, hazard, os.getenv('SERVER_PHOTO_DIR_PATH') + f'/{number}.png', files, answer
    else:
        print('скриншот не сделан')
        