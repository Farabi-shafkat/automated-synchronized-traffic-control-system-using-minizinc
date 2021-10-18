# automated-synchronized-traffic-control-system-using-minizinc
a project developed on for my undergrad Artificial Intelligence course requirement

I modeled the problem of traffic sign control as a constraint satisfaction problem. That is, given a set of roads with a specific amount of traffic congesion on various roads, what the optimum straffic sign state (which lights should be turned on or off) to minimize overall traffic congestion.

To solve the constraint problem, I used minizinc (https://www.minizinc.org/). To provide an interface and to run simulations, I used python and pymzn library.

* Get the project source code by running this command in git bash: 
`
git clone https://github.com/Farabi-shafkat/automated-synchronized-trafficcontrol-system-using-minizinc.git
`

* Install PyMzn 
`
pip install PyMzn
`
* Run the code using
`
python main.py
`
* in python editor console give input number of intersections you have in your 
model

* Then you have to build the graph. You have to give which junction is directly 
connected with other junction using road.

* Then you have to build the graph. You have to give which junction is directly 
connected with other junction using road. Sample input: 
`
9
2 11 1 4 10 2
1 10 3 3 4 4 5 4 5
2 3 6 6 26 7
1 2 8 7 13 9 5 15 10 
2 5 11 4 14 12 8 30 15 6 17 16
3 25 17 5 16 18 9 18 19
4 12 20 8 21 21 
5 31 22 7 22 23 9 4 24
8 2 25 6 19 26
10
`
* Then you have to give after how many second you want to change the lights of 
each junction. Then after each period of time your output will be shown. If you 
want to stop the system then press Ctrl+C


![gitimage](https://user-images.githubusercontent.com/37882738/137685488-0519a12b-8511-4d53-96d5-a2d07b765aed.png)







