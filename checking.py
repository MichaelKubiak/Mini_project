# Module to contain checking functions etc.
#---------------------------------------------------------------------------------------------------------------------
import sys


# Function to check that the input file exists - copied from my solution to the previous assignment
def checkInput(input_file):
    #check that file exists
    try:
        # open the file to check that it exists
        test = open(input_file)
        # close the file
        test.close()
        # if the file opened properly, return it
        return input_file
    # if the file wasn't in the stated place, do the following
    except FileNotFoundError:
        # inform user of lack of file and close
        print("The specified input file cannot be found, exiting script")
        sys.exit(0)
