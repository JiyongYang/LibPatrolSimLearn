import tkinter as tk
from PIL import ImageTk, Image
import time

PhotoImage = ImageTk.PhotoImage
UNIT = 25
HEIGHT = 100
WIDTH = 100
REVERSE = 100
SIZEOFCANVAS_HEIGHT = 1200
SIZEOFCANVAS_WIDTH = 1200

class Drawer(tk.Tk):
    def __init__(self):
        super(Drawer, self).__init__()
        self.geometry('{0}x{1}'.format(SIZEOFCANVAS_WIDTH, SIZEOFCANVAS_HEIGHT))#HEIGHT * UNIT, HEIGHT * UNIT))
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.texts = []
        self.policyHeatmap = None

    def setPolicyHeatmap(self, m):
        self.policyHeatmap = m

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=HEIGHT * UNIT,
                           width=WIDTH * UNIT,
                           scrollregion=(0, 0, WIDTH * UNIT, HEIGHT * UNIT))

        hbar=tk.Scrollbar(self,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=canvas.xview)
        vbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=canvas.yview)

        # create grid line
        for c in range(0, WIDTH * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, HEIGHT * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
            canvas.create_line(x0, y0, x1, y1)


        canvas.config(width=300,height=300)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        #canvas.pack()

        return canvas


    def load_images(self):
        sieofimage = 20
        up = PhotoImage(
            Image.open("img/up.png").resize((sieofimage, sieofimage)))
        down = PhotoImage(
            Image.open("img/down.png").resize((sieofimage, sieofimage)))
        left = PhotoImage(
            Image.open("img/left.png").resize((sieofimage, sieofimage)))
        right = PhotoImage(
            Image.open("img/right.png").resize((sieofimage, sieofimage)))
        rightup = PhotoImage(
            Image.open("img/rightup.png").resize((sieofimage, sieofimage)))
        rightdown = PhotoImage(
            Image.open("img/rightdown.png").resize((sieofimage, sieofimage)))
        leftup = PhotoImage(
            Image.open("img/leftup.png").resize((sieofimage, sieofimage)))
        leftdown = PhotoImage(
            Image.open("img/leftdown.png").resize((sieofimage, sieofimage)))

        return right, rightup, up, leftup, left, leftdown, down, rightdown

    def text_value(self, row, col, contents, action, font='Helvetica', size=7,
                   style='normal', anchor="nw"):

        # right
        if action == 0:
            origin_x, origin_y = 76, 42
        # rightup
        elif action == 1:
            origin_x, origin_y = 76, 5
        # up
        elif action == 2:
            origin_x, origin_y = 42, 5
        # leftup
        elif action == 3:
            origin_x, origin_y = 7, 5
        # left
        elif action == 4:
            origin_x, origin_y = 7, 42
        # leftdown
        elif action == 5:
            origin_x, origin_y = 7, 77
        # down
        elif action == 6:
            origin_x, origin_y = 42, 77
        # rightdown
        elif action == 7:
            origin_x, origin_y = 76, 77


        origin_x = origin_x / 100 * UNIT
        origin_y = origin_y / 100 * UNIT

        x, y = origin_x + (UNIT * row), origin_y + (UNIT * col)
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill="black", text=contents,
                                       font=font, anchor=anchor)
        return self.texts.append(text)

    def text_value_a(self, row, col, contents, font='Helvetica', size=7,
                   style='normal', anchor="nw"):


        x, y = (UNIT * row), (UNIT * col)
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill="black", text=contents,
                                       font=font, anchor=anchor)
        return self.texts.append(text)

    def print_value_all(self, policyHeatmap):
        for i in self.texts:
            self.canvas.delete(i)
        self.texts.clear()
        for i in range(WIDTH):
            for j in range(HEIGHT):
                dir = (0, 0)
                bal = 0
                for action in range(0, 8):
                    temp = policyHeatmap[i][j][action]
                    #self.text_value(i, REVERSE-j, round(temp, 2), action)
                    if dir[1] < temp:
                        dir = (action, temp)
                    bal += temp
                if bal != 0:
                    self.canvas.create_image(i*UNIT+UNIT/2, (REVERSE-j)*UNIT+UNIT/2, image=self.shapes[dir[0]])
        self.mainloop()

    def print_value_all_a(self, policyHeatmap):
        for i in self.texts:
            self.canvas.delete(i)
        self.texts.clear()
        for i in range(WIDTH):
            for j in range(HEIGHT):
                temp = policyHeatmap[i][j]
                self.text_value_a(i, REVERSE-j, temp)

        self.mainloop()

    def coords_to_state(self, coords):
        x = int((coords[0] - (UNIT/2)) / UNIT)
        y = int((coords[1] - (UNIT/2)) / UNIT)
        return [x, y]

    def state_to_coords(self, state):
        x = int(state[0] * UNIT + (UNIT/2))
        y = int(state[1] * UNIT + (UNIT/2))
        return [x, y]

    def render(self):
        time.sleep(0.03)
        self.update()
