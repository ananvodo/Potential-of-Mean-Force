#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:45:56 2019

This file contains a class that contains GMX GRO elements

@author: andresvodopivec
"""

class GROreader():
    """ GROreader class is a class to process and create .gro file objects from a list ONLY """

    def __init__(self, totalSystemAtoms, residNum, residType, atomType, atomNum, xCoord, yCoord, zCoord, xDim, yDim, zDim):
        """This is the Constructor to instanciate the object for GROreader() class"""
        self.totalSystemAtoms = totalSystemAtoms
        self.residNum = residNum
        self.residType = residType
        self.atomType = atomType
        self.atomNum = atomNum
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.zCoord = zCoord
        self.xDim = xDim
        self.yDim = yDim
        self.zDim = zDim


    @property
    def totalSystemAtoms(self):
        return self.__totalSystemAtoms

    @totalSystemAtoms.setter
    def totalSystemAtoms(self, totalSystemAtoms):
        """ totalSystemAtoms setter to restraint value only to integer """

        if isinstance(totalSystemAtoms, int):
            self.__totalSystemAtoms = totalSystemAtoms
        else:
            raise ValueError('totalSystemAtoms is not an integer')


    @property
    def residNum(self):
        return self.__residNum

    @residNum.setter
    def residNum(self, residNum):
        """ residNum setter to restraint value only to list """

        if isinstance(residNum, list):
            if all([isinstance(element, int) for element in residNum]):
                self.__residNum = residNum
            else:
                raise ValueError('All elements inside residNum are not integers')
        else:
            raise ValueError('residNum is not a list')


    @property
    def residType(self):
        return self.__residType

    @residType.setter
    def residType(self, residType):
        """ residType setter to restraint value only to list """

        if isinstance(residType, list):
            if all([isinstance(element, str) for element in residType]):
                self.__residType = residType
            else:
                raise ValueError('All elements inside residType are not strings')
        else:
            raise ValueError('residType is not a list')


    @property
    def atomType(self):
        return self.__atomType

    @atomType.setter
    def atomType(self, atomType):
        """ atomType setter to restraint value only to list """

        if isinstance(atomType, list):
            if all([isinstance(element, str) for element in atomType]):
                self.__atomType = atomType
            else:
                raise ValueError('All elements inside atomType are not strings')
        else:
            raise ValueError('atomType is not a list')


    @property
    def atomNum(self):
        return self.__atomNum

    @atomNum.setter
    def atomNum(self, atomNum):
        """ atomNum setter to restraint value only to list """

        if isinstance(atomNum, list):
            if all([isinstance(element, int) for element in atomNum]):
                self.__atomNum = atomNum
            else:
                raise ValueError('All elements inside atomNum are not integers')
        else:
            raise ValueError('atomNum is not a list')


    @property
    def xCoord(self):
        return self.__xCoord

    @xCoord.setter
    def xCoord(self, xCoord):
        """ xCoord setter to restraint value only to list """

        if isinstance(xCoord, list):
            if all([isinstance(element, float) for element in xCoord]):
                self.__xCoord = xCoord
            else:
                raise ValueError('All elements inside xCoord are not float')
        else:
            raise ValueError('xCoord is not a list')


    @property
    def yCoord(self):
        return self.__yCoord

    @yCoord.setter
    def yCoord(self, yCoord):
        """ yCoord setter to restraint value only to list """

        if isinstance(yCoord, list):
            if all([isinstance(element, float) for element in yCoord]):
                self.__yCoord = yCoord
            else:
                raise ValueError('All elements inside yCoord are not float')
        else:
            raise ValueError('yCoord is not a list')


    @property
    def zCoord(self):
        return self.__zCoord

    @zCoord.setter
    def zCoord(self, zCoord):
        """ zCoord setter to restraint value only to list """

        if isinstance(zCoord, list):
            if all([isinstance(element, float) for element in zCoord]):
                self.__zCoord = zCoord
            else:
                raise ValueError('All elements inside zCoord are not float')
        else:
            raise ValueError('zCoord is not a list')


    @property
    def xDim(self):
        return self.__xDim

    @xDim.setter
    def xDim(self, xDim):
        """ xDim setter to restraint value only to float """

        if isinstance(xDim, float):
            self.__xDim = xDim
        else:
            raise ValueError('xDim is not a float')


    @property
    def yDim(self):
        return self.__yDim

    @yDim.setter
    def yDim(self, yDim):
        """ yDim setter to restraint value only to float """

        if isinstance(yDim, float):
            self.__yDim = yDim
        else:
            raise ValueError('yDim is not a float')


    @property
    def zDim(self):
        return self.__zDim

    @zDim.setter
    def zDim(self, zDim):
        """ zDim setter to restraint value only to float """

        if isinstance(zDim, float):
            self.__zDim = zDim
        else:
            raise ValueError('zDim is not a float')


    @classmethod
    def fromList_GROreader(cls, grofile):
        """ fromList_GROreader is a Constructor that takes the gro file as the argument.
        The grofile must be a list type.
        Example how to use it:
            myGro = GROreader.fromList_GROreader(grofile)
            print(myGro.yDim)  # in case you want to print content
        """

        if isinstance(grofile, list):
            pass
            if all([isinstance(element, str) for element in grofile]):
                pass
            else:
                raise ValueError('Argument in GROreader.fromList_GROreader() is not a list of strings')
        else:
            raise ValueError('Argument in GROreader.fromList_GROreader() is not a list')

        # Initializing all variables that will be used
        totalSystemAtoms = 0
        residNum = []
        residType = []
        atomType = []
        atomNum = []
        xCoord = []
        yCoord = []
        zCoord = []
        xDim = 0
        yDim = 0
        zDim = 0

        # Saving the first line to get the total atoms in the system
        totalSystemAtoms = int(grofile[1].strip())

        # Making the lists of each variable accordingly to the spaces stated by GMX standard format.
        for line in range(2, len(grofile) - 1):

            residNum.append(int(grofile[line][0:5].strip()))
            residType.append(grofile[line][5:10].strip())
            atomType.append(grofile[line][10:15].strip())
            atomNum.append(int(grofile[line][15:20].strip()))
            xCoord.append(float(grofile[line][20:28].strip()))
            yCoord.append(float(grofile[line][28:36].strip()))
            zCoord.append(float(grofile[line][36:44].strip()))

        lastline = grofile[-1].split()
        xDim = float(lastline[0])
        yDim = float(lastline[1])
        zDim = float(lastline[2])

        return cls(totalSystemAtoms, residNum, residType, atomType, atomNum, xCoord, yCoord, zCoord, xDim, yDim, zDim)


    @classmethod
    def fromList_GROreader_Zmoving(cls, grofile, ZmovingDist, residTypesList, math_op):
        """ fromList_GROreader_Zmoving is a Constructor that takes as arguments:
            - grofile which is a GMX gro file as a list type.
            - ZmovingDist which is a float number for moving molecules in Z direction ONLY.
            - residTypesList which is a list of the residues you want to move or insert "all"
              if all residues want to be moved.
            - math_op which is the math operation to add or substract ZmovingDist.
              User must insert the word "+" or "-" for the value of math_op.
        If no moving distance is required please use fromList_GROreader() instead.
        Example how to use it:
            myGro = GROreader.fromList_GROreader_Zmoving(grofile)
            print(myGro.yDim)  # in case you want to print content
        """

        if isinstance(grofile, list):
            pass
        else:
            raise ValueError('Argument in grofile of GROreader.fromList_GROreader_Zmoving() is not a list')

        if isinstance(ZmovingDist, float) or isinstance(ZmovingDist, int):
            pass
        else:
            raise ValueError('Argument in ZmovingDist of GROreader.fromList_GROreader_Zmoving() is not a float')

        if math_op == "+" or math_op == "-":
            pass
        else:
            raise ValueError("Argument in ZmovingDist of GROreader.fromList_GROreader_Zmoving() must be '+' or '-' or 'none'")

        if isinstance(residTypesList, list):
            if all([isinstance(element, str) for element in residTypesList]):
                pass
            else:
                raise ValueError('All elements inside residTypesList are not string')
        elif residTypesList == "all":
            pass
        else:
            raise ValueError("Argument in residTypesList of GROreader.fromList_GROreader_Zmoving() is not a list nor 'all'")

        # Initializing all variables that will be used
        totalSystemAtoms = 0
        residNum = []
        residType = []
        atomType = []
        atomNum = []
        xCoord = []
        yCoord = []
        zCoord = []
        xDim = 0
        yDim = 0
        zDim = 0
        print('\nCreating new gro object with name using GROreader.fromList_GROreader_Zmoving()' + '\n')
        # Saving the first line to get the total atoms in the system
        totalSystemAtoms = int(grofile[1].strip())

        # Making the lists of each variable accordingly to the spaces stated by GMX standard format.
        for line in range(2, len(grofile) - 1):

            residNum.append(int(grofile[line][0:5].strip()))
            residType.append(grofile[line][5:10].strip())
            atomType.append(grofile[line][10:15].strip())
            atomNum.append(int(grofile[line][15:20].strip()))
            xCoord.append(float(grofile[line][20:28].strip()))
            yCoord.append(float(grofile[line][28:36].strip()))
            zCoord.append(float(grofile[line][36:44].strip()))

        lastline = grofile[-1].split()
        xDim = float(lastline[0])
        yDim = float(lastline[1])
        zDim = float(lastline[2])

        if math_op == "+":
            if isinstance(residTypesList, list):
                for element in residTypesList:
                    for  item in range(0, len(residType)):
                        if element == residType[item]:
                            zCoord[item] = zCoord[item] + ZmovingDist

            if residTypesList == "all":
                zCoord = [(num + ZmovingDist) for num in zCoord]

        elif math_op == "-":
            if isinstance(residTypesList, list):
                for element in residTypesList:
                    for  item in range(0, len(residType)):
                        if element == residType[item]:
                            zCoord[item] = zCoord[item] - ZmovingDist

            if residTypesList == "all":
                zCoord = [(num - ZmovingDist) for num in zCoord]

        return cls(totalSystemAtoms, residNum, residType, atomType, atomNum, xCoord, yCoord, zCoord, xDim, yDim, zDim)


    @classmethod
    def fromObject_GROconcat(cls, objectList, boxZextension):
        """ fromObject_GROconcat is a Constructor that takes a list of grofile objects as first argument.
        The argument boxExtension is the addition space that is to be left between the +Z edge and the
        last molecule.
        It return a single concatenated grofile.
        Order matters. The first grofile object in the list will be first and last objecet will
        be last.
        The grofile objects must comply with the class attribute's format.
        Example how to use it:
            groConcat = GROreader.fromObject_GROconcat(grofile)
            print(groConcat.yDim)       # in case you want to print content
        """

        if isinstance(objectList, list):
            pass
        else:
            raise ValueError('Argument in GROreader.fromObject_GROconcat() is not a list')

        # Initializing all variables that will be used
        totalSystemAtoms = 0
        residNum = []
        residType = []
        atomType = []
        atomNum = 0
        xCoord = []
        yCoord = []
        zCoord = []
        xDim = 0
        yDim = 0
        zDim = 0
        lastNum = 0          # to store the last number of each residNum object
        buffer = 0.1        # leave a small buffer to avoid posible molecule overlapping
        addToZcoord = 0
        atomCount = []

        for groObject in objectList:

            totalSystemAtoms = totalSystemAtoms + groObject.totalSystemAtoms

            residNum.extend([(num + lastNum) for num in groObject.residNum])
            lastNum = residNum[-1]

            residType.extend(groObject.residType)

            atomType.extend(groObject.atomType)

            atomNum = len(groObject.atomNum) + atomNum

            xCoord.extend(groObject.xCoord)

            yCoord.extend(groObject.yCoord)

            zCoord.extend([(num + addToZcoord + buffer) for num in groObject.zCoord])
            addToZcoord = max(zCoord)

            if groObject.xDim > xDim:
                xDim = groObject.xDim
            else:
                xDim = xDim

            if groObject.yDim > yDim:
                yDim = groObject.yDim
            else:
                yDim = yDim

        atomNumLess100k = 1
        atomNumHigher100k = 1
        for item in range(1, atomNum + 1):        # atom are counted from number 1
            if item <= 99999:
                atomCount.append(atomNumLess100k)
                atomNumLess100k += 1
            else:
                atomCount.append(atomNumHigher100k)
                atomNumHigher100k += 1

        atomNum = atomCount
        zDim = max(zCoord) + int(boxZextension)

        return cls(totalSystemAtoms, residNum, residType, atomType, atomNum, xCoord, yCoord, zCoord, xDim, yDim, zDim)


    def __del__(self):
        print("freeing memory by deleting GROreader object")
        # This is my destructor (it is not mandatory for python)


#lista = "all"
#
#with open ('/Users/andresvodopivec/Downloads/file1.gro', 'r') as fin:
#    file1 = fin.readlines()
#gro1 = GROreader.fromList_GROreader_Zmoving(file1, 10, lista, "+")
#
#with open ('/Users/andresvodopivec/Downloads/file2.gro', 'r') as fin:
#    file2 = fin.readlines()
#gro2 = GROreader.fromList_GROreader(file2)
#
#with open ('/Users/andresvodopivec/Downloads/file3.gro', 'r') as fin:
#    file3 = fin.readlines()
#gro3 = GROreader.fromList_GROreader(file3)
#
#
#groList = [gro1, gro2, gro3]
#
#groconcat = GROreader.fromObject_GROconcat(groList, 20)
#
#objecto = [groconcat]

































