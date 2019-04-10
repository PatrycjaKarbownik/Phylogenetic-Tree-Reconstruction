from parallel import simple_parallel, parallel  # , recursive_needleman_wunsch
from symmetric_matrix import SymmetricMatrix


def calculate_similarities_aligned(leaves):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            matrix[row, column] = simple_parallel(leaves[row].sequence, leaves[column].sequence)
    return matrix


def calculate_similarities(leaves):
    matrix = SymmetricMatrix(len(leaves))
    for row in range(len(matrix)):
        for column in range(row + 1):
            if row == column: continue
            # matrix[row, column] = recursive_needleman_wunsch(leaves[row].sequence, leaves[column].sequence,
            #                                                 0, len(leaves[column].sequence), 0)
            matrix[row, column] = parallel(leaves[row].sequence, leaves[column].sequence)
    return matrix


def _reference_sequence_index(similarity_matrix, leaves):
    max = -1
    index = -1
    for column in range(len(leaves)):
        sum = 0
        for row in range(len(leaves)):
            sum += similarity_matrix[column, row]
        if sum > max:
            max = sum
            index = column
    return index


def multiple_alignment(similarity_matrix, leaves):
    reference_sequence_index = _reference_sequence_index(similarity_matrix, leaves)
    # pairwise alignment
    # aligned_sequences = [["ATTGCCATT", "ATGGCCATT"], ["ATTGCCATT", "ATCTTC-TT"], ["ATTGCCATT--", "ATC-CAATTTT"],
    #                     ["ATTGCCATT", "ACTGACC--"]]
    aligned_sequences = [["ACT", "TCT"], ["ACT", "-CT"], ["A-CT", "ATCT"], ["ACT", "ACT"]]

    multiple_aligned_sequences = [aligned_sequences[0][0], aligned_sequences[0][1]]
    print(aligned_sequences)
    print(multiple_aligned_sequences)

    for pair in range(1, len(aligned_sequences)):
        print("pair = ", pair)
        aligned_guide = aligned_sequences[pair][0]
        aligned_sequence = aligned_sequences[pair][1]
        multiple_guide = multiple_aligned_sequences[0]
        print("aligned guide = ", aligned_guide)
        print("aligned sequence = ", aligned_sequence)
        print("multiple_guide = ", multiple_guide)
        # if len(aligned_guide) > len(multiple_guide):
        #     longer = len(aligned_guide)
        #     print("longer if = ", longer)
        # else:
        #     longer = len(multiple_guide)
        #     print("longer else = ", longer)
        if len(aligned_guide) > len(multiple_guide):
            longer = len(multiple_guide)
            print("longer if = ", longer)
        else:
            longer = len(aligned_guide)
            print("longer else = ", longer)

        for column in range(longer):
            # print("column = ", column)
            # print("len multiple = ", len(multiple_aligned_sequences[0]))
            # print("len aligned = ", len(aligned_sequences[pair][0]))

            if multiple_aligned_sequences[0][column] == '-' and aligned_sequences[pair][0][column] != '-':
                aligned_sequences[pair][1] = aligned_sequences[pair][1][:column] + '-' \
                                             + aligned_sequences[pair][1][column:]
                print("aligned sequence AFTER = ", aligned_sequences[pair][1])
            elif aligned_sequences[pair][0][column] == '-' and multiple_aligned_sequences[0][column] != '-':
                print("WELCOME")
                for sequence in range(len(multiple_aligned_sequences)):
                    print("sequence = ", sequence)
                    multiple_aligned_sequences[sequence] = str(multiple_aligned_sequences[sequence][:column]) + '-' \
                                                           + str(multiple_aligned_sequences[sequence][column:])
                    print("multiple_aligned_sequences[sequence] AFTER1 = ", multiple_aligned_sequences[sequence])

        # print("Aligned guide len: " + str(len(aligned_sequences[pair][0])))
        # print("Multiple Aligned guide len: " + str(len(multiple_aligned_sequences[0])))
        # print("Aligned guide: " + aligned_sequence[pair][0])
        # print("Aligned guide: " + multiple_aligned_sequences[0])

        if len(aligned_sequences[pair][0]) > len(multiple_aligned_sequences[0]):
            temp = len(aligned_sequences[pair][0]) - len(multiple_aligned_sequences[0])
            for sequence in range(len(multiple_aligned_sequences)):
                print("sequence = ", sequence)
                for i in range(temp):
                    multiple_aligned_sequences[sequence] += '-'
                    print("multiple_aligned_sequences[sequence] AFTER2 = ", multiple_aligned_sequences[sequence])

        if len(aligned_sequences[pair][0]) < len(multiple_aligned_sequences[0]):
            for i in range(len(multiple_aligned_sequences[0]) - len(aligned_sequences[pair][0])):
                aligned_sequences[pair][1] += '-'

        # print("Aligned guide len: " + str(len(aligned_sequences[pair][0])))
        # print("Multiple Aligned guide len: " + str(len(multiple_aligned_sequences[0])))
        # print("Aligned guide: " + aligned_sequence[pair][0])
        # print("Aligned guide: " + multiple_aligned_sequences[0])

        #    column = 0
        # while column < longer:
        #     print("column = ", column)
        #     print("len multiple = ", len(multiple_aligned_sequences[0]))
        #     print("len aligned = ", len(aligned_sequences[pair][0]))
        #   #  print("ALIGN: ", aligned_sequences[pair][0][column])
        #    #  print("MULT: ", multiple_aligned_sequences[0][column])
        #
        #     if len(multiple_aligned_sequences[0]) <= column:
        #         print("JESTEM MULT")
        #         #  multiple_aligned_sequences[0] += '-'
        #         for sequence in range(len(multiple_aligned_sequences)):
        #             print("sequence = ", sequence)
        #             multiple_aligned_sequences[sequence] = str(multiple_aligned_sequences[sequence][:column]) + '-' \
        #                                                    + str(multiple_aligned_sequences[sequence][column:])
        #             print("multiple_aligned_sequences[sequence] AFTER = ", multiple_aligned_sequences[sequence])
        #     elif len(aligned_sequences[pair][0]) <= column:
        #         print("JESTEM ALIGN")
        #         aligned_sequences[pair][0] += '-'
        #         longer += 1
        #     elif multiple_aligned_sequences[0][column] == '-' and aligned_sequences[pair][0][column] != '-':
        #         aligned_sequences[pair][1] = aligned_sequences[pair][1][:column] + '-' \
        #                                      + aligned_sequences[pair][1][column:]
        #         print("aligned sequence AFTER = ", aligned_sequences[pair][1])
        #     elif aligned_sequences[pair][0][column] == '-' and multiple_aligned_sequences[0][column] != '-':
        #         print("WELCOME")
        #         for sequence in range(len(multiple_aligned_sequences)):
        #             print("sequence = ", sequence)
        #             multiple_aligned_sequences[sequence] = str(multiple_aligned_sequences[sequence][:column]) + '-' \
        #                                                    + str(multiple_aligned_sequences[sequence][column:])
        #             print("multiple_aligned_sequences[sequence] AFTER = ", multiple_aligned_sequences[sequence])
        #     column += 1
        multiple_aligned_sequences.append(aligned_sequences[pair][1])
        print(multiple_aligned_sequences)

    print(multiple_aligned_sequences)
