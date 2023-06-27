import os,sys,time,glob
from datetime import date

today = date.today()
curr_date = today.strftime("%Y/%m/%d")
#need to get rid of 0X format...
m_list = curr_date.split("/")

_list = [int(m_list[0]),int(m_list[1]),int(m_list[2])]

curr_date = "{}/{}/{}".format(_list[0],_list[1],_list[2])
base_path = "/pscratch/darshanlogs/"
_path = os.path.join(base_path,curr_date)
assert(os.path.exists(_path))
print(_path)
m_files = glob.glob(_path+"abashyal*.darshan")
print(m_files)