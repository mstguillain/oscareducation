import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import re

BASE_URL = "http://127.0.0.1:8000/"
ADMIN_PSEUDO = "root"
ADMIN_PASSWORD = "root"
TEACHER_PSEUDO = "TestTeacher"
TEACHER_PASSWORD = "test"
CLASS_NAME = "testClass"
STUDENTS = (
	("fnselen11", "lnselen11"),
	("fnselen22", "lnselen22")
)

STUDENTS_SKILLS = (
	("P3D-U3-T2",),
	()
)


class Selenium:
	TIMEOUT_BUTTON_WAIT = 15
	def __init__(self):
		self.__initDriver()

	def __initDriver(self):
		""" See readme file for more explication if trouble to install """
		if os.name == "nt":  # if it is a windows platform
			self.driver = webdriver.Chrome(r"chromedriver.exe")
		else:
			self.driver = webdriver.Chrome()
		self.driver.wait = WebDriverWait(self.driver, 1)


	def test(self):
		""" All tests """
		#self.__testFunction(self.logInAdmin, ADMIN_PSEUDO, ADMIN_PASSWORD)
		#self.__testFunction(self.logOutAdmin)

		self.__testFunction(self.logInTeacher, TEACHER_PSEUDO, TEACHER_PASSWORD)
		self.__testFunction(self.addClass, CLASS_NAME)
		self.__testFunction(self.addStudents, STUDENTS)
		self.__testFunction(self.setSkillsToStudent, STUDENTS_SKILLS)


	def __testFunction(self, fun, *args):
		""" Test a given function on the given arguements"""
		functionName = fun.im_func.__name__
		print("Testing "+functionName+" with "+str(args)+" : ")
		try:
			fun(*args)
			print("\tOK")
		except TimeoutException as tex:
			print("\tERROR (Timeout) : "+ str(tex.args) +" One of the demanded ressource took to much time to be found. It's likely that it didn't existed or the page wasn't loaded/redirected as expected")
		except WebDriverException as wex:
			print("\tError (WebDriver) : ") + str(wex.args) + " The content have not beel loaded yet (need to call wait method)"
		except Exception as ex:
			print "\tERROR: " + str(ex.args)
		except BaseException as e:
			print "\tERROR: " + str(e.args)

	def __waitElementByName(self, name):
		return self.driver.wait.until(EC.presence_of_element_located((By.NAME, name)))

	def __waitElementByXPath(self, xPath):
		return self.driver.wait.until(EC.presence_of_element_located((By.XPATH, xPath)))

	def __fillBoxSubmit(self, name, text):
		box = self.__fillBox(name, text)
		box.submit()

	def __fillBox(self, name, text):
		box = self.__waitElementByName(name)
		box.send_keys(text)
		return box

	def __clickButtonByXPath(self, xPath):
		button = WebDriverWait(self.driver, self.TIMEOUT_BUTTON_WAIT).until(EC.element_to_be_clickable((By.XPATH, xPath)))
		actions = ActionChains(self.driver)
		actions.click(button).perform()

	def __testURL(self, lastURL, *exceptionArgs):
		""" Test si l'url match l'URL courante """
		if not re.compile(BASE_URL + lastURL).match(self.driver.current_url):
			raise BaseException(*exceptionArgs)

	## Tests Methods ##

	def logInAdmin(self, adminPseudo, adminPassword):
		""" We consider that the given credentials already exists"""
		self.driver.get(BASE_URL+'admin/login/?next=/admin/')

		userNameBox = self.__waitElementByName("username")
		userNameBox.send_keys(adminPseudo)

		self.__fillBoxSubmit("password", adminPassword)

		self.__testURL("admin/", r"Admin page wasn't loaded", r"Are you sure that the superuser username and password given are corrects?")

	def logOutAdmin(self):
		self.driver.get(BASE_URL+'admin/logout')
		# If we were not connected we will be redirected, so it's not always true
		self.__testURL("admin/logout/", r"Can't logout admin session", r"Are you sure that you were logged in as a super user?")

	def logInTeacher(self, teacherPseudo, teacherPassword):
		""" We consider that the teacher already exists """
		self.driver.get(BASE_URL+"accounts/usernamelogin")
		# First enter the log in
		self.__fillBoxSubmit("username", teacherPseudo)
		self.__testURL("accounts/passwordlogin/", r"The username passwords didn't show up", r"Are you sure that this username aws created ?")
		# As a teacher the tag is "password" "code" for students
		self.__fillBoxSubmit("password", teacherPassword)
		self.__testURL("professor/dashboard/", r"Teacher have not be logged in sucessfully", "Are you sure that this teacher existed ?")


	def logOutUser(self):
		""" LogOut for both user and teacher"""
		self.driver.get(BASE_URL+'accounts/logout')
		# Nothing to check as it redirect us to homepage wherever we were previously connected or not

	def addClass(self, className):
		""" We consider that a teacher is currently logged in """
		self.driver.get(BASE_URL+'professor/lesson/add/')
		self.__fillBox("name", className)

		radioButton = self.__waitElementByName("stage")
		# Add a 6th year "enseignement professionnel (3e degre)"
		self.driver.execute_script(
			"document.evaluate(\"/html/body/div[2]/div[2]/div/div[2]/form/div[2]/div[2]/div[2]/ul[5]/li/div/label\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()")
		radioButton.submit()
		# Logically it contains with a regex but we skip this part
		self.__testURL("professor/lesson/[0-9]*/student/add/", "The add student page wasn't loaded sucessfully after adding the class")

	def addStudents(self, studentList):
		""" We consider that we are in the add student class page """

		# Watch out that on this page there is only 2 student that could be added
		# We can add extra student by clicking the +1 button, so we fake it
		for i in range(0, len(studentList)-2):
			xPathToAddOneStudent = '/html/body/div[2]/div[2]/div[6]/form/ul/li['+str(3+i)+']/button[1]'
			self.__clickButtonByXPath(xPathToAddOneStudent)

		# Fill the student form
		for i in range(len(studentList)):
			self.__fillBox("first_name_" + str(i), studentList[i][0])
			self.__fillBox("last_name_" + str(i), studentList[i][1])

		xPathSubmit = "/html/body/div[2]/div[2]/div[6]/form/div/button"
		self.__waitElementByXPath(xPathSubmit).submit()

		self.__testURL("professor/lesson/[0-9]*/", "You have not been redirected to the class dashboard")

	def setSkillsToStudent(self, studentSkillsList):
		""" We consider that we are on lesson dashboard """
		saveUrl = self.driver.current_url
		# if we get the id of the first created student then it's easy to find the other one (just +1)
		xPathFirstTableEntry = '//*[@id="students"]/div[4]/div/table/tbody/tr[1]/td[1]/a'
		entry = self.__waitElementByXPath(xPathFirstTableEntry)#self.driver.find_element_by_xpath(xPathFirstTableEntry)
		print entry.get_attribute("href")


