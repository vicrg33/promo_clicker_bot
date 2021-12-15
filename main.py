from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import pause
from datetime import datetime
import time

#########################################################################
# NOTE: Check all 'xpaths' before the execution, all of them could change
# NOTE: Aliexpress timer is not synched with "regular" hours
#########################################################################

# Coupon code
coupon = 'SBD16'

# Before start the execution, assess the difference between timer and current time with 'timer_sync', and add it to
# these values. If the difference is positive, add the difference to the values below, if is negative subtract it (i.e.
# a '+' sign will make it)
year = 2021
month = 12
day = 15
hour = 16
minute = 00
second = 00
usecond = 000000 - 100000  # Always subtract 100000 useconds to account the execution time
# Avoid negative values by formatting the dates properly
if usecond < 0:
    second = second - 1
    usecond = usecond + 1000000
    if second < 0:
        minute = minute - 1
        second = second + 60
        if minute < 0:
            hour = hour - 1
            minute = minute + 60
            if hour < 0:
                day = day - 1
                hour = hour + 24

# Subtract the difference between timer and current time
second = second
usecond = usecond - 850000
# Avoid negative values by formatting the dates properly
if usecond < 0:
    second = second - 1
    usecond = usecond + 1000000
    if second < 0:
        minute = minute - 1
        second = second + 60
        if minute < 0:
            hour = hour - 1
            minute = minute + 60
            if hour < 0:
                day = day - 1
                hour = hour + 24

####### TO INITIATE THE SCRIPT A FEW MINUTES BEFORE THE PROMO STARTS
if (minute - 10) < 0:
    hour_big_wait = hour - 1
    minute_big_wait = minute - 10 + 60
    if hour_big_wait < 0:
        day_big_wait = day - 1
        hour_big_wait = hour_big_wait - 1 + 24
    else:
        day_big_wait = day
else:
    day_big_wait = day
    hour_big_wait = hour
    minute_big_wait = minute - 10
pause.until(datetime(year, month, day_big_wait, hour_big_wait, minute_big_wait, second, usecond))

# Start web browser (getting the profile that has Aliexpress logged in)
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("user-data-dir=D:\OneDrive - gib.tel.uva.es\Personal\Scripts Utiles\promo_clicker_bot/tmp")
service = Service('chromedriver.exe', log_path=os.devnull)
driver = webdriver.Chrome(options=options, service=service)

# Go to the Aliexpress shopping bag
driver.get('https://shoppingcart.aliexpress.com/shopcart/shopcartDetail.htm?spm=a2g0o.home.1000002.2.39a670e5WR9V62')

#################### PRESS THE BUTTON BUY
## FIRST WAY OF PRESSING THE BUTTON BUY - MANUALLY
# Wait until the product has been selected and the button "Buy" has been clicked. Afterwards, press any key on the
# Python console
# input()
## SECOND WAY OF PRESSING THE BUTTON BUY - AUTOMATICALLY VIA SHOPPING CART
time.sleep(20)
driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div[1]/div[1]/div[3]/div/div/div/div[1]/div/label/span/input').click()
time.sleep(5)
driver.find_element(By.ID, 'checkout-button').click()
time.sleep(25)
## THIRD  WAY OF PRESSING THE BUTTON BUY - AUTOMATICALLY VIA "BUY" IN THE ARTICLE
# time.sleep(20)
# driver.get('https://es.aliexpress.com/item/4001020086621.html?spm=a2g0o.superdeal.slashprice.item01')
# time.sleep(25)
# # driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/div/div[2]/div[8]/div/div/ul/li[2]/div/img').click()
# # time.sleep(20)
# driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div[2]/div[13]/span[1]/button').click()
# time.sleep(25)

# The coupon to be introduced
driver.find_element(By.ID, "code").send_keys(coupon)

# Pause until the promo specific time arrives
pause.until(datetime(year, month, day, hour, minute, second, usecond))

# When the promo hour arrives, apply the coupon
driver.find_element(By.XPATH,
    '//*[@id="price"]/div[3]/div/form/div[2]/div/button').click()
# ii = 0  # Counter for debugging, it measure how much tries it has taken to get the element where the price is placed

# Wait for the coupon to be applied. To do that, wait until the "Buy" button is available (visible and enabled)
## THIS METHOD IS NOT WORKING BECAUSE A DIV APPEARS, AND THE METHOD .click() RETURNS AN ERROR
# max_wait = 30
# element = WebDriverWait(driver, max_wait).until(EC.invisibility_of_element((By.XPATH, '//*[@id="price-overview"]/div[1]')))
# # The above line wait until the button is available with a maximum of 'max_wait' seconds waiting
# element.click()  # Uncomment this line only for the final execution, otherwise the script will buy the product

# Another way of waiting for the coupon to be applied. To do that, try to retrieve the element where the price is
# placed, suposing that when it is available the coupon has been already applied
## WORKING? BUT LESS ACCURATE THAT THE NEXT ONE
# ii = 0  # Counter for debugging, it measure how much tries it has taken to get the element where the price is placed
# while True:
#     try:  # If success, press "Buy"
#         price = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div[5]')
#         # The xpath above may change more than the others, so be careful and check it again before the final execution,
#         # as it has ruined some executions in the past
#         element = driver.find_element_by_xpath('//*[@id="checkout-button"]')  # .click() Put .click() at the end only
#         # for the final execution, otherwise the script will buy the product
#         break
#     except:  # Otherwise, try again
#         ii = ii + 1
#         pass

# Other way of waiting for the code to be applied. Try to click until it do not return an error
## THE BEST ALTERNATIVE. USE THIS
ii = 0  # Counter for debugging, it measure how much tries it has taken to get the element where the price is placed
while True:
    try:
        element = driver.find_element(By.ID, 'checkout-button').click()  # Put .click() at the end only for the final
        # execution, otherwise the script will buy the product
        break
    except:
        ii = ii + 1
        pass

# The last way of waiting for the code to be applied. Working but very VERY few accurate
## THIS APPROACH WILL WORK BUT IT IS VERY TEMPORARY INEFFECTIVE
# time.sleep(20)  # Waiting time (in seconds) for the coupon to be applied
# element = driver.find_element_by_id('checkout-button').click()

# Check how much time it has taken to apply the coupon and press buy. For debugging only
time_now = datetime.now()
time_now = time_now.strftime("%H:%M:%S:%f")
print("Current Time = " + time_now)
print("Number of iterations " + str(ii))
