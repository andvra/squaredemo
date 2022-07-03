import multiprocessing as mp
from typing import List
from squaredata import SquareData
import pygame
import array
import math
import pygame
import pygame.draw
import pygame.display
import pygame.time
import pygame.transform
import math
from pygame.locals import *
from utils import Point, Vector
from collections.abc import MutableSequence


def calculate_square_data(angle_rad: float, p1: Point, p4: Point):
    base_v = p4 - p1
    side_length = base_v.norm()
    scaled_normal = base_v.normals()[0].unit() * side_length
    p2 = p1+scaled_normal
    p3 = p4+scaled_normal
    new_side_length = math.cos(angle_rad) * side_length
    new_angle = base_v.angle() + angle_rad
    p5 = p2 + Vector(math.cos(new_angle),
                     math.sin(new_angle)) * new_side_length
    return SquareData(
        p1, p2, p3, p4, p5, new_side_length, new_angle)


def calculate_all_square_data(angle_rad: float, p1: Point, p4: Point, step_idx: int, idx: int, max_depth: int, a: MutableSequence[float]) -> None:
    """
    idx is given by parent
    """
    square_data = calculate_square_data(angle_rad, p1, p4)

    # No point in drawing invisible boxes
    if square_data.side_length < 1:
        return
    if step_idx > max_depth:
        return

    sd = square_data.as_array()
    # TODO: How to calculate array index?
    start_idx = idx * sd.count()
    end_idx = (idx+1) * sd.count()
    a[start_idx:end_idx] = sd
    # TODO: How to calculate IDX:es?
    idx_left = 0
    idx_right = 0
    calculate_square_data(
        angle_rad, square_data.p2, square_data.p5, step_idx+1, idx_left, max_depth, a)
    calculate_square_data(
        angle_rad, square_data.p5, square_data.p3, step_idx+1, idx_right, max_depth, a)


def multi_test_func(batchIdx: int, a: mp.Array):
    """
    This function can't be part of the class since that will require pickling the objects
    """
    # print(f"Process: {mp.current_process()} PID: {os.getpid()}")
    l = [(idx+batchIdx*10000, 123, [0.0, 1.1, 2.2, 3.3, 4.4])
         for idx in range(10000)]
    start_idx = batchIdx*10000
    end_idx = (batchIdx+1)*10000
    list_as_array = array.array('f', list(map(lambda x: x[1], l)))
    a[start_idx:end_idx] = list_as_array


class App2:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 480
        self.max_square_size = 100
        self.root_pos_x = (self.width - self.max_square_size) / 2
        self.root_pos_y = 20
        self.min_square_size = 1
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

    def render_list(self, angle_rad: float, p1: Point, p4: Point, step_index: int, do_draw=True) -> None:
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
        if do_draw:
            pygame.draw.polygon(
                self._display_surf,
                self.square_colors[(step_index-1) % len(self.square_colors)],
                [p1.to_tuple(), p2.to_tuple(), p3.to_tuple(), p4.to_tuple()])

        self.render_list(angle_rad, p2, p5, step_index+1, do_draw)
        self.render_list(angle_rad, p5, p3, step_index+1, do_draw)

    def on_render(self, angle_rad, do_draw=True):
        self._display_surf.fill((0, 0, 0))
        self.render_list(angle_rad, Point(self.root_pos_x, self.root_pos_y), Point(
            self.root_pos_x+self.max_square_size, self.root_pos_y), 1, do_draw)
        # Flip the Y-axis so we can have positive Y pointing upwards on the screen
        self._display_surf.blit(pygame.transform.flip(
            self._display_surf, False, True), (0, 0))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def get_splits(self, num_splits: int, angle_rad: float, array: MutableSequence[float]) -> List[SquareData]:
        """
        To get the splits, we only need to consider the square size at each step; a larger square size will have more childs.
        After getting the nodes where the split is to be made, make sure to:

        1. Add them and their parents to the list of squares to draw
        2. Get input parameters for the childs

        Continue down the tree a maximum of num_processes/2 steps.
        """
        class SquareInTree(object):
            __slots__ = ["square", "can_branch"]

            def __init__(self, square: SquareData, can_branch: bool):
                self.square = square
                self.can_branch = can_branch

        squares: List[SquareInTree] = []
        square_data_root = calculate_square_data(angle_rad, Point(self.root_pos_x, self.root_pos_y), Point(
            self.root_pos_x+self.max_square_size, self.root_pos_y))
        squares.append(SquareInTree(square_data_root, True))

        done = False
        while not done:
            # If there are multiple squares with the same side length, the first one will be picked
            largest_square = max(
                squares, key=lambda s: s.can_branch*s.square.side_length)
            largest_square.can_branch = False
            done = True
            # TODO: Continue here. Add all squares to the array. Also, return all the squares that has can_branch = True, which is the initial state going further.
            # Keep an array with pre-allocated tuple <SquareData, do_draw>. Add to this list and set do_draw=True based on index. For each iteration, start of
            #   with setting do_draw=False. Then, when drawing, loop over this array and only care for the ones where do_draw=True. Simple :)

        return squares

    def on_execute(self):
        max_num_processes_to_use = 8
        num_processes_to_use = min(max_num_processes_to_use, mp.cpu_count())
        print(f'Running with {num_processes_to_use} processes')
        if self.on_init() == False:
            self._running = False
        # We will limit the depth of our tree to 50, so the maximum number of squares is when angle = pi/4.
        depth_when_max_squares = math.ceil(math.log10(
            self.min_square_size/self.max_square_size)/math.log10(math.cos(math.pi/4)))
        # Rounded up to closest even tree depth
        max_squares = 2**depth_when_max_squares
        with mp.Pool(num_processes_to_use) as pool:
            manager = mp.Manager()
            array = manager.Array('f', [0 for _ in range(max_squares)])
            while(self._running):
                # 0-1
                t_current = (pygame.time.get_ticks() %
                             self.loop_duration_ms)/self.loop_duration_ms
                angle_rad = t_current*math.pi/2
                #splits = self.get_splits(
                #    num_processes_to_use, angle_rad, array)
                # TODO: Add the game loop here. Get splits in each iteration. Then run starmap() with the branches as arguments
                #pool.starmap(multi_test_func, [
                #    (batchIdx, array) for batchIdx in range(8)])
                # TODO: Our array will now hold the values we need.
                # What about encoding it, like [idx, data1, data2] directly in the array? Maging in max_square*num_bits long
                for event in pygame.event.get():
                    self.on_event(event)
                self.on_render(angle_rad)
        self.on_cleanup()


if __name__ == "__main__":
    app = App2()
    # splits = app.get_splits(8, math.pi/6)
    # a: bool
    # b: SquareData
    # for a, b in splits:
    #     print(b.as_array())

    app.on_execute()
