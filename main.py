import pygame


class Ship:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.velocity = Vector()
        # load image and create collision rectangle based on image
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        # center ship position
        self.rect.midbottom = self.screen_rect.midbottom
        # create laser sprite group
        self.lasers = pygame.sprite.Group()

    def center_ship(self):
        # center ship position
        self.rect.midbottom = self.screen_rect.midbottom

    def fire(self):
        # create a temporary laser at current position
        temp_laser = Laser(game=self.game, x=self.rect.left, y=self.rect.top)
        # add to list of active lasers
        self.lasers.add(temp_laser)

    def remove_lasers(self):
        # empty laser list
        self.lasers.remove()

    def move(self):
        # do not move if velocity equals default vector (0, 0)
        if self.velocity == Vector():
            return
        # add vector values to rect position
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        # have game class check for moving off screen
        self.game.limit_on_screen(self.rect)

    def draw(self):
        # draw current image at current rect location
        self.screen.blit(self.image, self.rect)

    def update(self):
        # update self
        self.move()
        self.draw()
        # update lasers
        for laser in self.lasers:
            laser.update()
        # check lasers for moving off screen using copy of list to avoid format issues
        for laser in self.lasers.copy():
            if laser.rect.bottom < 0:
                self.lasers.remove(laser)
        # check collision between aliens and lasers, removing all that connect
        pygame.sprite.spritecollide(self.game.fleet.aliens, self.lasers, True, True)


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __rmul__(self, k: float):
        return Vector(k * self.x, k * self.y)

    def __mul__(self, k: float):
        return self.__rmul__(k)

    def __truediv__(self, k: float):
        return self.__rmul__(1.0/k)

    def __neg__(self):
        self.x *= -1
        self.y *= -1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def test():
        v = Vector(x=2, y=2)
        u = Vector(x=5, y=5)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('uplusv is {}'.format(u + v))
        print('uminusv is {}'.format(u - v))
        print('ku is {}'.format(2.1 * u))
        print('-u is {}'.format(-1 * u))


def main():
    Vector.test()


if __name__ == '__main__':
    main()
