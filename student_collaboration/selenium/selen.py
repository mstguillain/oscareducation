import os
import traceback
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
	{"mastered":("P3D-U3-T2", "P3D-U3-C2"), "unmastered":("P3D-U3-A2",)},
	{"unmastered": ("P3D-U3-T2", "P3D-U3-C2"), "mastered": ("P3D-U3-A2",)}
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

		#self.fakeTest()

	def __testFunction(self, fun, *args):
		""" Test a given function on the given arguements"""
		functionName = fun.im_func.__name__
		print("Testing "+functionName+" with "+str(args)+" : ")
		try:
			fun(*args)
			print("\tOK")
		except TimeoutException as e:
			traceback.print_exc(e)
			print("\tERROR (Timeout) : "+ str(e.args) +" One of the demanded ressource took to much time to be found. It's likely that it didn't existed or the page wasn't loaded/redirected as expected")
		except WebDriverException as e:
			traceback.print_exc(e)
			print("\tError (WebDriver) : ") + str(e.args) + " The content have not beel loaded yet (need to call wait method)"
		except Exception as e:
			traceback.print_exc(e)
			print "\tERROR: " + str(e.args)
		except BaseException as e:
			traceback.print_exc(e)
			print "\tERROR: " + str(e.args)



	def __waitElementByName(self, name):
		return self.driver.wait.until(EC.presence_of_element_located((By.NAME, name)))

	def __waitElementByXPath(self, xPath):
		return self.driver.wait.until(EC.presence_of_element_located((By.XPATH, xPath)))

	def __waitElementByClassName(self, className):
		return self.driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, className)))

	def __fillBoxSubmit(self, name, text):
		box = self.__fillBox(name, text)
		box.submit()

	def __fillBox(self, name, text):
		box = self.__waitElementByName(name)
		box.send_keys(text)
		return box

	def __clickButtonByXPath(self, xPath):
		button = WebDriverWait(self.driver, self.TIMEOUT_BUTTON_WAIT).until(EC.element_to_be_clickable((By.XPATH, xPath)))
		# Do not try to create a parameter for this, it make crashs
		action = ActionChains(self.driver)
		action.click(button).perform()

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
		#self.driver.get("http://127.0.0.1:8000/professor/lesson/4") # TODO : to delete
		initUrl = self.driver.current_url
		# if we get the id of the first created student then it's easy to find the other one (just +1)
		xPathFirstTableEntry = '//*[@id="students"]/div[4]/div/table/tbody/tr[1]/td[1]/a'
		entry = self.__waitElementByXPath(xPathFirstTableEntry)#self.driver.find_element_by_xpath(xPathFirstTableEntry)
		href = entry.get_attribute("href")
		# get the id : 'http://127.0.0.1:8000/professor/lesson/1/student/1134/' -> 1134
		firstStudentIdStr = href[href[0:-2].rfind("/")+1:-1]
		firstStudentId = int(firstStudentIdStr)

		studentNumber = len(studentSkillsList)
		for i in range(studentNumber):
			studentId = firstStudentId+i
			urlToStudent = initUrl+"student/"+str(studentId)+"/"
			skillTab = "#heatmap"
			# We load the page where all its skills are
			self.driver.get(urlToStudent+skillTab)
			studentSkillsDict = studentSkillsList[i]
			for masteredStr, skillList in studentSkillsDict.iteritems():
				for skillStr in skillList:
					# We first make the popup appear

					# Be careful here to have an exact match, because after a skill is mastered it had invisible things with the name as well
					xPath = '//*[text()="{0}"]/..'.format(skillStr)
					# It won't appear if it is not in the scrolling view, so we center the button before clicking it
					button = self.__waitElementByXPath(xPath)
					centerY = button.location['y'] - self.driver.get_window_size()['height']//2
					self.driver.execute_script("window.scrollTo(0, " + str(centerY) + ");")

					self.__clickButtonByXPath(xPath)
#                   self.__clickButtonByXPath('//*[contains(text(), "{0}")]/..'.format(skillStr)) # DO NOT CALL, I don't know why but the function does not work there

					# As it appears we set the skill
					# The order is the one the buttons are displayed on the popup
					SKILL_MASTERED = 1
					SKILL_UNMASTERED = 2
					SKILL_UNKNOWN = 3
					if (masteredStr == "mastered"):
						skillIdx = SKILL_MASTERED
					else:
						skillIdx = SKILL_UNMASTERED
					test = self.__waitElementByClassName('popover-content')
					# Acess the correct button
					child = test.find_element_by_xpath("//div[2]/center/form[" + str(skillIdx) + "]")
					child.submit()

	def fakeTest(self):
		""" ca c'est juste pour faire des petit test vite fait """
		url = "http://127.0.0.1:8000/professor/lesson/4/student/1140/#heatmap"
		self.driver.get(url)

##### NEED TO BE ADAPTED ######
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


if False: # Ancien main, on l'apelle pas
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
