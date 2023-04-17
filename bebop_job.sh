#!/bin/bash

#!/bin/bash

#SBATCH --job-name=tmpi_job
#SBATCH --account=condo
#SBATCH --partition=bdwall
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --output=tmpi_job.out
#SBATCH --error=tmpi_job.error
#SBATCH --mail-user=abashyal@anl.gov # Optional if you require email
#SBATCH --mail-type=ALL                  # Optional if you require email
#SBATCH --time=01:00:00

# Setup My Environment
module load intel-parallel-studio/cluster.2018.4-ztml34f
module load root/6.14.04
export I_MPI_FABRICS=shm:tmi

# Run My Program
srun -n 8 ./build/test_tmpi
