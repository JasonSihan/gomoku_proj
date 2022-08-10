from threading import Thread
import compute

# I think depth can only be odd
# If it's the last search, it would return an array [score, x, y]
# Else, it would trace recursively to find the best move and return [score, x , y]
# Parent score is used to prune nodes
def search(depth, current):
    tree = []
    for i in range(0,15):
        for j in range(0,15):
            if current[i][j] != 0:
                pass
            is_upper_bound = j == 0
            is_lower_bound = j == 14
            is_left_bound = i == 0
            is_right_bound = i == 14
            # Check if there's a non empty neighbor and compute score if so
            if current[i][j] != 0 and not is_upper_bound:
                if current[i][j-1] != 0:    
                    # multi threading
                    thread = Thread(target=compute.compute_score,args=(current.copy(),i,j,tree))
                    thread.start()
                    thread.join()
                    pass
                if not is_left_bound:
                    if current[i-1][j-1] != 0 or current[i-1][j] != 0: 
                        thread = Thread(target=compute.compute_score,args=(current.copy(),i,j,tree))
                        thread.start()
                        thread.join()
                        pass
                if not is_right_bound:
                    if current[i+1][j-1] or current[i+1][j] != 0: 
                        thread = Thread(target=compute.compute_score,args=(current.copy(),i,j,tree))
                        thread.start()
                        thread.join()    
            if current[i][j] != 0 and not is_lower_bound:
                if current[i][j+1] != 0:
                    thread = Thread(target=compute.compute_score,args=(current.copy(),i,j,tree))
                    thread.start()
                    thread.join()
                if not is_left_bound and current[i-1][j+1]:
                    thread = Thread(target=compute.compute_score,args=(current.copy(),i,j,tree))
                    thread.start()
                    thread.join()
                if not is_right_bound and current[i+1][j+1]:
                    thread = Thread(target=compute.compute_score,args=(current.copy(),i,j,tree))
                    thread.start()
                    thread.join()     
    if depth == 1:
        # if this is the last search, we find the move with the largest score and return a tuple
        max = tree[0]
        for item in tree:
            if item[0] > max[0]:
                max = item
        return max        
    else:
        # if not we would find the best enemy move and best counter move
        # combining these and adding up the total score to get the move with the highest score
        score_board = []
        for item in tree:
            context = commit_move(item[1], item[2], current)
            enemy_tree = []
            print("enemy_tree created")
            print(str(context))
            for i in range(0,15):
                for j in range(0,15):
                    if current[i][j] != 0:
                        pass
                    is_upper_bound = j == 0
                    is_lower_bound = j == 14
                    is_left_bound = i == 0
                    is_right_bound = i == 14
                    # Check if there's a non empty neighbor and compute score if so
                    if current[i][j] != 0 and not is_upper_bound:
                        if current[i][j-1] != 0:    
                            thread = Thread(target=compute.compute_score_rev,args=(context.copy(),i,j,enemy_tree))
                            thread.start()
                            thread.join()
                            pass
                        if not is_left_bound:
                            if current[i-1][j-1] != 0 or current[i-1][j] != 0: 
                                thread = Thread(target=compute.compute_score_rev,args=(context.copy(),i,j,enemy_tree))
                                thread.start()
                                thread.join()
                                pass
                        if not is_right_bound:
                            if current[i+1][j-1] or current[i+1][j] != 0: 
                                thread = Thread(target=compute.compute_score_rev,args=(context.copy(),i,j,enemy_tree))
                                thread.start()
                                thread.join()    
                    if current[i][j] != 0 and not is_lower_bound:
                        if current[i][j+1] != 0:
                            thread = Thread(target=compute.compute_score_rev,args=(context.copy(),i,j,enemy_tree))
                            thread.start()
                            thread.join()
                        if not is_left_bound and current[i-1][j+1]:
                            thread = Thread(target=compute.compute_score_rev,args=(context.copy(),i,j,enemy_tree))
                            thread.start()
                            thread.join()
                        if not is_right_bound and current[i+1][j+1]:
                            thread = Thread(target=compute.compute_score_rev,args=(context.copy(),i,j,enemy_tree))
                            thread.start()
                            thread.join()
                        if not is_left_bound and current[i-1][j+1]:
                            thread = Thread(target=compute.compute_score_rev,args=(context,i,j,enemy_tree))
                            thread.start()
                            thread.join()
                        if not is_right_bound and current[i+1][j+1]:
                            thread = Thread(target=compute.compute_score_rev,args=(context,i,j,enemy_tree))
                            thread.start()
                            thread.join() 
                # find the best enemy move
                #print(str(context))
                #print(str(enemy_tree))
                max = enemy_tree[0]
                for item in enemy_tree:
                    if item[0] > max[0]:
                        max = item   
                new_depth = depth - 2
                context = commit_move_rev(max[1], max[2], context)
                # search recursively
                next_best_move = search(new_depth, context)
                # find the overall best move
                score_board.append([item[0]-max[0]+next_best_move[0],item[1],item[2]]) 
        max = score_board[0]
        #  find the overall best move
        for item in score_board:
            if item[0] > max[0]:
                max = item  
        return max
             
def commit_move(x, y, current):
    if current[x][y] != 0:
        print("overwrite occured")
        exit(-1)
    current[x][y] = 1
    return current       

def commit_move_rev(x, y, current):
    if current[x][y] != 0:
        print("overwrite occured")
        exit(-1)

    current[x][y] = 2
    return current       
