import time
from selenium import webdriver

driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('http://hisnet.handong.edu/login/login.php');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('id')
search_box.send_keys('ChromeDriver')
time.sleep(5) # Let the user actually see something!
driver.quit()
