import os,sys,time,glob
from datetime import date

print("USAGE: find_darshanlogs.py [Year]/[month]/[Day]\n Else defaults to today's date")

today = date.today()
curr_date = today.strftime("%Y/%m/%d")
if len(sys.argv)>1:
  curr_date = sys.argv[1]

#need to get rid of 0X format...
m_list = curr_date.split("/")
print("Printing for {}".format(curr_date))

_list = [int(m_list[0]),int(m_list[1]),int(m_list[2])]

curr_date = "{}/{}/{}".format(_list[0],_list[1],_list[2])
base_path = "/pscratch/darshanlogs/"
_path = os.path.join(base_path,curr_date)
assert(os.path.exists(_path))
print(_path)
m_files = glob.glob(_path+"/abashyal*.darshan")
m_files.sort(key=os.path.getmtime)
for file in m_files:
  print(file)
  
print("Total {} files".format(len(m_files)))