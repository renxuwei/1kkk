import re
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO

from compare_helper import *




browser = webdriver.Chrome()
browser.set_window_size(1400, 700)
# 显式等待 针对某个节点的等待
wait = WebDriverWait(browser, 5)


def get_page():
    url = 'http://www.1kkk.com/'
    browser.get(url)
    html = browser.page_source
    return browser


# 点击登录按钮
def get_position(html):
    html_etree = etree.HTML(html)
    login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.header-avatar')))
    time.sleep(1)
    login.click()
    # 获取大图url
    da_image = html_etree.xpath('//div[@class="rotate-background"]/@style')
    image_all = da_image[0]
    image_url = image_all.split('("')[1]
    image = image_url.split('")')[0]
    urll = image.split('=')[0]
    print(urll)

    # 组装url
    url = 'http://www.1kkk.com/' + urll + '=' + str(time.time()).split('.')[0]
    print(url)

    filename_list = []
    # 请求300次
    for _ in range(300):
        response = requests.get(url)
        filename = str(time.time()).split('.')[-1] + '.png'
        filename_list.append(filename)
        # 保存300张大图到本地
        with open('./images/%s' % filename, 'wb') as f:
            f.write(response.content)

    return filename_list

# 剪切大图为四个小图片
def jian_image(filename_list):
    xiao_img_list = []
    for name_list in filename_list:
        name = './images/' + name_list
        screenshot = Image.open(name)
        image1 = screenshot.crop((0, 0, 76, 76))
        image2 = screenshot.crop((76, 0, 152, 76))
        image3 = screenshot.crop((152, 0, 228, 76))
        image4 = screenshot.crop((228, 0, 304, 76))
        #name1 = str(time.time()).split('.')[-1] + '1' + '.png'
        #time.sleep(0.025)
        xiao_img_list.append(name_list)
        name2 = str(time.time()).split('.')[-1] + '2' + '.png'
        #time.sleep(0.023)
        xiao_img_list.append(name2)
        name3 = str(time.time()).split('.')[-1] + '3' + '.png'
        #time.sleep(0.021)
        xiao_img_list.append(name3)
        name4 = str(time.time()).split('.')[-1] + '4' + '.png'
        xiao_img_list.append(name4)
        image1.save('./images/' + name_list)
        image2.save('./images/' + name2)
        image3.save('./images/' + name3)
        image4.save('./images/' + name4)
    print(xiao_img_list)
    return xiao_img_list
# ==========================================

# 去重,匹配相似度，大于80就删除相似的图片
def qu_chong():
    for list1 in os.listdir('./images/'):
        # 如果list1存在于 文件路径中os.listdir('./images/')
        if list1 in os.listdir('./images/'):
            filename1 = './images/' + list1
            num1 = os.listdir('./images/').index(list1)

            # 四次翻转，分别去匹配
            for i in range(4):
                print('...........' + str(i))
                xuan_pil(filename1)

                for list2 in os.listdir('./images/'):
                    # 如果list2存在于 文件路径中os.listdir('./images/')
                    if list2 in os.listdir('./images/'):
                        num2 = os.listdir('./images/').index(list2)
                        # 拿num1后面的图片num2进行匹配
                        if num1 < num2:
                            filename2 = './images/' + list2
                            # 灰度匹配
                            compare = get_compare(filename1, filename2)
                            # 如果大于80就删除图片
                            print(compare)
                            if compare >= 80:
                                os.remove(filename2)
                                print(list2, compare)

# 图片90旋转
def xuan_pil(filename1):
    # 读取图像
    img = Image.open(filename1)
    # 显示图片
    # img.show()
    # 指定逆时针旋转的角度
    im_rotate = img.rotate(90)
    # 显示图片
    # im_rotate.show()
# =======================================
# 取浏览器窗口内全图
def get_big_image():
    browser.execute_script('window.scrollTo(0, 0)')
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


def get_page_qu(html):
    # #html_etree = etree.HTML(html)
    # login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.header-avatar')))
    # time.sleep(1)
    # login.click()

    # 暂停1s截取窗口
    time.sleep(2)
    screenshot = get_big_image()
    screenshot.save('./image/' + str(time.time()).split('.')[-1] + '.png')
    # 获取下图坐标
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
    loc = img.location
    # size = img.size
    # print(loc)
    # print(size)
# 第一张图截取、配比
    crop_image1 = screenshot.crop((loc['x'], loc['y'], loc['x'] + 76, loc['y'] + 76))
    file_name = './image/' + str(time.time()).split('.')[-1] + '.png'
    crop_image1.save(file_name)

# 第二张图截取、配比
    crop_image2 = screenshot.crop((loc['x'] + 78, loc['y'], loc['x'] + 154, loc['y'] + 76))
    file_name2 = './image/' + str(time.time()).split('.')[-1] + '.png'
    crop_image2.save(file_name2)

# 第三张图截取、配比
    crop_image3 = screenshot.crop((loc['x'] + 156, loc['y'], loc['x'] + 232, loc['y'] + 76))
    file_name3 = './image/' + str(time.time()).split('.')[-1] + '.png'
    crop_image3.save(file_name3)

