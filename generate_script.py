import os, sys
from datetime import date
#create wrapper and execute after creation...

if len(sys.argv)<2:
  print("Needed: nodes [tasks per node] [time]")
  sys.exit()

nodes = int(sys.argv[1])

ntasks_per_node=4
if len(sys.argv)>2:
  ntasks_per_node=int(sys.argv[2])
  
n_time = 10
if len(sys.argv)>3:
  n_time = int(sys.argv[3])

print("Creating wrapper for total {} tasks with {} tasks per node of runtime {}".format(nodes*ntasks_per_node,ntasks_per_node,n_time))
wrapper_name = "test_script.sh"

wp = open(wrapper_name,'r')
content=[]
for line in wp:
  content.append(line)
  
wp.close()

new_wrapper = wrapper_name.replace(".sh","_{}_{}_{}.sh".format(nodes,ntasks_per_node,n_time))

nwp = open(new_wrapper,'w')
for line in content:
  if "time" in line:
    nwp.write(line.replace("10",str(n_time)))
  elif "nodes" in line:
    nwp.write(line.replace("32",str(nodes)))
  elif "ntasks-per-node" in line:
    nwp.write(line.replace("4",str(ntasks_per_node)))
  else:
    nwp.write(line)
    
nwp.close()
