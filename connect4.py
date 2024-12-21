import pygame as p
import sys
import random as r
import copy
 
class Block(p.sprite.Sprite):
   def __init__(self, color):
      super().__init__()
      self.image = p.Surface([50,50])
      p.draw.circle(self.image,color,(25,25),25)
      self.rect = self.image.get_rect()
screen = p.display.set_mode((1000,600))
p.display.set_caption("Connect 4")
board=[]
clicked_comp=[]
clicked_user=[]
not_clicked=[]
valid_locations=[]
avail_col=[5]*7
sp=p.sprite.Group()
BOT_PIECE=1
PLAYER_PIECE=-1
ROW_COUNT=6
COLUMN_COUNT=7
n=-1
def create():
   l=[0,0,0,0,0,0,0]
   for i in range(6):
      board.append(l[:])
   for i in range(6):
      for j in range(7):
         not_clicked.append([310+j*55,200+i*55])
    
def create_board():
   white=(255,255,255)
   comp=(248, 200, 220)
   user = (176,224,230)
   button=p.Surface((50,50))
   p.draw.circle(button, comp, (25,25), 25)
   screen.blit(button,(150,10))
   font = p.font.SysFont('Candara', 30)
   comp_text = font.render('Computer: ', True,white)
   screen.blit(comp_text,(10,30))
   button=p.Surface((50,50))
   p.draw.circle(button, user, (25,25), 25)
   screen.blit(button,(150,70))
   user_text = font.render('User: ', True,white)
   screen.blit(user_text,(10,90))
   y=200
   for i in not_clicked:
      button=p.Surface((50,50))
      p.draw.circle(button, white, (25,25), 25)
      screen.blit(button,(i[0],i[1]))
      p.draw.rect(screen,(0,0,0),p.Rect((i[0],i[1]+50),(50,5)))
   p.display.update()
def user_clicked(x,y):
   user = (176,224,230)
   obj=Block(user)
   obj.rect.x=x
   obj.rect.y=200
   sp.add(obj)
   while obj.rect.y<=y:
      obj.rect.y+=1
      sp.update()
      sp.draw(screen)   
      p.display.update()
      create_board()
 
def computer_clicked(x,y):
   comp=(248, 200, 220)
   obj=Block(comp)
   obj.rect.x=x
   obj.rect.y=200
   sp.add(obj)
   while obj.rect.y<=y:
      obj.rect.y+=1
      sp.update()
      sp.draw(screen)
      p.display.update()
      create_board()

p.init()

def get_next_open_row(board, col):
   for ro in range(ROW_COUNT):
      if board[ro][col] == 0:
         return ro
def drop_piece(board, row, col, piece):
   if row is not None and col is not None:
      if row<6 and col<7:
         board[row][col] = piece
         return 1
      else:
         return -1
   else:
      return -1
      
 

def evaluate_window(window, piece):
   score = 0
   
   # Switch scoring based on turn
   opp_piece = PLAYER_PIECE
   if piece == PLAYER_PIECE:
      opp_piece = BOT_PIECE
   EMPTY=0
   # Prioritise a winning move
   # Minimax makes this less important
   if window.count(piece) == 4:
      score += 100
   # Make connecting 3 second priority
   elif window.count(piece) == 3 and window.count(EMPTY) == 1:
      score += 5
    # Make connecting 2 third priority
   elif window.count(piece) == 2 and window.count(EMPTY) == 2:
      score += 2
    # Prioritise blocking an opponent's winning move (but not over bot winning)
    # Minimax makes this less important
   if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
      score -=4
   
   return score
