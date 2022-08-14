import compute


def resolve_pattern_jump(pattern):
    # Check if there's a jump_three, four or five
    if pattern[0] == 1 and pattern[1] == 1:
        return compute.JUMP_FIVE
    elif pattern[0] == 1:
        return compute.JUMP_FOUR
    else:
        return compute.JUMP_THREE


def resolve_pattern_jump_rev(pattern):
    # Check if there's a jump_three, four or five
    if pattern[0] == 2 and pattern[1] == 2:
        return compute.JUMP_BLOCKED_THREE
    elif pattern[0] == 2:
        return compute.JUMP_BLOCKED_TWO
    else:
        return 0


# Winning conditions
FIVE = [1, 1, 1, 1, 1]  # len 5
FOUR = [0, 1, 1, 1, 1, 0]  # len 6
# Hooks
JUMP_FIVE_D1 = [1, 1, 1, 0, 1]  # len 5
JUMP_FIVE_D2 = [1, 0, 1, 1, 1]
JUMP_FIVE_D3 = [1, 1, 0, 1, 1]
JUMP_FOUR_D1 = [0, 1, 1, 0, 1, 0]  # len 6
JUMP_FOUR_D2 = [0, 1, 0, 1, 1, 0]
BLOCKED_FOUR_D1 = [2, 1, 1, 1, 1, 0]  # len 6
BLOCKED_FOUR_D2 = [0, 1, 1, 1, 1, 2]
THREE = [0, 1, 1, 1, 0]  # len 5
# Minors
JUMP_THREE_D1 = [0, 1, 1, 0, 1, 0]  # len 6
JUMP_THREE_D2 = [0, 1, 0, 1, 1, 0]
TWO = [0, 1, 1, 0]  # len four
BLOCKED_THREE_D1 = [2, 1, 1, 1, 0]  # len 5
BLOCKED_THREE_D2 = [0, 1, 1, 1, 2]
JUMP_BLOCKED_TWO_D1 = [2, 0, 1, 1, 0]  # len 5
JUMP_BLOCKED_TWO_D2 = [0, 1, 1, 0, 2]
JUMP_BLOCKED_THREE_D1 = [2, 0, 1, 1, 1, 0]  # len 6
JUMP_BLOCKED_THREE_D2 = [0, 1, 1, 1, 0, 2]  # len 6

      
# Winning conditions
FIVE_REV = [2, 2, 2, 2, 2]  # len 5
FOUR_REV = [0, 2, 2, 2, 2, 0]  # len 6
# Hooks
JUMP_FIVE_D1_REV = [2, 2, 2, 0, 2]  # len 5
JUMP_FIVE_D2_REV = [2, 0, 2, 2, 2]
JUMP_FIVE_D3_REV = [2, 2, 0, 2, 2]
JUMP_FOUR_D1_REV = [0, 2, 2, 0, 2, 0]  # len 6
JUMP_FOUR_D2_REV = [0, 2, 0, 2, 2, 0]
BLOCKED_FOUR_D1_REV = [2, 2, 2, 2, 2, 0]  # len 6
BLOCKED_FOUR_D2_REV = [0, 2, 2, 2, 2, 2]
THREE_REV = [0, 2, 2, 2, 0]  # len 5
# Minors
JUMP_THREE_D1_REV = [0, 2, 2, 0, 2, 0]  # len 6
JUMP_THREE_D2_REV = [0, 2, 0, 2, 2, 0]
TWO_REV = [0, 2, 2, 0]  # len four
BLOCKED_THREE_D1_REV = [2, 2, 2, 2, 0]  # len 5
BLOCKED_THREE_D2_REV = [0, 2, 2, 2, 2]
JUMP_BLOCKED_TWO_D1_REV = [2, 0, 2, 2, 0]  # len 5
JUMP_BLOCKED_TWO_D2_REV = [0, 2, 2, 0, 2]
JUMP_BLOCKED_THREE_D1_REV = [2, 0, 2, 2, 2, 0]  # len 6
JUMP_BLOCKED_THREE_D2_REV = [0, 2, 2, 2, 0, 2]  # len 6


