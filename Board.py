import pygame
from pygame import Color, Surface

from Enums import TileTypes
from Rooms import *
from Tile import Tile

class Board:
    def __init__(self, screen_width, screen_height, number_of_tiles, board_font):

        board_space = min(screen_width / 2, screen_height)
        self.tile_size = int(board_space / number_of_tiles)
        board_size = self.tile_size * number_of_tiles
        board_horizontal_margin = (screen_width / 2 - board_size) / 2
        board_vertical_margin = (screen_height - board_size) / 2
        self.board_top_left = (screen_width / 2 + board_horizontal_margin, board_vertical_margin)

        self.board = [[Tile(self.tile_size, x, y, self.board_top_left) for x in range(number_of_tiles)] for y in range(number_of_tiles)]

        self.rooms = [
            Kitchen(),
            DiningRoom(),
            Lounge(),
            Ballroom(),
            Center(),
            Hall(),
            Conservatory(),
            BilliardRoom(),
            Library(),
            Study()
        ]

        self.__add_blanks()
        self.__add_rooms()

        self.players = None
        self.board_font = board_font

    def __add_blanks(self):
        specific_blanks = [
            (1, 6),
            (1, 8),
            (1, 16),
            (1, 18),
            (7, 1),
            (7, 24),
            (9, 24),
            (10, 24),
            (11, 24),
            (12, 24),
            (13, 24),
            (14, 24),
            (15, 24),
            (16, 24),
            (18, 1),
            (18, 24),
            (24, 5),
            (24, 7),
            (24, 13),
            (24, 14),
            (24, 18),
            (24, 20)
        ]

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if (
                        (x == 0
                         or x == len(self.board[y]) - 1
                         or y == 0
                         or y == len(self.board) - 1
                         or (x, y) in specific_blanks
                        )
                        and ((x,y) not in [(10, 0), (15, 0)])
                ):
                    self.board[y][x].tile_type = TileTypes.EMPTY

    def __add_rooms(self):
        for room in self.rooms:
            for coord in room.locations:
                self.board[coord[1]][coord[0]].tile_type = TileTypes.ROOM
            for entrance in room.entrances:
                self.board[entrance[1]][entrance[0]].tile_type = TileTypes.ROOM_ENTRANCE
                self.board[entrance[1]][entrance[0]].entrance_direction = entrance[2]

    def __draw_walls(self, surface):
        for y in range(0, len(self.board)):
            for x in range(0, len(self.board[y])):
                current_tile = self.board[y][x]
                tile_size = current_tile.size
                left_x = current_tile.top_left_corner[0]
                top_y = current_tile.top_left_corner[1]
                top_left_corner = current_tile.top_left_corner
                top_right_corner = (left_x + tile_size, top_y)
                bottom_left_corner = (left_x, top_y + tile_size)
                bottom_right_corner = (left_x + tile_size, top_y + tile_size)
                border_width = 3

                if current_tile.tile_type != TileTypes.EMPTY and current_tile.tile_type != TileTypes.ROOM_ENTRANCE:
                    if y == 0 or self.__should_draw_wall(current_tile, self.board[y - 1][x], EntranceDirections.SOUTH):
                        pygame.draw.line(
                            surface,
                            Color(0, 0, 0),
                            top_left_corner,
                            top_right_corner,
                            border_width
                        )
                    if x == 0 or self.__should_draw_wall(current_tile, self.board[y][x - 1], EntranceDirections.EAST):
                        pygame.draw.line(
                            surface,
                            Color(0, 0, 0),
                            top_left_corner,
                            bottom_left_corner,
                            border_width
                        )
                    if y == len(self.board) - 1 or self.__should_draw_wall(current_tile, self.board[y + 1][x], EntranceDirections.NORTH):
                        pygame.draw.line(
                            surface,
                            Color(0, 0, 0),
                            bottom_left_corner,
                            bottom_right_corner,
                            border_width
                        )
                    if x == len(self.board[y]) - 1 or self.__should_draw_wall(current_tile, self.board[y][x + 1], EntranceDirections.WEST):
                        pygame.draw.line(
                            surface,
                            Color(0, 0, 0),
                            top_right_corner,
                            bottom_right_corner,
                            border_width
                        )

    def __should_draw_wall(self, current_tile, adjacent_tile, adjacent_tile_enter_from_direction):
        if adjacent_tile.tile_type == TileTypes.ROOM_ENTRANCE:
            if current_tile.tile_type == TileTypes.ROOM:
                return False
            else:
                return adjacent_tile_enter_from_direction != adjacent_tile.entrance_direction
        elif current_tile.tile_type != adjacent_tile.tile_type:
            return True
        else:
            return False

    def __draw_player(self, player, surface):
        tile = player.current_tile
        tile_center = (tile.top_left_corner[0] + (tile.size / 2), tile.top_left_corner[1] + (tile.size / 2))
        pygame.draw.circle(surface, player.color, tile_center, tile.size / 2.5)

    def draw_board_state(self, surface):
        for row in self.board:
            for tile in row:
                tile.draw(surface)

        for room in self.rooms:
            tile_drawing_over = self.board[room.center[1]][room.center[0]]
            text = self.board_font.render(room.name, True, Color("white"))
            text_rect = text.get_rect()
            text_rect.center = (tile_drawing_over.top_left_corner[0], tile_drawing_over.top_left_corner[1])
            surface.blit(text, text_rect)

        for player in self.players:
            self.__draw_player(player, surface)

        self.__draw_walls(surface)

    def get_move_candidates(self, start_tile, max_moves):
        #If player is in room check all posibilities from all entrances
        checked = []
        to_check = []

        if start_tile.tile_type == TileTypes.HALLWAY:
            to_check.append((start_tile.x, start_tile.y, 0))
        elif start_tile.tile_type == TileTypes.ROOM:
            room = self.__get_entrances_for_room(start_tile)
            for entrance in room.entrances:
                self.get_move_candidates(self.board[entrance[1]][entrance[0]], max_moves)
            return
        else:
            entry = start_tile.entrance_direction
            if entry == EntranceDirections.NORTH:
                to_check.append((start_tile.x, start_tile.y - 1, 1))
            elif entry == EntranceDirections.EAST:
                to_check.append((start_tile.x + 1, start_tile.y, 1))
            elif entry == EntranceDirections.SOUTH:
                to_check.append((start_tile.x, start_tile.y + 1, 1))
            elif entry == EntranceDirections.WEST:
                to_check.append((start_tile.x - 1, start_tile.y, 1))

        while len(to_check) != 0:
            tile = to_check.pop()
            checked.append(tile)

            x = tile[0]
            y = tile[1]

            up1 = y - 1
            down1 = y + 1
            left1 = x - 1
            right1 = x + 1

            # Don't check the tile we started from
            if ((x, y) != (start_tile.x, start_tile.y)) and not self.board[y][x].occupied:
                if self.board[y][x].tile_type == TileTypes.HALLWAY or self.board[y][x].tile_type == TileTypes.ROOM_ENTRANCE:
                    self.board[y][x].move_candidate = True
                else:
                    continue

            distance_moved_so_far = tile[2]
            if distance_moved_so_far + 1 > max_moves:
                continue

            if self.__check_direction(start_tile, left1, y, max_moves, EntranceDirections.EAST) and (left1, y, distance_moved_so_far + 1) not in checked:
                to_check.append((left1, y, distance_moved_so_far + 1))

            if self.__check_direction(start_tile, right1, y, max_moves, EntranceDirections.WEST) and (right1, y, distance_moved_so_far + 1) not in checked:
                to_check.append((right1, y, distance_moved_so_far + 1))

            if self.__check_direction(start_tile, x, up1, max_moves, EntranceDirections.SOUTH) and (x, up1, distance_moved_so_far + 1) not in checked:
                to_check.append((x, up1, distance_moved_so_far + 1))

            if self.__check_direction(start_tile, x, down1, max_moves, EntranceDirections.NORTH) and (x, down1, distance_moved_so_far + 1) not in checked:
                to_check.append((x, down1, distance_moved_so_far + 1))

    def __check_direction(self, start, new_x, new_y, max_moves, enter_direction):
        if 0 < new_y < len(self.board) and 0 < new_x < len(self.board[new_y]):
            if abs(new_x - start.x) + abs(new_y - start.y) <= max_moves and self.__is_viable_tile(start, self.board[new_y][new_x], enter_direction):
                return True

        return False

    def __get_room_for_entrance(self, tile):
        for room in self.rooms:
            for entrance in room.entrances:
                if (tile.x, tile.y) == (entrance[0], entrance[1]):
                    return room

        return None

    def __get_entrances_for_room(self, tile):
        for room in self.rooms:
            if tile.x in range(room.center[0] - 1, room.center[0] + 2) and tile.y in range(room.center[1], room.center[1] + 2):
                return room

        return None

    def __is_viable_tile(self, start, dest, enter_from_direction):
        if dest.tile_type == TileTypes.ROOM_ENTRANCE and dest.entrance_direction == enter_from_direction:
            if start.tile_type == TileTypes.HALLWAY or (start.tile_type == TileTypes.ROOM_ENTRANCE and self.__get_room_for_entrance(start) != self.__get_room_for_entrance(dest)):
                return True
        elif dest.tile_type == TileTypes.HALLWAY:
            return True
        else:
            return False

    def move_player_if_valid(self, player, pos):
        selected_tile = None
        for row in self.board:
            for tile in row:
                if tile.top_left_corner[0] <= pos[0] <= tile.top_left_corner[0] + tile.size and tile.top_left_corner[1] <= pos[1] <= tile.top_left_corner[1] + tile.size:
                    selected_tile = tile
                    break

        if selected_tile is None:
            return

        if selected_tile.move_candidate:
            player.current_tile.occupied = False
            if selected_tile.tile_type == TileTypes.ROOM_ENTRANCE:
                room = self.__get_room_for_entrance(selected_tile)
                room_center = room.center
                for y in range(2):
                    for x in range(-1, 2):
                        if not self.board[room_center[1] + y][room_center[0] + x].occupied:
                            fixed_pos = (room_center[0] + x, room_center[1] + y)
                            selected_tile = self.board[fixed_pos[1]][fixed_pos[0]]
                            break

            player.current_tile = selected_tile
            selected_tile.occupied = True

            for row in self.board:
                for tile in row:
                    tile.move_candidate = False
            return True
        else:
            return False