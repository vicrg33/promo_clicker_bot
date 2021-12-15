from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import numpy as np
from datetime import datetime
import os
import ntplib

###############################################################################################################
# NOTE: Next to the 0 and 59 minutes this script COULD get incorrect results, so do not use it at these moments
###############################################################################################################º

num_exec = 100
diff_vector = []
for ii in range(num_exec):
    # Start web browser (getting the profile that has Aliexpress logged in)
    options = Options()
    options.headless = True
    firefox_session = webdriver.FirefoxProfile('./firefox_profile/qj3gmn59.ali_bot_93')  # Firefox profile
    driver = webdriver.Firefox(firefox_session, options=options, service_log_path=os.devnull)
    
    # Go to the Aliexpress page with timer
    driver.get('https://es.aliexpress.com/campaign/wow/gcp/ae/channel/ae/accelerate/tupr?spm=a2g0o.home.Sale_mainvenue.1.39a670e5CB0Jdq&wh_weex=true&_immersiveMode=true&wx_navbar_hidden=true&wx_navbar_transparent=true&ignoreNavigationBar=true&wx_statusbar_hidden=true&wh_pid=ae%2Fmega%2Fae%2F2021_global_shopping_festival%2F1111mainvenue_2021&scm=1007.31960.250238.0&scm_id=1007.31960.250238.0&scm-url=1007.31960.250238.0&pvid=c75b44fd-67be-4598-a6d4-ecabf9262931')
    
    # Wait for the page to be charged
    time.sleep(7)
    
    # Assess execution time for datetime (not neccesary, it's 0...)
    # start_time = time.time()
    # xx = datetime.now()
    # end_time = time.time()
    # execution_time = start_time - end_time
    # print("Execution for datetime.now(): " + str(np.round(execution_time, 2)))
    
    # Retrieve the seconds from the timer and the current date to compare them when the seconds of the timer are 0
    while True:
        secs_units = driver.find_element_by_xpath(
            '//*[@id="2326793510"]/div/div/div/div/div[2]/div/div[4]/span[2]')
        secs_tens = driver.find_element_by_xpath(
            '//*[@id="2326793510"]/div/div/div/div/div[2]/div/div[4]/span[1]')
        # secs = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[3]/div/span[5]')
        current_date = datetime.now()  # Retrieve the current date just after the seconds to be as accurate as possible
    
        # Extract the text from the HTML elements
        secs_units = secs_units.text
        secs_tens = secs_tens.text
        # secs = secs.text

        # print("Seconds " + secs_tens + secs_units)
        # print("Seconds " + secs)

        # If the seconds are 0 (units and tens), break the loop
        if secs_units == '0' and secs_tens == '0':
            break
        # if secs == '00':
        #     break

    # Retrieve the minutes from the timer to compare them with the current time minutes
    mins_unit = driver.find_element_by_xpath(
            '//*[@id="2326793510"]/div/div/div/div/div[2]/div/div[3]/span[2]').text
    mins_tens = driver.find_element_by_xpath(
            '//*[@id="2326793510"]/div/div/div/div/div[2]/div/div[3]/span[1]').text
    # mins = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[3]/div/span[3]').text

    # "Convert" from timer to date
    minutes = 60 - int(mins_tens + mins_unit)
    # minutes = 60 - int(mins)

    # Differences between current time and Aliexpress timer
    if minutes == 60 and current_date.minute == 0:  # This loop account for the special case when the minutes from the timer
        # and from the current time are 0 (this provoke incorrect results, as the minutes from the timer will be converted
        # to 60 and those from the current time not)
        diff_mins = 0  # In this case, the difference should not be 1 hour but 0 minutes
    else:
        diff_mins = current_date.minute - minutes
    diff_seconds = current_date.second  # - 0, as the seconds from the timer are 0
    diff_useconds = current_date.microsecond  # - 0, as the seconds from the timer are (approximately) 0
    diff_total = diff_seconds + (diff_useconds * 10**-6) + 60 * diff_mins  # If the difference is <0 the timer is ahead of the real time, else (if >0)
    # it is behind it
    print("Total difference: " + str(diff_total))
    
    diff_vector.append(diff_total)
    
    driver.close()

print(np.mean(diff_vector))
