"""
==============================================
= FASTA Sequence Tool with Tabular Filtering =
==============================================

This program provides three modes of operation:
1. Extract sequences by accession numbers ('S' mode):
  - Inputs:
    - Accession list file (.txt)
    - FASTA file (.fasta)
    - Output filename (.fasta)
  - Output: FASTA file with matching sequences
            or error messages for missing accessions.

2. Assemble sequences by overlap ('O' mode):
  - Input: User-provided DNA sequences or FASTA file names
  - Output: Assembled sequence(s), optionally saved to a file (.fasta)
  - Issues:
    - This problem is NP-hard: https://cs.stackexchange.com/questions/93815/merge-a-set-of-strings-based-on-overlaps
    - Maybe implement a greedy algorithm to find overlaps: https://en.wikipedia.org/wiki/Sequence_assembly#Assembly_algorithms

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
        print(f"Error: FASTA file {fasta_file} not found.")
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
        print(f"Error parsing FASTA: {str(e)}.")
        return {}


def extract_sequences():
    """
    Extract sequences based on accession numbers.
    Provides detailed reporting of missing accessions.
    """
    accession_file = input("Enter accession list filename (.txt): ")
    fasta_file = input("Enter FASTA filename (.fasta): ")
    output_file = input("Enter output filename (.fasta): ")

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
    Returns a list of assembled contigs. Sequences are only joined if they overlap.
    """
    if not seq_list:
        return []
    if len(seq_list) == 1:
        return seq_list

    # Normalize case.
    seqs = [s.upper() for s in seq_list]

    # Get minimum overlap threshold from user.
    min_overlap = int(input("Enter minimum overlap length (default 3): ") or 3)
    if min_overlap < 1:
        print("Overlap length must be at least 1.")
        return seq_list
    if min_overlap > 1000:
        print("Warning: Very high minimum overlap may lead to no matches.")

    # Track which sequences have been merged
    merged = [False] * len(seqs)
    contigs = []

    # Try to build contigs from each unmerged sequence.
    for i in range(len(seqs)):
        # Print progress.
        if i % 10 == 0:
            print(f"Processing sequence {i + 1}/{len(seqs)}…")

        if merged[i]:
            continue

        # Start a new contig with this sequence.
        current_contig = seqs[i]
        merged[i] = True
        made_merge = True

        # Keep trying to extend this contig until no more merges possible.
        while made_merge:
            made_merge = False
            best_match = (0, -1, "")  # (overlap, index, merged_sequence)

            # Look for best overlap with any unmerged sequence.
            for j in range(len(seqs)):
                if merged[j]:
                    continue

                a, b = current_contig, seqs[j]

                # Check suffix of contig vs prefix of candidate.
                if a.endswith(b[:min_overlap]):
                    merged_seq = a + b[min_overlap:]
                    if min_overlap > best_match[0]:
                        best_match = (min_overlap, j, merged_seq)
                    break

                # Check prefix of contig vs suffix of candidate.
                if b.endswith(a[:min_overlap]):
                    merged_seq = b + a[min_overlap:]
                    if min_overlap > best_match[0]:
                        best_match = (min_overlap, j, merged_seq)
                    break

            # Apply best match if found.
            if best_match[0] >= min_overlap:
                current_contig = best_match[2]
                merged[best_match[1]] = True
                made_merge = True

        # Add the finished contig to our results.
        contigs.append(current_contig)

    return contigs


