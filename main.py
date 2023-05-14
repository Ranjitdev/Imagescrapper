from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
from urllib import request
from mongo_update import save_in_mongo

#defining the search char

q = str(input('Type the name you want to download photos of : ')).capitalize()
#defining the no of pic to save
image_need = int(input('Type how many images you want : '))
search_url = f'https://www.google.com/search?q={q}&sa=X&source=lnms&tbm=isch'
driver_path = r'C:\Users\RANJIT PC\Python Files\PYcharm\ImageScrapper\chromedriver.exe'
driver = wd.Chrome(service=Service(driver_path))
img_folder = r'C:\Users\RANJIT PC\Python Files\PYcharm\ImageScrapper\images'
save_path = os.path.join(img_folder, q)


def scroll():
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    except:
        raise Exception('Scroll Error : Interrupted')

def show_images(url):
    try:
        driver.get(url)
    except:
        pass


def save_image(url, path, counter):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        request.urlretrieve(str(url), f"{path}/{counter}.jpg")
        print(f'Saved successfully {counter+1}.jpg')
        time.sleep(0.5)
    except Exception as e:
        print(e)


def fetch_image_urls(search_url,no_of_images):
    driver.get(search_url)
    image_urls = []
    image_count = 0
    loop_count = 0

    while image_count < no_of_images:
        scroll()

        thumbnails = driver.find_elements(By.CLASS_NAME, 'Q4LuWd')
        fetched = len(thumbnails)

        for actual_url in thumbnails[image_count : fetched]:
            try:
                actual_url.click()
                time.sleep(0.5)
                if driver.find_element(By.CLASS_NAME, 'r48jcc').get_attribute('src') and 'https':
                    image_urls.append(driver.find_element(By.CLASS_NAME, 'r48jcc').get_attribute('src'))
                    image_count += 1
                    loop_count += 1
                    print('Reading Image no.',image_count)
            except Exception as e:
                continue
        if loop_count<no_of_images:
            loop_count=0
            if image_count >= no_of_images:
                break

    for i in  range(no_of_images):
        show_images(image_urls[i])
        save_image(image_urls[i], save_path , i)
    driver.close()
    check = save_in_mongo(q, img_folder, image_need).check()
    save = input(f'{check} Type y/n : ')
    if save.capitalize() == 'Y':
        save_in_mongo(q, img_folder, image_need).save()
    show = input('Do you want to show the images saved Type y/n : ')
    if show.capitalize() == 'Y':
        save_in_mongo(q, img_folder, image_need).show()



fetch_image_urls(search_url,image_need)