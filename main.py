import sys
import mysql.connector
import time
from datetime import datetime
from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService


def connectToMySQL():
    # establish connection to MySQL
    global connection, cursor
    print("Connecting to MySQL")
    connection = None
    for attempt in range(0, 10):
        try:
            connection = mysql.connector.connect(host='',
                                                 database='',
                                                 user='',
                                                 password='')
        except Exception as e:
            print("Error while connecting to MySQL", e)
            print("Retrying connection after 20 seconds..")
            numAttemptsLeft = 10 - attempt
            print(numAttemptsLeft, " attempts left.")
            time.sleep(20)

    if connection is None:
        print("Failed to connect to MySQL, closing program")
        sys.exit()
    elif connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server Version", db_Info)
        cursor = connection.cursor(buffered=True)
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record[0])
        connection.autocommit = True

def connectToAirMore():
    # establish connection to phone with Airmore
    print("Connecting to AirMore")
    global smsService
    ANDROID_IP = None
    ANDROID_SESSION = None
    for attempt in range(0,10):
        try:
            ANDROID_IP = IPv4Address("192.168.43.1")
            ANDROID_SESSION = AirmoreSession(ANDROID_IP)
        except Exception as e:
            print("Error while connecting to AirMore", e)
            print("Retrying connection after 20 seconds..")
            numAttemptsLeft = 10 - attempt
            print(numAttemptsLeft, " attempts left.")
            time.sleep(20)
        else:
            if not ANDROID_SESSION.is_server_running:
                print("Cannot connect to AirMore")
                print("Retrying connection after 20 seconds..")
                numAttemptsLeft = 10 - attempt
                print(numAttemptsLeft, " attempts left.")
                time.sleep(20)
            elif ANDROID_SESSION.is_server_running:
                break

    if ANDROID_SESSION.is_server_running:
        print("Connected to AirMore")
        # initializing SMS service
        smsService = MessagingService(ANDROID_SESSION)
        print("smsService initialized")
    else:
        print("Unable to connect to AirMore, closing program")
        sys.exit()

def checkInbox():
    None

def updateRecords():
    None

def main():
	print("Landslide Notification Service")
	print("Initializing interfaces..")
	connectToAirMore()
	print("Initialization successful!")
	print("Landslide Notification Service Started\n")
	genAttempt = 0
	while genAttempt < 5:
		try:
			CheckTime = datetime.today()
			checkInbox()
			print("Time checked: ", CheckTime)
			updateRecords()
		except Exception as e:
			print("Connection issues encountered!", e)
			genAttempt += 1
			leftAttempt = 5 - genAttempt
			print("Retrying after 20 seconds..")
			print(leftAttempt, "attempts left\n")
			time.sleep(20)
		else:
			print("Starting 10 seconds sleep..\n")
			time.sleep(10)
			print("Woke up. Again.")


if __name__ == '__main__':
	main()