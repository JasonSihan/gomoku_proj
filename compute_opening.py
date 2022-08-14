import pattern

# Defining constants
# Winning conditions
FIVE = 1000
FOUR = 200
CROSS_THREE = 100
# Hooks
JUMP_FIVE = 50  # XX XX
JUMP_FOUR = 20  # XX X
BLOCKED_FOUR = 20  # OXXXX
THREE = 20
# Minors
JUMP_THREE = 18  # X X
TWO = 18
BLOCKED_THREE = 8   # OXXX
JUMP_BLOCKED_TWO = 5  # O XX
JUMP_BLOCKED_THREE = 3  # O XXX
# LOCKED = 0  # X OOOX or X OO X or XOO X
ONE = 5

SEARCH_DEPTH = 5

# Computes score if a certain piece is drawn
# $current is a 15x15 matrix with 0, 1, 2 representing none, friendly piece and enemy piece
def compute_score_core(current, x, y):
    # init
    final_score = 0
    current[x][y] = 1
    # Check if it is a single piece
    x_start = min(x - 1, 0)
    x_end = max(x + 1, 14)
    y_start = min(y - 1, 0)
    y_end = max(y + 1, 14)
    is_single = True
    first_ring = []
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            block = current[x][y]
            if block != 0:
                is_single = False
                first_ring.append(([block, i, j]))
    if is_single:
        final_score += ONE
        # Manually compute the first ring (5x5)
        # If it's border a placeholder [-1] is inserted
        if y - 2 < 0:
            for i in range(1, 6):
                first_ring.append([-1])
        else:
            for i in range(-2, 3):
                if x + i < 0 or x + i > 14:
                    first_ring.append([-1])
                else:
                    first_ring.append([current[x + i][y - 2], x + i, y - 2])
        for i in range(-1, 2):
            if x - 2 < 0:
                first_ring.append([-1])
            else:
                first_ring.append([current[x - 2][y + i], x - 2, y + i])
            if x + 2 > 14:
                first_ring.append([-1])
            else:
                first_ring.append([current[x + 2][y + i], x + 2, y + i])
        if y + 2 > 14:
            for i in range(1, 6):
                first_ring.append([-1])
        else:
            for i in range(-2, 3):
                if x + i < 0 or x + i > 14:
                    first_ring.append([-1])
                else:
                    first_ring.append([current[x + i][y + 2], x + i, y + 2])

        # If it is a single, we would check if it blocks a potential enemy line
        # or if makes a jump three, four or five
        # First check for jumps:
        friend_in_first_ring = []
        enemy_in_first_ring = []
        for i in range(len(first_ring)):
            stat = first_ring[i]
            if stat[0] == 1:
                # The original identifier would be used tell the algorithm which direction to check
                stat[0] = i
                friend_in_first_ring.append(stat)
            else:
                # If it's not a friendly piece it must be an enemy
                stat[0] = i
                enemy_in_first_ring.append(stat)
            # We give score if it makes a jump_three or jump_four, with itself being the jump
            for f_potential in friend_in_first_ring:
                # use if-else s cause I'm lazy
                piece_patterns = []
                place = f_potential[0]
                if place == -1:
                    pass
                elif place == 0:
                    for i in range(1, 5):
                        # Border detection
                        if f_potential[1] - i < 0 or f_potential[1] - i < 0:
                            break
                        piece_patterns.append(current[f_potential[1] - i][f_potential[2] - i])
                elif place <= 3:
                    for i in range(1, 5):
                        if f_potential[2] - i < 0:
                            break
                        piece_patterns.append(current[f_potential[1]][f_potential[2] - i])
                elif place == 4:
                    for i in range(1, 5):
                        if f_potential[1] + i > 14 or f_potential[2] + i > 14:
                            break
                        piece_patterns.append(current[f_potential[1] + i][f_potential[2] + i])
                elif place == 5 or place == 7 or place == 9:
                    for i in range(1, 5):
                        if f_potential[1] - i < 0:
                            break
                        piece_patterns.append(current[f_potential[1] - i][f_potential[2]])
                elif place == 6 or place == 8 or place == 10:
                    for i in range(1, 5):
                        if f_potential[1] + i < 0:
                            break
                        piece_patterns.append(current[f_potential[1] + i][f_potential[2]])
                elif place == 11:
                    for i in range(1, 5):
                        if f_potential[1] - i > 0 or f_potential[2] - i > 0:
                            break
                        piece_patterns.append(current[f_potential[1] - i][f_potential[2] - i])
                elif place <= 14:
                    for i in range(1, 5):
                        if f_potential[2] + i > 14:
                            break
                        piece_patterns.append(current[f_potential[1]][f_potential[2] + i])
                elif place == 15:
                    for i in range(1, 5):
                        # Border detection
                        if f_potential[1] + i < 14 or f_potential[1] + i < 14:
                            break
                        piece_patterns.append(current[f_potential[1] + i][f_potential[2] + i])
                else:
                    final_score += pattern.resolve_pattern_jump(piece_patterns)
                    # Checking if it blocks a three or a two
                    for e_potential in enemy_in_first_ring:
                        # use if-else s cause I'm lazy
                        piece_patterns = []
                        place = e_potential[0]
                        if place == -1:
                            pass
                        elif place == 0:
                            for i in range(1, 5):
                                # Border detection
                                if e_potential[1] - i < 0 or e_potential[1] - i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1] - i][e_potential[2] - i])
                        elif place <= 3:
                            for i in range(1, 5):
                                if e_potential[2] - i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1]][e_potential[2] - i])
                        elif place == 4:
                            for i in range(1, 5):
                                if e_potential[1] + i > 14 or e_potential[2] + i > 14:
                                    break
                                piece_patterns.append(current[e_potential[1] + i][e_potential[2] + i])
                        elif place == 5 or place == 7 or place == 9:
                            for i in range(1, 5):
                                if e_potential[1] - i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1] - i][e_potential[2]])
                        elif place == 6 or place == 8 or place == 10:
                            for i in range(1, 5):
                                if e_potential[1] + i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1] + i][e_potential[2]])
                        elif place == 11:
                            for i in range(1, 5):
                                if e_potential[1] - i > 0 or e_potential[2] - i > 0:
                                    break
                                piece_patterns.append(current[e_potential[1] - i][e_potential[2] - i])
                        elif place <= 14:
                            for i in range(1, 5):
                                if e_potential[2] + i > 14:
                                    break
                                piece_patterns.append(current[e_potential[1]][e_potential[2] + i])
                        elif place == 15:
                            for i in range(1, 5):
                                # Border detection
                                if e_potential[1] + i < 14 or e_potential[1] + i < 14:
                                    break
                                piece_patterns.append(current[e_potential[1] + i][e_potential[2] + i])
                        else:
                            final_score += pattern.resolve_pattern_jump_rev(piece_patterns)
    else:
        # Case if the piece is not a single
        # Checks LT-RB U-D RT-LB L-R
        lt_rb = []
        u_d = []
        rt_lb = []
        l_r = []
        for i in range(-4, 5):
            if 0 <= y + i <= 14:
                l_r.append(current[x][y + i])
            else:
                l_r.append(-1)
            if 0 <= x + i <= 14:
                u_d.append(current[x + i][y])
            else:
                u_d.append(-1)
            if 0 <= y + i <= 14 and 0 <= x + i <= 14:
                rt_lb.append(current[x + i][y + i])
            else:
                rt_lb.append(-1)
            if 0 <= y + i <= 14 and 0 <= x - i <= 14:
                lt_rb.append(current[x - i][y + i])
            else:
                lt_rb.append(-1)
        final_score+=pattern.resolve_pattern_cont(lt_rb)
        lt_rb[4] = 2
        final_score+=pattern.resolve_pattern_cont_rev(lt_rb)
        final_score+=pattern.resolve_pattern_cont(u_d)
        u_d[4] = 2
        final_score+=pattern.resolve_pattern_cont_rev(u_d)
        final_score += pattern.resolve_pattern_cont(rt_lb)
        rt_lb[4] = 2
        final_score+= pattern.resolve_pattern_cont_rev(rt_lb)
        final_score += pattern.resolve_pattern_cont(l_r)
        l_r[4] = 2
        final_score += pattern.resolve_pattern_cont_rev(l_r)
    current[x][y] = 0
    return final_score

