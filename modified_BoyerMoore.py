# Dini Irdina Ahmad Ubaidah, 31279279
# Acknowledgement & Credits: Lecture notes, tutorial videos, sanity check session, youtube video (Ben Langmead), Wikipedia

from audioop import reverse
import sys

def zalgo(string):
    zarray = [0] * len(string)
    zarray[0] = len(string)

    l, r = 0, 0

    i = 1
    while i < len(string):
        remaining = r - i + 1
        k = i - l

        # Case 1: outside box
        if i > r:
            for j in range(i, len(string)):
                if string[j] == string[j-i]:
                    zarray[i] += 1 
                else:
                    break
            l, r = i, i + zarray[i] - 1
        # Case 2: inside box
        else:
            # Case 2a
            if zarray[k] < remaining:
                zarray[i] = zarray[k]
            # Case 2b
            elif zarray[k] > remaining:
                zarray[i] = remaining
            # Case 2c
            elif zarray[k] == remaining:
                matches = 0
                for j in range(r+1, len(string)):
                    if string[j] == string[j - i]:
                        matches += 1
                    else:
                        break
                l, r = i, r + matches
                zarray[i] = r - i + 1
        i += 1

    return zarray


def bad_character_table(pattern):
    """Function used to generate the bad character table. Ensures O(1) lookup 
       for bad character rule."""

    # There are 95 printable ascii characters
    table = [None] * 96

    for i in range(len(pattern)-1, -1, -1):
        # -32 because printable ascii starts from 32
        ascii_pos = ord(pattern[i]) -32

        # initialise  positions to -1 if character is found for the first time
        if table[ascii_pos] == None:
            table[ascii_pos] = [-1] * len(pattern)
        table[ascii_pos][i] = i

        # ensure that the rightmost position is recorded in other indexes
        if i < len(pattern) - 1 and table[ascii_pos][i+1] == -1:
            counter = 1
            while (i+counter) < len(pattern) and table[ascii_pos][i+counter] == -1:
                table[ascii_pos][i+counter] = i
                counter += 1
    return table


def bad_character_shift(bc_table, position, mismatch_char, pat_length):
    """Function returns the number of shifts calculated by bad character rule. If no bad character, return the number of shifts
       needed to move the pattern over the mismatch character in the text."""

    mismatch_ascii = ord(mismatch_char) -32
    if bc_table[mismatch_ascii] != None and bc_table[mismatch_ascii][position-1] >= 0:
        return pat_length - bc_table[mismatch_ascii][position-1] - 1
    else:
        return position + 1 


def good_suffix_array(pattern):
    """Function used to find good suffixes. It performs z algorithm on a reversed string, then reverses the results again. 
       Then it uses this to creates the good suffix array. The function returns both the gs array and the reverse z array."""
    # Reversing process
    rev_pattern = pattern[::-1]
    rev_z = zalgo(rev_pattern)
    rev_z.reverse()

    gs_array = [-1] * (len(pattern)+1)
    for i in range(0, len(pattern)):
        j = len(pattern) - rev_z[i]
        gs_array[j] = i

    return [gs_array, rev_z]


def good_suffix(pattern, suffix_length, position, gs_array, reverse_z_array, bc_table, mismatch_char):
    mismatch_char_ascii = ord(mismatch_char) -32
    """Function returns a good suffix position only if the char before that good suffix matches the mismatched
       char from the text."""

    if gs_array[position+1] <= 0: # no good suffix exists, so exit
        return 0

    char_before_suffix = position + 1 - gs_array[position+1]

    if pattern[char_before_suffix] == mismatch_char: # check if the char before the suffix matches the mismatched char from string
        return gs_array[position+1] 

    # loop through z suffix array to find a good suffix that has a char before it that matches the mismatch char from string
    for i in range(char_before_suffix, -1, -1):

        if reverse_z_array[i] == suffix_length: # checking for the suffix
            char_before_suffix = i - suffix_length  # position of char before suffix

            if bc_table[mismatch_char_ascii] != None and bc_table[mismatch_char_ascii][position] == char_before_suffix:
                shifts = position - (i - suffix_length)
                return shifts

    return 0 # if no good suffix found, return 0


def matched_prefix(pattern):
    """Function returns the number of shifts using matched prefix."""

    z_array = zalgo(pattern)
    mp_array = [0] * len(pattern)
    p_length =  len(pattern)

    for i in range(len(pattern)-1, 0, -1):
        if z_array[i] > 0 and z_array[i] + i == len(pattern):
            mp_array[i] = z_array[i]

        else:
            if i != len(pattern) - 1:
                mp_array[i] = mp_array[i+1]

    if mp_array[1] == 0:  # if no matched prefix, return 0
        return 0

    max_shifts = p_length - mp_array[1]
    return max_shifts


def Boyer_Moore(pattern, string):
    """Main Boyer Moore function. It runs the modified good suffix but if a good suffix isn't found, the matched prefix will be 
       used (only if it meets the required conditions). If matched prefix also fails, the last resort is running the normal bad character
       rule."""
    shift_pointer = len(pattern) - 1
    good_suffix_table = good_suffix_array(pattern)
    bad_char_table = bad_character_table(pattern)
    result = []

    if len(pattern) > 1:    #matched prefix is only run if length of pattern > 1
        mp_shifts = matched_prefix(pattern)

    previous_position = -1  # alignment in previous phase (used for Galil's optimisation)

    while shift_pointer < len(string):
        
        p_pointer = len(pattern) - 1
        s_pointer = shift_pointer
        matches = 0

        while p_pointer >= 0 and s_pointer > previous_position and \
             pattern[p_pointer] == string[s_pointer]:
             p_pointer -= 1
             s_pointer -= 1
             matches += 1
        
        if p_pointer == -1 or s_pointer == previous_position: # complete match found
            result.append(shift_pointer - len(pattern) + 1 + 1)
            shift_pointer += 1
        else:
            mismatch = string[s_pointer]
            gs_shifts = good_suffix(pattern, matches, p_pointer, good_suffix_table[0], good_suffix_table[1], # number of shifts from the modified good suffix
            bad_char_table, mismatch) 

            if gs_shifts != 0:
                if gs_shifts >= p_pointer + 1:
                    previous_position = shift_pointer # galil's optimisation for next iteration
                shift_pointer += gs_shifts

            else: # if good suffix wasn't found
                if len(pattern) > 1 and matches > 0 and mp_shifts != 0:
                    if mp_shifts >= p_pointer + 1:
                        previous_position = shift_pointer
                    shift_pointer += mp_shifts 

                else: #if matched prefix wasn't found
                    bc_shifts = bad_character_shift(bad_char_table, p_pointer, string[s_pointer], len(pattern)) 
                    if bc_shifts >= p_pointer + 1:
                        previous_position = shift_pointer
                    shift_pointer += bc_shifts
        
    return result


def read_file(pattern_file, string_file):
    with open(pattern_file) as p, open(string_file) as s:
        pattern, string = p.read(), s.read()
        return pattern, string

def return_file(pattern, string, output_file):
    with open(output_file, "w") as f:
        for position in Boyer_Moore(pattern, string):
            result = f'{position}\n'
            f.write(result)


if __name__ == "__main__":
    OUTPUT_PATH = 'output_modified_BoyerMoore.txt'

    _, string_file, pattern_file = sys.argv[0], sys.argv[1], sys.argv[2]

    pattern, string = read_file(pattern_file, string_file)

    return_file(pattern, string, OUTPUT_PATH)