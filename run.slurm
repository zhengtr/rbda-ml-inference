#!/bin/bash
#SBATCH --job-name=rbda-ml
#SBATCH --nodes=1 
#SBATCH --cpus-per-task=4
#SBATCH --output=.%A_%a.out
#SBATCH --error=./%j_%x.err
#SBATCH --gres=gpu:2
#SBATCH --time=20:00:00
#SBATCH --mem=160GB
#SBATCH -c 6

singularity exec --nv --overlay $SCRATCH/overlay-50G-10M.ext3:ro /scratch/work/public/singularity/cuda11.3.0-cudnn8-devel-ubuntu20.04.sif  /bin/bash -c "
source /ext3/miniconda3/etc/profile.d/conda.sh
export PATH=/ext3/miniconda3/bin:$PATH
conda activate
conda activate rbda-ml
python /scratch/tz408/rbda-ml/main.py --data_type questions --chunk_size 512

