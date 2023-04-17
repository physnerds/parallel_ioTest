cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

project(tmpi CXX C)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#find_package(MPI REQUIRED)
find_package(ROOT REQUIRED COMPONENTS)
#find_package(PythonLibs REQUIRED)

set(MPI_INCLUDE_DIRS /blues/gpfs/home/software/spack-0.10.1/opt/spack/linux-centos7-x86_64/intel-17.0.4/intel-mpi-2017.3-dfphq6kavje2olnichisvjjndtridrok/compilers_and_libraries_2017.4.196/linux/mpi/intel64/include)

set(MPI_CXX_LIBRARIES /blues/gpfs/home/software/spack-0.10.1/opt/spack/linux-centos7-x86_64/intel-17.0.4/intel-mpi-2017.3-dfphq6kavje2olnichisvjjndtridrok/compilers_and_libraries_2017.4.196/linux/mpi/intel64/lib/libmpi.so)

set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)


include_directories(SYSTEM
                    ${INCLUDE_DIR}
                    ${ROOT_INCLUDE_DIRS}
                    ${MPI_INCLUDE_DIRS}
                    ${MPI_CXX_INCLUDE_DIRS}
                    )

set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
set(CMAKE_CXX_EXTENSIONS OFF)

set(libraries ${libraries}
                ${ROOT_LIBRARIES}
                ${MPI_CXX_LIBRARIES}
                ROOT::Core
                ROOT::RIO
                ROOT::Tree
                ROOT::Hist
                )
                

include(${ROOT_USE_FILE})

set(SOURCE_FILES include/TMPIFile.cxx include/TMPIClientInfo.cxx)

REFLEX_GENERATE_DICTIONARY(G__tmpiDict include/TMPIFile.h include/TMPIClientInfo.h SELECTION include/tmpiDict.xml)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES} G__tmpiDict.cxx)

target_link_libraries(${PROJECT_NAME} PRIVATE ${libraries})

add_executable(test_tmpi 
 include/TMPIFile.cxx
 include/TMPIClientInfo.cxx
test_tmpi.C)
target_include_directories(test_tmpi PRIVATE ${INCLUDE_DIR}) 
target_link_libraries(test_tmpi PRIVATE ${PROJECT_NAME} ${libraries})

#add_executable(testTMPIFile
# include/TMPIFile.cxx
# include/TMPIClientInfo.cxx
#testTMPIFile.C)
#target_include_directories(testTMPIFile PRIVATE ${INCLUDE_DIR}) 
#target_link_libraries(testTMPIFile PRIVATE ${PROJECT_NAME} ${libraries})


