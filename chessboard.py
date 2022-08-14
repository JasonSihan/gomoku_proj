import tkinter as tk
from tkinter import *
import interpret
import search
import math
import opening

PIECE_SIZE = 10
piece_color = "black"
win_color = "black"
white_step_count = 0

'''Store the location that the pieces have been put, 15*15 matrix'''
# TODO: store_chess = [[0]*15]*15: initiation in this way will let store_chess[x][x] = 1 change x cols in all rows be 1
store_chess = [[0 for i in range(15)] for j in range(15)]
# store_chess = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

'''marker of winners: 1 as black wins, 2 as white wins, 0 as none of player wins'''
person_flag = 0

#root window as chess board
root_window = tk.Tk()
root_window.title("Gomoku Game by Kevin Ye & Sihan Chen")
root_window.geometry("995x660")
root_window.resizable(0,0)
root_window.iconbitmap('./GomokuIcon.ico') #Icon is from https://www.aigei.com/s?q=%E6%A3%8B&type=icon_7


#chess info
frames = tk.Canvas(root_window, width=220, height=70)
frames.grid(row = 0, column = 1)
frames.create_oval(110 - PIECE_SIZE, 25 - PIECE_SIZE, 110 + PIECE_SIZE, 25 + PIECE_SIZE, fill = piece_color, tags = ("show_pieces"))
var = tk.StringVar()
var.set("Your turn")
person_chess = tk.Label(root_window, textvariable = var, width = 20, anchor = tk.CENTER, font = ("Times New Roman", 15) )
person_chess.place(x = 650, y = 100)

'''Print the chess board'''
#background
board = tk.Canvas(root_window, bg = "#F5DEB3", width = 640, height = 640)
board.grid(row = 0, column = 0, rowspan = 6)
#line
for i in range(15):
    # Vertical Line
    board.create_line(32, (42 * i + 38), 622, (42 * i + 38))
    # Horizontal Line
    board.create_line((42 * i + 32), 38, (42 * i + 32), 628)
#Star points
point_x = [3, 3, 11, 11, 7]
point_y = [3, 11, 3, 11, 7]
for i in range(5):
    board.create_oval(42 * point_x[i] + 28, 42 * point_y[i] + 33, 42 * point_x[i] + 36, 42 * point_y[i] + 41, fill = "black")
# vertical coordinate in numbers
for i in range(15):
    label = tk.Label(board, text = str(i + 1), fg = "black", bg = "#F5DEB3", width = 2, anchor = tk.E)
    label.place(x = 2, y = 42 * i + 28)
# horizontal corrdinate in letters
count = 0
for i in range(65, 81):
    label = tk.Label(board, text = chr(i), fg = "black", bg = "#F5DEB3")
    label.place(x = 42 * count + 25, y = 2)
    count += 1

'''Set of intersection of lines'''
'''Each element is a 2-element array'''
intersection = []
for i in range(15):
    for j in range(15):
        intersection.append([(42 * i + 32),(42 * j + 38)])
#store intersects(x,y) in x first order: scan all intersects in one x then moves to x_1=x+42    
# print(intersection)
#Import search(AI Steps) and interpret(game position) (1 - our piece) (2 - enemy)

'''
Mouse Click Event
<Button-1>  Left
<Button-2>  Right
<Double-Button-1>   Double Left Click
<Double-Button-2>   Double Right Click
'''
click_x = 0
click_y = 0
'''Mouse click range'''
pieces_x = [i for i in range(32, 623, 42)]
pieces_y = [i for i in range(38, 629, 42)]

'''Return the coordinate of click'''
def click_cor(event):
    global click_x, click_y
    print(f"Left Click cooridinate:x= {event.x} y= {event.y}")
    click_x = event.x
    click_y = event.y
    ChessPos()

'''Bind the mouse click with chess board'''
board.bind("<Button-1>", click_cor)
#board.bind("<Double-Button-1>", click_cor)

