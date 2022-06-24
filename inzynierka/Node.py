import pygame

# kolory
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
cyan = (0, 180, 255)
magenta = (255, 0, 255)
pink = (255, 20, 147)
grey = (128, 128, 128)

owner_to_color = {
    0: grey,
    1: black,
    2: red,
    3: blue,
    4: green,
    5: orange,
}


class Node(pygame.sprite.Sprite):
    def __init__(self, node_id, x_cord, y_cord, owner_id):
        pygame.sprite.Sprite.__init__(self)
        # wlasne rzeczy
        self.id = node_id
        self.owner_id = owner_id
        self.units_amount = 0
        #self.x_cord = x_cord
        #self.y_cord = y_cord
        self.chosen = False
        self.marked_neighbour = False
        self.outside_score = 0
        # czcionka do liczb
        self.font = pygame.font.SysFont("Arial", 25)
        self.textSurf = self.font.render(str(self.units_amount), 1, white)

        self.size = 30
        # obiekt/wezel/node
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(owner_to_color.get(self.owner_id))

        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
        self.rect.topleft = (self.rect.x, self.rect.y)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        # pozycja tekstu wzgledem czegos w tym kwadracie
        self.image.blit(self.textSurf, [W+3, H - 22])

    def update(self):

        self.textSurf = self.font.render(str(self.units_amount), 1, white)

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(owner_to_color.get(self.owner_id))

        textrect = self.textSurf.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.textSurf, textrect)
        if self.chosen:
            #pygame.draw.circle(self.image, yellow, [0, 0], 20)
            pygame.draw.rect(self.image, yellow, [0, 0, self.size-1, self.size-1], 4)
            # self.chosen = False
        if self.marked_neighbour:
            pygame.draw.rect(self.image, magenta, [0, 0, self.size-1, self.size-1], 4)

    def set_ownership(self, owner):
        self.owner_id = owner

    def change_units_amount(self, units_change):
        self.units_amount += units_change

    def set_cords(self, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord

    def clicked(self, x):
        self.chosen = x

    def set_neighbour(self, x):
        self.marked_neighbour = x

    def manhattan_pos(self, game_tree):
        x = int(self.id/game_tree.columns)
        y = self.id % game_tree.columns

        return [x,y]
    def adjust_id(self):
        self.id -=1