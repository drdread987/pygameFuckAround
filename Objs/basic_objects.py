import pygame


class BasicObject:

    def __init__(self):

        self.eventer = False
        self.depth = 50
        self.living = False
        self.friendly = True
        self.id = None

        self.function = None

        self.image = pygame.image.load('images/ball.png')
        self.x = 0
        self.y = 0
        self.height = 35
        self.width = 35

        self.jumping = False

        self.gravity = True
        self.on_ground = False
        self.gravity_scale = 10
        self.gravity_velocity = 0
        self.gravity_adder = False

    def step(self, obj_list):

        if self.gravity and not self.jumping:

            if self.gravity_velocity < self.gravity_scale and self.gravity_adder:

                self.gravity_velocity += 1
                self.gravity_adder = False
            elif self.gravity_velocity < self.gravity_scale:

                self.gravity_adder = True

            doodads = obj_list.get_doodad_list()

            walls = []

            for dood in doodads:
                if dood[1].function == "WALL" and dood[0] != self.id:
                    walls.append(dood[1])

            for wall in walls:

                if self.y + self.height + self.gravity_velocity >= wall.y > self.y + self.height:

                    if self.x + self.width >= wall.x and self.x <= wall.x + wall.width:

                        self.y = wall.y - self.height
                        self.gravity_velocity = 0
                        self.on_ground = True

            if not self.on_ground:
                self.y += self.gravity_velocity

    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))

    def handle_events(self, events, obj_list):

        pass


class BasicUnit(BasicObject):

    def __init__(self, x, y):

        super().__init__()

        self.min_health = 1
        self.max_health = 1
        self.min_resource = 1
        self.max_resource = 1
        self.resource_type = 0
        self.min_speed = 0
        self.max_speed = 0

        self.x = x
        self.y = y

    def step(self, obj_list):

        BasicObject.step(self, obj_list)

        if self.id is None:

            self.id = obj_list.get_unit(obj=self)[0]


class BasicDoodad(BasicObject):

    def __init__(self, x, y):

        super().__init__()

        self.x = x
        self.y = y

    def step(self, obj_list):

        BasicObject.step(self, obj_list)

        if self.id is None:

            self.id = obj_list.get_doodad(obj=self)[0]


class BasicOther(BasicObject):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.min_speed = 0
        self.max_speed = 0

    def step(self, obj_list):
        BasicObject.step(self, obj_list)

        if self.id is None:
            self.id = obj_list.get_other(obj=self)[0]


