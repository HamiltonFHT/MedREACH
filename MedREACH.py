''' Appointment Counter 
    Copyright (C) 2014  Tom Sitter; Hamilton Family Health Team

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.'''


from tkinter.filedialog import askopenfilename, asksaveasfilename, Tk
import csv, sys
import pprint
from operator import itemgetter

#Prevent tk window from displaying
root = Tk()
root.withdraw()

#Get user to select a file
filename = askopenfilename(title='Select a PSS patient appointment report to analyze')

if filename == "":
    print("No file selected by using, exiting");
    sys.exit()

output = []
header = []

with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    #Read file row by row
    for row in reader:
        #Skip empty rows (usually at top or bottom of file)
        if len(row) == 0:
            continue
        #Skip header
        elif row[0] == 'Patient #':
            row.append('Number of Conditions');
            header = row
            continue
        #If first entry in row is a number (Patient ID)
        #Begin counting appointment for a new patient

        condList = row[5];

        numConditions = len(condList.split(','))
        row.append(numConditions)

        output.append(row)

#Ask the user to select a file for output
output_file = asksaveasfilename(initialfile='MedREACH_Analysis.csv', defaultextension='.csv',
                   filetypes=[('CSV','*.csv')],title='Export MedREACH List As...')

#If no file selected, print to console
if output_file == "":
    print("No file selected, printing to console")
    print(*header, sep='\t')
    for row in sorted(output, key=itemgetter(8), reverse=True):
        if row[8] >= 3:
            print(*row, sep='\t')
else:
    #Otherwise open the file and write appointments data to it
    with open(output_file, 'w', newline="") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(header)
            for row in sorted(output, key=itemgetter(8), reverse=True):
                if row[8] >= 3:
                    writer.writerow(row)

print("Finished Analysis")
        



