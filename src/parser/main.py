from .storage import log_res
from .parser_core import *
from common.database.connection import connect_with_database
from .config import chrome_options



@connect_with_database
def main(server,sql_data):
    sftp, ssh = server
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get("https://kompege.ru/task")
        for i in  range(18, 19):
            open_page(driver, i)
            examples = WebDriverWait(driver,10)\
                .until(EC.presence_of_element_located((By.TAG_NAME, "table")))\
                .find_element(By.TAG_NAME, 'tbody')\
                .find_elements(By.CSS_SELECTOR, "tr[data-v-6d3ef279]:has(td.center > div.number)")
            for num in range(1,46):
                res = example_info(driver, examples[num], i+1 if i <= 18 else i+3)
                log_res(res, sftp, sql_data)
                sleep(1)

