#Created by Creston Altiere
#11 February 2019

#Get Document
def inputFile(file):
    #Try to open input file; returns a list of each line of text
    try:
        inp = open(file, "r")
    except FileNotFoundError:
        print("Error: File not found!")
        return
    except:
        print("Error: Problem in loading file.")
        return
    ###print("File found!")
    #Move each line of text in file to array
    lstParagraph = []
    for i in inp:
        if i.endswith("\n"):
            i = i[:-1]
        lstParagraph.append(i)
    inp.close()
    return lstParagraph

def outputFile(file,lst):
    #Outpus a list to a file
    out = open(file, "w+")
    for i in range(len(lst)):
        if i < len(lst):
            out.write(lst[i] + "\n")
        else:
            out.write(lst[i])
    out.close()

def getRules(rouxl):
    #Gets and returns a list of all rules
    entries = []
    continuation = True
    while continuation:
        entry = input("Please enter the " + rouxl + ". Leave blank to finish.")
        if entry != "":
            entries.append(entry)
        else:
            continuation = False
    return entries

def search(item,lst):
    #Finds item in list, returns index. returns -1 if not in list
    index = 0
    for i in lst:
        if i == item:
            return index
        index += 1
    return -1

def find(word,string):
    #Finds the word by itself in string
    #One could simply use 'word in string' or string.find(word). They will find the word, but they'll also find the word if it is another word. Ex: both will see 'small' in the string 'that's even smaller'
    #This function will look for the word when it's only itself; will return index of first occurence
    abc = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    x = string.find(word)
    z = -1
    if x != -1:
        #The word is present in the string
        y = len(word)
        if x == 0:
            #word is at the start of string
            if y >= len(string):
                #word is the only item in string
                z = 0
            elif search(string[y],abc) == -1:
                #There is no letter right after word
                z = 0
            else:
                #The character after word is not a space
                z = -1
        else:
            #word is not at the start of string
            if string[x-1] == " ":
                #There is a space right before the word
                if (x+y) >= len(string):
                    #word is at the end of the string
                    z = x
                elif search(string[x+y],abc) == -1:
                    #There is no letter right after the word
                    z = x
                else:
                    #The character after word is not a space
                    z = -1
            else:
                #There is no space right before the word
                z = -1
    else:
        #The word isn't present in the string
        z = -1
    return z

def main():
    #Get lines
    lstLines = inputFile("input.txt")
    if lstLines == None:
        print("Please get an input file with text.")
        return
    #Get conditions
    codes = getRules("restricted characters")
    words = getRules("restricted words")
    target = input("Please enter the charecter to be replaced.")
    replacer = input("Please enter the charecter to replace.")
    #Check if target is in restricted words
    inWord = []
    for i in words:
        if target in i.lower():
            inWord.append(True)
        else:
            inWord.append(False)
    ###print(inWord)
    lstNewLines = []
    #Commit replacements
    for i in lstLines:
        ###print(i)
        new = ""
        #Look for targeted character
        findings = (i.lower()).find(target)
        ###print(findings)
        while findings > -1:
            ###print("Item found at index " + str(findings))
            continuation = True
            #See if character is in a restricted word
            for j in range(len(words)):
                ###print("Searching for " + words[j])
                if inWord[j] == True and continuation:
                    #Check if surrounding characters make the restricted word
                    #See if word is located by index
                    a = find((words[j]).lower(),i.lower())
                    if a > -1:
                        ###print("Word found at " + str(a))
                        b = len(words[j])
                        c = (words[j].lower()).find(target)
                        ###print(i[findings])
                        ###print(i[a + c])
                        if i[findings] == i[a + c]:
                            #The target is in the word's location; do not remove
                            continuation = False
            #Check if adjectent letters are restricted characters
            if continuation:
                for j in range(len(codes)):
                    ###print("looking for " + codes[j] + ".") 
                    if findings == 0:
                        #target is at beginning of string
                        if 1 > len(i):
                            #Character is the only thing in list 
                            pass
                        else:
                            #print(i[1])
                            if i[1].lower() == codes[j].lower():
                                #restricted character after target; do not replace
                                continuation = False
                            else:
                                #No restrited character after target
                                pass
                    else:
                        #target is not at beginning of string
                        if (findings + 1) > len(i):
                            #Character is the last thing in list
                            pass
                        else:
                            if i[findings + 1].lower() == codes[j].lower():
                                #Restricted character after target; Do not replace
                                ###print("character found!")
                                continuation = False
                            elif i[findings - 1].lower() == codes[j].lower():
                                #Restricted character before target; do not replace
                                ###print("character found!")
                                continuation = False
                            else:
                                #No restricted characters adjacent to target
                                pass
            ###print(continuation)
            #Target passed word and character test, replace
            if continuation:
                i = i[:findings] + replacer + i[findings + 1:]
            new += i[0:findings + 1]
            i = i[findings + 1:]
            ###print(i)
            ###print(new)
            findings = i.find(target)
        new += i
        ###print(new)
        lstNewLines.append(new)
    #Add new lines to file
    outputFile("output.txt",lstNewLines)

main()
