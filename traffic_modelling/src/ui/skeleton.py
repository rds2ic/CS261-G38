import pygame

pygame.init()
WIDTH = HEIGHT = 800
FPS = 240
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def update_display(s):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    s.fill("black")
    clock.tick(FPS)
    pygame.display.update()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                pass
        update_display(screen)


if __name__ == "__main__":
    main()
