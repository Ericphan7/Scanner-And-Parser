"""
Group 9:
Members:
    - Khoa Ho
    - Eric Phan
    - Khanh Nguyen
"""

#import regular expression for the use of matching other words in the lexcical analyzer
import re


analyzer = {

        #keyword dictionary contains the keywords
        "keyword": {'array':101,
               'begin':102,
               'bool':103,
               'byte':104,
               'call':105,
               'char':106,
               'constants':107,
               'declarations':108,
               'define':109,
               'definetype':110,
               'description':111,
               'display':112,
               'do':113,
               'else':114,
               'endfor':115,
               'endif':116,
               'endfun':117,
               'endrepeat':118,
               'endwhile':119,
               'endstruct':120,
               'enum':121,
               'exit':122,
               'float':123,
               'for':124,
               'forward':125,
               'function':126,
               'global':127,
               'if':128,
               'implementations':129,
               'import':130,
               'input':131,
               'integer':132,
               'is':133,
               'long':134,
               'loop':135,
               'main':136,
               'node':137,
               'not':138,
               'of':139,
               'parameters':140,
               'pointer':141,
               'references':142,
               'repeat':143,
               'return':144,
               'set':145,
               'setup':146,
               'short':147,
               'specifications':148,
               'struct':149,
               'structures':150,
               'symbol':151,
               'then':152,
               'to':153,
               'type':154,
               'unsigned':155,
               'until':156,
               'using':157,
               'variables':158,
               'void':159,
               'while':160,
               '\"':161},

        #operations dictionary contains operation symbols
        "operations": {
            '+':201,
            '-':202,
            '*':203,
            '/':204,
            '=':205,
            '**':206,
            '%':207,
            '==':208,
            '!=':209,
            '>':210,
            '<':211,
            '>=':212,
            '<=':213
            },
        "identifiers":{
            '\\<':301,          #word begins with '<'
            '\\>':302,          #word ends with '>'
            '[a-zA-Z]+':303}    #alpha word
    }





class Parser:

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
                        break
                    if word == '*/' or word[-1] == ',' or word == '"': 
                        break
                    self.tokenizer(word)




    #tokenizer function parser the words with different categories
    def tokenizer(self, word):
        # i variable used to traverse through each letter of the word to check
        i =0

        while i < len(word):
            print("The lexeme is "+ word)
            #if word that are keyword. Stop check and return. If not, through to next categories
            if word in analyzer["keyword"]:
                number = analyzer["keyword"][word]
                print("This token is " + str(number))
                print ("This word in <keyword>\n")
                return
            # if word that are operations. Stop check and return. If not, through to next categories
            elif word in analyzer["operations"]:
                number = analyzer["operations"][word]
                print("This token is " + str(number))
                print ("This word in <operations>\n")
                return
            # if word that are identifier. Stop check and return. If not, through to next categories
            elif word in analyzer["identifiers"]:
                number = analyzer["identifiers"][word]
                print("This token is " + str(number))
                print("This word in <identifiers>\n")
                return
            # if word that aren't any catagories. Stop check, return and go to next word.
            else:
                print("Syntax error\n")
                return




#Use user's string input as the file name
fName = input("Enter file name: ")

#create a new object from Parser class with the input file name
myParser = Parser(fName)


