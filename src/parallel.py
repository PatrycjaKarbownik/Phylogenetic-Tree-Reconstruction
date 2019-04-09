import numpy as np

A = 0
G = 1
C = 2
T = 3
GAP = 4

gap_penalty = -5

substitution_matrix = [[10,             -1,             -3,             -4,     gap_penalty],
                       [-1,              7,             -5,             -3,     gap_penalty],
                       [-3,             -5,              9,              0,     gap_penalty],
                       [-4,             -3,              0,              8,     gap_penalty],
                       [gap_penalty, gap_penalty,  gap_penalty,  gap_penalty,       2]]


def _match_score(nucleotide1, nucleotide2):
    return {
        ('A', 'A'): substitution_matrix[A][A],
        ('A', 'G'): substitution_matrix[A][G],
        ('A', 'C'): substitution_matrix[A][C],
        ('A', 'T'): substitution_matrix[A][T],
        ('A', '-'): substitution_matrix[A][GAP],
        ('G', 'A'): substitution_matrix[G][A],
        ('G', 'G'): substitution_matrix[G][G],
        ('G', 'C'): substitution_matrix[G][C],
        ('G', 'T'): substitution_matrix[G][T],
        ('G', '-'): substitution_matrix[G][GAP],
        ('C', 'A'): substitution_matrix[C][A],
        ('C', 'G'): substitution_matrix[C][G],
        ('C', 'C'): substitution_matrix[C][C],
        ('C', 'T'): substitution_matrix[C][T],
        ('C', '-'): substitution_matrix[C][GAP],
        ('T', 'A'): substitution_matrix[T][A],
        ('T', 'G'): substitution_matrix[T][G],
        ('T', 'C'): substitution_matrix[T][C],
        ('T', 'T'): substitution_matrix[T][T],
        ('T', '-'): substitution_matrix[T][GAP],
        ('-', 'A'): substitution_matrix[GAP][A],
        ('-', 'G'): substitution_matrix[GAP][G],
        ('-', 'T'): substitution_matrix[GAP][T],
        ('-', 'C'): substitution_matrix[GAP][C],
        ('-', '-'): substitution_matrix[GAP][GAP],

    }[nucleotide1, nucleotide2]


def simple_parallel(seq1, seq2):  # compare two sequences char-to-char
    length_of_seq = len(seq1)
    score = 0
    for i in range(length_of_seq):
        score += _match_score(seq1[i], seq2[i])

    return score


def _max_match(score, i, nucleotide1, nucleotide2):
    match = score[i-1][0] + _match_score(nucleotide1, nucleotide2)
    gap_first = score[i][0] + gap_penalty
    gap_second = score[i-1][1] + gap_penalty

    return max(match, gap_first, gap_second)


def _swap_columns(array, frm, to):
    array[:, [frm, to]] = array[:, [to, frm]]


def parallel(seq1, seq2):
    length_of_seq1, length_of_seq2 = len(seq1), len(seq2)
    score = np.empty([length_of_seq1 + 1, 2], int)  # use matrix with 2 columns to minimalizing computational complexity

    # prepare temp table to calculate score for the best alignment
    for x in range(length_of_seq1 + 1):
        score[x][0] = x * gap_penalty
        score[x][1] = 0

    # stripped Needleman-Wunsch algorithm using dynamic programming
    j = 1
    while j <= length_of_seq2:
        score[0][1] = j * gap_penalty
        i = 1
        while i <= length_of_seq1:
            score[i][1] = _max_match(score, i, seq1[i - 1], seq2[j - 1])  # calculating the best score using calculations for shorter sequences
            i += 1
        _swap_columns(score, 0, 1)  # swap to ease operations on matrix
        j += 1

    return score[length_of_seq1][0]


if __name__ == "__main__":
    input = open("../data/sequences.txt", "r")

    sequence1 = input.readline().rstrip('\n')
    sequence2 = input.readline().rstrip('\n')

    print(parallel(sequence1, sequence2))
