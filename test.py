import pygame
import sys
from Objs import player
from Objs import ground
from Objs import bad_ball

# todo make a basic object class


class ObjectHandler:

    def __init__(self):

        self.unit_list = []  # ai adjusted objects, stored [[id, object], ...]
        self.doodad_list = []  # non-ai objects, stored [[id, object], ...]
        self.other_list = []  # anything that is adjusted but not full ai, stored [[id, object], ...]

        self.all_ids = []  # stores all currently in use ids, or dieing ids, stored [id, ...]
        self.dieing_ids = []  # store id's that are dieing in order to make sure ids are not assigned too soon
        # stored [[age, id], ...]

    def get_unit_list(self):

        return self.unit_list

    def get_doodad_list(self):

        return self.doodad_list

    def get_other_list(self):

        return self.other_list

    def get_unit(self, uid=None, obj=None):

        if uid is not None:
            for unit_block in self.unit_list:
                if unit_block[0] == uid:
                    return unit_block
        elif obj is not None:
            for unit_block in self.unit_list:
                if unit_block[1] == obj:
                    return unit_block
        else:
            return False

    def get_doodad(self, did=None, obj=None):

        if did is not None:
            for doodad_block in self.doodad_list:
                if doodad_block[0] == did:
                    return doodad_block
        elif obj is not None:
            for doodad_block in self.doodad_list:
                if doodad_block[1] == obj:
                    return doodad_block
        else:
            return False

    def get_other(self, oid=None, obj=None):

        if oid is not None:
            for other_block in self.other_list:
                if other_block[0] == oid:
                    return other_block
        elif obj is not None:
            for other_block in self.other_list:
                if other_block[1] == obj:
                    return other_block
        else:
            return False

    def handle_step(self, screen, events):

        self.handle_ids()

        for unit in self.unit_list:
            if unit[1].eventer:
                unit[1].handle_events(events, self)
        for doodad in self.doodad_list:
            if doodad[1].eventer:
                doodad[1].handle_events(events, self)
        for other in self.other_list:
            if other[1].event:
                other[1].handle_events(events, self)

        for unit in self.unit_list:
            unit[1].step(self)
        for doodad in self.doodad_list:
            doodad[1].step(self)
        for other in self.other_list:
            other[1].step(self)

        draw_order = []
        for unit in self.unit_list:
            draw_order.append([unit[1].depth, unit, "UNIT"])
        for doodad in self.doodad_list:
            draw_order.append([doodad[1].depth, doodad, "DOODAD"])
        for other in self.other_list:
            draw_order.append([other[1].depth, other, "OTHER"])
        draw_order.sort()
        blank_health = pygame.image.load('images/empty_health_bar.png')
        full_health = pygame.image.load('images/full_health_bar.png')
        for i in draw_order:
            i[1][1].draw(screen)
            if i[2] == "UNIT":
                health_pct = int((i[1][1].current_health / i[1][1].max_health) * 100)
                if health_pct < 0:
                    health_pct = 0
                scaled_full_health = pygame.transform.scale(full_health, ((int(health_pct / 2)), 10))

                screen.blit(blank_health, ((int((i[1][1].x + (i[1][1].width / 2)) - 25)), int((i[1][1].y - 15))))
                screen.blit(scaled_full_health, ((int((i[1][1].x + (i[1][1].width / 2)) - 25)), int((i[1][1].y - 15))))

    def handle_ids(self):

        to_remove = []
        for die in self.dieing_ids:
            if die[0] > 5:
                self.all_ids.remove(die[1])
                to_remove.append(die)
            else:
                die[0] += 1
        for rem in to_remove:
            self.dieing_ids.remove(rem)

    def new_id(self):

        num = 0

        while True:
            if num in self.all_ids:
                num += 1
            else:
                self.all_ids.append(num)
                break

        return num

    def kill_id(self, num):

        self.dieing_ids.append([0, num])

    def new_unit(self, obj):

        uid = self.new_id()

        self.unit_list.append([uid, obj])

    def new_doodad(self, obj):

        did = self.new_id()

        self.doodad_list.append([did, obj])

    def new_other(self, obj):

        oid = self.new_id()

        self.other_list.append([oid, obj])

    def kill_unit(self, uid=None, obj=None):

        if uid is not None:

            obj = self.get_unit(uid=uid)[1]
            if obj:
                self.kill_id(uid)
                self.unit_list.remove([uid, obj])
                return True
            else:
                return False

        elif obj is not None:

            uid = self.get_unit(obj=obj)[0]
            if uid:
                self.kill_id(uid)
                self.unit_list.remove([uid, obj])
                return True
            else:
                return False

        else:

            return False

    def kill_doodad(self, did=None, obj=None):

        if did is not None:

            obj = self.get_doodad(did=did)[1]
            if obj:
                self.kill_id(did)
                self.doodad_list.remove([did, obj])
                return True
            else:
                return False

        elif obj is not None:

            did = self.get_doodad(obj=obj)[0]
            if did:
                self.kill_id(did)
                self.doodad_list.remove([did, obj])
                return True
            else:
                return False

        else:

            return False

    def kill_other(self, oid=None, obj=None):

        if oid is not None:

            obj = self.get_other(oid=oid)[1]
            if obj:
                self.kill_id(oid)
                self.other_list.remove([oid, obj])
                return True
            else:
                return False

        elif obj is not None:

            oid = self.get_other(obj=obj)[0]
            if oid:
                self.kill_id(oid)
                self.other_list.remove([oid, obj])
                return True
            else:
                return False

        else:

            return False


class Engine:

    def __init__(self):

        self.size = width, height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.black = 0, 0, 0

        self.obj_handler = ObjectHandler()
        self.obj_handler.new_unit(player.Player(50, 50))
        self.obj_handler.new_unit(bad_ball.BadBall(700, 50))
        self.obj_handler.new_unit(bad_ball.BadBall(600, 50))
        self.obj_handler.new_unit(bad_ball.BadBall(500, 50))
        self.obj_handler.new_unit(bad_ball.BadBall(400, 50))
        self.obj_handler.new_doodad(ground.Ground(0, 550))
        self.obj_handler.new_doodad(ground.Ground(200, 550))
        self.obj_handler.new_doodad(ground.Ground(400, 550))
        self.obj_handler.new_doodad(ground.Ground(600, 550))
        self.obj_handler.new_doodad(ground.Ground(100, 350))
        self.obj_handler.new_doodad(ground.Ground(200, 350))
        self.obj_handler.new_doodad(ground.Ground(100, 150))
        self.obj_handler.new_doodad(ground.Ground(500, 250))

        self.event_box = []

        self.main_loop()

    def main_loop(self):

        while True:

            self.clock.tick(30)
            self.screen.fill(self.black)

            for event in pygame.event.get():

                self.event_handler(event.type, event)

            self.obj_handler.handle_step(self.screen, self.event_box)

            pygame.display.flip()

    def event_handler(self, e_type, event):

        if e_type == pygame.QUIT:
            sys.exit()
        elif e_type == pygame.KEYDOWN:
            if event.key not in self.event_box:
                self.event_box.append(event.key)
        elif e_type == pygame.KEYUP:
            if event.key in self.event_box:
                    self.event_box.remove(event.key)


pygame.init()

eng = Engine()







