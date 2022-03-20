

from SCL_Interpreter import SCL_Interpreter
from datetime import datetime

# Absolute path to input SCL file
inputPath = "sample.scl"

# OMITTED: No output file path because program involves user input, so I will just copy-paste console output to file
#outputPath = "InterpreterTestOutput.txt"

# Output file
# testFile = open(outputPath, "w")

# Creates SCL_Parser object
interpreter = SCL_Interpreter(inputPath)

print("Log Time: ", str(datetime.now()), "\n")
print("="*50, "\n")

# Performs python interpretation
interpreter.interpret()


