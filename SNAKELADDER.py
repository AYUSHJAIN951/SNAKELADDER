import tkinter as tk
from time import sleep
from random import randint

root = tk.Tk()

Grid = []
for i in range(8):
  GridRow = []
  for j in range(8):
    GridRow.append("Empty")
  Grid.append(GridRow)
Grid[0][0] = "End"
Grid[7][0] = "Start"

#Snakes
Grid[0][3] = [2,1,"S"]
Grid[0][6] = [2,7,"S"]
Grid[2][6] = [5,2,"S"]
Grid[3][1] = [4,0,"S"]
Grid[3][5] = [5,6,"S"]
Grid[6][2] = [6,5,"S"]

#Ladders
Grid[2][0] = [0,0,"L"]
Grid[1][7] = [0,7,"L"]
Grid[2][4] = [1,5,"L"]
Grid[5][5] = [1,2,"L"]
Grid[7][2] = [5,0,"L"]
Grid[7][5] = [5,7,"L"]

#[Row,Collumn]
player1 = [7,0]
player2 = [7,0]

LabelGrid = []

def updateGrid():
  global player1
  global player2
  global LabelGrid
  global Grid
  for i in LabelGrid:
    i.grid_forget()
  for i in range(8):
    for j in range(8):
      root.grid_rowconfigure(i,weight=1,minsize=128)
      root.grid_columnconfigure(j,weight=1,minsize=128)
      Label = tk.Label(root)
      Label.grid(column=j,row=i,sticky="nsew")
      LabelGrid.append(Label)
      if (i+j)%2 == 0:
        Label.configure(bg="Black")
      if Grid[i][j] == "Empty":
        Label.configure(text="")
      elif Grid[i][j] == "Start":
        Label.configure(text="Start",bg="Sky Blue")
      elif Grid[i][j] == "End":
        Label.configure(text="End",bg="Gold")
      else:
        LabelText = "Leads to\nCollumn "+str(Grid[i][j][1])+"\nRow "+str(Grid[i][j][0])
        Label.configure(text=LabelText,bg="Red" if Grid[i][j][2] == "S" else "Green")
  
  p1 = tk.Label(root,text="Player 1",bg="Yellow")
  p1.grid(column=player1[1],row=player1[0],sticky="n")
  LabelGrid.append(p1)  
  p2 = tk.Label(root,text="Player 2",bg="Blue")
  p2.grid(column=player2[1],row=player2[0],sticky="s")
  LabelGrid.append(p2)
  root.update()

def movePlayer(player,spaces):
  global Grid
  endSpace = player
  for i in range(spaces):
    if endSpace == [0,0]:
      return endSpace
    if endSpace[0]%2 == 1:
      if endSpace[1] == 7:
        endSpace[0] -= 1
      else:
        endSpace[1] += 1
    else:
      if endSpace[1] == 0:
        endSpace[0] -= 1
      else:
        endSpace[1] -= 1
  if type(Grid[endSpace[0]][endSpace[1]]) == list :
    return [Grid[endSpace[0]][endSpace[1]][0],Grid[endSpace[0]][endSpace[1]][1]]
  return endSpace

Turn = 1
Winner = ""

Text = tk.Label(root,text="Loading")
WaitVariable = tk.IntVar()
Button = tk.Button(root,text="Roll",command=lambda: WaitVariable.set(1))
Text.grid(column=0,row=8,columnspan=8,sticky="nsew")
Button.grid(column=0,row=9,columnspan=8,sticky="nsew")

root.grid_rowconfigure(8,weight=1,minsize=64)
root.grid_rowconfigure(9,weight=1,minsize=64)

updateGrid()
while True:
  Text.configure(text="Player "+("1" if Turn%2 ==1 else "2")+"'s turn")
  Button.wait_variable(WaitVariable)
  roll = randint(1,6)
  Text.configure(text="Rolled a "+str(roll))
  if Turn%2 == 1:
    player1 = movePlayer(player1,roll)
    if player1 == [0,0]:
      Winner = "Player 1"
      break
  else:
    player2 = movePlayer(player2,roll)
    if player2 == [0,0]:
      Winner = "Player 2"
      break
  Turn += 1
  updateGrid()
  sleep(1)

Text.configure(text=Winner+" wins!")
updateGrid()