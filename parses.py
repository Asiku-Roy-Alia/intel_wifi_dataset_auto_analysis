import argparse
import sys
import os
from tabnanny import verbose

parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('-path',
                       type=str,
                       help='the path to dataset')
parser.add_argument('-mode',
                    '--mode', 
                    type=str,
                    help='c for communications engineering, d for data science mode')
parser.add_argument("-verbosity", 
                    "--verbose", action="store_true",
                    help="increase output verbosity")

# Parse arguments
args = parser.parse_args()

input_path = args.path
verbosity_level=args.verbosity
mode=args.mode
# Clean arguments

if not os.path.isfile(input_path):
    print('The path specified does not exist')
    sys.exit() 
