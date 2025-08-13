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

    # Check suffix of seq1 vs prefix of seq2.
    for overlap in range(min_overlap, min(len(seq1), len(seq2)) + 1):
        suffix = seq1[-overlap:]
        prefix = seq2[:overlap]
        mismatches = sum(1 for a, b in zip(suffix, prefix) if a != b)

        if mismatches <= max_mismatches and mismatches < best_mismatches:
            best_overlap = overlap
            best_mismatches = mismatches
            merged_seq = seq1 + seq2[overlap:]

    # Check prefix of seq1 vs suffix of seq2.
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

    # Try pipe-separated format.
    if "|" in header:
        parts = header.split("|")
        if len(parts) > 1:
            range_info = parts[1].strip()
    else:
        # Try space-separated format.
        range_info = header.split(" ")[-1].strip()

    # Parse range information.
    if ":" in range_info and "-" in range_info:
        contig_part, range_part = range_info.split(":", 1)
        contig = contig_part.strip()

        if "-" in range_part:
            start_str, end_str = range_part.split("-", 1)
            try:
                start = int(start_str)
                end = int(end_str)
            except ValueError:
                # Handle non-integer ranges gracefully.
                pass

    return accession, contig, start, end


def cluster_by_genomic_range(sequences, overlap_threshold=0.8):
    """Group sequences by overlapping genomic positions"""
    # Group by contig first.
    contig_groups = {}
    for seq in sequences:
        # Skip sequences without range info.
        if not seq.contig or seq.start is None or seq.end is None:
            continue

        if seq.contig not in contig_groups:
            contig_groups[seq.contig] = []
        contig_groups[seq.contig].append(seq)

    # Cluster each contig group.
    clusters = []
    for contig, seqs in contig_groups.items():
        # Sort by start position.
        sorted_seqs = sorted(seqs, key=lambda x: x.start)

        current_cluster = []
        last_end = -1

        for seq in sorted_seqs:
            # First sequence in cluster.
            if not current_cluster:
                current_cluster.append(seq)
                last_end = seq.end
                continue

            # Check for overlap.
            overlap = min(seq.end, last_end) - seq.start
            seq_length = seq.end - seq.start

            if overlap > 0:
                # Calculate overlap percentage.
                overlap_percent = overlap / seq_length if seq_length > 0 else 0

                if overlap_percent >= overlap_threshold:
                    current_cluster.append(seq)
                    last_end = max(last_end, seq.end)
                    continue

            # Finalize current cluster and start new one.
            clusters.append(current_cluster)
            current_cluster = [seq]
            last_end = seq.end

        # Add last cluster for contig.
        if current_cluster:
            clusters.append(current_cluster)

    return clusters


"""
PROBABILISTIC ASSEMBLY FUNCTIONS
"""
import math


def find_best_paths(graph, sequences):
    """Find highest probability paths using dynamic programming"""
    # Find starting nodes (nodes with no incoming edges).
    all_targets = set()
    for edges in graph.values():
        for edge in edges:
            all_targets.add(edge[0])  # edge[0] is the neighbor index.

    start_nodes = [i for i in graph if i not in all_targets]

    # If no clear start nodes, use all nodes.
    if not start_nodes:
        start_nodes = list(graph.keys())

    # Track best paths.
    best_paths = []

    for start in start_nodes:
        # Initialize DP table: (current_node, path, path_score).
        dp = [(start, [start], 0.0)]
        completed_paths = []

        while dp:
            current, path, score = dp.pop(0)
            extended = False

            # Check if current node has outgoing edges.
            if current in graph:
                for edge in graph[current]:
                    neighbor, edge_score, _ = edge
                    # Avoid cycles.
                    if neighbor in path:
                        continue

                    # Calculate new path score.
                    new_score = score + edge_score
                    new_path = path + [neighbor]
                    dp.append((neighbor, new_path, new_score))
                    extended = True

            # If no extensions, path is complete.
            if not extended:
                completed_paths.append((path, score))

        # Find best path from this start node.
        if completed_paths:
            best_path = max(completed_paths, key=lambda x: x[1])[0]
            best_paths.append(best_path)

    # Convert paths to sequences.
    contigs = []
    for path in best_paths:
        if len(path) == 1:
            contigs.append(sequences[path[0]])
            continue

        # Build contig from path.
        current_seq = sequences[path[0]]
        for i in range(1, len(path)):
            prev_idx = path[i - 1]
            current_idx = path[i]
            seq_j = sequences[current_idx]

            # Find the overlap info for this edge.
            overlap = 0
            for edge in graph.get(prev_idx, []):
                if edge[0] == current_idx:
                    overlap = edge[2]  # The third element is overlap length.
                    break

            current_seq += seq_j[overlap:]

        contigs.append(current_seq)

    return contigs


