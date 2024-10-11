import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo,showerror

colors = {
    1: 'blue',2: 'green',3: 'dark green',4:'orange', 5:'black', 6:'purple', 7:'yellow',8:'red'}

class MyButton(tk.Button):
    def __init__(self, master, x, y, number = 0, *args, **kwargs):
        super(MyButton,self).__init__(master,width=3,font='Arial 15 bold',*args,**kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.neighbors_mines = 0
        self.is_open=0


    def __repr__(self) -> str:
        return f"({self.number}:[{self.x},{self.y}],{self.is_mine})"

class Minesweeper:
    row = 10
    column = 10 
    mines = 10
    window = tk.Tk()
    window.title ("Minesweeper by Oleksii Horovych")
    photo = tk.PhotoImage(file='logo.png')
    window.iconphoto(False,photo)
    is_gameover = False
    flags_correct = 0

    def __init__(self):
        self.buttons = []
        for i in range(Minesweeper.row + 2):
            temp = []
            for j in range(Minesweeper.column + 2):
                btn = MyButton(Minesweeper.window,x = i, y = j)
                btn.config(command=lambda button = btn: self.click(button))
                btn.bind('<Button-3>',self.right_click)
                temp.append(btn)
            self.buttons.append(temp)
            
    def right_click(self, event):
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            if cur_btn.is_mine:
                Minesweeper.flags_correct += 1
        elif cur_btn['text'] == '🚩':
            cur_btn['state'] = 'normal'
            cur_btn['text'] = ' '
            if cur_btn.is_mine:
                Minesweeper.flags_correct -= 1
        self.check_victory()

    def check_victory(self):
        total_cells = Minesweeper.row * Minesweeper.column
        if Minesweeper.flags_correct == Minesweeper.mines and self.count_open_cells() == total_cells - Minesweeper.mines:
            self.is_gameover = True
            self.open_all()
            showinfo("Congratulations!", "You won!")
            save_btn = tk.Button(showinfo, text="Save and restart", command=lambda: self.change_settings(self.row_entry, self.column_entry, self.mines_entry))
            save_btn.grid(row=3, column=0, columnspan=2)

    def create_settings(self):
        win_settings=tk.Toplevel(self.window)
        win_settings.wm_title("Settings")

        tk.Label(win_settings,text="Rows:").grid(row=0,column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0,Minesweeper.row)
        row_entry.grid(row=0,column=1,padx=20,pady=20)

        tk.Label(win_settings,text="Columns:").grid(row=1,column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0,Minesweeper.column)
        column_entry.grid(row=1,column=1,padx=20,pady=20)
        
        tk.Label(win_settings,text="Mines:").grid(row=2,column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0,Minesweeper.mines)
        mines_entry.grid(row=2,column=1,padx=20,pady=20)

        save_btn=tk.Button(win_settings,text="Save and restart",command=lambda:self.change_settings(row_entry,column_entry,mines_entry))
        save_btn.grid(row=3,column=0,columnspan=2)

    def change_settings(self,row:tk.Entry,column:tk.Entry,mines:tk.Entry):    
        try:
            int(row.get()),int(column.get()),int(mines.get())
        except ValueError:
            showerror("Wrong input", "Input integer numbers")
            

        Minesweeper.row = int(row.get())
        Minesweeper.column = int(column.get())
        Minesweeper.mines = int(mines.get())
        self.restart()

    def create_widget(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        menubar.add_command(label="Restart", command=self.restart)
        menubar.add_command(label="Settings", command=self.create_settings)
        menubar.add_command(label="Exit",command=self.window.destroy)

        for i in range(1, Minesweeper.row + 1):
            tk.Grid.rowconfigure(self.window,i,weight = 1)
            for j in range(1, Minesweeper.column + 1):
                tk.Grid.columnconfigure(self.window,j,weight = 1)
                btn = self.buttons[i][j]
                btn.grid(row = i, column = j,stick="NWES")
   

    def restart(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widget()
        self.insert_mines()
        self.cont_neighbours_mines()
        self.print_button() 
        Minesweeper.window.mainloop()


    def open_all(self):
         for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.is_mine: btn.config(text="💣",background="red", disabledforeground="black")
                
    def click(self, clicked_button: MyButton):
        if Minesweeper.is_gameover:
            return

        if clicked_button.is_mine:
            clicked_button.config(text="💣", background="red", disabledforeground="black")
            clicked_button.is_open = True
            self.is_gameover = True
            self.open_all()
            showinfo("Game over", "You lost")
        else:
            color = colors.get(clicked_button.neighbors_mines)
            if clicked_button.neighbors_mines:
                clicked_button.config(text=clicked_button.neighbors_mines, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)

        clicked_button.config(state="disabled")
        clicked_button.config(relief=tk.SUNKEN)

        if not Minesweeper.is_gameover:
            self.check_victory()


    def count_open_cells(self):
        count = 0
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.is_open:
                    count += 1
        return count

    
    def breadth_first_search(self, btn: MyButton):
        q = [btn]
        while q:
            cur_btn = q.pop()
            color = colors.get(cur_btn.neighbors_mines)
            if cur_btn.neighbors_mines:
                cur_btn.config(text=cur_btn.neighbors_mines, disabledforeground=color)
            else:
                cur_btn.config(text=" ")
            cur_btn.is_open = True
            cur_btn.config(state="disabled")
            cur_btn.config(relief=tk.SUNKEN)
            if cur_btn.neighbors_mines == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= Minesweeper.row and 1 <= next_btn.y <= Minesweeper.column and next_btn not in q:
                            q.append(next_btn)

    def start(self):
        self.create_widget()
        self.insert_mines()
        self.cont_neighbours_mines()
        self.print_button()
        Minesweeper.window.mainloop()
    
    def print_button(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("M",end=" ")
                else: print(btn.neighbors_mines,end=' ')
            print()

    def insert_mines(self):
        indexes = self.get_mines_places()
        print(indexes)
        count = 1
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                btn.number = count
                if btn.number in indexes:
                    btn.is_mine = True
                count +=1

    def cont_neighbours_mines(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn=self.buttons[i][j]
                cnt_mines = 0
                if not btn.is_mine:
                    for row_dx in [-1,0,1]:
                        for col_dx in [-1,0,1]:
                            neihbour = self.buttons[i+row_dx][j+col_dx]
                            if neihbour.is_mine:
                                cnt_mines += 1                        
                btn.neighbors_mines = cnt_mines

    def get_mines_places(self):
        a = list(range(1, Minesweeper.column*Minesweeper.row + 1))
        shuffle(a)
        return a [:Minesweeper.mines]
  
game = Minesweeper()
game.start()    