# Same concept but compute score for enemy moves
def compute_score_rev_core(current, x, y):
    final_score = 0
    current[x][y] = 2
    # Check if it is a single piece
    x_start = min(x - 1, 0)
    x_end = max(x + 1, 14)
    y_start = min(y - 1, 0)
    y_end = max(y + 1, 14)
    is_single = True
    first_ring = []
    for i in range(x_start, x_end):
        for j in range(y_start, y_end):
            block = current[x][y]
            if block != 0:
                is_single = False
                first_ring.append(([block, i, j]))
    if is_single:
        final_score += ONE
        # Manually compute the first ring (5x5)
        # If it's border a placeholder [-1] is inserted
        if y - 2 < 0:
            for i in range(1, 6):
                first_ring.append([-1])
        else:
            for i in range(-2, 3):
                if x + i < 0 or x + i > 14:
                    first_ring.append([-1])
                else:
                    first_ring.append([current[x + i][y - 2], x + i, y - 2])
        for i in range(-1, 2):
            if x - 2 < 0:
                first_ring.append([-1])
            else:
                first_ring.append([current[x - 2][y + i], x - 2, y + i])
            if x + 2 > 14:
                first_ring.append([-1])
            else:
                first_ring.append([current[x + 2][y + i], x + 2, y + i])
        if y + 2 > 14:
            for i in range(1, 6):
                first_ring.append([-1])
        else:
            for i in range(-2, 3):
                if x + i < 0 or x + i > 14:
                    first_ring.append([-1])
                else:
                    first_ring.append([current[x + i][y + 2], x + i, y + 2])

        # If it is a single, we would check if it blocks a potential enemy line
        # or if makes a jump three, four or five
        # First check for jumps:
        friend_in_first_ring = []
        enemy_in_first_ring = []
        for i in range(len(first_ring)):
            stat = first_ring[i]
            if stat[0] == 2:
                # The original identifier would be used tell the algorithm which direction to check
                stat[0] = i
                friend_in_first_ring.append(stat)
            else:
                # If it's not a friendly piece it must be an enemy
                stat[0] = i
                enemy_in_first_ring.append(stat)
            # We give score if it makes a jump_three or jump_four, with itself being the jump
            for f_potential in friend_in_first_ring:
                # use if-else s cause I'm lazy
                piece_patterns = []
                place = f_potential[0]
                if place == -1:
                    pass
                elif place == 0:
                    for i in range(1, 5):
                        # Border detection
                        if f_potential[1] - i < 0 or f_potential[1] - i < 0:
                            break
                        piece_patterns.append(current[f_potential[1] - i][f_potential[2] - i])
                elif place <= 3:
                    for i in range(1, 5):
                        if f_potential[2] - i < 0:
                            break
                        piece_patterns.append(current[f_potential[1]][f_potential[2] - i])
                elif place == 4:
                    for i in range(1, 5):
                        if f_potential[1] + i > 14 or f_potential[2] + i > 14:
                            break
                        piece_patterns.append(current[f_potential[1] + i][f_potential[2] + i])
                elif place == 5 or place == 7 or place == 9:
                    for i in range(1, 5):
                        if f_potential[1] - i < 0:
                            break
                        piece_patterns.append(current[f_potential[1] - i][f_potential[2]])
                elif place == 6 or place == 8 or place == 10:
                    for i in range(1, 5):
                        if f_potential[1] + i < 0:
                            break
                        piece_patterns.append(current[f_potential[1] + i][f_potential[2]])
                elif place == 11:
                    for i in range(1, 5):
                        if f_potential[1] - i > 0 or f_potential[2] - i > 0:
                            break
                        piece_patterns.append(current[f_potential[1] - i][f_potential[2] - i])
                elif place <= 14:
                    for i in range(1, 5):
                        if f_potential[2] + i > 14:
                            break
                        piece_patterns.append(current[f_potential[1]][f_potential[2] + i])
                elif place == 15:
                    for i in range(1, 5):
                        # Border detection
                        if f_potential[1] + i < 14 or f_potential[1] + i < 14:
                            break
                        piece_patterns.append(current[f_potential[1] + i][f_potential[2] + i])
                else:
                    final_score += pattern.resolve_pattern_jump_rev(piece_patterns)
                    # Checking if it blocks a three or a two
                    for e_potential in enemy_in_first_ring:
                        # use if-else s cause I'm lazy
                        piece_patterns = []
                        place = e_potential[0]
                        if place == -1:
                            pass
                        elif place == 0:
                            for i in range(1, 5):
                                # Border detection
                                if e_potential[1] - i < 0 or e_potential[1] - i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1] - i][e_potential[2] - i])
                        elif place <= 3:
                            for i in range(1, 5):
                                if e_potential[2] - i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1]][e_potential[2] - i])
                        elif place == 4:
                            for i in range(1, 5):
                                if e_potential[1] + i > 14 or e_potential[2] + i > 14:
                                    break
                                piece_patterns.append(current[e_potential[1] + i][e_potential[2] + i])
                        elif place == 5 or place == 7 or place == 9:
                            for i in range(1, 5):
                                if e_potential[1] - i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1] - i][e_potential[2]])
                        elif place == 6 or place == 8 or place == 10:
                            for i in range(1, 5):
                                if e_potential[1] + i < 0:
                                    break
                                piece_patterns.append(current[e_potential[1] + i][e_potential[2]])
                        elif place == 11:
                            for i in range(1, 5):
                                if e_potential[1] - i > 0 or e_potential[2] - i > 0:
                                    break
                                piece_patterns.append(current[e_potential[1] - i][e_potential[2] - i])
                        elif place <= 14:
                            for i in range(1, 5):
                                if e_potential[2] + i > 14:
                                    break
                                piece_patterns.append(current[e_potential[1]][e_potential[2] + i])
                        elif place == 15:
                            for i in range(1, 5):
                                # Border detection
                                if e_potential[1] + i < 14 or e_potential[1] + i < 14:
                                    break
                                piece_patterns.append(current[e_potential[1] + i][e_potential[2] + i])
                        else:
                            final_score += pattern.resolve_pattern_jump_rev(piece_patterns)
    else:
        # Case if the piece is not a single
        # Checks LT-RB U-D RT-LB L-R
        lt_rb = []
        u_d = []
        rt_lb = []
        l_r = []
        for i in range(-4, 5):
            if 0 <= y + i <= 14:
                l_r.append(current[x][y + i])
            else:
                l_r.append(-1)
            if 0 <= x + i <= 14:
                u_d.append(current[x + i][y])
            else:
                u_d.append(-1)
            if 0 <= y + i <= 14 and 0 <= x + i <= 14:
                rt_lb.append(current[x + i][y + i])
            else:
                rt_lb.append(-1)
            if 0 <= y + i <= 14 and 0 <= x - i <= 14:
                lt_rb.append(current[x - i][y + i])
            else:
                lt_rb.append(-1)
        final_score+=pattern.resolve_pattern_cont_rev(lt_rb)
        lt_rb[4] = 1
        final_score+=pattern.resolve_pattern_cont(lt_rb)
        final_score+=pattern.resolve_pattern_cont_rev(u_d)
        u_d[4] = 1
        final_score+=pattern.resolve_pattern_cont(u_d)
        final_score += pattern.resolve_pattern_cont_rev(rt_lb)
        rt_lb[4] = 1
        final_score+= pattern.resolve_pattern_cont(rt_lb)
        final_score += pattern.resolve_pattern_cont_rev(l_r)
        l_r[4] = 1
        final_score += pattern.resolve_pattern_cont(l_r)
    current[x][y] = 0
    return final_score    

# wrapper for compute score
def compute_score(current, x, y, cache):
    cache.append([compute_score_core(current, x, y),x,y])
    #print("e")

def compute_score_rev(current, x, y, cache):
    cache.append([compute_score_rev_core(current, x, y),x,y])   
    #print("e")
