import pygame
import pygame.draw
import pygame.display
import pygame.time
import pygame.transform
import math
from pygame.locals import *
from utils import Point, Vector


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 800, 600
        self.max_square_size = 100
        self.root_pos_x = (self.width - self.max_square_size) / 2
        self.root_pos_y = 20
        self.loop_duration_ms = 3000
        self.max_list_size = 50

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self._running = False

    def on_loop(self):
        pass

    def render_root(self, pos):
        pygame.draw.rect(
            self._display_surf,
            (255, 0, 0),
            pos)

    def render_list(self, angle_rad: float, t_current: float, anchor_point: Point, step_index: int, size_parent: float, is_old_list: bool) -> None:
        if is_old_list == True:
            size_current = size_parent * math.cos(angle_rad)
        else:
            size_current = size_parent * math.sin(angle_rad)
        # No point in drawing invisible boxes
        if size_current < 1:
            return
        if step_index > self.max_list_size:
            return
        # Think of each box rotating around its anchor point. This is the value we use for actual rotation
        angle_rad_current = angle_rad * step_index
        # Calculate points in clockwise in the square, starting with the anchor point
        p1 = anchor_point
        p2 = p1 + Vector(size_current*math.cos(angle_rad_current+math.pi/2),
                         size_current*math.sin(angle_rad_current+math.pi/2))
        p3 = p2 + Vector(size_current*math.cos(angle_rad_current),
                         size_current*math.sin(angle_rad_current))
        p4 = p1 + Vector(size_current*math.cos(angle_rad_current),
                         size_current*math.sin(angle_rad_current))

        pygame.draw.polygon(
            self._display_surf,
            (0, 255, 0),
            [p1.to_tuple(), p2.to_tuple(), p3.to_tuple(), p4.to_tuple()])
        # p_ref = p2 if is_old_list else p3
        # self.render_list(angle_rad, t_current, p_ref,
        #                  step_index+1, size_current, is_old_list)

    def on_render(self, angle_rad, t_current):
        self._display_surf.fill((0, 0, 0))
        root_pos = (self.root_pos_x, self.root_pos_y,
                    self.max_square_size, self.max_square_size)
        self.render_root(root_pos)
        self.render_list(angle_rad, t_current,
                         Point(self.root_pos_x, self.root_pos_y+self.max_square_size), 1, self.max_square_size, True)
        self.render_list(angle_rad, t_current,
                         Point(self.root_pos_x+self.max_square_size, self.root_pos_y+self.max_square_size), 1, self.max_square_size, False)
        # Flip the Y-axis so we can have positive Y pointing upwards on the screen
        self._display_surf.blit(pygame.transform.flip(
            self._display_surf, False, True), (0, 0))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            # 0-1
            t_current = (pygame.time.get_ticks() %
                         self.loop_duration_ms)/self.loop_duration_ms
            angle_rad = t_current*math.pi/2
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render(angle_rad, t_current)
        self.on_cleanup()


if __name__ == "__main__":
    app = App()
    app.on_execute()