# Conflicts
# JUMP_FIVE_D1, 2  -> THREE
# JUMP_FOUR_D1, 2  -> TWO
# JUMP_THREE_D1, 2 -> TWO
# JUMP_BLOCKED_THREE_D1,2 -> THREE
# JUMP_BLOCKED_TWO_D1, 2 -> TWO
# Get pattern in a square and see if there are patterns that we would want
def resolve_pattern_cont(pattern):
    final_score = 0
    jumps = [0, 0, 0, 0, 0]
    # match len 6
    for i in range(0, 4):
        match = pattern[i:i + 6]
        # The reason for the ifs is to exclude -1
        if match[0] == 0:
            # Check for FOUR JUMP_FOUR BLOCKED_FOUR_D2 JUMP_THREE JUMP_BLOCKED_THREE_D2
            if match == FOUR:
                final_score += compute.FOUR
            elif match == JUMP_FOUR_D1 or match == JUMP_FOUR_D2:
                final_score += compute.JUMP_FOUR
                jumps[1] += 1
            elif match == BLOCKED_FOUR_D2:
                final_score += compute.BLOCKED_FOUR
            elif match == JUMP_THREE_D1 or match == JUMP_THREE_D2:
                final_score += compute.JUMP_THREE
                jumps[2] += 1
            elif match == JUMP_BLOCKED_THREE_D2:
                final_score += compute.JUMP_BLOCKED_THREE
                jumps[3] += 1
        elif match[0] == 2:
            # Check for BLOCKED_FOUR_D1 BLOCKED_THREE_D2
            if match == BLOCKED_FOUR_D1:
                final_score += compute.BLOCKED_FOUR
            elif match == BLOCKED_THREE_D2:
                final_score += compute.BLOCKED_THREE
    # match len 5
    for i in range(0, 5):
        match = pattern[i:i + 5]
        if match[0] == 1:
            if match == FIVE:
                return compute.FIVE
            elif match == JUMP_FIVE_D1 or match == JUMP_FIVE_D2 or match == JUMP_FIVE_D3:
                final_score += compute.JUMP_FIVE
                jumps[0] += 1
            elif match == THREE:
                final_score += compute.THREE
        elif match[0] == 2:
            if match == BLOCKED_THREE_D1:
                final_score += compute.BLOCKED_THREE
            elif match == JUMP_BLOCKED_TWO_D1:
                final_score += compute.JUMP_BLOCKED_TWO
                jumps[4] += 1
        elif match[0] == 0:
            if match == BLOCKED_THREE_D2:
                final_score += compute.BLOCKED_THREE
            elif match == JUMP_BLOCKED_TWO_D2:
                final_score += compute.JUMP_BLOCKED_TWO
                jumps[4] += 1
    # Subtracting the score counted twice
    for i in range(0,jumps[0]+jumps[3]):
        final_score-=compute.THREE
    for i in range(0,jumps[1]+jumps[2]+jumps[4]):
        final_score-=compute.TWO        
    return final_score            

# Same concept but for enemy move
def resolve_pattern_cont_rev(pattern):
    final_score = 0
    jumps = [0, 0, 0, 0, 0]
    # match len 6
    for i in range(0, 4):
        match = pattern[i:i + 6]
        # The reason for the ifs is to exclude -1
        if match[0] == 0:
            # Check for FOUR JUMP_FOUR BLOCKED_FOUR_D2 JUMP_THREE JUMP_BLOCKED_THREE_D2 (_REV)
            if match == FOUR_REV:
                final_score += compute.FOUR
            elif match == JUMP_FOUR_D1_REV or match == JUMP_FOUR_D2_REV:
                final_score += compute.JUMP_FOUR
                jumps[1] += 1
            elif match == BLOCKED_FOUR_D2_REV:
                final_score += compute.BLOCKED_FOUR
            elif match == JUMP_THREE_D1_REV or match == JUMP_THREE_D2_REV:
                final_score += compute.JUMP_THREE
                jumps[2] += 1
            elif match == JUMP_BLOCKED_THREE_D2_REV:
                final_score += compute.JUMP_BLOCKED_THREE
                jumps[3] += 1
        if match[0] == 2:
            # Check for BLOCKED_FOUR_D1_REV BLOCKED_THREE_D2_REV
            if match == BLOCKED_FOUR_D1_REV:
                final_score += compute.BLOCKED_FOUR
            elif match == BLOCKED_THREE_D2_REV:
                final_score += compute.BLOCKED_THREE
    for i in range(0, 5):
    # match len 5
        match = pattern[i:i + 5]
        if match[0] == 0:
            if match[0] == 1:
                return compute.FIVE
            elif match == JUMP_FIVE_D1_REV or match == JUMP_FIVE_D2_REV or match == JUMP_FIVE_D3_REV:
                final_score += compute.JUMP_FIVE
                jumps[0] += 1
            elif match == THREE_REV:
                final_score += compute.THREE
        elif match[0] == 2:
            if match == BLOCKED_THREE_D1_REV:
                final_score += compute.BLOCKED_THREE
            elif match == JUMP_BLOCKED_TWO_D1_REV:
                final_score += compute.JUMP_BLOCKED_TWO
                jumps[4] += 1
        elif match[0] == 0:
            if match == BLOCKED_THREE_D2_REV:
                final_score += compute.BLOCKED_THREE
            elif match == JUMP_BLOCKED_TWO_D2_REV:
                final_score += compute.JUMP_BLOCKED_TWO
                jumps[4] += 1
    # Subtracting the score counted twice
    for i in range(0,jumps[0]+jumps[3]):
        final_score-=compute.THREE
    for i in range(0,jumps[1]+jumps[2]+jumps[4]):
        final_score-=compute.TWO
    return final_score
