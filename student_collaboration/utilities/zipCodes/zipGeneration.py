import googlemaps # pip install -U googlemaps
import csv

FILE_SQL_PATH = "./zipCodes.sql"
APP_NAME = "student_collaboration"
TABLE_NAME = "postalcode"
databaseName = APP_NAME + "_" + TABLE_NAME
SQL_COMMAND = "INSERT INTO " + databaseName +\
			  " (id, postal_code, longitude, latitude) VALUES (%d, %d, %f, %f);\n"

gmaps = googlemaps.Client(key='AIzaSyArd518ntiFlTnSsTRwtYz5t8L-ZKdLDUo')

def searchLatLngOfZipCode(zipCode):
	# Geocoding an address
	print zipCode
	geocode_result = gmaps.geocode(str(zipCode)+' Belgium', region="be")
	try:
		location = geocode_result[0]["geometry"]["location"]
		return location["lat"], location["lng"]
	except Exception as e:
		print "Passing"
		print e, zipCode
		return None

def generateAllDistinctZipBelgium():
	# We use a set as it ignored duplicated items
	allZip = set()

	with open('zipcodes.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			currentZip = row[0]
			if currentZip not in allZip:
				allZip.add(currentZip)
	return allZip


def generateSQLfile():
	# First we retrieve all zip codes : 
	allZips = generateAllDistinctZipBelgium()


	# As we ask for google maps we refresh the file
	SQLfile = open(FILE_SQL_PATH, "w")
	SQLfile.write("TRUNCATE " + databaseName + " CASCADE;\n")
	id = 1
	for zipCode in allZips:
		res = searchLatLngOfZipCode(zipCode) 
		if res != None :
			lat, lng = res
			SQLfile.write(SQL_COMMAND % (id, int(zipCode), float(lng), float(lat)))
			id += 1

	SQLfile.close()

def main():
	generateSQLfile()

if __name__ == '__main__':
	main()
