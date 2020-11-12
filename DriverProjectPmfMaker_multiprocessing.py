#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:53:17 2019

This is the Driver Project file or the main file.

@author: andresvodopivec
"""

#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================
"""
Information:
------------

This script is meant to do a Potential of Mean Force in a reaction coordinate along the Z axis ONLY.
Your molecule of interest must be inside a box (iniBoxName variable in script).
This script has the following steps:
    a) It will move the molecule in the Z axis, solvate with scp216.gro ONLY and insert ions (cation and anion variables).

    b) Further EM (emIniMdpName varible for mdp file) will take place.

    c) It will concatenate with another box (mmtBoxName variable).

    d) The concatenated gro file will have an EM (emMdpName variable), NVT (nvtMdpName variable) for equilibration.

    e) The equilibrated system will be use to create a tpr file for the PMF.

    f) slurm pmf files must be submitted manually.

Requirements:
-------------

Create a main directory (pmfSimName + str(pmfSimNum) variable). Inside this directory paste the following files:
    1) The folder of your force field (.ff extension) in case it is required.
       If you are using FF that are Built-in Gromacs then you do not need to do this part.
    2) Create a new directory (topolSlurmMdpFolder variable). Inside this directory paste:
       a) The SLURM files for job submission. Current script ONLY works with SLURM files.
       b) The mdp files. Which are for EM initial, EM and NVT.
          Difference between EM initial an EM are details above.
       c) Box for step a) and step c) in the Purpose statement.
    3) The python files FuncForGMX.py, FileUtil.py and GROreader.py.
       For further information about this files use python help or read the information inside the files themselves.

This script will create 3 directories inside the main directory: initial, em_nvt and pmf.
From the information section, parts a) and b) will take place in the initial folder, parts c) and d) wiil take place in the
em_nvt directory, and parts e) and f) will take place in the pmf directory.
SLURM files will be saved in the em_nvt and pmf directories along the corresponding mdp files required to create the tpr files.

Usage:
------

All inputs to the program are be changed in the INPUT_USER_PMF_MAKER.json file.
Once you have all the files required just type:
    python DriverProjectPmfMaker.py

