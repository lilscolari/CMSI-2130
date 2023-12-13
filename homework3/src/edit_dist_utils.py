'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''


def get_edit_dist_table(row_str: str, col_str: str) -> list[list[int]]:
    '''
    Returns the completed Edit Distance memoization structure: a 2D list
    of ints representing the number of string manupulations required to
    minimally turn each subproblem's string into the other.

    Parameters:
        row_str (str):
            The string located along the table's rows
        col_str (col):
            The string located along the table's columns

    Returns:
        list[list[int]]:
            Completed memoization table for the computation of the
            edit_distance(row_str, col_str)
    '''

    table: list[list[int]] = []

    row_str = " " + row_str
    col_str = " " + col_str

    for r_num, r_str in enumerate(row_str):
        row: list[int] = []
        for c_num, c_str in enumerate(col_str):
            insertion: float = float("inf")
            deletion: float = float("inf")
            replacement: float = float("inf")
            transposition: float = float("inf")
            if r_num == 0:
                for num, string in enumerate(col_str):
                    row.append(num)
                break
            if c_num == 0:
                row.append(r_num)
                continue
            if c_num >= 1:
                insertion = row[c_num - 1] + 1
            if r_num >= 1:
                deletion = table[r_num - 1][c_num] + 1
            if c_num >= 1 and r_num >= 1:
                if r_str == c_str:
                    replacement = table[r_num - 1][c_num - 1]
                else:
                    replacement = table[r_num - 1][c_num - 1] + 1
            if r_num >= 2 and c_num >= 2:
                if r_str == col_str[c_num - 1: c_num] and c_str == row_str[r_num - 1: r_num]:
                    transposition = table[r_num - 2][c_num - 2] + 1
            best_transformation: float = min(insertion, deletion, replacement, transposition)

            row.append(int(best_transformation))
        table.append(row)

    return table


def edit_distance(s0: str, s1: str) -> int:
    '''
    Returns the edit distance between two given strings, defined as an
    int that counts the number of primitive string manipulations (i.e.,
    Insertions, Deletions, Replacements, and Transpositions) minimally
    required to turn one string into the other.
    
    [!] Given as part of the skeleton, no need to modify
    
    Parameters:
        s0, s1 (str):
            The strings to compute the edit distance between
    
    Returns:
        int:
            The minimal number of string manipulations
    '''
    if s0 == s1: return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]


def get_transformation_list(s0: str, s1: str) -> list[str]:
    '''
    Returns one possible sequence of transformations that turns String s0
    into s1. The list is in top-down order (i.e., starting from the largest
    subproblem in the memoization structure) and consists of Strings representing
    the String manipulations of:
        1. "R" = Replacement
        2. "T" = Transposition
        3. "I" = Insertion
        4. "D" = Deletion
    In case of multiple minimal edit distance sequences, returns a list with
    ties in manipulations broken by the order listed above (i.e., replacements
    preferred over transpositions, which in turn are preferred over insertions, etc.)
    
    [!] Given as part of the skeleton, no need to modify
    
    Example:
        s0 = "hack"
        s1 = "fkc"
        get_transformation_list(s0, s1) => ["T", "R", "D"]
        get_transformation_list(s1, s0) => ["T", "R", "I"]
    
    Parameters:
        s0, s1 (str):
            Start and destination strings for the transformation
    
    Returns:
        list[str]:
            The sequence of top-down manipulations required to turn s0 into s1
    '''

    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))


def get_transformation_list_with_table(s0: str, s1: str, table: list[list[int]]) -> list[str]:
    '''
    See get_transformation_list documentation.
    
    This method does exactly the same thing as get_transformation_list, except that
    the memoization table is input as a parameter. This version of the method can be
    used to save computational efficiency if the memoization table was pre-computed
    and is being used by multiple methods.
    
    [!] MUST use the already-solved memoization table and must NOT recompute it.
    [!] MUST be implemented recursively (i.e., in top-down fashion)

    1. "R" = Replacement
    2. "T" = Transposition
    3. "I" = Insertion
    4. "D" = Deletion
    '''

    transformation_list: list[str] = []

    return recursion(s0, s1, table, transformation_list)[3]

#>>[NO] I'd recommend a better name than recursion for this method, something that is somewhat descriptive of the functionality
def recursion(string0: str, string1: str, table: list[list[int]], transformation_list: list[str]) -> tuple[
    str, str, list[list[int]], list[str]]:
    '''
    Recursive function associated with get_transformation_list_with_table. Implements retrieving the transformations
    with top-down structure.
    Parameters:
        string0 (str):
            The string located along the table's rows
        string1 (str):
            The string located along the table's columns
        table (list[list[int]])
            The memoization table that has already been computed.
        transformation_list (list[str])
            The transformation list after recursing through the memoization table top-down. The transformations
            necessary to transform string0 to string1.

    Returns:
        list[tuple[str, str, list[list[int]], list[str]]:
            Completed memoization table for the computation of the
            edit_distance(row_str, col_str)
    '''

    if table[len(string0)][len(string1)] == 0:
        return string0, string1, table, transformation_list

    insertion: float = float("inf")
    deletion: float = float("inf")
    replacement: float = float("inf")
    transposition: float = float("inf")

    if len(string0) >= 1:
        deletion = table[len(string0) - 1][len(string1)] + 1
    if len(string1) >= 1:
        insertion = table[len(string0)][len(string1) - 1] + 1
    if len(string0) >= 1 and len(string1) >= 1:
        if string0[-1] == string1[-1]:
            replacement = table[len(string0) - 1][len(string1) - 1]
        else:
            replacement = table[len(string0) - 1][len(string1) - 1] + 1
    if len(string0) >= 2 and len(string1) >= 2:
        if string0[-1] == string1[-2:-1] and string1[-1] == string0[-2:-1]:
            transposition = table[len(string0) - 2][len(string1) - 2] + 1

    minimum: float = min(deletion, insertion, replacement, transposition)

    if minimum == replacement:
        if string0[-1] != string1[-1]:
            transformation_list.append("R")
        string0 = string0[:-1]
        string1 = string1[:-1]
        table.pop()
        for row in table:
            row.pop()
    elif minimum == transposition:
        string0 = string0[:-2]
        string1 = string1[:-2]
        table.pop()
        table.pop()
        for row in table:
            row.pop()
            row.pop()
        transformation_list.append("T")
    elif minimum == insertion:
        string1 = string1[:-1]
        for row in table:
            row.pop()
        transformation_list.append("I")
    else:
        string0 = string0[:-1]
        table.pop()
        transformation_list.append("D")

    return recursion(string0, string1, table, transformation_list)

# ===================================================
# >>> [NO] Summary
# Excellent submission that has a ton to like and was
# obviously well-tested. Generally clean style, and shows
# strong command of programming foundations alongside
# data structure and algorithmic concepts. Keep up
# the great work!
# ---------------------------------------------------
# >>> [NO] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [X] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [X] Proper JavaDocs provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:           96 / 100
# -> EditDistUtils:      20 / 20  (-2 / missed test)
# -> DistlePlayer:      267 / 265 (-1 / below threshold; max -30)
# Style Penalty:         -0
# Total:                 96 / 100
# ===================================================
