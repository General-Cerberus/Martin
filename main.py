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
      - https://en.wikipedia.org/wiki/NP-hardness
    - Maybe implement a greedy algorithm to find overlaps: https://en.wikipedia.org/wiki/Sequence_assembly#Assembly_algorithms
  - To add:
    - Multiprocessing support.
      - Could array comparisons be more efficient than string comparisons?
      - https://numpy.org/doc/stable/reference/generated/numpy.isin.html#numpy.isin
    - Mutation tolerance.
      - Partial string matching.
      - Amino acid sequence matching vs. nucleotide sequence matching.
    - BLASTX integration for pre-sorting of sequences.
      - Partitioning the data in advance will drastically reduce the number of comparisons needed.

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
from helpers import (
    cluster_by_genomic_range,
    find_approximate_overlap,
    parse_fasta_with_ranges,
    parse_header_ranges,
    SequenceWithRange,
)


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


def assemble_sequences(seq_list, min_overlap=18, max_mismatches=3, mutation_rate=0.01):
    """
    Assemble sequences with mutation tolerance
    """
    if not seq_list:
        return []
    if len(seq_list) == 1:
        return seq_list

    # Normalize sequences
    seqs = list(set([s.upper() for s in seq_list]))

    # Get parameters from user if not provided
    if min_overlap is None:
        min_overlap = int(input("Enter minimum overlap length (default 18): ") or 18)
    if max_mismatches is None:
        max_mismatches = int(input("Enter max allowed mismatches (default 3): ") or 3)

    # Track merged sequences
    merged = [False] * len(seqs)
    contigs = []

    for i in range(len(seqs)):
        if merged[i]:
            continue

        current_contig = seqs[i]
        merged[i] = True
        made_merge = True

        while made_merge:
            made_merge = False
            best_candidate = None
            best_overlap = min_overlap - 1  # Initialize below threshold
            best_mismatches = max_mismatches + 1
            best_merged = None

            for j in range(len(seqs)):
                if merged[j]:
                    continue

                # Calculate approximate overlap
                overlap_len, mismatches, merged_seq = find_approximate_overlap(
                    current_contig, seqs[j], min_overlap, max_mismatches
                )

                # Calculate quality score (higher is better)
                quality = overlap_len * (1 - mutation_rate) - mismatches * mutation_rate

                # Update best candidate
                if quality > best_overlap:
                    best_candidate = j
                    best_overlap = quality
                    best_mismatches = mismatches
                    best_merged = merged_seq

            # Merge if we found a suitable candidate
            if best_merged:
                current_contig = best_merged
                merged[best_candidate] = True
                made_merge = True
                print(
                    f"Merged with {best_overlap:.1f} quality (overlap: {best_overlap}, mismatches: {best_mismatches})"
                )

        contigs.append(current_contig)

    return contigs


def assemble_sequences_with_ranges(sequences, min_overlap=18, max_mismatches=3):
    """
    Assemble sequences grouped by genomic range
    """
    # Cluster sequences by genomic range.
    clusters = cluster_by_genomic_range(sequences)
    print(f"Grouped {len(sequences)} sequences into {len(clusters)} genomic clusters")

    assembled_contigs = []

    for i, cluster in enumerate(clusters):
        print(
            f"\nAssembling cluster {i+1}/{len(clusters)}: "
            f"{len(cluster)} sequences, contig={cluster[0].contig}"
        )

        # Extract sequences for assembly.
        seq_list = [seq.sequence for seq in cluster]

        # Assemble this cluster.
        contigs = assemble_sequences(
            seq_list, min_overlap=min_overlap, max_mismatches=max_mismatches
        )

        # Create headers with cluster info.
        for j, contig_seq in enumerate(contigs):
            header = (
                f"Cluster_{i+1}_Contig_{j+1}_"
                f"ContigID={cluster[0].contig}_"
                f"Sources={len(cluster)}_"
                f"Length={len(contig_seq)}"
            )

            # Try to determine genomic range for contig.
            min_start = min(seq.start for seq in cluster if seq.start is not None)
            max_end = max(seq.end for seq in cluster if seq.end is not None)
            range_info = ""
            if min_start is not None and max_end is not None:
                range_info = f"|GenomicRange:{min_start}-{max_end}"

            assembled_contigs.append(
                SequenceWithRange(
                    header + range_info,
                    contig_seq,
                    contig=cluster[0].contig,
                    start=min_start,
                    end=max_end,
                )
            )

    return assembled_contigs


