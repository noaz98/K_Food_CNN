from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

def extract_insta_data(login_option, user_id, user_passwd, wish_num, keyword, driver_path, save_path):  # 추출

    save_file_name = "instagram_extract"

    instagram_id_name = "username"
    instagram_pw_name = "password"
    instagram_login_btn = ".sqdOP.L3NKy.y3zKF"

    facebook_login_page_css = ".sqdOP.L3NKy.y3zKF"
    facebook_login_page_css2 = ".sqdOP.yWX7d.y3zKF"
    facebook_id_form_name = "email"
    facebook_pw_form_name = "pass"
    facebook_login_btn_name = "login"

    first_img_css = "div._ac7v._aang > div._aabd._aa8k._aanf"
    location_object_css = "div._aaqm > div._aacl._aacn._aacu._aacy._aada._aade > a"
    upload_id_object_css = "div._ab8w._ab94._ab97._ab9f._ab9k._ab9p._abcm > div._aacl._aaco._aacw._aacx._aad6._aade > span._aap6._aap7._aap8"
    date_object_css = "div._aacl._aacm._aacu._aacy._aad6 > time._aaqe"
    main_text_object_css = "div._a9zr > div._a9zs > span._aacl._aaco._aacu._aacx._aad7._aade"

    print_flag = True
    next_arrow_btn_css1 = "div._aear > div._aaqg._aaqh > button._abl-"

    driver = webdriver.Chrome(driver_path)

    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)
    time.sleep(7)

    is_login_success = False

    if login_option == "instagram":
        try:
            instagram_id_form = driver.find_element(By.NAME, instagram_id_name)
            instagram_id_form.send_keys(user_id)
            time.sleep(7)

            instagram_pw_form = driver.find_element(By.NAME, instagram_pw_name)
            instagram_pw_form.send_keys(user_passwd)
            time.sleep(7)

            login_ok_button = driver.find_element(
                By.CSS_SELECTOR, instagram_login_btn)

            login_ok_button.click()
            is_login_success = True
        except:
            print("instagram login fail")
            is_login_success = False

        time.sleep(10)
    elif login_option == "facebook":
        is_facebook_btn_click = False
        try:

            facebook_login_btn = driver.find_element(
                By.CSS_SELECTOR, facebook_login_page_css)
            time.sleep(7)
            facebook_login_btn.click()
            is_facebook_btn_click = True
            is_login_success = True
        except:
            print("click facebook login button 1 fail")
            is_facebook_btn_click = False
            is_login_success = False

        time.sleep(10)

        if not is_facebook_btn_click:

            try:
                facebook_login_btn = driver.find_element(
                    By.CSS_SELECTOR, facebook_login_page_css2)
                time.sleep(7)
                facebook_login_btn.click()
                is_facebook_btn_click = True
                is_login_success = True
            except:
                print("click facebook login button 2 fail")
                is_login_success = False

        time.sleep(10)

        if is_facebook_btn_click:
            id_input_form = driver.find_element(By.NAME, facebook_id_form_name)
            time.sleep(7)
            id_input_form.send_keys(user_id)

            time.sleep(7)

            pw_input_form = driver.find_element(By.NAME, facebook_pw_form_name)
            time.sleep(7)
            pw_input_form.send_keys(user_passwd)

            time.sleep(7)

            login_btn = driver.find_element(By.NAME, facebook_login_btn_name)
            time.sleep(7)
            login_btn.click()
        time.sleep(7)

    if is_login_success:
        url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

        instagram_tags = []
        instagram_tag_dates = []

        driver.get(url)
        time.sleep(7)

        # 첫번째 게시물
        driver.find_element(By.CSS_SELECTOR, first_img_css).click()

        # data lists

        location_hrefs = []
        upload_ids = []
        date_titles = []
        main_texts = []

        check_arrow = True

        count_extract = 0

        while True:

            if count_extract >= wish_num:  # check num
                driver.close()
                driver.quit()
                break
            time.sleep(7)

            if check_arrow == False:
                break

            #href
            try:

                location_href = driver.current_url
            except:

                location_href = None

            # 올린사람 ID
            try:
                upload_id_object = driver.find_element(
                    By.CSS_SELECTOR, upload_id_object_css)
                upload_id = upload_id_object.text
            except:
                upload_id = None

            # 날짜
            try:
                date_object = driver.find_element(
                    By.CSS_SELECTOR, date_object_css)
                date_title = date_object.get_attribute("title")
            except:

                date_title = None

            # 본문
            try:
                main_text_object = driver.find_element(
                    By.CSS_SELECTOR, main_text_object_css)
                main_text = main_text_object.text
            except:
                main_text = None

            location_hrefs.append(location_href)
            upload_ids.append(upload_id)
            date_titles.append(date_title)
            main_texts.append(main_text)

            try:
                WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, next_arrow_btn_css1)))
                time.sleep(3)
                next_arrow_btn = driver.find_element(
                    By.CSS_SELECTOR, next_arrow_btn_css1)
                next_arrow_btn.send_keys(Keys.ENTER)

            except:
                check_arrow = False

            count_extract += 1

        #datafram and save
        try:
            insta_info_df = pd.DataFrame(
                {"location_href": location_hrefs, "upload_id": upload_ids, "date_title": date_titles, "main_text": main_texts})
            insta_info_df.to_csv(
                "{}/{}.csv".format(save_path, save_file_name), index=False)
        except:
            print("fail to save data")

    #login failed
    elif not is_login_success:
        print(f"login {login_option} fail")
