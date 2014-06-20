import unittest, os, pysearch, zipfile, shutil

# Unit tests for PySearch.py utility
class TestPySearch(unittest.TestCase):
    testDirectory = "." + os.sep + "testfolder"
    testFile1 = "testfile.xyz"
     
    def setUp(self):
        if not os.path.exists(self.testDirectory):
            os.makedirs(self.testDirectory)
            os.makedirs(self.testDirectory+os.sep+"sub1")
            os.makedirs(self.testDirectory+os.sep+"sub2")
            os.makedirs(self.testDirectory+os.sep +"sub2"+ os.sep+"sub3")

        aFile = open(self.testDirectory + os.sep + self.testFile1, 'a')
        aFile.write('1234567890Ilike \ng frank cheesels in the morning\n\n')
        aFile.close()
        open(self.testDirectory + os.sep + "sub1" + os.sep + self.testFile1, 'a').close()
        open(self.testDirectory + os.sep + "sub1" + os.sep + "A"+self.testFile1, 'a').close()
        open(self.testDirectory + os.sep + "sub2" + os.sep + "bb"+self.testFile1, 'a').close()
        open(self.testDirectory + os.sep + "sub2" + os.sep + "sub3" + os.sep + "cc"+self.testFile1, 'a').close()
        open(self.testDirectory + os.sep + "sub2" + os.sep + "sub3" + os.sep + "adudfile.dud", 'a').close()
        aFile = open(self.testDirectory + os.sep + "sub2" + os.sep + "sub3" + os.sep + "dd"+self.testFile1, 'a')
        aFile.write('1234567890Ilike \ng why o why can\'t I still like to sdmake cheeserz  fkjsdfkjdsgfsdcheesels in the morning\n\n')
        aFile.close()

        #create a zip file
        aFile = open(self.testDirectory + os.sep + "testzip.txt", 'a')
        aFile.write('testing a  cheese zip file\n')
        aFile.close()
        with zipfile.ZipFile(self.testDirectory + os.sep +'spam.zip', 'w') as myzip:
            myzip.write(self.testDirectory + os.sep + 'testzip.txt')
        os.remove(self.testDirectory + os.sep + 'testzip.txt')   

        #create a 2nd zip file
        aFile = open(self.testDirectory + os.sep + "testzip2.txt", 'a')
        aFile.write('testing a  cheese zip file\n')
        aFile.close()
        with zipfile.ZipFile(self.testDirectory + os.sep + "sub2" + os.sep + "sub3" + os.sep +'spam.zip', 'w') as myzip:
            myzip.write(self.testDirectory + os.sep + 'testzip2.txt')
        os.remove(self.testDirectory + os.sep + 'testzip2.txt')   


    # will use current dir as default path
    def testNoPath(self):
       print('- testNoArgs')
       files = pysearch.fileInAPath("*.xyz")
       self.assertEqual(0, len(files))

    # with path
    def testPath(self):
       print('- testPath')
       files = pysearch.fileInAPath("*.xyz",self.testDirectory)
       self.assertEqual(1, len(files))


    # recursive paths
    def testRecursivePaths(self):
        print('- testRecursivePaths')       
        files = pysearch.filesInPath("*.xyz",self.testDirectory)
        self.assertEqual(6, len(files))


    # file size in bytes
    def testFileSize(self):
        print ('- testFileSize')
        bytes = pysearch.fileBytes(self.testDirectory + os.sep + self.testFile1)
        self.assertEqual(50,bytes)
        
    # search text in file
    def testFindText(self):
        print ('- testFindText')
        res = pysearch.findText("das",self.testDirectory + os.sep + self.testFile1)
        self.assertEqual(-1,res)

        res = pysearch.findText("4",self.testDirectory + os.sep + self.testFile1)
        self.assertEqual(3,res)

        res = pysearch.findText("cheese",self.testDirectory + os.sep + self.testFile1)
        self.assertEqual(26,res)

     # search for a text in files in a path
    def testFindTextInPath(self):
        print('- findTextInPath')

        resultFiles = pysearch.findTextInPath("cheese","*s.xyz",self.testDirectory)
        self.assertEqual(0,len(resultFiles))
 
        resultFiles = pysearch.findTextInPath("dheese","*.xyz",self.testDirectory)
        self.assertEqual(0,len(resultFiles))


        resultFiles = pysearch.findTextInPath("cheese","*.xyz",self.testDirectory)
        self.assertEqual(2,len(resultFiles))
        self.assertEqual('.\\testfolder\\testfile.xyz',resultFiles[0])
        self.assertEqual('.\\testfolder\\sub2\\sub3\\ddtestfile.xyz',resultFiles[1])

        resultFiles = pysearch.findTextInPath("frank","*.xyz",self.testDirectory)
        self.assertEqual(1,len(resultFiles))


    # test zip search
    def testZip(self):
        print ('- testZip')
        resultFiles = pysearch.findTextInPath("xcheese","*.zip",self.testDirectory)
        self.assertEqual(0,len(resultFiles))
        
        resultFiles = pysearch.findTextInPath("cheese","*.zip",self.testDirectory)
        self.assertEqual(2,len(resultFiles))
        
    # cleanup
    def tearDown(self):
        print(" ")
        shutil.rmtree(self.testDirectory)
      


if __name__ == '__main__':
    unittest.main()