def score_position(board, piece):
   score = 0
   WINDOW_LENGTH=4
   # Score centre column

   #print(board[:,COLUMN_COUNT // 2])
   centre_array = [row[COLUMN_COUNT // 2] for row in board]
   centre_count = centre_array.count(piece)
   score += centre_count * 3

   # Score horizontal positions
   
   
   for ro in range(ROW_COUNT):

      row_array = [int(q) for q in board[ro]]
      #row_array = [int(q) for q in list(board[ro, :])]
         
      for c in range(COLUMN_COUNT - 3):
         # Create a horizontal window of 4
         window = row_array[c:c + WINDOW_LENGTH]
         score += evaluate_window(window, piece)

   # Score vertical positions
   for c in range(COLUMN_COUNT):
  

      #col_array = [int(i) for i in list(board[:, c])]
      col_array = [int(row[c]) for row in board]

      for r in range(ROW_COUNT - 3):
         # Create a vertical window of 4
         window = col_array[r:r + WINDOW_LENGTH]
         score += evaluate_window(window, piece)

    # Score positive diagonals
   for r in range(ROW_COUNT - 3):
      for c in range(COLUMN_COUNT - 3):
         # Create a positive diagonal window of 4
         window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
         score += evaluate_window(window, piece)
   # Score negative diagonals
   for r in range(ROW_COUNT - 3):
      for c in range(COLUMN_COUNT - 3):
         # Create a negative diagonal window of 4
         window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
         score += evaluate_window(window, piece)

   return score
def winning_move(board, piece):

   # Check valid horizontal locations for win
   for c in range(COLUMN_COUNT - 3):
      for r in range(ROW_COUNT):
         if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
       
            return True
   # Check valid vertical locations for win
   for c in range(COLUMN_COUNT):
      for r in range(ROW_COUNT - 3):
         if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
          
            return True

   # Check valid positive diagonal locations for win
   for c in range(COLUMN_COUNT - 3):
      for r in range(ROW_COUNT - 3):
         if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
          
            return True

   # check valid negative diagonal locations for win
   for c in range(COLUMN_COUNT - 3):
      for r in range(3, ROW_COUNT):
         if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
            
            return True
   return False
def is_terminal_node(board,valid_locations):
   #print(winning_move(board, PLAYER_PIECE),winning_move(board, BOT_PIECE),len(valid_locations) == 0)
   return winning_move(board, PLAYER_PIECE) or winning_move(board, BOT_PIECE) or valid_locations == []
def minimax(board, depth, alpha, beta, maximisingPlayer):
  
   j=0
   valid_locations=[]
   for i in avail_col:
      if i>=0:
         valid_locations.append(j)
      j+=1
   is_terminal = is_terminal_node(board,valid_locations)

   if depth == 0 or is_terminal:
      if is_terminal:
       
         # Weight the bot winning really high
         if winning_move(board, BOT_PIECE):
            return (None, 9999999)
         # Weight the human winning really low
         elif winning_move(board, PLAYER_PIECE):
            return (None, -9999999)
         else:  # No more valid moves
            return (None, 0)
      # Return the bot's score
      else:
         
         return (None, score_position(board, 1))
   if maximisingPlayer:
      value = -9999999
      # Randomise column to start
      column = r.choice(valid_locations)
      for col in valid_locations:
         row = get_next_open_row(board,col)
         
         # Create a copy of the board

         b_copy = copy.deepcopy(board)
         # Drop a piece in the temporary board and record score
         fl=drop_piece(b_copy, row, col, BOT_PIECE)
         if fl==-1:
            continue
         new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
         if new_score > value:
         
            value = new_score
            # Make 'column' the best scoring column we can get
            column = col
         alpha=max(alpha,value)
         if alpha >= beta:
            
            break
      return column, value
   else:  # Minimising player
      value = 9999999
      # Randomise column to start
      column = r.choice(valid_locations)
   
      for col in valid_locations:
         row = get_next_open_row(board,col)
         # Create a copy of the board
         b_copy = copy.deepcopy(board)
         # Drop a piece in the temporary board and record score
         fl=drop_piece(b_copy, row, col, PLAYER_PIECE)
         if fl==-1:
            continue
         new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
         if new_score < value:
            value = new_score
            # Make 'column' the best scoring column we can get
            column = col
         beta = min(beta, value)
         if alpha >= beta:
            break
      return column, value

def game(p,prev,n):
  
   play=1
   user = (176,224,230)
   comp=(248, 200, 220)
   font = p.font.SysFont('Candera', 50)
   while play==1:
      for event in p.event.get():
         if event.type == p.QUIT:
               p.quit()
               sys.exit()
       
         if n==0:
            n=5
            res = font.render('Wait', True,comp)
            screen.blit(res,(470,140))
            first=r.randint(2,4)
            avail_col[first]-=1
            clicked_comp.append([first,0])
            drop_piece(board,0,first,1)
            first=first*55+310
            not_clicked.remove([first,475])
            computer_clicked(first,475)
            p.display.update()
            p.draw.rect(screen,(0,0,0),p.Rect((430,130),(300,50)))
                  
            
         res = font.render('Your turn', True,user)
         screen.blit(res,(430,140))
         p.display.update()
            
           
         if event.type == p.MOUSEBUTTONDOWN:
            pos = p.mouse.get_pos()
            if pos[0]>310 and pos[1]>200:
          
               if prev!=pos:
                  
                  x2=(pos[0]-310)//55
                  y=avail_col[x2]*55+200
                  x=x2*55
                  x+=310
                  if [x,y] in not_clicked:
                     not_clicked.remove([x,y])
                     clicked_user.append([x2,5-avail_col[x2]])
                     user_clicked(x,y)
                     drop_piece(board,5-avail_col[x2],x2,-1)
                     avail_col[x2]-=1
                            
            
                     p.display.update()      
                     if winning_move(board,-1)==True:
                       
                
                        return 1
                        
                     if not_clicked==[]:
    
                        return 0
                     p.draw.rect(screen,(0,0,0),p.Rect((430,130),(300,100)))
                     res = font.render('Wait', True,comp)
                     screen.blit(res,(470,140))
                     first,val=minimax(board,3,-9999999,9999999,True)
                     last=avail_col[first]*55+200
                     clicked_comp.append([first,5-avail_col[first]])
               
                     drop_piece(board,5-avail_col[first],first,1)
                     avail_col[first]-=1
                     first=first*55+310
                     not_clicked.remove([first,last])
                     computer_clicked(first,last)
                     if not_clicked==[]:
          
                        return 0
                     if winning_move(board,1)==True:
                        
                        return -1
     
                     prev=pos
                     p.draw.rect(screen,(0,0,0),p.Rect((430,130),(300,50)))
                     
      
def intro():

   font = p.font.SysFont('Candara', 70,bold=True)
   heading = font.render('CONNECT4', True,(8, 143, 143))
  
   screen.blit(heading,(350,200))
   font_button=p.font.SysFont(' Inkfree ',30)
   start_button=font_button.render(' Click here to start ',True,(173, 216, 230))
   start_rect = start_button.get_rect(topleft=(400,300))
   start_rect_inflated = start_rect.inflate(20, 20)
   screen.blit(start_button, start_rect)
   p.draw.rect(screen,(182, 208, 226),start_rect_inflated,2)
   p.display.update()
   if event.type == p.MOUSEBUTTONDOWN:
      if start_rect_inflated.collidepoint(event.pos):
         
         n=r.randint(0,1)
         return n
   return -1

def result(outcome):
   if outcome==1:
      font = p.font.SysFont('Footlight', 70,bold=True)
      res = font.render('YOU WON', True,(150, 222, 209))
      screen.blit(res,(350,200))
   elif outcome==-1:
      font = p.font.SysFont('Footlight', 70,bold=True)
      res = font.render('YOU LOST', True,(150, 222, 209))
      screen.blit(res,(350,200))
   else:
      font = p.font.SysFont('Footlight', 70,bold=True)
      res = font.render('DRAW', True,(150, 222, 209))
      screen.blit(res,(350,200))
   p.display.update()
   font_button=p.font.SysFont(' Inkfree ',30)
   restart_button=font_button.render(' Click here to play again ',True,(204, 204, 255))
   restart_rect = restart_button.get_rect(topleft=(400,300))
   restart_rect_inflated = restart_rect.inflate(20, 20)
   screen.blit(restart_button, restart_rect)
   p.draw.rect(screen, (96, 130, 182),restart_rect_inflated,2)
   p.display.update()
   
   if event.type == p.MOUSEBUTTONDOWN:
      pos=p.mouse.get_pos()

      if pos[0]>=400 and pos[0]<=720 and pos[1]>=300 and pos[1]<=330:
         return -1
   return -2
   
while n<0:
        
   for event in p.event.get():
      if event.type == p.QUIT:
            p.quit()
            sys.exit()
      if n==-1:
         n=intro()

      if n==0 or n==1:
     
         screen.fill((0,0,0))
         create()
         create_board()
         outcome=game(p,-1,n)
         p.time.delay(1000)
         n=-2

      if n==-2:
         p.display.update()
         screen.fill((0,0,0))
         n=result(outcome)

         if n==-1:
            screen.fill((0,0,0))
            board=[]
            clicked_comp=[]
            clicked_user=[]
            not_clicked=[]
            valid_locations=[]
            avail_col=[5]*7
            sp.empty()
         


