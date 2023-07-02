cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

project(tmpi CXX C CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
find_package(MPI REQUIRED)
find_package(ROOT REQUIRED COMPONENTS)
find_package(HDF5 REQUIRED)

message("STATUS OF HDF5_FOUND IS ${HDF5_FOUND}")
set(HDF5_PREFER_PARALLEL TRUE)

#find_package(PythonLibs REQUIRED)

enable_language(CUDA)
set(CMAKE_CUDA_STANDARD 17) #NEED TO FIX WITH 17
set(CMAKE_CUDA_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)



set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)


include_directories(SYSTEM
                    ${INCLUDE_DIR}
                    ${ROOT_INCLUDE_DIRS}
                    ${MPI_INCLUDE_DIRS}
                    ${MPI_CXX_INCLUDE_DIRS}
                    ${MPI_C_INCLUDR_DIRS}
                    ${HDF5_INCLUDE_DIRS}
                    )
#This is only 
#set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
set(CMAKE_CXX_EXTENSIONS OFF)

set(libraries ${libraries}
                ${ROOT_LIBRARIES}
                ${MPI_CXX_LIBRARIES}
                ${HDF5_LIBRARIES}
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


add_executable(test_parallel_hdf5 test_parallel_hdf5.cc)
target_compile_options(test_parallel_hdf5 PRIVATE ${HDF5_CXX_COMPILER_EXECUTABLE})
target_link_libraries(test_parallel_hdf5 ${libraries})

