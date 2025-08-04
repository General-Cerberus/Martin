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
