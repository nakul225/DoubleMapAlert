DoubleMapAlert
==============

A web application that alerts user of an approaching bus near a user specified location.

To run the application, run sse_server.py  
	python sse_server.py 
This will start the server that can push alerts about upcoming buses to the client  
	Open http://localhost:8001/ in you browser.  

Status about each bus in the input section would flash showing how far the bus is from target coordinates. When the bus comes within 0.3 miles from specified location, the webpage would alert user with name of the approaching bus.


##Current harcoded values:  

*city = IUB (Indiana University at Bloomington)  

*list of buses tracked = ('3 College Mall / Bradford Place','6 Campus Shuttle - Fri','6 Limited', '9 IU Campus / College Mall / Campus Corner', 'A Route', 'B Route', 'C Route', 'D Route')  

*Target coorodinates = (39.17159402400064, -86.51633620262146) #10th St Bloomington, IN 47408   

*Alert Distance = 0.3 miles
