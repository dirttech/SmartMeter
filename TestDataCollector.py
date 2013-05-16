import dataCollector
import unittest



class WRITING_HEADER_Bad_Input(unittest.TestCase):

    def testIsPathEmpty(self):
        "Path should not be empty"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.WRITING_HEADER, "", "0.csv")
        
    def testIsPathNonString(self):
        "Path should be string"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.WRITING_HEADER, 1, "0.csv")

    def testIsPathExists(self):
        "Path given  should exist"
        self.assertRaises(dataCollector.PathNotExistsError, dataCollector.WRITING_HEADER, "/home/pi/pathNotExists/","0.csv")

    def testProperFileName(self):
        "File name should be proper (ends with csv)"    
        self.assertRaises(dataCollector.FaultyFileError, dataCollector.WRITING_HEADER, "/home/","abc.txt")

    def testIsFileNameEmpty(self):
        "File name should not be empty"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.WRITING_HEADER, "/home/", "")
        
    def testIsFileNameNonString(self):
        "File name should be string"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.WRITING_HEADER, "/home/", 1)

class WRITE_METER_DATA_Bad_Input(unittest.TestCase):

    def testIsPathEmpty(self):
        "Path should not be empty"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.WRITE_METER_DATA, "", "0.csv", "1,1,1,1,1,1,1,1,1,1,1,1,1\n")
        
    def testIsPathNonString(self):
        "Path should be string"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.WRITE_METER_DATA, 1, "0.csv", "1,1,1,1,1,1,1,1,1,1,1,1,1\n")

    def testIsPathExists(self):
        "Path given  should exist"
        self.assertRaises(dataCollector.PathNotExistsError, dataCollector.WRITE_METER_DATA, "/home/pi/pathNotExists/","0.csv", "1,1,1,1,1,1,1,1,1,1,1,1,1\n")

    def testProperFileName(self):
        "File name should be proper (ends with csv)"    
        self.assertRaises(dataCollector.FaultyFileError, dataCollector.WRITE_METER_DATA, "/home/","abc.txt", "1,1,1,1,1,1,1,1,1,1,1,1,1\n")

    def testIsFileNameEmpty(self):
        "File name should not be empty"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.WRITE_METER_DATA, "/home/", "", "1,1,1,1,1,1,1,1,1,1,1,1,1\n")
        
    def testIsFileNameNonString(self):
        "File name should be string"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.WRITE_METER_DATA, "/home/", 1, "1,1,1,1,1,1,1,1,1,1,1,1,1\n")

    def testIsDataInCorrectFormat(self):
        "in-correct format(check number of param and if is row end with \n?"
        self.assertRaises(dataCollector.ParamInvalidFormatError, dataCollector.WRITE_METER_DATA,"/home/", "0.csv", "1,2,3")


class FORMAT_READ_DATA_Bad_Input(unittest.TestCase):

    def testIsRegisterObjectEmpty(self):
        "Register object passed is empty"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.FORMAT_READ_DATA, "", 1)

    def testIsMeterIdNull(self):
        "Meter Id passed is null"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.FORMAT_READ_DATA, "abc", None)

    def testIsRegisterInvalidType(self):
        "Register object passed is of invalid datatype"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.FORMAT_READ_DATA, 1, 1)

    def testIsMeterIdInvalidType(self):
        "Meter Id is of wrong type"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.FORMAT_READ_DATA, "abc", "err")
"""
#have to mock register object for these test cases ! not done !

class FORMAT_READ_DATA_Bad_Output(unittest.TestCase):

    def testIfNone(self):
        "function FORMAT_READ_DATA is returning none"
        row = dataCollector.FORMAT_READ_DATA(registerObject, 1)
        self.assertIsNone(row)

    def testIfNotReturnString(self):
        "function FORMAT_READ_DATA is not returning string type"
        row = dataCollector.FORMAT_READ_DATA(registerObject, 1)
        ty = isinstance(row, str)
        self.assertFalse(ty)

    def testIfInvalidParamCount(self):
        "Number of parameters Less/More than defined value"        
        row = dataCollector.FORMAT_READ_DATA(registerObject, 1)
        no = row.count(',')
        self.assertEqual(no,13)

    def testIfNotEndsWithNewLine(self):
        "row should ends with '\n'"
        row = dataCollector.FORMAT_READ_DATA(registerObject, 1)
        suffix = "\n"
        bo = row.endswith(suffix)
        self.assertFalse(bo)
"""

class READ_METER_DATA_Bad_Input(unittest.TestCase):

    def testIfRegIndexNull(self):
        "Initial register index is null"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.READ_METER_DATA, None, 10, 1)

    def testIfRegIndexTypeInvalid(self):
        "Initial register index passed in not integer"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.READ_METER_DATA,"as", 10, 1)

    def testIfRegIndexInOutOfRange(self):
        "Initial register index is out of range"
        self.assertRaises(dataCollector.ParamOutOfRangeError, dataCollector.READ_METER_DATA, 4500, 10, 1)

    def testIfNumberOfRegistersNull(self):
        "Number of registers passed is null"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.READ_METER_DATA, 3900, None, 1)

    def testIfNumberOfRegistersTypeInvalid(self):
        "Number of registers passed is not integer"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.READ_METER_DATA, 3900, "as", 1)

    def testIfNumberOfRegistersOutOfRange(self):
        "Number of registers passed is out of range"
        self.assertRaises(dataCollector.ParamOutOfRangeError, dataCollector.READ_METER_DATA, 3900, 500, 1)

    def testIfRegIndexInInvalidFormat(self):
        "Number of registers passed should be even"
        self.assertRaises(dataCollector.ParamInvalidFormatError, dataCollector.READ_METER_DATA, 3901, 22, 1)

    def testIfNumberOfRegistersInvalidFormat(self):
        "Number of registers passed should be even"
        self.assertRaises(dataCollector.ParamInvalidFormatError, dataCollector.READ_METER_DATA, 3900, 21, 1)

    def testIfSlaveUnitNull(self):
        "Meter Id passed is null"
        self.assertRaises(dataCollector.ParamNullError, dataCollector.READ_METER_DATA, 3900, 20, None)

    def testIfSlaveUnitTypeInvalid(self):
        "Meter Id passes is of Inavild type (not integer)"
        self.assertRaises(dataCollector.ParamInvalidTypeError, dataCollector.READ_METER_DATA, 3900, 20, "as")

    def testIfSlaveUnitOutOfRange(self):
        "Meter Id should be between 1-31"
        self.assertRaises(dataCollector.ParamOutOfRangeError, dataCollector.READ_METER_DATA, 3900, 20 , 50)

"""
#have to mock register object for these test cases ! not done !

class READ_METER_DATA_Bad_Output(unittest.TestCase):

    def testIfReturningNull(self):
        "READ_METER_DATA is returning null"
        ro = dataCollector.READ_METER_DATA(3900, 20, 1)
        self.assertIsNone(row)

    def testIfReturnTypeInvalid(self):
        "READ_METER_DATA is returning value in invalid type. Expected type was:  "
        ro = dataCollector.READ_METER_DATA(3900, 20, 1)
        ty = isinstance(ro, str)
        self.assertFalse(ty)
        
"""


if __name__ == "__main__":

    unittest.main()   
