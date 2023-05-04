import os,sys,time
from optparse import OptionParser
import datetime



def Createwrapper(wrapper):
    wrapper.write("#!/bin/bash")


#this is bssed on https://docs.nersc.gov/systems/perlmutter/running-jobs/
#Calculate the number of logical CPUs per task
#Only true for Perlmutter

def CalculateProcessPerTask(tot_nodes, tot_ranks,isGPU=False):
    max_nodes = 128
    if isGPU: max_nodes=64
    ranks_pnode = tot_ranks/tot_nodes
    if ranks_pnode>max_nodes:
        print("Ranks per node ",ranks_pnode," Cannot excede max_nodes ",max_nodes)
        sys.exit()
    val = 2*max_nodes/ranks_pnode
    return str(int(val))
    
usage = "usage: %prog[opts]"
parser = OptionParser(usage=usage)

parser.add_option('--qos',dest='qos', help="debug or regular",default="regular")
parser.add_option("--account", dest='account',help="what account to charge the job",default="m2845")
parser.add_option("--isGPU",dest="isGPU",help="Specify for CPU or GPU task",default=False,action="store_true")
parser.add_option("--ntasks",dest="ntasks",help="Number of total Tasks",default=1)
parser.add_option("--n_nodes",dest="n_nodes",help="Number of CPU nodes to be used",default=1)
parser.add_option("--time",dest="time",help="time allocation for task completion",default="10")
parser.add_option("--executable",dest="executable",help="executable with full path",default="bla")
parser.add_option("--arguments",dest="arguments",help="additional arguments to the executable",default="")

#Need to find a way to write multiple srun commands in a single bash script.


(opts,args) = parser.parse_args()

tot_tasks = int(opts.ntasks)
tot_nodes = int(opts.n_nodes)
isGPU = opts.isGPU
executable = opts.executable
if "./" in executable:
    executable = executable.replace("./","")
if not os.path.exists(executable):
    print("Executable path does not exist ",executable)
    sys.exit()


process ="cpu" 
if isGPU: process = "gpu"
np_task = CalculateProcessPerTask(tot_nodes,tot_tasks,isGPU)

time_stamp = int(time.time())
wrapper_name = "batch_"+str(time_stamp)+".sh"

mwrap = open(wrapper_name,"w")
mwrap.write("#!/bin/sh\n")
mwrap.write("#SBATCH -A "+opts.account+"\n")
mwrap.write("#SBATCH --qos="+opts.qos+"\n")
mwrap.write("#SBATCH -C "+process+"\n")
mwrap.write("#SBATCH --time="+opts.time+"\n")

msrun = "srun -n "+str(tot_tasks)+" "
if not isGPU:
    msrun+="--cpu-bind=cores "

msrun += "-c "+np_task+" "
msrun += "./"+executable+" "+opts.arguments+" \n"

mwrap.write(msrun)
mwrap.close()

    



