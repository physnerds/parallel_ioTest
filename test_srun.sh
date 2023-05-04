#!/bin/bash
#SBATCH -A m2845
#SBATCH --qos=regular
#SBATCH -C cpu
#SBATCH --ntasks-per-node=16
#SBATCH --time=10
export TOT=512
srun -n 32 --cpu-bind=cores -c $TOT ./build/test_tmpi



