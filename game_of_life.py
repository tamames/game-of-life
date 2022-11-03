import time
import numpy as np
import pygame


# define the colors we are going to use
COLOR_BG = (10,10,10)
COLOR_GRID = (40,40,40)
COLOR_DIE_NEXT = (170,170,170)
COLOR_ALIVE_NEXT = (255,255,255)

def update(screen, cells, size, with_progress=False):
    # if with_progress is True we are ejecuting the next step 
    # of the game, if not we are just updating the screen

    update_cells = np.zeros(cells.shape)

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col]==0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1: #is alive
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            
            elif 2 <= alive <= 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        
        else: #the cell is not alive
            if alive == 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))

    return update_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False


    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.display.quit()
                quit()
                return
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # if we press space we want to pause the game
                    # whereas it's running or not
                    running = not running 
                    update(screen, cells, 10)
                    pygame.display.update()

                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    quit()
                    # break

                if event.key == pygame.K_c:
                    # clear the screen
                    cells[:,:] = 0
                    update(screen, cells, 10)
                    pygame.display.update()
            
            if pygame.mouse.get_pressed()[0]: #this gets us the first button of the mause
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()
        
        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)



if __name__ == '__main__':
    main()
