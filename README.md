# FASTA & Tabular Processing Toolkit

This Python program provides three modes for bioinformatics and virome analysis tasks, combining sequence extraction, assembly, and tabular filtering capabilities into a single user-friendly interface.

## Installation

```bash
# Ensure Python 3 is installed.
sudo apt install python

# Clone the repository.
git clone https://github.com/General-Cerberus/Martin.git

# Navigate to project directory
cd Martin
```

## Usage

Run the program with:

```bash
python main.py
```

You'll be presented with a menu-driven interface:

```
==================================================
FASTA & Tabular Processing Toolkit
==================================================

Main Menu:
  S - Extract sequences by accession
  O - Assemble sequences by overlap
  F - Filter tabular file by column content
  Q - Quit
```

### Sequence Extraction Mode (S)

Extracts specific sequences from a FASTA file based on a list of accessions.

Inputs:
- Accession list file (text file with one accession per line)
- FASTA file containing sequences
- Output filename for extracted sequences

Process:
- Program reads accessions and scans FASTA file
- Matching sequences are written to output file
- Detailed report of found/missing accessions

### Sequence Assembly Mode (O)

Assembles multiple DNA sequences by finding overlapping regions.

Inputs:
- DNA sequences entered interactively
- Minimum 3 bp overlap required

Process:
- Performs greedy assembly with bidirectional overlap checking
- Reports assembled sequence length
- Validates DNA sequences

### Tabular Filtering Mode (F)

Filters tabular data files based on column content.

Inputs:
- Input tabular file (TSV, CSV, or other delimited format)
- Output filename for filtered results
- Column identifier (name or 1-based index)
- Search phrase (case-insensitive)
- Header presence confirmation

Process:
- Auto-detects file delimiter
- Preserves header in output
- Performs substring matching in specified column
- Handles large files efficiently

## Examples

### Sequence Extraction Example

Input Files:

`accessions.txt`:

```
TRINITY_DN12345
TRINITY_DN67890
TRINITY_DN54321
```

`virome.fasta`:

```
>TRINITY_DN12345 gene=ORF1
ATGCGATCGATCGATC
>TRINITY_DN54321 gene=ORF2
CGATCGATCGATCG
>TRINITY_DN99999 hypothetical protein
GGGATCGATCGATC
```

Output (`extracted.fasta`):

```
>TRINITY_DN12345 gene=ORF1
ATGCGATCGATCGATC
>TRINITY_DN54321 gene=ORF2
CGATCGATCGATCG
```

Console Output:

```
Extraction complete!
Total sequences extracted: 2
Total missing accessions: 1

Missing accessions:
  1. TRINITY_DN67890
```

### Sequence Assembly Example

```
Sequence Assembly Mode
----------------------
Insert sequence: GTAGATCGGAAGAGC
Add another sequence? (y/n): y
Insert sequence: GAGCACCGTCTGA
Add another sequence? (y/n): n

Assembly complete!
Final sequence length: 24 bp

Assembled sequence:
GTAGATCGGAAGAGCACCGTCTGA
```

### Tabular Filtering Example

Input File (`annotations.tab`):

```
ID	Accession	Species	Length
1	TRINITY_DN123	Human betaherpesvirus 5	1200
2	TRINITY_DN456	Escherichia coli	800
3	TRINITY_DN789	Torque teno virus	950
4	TRINITY_DN101	Bacteroides fragilis	1100
```

Output (`virus_only.tab`):

```
ID	Accession	Species	Length
1	TRINITY_DN123	Human betaherpesvirus 5	1200
3	TRINITY_DN789	Torque teno virus	950
```

Console Output:

```
Detected delimiter: '\t'
Enter column to search (name or 1-based index): Species
Enter search phrase: virus
Does the file have a header row? (y/n): y

Filtering complete! Matched 2 rows
Results saved to virus_only.tab
```

## Output Formats

1. Sequence Extraction:
  - Standard FASTA format
  - Preserves original header information
  - Includes all sequence data for matched accessions
2. Sequence Assembly:
  - Single DNA sequence string
  - Console report with length and partial sequence display
  - Full sequence output to console
3. Tabular Filtering:
  - Maintains original file format and delimiter
  - Preserves header row (if present)
  - Identical column structure to input file
  - Only contains rows matching search criteria

## Limitations

1. Sequence Assembly:
  - Requires minimum 3 bp overlap
  - May not handle complex repeat regions
  - No mutation tolerance in current implementation
2. Sequence Extraction:
  - Matches exact accession IDs only
  - Case-sensitive matching
3. Tabular Filtering:
  - Substring matching only (no regex)
  - Limited to single-column filtering
  - Large files (>1GB) may require significant memory

For support or feature requests, please open an issue on our GitHub repository.