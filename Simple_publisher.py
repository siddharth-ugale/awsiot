import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a3a**4pzt-ats.iot.ap-south-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "certificates/6e11-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/6e11-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1.pem"
MESSAGE = "I am IoT Trainer"
TOPIC = "vit"
RANGE = 10

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTClient.connect()
print('Begin Publish')
for i in range (RANGE):
    data = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
    t.sleep(1)
print('Publish End')
myAWSIoTMQTTClient.disconnect()
