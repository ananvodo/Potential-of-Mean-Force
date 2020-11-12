#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:45:56 2019

This file contains a class to read ONLY and write ONLY files

@author: andresvodopivec
"""
import os
import GROreader

class FileUtil():
    """ FileUtil is a class to read and wrtie files ONLY """

    def __init__(self, file):
        """This is the Constructor to instanciate the object for FileUtil() class """
        self.file = file

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, file):
        """ file setter to restraint value only to a list of strings """

        if isinstance(file, list):
            if all([isinstance(element, str) for element in file]):
                self.__file = file
            else:
                raise ValueError('All elements inside file are not strings')
        else:
            raise ValueError('file is not a list')




    @classmethod
    def FileReader(cls, destinationFilePath, fileName):
        """FileUtil.FileReader is a Constructor that takes a path (/destinationFilePath/fileName) to instanciste the object. """

        if not isinstance(destinationFilePath, str) and not isinstance(fileName, str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for FuncForGMX.FileWriter() must be strings')


        print('\nReading new file with name ' + fileName + ' in directory: ' + destinationFilePath + '\n')
        filepath = os.path.join(destinationFilePath, fileName)
        fileList = []

        if not os.path.exists(filepath):
            raise FileNotFoundError('The file ' + fileName + ' in directory: ' + destinationFilePath + ' was not found.')

        else:
            with open(filepath, 'r') as fin:
                fileList = fin.readlines()

        return cls(fileList)



    def FileWriter(self, destinationFilePath, fileName):
        """FileUtil.FileWriter is an instance method that print a object to /destinationFilePath/fileName. """
        args = locals() # locals() is a function to get the arguments of a function. The output is a diccionary.

        for i in args:
            if not isinstance(destinationFilePath, str) and not isinstance(fileName, str): # Chechiing that all arguments given to the func are strings.
                raise ValueError('all arguments for FuncForGMX.FileWriter() must be strings')

        print('\nWriting the new file with name ' + fileName + ' in directory: ' + destinationFilePath + '\n')
        filepath = os.path.join(destinationFilePath, fileName)

        if not os.path.exists(destinationFilePath):
            raise FileNotFoundError('The directory: ' + destinationFilePath + ' was not found.')

        else:
            with open(filepath, 'w') as fout:
                fout.writelines(self.file)

        return None



    def pmfMdpWriter(self, destinationFilePath, fileName, fZ_dist_moving, operation):
        """
        FileUtil.slurmFileWriter is an instance method that print a object (SLURM submission file) to /destinationFilePath/fileName.
        The argument operation has to be: '- or '+' or 'none'.
        """
        if (not isinstance(destinationFilePath, str) and not isinstance(fileName, str) and not isinstance(operation, str)
            (not isinstance(fZ_dist_moving, str) or not isinstance(fZ_dist_moving, float))):
            raise ValueError('Argument in FileUtil.pmfMdpWriter() are not the right type')

        filepath = os.path.join(destinationFilePath, fileName)
        print('\nWriting new ' + fileName + 'for current simulation in directory: ' + destinationFilePath + '\n')

        if not os.path.exists(destinationFilePath):
            raise FileNotFoundError('The directory: ' + destinationFilePath + ' was not found.')

        else:
            if operation == '-':
                with open(filepath, 'w') as fo:
                    for line in self.file:
                        try:
                            if line.find('-init') > 0:
                               old_value = line[27:]
                               new_value = '{:>5.3f}\n'.format(float(old_value) - float(fZ_dist_moving))
                               line = line.replace(old_value, new_value, 1)
                        finally:
                            fo.write(line)
            elif operation == '+':
                with open(filepath, 'w') as fo:
                    for line in self.file:
                        try:
                            if line.find('-init') > 0:
                               old_value = line[27:]
                               new_value = '{:>5.3f}\n'.format(float(old_value) + float(fZ_dist_moving))
                               line = line.replace(old_value, new_value, 1)
                        finally:
                            fo.write(line)
            else:
                raise Exception("Argument operation in FileUtil.pmfMdpWriter() must be '+' or '-'. If just c/p is needed use FileUtil.FileWriter() func.")

        return None




    def slurmFileWriter(self, destinationFilePath, slurmFileName, newJobSlurmName, jobSlurmName):
        """FileUtil.slurmFileWriter is an instance method that print a object (SLURM submission file) to /destinationFilePath/fileName."""

        if (not isinstance(destinationFilePath, str) and not isinstance(slurmFileName, str)
            and not isinstance(newJobSlurmName, str)): # Chechiing that all arguments given to the func are strings.
            raise ValueError('all arguments for FuncForGMX.slurmFileWriter() must be strings')

        filepath = os.path.join(destinationFilePath, slurmFileName)
        print('\nWriting the new slurmFileName for current simulation in directory: ' + destinationFilePath + '\n')
        new_slurm = []

        for line in self.file:
            line = line.replace(jobSlurmName, newJobSlurmName, 1)
            new_slurm.append(line)

        if not os.path.exists(destinationFilePath):
            raise FileNotFoundError('The directory: ' + destinationFilePath + ' was not found.')

        else:
            with open(filepath, 'w') as fo: # naming the output with the same input file in order to replace the .slurm with the new value
                fo.writelines(new_slurm)

        return None




    def topolFileAddResid(self,residName, residNum, position):
        """
        FileUtil.topolFileAddResid is an instance method that MODIFIES a topology file object.
        The arguments are:
            residName (residue name)
            residNum (total number of residues for the specific residue
            position (must type 'begin' to insert the new residue at the begining of the topology molecules' section
                      or 'end' to place it at the end of the topology molecules' section.
        """

        if not isinstance(residName, str) and not isinstance(residNum, str) and not isinstance(position, str): # Chechiing that all arguments given to the func are strings.
            raise ValueError('all arguments for FuncForGMX.topolFileWriter() must be strings')


        print('\nAdding new residName due to concatenation in topol.top\n')
        stringToAdd = '\n{}               {}\n'.format(residName,str(residNum))

        file = []
        wordCounter = 0
        for line in self.file:
            if line.find('; Compound') >= 0 or line.find(';Compound') >= 0:
                wordCounter += 1

        if position == 'begin' and wordCounter > 0:
            for line in self.file:
                file.append(line)
                if line.find('; Compound') >= 0 or line.find(';Compound') >= 0:
                    file.append(stringToAdd)
            self.file = file

        elif position == 'begin' and wordCounter <= 0:
            for line in self.file:
                file.append(line)
                if line.find('[ molecules ]') >= 0 or line.find('[molecules]') >= 0:
                    file.append(stringToAdd)
            self.file = file

        elif position == 'end':
            (self.file).append(stringToAdd)

        else:
            raise Exception('''As position argument in function FileUtil.topolFileAddResid() you must type 'begin' or 'end'.
                            If you inserted 'begin' or 'end' correctly then there is a format error in your original topology file.
                            IMPORTANT: Your original topology file has not being modified.''')

        return None



    @classmethod
    def fromGROreaderToFileUtil(cls, groFileObject):

        if not isinstance(groFileObject, GROreader.GROreader): # Chechiing that all arguments given to the func are strings.
            raise ValueError('\ngroFileObject argument in FileUtil.fromGROreaderToFileUtil() must be GROreader Object\n')


        print('\nCreating the new gro file list as FileUtil Object\n')
        gro_format = '%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n'
        box_dim_format = '%10.5f%10.5f%10.5f\n'
        totalSystemAtoms = groFileObject._GROreader__totalSystemAtoms
        residNum = groFileObject._GROreader__residNum
        residType = groFileObject._GROreader__residType
        atomType = groFileObject._GROreader__atomType
        atomNum = groFileObject._GROreader__atomNum
        xCoord = groFileObject._GROreader__xCoord
        yCoord = groFileObject._GROreader__yCoord
        zCoord = groFileObject._GROreader__zCoord
        xDim = groFileObject._GROreader__xDim
        yDim = groFileObject._GROreader__yDim
        zDim = groFileObject._GROreader__zDim

        fileList = []
        fileList.append('This is a box printed by FileUtil class (created by AVK on Feb 27, 2019)\n')
        fileList.append('{}\n'.format(str(totalSystemAtoms)))

        for i in range(0, len(residNum)):
            stringToAdd = gro_format%(residNum[i], residType[i], atomType[i], atomNum[i], xCoord[i], yCoord[i], zCoord[i])
            fileList.append(stringToAdd)

        fileList.append(box_dim_format%(xDim, yDim, zDim))

        return cls(fileList)


    def __del__(self):
        print("freeing memory by deleting FileUtil object")
        # This is my destructor (it is not mandatory for python)

#lista = []
#my_file = FileUtil.FileReader('/Users/andresvodopivec/Downloads', 'topol.top')
#
#lista = [my_file]
#
#my_file.FileWriter('/Users/andresvodopivec/Downloads', 'output.gro')
#
#my_file.topolFileAddResid('SURF', '1', 'begin')
#
#my_file.FileWriter('/Users/andresvodopivec/Downloads', 'output.gro')
