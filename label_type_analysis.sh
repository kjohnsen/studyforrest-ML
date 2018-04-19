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

# with offset
echo -e 'strategy\tsubject\tlabel_type\taccuracy\toffset'
python3 simple.py "01" "valence" True
python3 simple.py "02" "valence" True
python3 simple.py "03" "valence" True
python3 simple.py "04" "valence" True
python3 simple.py "05" "valence" True
python3 simple.py "01" "arousal" True
python3 simple.py "02" "arousal" True
python3 simple.py "03" "arousal" True
python3 simple.py "04" "arousal" True
python3 simple.py "05" "arousal" True
python3 simple.py "01" "direction" True
python3 simple.py "02" "direction" True
python3 simple.py "03" "direction" True
python3 simple.py "04" "direction" True
python3 simple.py "05" "direction" True
