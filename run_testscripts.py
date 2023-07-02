import os,sys,subprocess

m_cwd = os.getcwd()
files = os.listdir()

pre_command = ["sbatch","-A","m2845"]
scripts = []
outputs={}

for file in files:
  if "test_script_" in file:
    scripts.append(file)
    
for file in scripts:
  command=pre_command.copy()
  command.append("./"+file)
  result = subprocess.run(command,capture_output=True,text=True,check=True)
  outputs[file]=(result.stdout)

  
for output in outputs:
  print(output,outputs[output])



