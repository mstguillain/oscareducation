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

def addValByName(val, name, submit=False):
    try:
        box = driver.wait.until(EC.presence_of_element_located((By.NAME, name)))
        box.send_keys(val)
        if submit:
            box.submit()
    except Exception as ex:
        print(ex)

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

def login(username, password, student=True):
    driver.get("http://localhost:8000/accounts/usernamelogin/")
    try:
        userNameBox = driver.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        userNameBox.send_keys(username)
        userNameBox.submit()

        if student:
            byVal = "code"
        else:
            byVal = "password"
        pwdBox = driver.wait.until(EC.presence_of_element_located((By.NAME, byVal)))
        pwdBox.send_keys(password)
        pwdBox.submit()
    except Exception as ex:
        print("Could not connect : %s" % ex)
    
def logout():
    driver.get('http://localhost:8000/accounts/logout')

def profAddClass(classname):
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

def profGetClass(classId):
    driver.get('http://localhost:8000/professor/lesson/%s/' % classId)
        
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
        
# students_password_page
def getStudentsPassword():
    driver.get(driver.current_url + "students_password_page")
    table = driver.find_elements_by_xpath("/html/body/table")
    studentList = table[0].text.split()
    studentDict = {}
    for i in range(len(studentList)//8):
        studentDict[studentList[i*8].decode() + " " + studentList[1 + i*8].decode()] = [studentList[4 + i*8].decode(), studentList[7 + i*8].decode()]
    return studentDict

def addPassword(pwd):
    addValByName(pwd, "password")
    addValByName(pwd, "confirmed_password", submit=True)

if __name__ == "__main__":
    admin = "oscar02"
    adminPwd = "oscar02"
    studentList = [["fnselen11", "lnselen11"], ["fnselen22", "lnselen22"]]
    driver = init_driver()
    #loginAdmin(driver, admin, adminPwd)
    #logoutAdmin(driver)
    login("prof02", "prof02", student=False)
    #profAddClass("selenium03")
    profGetClass(29)
    #profAddStudents(studentList)
    stPwdDict = getStudentsPassword()
    logout()
    for student in stPwdDict.keys():
        print(stPwdDict[student][0] + " " + str(stPwdDict[student][1]))
        login(stPwdDict[student][0], str(stPwdDict[student][1]))
        if "http://localhost:8000/accounts/createpassword/" == driver.current_url:
            addPassword(student)
        time.sleep(3)
        logout()
    
    #logout(driver)
    #driver.close()
    # driver.quit()
