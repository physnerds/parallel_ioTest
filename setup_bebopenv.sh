#!/bin/bash

# Setup My Environment
module load cmake
module load intel-parallel-studio/cluster.2018.4-ztml34f
module load root/6.14.04
export I_MPI_FABRICS=shm:tmi
