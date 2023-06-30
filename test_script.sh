#!/bin/bash
#SBATCH -A m2845
#SBATCH --qos=regular
#SBATCH -C cpu
#SBATCH --time=10
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=4

srun --export=ALL,LD_PRELOAD="$DARSHAN_BASE_DIR/lib/libdarshan.so" ./build/test_tmpi
