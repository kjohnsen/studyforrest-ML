#!/bin/bash

#SBATCH --time=01:00:00   # walltime
#SBATCH --ntasks=8   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10096M   # memory per CPU core
#SBATCH -J "fmrilearn"   # job name


# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch

# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

module load python/3/6
python3 svc_reduced.py "01" "valence" 0.1
python3 svc_reduced.py "01" "valence" 1
python3 svc_reduced.py "01" "valence" 5
python3 svc_reduced.py "01" "valence" 10
python3 svc_reduced.py "01" "valence" 100
python3 svc_reduced.py "02" "valence" 0.1
python3 svc_reduced.py "02" "valence" 1
python3 svc_reduced.py "02" "valence" 5
python3 svc_reduced.py "02" "valence" 10
python3 svc_reduced.py "02" "valence" 100
python3 svc_reduced.py "03" "valence" 0.1
python3 svc_reduced.py "03" "valence" 1
python3 svc_reduced.py "03" "valence" 5
python3 svc_reduced.py "03" "valence" 10
python3 svc_reduced.py "03" "valence" 100
python3 svc_reduced.py "04" "valence" 0.1
python3 svc_reduced.py "04" "valence" 1
python3 svc_reduced.py "04" "valence" 5
python3 svc_reduced.py "04" "valence" 10
python3 svc_reduced.py "04" "valence" 100
python3 svc_reduced.py "05" "valence" 0.1
python3 svc_reduced.py "05" "valence" 1
python3 svc_reduced.py "05" "valence" 5
python3 svc_reduced.py "05" "valence" 10
python3 svc_reduced.py "05" "valence" 100
