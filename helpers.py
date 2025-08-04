"""
MUTATION TOLERANCE ASSEMBLY HELPER FUNCTIONS
"""


def find_approximate_overlap(seq1, seq2, min_overlap=18, max_mismatches=3):
    """
    Find the best approximate overlap between two sequences
    Returns tuple: (overlap_length, mismatch_count, merged_sequence)
    """
    best_overlap = 0
    best_mismatches = float("inf")
    merged_seq = None

    # Check suffix of seq1 vs prefix of seq2
    for overlap in range(min_overlap, min(len(seq1), len(seq2)) + 1):
        suffix = seq1[-overlap:]
        prefix = seq2[:overlap]
        mismatches = sum(1 for a, b in zip(suffix, prefix) if a != b)

        if mismatches <= max_mismatches and mismatches < best_mismatches:
            best_overlap = overlap
            best_mismatches = mismatches
            merged_seq = seq1 + seq2[overlap:]

    # Check prefix of seq1 vs suffix of seq2
    for overlap in range(min_overlap, min(len(seq1), len(seq2)) + 1):
        prefix = seq1[:overlap]
        suffix = seq2[-overlap:]
        mismatches = sum(1 for a, b in zip(prefix, suffix) if a != b)

        if mismatches <= max_mismatches and mismatches < best_mismatches:
            best_overlap = overlap
            best_mismatches = mismatches
            merged_seq = seq2 + seq1[overlap:]

    return (
        (best_overlap, best_mismatches, merged_seq)
        if best_overlap >= min_overlap
        else (0, 0, None)
    )


"""
RANGE-BASED ASSEMBLY HELPER FUNCTIONS
"""


class SequenceWithRange:
    def __init__(self, header, sequence, contig=None, start=None, end=None):
        self.header = header
        self.sequence = sequence
        self.contig = contig
        self.start = start
        self.end = end

    def __len__(self):
        return len(self.sequence)

    def __repr__(self):
        return f"Sequence({self.header}, {self.contig}:{self.start}-{self.end})"


def parse_fasta_with_ranges(fasta_file):
    """
    Parse FASTA files with genomic range information in headers
    Expected header format: >accession|contig:start-end
    """
    fasta_dict = {}
    try:
        with open(fasta_file, "r") as f:
            current_header = ""
            current_seq = []
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    if current_header:
                        header, contig, start, end = parse_header_ranges(current_header)
                        seq = "".join(current_seq)
                        fasta_dict[header] = SequenceWithRange(
                            header, seq, contig, start, end
                        )

                    current_header = line[1:]
                    current_seq = []
                else:
                    current_seq.append(line)

            if current_header:
                header, contig, start, end = parse_header_ranges(current_header)
                seq = "".join(current_seq)
                fasta_dict[header] = SequenceWithRange(header, seq, contig, start, end)

        return fasta_dict
    except Exception as e:
        print(f"Error parsing FASTA: {str(e)}")
        return {}


def parse_header_ranges(header):
    """
    Extract genomic range from FASTA header
    Supports formats:
      >accession|contig:start-end
      >accession contig:start-end
    """
    accession = header.split()[0]
    contig, start, end = None, None, None

    # Try pipe-separated format
    if "|" in header:
        parts = header.split("|")
        if len(parts) > 1:
            range_info = parts[1].strip()
    else:
        # Try space-separated format
        range_info = header.split(" ")[-1].strip()

    # Parse range information
    if ":" in range_info and "-" in range_info:
        contig_part, range_part = range_info.split(":", 1)
        contig = contig_part.strip()

        if "-" in range_part:
            start_str, end_str = range_part.split("-", 1)
            try:
                start = int(start_str)
                end = int(end_str)
            except ValueError:
                # Handle non-integer ranges gracefully
                pass

    return accession, contig, start, end


def cluster_by_genomic_range(sequences, overlap_threshold=0.8):
    """Group sequences by overlapping genomic positions"""
    # Group by contig first
    contig_groups = {}
    for seq in sequences:
        # Skip sequences without range info
        if not seq.contig or seq.start is None or seq.end is None:
            continue

        if seq.contig not in contig_groups:
            contig_groups[seq.contig] = []
        contig_groups[seq.contig].append(seq)

    # Cluster each contig group
    clusters = []
    for contig, seqs in contig_groups.items():
        # Sort by start position
        sorted_seqs = sorted(seqs, key=lambda x: x.start)

        current_cluster = []
        last_end = -1

        for seq in sorted_seqs:
            # First sequence in cluster
            if not current_cluster:
                current_cluster.append(seq)
                last_end = seq.end
                continue

            # Check for overlap
            overlap = min(seq.end, last_end) - seq.start
            seq_length = seq.end - seq.start

            if overlap > 0:
                # Calculate overlap percentage
                overlap_percent = overlap / seq_length if seq_length > 0 else 0

                if overlap_percent >= overlap_threshold:
                    current_cluster.append(seq)
                    last_end = max(last_end, seq.end)
                    continue

            # Finalize current cluster and start new one
            clusters.append(current_cluster)
            current_cluster = [seq]
            last_end = seq.end

        # Add last cluster for contig
        if current_cluster:
            clusters.append(current_cluster)

    return clusters
