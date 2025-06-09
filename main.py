#!/usr/bin/env python3
"""
==============================================
= FASTA Sequence Tool with Tabular Filtering =
==============================================

This program provides three modes of operation:
1. Extract sequences by accession numbers ('S' mode)
  - Inputs:
    - Accession list file
    - FASTA file
    - Output filename
  - Output: FASTA file with matching sequences

2. Assemble sequences by overlap ('O' mode)
  - Input: User-provided DNA sequences
  - Output: Assembled sequence

3. Filter tabular files ('F' mode)
  - Inputs:
    - Input tabular file (TSV/CSV)
    - Output filename
    - Column to search (index or name)
    - Search phrase
    - Optional: Delimiter (default: tab)
  - Output: Filtered tabular file
"""

import csv
import os


def parse_fasta(fasta_file):
    """
    Parse FASTA files into a dictionary with accessions as keys.
    Handles multi-line sequences and missing files gracefully.
    """
    if not os.path.exists(fasta_file):
        print(f"Error: FASTA file {fasta_file} not found")
        return {}

    fasta_dict = {}
    current_id = None
    current_header = ""
    current_seq = []

    try:
        with open(fasta_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    if current_id is not None:
                        fasta_dict[current_id] = (current_header, "".join(current_seq))
                    current_header = line[1:]
                    current_id = current_header.split()[0]
                    current_seq = []
                else:
                    current_seq.append(line)

            if current_id is not None:
                fasta_dict[current_id] = (current_header, "".join(current_seq))
        return fasta_dict

    except Exception as e:
        print(f"Error parsing FASTA: {str(e)}")
        return {}


def extract_sequences():
    """
    Extract sequences based on accession numbers.
    Provides detailed reporting of missing accessions.
    """
    accession_file = input("Enter accession list filename: ")
    fasta_file = input("Enter FASTA filename: ")
    output_file = input("Enter output filename: ")

    # Read accessions with error handling.
    try:
        with open(accession_file, "r") as f:
            accession_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Accession file {accession_file} not found")
        return

    fasta_dict = parse_fasta(fasta_file)
    if not fasta_dict:
        return

    found_count = 0
    missing_accessions = []

    try:
        with open(output_file, "w") as out:
            for acc in accession_list:
                if acc in fasta_dict:
                    header, seq = fasta_dict[acc]
                    out.write(f">{header}\n{seq}\n")
                    found_count += 1
                else:
                    missing_accessions.append(acc)

        print(f"\nExtraction complete!")
        print(f"Total sequences extracted: {found_count}")
        print(f"Total missing accessions: {len(missing_accessions)}")

        if missing_accessions:
            print("\nMissing accessions:")
            for i, acc in enumerate(missing_accessions[:10], 1):
                print(f"  {i}. {acc}")
            if len(missing_accessions) > 10:
                print(f"  ... and {len(missing_accessions)-10} more")

    except IOError as e:
        print(f"Output error: {str(e)}")


def assemble_sequences(seq_list):
    """
    Assemble sequences using overlap detection with adjustable threshold.
    Implements bidirectional matching (suffix-prefix and prefix-suffix).
    """
    if not seq_list:
        return ""
    if len(seq_list) == 1:
        return seq_list[0]

    seqs = [s.upper() for s in seq_list]  # Normalize case
    min_overlap = 3  # Minimum required overlap

    while len(seqs) > 1:
        best_match = (0, -1, "")  # (overlap, index, merged_sequence)

        for j in range(1, len(seqs)):
            a, b = seqs[0], seqs[j]

            # Check suffix of A vs prefix of B
            min_len = min(len(a), len(b))
            for overlap in range(min_len, min_overlap - 1, -1):
                if a.endswith(b[:overlap]):
                    merged = a + b[overlap:]
                    if overlap > best_match[0]:
                        best_match = (overlap, j, merged)
                    break

            # Check prefix of A vs suffix of B
            for overlap in range(min_len, min_overlap - 1, -1):
                if b.endswith(a[:overlap]):
                    merged = b + a[overlap:]
                    if overlap > best_match[0]:
                        best_match = (overlap, j, merged)
                    break

        # Apply best match if found
        if best_match[0] >= min_overlap:
            seqs[0] = best_match[2]
            del seqs[best_match[1]]
        else:
            break  # No more overlaps found

    return "".join(seqs)


def assemble_mode():
    """Interactive sequence assembly with input validation."""
    sequences = []
    print("\nSequence Assembly Mode")
    print("----------------------")

    while True:
        seq = input("Insert sequence: ").strip()
        if not seq:
            print("Invalid sequence. Please enter at least 3 characters.")
            continue

        # Validate DNA sequence
        if any(c not in "ACGTacgt" for c in seq):
            print("Warning: Sequence contains non-DNA characters")

        sequences.append(seq)

        if input("Add another sequence? (y/n): ").lower() != "y":
            break

    if not sequences:
        print("No sequences provided")
        return

    result = assemble_sequences(sequences)

    print("\nAssembly complete!")
    print(f"Final sequence length: {len(result)} bp")
    print("\nAssembled sequence:")
    print(result[:100] + "..." if len(result) > 100 else result)


def filter_tabular():
    """
    Filter tabular files based on column content.
    Supports both header-based and index-based column selection.
    Handles large files efficiently.
    """
    print("\nTabular File Filter")
    print("-------------------")

    input_file = input("Enter input filename: ")
    output_file = input("Enter output filename: ")

    # Auto-detect delimiter
    delimiters = ["\t", ",", ";", "|"]
    detected_delim = "\t"  # Default to tab

    try:
        with open(input_file, "r", newline="") as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            detected_delim = dialect.delimiter
            print(f"Detected delimiter: {repr(detected_delim)}")
    except Exception:
        print("Using default tab delimiter")

    # Get column identifier
    col_id = input("Enter column to search (name or 1-based index): ").strip()

    # Check if column is numeric index
    try:
        col_index = int(col_id) - 1
        use_header = False
    except ValueError:
        col_index = col_id
        use_header = True

    search_phrase = input("Enter search phrase: ").strip().lower()

    # Determine header presence
    has_header = "y" in input("Does the file have a header row? (y/n): ").lower()

    matched_rows = 0
    skipped_header = False

    try:
        with open(input_file, "r", newline="") as infile, open(
            output_file, "w", newline=""
        ) as outfile:

            reader = csv.reader(infile, delimiter=detected_delim)
            writer = csv.writer(outfile, delimiter=detected_delim)

            for row in reader:
                # Process header
                if has_header and not skipped_header:
                    writer.writerow(row)
                    skipped_header = True
                    continue

                # Get target column
                try:
                    if use_header:
                        # Find column by name (if header available)
                        if skipped_header:
                            target_col = row[list(reader.fieldnames).index(col_id)]
                        else:
                            # We haven't read header yet
                            reader.fieldnames = row
                            writer.writerow(row)
                            skipped_header = True
                            continue
                    else:
                        target_col = row[col_index]
                except (IndexError, ValueError):
                    continue

                # Case-insensitive search
                if search_phrase in target_col.lower():
                    writer.writerow(row)
                    matched_rows += 1

        print(f"\nFiltering complete! Matched {matched_rows} rows")
        print(f"Results saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
    except Exception as e:
        print(f"Processing error: {str(e)}")


def main():
    """Main program interface with enhanced user experience."""
    print("\n" + "=" * 50)
    print("FASTA & Tabular Processing Toolkit")
    print("=" * 50)

    while True:
        print("\nMain Menu:")
        print("  S - Extract sequences by accession")
        print("  O - Assemble sequences by overlap")
        print("  F - Filter tabular file by column content")
        print("  Q - Quit")

        choice = input("\nSelect mode: ").upper()

        if choice == "S":
            extract_sequences()
        elif choice == "O":
            assemble_mode()
        elif choice == "F":
            filter_tabular()
        elif choice in ("Q", "EXIT"):
            print("\nExiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose S, O, F, or Q")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