def assemble_mode():
    print("\n" + "=" * 50)
    print("= Enhanced Assembly with Mutation Tolerance & Range Support =")
    print("=" * 50 + "\n")

    # Initialize storage for sequences with range data.
    sequences = []

    # Get input file from user.
    input_file = input(
        "Enter FASTA file with range information (or press Enter for manual input): "
    ).strip()

    # File-based input.
    if input_file:
        if not os.path.exists(input_file):
            print(f"Error: File {input_file} not found.")
            return

        # Parse FASTA with range information.
        fasta_dict = parse_fasta_with_ranges(input_file)
        if not fasta_dict:
            return

        sequences = list(fasta_dict.values())
        print(f"Loaded {len(sequences)} sequences with genomic ranges")

    # Manual input option.
    else:
        print("\nManual Sequence Input with Genomic Ranges")
        print("Format: sequence|contig:start-end")
        print("Example: ATGCGATACGT|NC_001416:1024-49526")
        print("Leave range empty for sequences without position data")

        while True:
            user_input = input(
                "\nEnter sequence with range (or blank to finish): "
            ).strip()
            if not user_input:
                break

            # Parse manual input.
            if "|" in user_input:
                seq_part, range_part = user_input.split("|", 1)
                header = f"Manual|{range_part}"
                accession, contig, start, end = parse_header_ranges(header)
                sequences.append(
                    SequenceWithRange(accession, seq_part.upper(), contig, start, end)
                )
                print(f"Added sequence: {contig}:{start}-{end} ({len(seq_part)} bp)")
            else:
                sequences.append(SequenceWithRange("Manual", user_input.upper()))
                print(f"Added sequence without range ({len(user_input)} bp)")

    if not sequences:
        print("No sequences provided.")
        return

    # Get assembly parameters.
    print("\nAssembly Parameters:")
    min_overlap = int(input("  Minimum overlap length (default 18): ") or 18)
    max_mismatches = int(input("  Max allowed mismatches (default 3): ") or 3)
    mutation_rate = float(input("  Estimated mutation rate (default 0.01): ") or 0.01)
    overlap_threshold = float(
        input("  Genomic overlap threshold (0.0-1.0, default 0.8): ") or 0.8
    )

    # Cluster sequences by genomic range.
    clusters = cluster_by_genomic_range(sequences, overlap_threshold)

    # Separate clustered and unclustered sequences.
    clustered_seqs = [seq for cluster in clusters for seq in cluster]
    unclustered_seqs = [seq for seq in sequences if seq not in clustered_seqs]

    print(f"\nClustering Results:")
    print(f"- Formed {len(clusters)} genomic clusters")
    print(f"- {len(clustered_seqs)} sequences grouped by genomic position")
    print(f"- {len(unclustered_seqs)} sequences without position data")

    # Assemble each cluster separately.
    assembled_contigs = []

    # Process genomic clusters.
    for i, cluster in enumerate(clusters):
        print(
            f"\nAssembling Cluster {i+1}/{len(clusters)}: "
            f"contig={cluster[0].contig}, "
            f"{len(cluster)} sequences, "
            f"span={min(s.start for s in cluster)}-{max(s.end for s in cluster)}"
        )

        # Extract sequences for assembly.
        seq_list = [seq.sequence for seq in cluster]

        # Assemble with mutation tolerance.
        contigs = assemble_sequences(
            seq_list,
            min_overlap=min_overlap,
            max_mismatches=max_mismatches,
            mutation_rate=mutation_rate,
        )

        # Create annotated headers.
        for j, contig_seq in enumerate(contigs):
            min_start = min(seq.start for seq in cluster)
            max_end = max(seq.end for seq in cluster)
            sources = len([seq for seq in cluster if seq.sequence in contig_seq])

            header = (
                f"Cluster_{i+1}_Contig_{j+1}_"
                f"Contig={cluster[0].contig}_"
                f"Sources={sources}_"
                f"Length={len(contig_seq)}"
            )

            if min_start and max_end:
                header += f"|GenomicRange:{min_start}-{max_end}"

            assembled_contigs.append(
                SequenceWithRange(
                    header,
                    contig_seq,
                    contig=cluster[0].contig,
                    start=min_start,
                    end=max_end,
                )
            )

    # Process unclustered sequences.
    if unclustered_seqs:
        print(f"\nAssembling {len(unclustered_seqs)} unclustered sequences...")
        seq_list = [seq.sequence for seq in unclustered_seqs]
        contigs = assemble_sequences(
            seq_list,
            min_overlap=min_overlap,
            max_mismatches=max_mismatches,
            mutation_rate=mutation_rate,
        )

        for j, contig_seq in enumerate(contigs):
            sources = len(
                [seq for seq in unclustered_seqs if seq.sequence in contig_seq]
            )
            header = (
                f"Unclustered_Contig_{j+1}_"
                f"Sources={sources}_"
                f"Length={len(contig_seq)}"
            )

            assembled_contigs.append(SequenceWithRange(header, contig_seq))

    # Output results.
    print("\nAssembly complete!")
    print(
        f"Generated {len(assembled_contigs)} contigs from {len(sequences)} input sequences"
    )

    # Save to file.
    output_file = input("\nEnter output filename (.fasta): ")
    try:
        with open(output_file, "w") as out:
            for contig in assembled_contigs:
                out.write(f">{contig.header}\n{contig.sequence}\n")
        print(f"Results saved to {output_file}")

        # Generate cluster report.
        report_file = os.path.splitext(output_file)[0] + "_report.csv"
        with open(report_file, "w") as report:
            report.write("Cluster,Contig,ContigID,Start,End,Length,Sources,Type\n")
            for contig in assembled_contigs:
                parts = contig.header.split("_")
                cluster_id = parts[1] if "Cluster" in contig.header else "NA"
                contig_id = parts[3] if len(parts) > 3 else "1"
                report.write(f"{cluster_id},{contig_id},{contig.contig or 'NA'},")
                report.write(f"{contig.start or 'NA'},{contig.end or 'NA'},")
                report.write(f"{len(contig.sequence)},")
                report.write(f"{contig.header.split('Sources=')[1].split('_')[0]},")
                report.write(f"{'Genomic' if contig.contig else 'Unclustered'}\n")
        print(f"Cluster report saved to {report_file}")

    except IOError as e:
        print(f"Error saving results: {str(e)}")


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
    print("\n" + "=" * 46)
    print("= Viral Genome Assembly Toolkit (Mutation + Range Support) =")
    print("=" * 46)
    print("Features:")
    print("- Mutation-tolerant assembly (viral quasi-species support)")
    print("- Genomic range-based clustering")
    print("- Detailed assembly reporting\n")

    while True:
        print("\nMain Menu:")
        print("  s : Extract sequences by accession")
        print("  o : Assemble sequences with mutation tolerance & range support")
        print("  f : Filter tabular file by column content")
        print("  q : Quit")

        choice = input("\nSelect mode: ").lower()

        if choice in ("s", "extract"):
            extract_sequences()
        elif choice in ("o", "0", "assemble"):
            assemble_mode()
        elif choice in ("f", "filter"):
            filter_tabular()
        elif choice in ("q", "quit"):
            print("\nExiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose s, o, f, or q.")

        input("\nPress Enter to continue...")
