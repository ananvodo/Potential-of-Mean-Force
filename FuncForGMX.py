#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:45:56 2019

This file contains GMX command lines for EM, NVT and PMF simulations.
Also functions to copy/paste files required for the PMF procedure

@author: andresvodopivec
"""

import os
import shutil
import shlex, subprocess
from scipy import constants
import GROreader
from FileUtil import FileUtil as fu


class FuncForGMX():
    """ FuncForGMX is a class to call GMX programs """

    def __init__(self):
        print("Using static function from FuncForGMX class")
        # This is my constructor (it is not mandatory for python)

    @staticmethod
    def forMkDirs(mainPath, simName, simNum):
        """
        Function FuncForGMX.forMkDirs() creates the directories for the pmf simulation.
        The arguments are: mainPath, simName and simNum.
        mainpath is the main oath were all the simulation pmf folders will be created.
        simName is the pmf simulation name. Example: MMT
        simNum is the pmf simulation number. Must be a string too.
        This three areguments will create a directory: /mainPath/simName_simNum.
        This function returns the Initial Directory, EM_NVT directory and PMF directory
        for the current simulation number.
        This function returns: pathInitialDir, pathEM_NVT_Dir, pathPMFdir
        pathInitialDir is the Initial folder were the solvation, genion and concatenation will take place.
        pathEM_NVT_Dir is the EM and NVT folder is were Em and NVT simulation takes place.
        pathPMFdir is the PMF folder is were PMF simulation takes place.
        If directories already exist they WILL be DELETED.
        """
        args = locals() # locals() is a function to get the arguments of a function. The output is a diccionary.

        for i in args:
            if not isinstance(args[i], str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for FuncForGMX.forMkDirs() must be strings')

        mainDir = os.path.join(mainPath, simName + str(simNum) + '_pmf')

        if os.path.exists(mainDir):
            shutil.rmtree(mainDir)
        else:
            pass

        pathInitialDir = os.path.join(mainDir, 'initial')
        pathEM_NVT_Dir = os.path.join(mainDir, 'em_nvt')
        pathPMFdir = os.path.join(mainDir, 'pmf')

        os.makedirs(pathInitialDir)
        os.makedirs(pathEM_NVT_Dir)
        os.makedirs(pathPMFdir)

        print('\nCreated directory: ' + pathInitialDir)
        print('\nCreated directory: ' + pathEM_NVT_Dir)
        print('\nCreated directory: ' + pathPMFdir)

        return pathInitialDir, pathEM_NVT_Dir, pathPMFdir


    @staticmethod
    def forGMXgrompp_EM_NVT(pathEM_NVT_Dir, gmxExtension, mdpName, groName, topolName, outNameTPR, outputTxt):
        """
        Function FuncForGMX.forGMXgrompp_EM_NVT() does the gmx grompp command line for EM and NVT.
        The arguments are: pathDir_EM_NVT, gmxExtension, mdpName, groName, topolName, outNameTPR.
        pathDir_EM_NVT is the path to the EM_NVT directory.
        gmxExtension is the way gmx is called. Example: gmx, gmx_mpi. /usr/local/bin/gmx, etc.
        The rest of arguments to be inserted ONLY as the wanted names and NOT paths. Example: topol.top.
        """
        args = locals() # locals() is a function to get the arguments of a function. The output is a diccionary.

        for i in args:
            if not isinstance(args[i], str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for FuncForGMX.forGMXgrompp_EM_NVT() must be strings')

        os.chdir(pathEM_NVT_Dir) # Changing directory to EM and NVT folder
        cmdline = '{} grompp -f {} -c {} -p {} -o {} -maxwarn 2'.format(gmxExtension, mdpName, groName, topolName, outNameTPR, outputTxt)
        print('\nDoing gmx grompp for EM_NVT in directory: ' + pathEM_NVT_Dir + '\n')
        print('\nThe gmx command line is: ' + cmdline + '\n')
        args = shlex.split(cmdline)
        gmxOutFile = open(outputTxt, 'w')
        proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=gmxOutFile)
        streamdata = proc.communicate()
        outproc = proc.returncode
        gmxOutFile.close()

        if outproc != 0:
            raise Exception('gmx grompp in command line from FuncForGMX.forGMXsolvateSPC() failed')

        del proc, outproc, streamdata

        return None


    @staticmethod
    def forGMXsolvateSPC(pathInitialDir, gmxExtension, groName, topolName, outNameGro, outputTxt):
        """
        Function FuncForGMX.forGMXsolvateSPC() returns the gmx solvate output as a list of strings
        It solvates ONLY with spc216.gro.
        """
        args = locals() # locals() is a function to get the arguments of a function. The output is a diccionary.

        for i in args:
            if not isinstance(args[i], str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for forGMXsolvateSPC.forGMXsolvateSPC() must be strings')

        os.chdir(pathInitialDir) # Changing directory to Initial folder
        cmdline = '{} solvate -cp {} -cs spc216.gro -p {} -o {}'.format(gmxExtension, groName, topolName, outNameGro, outputTxt)
        print('\nDoing gmx solvate in Intitial directory: ' + pathInitialDir + '\n')
        print('\nThe gmx command line is: ' + cmdline + '\n')
        args = shlex.split(cmdline)
        gmxOutFile = open(outputTxt, 'w')
        proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=gmxOutFile)
        streamdata = proc.communicate()
        outproc = proc.returncode
        gmxOutFile.close()

        if outproc != 0:
            raise Exception('gmx grompp in command line from FuncForGMX.forGMXsolvateSPC() failed')

        del proc, outproc, streamdata

        return None



    @staticmethod
    def forGMXgenions(pathInitialDir, gmxExtension, mdpName, groToInsertIonsName, topolName, cationName, anionName, groFileObject, outNameGro, outputTxt):
        """ Function FuncForGMX.forGMXgenions() returns the gmx genions output as a list of strings """

        if (isinstance(pathInitialDir, str) and isinstance(gmxExtension, str) and isinstance(mdpName, str) and isinstance(topolName, str)
            and isinstance(cationName, str) and isinstance(anionName, str) and isinstance(groFileObject, GROreader.GROreader)
            and isinstance(outNameGro, str) and isinstance(groToInsertIonsName, str)):
            pass

        else:
             raise ValueError('incorrect argument types for FuncForGMX.forGMXgenions()')


        # Defining constants and variables
        boxXdim = groFileObject._GROreader__xDim
        boxYdim = groFileObject._GROreader__yDim
        boxZdim = groFileObject._GROreader__zDim

        ionConcen = 0.45 # mol/liters
        boxVolume = (boxXdim * boxYdim * boxZdim) * 1e-024 # converting nm3 to liters
        avogadroNum = constants.N_A
        ionsNum = int(round(ionConcen * boxVolume * avogadroNum)) # Number of cations and anions to insert in the system. In total would be 2*ionsNum.

        # For gmx grompp cmdline
        os.chdir(pathInitialDir)
        gromppCMDline = '{} grompp -f {} -c {} -p {} -o ions.tpr'.format(gmxExtension, mdpName, groToInsertIonsName, topolName, outputTxt)
        print('\nDoing gmx grompp for inserting ions in Intitial directory: ' + pathInitialDir + '\n')
        print('\nThe gmx command line is: ' + gromppCMDline + '\n')
        gmxOutFileGrompp = open(outputTxt, 'w')
        argsGrompp = shlex.split(gromppCMDline)
        procGrompp = subprocess.Popen(argsGrompp, stderr=subprocess.STDOUT, stdout=gmxOutFileGrompp)
        streamdataGrompp = procGrompp.communicate()
        outprocGrompp = procGrompp.returncode
        gmxOutFileGrompp.close()

        if outprocGrompp != 0:
            raise Exception('gmx grompp in command line from FuncForGMX.forGMXgenions() failed')

        # For gmx genion cmdline
        genionCMDline = '{} genion -s ions.tpr -o {} -p {} -pname {} -nname {} -np {} -nn {} -neutral'.format(gmxExtension, outNameGro, topolName, cationName, anionName, ionsNum, ionsNum, outputTxt)
        print('\nDoing gmx grompp for inserting ions in Intitial directory: ' + pathInitialDir + '\n')
        print('\nThe gmx command line is: ' + genionCMDline + '\n')
        gmxOutFileGenion = open(outputTxt, 'w')
        argsGenion = shlex.split(genionCMDline)
        procGenion = subprocess.Popen(argsGenion, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=gmxOutFileGenion)
        streamdataGenion = procGenion.communicate(input=b'SOL')
        outprocGenion = procGenion.returncode
        gmxOutFileGenion.close()

        if outprocGenion != 0:
            raise Exception('gmx grompp in command line from FuncForGMX.forGMXgenions() failed')

        del procGrompp, streamdataGrompp, outprocGrompp, procGenion, streamdataGenion, outprocGenion

        return None



    @staticmethod
    def forGMXmdrun(mainPath, gmxExtension, tprName, ntomp, outputTxt):
        """
        Function to do the gmx mdrun.
        The agruments are gmxExtension, mainPath, tprName.
        gmxExtension is how gromacs is called in the OS system. Include 'mpirun -n xx gmx' if needed.
        mainPath is the path were the tpr file is located.
        tprName is the tpr file name.
        The workdir will be /mainPath/tprName.
        """
        args = locals() # locals() is a function to get the arguments of a function. The output is a diccionary.
        for i in args:
            if not isinstance(args[i], str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for FuncForGMX.forGMXmdrun() must be strings')

        tprPath = os.path.join(mainPath, tprName)
        os.chdir(mainPath)
        cmdline = '{} mdrun -ntomp {} -v -deffnm {}'.format(gmxExtension, str(ntomp), tprName[:-4], outputTxt)
        print('\nDoing gmx mdrun for in directory: ' + tprPath + '\n')
        print('\nThe gmx command line is: ' + cmdline + '\n')
        args = shlex.split(cmdline)
        gmxOutFile = open(outputTxt, 'w')
        proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=gmxOutFile)
        streamdata = proc.communicate()
        outproc = proc.returncode
        gmxOutFile.close()

        if outproc != 0:
            raise Exception('gmx grompp in command line from FuncForGMX.forGMXmdrun() failed')

        del proc, outproc, streamdata

        return None



    @staticmethod
    def forPMFgrompp(pathPMFdir, gmxExtension, mdpName, groName, topolName, outNameTPR, outputTxt):
        """
        Function FuncForGMX.forPMFgrompp() does the gmx grompp command line for the PMF.
        The arguments are: pathDir_EM_NVT, gmxExtension, mdpName, groName, topolName, outNameTPR.
        pathPMFdir is the path to the PMF directory.
        gmxExtension is the way gmx is called. Example: gmx, gmx_mpi. /usr/local/bin/gmx, etc.
        The rest of arguments to be inserted ONLY as the wanted names and NOT paths. Example: topol.top.
        This func returns distAtStart and distToReference for further evaluation.
        """
        args = locals() # locals() is a function to get the arguments of a function. The output is a diccionary.

        for i in args:
            if not isinstance(args[i], str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for FuncForGMX.forPMFgrompp() must be strings')

        os.chdir(pathPMFdir)
        cmdline = '{} grompp -f {} -c {} -p {} -o {} -maxwarn 2'.format(gmxExtension, mdpName, groName, topolName, outNameTPR, outputTxt)
        print('\nDoing gmx grompp for PMF in PMF directory: ' + pathPMFdir + '\n')
        print('\nThe gmx command line is: ' + cmdline + '\n')
        args = shlex.split(cmdline)
        gmxOutFile = open(outputTxt, 'w')
        proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=gmxOutFile)
        streamdata = proc.communicate()
        outproc = proc.returncode
        gmxOutFile.close()

        if outproc != 0:
            raise Exception('gmx grompp in command line from FuncForGMX.forPMFgrompp() failed')

        gmxOutFileObject = fu.FileReader(pathPMFdir, outputTxt)
        for line in range(0, len(gmxOutFileObject.file)):
            if gmxOutFileObject.file[line][0:8] == 'Estimate': # Taking this word as reference for the line that is really needed.
                parts = gmxOutFileObject.file[line - 1].split() # line-1 is the line were the variable needed are.
                distAtStart, distToReference = float(parts[3]), float(parts[5])

        del proc, outproc, streamdata, gmxOutFileObject

        return distAtStart, distToReference


    def __del__(self):
        print("freeing memory by deleting FileUitl object")
        # This is my destructor (it is not mandatory for python)

#forMkDirs('/Users/andresvodopivec/Downloads', 'sim', '1')

#out = forGMXgrompp_EM_NVT('/Users/andresvodopivec/Downloads/pmf_CNC_trials/xy0_pmf', '/usr/local/bin/gmx', '../topologies_mpd/em.mdp', 'xy0_em.gro',
#                    '../topologies_mpd/topol.top', 'trial.tpr')

#solvate = forGMXsolvateSPC('/Users/andresvodopivec/Downloads/pmf_CNC_trials/xy0_pmf', '/usr/local/bin/gmx', 'xy0_em.gro', '../topologies_mpd/topol.top', 'solva.gro')

#geions = forGMXgenions('/Users/andresvodopivec/Downloads/pmf_CNC_trials/xy0_pmf', '/usr/local/bin/gmx', '../topologies_mpd/ions.mdp', 'solva.gro',
#                       '../topologies_mpd/topol.top', 'NA', 'CL', 10.38360, 10.81840, 40.00460, 'trail.gro')

#grompp = forPMFgrompp('/Users/andresvodopivec/Downloads/pmf_CNC_trials/xy0_pmf/pmf_run', '/usr/local/bin/gmx', 'pmf.mdp', 'xy0_nvt.gro', '../../topologies_mpd/topol.top', 'trial_frompy.tpr')

#mdrun = forGMXmdrun('/usr/local/bin/gmx', '/Users/andresvodopivec/Downloads/pmf_CNC_trials/xy0_pmf/pmf_run', 'trial_frompy.tpr', '1')

#proc2 = subprocess.check_output(["/usr/local/bin/gmx", "grompp", "-h"], stderr=subprocess.STDOUT)



