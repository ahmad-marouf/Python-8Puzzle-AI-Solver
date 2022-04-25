from os import waitpid
from tkinter import *
from tkinter import font
from puzzle import *
from threading import Thread
import concurrent.futures

class GUI:
    def __init__(self,master):
        master.geometry("800x650")
        #----------------------------Functions----------------------------------------------
        def checkInput(initState):
            flag = 0

            if not initState.isnumeric(): flag = 1
            elif len(initState) != 9: flag = 1
            elif len(initState) != len(set(initState)): flag = 1
            else:
                sum = 0
                for c in initState:
                    sum = sum + int(c)
                if sum != 36: flag = 1

            if flag == 1:
                printErr("Error in state, please enter the state using 9 digits ( 0 -> 8 )")
                return False
            else:
                setError.grid_forget()
                return True
        
        def solve():
            b.configure(state='disabled')
            if not isSolvable(e.get()):
                printErr("Initial State Entered is Unsolvable")
                return
            # RUN SEARCH
            #---------------------------------------------------------------
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(main, e.get(), variable.get())
                master.update()
                resultList = future.result()
            #---------------------------------------------------------------
            if resultList == 'goal not found':
                printErr("Goal Not Found")
                return
            if (len(resultList[1]) <= 50):
                initBoard.configure(state='disabled')
                printResults(resultList)
                animateSol(resultList)
            else:
                printFile(resultList)
                setBoard('012345678')
        
        def setBoardInit():
            resTxt.configure(state='normal')
            resTxt.delete('1.0','end')
            resTxt.configure(state='disabled')
            istate = e.get()
            if checkInput(istate):
                b.configure(state='normal')
                setBoard(istate)
            else:
                b.configure(state='disabled')
            
        def setBoard(state):
            tileCoords = []
            tileCoords = getRelCoord(state.find('1'))
            self.tile1Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('2'))
            self.tile2Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('3'))
            self.tile3Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('4'))
            self.tile4Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('5'))
            self.tile5Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('6'))
            self.tile6Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('7'))
            self.tile7Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            tileCoords = getRelCoord(state.find('8'))
            self.tile8Label.place(in_=self.boardLabel, relx=tileCoords[0], rely=tileCoords[1])
            return
            
        def getRelCoord(index):
            coords = {
                0: [0.025,0.025],
                1: [0.345,0.025],
                2: [0.665,0.025],
                3: [0.025,0.345],
                4: [0.345,0.345],
                5: [0.665,0.345],
                6: [0.025,0.665],
                7: [0.345,0.665],
                8: [0.665,0.665]
            }
            return coords.get(index)

        def animateSol(resultList):
            state = e.get()
            time.sleep(0.5)
            for path in resultList[1]:
                adjacent = getAdj(state.find('0'))
                possiblePaths = {
                    'Up': state[adjacent[0]],
                    'Left': state[adjacent[1]],
                    'Right': state[adjacent[2]],
                    'Down': state[adjacent[3]]
                }
                state = swapTiles(state,'0',possiblePaths.get(path))
                setBoard(state)
                master.update()
                time.sleep(0.5)
            initBoard.configure(state='normal')

        def printResults(resultList):
            resTxt.configure(state='normal')
            resTxt.delete('1.0','end')
            resTxt.insert('end', "Path: \t" + str(resultList[1]) + "\n\n")
            resTxt.insert('end', "Cost: \t" + str(resultList[0].cost) + "\n")
            resTxt.insert('end', "Nodes Expanded: \t" + str(resultList[2]) + "\n")
            resTxt.insert('end', "Maximum Search Depth: \t" + str(resultList[4]) + "\n")
            resTxt.insert('end', "Running Time: \t" + str(resultList[3]) + "\n")
            resTxt.configure(state='disabled')

        def printFile(resultList):
            resTxt.configure(state='normal')
            resTxt.delete('1.0','end')
            resTxt.insert('end', "Path too long to visualize, printed in output.txt \n\n")
            resTxt.insert('end', "Cost: \t" + str(resultList[0].cost) + "\n\n")
            resTxt.insert('end', "Nodes Expanded: \t" + str(resultList[2]) + "\n\n")
            resTxt.insert('end', "Maximum Search Depth: \t" + str(resultList[4]) + "\n\n")
            resTxt.insert('end', "Running Time: \t" + str(resultList[3]) + "\n\n")
            resTxt.configure(state='disabled')
            file = open('output.txt', 'w')
            file.write("path:" + str(resultList[1]) + "\n")
            file.write("cost:" + str(resultList[0].cost) + "\n")
            file.write("nodes expanded:" + str(resultList[2]) + "\n")
            file.write("maximum search depth:" + str(resultList[4]) + "\n")
            file.write("running time:" + str(resultList[3]) + "\n")
            file.close()
        
        def printErr(message):
            setError.grid(row=2, columnspan=2)
            setError.config(text=message)

        #---------------------------------Menus------------------------------------------
        titleLbl = Label(master, text= "8-puzzle Solver", fg = "red")
        titleLbl.config(font=("Courier", 44))
        titleLbl.grid(row=0, columnspan=4)
        Label(master, text="Enter Initial State:").grid(row=1, sticky=W)
        e = Entry(master)
        e.grid(row=1, column=1)
        b = Button(master, height=1, width=10, text="Solve", command=solve)
        b.grid(row=4,column=1, sticky=E)
        Label(master, text="Choose The Type of Algorithm:", width=25).grid(row=3)
        choices = ['BFS', 'DFS', 'A* (Manhattan)', 'A* (Euclidean)']
        variable = StringVar(master)
        variable.set('BFS')
        w = OptionMenu(master, variable, *choices)
        w.configure(width=15)
        w.grid(row=3,column=1, sticky=E)

        initBoard = Button(master, text="Set Board", command=setBoardInit)
        initBoard.grid(row=1, column=2, padx=10)

        setError = Label(master, text="Error in state, please enter the state using 9 digits ( 0 -> 8 )", fg="red")
        

        resTxt = Text(master, state='disabled', height=10, width=80)
        resTxt.grid(row=8, column=0, columnspan=4, padx=20, pady=10)

        scrollbar = Scrollbar(master, command=resTxt.yview)
        scrollbar.place(in_=resTxt, relx=1)
        resTxt['yscrollcommand'] = scrollbar.set
        
        #--------------------------------Puzzle GUI----------------------------------------
        # BOARD LAYOUT
        self.boardPhoto = PhotoImage(file="images/board.png")
        self.boardLabel = Label(master, image=self.boardPhoto)

        self.tile1Photo = PhotoImage(file="images/tile1.png")
        self.tile1Label = Label(master, image=self.tile1Photo)
        self.tile2Photo = PhotoImage(file="images/tile2.png")
        self.tile2Label = Label(master, image=self.tile2Photo)
        self.tile3Photo = PhotoImage(file="images/tile3.png")
        self.tile3Label = Label(master, image=self.tile3Photo)
        self.tile4Photo = PhotoImage(file="images/tile4.png")
        self.tile4Label = Label(master, image=self.tile4Photo)
        self.tile5Photo = PhotoImage(file="images/tile5.png")
        self.tile5Label = Label(master, image=self.tile5Photo)
        self.tile6Photo = PhotoImage(file="images/tile6.png")
        self.tile6Label = Label(master, image=self.tile6Photo)
        self.tile7Photo = PhotoImage(file="images/tile7.png")
        self.tile7Label = Label(master, image=self.tile7Photo)
        self.tile8Photo = PhotoImage(file="images/tile8.png")
        self.tile8Label = Label(master, image=self.tile8Photo)

        self.boardLabel.grid(row=1, column=3, rowspan=5, padx=50, pady=5)
        #--------------------------------Initialize Window----------------------------------------
        setBoard('012345678')
        b.configure(state='disabled')

        


root = Tk()
g = GUI(root)
root.mainloop()