def find_best_overlap(seq1, seq2, min_overlap, max_mismatches):
    """
    Find best approximate overlap between two sequences
    Returns: (overlap_length, mismatch_count)
    """
    best_overlap = 0
    best_mismatches = max_mismatches + 1
    len1, len2 = len(seq1), len(seq2)

    # Check suffix of seq1 vs prefix of seq2
    for overlap in range(min_overlap, min(len1, len2) + 1):
        suffix = seq1[-overlap:]
        prefix = seq2[:overlap]
        mismatches = sum(1 for a, b in zip(suffix, prefix) if a != b)

        if mismatches <= max_mismatches and mismatches < best_mismatches:
            best_overlap = overlap
            best_mismatches = mismatches

    # Check prefix of seq1 vs suffix of seq2
    for overlap in range(min_overlap, min(len1, len2) + 1):
        prefix = seq1[:overlap]
        suffix = seq2[-overlap:]
        mismatches = sum(1 for a, b in zip(prefix, suffix) if a != b)

        if mismatches <= max_mismatches and mismatches < best_mismatches:
            best_overlap = overlap
            best_mismatches = mismatches

    return best_overlap, best_mismatches


def calculate_probability_score(overlap_len, mismatches, mutation_rate):
    """
    Calculate log-probability score for an overlap:
    score = (overlap_len - mismatches)*log(1-mutation_rate) + mismatches*log(mutation_rate)
    """
    if mutation_rate <= 0 or mutation_rate >= 1:
        mutation_rate = 0.01  # Default to 1% mutation rate

    # Avoid log(0) issues
    safe_log = lambda x: math.log(max(x, 1e-10))

    match_score = (overlap_len - mismatches) * safe_log(1 - mutation_rate)
    mismatch_score = mismatches * safe_log(mutation_rate)
    return match_score + mismatch_score


def probabilistic_assembly(
    seq_list, min_overlap=18, max_mismatches=3, mutation_rate=0.01
):
    """
    Probabilistic assembly using likelihood scores and path optimization
    """
    if len(seq_list) <= 1:
        return seq_list

    # Build overlap graph
    graph = build_overlap_graph(seq_list, min_overlap, max_mismatches, mutation_rate)

    # Find best paths using probabilistic scoring
    contigs = find_best_paths(graph, seq_list)

    return contigs


def build_overlap_graph(sequences, min_overlap, max_mismatches, mutation_rate):
    """Construct directed graph of sequence overlaps with probability scores"""
    graph = {i: [] for i in range(len(sequences))}

    for i in range(len(sequences)):
        for j in range(len(sequences)):
            if i == j:
                continue

            # Check suffix of i to prefix of j
            overlap, mismatches = find_best_overlap(
                sequences[i], sequences[j], min_overlap, max_mismatches
            )

            if overlap >= min_overlap:
                # Calculate probability score
                prob_score = calculate_probability_score(
                    overlap, mismatches, mutation_rate
                )
                graph[i].append((j, prob_score, overlap))

    return graph
