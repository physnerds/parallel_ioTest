cmake_minimum_required(VERSION 3.9 FATAL_ERROR)

project(tmpi CXX C)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#find_package(MPI REQUIRED)
find_package(ROOT REQUIRED COMPONENTS)
#find_package(PythonLibs REQUIRED)

set(MPI_INCLUDE_DIRS $ENV{MPI_DIR}/include)

set(MPI_CXX_LIBRARIES $ENV{MPI_DIR}/lib/libmpi.so)

set(HDF5_INCLUDE_DIRS $ENV{HDF5_DIR}/include)

set(HDF5_LIBRARIES $ENV{HDF5_DIR}/lib/libhdf5.so)

set(HDF5_CXX_LIBRARIES $ENV{HDF5_DIR}/lib/libhdf5_cpp.so)
  
set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)


include_directories(SYSTEM
                    ${INCLUDE_DIR}
                    ${ROOT_INCLUDE_DIRS}
                    ${MPI_INCLUDE_DIRS}
                    ${MPI_CXX_INCLUDE_DIRS}
                    ${HDF5_INCLUDE_DIRS}
                    )

set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
set(CMAKE_CXX_EXTENSIONS OFF)

set(libraries ${libraries}
                ${ROOT_LIBRARIES}
                #${MPI_CXX_LIBRARIES}
                #${HDF5_LIBRARIES}
                #${HDF5_CXX_LIBRARIES}
                ROOT::Core
                ROOT::RIO
                ROOT::Tree
                ROOT::Hist
                )
                

include(${ROOT_USE_FILE})

set(SOURCE_FILES include/TMPIFile.cxx include/TMPIClientInfo.cxx)

REFLEX_GENERATE_DICTIONARY(G__tmpiDict include/TMPIFile.h include/TMPIClientInfo.h SELECTION include/tmpiDict.xml)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES} G__tmpiDict.cxx)

target_link_libraries(${PROJECT_NAME} PRIVATE ${libraries} ${MPI_CXX_LIBRARIES})

add_executable(test_tmpi 
 include/TMPIFile.cxx
 include/TMPIClientInfo.cxx
test_tmpi.C)
target_include_directories(test_tmpi PRIVATE ${INCLUDE_DIR}) 
target_link_libraries(test_tmpi PRIVATE ${PROJECT_NAME} ${libraries} ${MPI_CXX_LIBRARIES})

add_executable(test_parallel_hdf5 test_parallel_hdf5.cc)
target_compile_options(test_parallel_hdf5 PRIVATE 
${HDF5_CXX_COMPILER_EXECUTABLE})
target_link_libraries(test_parallel_hdf5 ${libraries} ${HDF5_LIBRARIES} ${MPI_CXX_LIBRARIES})


