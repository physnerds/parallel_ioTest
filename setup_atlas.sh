export PATH=$PATH:$HOME/bin

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
asetup Athena,master,latest

#setup ROOT
lsetup "root 6.26.04-x86_64-centos8-gcc11-opt" 
export JSON_CMAKE=/cvmfs/sft.cern.ch/lcg/releases/jsonmcpp/3.10.5-f26c3/x86_64-centos8-gcc12-opt/lib64/cmake
export TBB_CMAKE=/cvmfs/sft.cern.ch/lcg/releases/tbb/2020_U2-daa7e/x86_64-centos8-gcc11-opt/lib/cmake

alias my_cmake='cmake ..  -DCMAKE_PREFIX_PATH=$JSON_CMAKE'
