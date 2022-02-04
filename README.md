# Intel WiFi RTT Dataset - Automated data extraction, analysis, and visualization with Python 
Software for automated processing and visualization of extracted information from the Intel Open Wi-Fi Round Trip Times Dataset
 
Dataset and theory:
The dataset used for this project is available at https://ieee-dataport.org/open-access/intel-open-wi-fi-rtt-dataset and a sample in the project repository is called *RTT_dataset_sample.csv* 
and the notations used are from the paper  https://www.researchgate.net/publication/329887019_A_Machine_Learning_Approach_for_Wi-Fi_RTT_Ranging 

Command Line Interface 
The program main.py runs the command interface in 5 modes. 

Usage:
usage: main.py [-h] [-path PATH] [-m MODE] [-v VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  -path PATH            the path to dataset
  -m MODE, --mode MODE  c for communications engineering, d for data science mode   
  -v VERBOSE, --verbose VERBOSE
                        increase output verbosity (1, 0) 


Graphical interface:
The program main_gui.py when executed runs the graphical interface. The sample data provided can be loaded with the load data button or
you can select data from the local machine with the 'Select and Load' 
button. 

The interface is simple and basic enough for easy use. 

Requirements
The python modules we used are specified in the requirements.txt file. Core python modules are not mentioned.  

Folder organization:
license: The license for the software 
README.md: This Readme file
requirements.txt: Software modules used
main.py : Main runner program for command line interface
RTT_dataset_sample.csv: A sample of the dataset
    functions: Functions used in the main programs
     comm.py      Basic communications mode analysis module 
     comm_v.py    Verbose communications mode analysis module 
     dat.py       Data Science Mode Analysis 
     dat_v.py     Verbose Data Science Mode Analysis
     stats_model.py Statistical modelling 
     rangest.py   Runner for range and ToA estimation 
     estimate_range.py Range estimator without graphs 
     range_est_graphs.py Range estimator with graphs
    graphs: Folder for storing graphs from the main programs





 


