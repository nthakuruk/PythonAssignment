import re
from pathlib import PurePosixPath

# Dictionary to identify individual score for each letter
scoredictionary = {"Q":1,
            "Z":1,
            "J":3,
            "X":3,
            "K":6,
            "F":7,
            "H":7,
            "V":7,
            "W":7,
            "Y":7,
            "B":8,
            "C":8,
            "M":8,
            "P":8,
            "D":9,
            "G":9,
            "L":15,
            "N":15,
            "R":15,
            "S":15,
            "T":15,
            "O":20,
            "U":20,
            "A":25,
            "I":25,
            "E":35}

# Function to read a file from a given path and return names as a list
def inputreader(path):

    with open(path,"r") as inputtext:
        inputdata = inputtext.readlines()

    inputnames = [name.strip().replace("\n","") for name in inputdata]

    return inputnames


# Function to clean each name as per required specification
def namecleaner(string):
    
    string = string.replace("'","") 
    string = re.sub(r"[^a-zA-Z]"," ",string)
    words = [word.strip().upper() for word in string.split(" ")]
    return words

# Function to get a list of scores for each letter based on their index position
def getscores(words, scoredict):

    scoretracker=[]
    for word in words:
        
        for idx,letter in enumerate(word,1):
            
            if idx==1:
                score = 0

            elif idx == len(word):
                
                if letter == "E":
                    score = 20
                else:
                    score = 5
                    
            else:

                if idx == 2:
                    score = 1
                elif idx == 3:
                    score = 2
                else :
                    score = 3
                
                score = score + scoredict[letter]

            scoretracker.append(score)
                
    return scoretracker


# Function to get all valid combinations for a name with their corresponding scores
def namecombs(namewords, scoredict):

    scoretracker = getscores(namewords, scoredict)
    nameletters = "".join(namewords)
    validcombs = {}
    
    first = nameletters[0]
    
    for secondidx,second in enumerate(nameletters[1:],1):
        
        for thirdidx, third in enumerate(nameletters[secondidx+1:], secondidx+1):

            tempcomb = "".join([first,second,third])
            tempscore = scoretracker[secondidx]+scoretracker[thirdidx]
            if validcombs.get(tempcomb):
                
                if validcombs[tempcomb] <= tempscore:
                    pass
                else:
                    validcombs[tempcomb] = tempscore
                    
            else:
                validcombs = updatedict(validcombs, 'add', tempcomb, tempscore)
                
    return validcombs

# Function to clean a name and return valid combinations
def validcombinations(name, scoredict):

    namewords = namecleaner(name)
    validcombs = namecombs(namewords, scoredict)
    return validcombs

# Utility function to perform add or remove operations on a dictionary
def updatedict(dict, operation = 'add', key=None, val = None):

    if operation == 'add':
        dict[key] = val
    elif operation == 'remove':
        dict.pop(key)

    return dict

# function to get least score abbreviation for each name
def formattedoutput(tempabbrs):

    output = []
    for name, abbrdict in tempabbrs:

        output.append(name)

        if len(abbrdict) == 0:
            output.append(" ")
        else:
            sorteddict = dict(sorted(abbrdict.items(),key=lambda x:x[1]))
            sortedkeys = list(sorteddict.keys())
            output.append(sortedkeys[0])
    return output




# Main function which takes all the names, score dictionary and return abbreviation having least score
def main(namesinput,scoredict):
    
    tempoutput=[]
    existingabbrs = []
    
    for name in namesinput:

        tempabbr = validcombinations(name, scoredict)
        tempcombs = list(tempabbr.keys())

        for abbr in tempcombs:
            
            if abbr in existingabbrs:
                tempabbr = updatedict(tempabbr,'remove', abbr)

                for idx, value in enumerate(tempoutput):
                    nametochange, abbrstochange = value
                    if abbr in abbrstochange:
                        revisedabbr = updatedict(abbrstochange,'remove', abbr)
                        tempoutput[idx] = [nametochange,revisedabbr]
            
            else:
                existingabbrs.append(abbr)

        tempoutput.append([name, tempabbr])

 
    requiredoutput = formattedoutput(tempoutput)
    return requiredoutput


if __name__ == '__main__':

    inputfile = input("Enter file containing names: ")
    file =  PurePosixPath(inputfile).stem #Using PurePosixPath function to extract the name of the file
    input = inputreader(inputfile)
    output = main(input, scoredictionary)
    with open(r'Thakur'+''+ file +''+'abbrevs.txt', 'w') as writer:
        for text in output:
        # write each item on a new line
            writer.write("%s\n" % text)