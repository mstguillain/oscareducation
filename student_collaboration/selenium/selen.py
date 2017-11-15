import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 1)
    return driver

def loginAdmin(driver, username, password):
    driver.get('http://localhost:8000/admin/login/?next=/admin/')
    try:
        userNameBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        pwdBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        userNameBox.send_keys(username)
        pwdBox.send_keys(password)
        
        pwdBox.submit()
    except Exception as ex:
        print("Could not connect : %s" % ex)

def logoutAdmin(driver):
    driver.get('http://localhost:8000/admin/logout')
    driver.get('http://localhost:8000')

def login(username, password):
    driver.get("http://localhost:8000/accounts/usernamelogin/")
    try:
        userNameBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        userNameBox.send_keys(username)
        userNameBox.submit()

        pwdBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        pwdBox.send_keys(password)
        pwdBox.submit()
    except Exception as ex:
        print("Could not connect : %s" % ex)
    
def logout(driver):
    driver.get('http://localhost:8000/accounts/logout')

def profAddClass(classname, inputValue):
    driver.get('http://localhost:8000/professor/lesson/add/')
    try:
        nameBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "name")))
        nameBox.send_keys(classname)
        
        radioButton = driver.wait.until(EC.presence_of_element_located((By.NAME, "stage")))
        
        #print(radioButton)
        #inpt = driver.wait.until(EC.presence_of_element_located((By.NAME, "stage")))
        #inpt = driver.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div[2]/ul[5]/li/div/label/input[@value='11']")))
        #print(inpt.text)
        #inpt.click()
        #print(r)
        #r.submit()
        #driver.execute_script("arguments[0].click();", r)
        #radioButton.submit()
        
        b = driver.execute_script("document.evaluate(\"/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div[2]/ul[5]/li/div/label\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()")
        radioButton.submit()
        
        
    except Exception as ex:
        print("Error : %s" % ex)

def profAddStudents(studentList):
    # actually max 2 type = [["firstname", "lastname"], [...]]
    #driver.get('http://localhost:8000/professor/lesson/5/student/add/')
    try:
        for i in range(len(studentList)):
            firstNameBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "first_name_%s" % i)))
            firstNameBox.send_keys(studentList[i][0])
            lastNameBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "last_name_%s" % i)))
            lastNameBox.send_keys(studentList[i][1])
        lastNameBox.submit()
    except Exception as ex:
        print("Error : %s" %ex)
        
if __name__ == "__main__":
    admin = "oscar02"
    adminPwd = "oscar02"
    driver = init_driver()
    loginAdmin(driver, admin, adminPwd)
    #time.sleep(2)
    logoutAdmin(driver)
    #time.sleep(2)
    login("prof02", "prof02")
    profAddClass("selenium02", 11)
    time.sleep(2)
    profAddStudents([["fnselen01", "lnselen01"], ["fnselen02", "lnselen02"]])
    #time.sleep(2)
    
    #logout(driver)
    #time.sleep(2)
    #driver.close()
    # driver.quit()
