# import pygame library 
import pygame
import copy

# Default Sudoku Board.
DEFAULT_GRID = [ 
                    [7, 8, 0, 4, 0, 0, 1, 2, 0], 
                    [6, 0, 0, 0, 7, 5, 0, 0, 9], 
                    [0, 0, 0, 6, 0, 1, 0, 7, 8], 
                    [0, 0, 7, 0, 4, 0, 2, 6, 0], 
                    [0, 0, 1, 0, 5, 0, 9, 3, 0], 
                    [9, 0, 4, 0, 6, 0, 0, 0, 5], 
                    [0, 7, 0, 3, 0, 0, 0, 1, 2], 
                    [1, 2, 0, 0, 0, 7, 4, 0, 0], 
                    [0, 4, 9, 2, 0, 6, 0, 0, 7] 
                ]



class Game:
    def __init__(self):
        self.running = True
        self.screen = None
        self.size = (500, 600)
        self.grid = copy.deepcopy(DEFAULT_GRID)
        self.x = 0
        self.y = 0
        self.dif = 500 / 9

    def game_init(self):
        pygame.init()
        pygame.font.init()
        
        # Title and Icon 
        pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING") 
        img = pygame.image.load('icon.png') 
        pygame.display.set_icon(img) 

        self.screen = pygame.display.set_mode((500, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        # Load test fonts for future use 
        self.font1 = pygame.font.SysFont("comicsans", 40) 
        self.font2 = pygame.font.SysFont("comicsans", 20) 

        self.running = True
        
    def get_cord(self, pos): 
        self.x = pos[0]//self.dif 
        self.y = pos[1]//self.dif 

    # Highlight the cell selected 
    def draw_box(self): 
        for i in range(2): 
            pygame.draw.line(self.screen, (255, 0, 0),
                             (self.x * self.dif-3, (self.y + i)*self.dif), (self.x * self.dif + self.dif + 3, (self.y + i)*self.dif), 7) 
            pygame.draw.line(self.screen, (255, 0, 0),
                             ((self.x + i)* self.dif, self.y * self.dif ), ((self.x + i) * self.dif, self.y * self.dif + self.dif), 7)

    # Function to draw required lines for making Sudoku grid         
    def draw(self): 
        # Draw the lines 

        for i in range (9): 
            for j in range (9): 
                if self.grid[i][j]!= 0: 

                    # Fill blue color in already numbered grid 
                    pygame.draw.rect(self.screen, (0, 153, 153), (i * self.dif, j * self.dif, self.dif + 1, self.dif + 1)) 

                    # Fill gird with default numbers specified 
                    text1 = self.font1.render(str(self.grid[i][j]), 1, (0, 0, 0)) 
                    self.screen.blit(text1, (i * self.dif + 15, j * self.dif + 15)) 
        # Draw lines horizontally and verticallyto form grid         
        for i in range(10): 
            if i % 3 == 0 : 
                thick = 7
            else: 
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.dif), (500, i * self.dif), thick) 
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.dif, 0), (i * self.dif, 500), thick)     

    # Fill value entered in cell     
    def draw_val(self, val): 
        text1 = self.font1.render(str(val), 1, (0, 0, 0)) 
        self.screen.blit(text1, (self.x * self.dif + 15, self.y * self.dif + 15))     

    # Raise error when wrong value entered 
    def raise_error1(self): 
        text1 = self.font1.render("WRONG !!!", 1, (0, 0, 0)) 
        self.screen.blit(text1, (20, 570))
        
    def raise_error2(self): 
        text1 = self.font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0)) 
        self.screen.blit(text1, (20, 570)) 

    # Check if the value entered in board is valid 
    def valid(self, m, i, j, val): 
        for it in range(9): 
            if m[i][it]== val: 
                return False
            if m[it][j]== val: 
                return False
        it = i//3
        jt = j//3
        for i in range(it * 3, it * 3 + 3): 
            for j in range (jt * 3, jt * 3 + 3): 
                if m[i][j]== val: 
                    return False
        return True

    # Solves the sudoku board using Backtracking Algorithm 
    def solve(self, grid, i, j): 

        while grid[i][j]!= 0: 
            if i<8: 
                i+= 1
            elif i == 8 and j<8: 
                i = 0
                j+= 1
            elif i == 8 and j == 8: 
                return True
        pygame.event.pump()  
        for it in range(1, 10): 
            if self.valid(grid, i, j, it)== True: 
                grid[i][j]= it
                
                self.x = i 
                self.y = j 
                # white color background\ 
                self.screen.fill((255, 255, 255)) 
                self.draw() 
                self.draw_box() 
                pygame.display.update() 
                pygame.time.delay(20) 
                if self.solve(grid, i, j)== 1: 
                    return True
                else: 
                    grid[i][j]= 0
                # white color background\ 
                self.screen.fill((255, 255, 255)) 

                self.draw() 
                self.draw_box() 
                pygame.display.update() 
                pygame.time.delay(50)    
        return False

    # Display instruction for the game 
    def instruction(self):
        text1 = self.font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", 1, (0, 0, 0)) 
        text2 = self.font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 540))        
        self.screen.blit(text2, (20, 560)) 

    # Display options when solved 
    def result(self): 
        text1 = self.font1.render("FINISHED PRESS R or D", 1, (0, 0, 0)) 
        self.screen.blit(text1, (20, 570))

    def main_loop(self):
        val = 0
        flag1 = 0
        flag2 = 0
        rs = 0
        error = 0
        # The loop thats keep the window running 
        while self.running: 

            # White color background 
            self.screen.fill((255, 255, 255)) 
            # Loop through the events stored in event.get() 
            for event in pygame.event.get(): 
                # Quit the game window 
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                # Get the mouse postion to insert number     
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    flag1 = 1
                    pos = pygame.mouse.get_pos() 
                    self.get_cord(pos) 
                # Get the number to be inserted if key pressed   
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_LEFT: 
                        self.x-= 1
                        flag1 = 1
                    if event.key == pygame.K_RIGHT: 
                        self.x+= 1
                        flag1 = 1
                    if event.key == pygame.K_UP: 
                        y-= 1
                        flag1 = 1
                    if event.key == pygame.K_DOWN: 
                        y+= 1
                        flag1 = 1   
                    if event.key == pygame.K_1: 
                        val = 1
                    if event.key == pygame.K_2: 
                        val = 2 
                    if event.key == pygame.K_3: 
                        val = 3
                    if event.key == pygame.K_4: 
                        val = 4
                    if event.key == pygame.K_5: 
                        val = 5
                    if event.key == pygame.K_6: 
                        val = 6
                    if event.key == pygame.K_7: 
                        val = 7
                    if event.key == pygame.K_8: 
                        val = 8
                    if event.key == pygame.K_9: 
                        val = 9
                    if event.key == pygame.K_RETURN: 
                        flag2 = 1
                    # If R pressed clear the sudoku board 
                    if event.key == pygame.K_r: 
                        rs = 0
                        error = 0
                        flag2 = 0
                        self.grid =[ 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0] 
                        ] 
                    # If D is pressed reset the board to default 
                    if event.key == pygame.K_d: 
                        rs = 0
                        error = 0
                        flag2 = 0
                        self.grid = copy.deepcopy(DEFAULT_GRID)

            if flag2 == 1: 
                if self.solve(self.grid, 0, 0)== False: 
                    error = 1
                else: 
                    rs = 1
                flag2 = 0

            if val != 0:             
                self.draw_val(val) 
                # print(self.x) 
                # print(self.y) 
                if self.valid(self.grid, int(self.x), int(self.y), val)== True: 
                    self.grid[int(self.x)][int(self.y)]= val 
                    flag1 = 0
                else: 
                    self.grid[int(self.x)][int(self.y)]= 0
                    self.raise_error2()

                val = 0 

            if error == 1: 
                self.raise_error1()

            if rs == 1: 
                self.result()
                
            self.draw()
            
            if flag1 == 1: 
                self.draw_box()
                
            self.instruction()    

            # Update window 
            pygame.display.update()

        # Quit pygame window     
        pygame.quit()    

        



if __name__ == '__main__':
    game = Game()
    game.game_init()
    game.main_loop()
