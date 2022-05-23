from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #Import from AWS-IoT Library
import time#To create delay
from datetime import date, datetime #To get date and time
#import Adafruit_CharLCD as LCD #Import LCD library 
import Adafruit_DHT #Import DHT Library for sensor

myMQTTClient = AWSIoTMQTTClient("new_Client") #add your cliend id from Test menu

myMQTTClient.configureEndpoint("a11y5asn11fe7b-ats.iot.ap-south-1.amazonaws.com", 8883) #add your endpoint from act menu

#download Root CA1 certificate
myMQTTClient.configureCredentials("/home/pi/Desktop/IoT/AWS-Certificates/AmazonRootCA1.pem", "/home/pi/Desktop/IoT/AWS-Certificates/private.pem.key", "/home/pi/Desktop/IoT/AWS-Certificates/SSLCertificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

sensor_name = Adafruit_DHT.DHT11 #we are using the DHT11 sensor
sensor_pin = 4 #The sensor is connected to GPIO17 on Pi
time.sleep(2) #wait for 2 secs

connecting_time = time.time() + 10

if time.time() < connecting_time:  #try connecting to AWS for 10 seconds
    myMQTTClient.connect()
    myMQTTClient.publish("DHT11/info", "connected", 0)
    print "MQTT Client connection success!"
    #lcd.message('Connected to \n AWS thing') #if connected
else:
    print "Error: Check your AWS details in the program"
    #lcd.message('Error: \nInvalid details') #if not connected

    
time.sleep(2) #wait for 2 secs

while 1: #Infinite Loop
    now = datetime.utcnow() #get date and time 
    current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ') #get current time in string format 
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin) #read from sensor and save respective values in temperature and humidity varibale  
    #lcd.clear() #Clear the LCD screen
    #lcd.message ('Temp = %.1f C' % temperature) # Display the value of temperature
    #lcd.message ('\nHum = %.1f %%' % humidity)  #Display the value of Humidity
    time.sleep(2) #Wait for 2 sec then update the values

    #prepare the payload in string format 
    payload = '{ "timestamp": "' + current_time + '","temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' }'

    print payload #print payload for reference 
    myMQTTClient.publish("DHT11/data", payload, 0) #publish the payload
    
    #lcd.clear() #Clear the LCD screen
    #lcd.message ('Published to \n  AWS-IOT') # Display the value of temperature
    print 'Published data to AWS-IoT'
    time.sleep(2) #Wait for 2 sec then update the values
