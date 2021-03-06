from selenium import webdriver

f = open("classObject.json", "w")

hak_year = '2018'
hak_term = ['1','2','summer','winter']
everything = '%C0%FC%C3%BC'
hakbu_list = ['0001', '0007', '0008', '0009', '0011', '0012', '0021', '0022', '0024', '0033', '0041', '0071', '0077', '0078', '0079', '0090']
base_url = 'http://hisnet.handong.edu/for_student/course/PLES330M.php'

driver = webdriver.Chrome('chromedriver')
driver.get("https://hisnet.handong.edu/login/login.php")

driver.find_element_by_name('id').send_keys('minglee68')
driver.find_element_by_name('password').send_keys('aa')

driver.find_element_by_xpath('//input[@src="/2012_images/intro/btn_login.gif"]').click()

for hakbu in hakbu_list:

    url_want = base_url + '?hak_year=' + hak_year + '&hak_term=' + hak_term[1] + '&hakbu=' + hakbu + '&isugbn=' + everything + '&injung=' + everything + '&eng=' + everything + '&prof_name=' + '&gwamok=' + '&gwamok_code=' + '&ksearch=search'
    driver.get(url_want)
    page = 2
    
    while True:
        table = driver.find_elements_by_xpath('//table[@id="att_list"]/tbody//tr//td')

        #table_data = [(x.text).encode('utf-8') for x in table]
        table_data = [(x.text) for x in table]


        classes = [];
        oneclass = {};
        count = 0
        totalcount = 0
        for data in table_data:
            if 0 <= count <= 16:
                if count == 1:
                    oneclass['class_code'] = data
                elif count == 2:
                    oneclass['section'] = data
                elif count == 3:
                    oneclass['class_name'] = data
                elif count == 5:
                    oneclass['prof_name'] = data
            
                if count == 16:
                    if totalcount != 0:
                        oneclass['department'] = hakbu
                        classes.append(oneclass.copy())
                    else:
                        totalcount = 1
                    count = 0
                else:
                    count = count + 1

        if len(classes) == 0:
            break
        else:
            for data in classes:
                #print(data)
                f.write(str(data) + '\n')
            print('-' * 30)
            url_page = url_want + '&Page=' + str(page)
            driver.get(url_page)
            page = page + 1

    print('*' * 30)

f.close()
driver.quit()
