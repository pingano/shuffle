
import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


def parseArgs(argv):
    '''parse out Command line options.'''


    try:
        # Setup argument parser
        parser = ArgumentParser(description="script to shuffle fasta sequences", formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-f", "--fasta_file", dest="fastafile", action="store", help="fasta file of sequences to be shuffled [default: %(default)s]")
        parser.add_argument("-n", "--no_of_shuffles", dest="noofshuffles", action="store", help="no of times to shuffle each sequence [default: %(default)s]")

        # Process arguments
        args = parser.parse_args()

        global fastaFile
        global noOfShuffles
        global seedBegin

        fastaFile = args.fastafile
        noOfShuffles = int(args.noofshuffles)


        # check the user specified a fasta file, if not warn and and exit
        if fastaFile:
            print("fasta file is <" + fastaFile + ">")
        else:
            print("you must specify a fasta file using the -f/--fasta_file parameter")
            exit

            
        # check the user specified a start position for the seed region, if not warn and and exit
        if noOfShuffles:
            print("sequences will be shuffled <" + str(noOfShuffles) + "> times")
        else:
            print("you must specify the number of shuffles using the -n/--no_of_shuffles parameter")
            exit
            

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        print(e)
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


def readFastaFile(filename):
    '''
    load specified fasta file and store header and sequence as entries in two lists
    :param self:
    :return:
    '''

    print("load sequences from fasta file <" + fastaFile + ">")
    global headerLines
    global sequenceLines

    # load the fasta lines into a list
    try:
        fFA = open(filename, 'r')
        fastaLines = fFA.readlines()
        fFA.close()
    except Exception as e:
        raise(e)

    headerLines = []
    headerLine = ""
    sequenceLines = []
    sequence = ""

    s = 0
    for fastaLine in fastaLines:
        if fastaLine[0] == '>':
            if s > 0:
                headerLines.append(headerLine)
                sequenceLines.append(sequence)
                sequence = ""
            headerLine = fastaLine[1:].strip()
            sequence = ""
            
        else:
            sequence = sequence + fastaLine.strip()
        s += 1

    headerLines.append(headerLine)
    sequenceLines.append(sequence)        

    print("--loaded <" + str(len(headerLines)) + "> sequences")

    return len(headerLines)


def shuffleAndWriteSequences():
    '''
    shuffle each sequence and write to output file 'on the fly'
    '''
    print("shuffle and write sequences")
    import os
    from pathlib import Path
    
    foldername = os.path.dirname(fastaFile)
    basename = Path(fastaFile).stem    
    outputfafile = os.path.join(foldername, basename + "__shuffled" + ".fa")
    
    print("--output fasta file is <" + outputfafile + ">")
    file = open(outputfafile,'w')
    import string_utils

    
    s = 0
    for sequenceLine in sequenceLines:
        for n in range(noOfShuffles):            
            file.writelines(">" + headerLines[s] + "__" + str(n) + os.linesep)
            file.writelines(string_utils.shuffle(sequenceLine) + os.linesep)
        s+=1
    file.close()      
    print("--finished")


def main(argv=None): 

    if argv is None:
        argv = sys.argv

    parseArgs(argv)

    n = readFastaFile(fastaFile)
    
    shuffleAndWriteSequences()



if __name__ == '__main__':

    sys.exit(main())