"""
#===============================================================================================================================
#===============================================================================================================================
#===============================================================================================================================

# =============================================================================
# IMPORTING LIBRARIES
# =============================================================================

import traceback
import os
from FileUtil import FileUtil as fu
from GROreader import GROreader as gr
from FuncForGMX import FuncForGMX as ffg
from ConstantsPMFmaker import Configuration as conf
import multiprocessing

# =============================================================================
# MULTIPROCESSING PMF FUNCTION
# =============================================================================
# Creating a single funciton where all the pmf will take place. This is required for multiprocessing

def run_PMF(a_pmfSimNum, a_zDistCumulative):
    folderName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '_pmf'
    print('\n\n=============================================================')
    print('=============================================================')
    print('\n\nDoing ' + folderName + '\n\n')
    print('=============================================================')
    print('=============================================================\n\n')

    # Names for gro and tpr files inside initial directory (initialDir)
    groIniName = conf.residToMove.value + str(a_pmfSimNum) + '.gro'
    groSolvaName = conf.residToMove.value + str(a_pmfSimNum) + '_solva.gro'
    groIonsName = conf.residToMove.value + str(a_pmfSimNum) + '_ions.gro'
    tprIniEmName = conf.residToMove.value + str(a_pmfSimNum) + '_em.tpr'
    groIniEmName = conf.residToMove.value + str(a_pmfSimNum) + '_em.gro'

    # Names for gro and tpr files inside em_nvt directory (emNvtDir)
    groConcatName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '.gro'
    groConcatEmName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '_em.gro'
    groConcatNvtName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '_nvt.gro'
    tprConcatEmName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '_em.tpr'
    tprConcatNvtName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '_nvt.tpr'

    # Names for tpr file inside pmf directory (pmfDir)
    tprConcatPmfName = conf.pmfSimName.value + '_' + str(a_pmfSimNum) + '_pmf.tpr'

    dirs = ffg.forMkDirs(mainWorkDir, conf.pmfSimName.value, str(a_pmfSimNum)) # Creating initial, em_nvt and pmf directories inside current main dir.
    initialDir = dirs[0] # initial directory
    emNvtDir = dirs[1] # em_nvt directory
    pmfDir = dirs[2] # pmf directory

    # Reading, creating an object, and writing iniBoxName gro file
    movedzO = gr.fromList_GROreader_Zmoving(iniBoxOb.file, a_zDistCumulative, conf.residToMoveIni.value, conf.operation.value)
    movedzObList = fu.fromGROreaderToFileUtil(movedzO)
    movedzObList.FileWriter(initialDir, groIniName)

    # Writing object of mmtBoxName gro file
    mmtBoxObGMX = gr.fromList_GROreader(mmtBoxOb.file)

    # Writing object of ions.mdp file
    ionsMdpOb.FileWriter(initialDir, conf.ionsMdpName.value)

    # Reading and creating an object of topol.top file
    topoIniOb.FileWriter(initialDir, conf.topoIniName.value)

    # Writing object of em_initial.mdp file
    emIniMdpOb.FileWriter(initialDir, conf.emIniMdpName.value)

    # Reading and creating an object of em.mdp file
    emMdpOb.FileWriter(emNvtDir, conf.emMdpName.value)

    # Writing object of short_nvt.mdp file
    nvtMdpOb.FileWriter(emNvtDir, conf.nvtMdpName.value)

    # Reading and writing an object of pmf.mdp file
    pmfMdpOb.pmfMdpWriter(pmfDir, conf.pmfMdpName.value, a_zDistCumulative, conf.operation.value)

    # Reading, creating an object, and writing SLURM files in em_nvt and pmf directories
    cpuHungSlurmOb.slurmFileWriter(emNvtDir, conf.cpuHungSlurmName.value, conf.pmfSimName.value+str(a_pmfSimNum)+'_em', jobSlurmName)
    cpuHungSlurmOb.slurmFileWriter(pmfDir, conf.cpuHungSlurmName.value, conf.pmfSimName.value+str(a_pmfSimNum)+'_pmf', jobSlurmName)

    gpuHungSlurmOb.slurmFileWriter(emNvtDir, conf.gpuHungSlurmName.value, conf.pmfSimName.value+str(a_pmfSimNum)+'_em', jobSlurmName)
    gpuHungSlurmOb.slurmFileWriter(pmfDir, conf.gpuHungSlurmName.value, conf.pmfSimName.value+str(a_pmfSimNum)+'_pmf', jobSlurmName)

    cpuFullnodeSlurmOb.slurmFileWriter(emNvtDir, conf.cpuFullnodeSlurmName.value, conf.pmfSimName.value+str(a_pmfSimNum)+'_em', jobSlurmName)
    cpuFullnodeSlurmOb.slurmFileWriter(pmfDir, conf.cpuFullnodeSlurmName.value, conf.pmfSimName.value+str(a_pmfSimNum)+'_pmf', jobSlurmName)

    # Doing solvation, ion insertion and EM in initial dir.
    ffg.forGMXsolvateSPC(initialDir, conf.gmxCall.value, groIniName, conf.topoIniName.value, groSolvaName, conf.outSolvate.value)
    ffg.forGMXgenions(initialDir, conf.gmxCall.value, conf.ionsMdpName.value, groSolvaName, conf.topoIniName.value,
                      conf.cation.value, conf.anion.value, movedzO, groIonsName, conf.outGenion.value)
    ffg.forGMXgrompp_EM_NVT(initialDir, conf.gmxCall.value, conf.emIniMdpName.value, groIonsName, conf.topoIniName.value,
                            tprIniEmName, conf.outGromppEmInitial.value)
    ffg.forGMXmdrun(initialDir, conf.gmxCall.value, tprIniEmName, conf.ompThreads.value, conf.outMdrunEmInitial.value)

    # Reading and creating an object of groIniEmName gro file (initial file+solvate+ions+EM)
    iniEmBoxObFU = fu.FileReader(initialDir, groIniEmName)
    iniEmBoxObGMX = gr.fromList_GROreader(iniEmBoxObFU.file)

    # Creaing the concat gro from mmtBoxName and groIniEmName, creating an object, and writing it in em_nvt dir
    groListToConcat = [mmtBoxObGMX, iniEmBoxObGMX]
    groConcatOb = gr.fromObject_GROconcat(groListToConcat, conf.zBoxAdditional.value)
    groConcatObList = fu.fromGROreaderToFileUtil(groConcatOb)
    groConcatObList.FileWriter(emNvtDir, groConcatName)

    # Reading and creating an object and wrting of topol.top file for concat gro in em_nvt and pmf dirs.
    #This topology now includes the water and ion molecules inserted by gmx.
    topoConcatOb = fu.FileReader(initialDir, conf.topoIniName.value)
    topoConcatOb.topolFileAddResid('SURF', '1', 'begin') # Adding the new molecule in mmtBoxName gro file.
    topoConcatOb.FileWriter(emNvtDir, conf.topoIniName.value)
    topoConcatOb.FileWriter(pmfDir, conf.topoIniName.value)

    # Doing EM to concat gro in em_nvt dir.
    ffg.forGMXgrompp_EM_NVT(emNvtDir, conf.gmxCall.value, conf.emMdpName.value, groConcatName, conf.topoIniName.value,
                            tprConcatEmName, conf.outGromppEm.value)
    ffg.forGMXmdrun(emNvtDir, conf.gmxCall.value, tprConcatEmName, conf.ompThreads.value, conf.outMdrunEm.value)

    # Doing NVT to concat gro in em_nvt dir.
    ffg.forGMXgrompp_EM_NVT(emNvtDir, conf.gmxCall.value, conf.nvtMdpName.value, groConcatEmName, conf.topoIniName.value,
                            tprConcatNvtName, conf.outGromppNvt.value)
    ffg.forGMXmdrun(emNvtDir, conf.gmxCall.value, tprConcatNvtName, conf.ompThreads.value, conf.outMdrunNvt.value)

    # Reading gro file output from the NVT equilibration and writing it in pmf dir.
    concatnvtBoxObList = fu.FileReader(emNvtDir, groConcatNvtName)
    concatnvtBoxObList.FileWriter(pmfDir, groConcatNvtName)

    # Getting the tpr file for the pmf and getting distance at start and distance to reference.
    gromppPmfOut = ffg.forPMFgrompp(pmfDir, conf.gmxCall.value, conf.pmfMdpName.value, groConcatNvtName, conf.topoIniName.value,
                                    tprConcatPmfName, conf.outGromppPmf.value)
    distAtStart, distToReference = gromppPmfOut[0], gromppPmfOut[1]

    print('\nDistance at start in {} is: {}\n'.format(folderName, distAtStart))
    print('\nDistance at reference in {} is: {}\n'.format(folderName, distToReference))

    # Deleting all object
    del movedzObList, movedzO, mmtBoxObGMX, iniEmBoxObFU, iniEmBoxObGMX, groConcatOb, groConcatObList, topoConcatOb, concatnvtBoxObList, groListToConcat

    return None


# =============================================================================
# GENERALITIES
# =============================================================================

# Creating the working directories
# --------------------------------
mainWorkDir = os.getcwd() # Getting the path to directory
mainFilesDir = os.path.join(mainWorkDir, conf.topolSlurmMdpFolder.value) # Folder were all required files are located

# Creating objects for files in slurm topolSlurmMdpFolder folder
#---------------------------------------------------------------
cpuHungSlurmOb = fu.FileReader(mainFilesDir, conf.cpuHungSlurmName.value)
gpuHungSlurmOb = fu.FileReader(mainFilesDir, conf.gpuHungSlurmName.value)
cpuFullnodeSlurmOb = fu.FileReader(mainFilesDir, conf.cpuFullnodeSlurmName.value)
iniBoxOb = fu.FileReader(mainFilesDir, conf.iniBoxName.value)
mmtBoxOb = fu.FileReader(mainFilesDir, conf.mmtBoxName.value)
ionsMdpOb = fu.FileReader(mainFilesDir, conf.ionsMdpName.value)
topoIniOb = fu.FileReader(mainFilesDir, conf.topoIniName.value)
emIniMdpOb = fu.FileReader(mainFilesDir, conf.emIniMdpName.value)
emMdpOb = fu.FileReader(mainFilesDir, conf.emMdpName.value)
nvtMdpOb = fu.FileReader(mainFilesDir, conf.nvtMdpName.value)
pmfMdpOb = fu.FileReader(mainFilesDir, conf.pmfMdpName.value)

# Creating the constant variables
jobSlurmName = conf.jobSlurmName.value
pmfSimNum = conf.pmfSimNum.value
zDistIni = conf.zDistIni.value
zDist = conf.zDist.value
zDistCumulative = zDistIni
pmfTotalSteps = conf.pmfTotalSteps.value


# =============================================================================
# DOING MULTIPLE PMF SECTION
# =============================================================================

processes = []

try:

    while pmfSimNum < pmfTotalSteps:
        p = multiprocessing.Process(target=run_PMF, args=[pmfSimNum, zDistCumulative])
        p.start()
        processes.append(p)

        # Moving to the next pmf folder
        zDistCumulative += zDist
        pmfSimNum += 1

    for process in processes:
        process.join()



except Exception:
    print('\n\nCaught an error:\n----------------')
    traceback.print_exc()


