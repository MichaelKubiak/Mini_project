# pdb_parser_mk626

This program takes a pdb file, and parses it to perform three possible functions:
1) Calculate the distance between two atoms within the structure,
2) Draw the structure using Pymol, highlighting beta strands in blue and helices in yellow, then output 2 png files, one with the cartoon representation, and the other with the stick representation,
3) Produce a FASTA file containing the amino acid sequence of a chain, showing residues not present in the structure as lowercase.

### Requirements

To run this program an installation of python3 is required.

Drawing the molecule also requires an installation of Pymol, and production of the fasta file requires an installation of BioPython, and access to the internet at the time of running.

To provide a fresh installation of python3 to which modules can be added without interfering with anything already present, it is advised that anaconda is installed from the [anaconda website](https://anaconda.com/download).

With anaconda installed, Pymol can be installed through use of the command `conda install -c schrodinger pymol` in the terminal.  In the same way, BioPython can be installed  using `conda install -c anaconda biopython`.

### Installation

This program can be installed using the 'clone or download' button on github, then selecting 'Download ZIP'.  The downloaded file can be extracted as usual using an archive manager.  Further instructions will assume that the file is extracted to the home directory, but if another path is used, substitute that path in later instructions.

### Running the Program

Now that the program is installed, it can be run like any other program, navigate to the correct directory using e.g. `cd ~/pdb_parser_mk626', then run the program with the example pdb file by typing `./pdb_parser_mk626.py -i 1vyd.pdb -c -d -s`.

#### Arguments

* -i or --input - this argument tells the program where to find the pdb file that it needs to parse, as seen above, this path can simply be the name of the file, if it is in the same directory as the program.

* -c or --calculate - requires the calculate function to be performed, this argument can also be followed by any number of arguments of the form [Chain_Name][Residue_Number][Atom_Type/Number](:[Chain_Name][Residue_Number][Atom_Type/Number]), with the part in brackets optional.  These arguments instruct the function on which atoms it should find the distance between.  If only one atom is named, the distance between that atom and the next atom in the chain will be found.  The default argument for this function is 'A,1,1:A,1,CA'.  If a pdb file does not contain chain A, and the program is run with no arguments, it will inform the user that the atom does not exist.  Information about the names of chains in a pdb file can be found in the COMPND section near the top of the file.

* -d or --draw - requires the draw function to be performed, this argument can be followed by one argument containing the preferred name of the png output files.  If no argument is used, the png files will be named after the pdb input file (1vyd.pdb becomes 1vyd_cartoon.png etc.).

* -s or --sequence - requires the sequence function to be performed, this argument can be followed by any number of arguments which are the names of the chains for which the sequence should be output.  As for calculate, the COMPND section shows chain names within a file.