"""
def addValByName(val, name, submit=False):
	try:
		box = driver.wait.until(EC.presence_of_element_located((By.NAME, name)))
		box.clear()
		box.send_keys(val)
		if submit:
			box.submit()
	except Exception as ex:
		print(ex)


def findElemByValue(elem, val):
	print(elem)
	print(val)
	print("//" + elem + "[contains(text(), " + val + ")]")
	eList = driver.find_elements_by_xpath("//" + elem + "[contains(text(), " + val + ")]")  # doesn't work correctly
	for e in eList:
		print(e.text)
		if val.lower() in e.text.lower():
			return e
	print("Couldn't find the value '%s'" % val)


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
"""

def profSetSkill(classId, studentName):
	driver.get('http://localhost:8000/professor/lesson/%s/' % classId)
	# table = driver.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div[4]/div/table/tbody")
	driver.find_elements_by_xpath("//a[contains(text(), " + studentName + ")]")

	# driver.get('/professor/lesson/%s/skill/%s/' % (classId, skillCode))


def profGetClass(className):
	driver.get("http://localhost:8000/professor/dashboard/")
	classA = findElemByValue("a", className)
	classA.click()



def addSkillToStudent(student, skillCode):
	studentElem = findElemByValue("a", student.split()[0].lower())
	studentElem.click()
	driver.get(driver.current_url[:-1] + "#heatmap")
	studentElem = findElemByValue("abbr", skillCode)
	print(type(studentElem))
	print(studentElem)
	print(studentElem.text)

	# studentElem.submit()
	# studentElem.click()


# students_password_page
def getStudentsPassword():
	driver.get(driver.current_url + "students_password_page")
	table = driver.find_elements_by_xpath("/html/body/table")
	studentList = table[0].text.split()
	studentDict = {}
	for i in range(len(studentList) // 8):
		studentDict[studentList[1 + i * 8].decode() + " " + studentList[i * 8].decode()] = [
			studentList[4 + i * 8].decode(), studentList[7 + i * 8].decode()]
	return studentDict


def addPassword(pwd):
	addValByName(pwd, "password")
	addValByName(pwd, "confirmed_password", submit=True)

if __name__ == '__main__':
	selenium = Selenium()
	selenium.test()


if False:
	admin = "root"
	adminPwd = "root"
	#classId = 29
	skillCode = "P3D-U3-T2"
	studentList = [["fnselen11", "lnselen11"], ["fnselen22", "lnselen22"]]
	driver = init_driver()
	# loginAdmin(driver, admin, adminPwd)
	# logoutAdmin(driver)
	login("prof02", "prof02", student=False)
	# profAddClass("selenium03")
	profGetClass("selenium03")
	stPwdDict = getStudentsPassword()
	# print(stPwdDict)
	# profGetClass("selenium03")
	# addSkillToStudent(stPwdDict.keys()[0], skillCode)
	# time.sleep(8)

	# profGetClass("selenium03")
	# addSkillToStudent(stPwdDict.keys()[1], skillCode)
	# time.sleep(8)



	# profAddStudents(studentList)
	# profSetSkill(classId, skillCode)

	logout()
	for student in stPwdDict.keys():
		print(stPwdDict[student][0] + " " + str(stPwdDict[student][1]))
		login(stPwdDict[student][0], str(stPwdDict[student][1]))
		if "http://localhost:8000/accounts/createpassword/" == driver.current_url:
			addPassword(student)
		driver.get("http://localhost:8000/student_collaboration/settings/")

		# addValByName(20, "distance")

		optionSelector = driver.wait.until(EC.presence_of_element_located((By.NAME, "option")))
		# for option in optionSelector.find_elements_by_name('1100'):
		#    if option.text == "1100":
		#        option.click()

		# collabTool = driver.wait.until(EC.presence_of_element_located((By.NAME, "collaborative_tool")))
		# collabTool.submit()

		time.sleep(300)
		logout()

		# logout(driver)
		# driver.close()
		# driver.quit()
