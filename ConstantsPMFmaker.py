#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 19:35:33 2019

This file contains a class that contains all the constant variables

@author: andresvodopivec
"""
from enum import Enum
import json

class Configuration(Enum):
    with open('INPUT_USER_PMF_MAKER.json', 'r') as fjson:
        config = json.load(fjson)

    # Assigning variables to the files present in topolSlurmMdpFolder.
    # topolSlurmMdpFolder is the folder were all the required files are located.
    # Including the .ff folder in case needed.
    #---------------------------------------------------------------------------
    iniBoxName = config['REQUIRED_FILES_NAMES']['INI_BOX_NAME']
    mmtBoxName = config['REQUIRED_FILES_NAMES']['BOX_TO_CONCAT']
    emIniMdpName = config['REQUIRED_FILES_NAMES']['EM_INI_MPD']
    emMdpName = config['REQUIRED_FILES_NAMES']['EM_MDP']
    pmfMdpName = config['REQUIRED_FILES_NAMES']['PMF_MDP']
    nvtMdpName = config['REQUIRED_FILES_NAMES']['NVT_MDP']
    ionsMdpName = config['REQUIRED_FILES_NAMES']['IONS_MDP']
    topoIniName = config['REQUIRED_FILES_NAMES']['TOPO_INI']
    cpuHungSlurmName = config['REQUIRED_FILES_NAMES']['SLURM_SUBMISSION_FILE_1']
    gpuHungSlurmName = config['REQUIRED_FILES_NAMES']['SLURM_SUBMISSION_FILE_2']
    cpuFullnodeSlurmName = config['REQUIRED_FILES_NAMES']['SLURM_SUBMISSION_FILE_3']
    topolSlurmMdpFolder = config['REQUIRED_FILES_NAMES']['ALL_INITIAL_FILES_FOLDER']
    jobSlurmName = config['REQUIRED_FILES_NAMES']['INI_SLURM_JOB_NAME'] # the job name #SBATCH -J option in the slurm file.

    # Outputs from GMX when using grompp, solvate, genion, mdrun
    #-----------------------------------------------------------
    outSolvate = config['GMX_OUTPUT_FILES_NAMES']['GMX_SOLVATE_OUTPUT']
    outGenion = config['GMX_OUTPUT_FILES_NAMES']['GMX_GENION_OUTPUT']
    outGromppEmInitial = config['GMX_OUTPUT_FILES_NAMES']['GMX_GROMPP_EM_INITIAL_OUTPUT']
    outMdrunEmInitial = config['GMX_OUTPUT_FILES_NAMES']['GMX_MDRUN_EM_INITIAL_OUTPUT']
    outGromppEm = config['GMX_OUTPUT_FILES_NAMES']['GMX_GROMPP_EM_OUTPUT']
    outMdrunEm = config['GMX_OUTPUT_FILES_NAMES']['GMX_MDRUN_EM_OUTPUT']
    outGromppNvt = config['GMX_OUTPUT_FILES_NAMES']['GMX_GROMPP_NVT_OUTPUT']
    outMdrunNvt = config['GMX_OUTPUT_FILES_NAMES']['GMX_MDRUN_NVT_OUTPUT']
    outGromppPmf = config['GMX_OUTPUT_FILES_NAMES']['GMX_GROMPP_PMF_OUTPUT']

    # Parameters required for running Gromacs simulation
    #---------------------------------------------------
    pmfTotalSteps = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['PMF_TOTAL_STEPS']
    gmxCall = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['GMX_CALL'] # way to call gromacs in current machine
    pmfSimName = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['PMF_SIMULATION_NAME'] # Name for folders that will have each pmf steps
    residToMove = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['RESIDUE_TO_MOVE_IN_INI_BOX_NAME'] # The molecule that is alone in the box and will be moved. This box is refered to as iniBoxName.
    cation = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['CATION_FOR_GENION'] # name of the cation to be inserted in the system
    anion = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['ANION_FOR_GENION'] # name of the anion to be inserted in the system
    pmfSimNum = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['PMF_SIMULATION_NUMBER'] # the simulation pmf number to start. It has to be integer values (In case something fails, you can restart wherever you were left)
    zDistIni = float(config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['Z_DISTANCE_TO_MOVE_FOR_PMF_INI']) # just an initial distance. Needed more for initial debugging
    zDist = float(config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['Z_DISTANCE_TO_MOVE_FOR_PMF']) # The distance the residToMove will be moved for each pmf step simulation
    ompThreads = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['OPEN_MP_THREAD'] # OpenMP threads that are specified in the gmx command line as -ntomp
    zBoxAdditional = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['Z_BOX_ADDTIONAL_LENGTH'] # For additional increment of the box in Z direction
    operation = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['OPERATION_FOR_MOLECULE_TO_MOVE'] # The Z direction the molecule is going to be moved.
    residToMoveIni = config['SCRIPT_PARAMETERS_FOR_GMX_AND_PMF_MAKER']['RESIDUE_TO_MOVE_INITIAL'] # All residues will be moved in the iniBoxName.


#print(Configuration.operation.value)