# 第四张图截取、配比
    crop_image4 = screenshot.crop((loc['x'] + 234, loc['y'], loc['x'] + 310, loc['y'] + 76))
    file_name4 = './image/' + str(time.time()).split('.')[-1] + '.png'
    crop_image4.save(file_name4)

    # 第一张图配比
    list1 = []
    i = 1
    while i < 6:
        i += 1
        for image in os.listdir('./images/'):
            h_ima = './images/' + image
            compare = get_compare(file_name, h_ima)
            if compare >= 85:
                i = 6
                print('*** 1 ok ok ok ***')
                break
        list1.append(compare)
        if compare < 85:
            dian_imgs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rotate-background')))[0]
            dian_imgs.click()
            # 暂停2s截取窗口
            time.sleep(1)
            screenshot1 = get_big_image()
            screenshot1.save('./image/' + str(time.time()).split('.')[-1] + '.png')

            dian_imgl = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
            dian_loc = dian_imgl.location

            dian_crop = screenshot1.crop((dian_loc['x'], dian_loc['y'], dian_loc['x'] + 76, dian_loc['y'] + 76))
            dian_file_name = './image/' + str(time.time()).split('.')[-1] + '.png'
            dian_crop.save(dian_file_name)
            file_name = dian_file_name

    if list1[-1] < 85:
        print('...第一个无法配比，点击下一组，再次进行配比...')
        return True

    # 第二张图配比
    list2 = []
    i2 = 1
    while i2 < 6:
        for image2 in os.listdir('./images/'):
            h_ima2 = './images/' + image2
            compare2 = get_compare(file_name2, h_ima2)
            if compare2 >= 85:
                i2 = 6
                print('*** 2 ok ok ok ***')
                break
        list2.append(compare2)
        if compare2 < 85:
            dian_imgs2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rotate-background')))[1]
            dian_imgs2.click()
            # 暂停2s截取窗口
            time.sleep(1)
            screenshot2 = get_big_image()
            screenshot2.save('./image/' + str(time.time()).split('.')[-1] + '.png')

            dian_img2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
            dian_loc2 = dian_img2.location

            dian_crop2 = screenshot2.crop((dian_loc2['x']+78, dian_loc2['y'], dian_loc2['x'] + 154, dian_loc2['y'] + 76))
            dian_file_name2 = './image/' + str(time.time()).split('.')[-1] + '.png'
            dian_crop2.save(dian_file_name2)
            file_name2 = dian_file_name2
        i2 += 1
    if list2[-1] < 85:
        print('...第二个无法配比，点击下一组，再次进行配比...')
        return True

    # 第三张图配比
    list3 = []
    i3 = 1
    while i3 < 6:
        for image3 in os.listdir('./images/'):
            h_ima3 = './images/' + image3
            compare3 = get_compare(file_name3, h_ima3)
            if compare3 >= 85:
                i3 = 6
                print('*** 3 ok ok ok ***')
                break
        list3.append(compare3)
        if compare3 < 85:
            dian_imgs3 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rotate-background')))[2]
            dian_imgs3.click()
            # 暂停2s截取窗口
            time.sleep(1)
            screenshot3 = get_big_image()
            screenshot3.save('./image/' + str(time.time()).split('.')[-1] + '.png')

            dian_img3 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
            dian_loc3 = dian_img3.location

            dian_crop3 = screenshot3.crop((dian_loc3['x']+156, dian_loc3['y'], dian_loc3['x'] + 232, dian_loc3['y'] + 76))
            dian_file_name3 = './image/' + str(time.time()).split('.')[-1] + '.png'
            dian_crop3.save(dian_file_name3)
            file_name3 = dian_file_name3
        i3 += 1
    if list3[-1] < 85:
        print('...第三个无法配比，点击下一组，再次进行配比...')
        return True

    # 第四张截取、配比
    list4 = []
    i4 = 1
    while i4 < 6:
        for image4 in os.listdir('./images/'):
            h_ima4 = './images/' + image4
            compare4 = get_compare(file_name4, h_ima4)
            if compare4 >= 85:
                i4 = 6
                print('*** 4 ok ok ok ***')
                break
        list4.append(compare4)
        if compare4 < 85:
            dian_imgs4 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rotate-background')))[3]
            dian_imgs4.click()
            # 暂停2s截取窗口
            time.sleep(1)
            screenshot4 = get_big_image()
            screenshot4.save('./image/' + str(time.time()).split('.')[-1] + '.png')

            dian_img4 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
            dian_loc4 = dian_img4.location

            dian_crop4 = screenshot4.crop((dian_loc4['x']+234, dian_loc4['y'], dian_loc4['x'] + 310, dian_loc4['y'] + 76))
            dian_file_name4 = './image/' + str(time.time()).split('.')[-1] + '.png'
            dian_crop4.save(dian_file_name4)
            file_name4 = dian_file_name4
        i4 += 1
    if list4[-1] < 85:
        print('...第四个无法配比，点击下一组，再次进行配比...')
        return True


    return False



def main():
    html = get_page()
    # filename_list = get_position(html)
    # xiao_img_list = jian_image(filename_list)
    # qu_chong(xiao_img_list)     # 去重1
    # qu_chong()     # 去重2
    # 获取页面
    # html_etree = etree.HTML(html)

    # 点击首页登陆按钮
    login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.header-avatar')))
    time.sleep(1)
    login.click()
    num = get_page_qu(html)
    # 如果没有匹配上，就点击 ‘换一组’ 继续从头匹配
    while num:
        huan_yi_zu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-refresh')))
        huan_yi_zu.click()
        time.sleep(2)
        num = get_page_qu(html)



if __name__ == '__main__':
    main()
