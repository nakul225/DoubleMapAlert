#!/usr/bin/env python
#Makes use of Server sent event example given at : https://github.com/stevenewey/ssedemo
import gevent
import gevent.monkey
from Bus import *
from Route import *
from constants import *
from BusOperations import *
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template
const = Constants()
const.load_constants("constants.json")

app = Flask(__name__)

def event_stream():
    #TODO: Get these inputs from client:
    city = "IUB"
    #Buses whose coordinates 
    listColloquialBusNumbers = ['3 College Mall / Bradford Place','6 Campus Shuttle - Fri','6 Limited', '9 IU Campus / College Mall / Campus Corner', 'A Route', 'B Route', 'C Route', 'D Route']
    #target location coordinates
    targetCoordinates = (39.17159402400064, -86.51633620262146) #10th St Bloomington, IN 47408 
    alertDistance = 0.3 #miles
    
    #Create constans object to fetch all constant values
    constantsObject = Constants()
    constantsObject.load_constants("constants.json")
    #Create bus operations object
    busOperationsObject = BusOperations(constantsObject, city)
    #Create route object
    routeObject = Route(constantsObject, city)
    #Create a map of actual to colloquial bus numbers
    map_actual_bus_numbers_to_colloquial_bus_numbers = routeObject.get_colloquial_bus_numbers_from_actual_bus_numbers()
    #Make a list of bus objects
    listOfActualBusNumbers = routeObject.get_actual_bus_numbers(listColloquialBusNumbers)
    #Create bus objects
    listOfBusObjects = [] #Stores list of all bus objects
    for actualNumber in listOfActualBusNumbers:
        busObject = Bus(constantsObject)
        busObject.set_actual_number(actualNumber)
        listOfBusObjects.append(busObject)
    flag = True
    while flag:
        #gevent.sleep(2) #sleep for 2 second before updating status of each bus to avoid overloading servers with requests
        listOfBusObjects = busOperationsObject.updateBusStatus(listOfBusObjects)
        #check which buses are approaching, then track them or show them or whatever
        for bus in listOfBusObjects:
            status = bus.getBusMovementAgainstTarget(targetCoordinates)
            if status == constantsObject.APPROACHING:
                status = "APPROACHING"
            elif status == constantsObject.LEAVING:
                status = "LEAVING"
            else:
                status = "STOPPED"
            data = map_actual_bus_numbers_to_colloquial_bus_numbers[bus.get_actual_number()]," :",status, " is at distance: ",str(bus.getBusDistanceFromTarget(targetCoordinates))," miles"
            printableData = " ".join(data)
            gevent.sleep(2) #sleep for 2 second before updating status of each bus to avoid overloading servers with requests
            if status == "APPROACHING" and  bus.getBusDistanceFromTarget(targetCoordinates) <= alertDistance:
                printableData = "ALERT! bus: "+str(map_actual_bus_numbers_to_colloquial_bus_numbers[bus.get_actual_number()])+" is near"
                #print type(printableData)
                #print printableData
            yield 'data: %s\n\n' % printableData
    
@app.route('/my_event_source')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('sse.html')

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8001), app)
    http_server.serve_forever()