def assemble_mode():
    """
    Interactive sequence assembly with input validation.
    Accepts manually entered sequences or sequences from a FASTA file.
    """
    sequences = []
    print("\nSequence Assembly Mode")
    print("----------------------")
    print("You can enter sequences directly or provide a FASTA file path")

    while True:
        user_input = input(
            "Enter sequence or FASTA file path (or press Enter to finish adding): "
        ).strip()

        if not user_input:
            break

        # Check if input is an existing file.
        if os.path.exists(user_input):
            # Check if file appears to be in FASTA format.
            try:
                with open(user_input, "r") as f:
                    first_line = f.readline().strip()
                    if first_line.startswith(">"):
                        print(f"Reading sequences from FASTA file: {user_input}")
                        fasta_dict = parse_fasta(user_input)
                        if fasta_dict:
                            for acc, (header, seq) in fasta_dict.items():
                                sequences.append(seq)
                            print(f"Added {len(fasta_dict)} sequences from file.")
                        else:
                            print("No valid sequences found in the file.")
                        # Skip to next iteration after processing FASTA file.
                        if (
                            len(sequences) > 0
                            and input("Add another sequence? (y/n): ").lower() != "y"
                        ):
                            break
                        continue
                    else:
                        print("File exists, but does not appear to be in FASTA format.")
            except Exception as e:
                print(f"Error reading file: {str(e)}")

        # If we get here, treat as direct sequence input.
        if len(user_input) < 3:
            print("Invalid sequence. Please enter at least 3 characters.")
            continue

        # Validate DNA sequence.
        if any(c not in "ACGTacgt" for c in user_input):
            print("Warning: Sequence contains non-DNA characters.")

        sequences.append(user_input)
        print(f"Added sequence of length {len(user_input)}.")

        if input("Add another sequence? (y/n): ").lower() != "y":
            break

    if not sequences:
        print("No sequences provided.")
        return

    print(f"\nAssembling {len(sequences)} sequences…")
    result_contigs = assemble_sequences(sequences)

    print("\nAssembly complete!")
    if len(result_contigs) == 1:
        print(
            f"All sequences were assembled into one contig of length {len(result_contigs[0])} bp."
        )
        print("\nAssembled sequence:")
        result = result_contigs[0]
        print(result[:128] + "…" if len(result) > 128 else result)
    else:
        print(f"Assembled into {len(result_contigs)} separate contigs.")
        for i, contig in enumerate(result_contigs, 1):
            print(f"\nContig {i} (length: {len(contig)} bp):")
            print(contig[:64] + "…" if len(contig) > 64 else contig)

    # Save results to file
    output_file = input("Enter output filename for assembled sequence(s): ")
    try:
        with open(output_file, "w") as out:
            for i, contig in enumerate(result_contigs, 1):
                if len(result_contigs) == 1:
                    out.write(f">assembled_sequence\n{contig}\n")
                else:
                    out.write(f">contig_{i}_length_{len(contig)}\n{contig}\n")
        print(f"Results saved to {output_file}.")
    except IOError as e:
        print(f"Error saving result: {str(e)}.")


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

    # For now, let's assume tab-delimited files.
    detected_delim = "\t"

    # Try to detect delimiter from sample data.
    try:
        with open(input_file, "r", newline="") as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            detected_delim = dialect.delimiter
            print(f"Detected delimiter: {repr(detected_delim)}")
    except Exception:
        print("Using default tab delimiter.")

    # Get column identifier.
    col_id = input("Enter column to search (name or 1-based index): ").strip()

    # Check if column is numeric index.
    try:
        col_index = int(col_id) - 1
        use_header = False
    except ValueError:
        col_index = col_id
        use_header = True

    search_phrase = input("Enter search phrase: ").strip().lower()

    # Determine header presence.
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
                # Process header.
                if has_header and not skipped_header:
                    writer.writerow(row)
                    skipped_header = True
                    continue

                # Get target column.
                try:
                    if use_header:
                        # Find column by name (if header available).
                        if skipped_header:
                            target_col = row[list(reader.fieldnames).index(col_id)]
                        else:
                            # We haven't read header yet.
                            reader.fieldnames = row
                            writer.writerow(row)
                            skipped_header = True
                            continue
                    else:
                        target_col = row[col_index]
                except (IndexError, ValueError):
                    continue

                # Case-insensitive search.
                if search_phrase in target_col.lower():
                    writer.writerow(row)
                    matched_rows += 1

        print(f"\nFiltering complete! Matched {matched_rows} rows.")
        print(f"Results saved to {output_file}.")

    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
    except Exception as e:
        print(f"Processing error: {str(e)}.")


def main():
    """Main program interface with enhanced user experience."""
    print("\n" + "=" * 38)
    print("\n= FASTA & Tabular Processing Toolkit =")
    print("\n" + "=" * 38)

    while True:
        print("\nMain Menu:")
        print("  s : Extract sequences by accession.")
        print("  o : Assemble sequences by overlap.")
        print("  f : Filter tabular file by column content.")
        print("  q : Quit.")

        choice = input("\nSelect mode: ").upper()

        if choice.upper() in ("S", "EXTRACT"):
            extract_sequences()
        elif choice.upper() in ("O", "0", "ASSEMBLE"):
            assemble_mode()
        elif choice.upper() in ("F", "FILTER"):
            filter_tabular()
        elif choice.upper() in ("Q", "QUIT"):
            print("\nExiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose s, o, f, or q.")

        input("\nPress Enter to continue…")


if __name__ == "__main__":
    main()
