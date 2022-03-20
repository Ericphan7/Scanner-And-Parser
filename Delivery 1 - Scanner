

#import regular expression for the use of matching other words in the lexcical analyzer
import re
analyzer = {

    #keyword dictionary contains the keywords
    "keyword": {'array',
           'begin',
           'bool',
           'byte',
           'call',
           'char',
           'constants', 
           'declarations', 
           'define',
           'definetype',
           'description',
           'display', 
           'do', 
           'else', 
           'endfor', 
           'endif', 
           'endfun',
           'endrepeat', 
           'endwhile', 
           'endstruct',
           'enum', 
           'exit', 
           'float',
           'for', 
           'forward', 
           'function', 
           'global', 
           'if', 
           'implementations', 
           'import', 
           'input', 
           'integer', 
           'is', 
           'long',
           'loop',
           'main',
           'node',
           'not',
           'of',
           'parameters', 
           'pointer', 
           'references', 
           'repeat',
           'return',
           'set',
           'setup',
           'short',
           'specifications',
           'struct',
           'structures',
           'symbol',
           'then',
           'to',
           'type',
           'unsigned',
           'until',
           'using',
           'variables',
           'void',
           'while',
           '\"'},

    #operations dictionary contains operation symbols
    "operations": {
        '+',
        '-',
        '*',
        '/',
        '=',
        '**',
        '%'
        '==',
        '!=',
        '>',
        '<',
        '>=',
        '<='
        },
    "identifiers":{
        '\\<',          #word begins with '<'
        '\\>',          #word ends with '>'                      
        '[a-zA-Z]+'}    #alpha word
    }

#3 lists to store the words of each type
keywords = []
operations = []
identifiers = []

#Scanner class
class Scanner:

    #boolean variable commentBlock to idicate the block of comments (start with description and end with '*/)
    commentBlock = False

    #Scanner class constructor
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            content = f.readlines()
        for line in content:
            for word in line.split():
                #if it recognizes the comment line, break the loop and move to the next line
                if word == '//':
                    break         

                #if reaches the end of block of comments, switches back to False --> read lines normally
                if word == '*/':
                    self.commentBlock = False
                if word == 'description':
                    self.commentBlock = True
                if not self.commentBlock:
                    if re.match('[\-]?[0-9]', word):
                        print(word)
                        break
                    if word == '*/' or word[-1] == ',' or word == '"': 
                        break
                    self.tokenizer(word)
        #print 3 lists
        self.printList("\nKeywords Found: ", keywords)
        self.printList("Operations Found: ", operations)
        self.printList("Identifiers Found: ", identifiers)

    #tokenizer function puts the words into different categories
    def tokenizer(self, word):

        #put words that are keywords to keywords list
        for subkey in analyzer["keyword"]:
            if re.match(subkey, word):

                #words that are operations, do nothing and return
                if word in analyzer["operations"]:
                    return

                #add words that are keywords to keywords list
                keywords.append(word)

        #put words that are operations into operations list
        if word in analyzer["operations"]:
            operations.append(word)

        #put words that are identifiers into identifiers list
        for subkey in analyzer["identifiers"]:
            if re.match(subkey, word):

                #i variable used to traverse through each letter of the word to check '.' in between
                i = 0
                #if words that are already keywords, do nothing and return
                if word in analyzer["keyword"]:          
                    return

                #if words that are already operators, do nothing and return
                elif word in analyzer["operations"]:
                    return

                #if the word begins or ends with parenthesis or square brackets, print it out and return
                elif word[0] == '(' or word[-1] == ')' or word[0] == '[' or word[-1] == ']':
                    print(word)
                    return
                #if word has the '.' or '>' in between (object's function call), print it out and return it
                while i < len(word):
                    if word[i] == '.' or word[i] == '>':
                        print(word)
                        return
                    i += 1
                #the remaining words are identifiers, add to the end of the identifiers list
                identifiers.append(word)

    #print list function
    def printList(self, str, list):
            print(str, list, "\n")

#Use user's string input as the file name
fName = input("Enter file name: ")

#create a new object from Scanner class with the input file name
myScanner = Scanner(fName)
