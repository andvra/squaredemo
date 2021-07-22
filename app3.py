import pygame
import pygame.draw
import pygame.display
import pygame.time
import pygame.transform
import math
from pygame.locals import *
from utils import Point, Vector


class App3:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 480
        self.max_square_size = 100
        self.root_pos_x = (self.width - self.max_square_size) / 2
        self.root_pos_y = 20
        self.loop_duration_ms = 3000
        self.max_list_size = 15
        self.square_colors = [
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 0, 255)
        ]

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

    def render_square(self, angle_rad: float, seq: list[bool], start_pos: Point):
        # false = left, true = right
        step = len(seq)
        num_left = seq.count(False)
        num_right = seq.count(True)
        new_angle = step*angle_rad-num_right*math.pi/2
        side_length = self.max_square_size * \
            (math.cos(angle_rad)**num_left)*(math.sin(angle_rad)**num_right)
        if step > 1:
            cur_side_length = self.max_square_size
            cur_num_right = 0
            for i, v in enumerate(seq):
                if seq[i] == True:
                    cur_num_right = cur_num_right + 1
                if seq[i] == False:
                    cur_side_length = cur_side_length*math.cos(angle_rad)
                else:
                    cur_side_length = cur_side_length*math.sin(angle_rad)
                cur_angle = (i+1)*angle_rad-cur_num_right*math.pi/2
                if i > 0:
                    if seq[i-1] == False and seq[i] == False:   # Parent left, current left
                        start_pos = Point(
                            start_pos.X + cur_side_length *
                            math.sin(cur_angle+math.pi/2),
                            start_pos.Y + cur_side_length *
                            math.cos(cur_angle))
                    elif seq[i-1] == False and seq[i] == True:  # Parent left, current right
                        start_pos = Point(
                            start_pos.X + cur_side_length *
                            math.cos(cur_angle),
                            start_pos.Y + cur_side_length *
                            math.sin(cur_angle))
                    elif seq[i-1] == True and seq[i] == False:  # Parent right, current left
                        start_pos = Point(
                            start_pos.X + cur_side_length *
                            math.cos(cur_angle + math.pi/2),
                            start_pos.Y + cur_side_length *
                            math.sin(cur_angle + math.pi/2))
                    elif seq[i-1] == True and seq[i] == True:  # Parent right, current right
                        start_pos = Point(
                            start_pos.X + cur_side_length *
                            math.cos(cur_angle + math.pi/2 +
                                     math.cos(angle_rad)*cur_side_length *
                                     math.cos(cur_angle+angle_rad)
                                     ),
                            start_pos.Y + cur_side_length *
                            math.sin(cur_angle + math.pi/2 +
                                     math.cos(angle_rad)*cur_side_length *
                                     math.sin(cur_angle+angle_rad))
                        )
        pygame.draw.rect(
            self._display_surf,
            self.square_colors[(step-1) % len(self.square_colors)],
            Rect(start_pos.X, start_pos.Y, side_length, side_length)
        )

    def render_list(self, angle_rad: float, p1: Point, p4: Point, step_index: int) -> None:
        base_v = p4 - p1
        side_length = base_v.norm()
        scaled_normal = base_v.normals()[0].unit()*side_length
        p2 = p1+scaled_normal
        p3 = p4+scaled_normal
        new_side_length = math.cos(angle_rad)*side_length
        new_angle = base_v.angle()+angle_rad
        p5 = p2 + Vector(math.cos(new_angle),
                         math.sin(new_angle))*new_side_length

        # No point in drawing invisible boxes
        if side_length < 1:
            return
        if step_index > self.max_list_size:
            return
        # Think of each box rotating around its anchor point. This is the value we use for actual rotation
        angle_rad_current = angle_rad * step_index

        pygame.draw.polygon(
            self._display_surf,
            self.square_colors[(step_index-1) % len(self.square_colors)],
            [p1.to_tuple(), p2.to_tuple(), p3.to_tuple(), p4.to_tuple()])

        self.render_list(angle_rad, p2, p5, step_index+1)
        self.render_list(angle_rad, p5, p3, step_index+1)

    def on_render(self, angle_rad):
        self._display_surf.fill((0, 0, 0))
        self.render_square(angle_rad, [False], Point(100, 100))
        self.render_square(angle_rad, [True], Point(300, 100))
        self.render_square(angle_rad, [False, False], Point(100, 100))
        self.render_square(angle_rad, [False, True], Point(100, 100))
        # root_pos = (self.root_pos_x, self.root_pos_y,
        #             self.max_square_size, self.max_square_size)
        # self.render_list(angle_rad, Point(self.root_pos_x, self.root_pos_y), Point(
        #     self.root_pos_x+self.max_square_size, self.root_pos_y), 1)
        # self.render_list(angle_rad, Point(self.root_pos_x, self.root_pos_y), Point(
        #     self.root_pos_x+self.max_square_size, self.root_pos_y), 1)
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
            self.on_render(angle_rad)
        self.on_cleanup()


if __name__ == "__main__":
    app = App3()
    app.on_execute()
