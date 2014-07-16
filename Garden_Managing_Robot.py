import subprocess
import os
import shlex
import array
import string
import shutil
import Tkinter as tk
from PIL import Image, ImageTk
import re

def main():

    global clingo_path
    clingo_path=raw_input('Enter the path for clingo')
    print "Path given :"+clingo_path+"\n"
    clingo_path=os.path.abspath(clingo_path)
   
    for garden_no in range(1,4):
        print " ****************  Welcome to Garden :"+str(garden_no)+" ************* "
        print "\n"
        planner(garden_no)
        Observe(garden_no)
    
     
def printer(plant_no):
    root = tk.Tk()
    root.title('Actions to be performed')
    imageFile = "robot-"+str(plant_no)+".jpg"
    image1 = ImageTk.PhotoImage(Image.open(imageFile))
    w = image1.width()
    h = image1.height()
    x = 0
    y = 0
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    panel1 = tk.Label(root, image=image1)
    panel1.pack(side='top', fill='both', expand='yes')
    panel1.image = image1
    root.mainloop()
        

                    
def planner(garden_no):    
    
    
    Prog_instance = 'situation_'+str(garden_no)+'.sm'
    
    
    print " %%%%%%%%%%%%%%% The Current Situation is %%%%%%%%%%%%%% "
    f_instance = open('situation_'+str(garden_no)+'.sm', "r+")

    goal_stmt = "goal(T):-"    
    for k in f_instance.readlines():
        print k
        if "symptom" in k:
            if "-holds" not in k:
                goal_stmt=goal_stmt+'-'+k.strip()[:-3]+'T),'
    goal_stmt=goal_stmt+'step(T).'                            
    f_instance.close()
    print "\n"
    
    # Goal File Generation
    file_goal = open('goal_'+str(garden_no)+'.sm',"w+")
    file_goal.write(goal_stmt.strip())
    file_goal.close()
    
    # Calling Clingo Planner Files
    process = subprocess.Popen([clingo_path,"Garden.sm",'goal_'+str(garden_no)+'.sm',"Planner.sm",str(Prog_instance),"1"], \
                                      stderr=subprocess.PIPE,stdout=subprocess.PIPE)

    print " %%%%%%%%%%%%%%%%%I am Planning. Wait for some time and don't disturb me.%%%%%%%%%%%%%%%%"
    print "\n"
    if process.stderr:
        print process.stderr.readlines()
        
    if process.stdout:
        
        f1 = open('actions_'+str(garden_no)+'.sm', "w+")
        f2 = open('fluents_'+str(garden_no)+'.sm', "w+")
        
        
        for line in process.stdout.readlines():    
            
           
            if "UNSATISFIABLE" in line:
                print " %%%%%%%%%%%%%% Once check your description file %%%%%%%%%%%%%"
                break
            
            
            fluents=shlex.split(line)   
            for j in fluents:
                
                if "occurs" in j:
                    f1.write(j+'.\n')
                    print j+'\n'
                elif "holds" in j:    
                    f2.write(j+'.\n')
        f1.close()
        f2.close()
        read_file(garden_no)
        print "\n"

def read_file(file_no):
    f1 = open('actions_'+str(file_no)+'.sm', "r+")
    data=f1.read()
    substring = 'supply'
    substring1='apply'
    substring2='identify'
    search = re.search(substring,data)
    search2 = re.search(substring1,data)
    search3 = re.search(substring2,data)
    if search:
        printer(1)
    if search3:
        printer(3)
    if search2:
        printer(2)
    f1.close()

       
def Observe(garden_no):
    
    print " %%%%%%%%%%%%%% Faults in Planning %%%%%%%%%%%%%%% " 
    ans=raw_input('Do you find anything missing in the give plan(Yes/No)?')
    
    if ans.lower() == "yes":
        obs=raw_input("Please enter what you find as missing and enter as following [Ex:obs(fluent(X),3)]:")               
        think(obs,garden_no)
                
    elif ans.lower() == "no":
        pass
    else:
        print "Enter either yes or no.Please correct your string"
    print "\n"
    
    

def think(obs,garden_no):
    
    check=0
    if obs[-1:] != '.':
        obs=obs+'.'
    
    
    observe=string.replace(obs,'obs','holds')
    file=open('fluents_'+str(garden_no)+'.sm',"r+")
    lines=file.readlines()    
    
    for line in lines:
        
        if (str(line).strip() == str(observe).strip()):
           print ("Given plan is perfect.")
           check=1
           break
    file.close()   
        
    if check==0:
       prog_instance='situation_'+str(garden_no)+'.sm' 
       diag_instance='diag_'+str(garden_no)+'.sm' 
       
       
       shutil.copyfile(prog_instance,diag_instance)
       f3=open(diag_instance,"a+")
       f3.write("\n")
       if obs[-1:] != '.':
          obs=obs+'.' 
       f3.write(obs+'\n')
       current_timestep=obs[string.rindex(obs,',')+1:]
       f3.write("current("+current_timestep+"\n")
       f3.close()
       Diagnosis(garden_no)

                    
def Diagnosis(garden_no):    
    
    print "\n"
    print " ******** I am doing Diagnosis on given set of actions*********** "
    
    process = subprocess.Popen([clingo_path,"Garden.sm","Diagnosis.sm",'actions_'+str(garden_no)+'.sm','diag_'+str(garden_no)+'.sm',"1"], \
                                    stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    if process.stderr:
        print process.stderr.readlines()
    
    if process.stdout:
        
        f4 = open('diag_'+str(garden_no)+'.sm', "w+")
        
        
        for line in process.stdout.readlines():    
            
            # Conditions are not satisfied
            if "UNSATISFIABLE" in line:
                print "Find if you have missed anything in description"
                break
            
            # Capturing Diagnostics results
            results=shlex.split(line)
            for j in results:
                
                if "occurs" in j:
                    f4.write(j+'.\n')
                    print j+'.\n'
                
        f4.close()
        
    
# Calling main module    
if __name__ == "__main__":
    main()
