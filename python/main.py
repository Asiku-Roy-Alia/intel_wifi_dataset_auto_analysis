from ast import arg
from unicodedata import name

def main():
    import argparse
    import sys
    import os
    from tabnanny import verbose

    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-path',
                        type=str,
                        help='the path to dataset')
    parser.add_argument('-m', 
                        '--mode',    
                        type=str,
                        help='c for communications engineering, d for data science mode')
    parser.add_argument("-v", 
                        "--verbose",    
                        type=int, 
                        help="increase output verbosity (1, 0)")

    # Parse arguments
    args = parser.parse_args()
    
    input_path = args.path
    mode=args.mode
    verbosity_level=args.verbose

    # Clean arguments

    if not os.path.isfile(input_path):
        print('The path specified does not exist')
        sys.exit() 

    # Execute main program 


    if mode=='c' and not verbosity_level:
        comm()
        
    elif mode=='c' and verbosity_level:
        comm_v() 

    elif mode=='d' and not verbosity_level:
        dat()

    elif mode=='d' and verbosity_level:
        dat_v()

    else:
        default()
    

def comm():
    print('Communications mode')

def comm_v():
    print('Verbose communications mode')

def dat():
    print('Data science mode')

def dat_v():
    print('Verbose data science mode')

def default():
    print('Combined mode')

if __name__ =="__main__":
    main()




