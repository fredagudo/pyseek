# File search utility

import glob, zipfile, os, tempfile

ISTRUE = [True, 1, '1', 'true', 't', 'yes', 'y']

# Return list of files in path matching the pattern
def fileInAPath(filePattern,path = ".", printResult = False):
    fileList = []
    for x in glob.glob(path + os.sep + filePattern) :
        if os.path.isfile(x) in ISTRUE :
           fileList.append(x)

    if printResult in ISTRUE:
        print(fileList)
        
    return fileList


# Return list of files in recursive paths matching the pattern
def filesInPath(filePattern = "*.py",path = ".", printResult = False):
    print("searching : ");
    fileList = []
    
    for root, dirs, files in os.walk(path, topdown=True):
        print(" " , root)
        result = fileInAPath(filePattern,root)
        fileList.extend(result)
        #print(len(fileList))

    #print(fileList)
    return fileList 


# Search for a text within a file and return an array of line numbers
def findText(searchString, fname):

    #if as zip file find first occurence in zip then return
    if fname.endswith('.zip') :
        z = zipfile.ZipFile(fname, "r")
        print ("  " + fname)           
        for filename in z.namelist():           #if a zip file, copy to tmp file first 
            print ("      " +  filename)           
            bytes = z.read(filename)
            fp = tempfile.TemporaryFile(delete=False)
            fp.write(bytes)
           
            #print('.name = ' + fp.name)
            fname = fp.name
            fp.close()
            return searchInFile(fname,searchString)
    else:
        return searchInFile(fname,searchString)
          
# search in a binary opened file
def searchInFile(fname,searchString):
    start = 0
    bText = str.encode(searchString) #convert search string to binary
    with open(fname, 'rb') as f:
        if len(bText) > 4096:
            raise Exception("Search text too large")
        
        fsize = os.path.getsize(fname)
        bsize = 4096
        buffer = None
        if start > 0:
            f.seek(bText)
        overlap = len(bText) - 1
        while True:
            if (f.tell() >= overlap and f.tell() < fsize):
                f.seek(f.tell() - overlap)
            buffer = f.read(bsize)
            if buffer:
                pos = buffer.find(bText)
                if pos >= 0:
                    return f.tell() - (len(buffer) - pos)
            else:
                return -1




# byte size of file
def fileBytes(filename):
    return len(open(filename, encoding='utf-8').read())

# returns array of files that have a text in the path
def findTextInPath(searchString, filePattern, path):
    files = filesInPath(filePattern,path)
    resultFiles = []
    for f in files:
        bpos = findText(searchString,f)
        #print("1-",bpos)
        if bpos > -1:
            resultFiles.append(f)
            
    return resultFiles      
        

def main():
    print('#################################################')
    str = 'Utilities for file searching'
    print(str.rjust(35,' '))
    print("fileInAPath(filepattern, [path], [output result] - returns a list of files matching this pattern") 
    print("fileInPath(filepattern, paths, [output result]  - returns a list of files matching this pattern recursivley")
    print("fileBytes(filename) - returns number of bytes in a file")
    print("findText(searchString, fname) - returns byte")
    print('#################################################')
      
    

if __name__ == "__main__":
    main()
