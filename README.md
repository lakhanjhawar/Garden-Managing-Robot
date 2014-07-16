Garden Managing Robot
============
Software Requirements:
Clingo 3.0.5
python 2.7.7
python packages: PIL, re, Tkinter
*************************NOTE************************************
You should close the image which says what action should be performed ,to get the next image.
You should give whether yes or no when asked to run next instance.
I have 3 different inputs or situation for my progam. When ever you are asked the following on screen do as shown below 

%%%%%%%%%%%%%% Faults in Planning %%%%%%%%%%%%%%% 
Do you find anything missing in the give plan(Yes/No)?


 and you enter input the program will take next instance automatically and execute.
New files will be created after execution of program with names "actions","goal" and "fluents".

***********************************************************************************



Action Language (AL) program on answer set programming with python interface.



  Garden Managing Robot is considered as a domain here. Robot is responsible to maintain water-  
  level in GARDEN. Water is assumed to be absorbed by the crops in two time-steps. So the Robot     
  should supply water after every two steps (Persistance Action).Symptoms of the nutrients deficiency 
  can also be percieved. According to the deficiency, weakness should be identified and corresponding 
  manure should be applied. Suppose deficiency is identified and plants are not watered,then actions   
  for water supply & manure application occur parallel and cause the effects of both actions(Parallel 
  actions).                                                                                           
                                                                                                      
  If manure is applied at a time-step, then neither water supply or opening reservoir should not be    
  executed in the next time step(Heuristics). Breakage of reservoir door can happen exogenously and   
  impact the events of the domain(Exogenous action).                                                  


•	The python program (Robot_on_Farms.py) uses four files as its input.
  o Garden.sm – Domain Description file.
  o	Planner.sm – Planner module.
  o	Diagnosis.sm – Diagnosis module.
  o	Situation_(Garden no).sm – Program instance files for each farm to process planning.
  
•	The interface program creates following intermediate files for its processing.
  o	Goal_(Garden no).sm – Goals generated as per the supplied program instance.
  o	Actions_(Garden no).sm – File contains all the actions retrieved from planner result.
  o	Fluents_(Garden no).sm – This file provides all the fluents obtained from planner result.
  o	Fdprob_(Garden no).sm – Program instance files for each Garden to do diagnosis (i.eFprob_(Garden no).sm + observations)
  o	Diag_(Garden no).sm – Result of Diagnosis.
  
•	The program expects user to enter inputs as similar to example provided.
•	The clingo.exe can be anywhere but the interface program & input files are expected to be in same directory.

•	Program Flow :
  1.	Receiving clingo.exe path from user.
  2.	Display program instance (Ex: Situation_1.sm) and construct goals according to the instance. Save those goals in a separate file (Ex: Goal_1.sm).
  3.	Planner module is called to generate a plan.
      a.	Files Garden.sm, Planner.sm, Situation_(Garden no).sm, & Goal_(Garden no).sm are given as inputs to Clingo to generate plan.
      b.	The fluents and actions of the generated plan are captured in two different files fluent_(Garden no).sm & actions_(Garden no).sm respectively.
      c.	The generated plan is displayed.
  4.	After planning, Observation module is called to get observations from the user.
  5.	If there are observations, then Think module is called to evaluate received observations.
      a.	First the observations are checked whether it is present in fluent file.
      b.	If it is not, then Diagnosis module is called. Otherwise, a message will be displayed that the observation is acceptable as per the plan.
  6.	Diagnosis module calls the solver to do diagnosis for the observation.
      a.	Garden.sm, Diagnosis.sm, and actions_(Garden no).sm are provided as input.
      b.	Results of the diagnosis are captured in diag_(Garden no).sm.