'''Find the closest intersection of lines'''
def ChessPos():
    global click_x, click_y, person_flag, pieces_x, pieces_y, intersection, piece_color, store_chess, white_step_count
    # if white_step_count <= 5 and piece_color == "white":
    #     open = opening.opening_move(store_chess)
    #     print("", open)
    #     putPiece(piece_color, open[1]*42+32, open[2]*42+38)
    #     return
    if piece_color == "white":        
        check = search.search(1, store_chess)
        print("", check)
        putPiece(piece_color, check[1]*42 + 32, check[2]* 42 + 38)
        return
    
    min_dist = 255
    chess_x = -1
    chess_y = -1
    for i in range(len(intersection)):
        delta_x = math.pow((click_x - intersection[i][0]), 2)
        delta_y = math.pow((click_y - intersection[i][1]), 2)
        dist = math.sqrt(delta_x + delta_y)
        if dist < min_dist:
            min_dist = dist
            chess_x = intersection[i][0]
            chess_y = intersection[i][1]
    print(f"chess_x = {chess_x}, chess_y = {chess_y}")         
    putPiece(piece_color, chess_x, chess_y)


'''Draw piece after find the chess position'''
def putPiece(piece_color, chess_x, chess_y):
    global store_chess, person_flag, board, white_step_count
    cols_float = (chess_x - 32)/42
    rows_float = (chess_y - 38)/42
    # print(f"rows_float = {rows_float}, cols_float = {cols_float}")
    rows = math.ceil(rows_float)
    cols = math.ceil(cols_float)
    print(f"rows = {rows}, cols = {cols}")
    if store_chess[rows][cols] == 0:
        board.create_oval(chess_x - PIECE_SIZE, chess_y - PIECE_SIZE, chess_x + PIECE_SIZE, chess_y + PIECE_SIZE, fill = piece_color, tags = ("piece"))
        if piece_color == "white":
            store_chess[rows][cols] = 2
            ChangeTurn("black")
            white_step_count = white_step_count + 1
            # print("white")
        elif piece_color == "black":
            store_chess[rows][cols] = 1
            ChangeTurn("white")
            # print("black")
        print()
        for some in store_chess:
            print("",some)
        print()       
    #print(store_chess) #check correction of position
    #TODO Add the judge of game position: win to end/continues?
    # Check Game Position each turn
    result = interpret.is_at_win_state(store_chess)
    if result[0] == True:
        end_message.set("Game Ends")
        if result[1] == True:
            person_flag = 1
            win_message.set("You Win!")
        elif result[1] == False:
            person_flag = 2
            win_message.set("AI Wins!")
        board.unbind("<Button-1>", "")    


def ChangeTurn(color):
    global piece_color, var, person_chess, frames
    piece_color = color
    frames.delete("show_piece")
    frames.create_oval(110 - PIECE_SIZE, 25 - PIECE_SIZE, 110 + PIECE_SIZE, 25 + PIECE_SIZE, fill = piece_color, tags = ("show_piece"))
    if color == "black":
        var.set("Your turn")
    elif color == "white":
        var.set("AI's turn")
    person_chess.destroy()
    person_chess = tk.Label(root_window, textvariable = var, width = 20, anchor = tk.CENTER, font = ("Times New Roman", 15) )
    person_chess.place(x = 650, y = 100)

'''Define reset button'''
def gameReset():
    global store_chess, piece_color, person_flag, intersection, board,step_count
    var.set("Holding Black")      
    win_message.set("")
    end_message.set("")         
    ChangeTurn("black")             
    board.delete("piece")
    store_chess = [[0 for i in range(15)] for j in range(15)]
    piece_color = "black"
    person_flag = 0
    board.bind("<Button-1>", click_cor)
    step_count = 0

'''Label of Who is the winner'''
win_message = tk.StringVar()
win_message.set("")
result_label = tk.Label(root_window, textvariable = win_message, width = 12, height = 4, anchor = tk.CENTER, fg = "red", font = ("Arial", 25) )
result_label.grid(row = 2, column = 1, rowspan = 2)

'''Labal of Game Ends'''
end_message = tk.StringVar()
end_message.set("")
game_label = tk.Label(root_window, textvariable = end_message, width = 12, height = 4, anchor = tk.CENTER, font = ("Arial", 18) )
game_label.grid(row = 4, column = 1)

'''Restart Button'''
reset_button = tk.Button(root_window, text = "Restart", font = ("Arial", 20), width = 8, command = gameReset)
reset_button.grid(row = 5, column = 1)


root_window.mainloop()
