from selenium.webdriver.chrome.options import Options


chrome_options  = Options()
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--log-level=1')


fieldnames = ['number', 'type', 'difficulty', 'file_path', 'file_links', 'answer', 'date_create']
