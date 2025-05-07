import pygame as pg
import asyncio
import platform
import random
import math

# Game Configuration
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 672
FPS = 60
TILE_SIZE = 48
PIXEL_SCALE = 3

# Physics Constants
GRAVITY = 0.8
PLAYER_ACCEL = 0.8
PLAYER_FRICTION = -0.15
PLAYER_MAX_SPEED_X = 6
PLAYER_JUMP_POWER = 17
PLAYER_SUPER_JUMP_POWER = 18
MAX_FALL_SPEED = 15
ENEMY_MOVE_SPEED = 1
KOOPA_SHELL_SPEED = 8

# Player states
PLAYER_STATE_SMALL = "small"
PLAYER_STATE_SUPER = "super"
PLAYER_STATE_RACCOON = "raccoon"

# SMB3 Color Map
TRANSPARENT_CHAR = 'T'
SMB3_COLOR_MAP = {
    'T': (0,0,0,0), 'R': (220, 0, 0), 'B': (0, 80, 200), 'S': (255, 200, 150),
    'Y': (255, 240, 30), 'O': (210, 120, 30), 'o': (160, 80, 20), 'K': (10, 10, 10),
    'W': (250, 250, 250), 'G': (0, 180, 0), 'g': (140, 70, 20), 'N': (130, 80, 50),
    'n': (80, 50, 30), 'L': (90, 200, 255), 'F': (100, 200, 50), 'X': (190, 190, 190),
    'D': (60, 60, 60), 'U': (180, 100, 60), 'M': (255, 100, 90), 'm': (240, 230, 210),
    'k': (0, 100, 0), 'y': (255,255,150)
}
color_map = SMB3_COLOR_MAP
BACKGROUND_COLOR = color_map['L']

# SMB3 Asset Definitions (unchanged, included for completeness)
SMB3_MARIO_SMALL_IDLE_R_ART = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKRTTTTTT", "TTKSRSRSKRTTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTBBBBBBBBTTTTTT", "TTBBRBBBRBTTTTTT",
    "TTTRRnnRRTTTTTTT", "TTTRnnnnRTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_MARIO_SMALL_WALK_R_ART_1 = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKRTTTTTT", "TTKSRSRSKRTTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTBBBBBBBBTTTTTT", "TTBBRBBBRBTTTTTT",
    "TTTRRTRnRTTTTTTT", "TTTRnnnnRTTTTTTT", "TTTTTTnnTTTTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_MARIO_SMALL_WALK_R_ART_2 = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKRTTTTTT", "TTKSRSRSKRTTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTBBBBBBBBTTTTTT", "TTBBRBBBRBTTTTTT",
    "TTTRRnnRRTTTTTTT", "TTTRTRTRRTTTTTTT", "TTTTTTnnTTTTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_MARIO_SMALL_JUMP_R_ART = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKBBTTTTT", "TTKSRSRSKBBTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTBBBBBBBBTTTTTT", "TTBBRBBBRBTTTTTT",
    "TTTTRnRTRTTTTTTT", "TTTTRnRnRTTTTTTT", "TTTTnnTTnnTTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_MARIO_SUPER_IDLE_R_ART = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKRTTTTTT", "TTKSRSRSKRTTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTTRRBBBRRTTTTTT", "TTTRBBBBBRTTTTTT",
    "TTTRBBBBBRTTTTTT", "TTTRBBBBBRTTTTTT", "TTBBBBBBBBBBTTTT", "TTBBBBBBBBBBTTTT",
    "TTTTRRRRRRTTTTTT", "TTTTnnnnnnTTTTTT", "TTTTnnnnnnTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_MARIO_SUPER_WALK_R_ART_1 = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKRTTTTTT", "TTKSRSRSKRTTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTTRRBBBRRTTTTTT", "TTTRBBBBBRTTTTTT",
    "TTTRBBBBBRTTTTTT", "TTTRBBBBBRTTTTTT", "TTBBBBBBBBBBTTTT", "TTBBRBBBRBBTTTTT",
    "TTTTTRRRnRTTTTTT", "TTTTTnnnnnTTTTTT", "TTTTTnnnnnTTTTTT", "TTTTTTTnnTTTTTTT"
]
SMB3_MARIO_SUPER_WALK_R_ART_2 = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKRTTTTTT", "TTKSRSRSKRTTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTTRRBBBRRTTTTTT", "TTTRBBBBBRTTTTTT",
    "TTTRBBBBBRTTTTTT", "TTTRBBBBBRTTTTTT", "TTBBBBBBBBBBTTTT", "TTBBBRBBBRBTTTTT",
    "TTTTTRnnRRTTTTTT", "TTTTTnnnnnTTTTTT", "TTTTTnnnnnTTTTTT", "TTTTTTTnnTTTTTTT"
]
SMB3_MARIO_SUPER_JUMP_R_ART = [
    "TTTTTRRRRTTTTTTT", "TTTTRRRRRRTTTTTT", "TTTKKSSSKBBTTTTT", "TTKSRSRSKBBTTTTT",
    "TTKSSSSSKRTTTTTT", "TTTKRKRRKTTTTTTT", "TTTRRBBBRBTTTTTT", "TTTRBBBBBBTTTTTT",
    "TTTRBBBBBBTTTTTT", "TTTRBBBBBBTTTTTT", "TTBBBBBBBBBBTTTT", "TTBBBBBBBBBBTTTT",
    "TTTTTRnRTRTTTTTT", "TTTTTRnRnRTTTTTT", "TTTTnnTTnnTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_GOOMBA_WALK1_ART = [
    "TTTTNNNNNNTTTTTT", "TTTNNNNNNNNTTTTT", "TTNNWWKKWWNNTTTT", "TTNKKWWWWKKNNTTT",
    "TTNNNNNNNNNNTTTT", "TTNNNNNNNNNNNNTT", "TTTNNNNNNNNTTTTT", "TTTTNNNNNNTTTTTT",
    "TTTTTnnnnTTTTTTT", "TTTTNnnnnNTTTTTT", "TTTNNNNNNNNTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_GOOMBA_WALK2_ART = [
    "TTTTNNNNNNTTTTTT", "TTTNNNNNNNNTTTTT", "TTNNWWKKWWNNTTTT", "TTNKKWWWWKKNNTTT",
    "TTNNNNNNNNNNTTTT", "TTNNNNNNNNNNNNTT", "TTTNNNNNNNNTTTTT", "TTTTNNNNNNTTTTTT",
    "TTTTnnNNnnTTTTTT", "TTTTNnnnnNTTTTTT", "TTTNNNNNNNNTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_GOOMBA_SQUISHED_ART = [
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTNNNNNNTTTTTT",
    "TTTNNNNNNNNTTTTT", "TTNNWWKKWWNNTTTT", "TTNKKWWWWKKNNTTT", "TTNNNNNNNNNNTTTT",
    "TTNNNNNNNNNNNNTT", "TTTNNNNNNNNTTTTT", "TTTTNNNNNNTTTTTT", "TTTTTnnnnTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_KOOPA_WALK1_R_ART = [
    "TTTTTGGGGTTTTTTT", "TTTTGGGGGGTTTTTT", "TTTGGkkGGGGTTTTT", "TTGGkWWkkyyGTTTT",
    "TTGkWKKkWyyGGTTT", "TTGkyyyykWWGTTTT", "TTGkyyyykKKGGTTT", "TTGkyyyykWWGGTTT",
    "TTTGGkyyGGGGTTTT", "TTTTGGGGGGykTTTT", "TTTTTyyGGyyTTTTT", "TTTTTyyTTyyTTTTT",
    "TTTTyyTTTTTyyTTT", "TTTTnnTTTTTnnTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_KOOPA_WALK2_R_ART = [
    "TTTTTGGGGTTTTTTT", "TTTTGGGGGGTTTTTT", "TTTGGkkGGGGTTTTT", "TTGGkWWkkyyGTTTT",
    "TTGkWKKkWyyGGTTT", "TTGkyyyykWWGTTTT", "TTGkyyyykKKGGTTT", "TTGkyyyykWWGGTTT",
    "TTTGGkyyGGGGTTTT", "TTTTGGGGGGykTTTT", "TTTTTyyGGyyTTTTT", "TTTTyyTTyyTTTTTT",
    "TTTnnTTyyTTTTTTT", "TTTTTTTTnnTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_KOOPA_SHELL_ART = [
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTGGGGTTTTTTT", "TTTTGGGGGGTTTTTT",
    "TTTGGkkGGGGTTTTT", "TTGGkyyykyyGTTTT", "TTGkyyyyyyyGGTTT", "TTGkyyyyyyyGGTTT",
    "TTGGkyyykyyGTTTT", "TTTGGkkGGGGTTTTT", "TTTTGGGGGGTTTTTT", "TTTTTGGGGTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_BRICK_BLOCK_ART = [
    "OOOOOOOOOOOOOOOO", "OKKOoKKOoKKOoKKO", "OOOOOOOOOOOOOOOO", "OoKKOoKKOoKKOoKK",
    "OOOOOOOOOOOOOOOO", "OKKOoKKOoKKOoKKO", "OOOOOOOOOOOOOOOO", "OoKKOoKKOoKKOoKK",
    "OOOOOOOOOOOOOOOO", "OKKOoKKOoKKOoKKO", "OOOOOOOOOOOOOOOO", "OoKKOoKKOoKKOoKK",
    "OOOOOOOOOOOOOOOO", "OKKOoKKOoKKOoKKO", "OOOOOOOOOOOOOOOO", "oooooooooooooooo"
]
SMB3_BRICK_DEBRIS_ART = [
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTToOTTTTTTTT", "TTTTToooOTTTTTTT",
    "TTTTTooootTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_QUESTION_BLOCK_ART_FRAME1 = [
    "YYYYYYYYYYYYYYYY", "YXWYYYYYYYWXYYYY", "YWKKWYYYYYWKKYWY", "YTWKKWYYYWKKWTYY",
    "YTTWKKWWKKWTTTYY", "YTTTWKWWKWTTTTYY", "YTTTTWWWWTTTTTYY", "YTTTTWKKWTTTTTYY",
    "YTTTTWKKWTTTTTYY", "YTTTTWWWWTTTTTYY", "YXTTKWKKWKTTTXYY", "YWWWWKKKKWWWWWYW",
    "YYYYYYYYYYYYYYYY", "YXXXXXXXXXXXXXXY", "YooooooooooooooY", "oooooooooooooooo"
]
SMB3_QUESTION_BLOCK_ART_FRAME2 = [
    "YYYYYYYYYYYYYYYY", "YXWYYYYYYYWXYYYY", "YWKKYYYYYYWKKYWY", "YTWKKWYYYWKKWTYY",
    "YTTWKKWWKKWTTTYY", "YTTTWKWWKWTTTTYY", "YTTTTWKKWTTTTTYY", "YTTTTWKKWTTTTTYY",
    "YTTTTWWWWTTTTTYY", "YTTTTWWWWTTTTTYY", "YXTTKWWWWKTTTXYY", "YWWWWKKKKWWWWWYW",
    "YYYYYYYYYYYYYYYY", "YXXXXXXXXXXXXXXY", "YooooooooooooooY", "oooooooooooooooo"
]
SMB3_USED_BLOCK_ART = [
    "UUUUUUUUUUUUUUUU", "UooUooUooUooUooU", "UooUooUooUooUooU", "UUUUUUUUUUUUUUUU",
    "UooUooUooUooUooU", "UooUooUooUooUooU", "UUUUUUUUUUUUUUUU", "UooUooUooUooUooU",
    "UooUooUooUooUooU", "UUUUUUUUUUUUUUUU", "UooUooUooUooUooU", "UooUooUooUooUooU",
    "UUUUUUUUUUUUUUUU", "UooUooUooUooUooU", "UooUooUooUooUooU", "oooooooooooooooo"
]
SMB3_GROUND_BLOCK_ART = [
    "gggggggggggggggg", "gOgOgOgOgOgOgOgO", "gOgOgOgOgOgOgOgO", "gggggggggggggggg",
    "gggggggggggggggg", "gggggggggggggggg", "DDDDDDDDDDDDDDDD", "DDDDDDDDDDDDDDDD",
    "gggggggggggggggg", "gOgOgOgOgOgOgOgO", "gOgOgOgOgOgOgOgO", "gggggggggggggggg",
    "gggggggggggggggg", "gggggggggggggggg", "DDDDDDDDDDDDDDDD", "DDDDDDDDDDDDDDDD"
]
SMB3_SUPER_LEAF_ART = [
    "TTTTTTGGTTTTTTTT", "TTTTTGGGGTTTTTTT", "TTTTGGGGGGTTTTTT", "TTTGGFFFFFFGTTTT",
    "TTGGFFFFFFFFGTTT", "TTGFFFFgFFFFFGTT", "TTGFFFggFFFFFGTT", "TTGFFFggFFFFFGTT",
    "TTTGFFggggFFGTTT", "TTTTGFFggFFGTTTT", "TTTTTGFFGGTTTTTT", "TTTTTTGggGTTTTTT",
    "TTTTTTTggTTTTTTT", "TTTTTTTggTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_MUSHROOM_ART = [
    "TTTTTMMMMMMTTTTT", "TTTTMMMMMMMMTTTT", "TTTMMmMMMmMMMTTT", "TTMmWWmWWmWWMMTT",
    "TTMWWWWWWWWWMMTT", "TTMWWWWWWWWWMMTT", "TTMMWWWWWWMMMMTT", "TTTMMMMMMMMMTTTT",
    "TTTTTmmmmTTTTTTT", "TTTTmmKKmmTTTTTT", "TTTTmmWWmmTTTTTT", "TTTTmmmmmmTTTTTT",
    "TTTTTmmmmTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT", "TTTTTTTTTTTTTTTT"
]
SMB3_FLAGPOLE_ART = [
    "TTTTTTTTXTTTTTTT", "TTTTTTGGGXTTTTTT", "TTTTTGGGGGXTTTTT", "TTTTGGGGGGXTTTTT",
    "TTTGGGGGGGXTTTTT", "TTTTGGGGGXTTTTTT", "TTTTTTGGGXTTTTTT", "TTTTTTTTXTTTTTTT",
    "TTTTTTTTXTTTTTTT", "TTTTTTTTXTTTTTTT", "TTTTTTTTXTTTTTTT", "TTTTTTTTXTTTTTTT",
    "TTTTTTTTXTTTTTTT", "TTTTTTTTXTTTTTTT", "TTTTTTTTXTTTTTTT", "TTTTTTTTXTTTTTTT"
]

# SNES-like Graphics Functions
def build_sprite_palette(pixel_art_rows):
    palette = [(0,0,0,0)]
    unique_colors_in_art = set()
    for row in pixel_art_rows:
        for char_code in row:
            if char_code != TRANSPARENT_CHAR and char_code in color_map:
                unique_colors_in_art.add(color_map[char_code])
    palette.extend(sorted(unique_colors_in_art, key=lambda c: (c[0], c[1], c[2])))
    return palette

def create_snes_tile_indices(pixel_art_rows, palette):
    tile_indices = []
    for row_str in pixel_art_rows:
        indices_for_row = []
        for char_code in row_str:
            if char_code == TRANSPARENT_CHAR:
                indices_for_row.append(0)
            else:
                actual_color_tuple = color_map.get(char_code)
                if actual_color_tuple and actual_color_tuple in palette:
                    indices_for_row.append(palette.index(actual_color_tuple))
                else:
                    indices_for_row.append(0)
        tile_indices.append(indices_for_row)
    return tile_indices

def draw_snes_tile_indexed(screen, tile_indices, palette, x, y, scale):
    for r_idx, row_of_indices in enumerate(tile_indices):
        for c_idx, palette_idx in enumerate(row_of_indices):
            if palette_idx != 0:
                color_tuple = palette[palette_idx]
                pg.draw.rect(screen, color_tuple, (x + c_idx * scale, y + r_idx * scale, scale, scale))

def flip_pixel_art(pixel_art_rows):
    return ["".join(reversed(row)) for row in pixel_art_rows]

# Classes
class AnimatedSprite(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_frames = {}
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.image_scale = PIXEL_SCALE
        self.state = "idle"
        self.facing_left = False

    def load_animation_frames(self, action_name, frame_art_list_right):
        key_r = f"{action_name}_right"
        processed_frames_r = []
        for art_strings in frame_art_list_right:
            palette = build_sprite_palette(art_strings)
            indices = create_snes_tile_indices(art_strings, palette)
            processed_frames_r.append((indices, palette))
        self.animation_frames[key_r] = processed_frames_r
        key_l = f"{action_name}_left"
        processed_frames_l = []
        for art_strings in frame_art_list_right:
            flipped_art_strings = flip_pixel_art(art_strings)
            palette = build_sprite_palette(flipped_art_strings)
            indices = create_snes_tile_indices(flipped_art_strings, palette)
            processed_frames_l.append((indices, palette))
        self.animation_frames[key_l] = processed_frames_l

    def get_current_animation_set(self):
        direction = "left" if self.facing_left else "right"
        state_prefix = ""
        if hasattr(self, 'player_form') and self.player_form:
            state_prefix = f"{self.player_form}_"
        key = f"{state_prefix}{self.state}_{direction}"
        default_key_direction = f"{state_prefix}idle_{direction}"
        default_key_universal = f"{state_prefix}idle_right"
        return (self.animation_frames.get(key) or
                self.animation_frames.get(default_key_direction) or
                self.animation_frames.get(default_key_universal) or
                self.animation_frames.get("idle_right", [([[]], [(0,0,0,0)])]))

    def update_animation(self, dt):
        self.animation_timer += dt * FPS * self.animation_speed
        current_animation_set = self.get_current_animation_set()
        if not current_animation_set or not current_animation_set[0][0]:
            return
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(current_animation_set)

    def draw(self, screen, camera_offset_x, camera_offset_y):
        current_animation_set = self.get_current_animation_set()
        if not current_animation_set or not current_animation_set[0][0]:
            return
        if self.current_frame_index >= len(current_animation_set):
            self.current_frame_index = 0
        tile_indices, palette = current_animation_set[self.current_frame_index]
        if not tile_indices:
            return
        draw_y = self.rect.y - camera_offset_y
        if hasattr(self, 'player_form') and self.player_form == PLAYER_STATE_SUPER:
            pass
        draw_snes_tile_indexed(screen, tile_indices, palette,
                               self.rect.x - camera_offset_x,
                               draw_y,
                               self.image_scale)

class Player(AnimatedSprite):
    def __init__(self, game, x_tile, y_tile):
        super().__init__()
        self.game = game
        self.pos = pg.math.Vector2(x_tile * TILE_SIZE, y_tile * TILE_SIZE)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.player_form = PLAYER_STATE_SMALL
        self.set_form(PLAYER_STATE_SMALL, initial_load=True)
        self.on_ground = False
        self.can_jump = True
        self.score = 0
        self.lives = 3
        self.invincible_timer = 0
        self.invincibility_duration = FPS * 2
        self.blink_timer = 0

    def set_form(self, new_form, initial_load=False):
        old_bottom = self.rect.bottom if hasattr(self, 'rect') and not initial_load else self.pos.y + TILE_SIZE
        self.player_form = new_form
        self.animation_frames = {}
        if self.player_form == PLAYER_STATE_SMALL:
            self.art_height_chars = 16
            self.player_height_tiles = 1
            self.load_animation_frames(f"{PLAYER_STATE_SMALL}_idle", [SMB3_MARIO_SMALL_IDLE_R_ART])
            self.load_animation_frames(f"{PLAYER_STATE_SMALL}_walk", [SMB3_MARIO_SMALL_WALK_R_ART_1, SMB3_MARIO_SMALL_WALK_R_ART_2])
            self.load_animation_frames(f"{PLAYER_STATE_SMALL}_jump", [SMB3_MARIO_SMALL_JUMP_R_ART])
        elif self.player_form == PLAYER_STATE_SUPER:
            self.art_height_chars = 16
            self.player_height_tiles = 2
            self.load_animation_frames(f"{PLAYER_STATE_SUPER}_idle", [SMB3_MARIO_SUPER_IDLE_R_ART])
            self.load_animation_frames(f"{PLAYER_STATE_SUPER}_walk", [SMB3_MARIO_SUPER_WALK_R_ART_1, SMB3_MARIO_SUPER_WALK_R_ART_2])
            self.load_animation_frames(f"{PLAYER_STATE_SUPER}_jump", [SMB3_MARIO_SUPER_JUMP_R_ART])
        current_x = self.pos.x
        new_height_pixels = self.player_height_tiles * TILE_SIZE
        self.rect = pg.Rect(current_x, old_bottom - new_height_pixels, TILE_SIZE, new_height_pixels)
        self.pos.x = self.rect.x
        self.pos.y = self.rect.y
        self.current_frame_index = 0

    def jump(self):
        if self.on_ground:
            jump_power = PLAYER_SUPER_JUMP_POWER if self.player_form != PLAYER_STATE_SMALL else PLAYER_JUMP_POWER
            self.vel.y = -jump_power
            self.on_ground = False
            self.can_jump = False

    def take_damage(self):
        if self.invincible_timer > 0:
            return False
        if self.player_form == PLAYER_STATE_SUPER:
            self.set_form(PLAYER_STATE_SMALL)
            self.invincible_timer = self.invincibility_duration
            return True
        elif self.player_form == PLAYER_STATE_SMALL:
            self.die()
            return True
        return False

    def update(self, dt, platforms):
        self.acc = pg.math.Vector2(0, GRAVITY)
        keys = pg.key.get_pressed()
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            self.blink_timer = (self.blink_timer + 1) % 10
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCEL
            self.facing_left = True
        elif keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACCEL
            self.facing_left = False
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel.x += self.acc.x
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.vel.x = max(-PLAYER_MAX_SPEED_X, min(self.vel.x, PLAYER_MAX_SPEED_X))
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        self.collide_with_platforms_x(platforms)
        if keys[pg.K_SPACE]:
            if self.can_jump and self.on_ground:
                self.jump()
        else:
            self.can_jump = True
        self.vel.y += self.acc.y
        self.vel.y = min(self.vel.y, MAX_FALL_SPEED)
        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)
        self.on_ground = False
        self.collide_with_platforms_y(platforms)
        if not self.on_ground:
            self.state = "jump"
        elif abs(self.vel.x) > 0.1:
            self.state = "walk"
        else:
            self.state = "idle"
        self.update_animation(dt)
        if self.rect.top > SCREEN_HEIGHT + TILE_SIZE * 2:
            self.die()

    def collide_with_platforms_x(self, platforms):
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel.x > 0:
                    self.rect.right = plat.rect.left
                    self.vel.x = 0
                elif self.vel.x < 0:
                    self.rect.left = plat.rect.right
                    self.vel.x = 0
                self.pos.x = self.rect.x

    def collide_with_platforms_y(self, platforms):
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel.y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = plat.rect.bottom
                    self.vel.y = 0
                    if hasattr(plat, 'hit_from_bottom'):
                        plat.hit_from_bottom(self)
                self.pos.y = self.rect.y

    def die(self):
        self.lives -= 1
        if self.lives > 0:
            self.game.reset_level_soft()
        else:
            self.game.game_over = True

    def draw(self, screen, camera_offset_x, camera_offset_y):
        if self.invincible_timer > 0 and self.blink_timer < 5:
            return
        super().draw(screen, camera_offset_x, camera_offset_y)

class Particle(AnimatedSprite):
    def __init__(self, game, x, y, art_frames, vel_x, vel_y, lifetime_frames):
        super().__init__()
        self.game = game
        self.pos = pg.math.Vector2(x, y)
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE // 2, TILE_SIZE // 2)
        self.load_animation_frames("idle", art_frames)
        self.vel = pg.math.Vector2(vel_x, vel_y)
        self.lifetime = lifetime_frames
        self.animation_speed = 0

    def update(self, dt, platforms):
        self.vel.y += GRAVITY / 2
        self.pos += self.vel
        self.rect.topleft = self.pos
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Block(AnimatedSprite):
    def __init__(self, game, x_tile, y_tile, art_frames_list, solid=True, block_type="generic"):
        super().__init__()
        self.game = game
        self.pos = pg.math.Vector2(x_tile * TILE_SIZE, y_tile * TILE_SIZE)
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.load_animation_frames("idle", art_frames_list)
        self.solid = solid
        self.block_type = block_type
        self.animation_speed = 0

    def update(self, dt):
        if self.animation_speed > 0:
            self.update_animation(dt)

class BrickBlock(Block):
    def __init__(self, game, x_tile, y_tile):
        super().__init__(game, x_tile, y_tile, [SMB3_BRICK_BLOCK_ART], solid=True, block_type="brick")

    def hit_from_bottom(self, player):
        if player.player_form != PLAYER_STATE_SMALL:
            self.game.spawn_particles(self.rect.centerx, self.rect.top)
            self.kill()
            player.score += 50
        else:
            pass

class QuestionBlock(Block):
    def __init__(self, game, x_tile, y_tile, contains="mushroom"):
        super().__init__(game, x_tile, y_tile,
                         [SMB3_QUESTION_BLOCK_ART_FRAME1, SMB3_QUESTION_BLOCK_ART_FRAME2],
                         solid=True, block_type="qblock")
        self.is_active = True
        self.animation_speed = 0.05
        self.contains = contains

    def hit_from_bottom(self, player):
        if self.is_active:
            self.is_active = False
            self.animation_speed = 0
            self.load_animation_frames("idle", [SMB3_USED_BLOCK_ART])
            self.current_frame_index = 0
            item_to_spawn = None
            if player.player_form == PLAYER_STATE_SMALL:
                item_to_spawn = Mushroom(self.game, self.pos.x / TILE_SIZE, self.pos.y / TILE_SIZE)
            else:
                item_to_spawn = SuperLeaf(self.game, self.pos.x / TILE_SIZE, self.pos.y / TILE_SIZE)
            if item_to_spawn:
                self.game.all_sprites.add(item_to_spawn)
                self.game.items.add(item_to_spawn)

class GroundBlock(Block):
    def __init__(self, game, x_tile, y_tile):
        super().__init__(game, x_tile, y_tile, [SMB3_GROUND_BLOCK_ART], solid=True, block_type="ground")

class Enemy(AnimatedSprite):
    def __init__(self, game, x_tile, y_tile):
        super().__init__()
        self.game = game
        self.pos = pg.math.Vector2(x_tile * TILE_SIZE, y_tile * TILE_SIZE)
        self.vel = pg.math.Vector2(-ENEMY_MOVE_SPEED, 0)
        self.on_ground = False
        self.state = "walk"
        self.health = 1

    def common_update_physics(self, dt, platforms):
        self.pos.x += self.vel.x * dt * FPS
        self.rect.x = round(self.pos.x)
        self.collide_with_platforms_x(platforms)
        self.check_ledge_turn(platforms)

    def collide_with_platforms_x(self, platforms):
        for plat in platforms:
            if plat.solid and self.rect.colliderect(plat.rect):
                if self.vel.x > 0:
                    self.rect.right = plat.rect.left
                    self.vel.x *= -1
                    self.facing_left = True
                elif self.vel.x < 0:
                    self.rect.left = plat.rect.right
                    self.vel.x *= -1
                    self.facing_left = False
                self.pos.x = self.rect.x
                if self.vel.x < 0:
                    self.facing_left = True
                elif self.vel.x > 0:
                    self.facing_left = False
                break

    def check_ledge_turn(self, platforms):
        lookahead_x = self.rect.centerx + (TILE_SIZE / 1.5 * (1 if self.vel.x > 0 else -1))
        lookahead_y = self.rect.bottom + TILE_SIZE / 2
        ledge_check_rect = pg.Rect(lookahead_x - TILE_SIZE / 4, lookahead_y - TILE_SIZE/4, TILE_SIZE/2, TILE_SIZE/2)
        on_solid_ground_ahead = any(plat.solid and ledge_check_rect.colliderect(plat.rect) for plat in platforms)
        if not on_solid_ground_ahead and self.on_ground:
            self.vel.x *= -1
            self.facing_left = not self.facing_left

    def collide_with_platforms_y(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect) and self.vel.y >= 0:
                if self.rect.bottom > plat.rect.top and self.rect.bottom < plat.rect.top + MAX_FALL_SPEED + 1:
                    self.rect.bottom = plat.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                    self.pos.y = self.rect.y
                    break

    def get_stomped(self, player):
        self.state = "squished"
        self.animation_speed = 0
        self.current_frame_index = 0
        self.vel.x = 0
        self.squish_timer = FPS // 2
        player.vel.y = -PLAYER_JUMP_POWER / 2.0
        player.score += 100
        return True

    def take_hit(self, projectile=None):
        self.kill()
        return True

class Goomba(Enemy):
    def __init__(self, game, x_tile, y_tile):
        super().__init__(game, x_tile, y_tile)
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.load_animation_frames("walk", [SMB3_GOOMBA_WALK1_ART, SMB3_GOOMBA_WALK2_ART])
        self.load_animation_frames("squished", [SMB3_GOOMBA_SQUISHED_ART])
        self.animation_speed = 0.08
        self.squish_timer = 0
        self.facing_left = self.vel.x < 0

    def update(self, dt, platforms):
        if self.state == "walk":
            self.common_update_physics(dt, platforms)
            self.vel.y += GRAVITY
            self.pos.y += self.vel.y
            self.rect.y = round(self.pos.y)
            self.collide_with_platforms_y(platforms)
            self.update_animation(dt)
        elif self.state == "squished":
            self.squish_timer -= 1
            if self.squish_timer <= 0:
                self.kill()

class Koopa(Enemy):
    def __init__(self, game, x_tile, y_tile):
        super().__init__(game, x_tile, y_tile)
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.load_animation_frames("walk", [SMB3_KOOPA_WALK1_R_ART, SMB3_KOOPA_WALK2_R_ART])
        self.load_animation_frames("shell", [SMB3_KOOPA_SHELL_ART])
        self.animation_speed = 0.1
        self.shell_timer = 0
        self.SHELL_WAKE_TIME = FPS * 8

    def update(self, dt, platforms):
        if self.state == "walk":
            self.common_update_physics(dt, platforms)
            self.vel.y += GRAVITY
            self.pos.y += self.vel.y
            self.rect.y = round(self.pos.y)
            self.collide_with_platforms_y(platforms)
            self.update_animation(dt)
        elif self.state == "shell":
            self.common_update_physics(dt, platforms)
            self.vel.y += GRAVITY
            self.pos.y += self.vel.y
            self.rect.y = round(self.pos.y)
            self.collide_with_platforms_y(platforms)
            if self.vel.x == 0:
                self.shell_timer -= 1
                if self.shell_timer <= 0:
                    self.state = "walk"
                    self.vel.x = -ENEMY_MOVE_SPEED if self.facing_left else ENEMY_MOVE_SPEED
                    self.animation_speed = 0.1

    def get_stomped(self, player):
        if self.state == "walk":
            self.state = "shell"
            self.vel.x = 0
            self.animation_speed = 0
            self.current_frame_index = 0
            self.shell_timer = self.SHELL_WAKE_TIME
            player.vel.y = -PLAYER_JUMP_POWER / 1.5
            player.score += 100
            return False
        elif self.state == "shell":
            if self.vel.x == 0:
                self.vel.x = KOOPA_SHELL_SPEED if player.rect.centerx < self.rect.centerx else -KOOPA_SHELL_SPEED
                self.facing_left = self.vel.x < 0
            else:
                self.vel.x = 0
                self.shell_timer = self.SHELL_WAKE_TIME
            player.vel.y = -PLAYER_JUMP_POWER / 1.8
            return False
        return False

    def take_hit(self, projectile=None):
        if self.state == "walk":
            self.kill()
            return True
        return False

class Item(AnimatedSprite):
    def __init__(self, game, x_tile, y_tile_spawn_base):
        super().__init__()
        self.game = game
        self.vel = pg.math.Vector2(0,0)
        self.on_ground = False
        self.spawn_state = "rising"
        self.rise_target_y = (y_tile_spawn_base - 1) * TILE_SIZE
        self.rise_speed = -1

    def update_spawn_rise(self):
        if self.spawn_state == "rising":
            self.pos.y += self.rise_speed
            self.rect.y = round(self.pos.y)
            if self.pos.y <= self.rise_target_y:
                self.pos.y = self.rise_target_y
                self.rect.y = round(self.pos.y)
                self.spawn_state = "active"
                self.vel.x = ENEMY_MOVE_SPEED * 0.75
                return True
        return False

    def common_item_physics(self, dt, platforms):
        self.vel.y += GRAVITY
        self.vel.y = min(self.vel.y, MAX_FALL_SPEED)
        self.pos.x += self.vel.x * dt * FPS
        self.pos.y += self.vel.y
        self.rect.x = round(self.pos.x)
        for plat in platforms:
            if plat.solid and self.rect.colliderect(plat.rect):
                if self.vel.x > 0:
                    self.rect.right = plat.rect.left
                    self.vel.x *= -1
                elif self.vel.x < 0:
                    self.rect.left = plat.rect.right
                    self.vel.x *= -1
                self.pos.x = self.rect.x
                break
        self.rect.y = round(self.pos.y)
        self.on_ground = False
        for plat in platforms:
            if plat.solid and self.rect.colliderect(plat.rect):
                if self.vel.y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = plat.rect.bottom
                    self.vel.y = 0
                self.pos.y = self.rect.y
                break
        if self.on_ground:
            lookahead_x = self.rect.centerx + (TILE_SIZE / 2 * (1 if self.vel.x > 0 else -1))
            lookahead_y = self.rect.bottom + TILE_SIZE / 4
            ledge_check_rect = pg.Rect(lookahead_x - TILE_SIZE / 8, lookahead_y - TILE_SIZE/8, TILE_SIZE/4, TILE_SIZE/4)
            on_solid_ground_ahead = any(plat.solid and ledge_check_rect.colliderect(plat.rect) for plat in platforms)
            if not on_solid_ground_ahead:
                self.vel.x *= -1

class Mushroom(Item):
    def __init__(self, game, x_tile, y_tile_spawn_base):
        super().__init__(game, x_tile, y_tile_spawn_base)
        self.pos = pg.math.Vector2(x_tile * TILE_SIZE, y_tile_spawn_base * TILE_SIZE)
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.load_animation_frames("idle", [SMB3_MUSHROOM_ART])
        self.animation_speed = 0

    def update(self, dt, platforms):
        if self.update_spawn_rise():
            self.common_item_physics(dt, platforms)
        self.update_animation(dt)

class SuperLeaf(Item):
    def __init__(self, game, x_tile, y_tile_spawn_base):
        super().__init__(game, x_tile, y_tile_spawn_base)
        self.pos = pg.math.Vector2(x_tile * TILE_SIZE, y_tile_spawn_base * TILE_SIZE)
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.load_animation_frames("idle", [SMB3_SUPER_LEAF_ART])
        self.animation_speed = 0.1
        self.base_y_drift = 0
        self.drift_amplitude_y = TILE_SIZE / 4
        self.drift_frequency_y = 0.05
        self.drift_timer_y = random.uniform(0, 2 * math.pi)

    def update(self, dt, platforms):
        if self.spawn_state == "rising":
            if self.update_spawn_rise():
                self.base_y_drift = self.pos.y
                self.vel.x = random.choice([ENEMY_MOVE_SPEED * 0.5, -ENEMY_MOVE_SPEED * 0.5])
        elif self.spawn_state == "active":
            self.pos.x += self.vel.x * dt * FPS
            self.drift_timer_y += self.drift_frequency_y * FPS * dt
            offset_y = self.drift_amplitude_y * math.sin(self.drift_timer_y)
            self.pos.y = self.base_y_drift + offset_y
            self.rect.x = round(self.pos.x)
            self.rect.y = round(self.pos.y)
            for plat in platforms:
                if plat.solid and self.rect.colliderect(plat.rect):
                    if self.vel.x > 0 and self.rect.right > plat.rect.left:
                        self.rect.right = plat.rect.left
                        self.vel.x *= -1
                    elif self.vel.x < 0 and self.rect.left < plat.rect.right:
                        self.rect.left = plat.rect.right
                        self.vel.x *= -1
                    self.pos.x = self.rect.x
                    break
        self.update_animation(dt)

class Flagpole(AnimatedSprite):
    def __init__(self, game, x_tile, y_tile):
        super().__init__()
        self.game = game
        self.pos = pg.math.Vector2(x_tile * TILE_SIZE, y_tile * TILE_SIZE)
        level_height_tiles = len(self.game.levels[self.game.current_level_char])
        rect_height = (level_height_tiles - y_tile) * TILE_SIZE
        self.rect = pg.Rect(self.pos.x, self.pos.y, TILE_SIZE, rect_height)
        self.load_animation_frames("idle", [SMB3_FLAGPOLE_ART])
        self.animation_speed = 0

class Camera:
    def __init__(self, width_tiles, height_tiles):
        self.camera_rect_on_screen = pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.offset = pg.math.Vector2(0, 0)
        self.world_width_pixels = 0
        self.world_height_pixels = 0

    def update(self, target_player):
        target_cam_x = -target_player.rect.centerx + SCREEN_WIDTH // 2
        clamped_cam_x = min(0, target_cam_x)
        clamped_cam_x = max(clamped_cam_x, -(self.world_width_pixels - SCREEN_WIDTH))
        clamped_cam_y = 0
        self.offset.x = clamped_cam_x
        self.offset.y = clamped_cam_y

    def get_world_view_rect(self):
        return pg.Rect(-self.offset.x, -self.offset.y, SCREEN_WIDTH, SCREEN_HEIGHT)

# Level and Overworld Data
LEVEL_1_1_DATA = [
    "..................................................................................................F.",
    "..................................................................................................F.",
    "..................BBQB............................................................................F.",
    "..................................................................................................F.",
    "...................................Q....B................K........................................F.",
    ".........................BBBB.........QQQ.........................................................F.",
    "............................................................E.....................................F.",
    "...................E................E.........E.E.................................................F.",
    "GGGGGGGGGGGGGGGGGGGGGGGG...GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG...GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGG...GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG...GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
]
LEVEL_1_2_DATA = [
    "..................................................F.",
    "..................................................F.",
    "............Q....B............K...................F.",
    ".........................E........................F.",
    ".......E............E................BBQ..........F.",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
]
OVERWORLD_DATA = [
    "                    ",
    " . 1 . 2 . . . . .  ",
    " . . . . . . . . .  ",
    " . . . . . . . . .  ",
    " . . . . . . . . .  ",
    " . . . . . . . . .  ",
    " . . . . . . . . .  ",
    "                    "
]

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("SMB3 Style Game - CATSDK Edition, MEOW!")
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, TILE_SIZE // 2)
        self.game_state = "overworld"
        self.overworld_data = OVERWORLD_DATA
        self.mario_overworld_pos = (2,1)
        found_first_level_node = False
        for r, row in enumerate(self.overworld_data):
            for c, char_code in enumerate(row):
                if char_code.isdigit() or (char_code.isalpha() and char_code != 'P'):
                    self.mario_overworld_pos = (c,r)
                    found_first_level_node = True; break
            if found_first_level_node: break
        self.overworld_cell_size = TILE_SIZE
        self.levels = {'1': LEVEL_1_1_DATA, '2': LEVEL_1_2_DATA}
        self.game_over = False
        self.debug_mode = False
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.flagpoles = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.player = None
        self.camera = Camera(0,0)
        self.current_level_char = '1'

    def spawn_particles(self, center_x, top_y):
        for _ in range(4):
            vel_x = random.uniform(-5, 5)
            vel_y = random.uniform(-8, -3)
            particle = Particle(self, center_x - TILE_SIZE//4, top_y - TILE_SIZE//4,
                                [SMB3_BRICK_DEBRIS_ART],
                                vel_x, vel_y, FPS // 2)
            self.all_sprites.add(particle)
            self.particles.add(particle)

    def load_level(self, level_data_str_array):
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.items.empty()
        self.flagpoles.empty()
        self.particles.empty()
        player_start_pos_tiles = (2, len(level_data_str_array) - 5)
        for row_idx, row_str in enumerate(level_data_str_array):
            for col_idx, char_code in enumerate(row_str):
                if char_code == 'G':
                    block = GroundBlock(self, col_idx, row_idx)
                    self.all_sprites.add(block); self.platforms.add(block)
                elif char_code == 'B':
                    block = BrickBlock(self, col_idx, row_idx)
                    self.all_sprites.add(block); self.platforms.add(block)
                elif char_code == 'Q':
                    block = QuestionBlock(self, col_idx, row_idx, contains="mushroom")
                    self.all_sprites.add(block); self.platforms.add(block)
                elif char_code == 'E':
                    enemy = Goomba(self, col_idx, row_idx)
                    self.all_sprites.add(enemy); self.enemies.add(enemy)
                elif char_code == 'K':
                    enemy = Koopa(self, col_idx, row_idx)
                    self.all_sprites.add(enemy); self.enemies.add(enemy)
                elif char_code == 'F':
                    flagpole = Flagpole(self, col_idx, row_idx)
                    self.all_sprites.add(flagpole); self.flagpoles.add(flagpole)
        prev_lives = 3; prev_score = 0; prev_form = PLAYER_STATE_SMALL
        if self.player:
            prev_lives = self.player.lives
            prev_score = self.player.score
            prev_form = self.player.player_form
        self.player = Player(self, player_start_pos_tiles[0], player_start_pos_tiles[1])
        self.player.lives = prev_lives
        self.player.score = prev_score
        self.player.set_form(prev_form)
        self.all_sprites.add(self.player)
        level_width_pixels = len(level_data_str_array[0]) * TILE_SIZE
        level_height_pixels = len(level_data_str_array) * TILE_SIZE
        self.camera = Camera(level_width_pixels // TILE_SIZE, level_height_pixels // TILE_SIZE)
        self.camera.world_width_pixels = level_width_pixels
        self.camera.world_height_pixels = level_height_pixels

    def enter_level(self, level_char_id):
        if level_char_id in self.levels:
            self.current_level_char = level_char_id
            current_score = 0; current_lives = 3; current_form = PLAYER_STATE_SMALL
            if self.player:
                current_score = self.player.score
                current_lives = self.player.lives
                current_form = self.player.player_form
            self.load_level(self.levels[level_char_id])
            self.player.score = current_score
            self.player.lives = current_lives
            self.player.set_form(current_form)
            self.game_state = "level"
            self.game_over = False

    def complete_level(self):
        self.game_state = "overworld"

    def reset_level_soft(self):
        if self.player:
            current_score = self.player.score
            current_lives = self.player.lives
            self.load_level(self.levels[self.current_level_char])
            self.player.score = current_score
            self.player.lives = current_lives
            self.player.set_form(PLAYER_STATE_SMALL)
            if self.player.lives <= 0:
                self.game_over = True
        else:
            self.enter_level(self.current_level_char)

    def reset_game_hard(self):
        self.game_over = False
        level_to_start_char = self.overworld_data[self.mario_overworld_pos[1]][self.mario_overworld_pos[0]]
        if level_to_start_char not in self.levels:
            level_to_start_char = '1'
            found_level_1_node = False
            for r_idx, r_str in enumerate(self.overworld_data):
                if found_level_1_node: break
                for c_idx, char_val in enumerate(r_str):
                    if char_val == '1':
                        self.mario_overworld_pos = (c_idx, r_idx); found_level_1_node = True; break
        self.player = None
        self.enter_level(level_to_start_char)
        self.player.score = 0
        self.player.lives = 3
        self.player.set_form(PLAYER_STATE_SMALL)

    def draw_overworld(self):
        self.screen.fill(BACKGROUND_COLOR)
        ow_tile_size = self.overworld_cell_size
        for r, row_str in enumerate(self.overworld_data):
            for c, char_code in enumerate(row_str):
                x, y = c * ow_tile_size, r * ow_tile_size
                rect = (x, y, ow_tile_size, ow_tile_size)
                if char_code == ' ':
                    pg.draw.rect(self.screen, color_map['B'], rect, 1)
                elif char_code == '.':
                    pg.draw.rect(self.screen, color_map['G'], rect)
                elif char_code.isdigit() or (char_code.isalpha() and char_code not in 'P'):
                    pg.draw.rect(self.screen, color_map['Y'], rect)
                    self.draw_text(char_code, x + ow_tile_size // 3, y + ow_tile_size // 3, 'K')
        mario_ow_x = self.mario_overworld_pos[0] * ow_tile_size
        mario_ow_y = self.mario_overworld_pos[1] * ow_tile_size
        pg.draw.rect(self.screen, color_map['R'],
                     (mario_ow_x + ow_tile_size//4, mario_ow_y + ow_tile_size//4,
                      ow_tile_size//2, ow_tile_size//2))

    def draw_text(self, text_str, x, y, color_char_code='W', Sfont=None):
        if Sfont is None: Sfont = self.font
        text_surface = Sfont.render(text_str, True, color_map[color_char_code])
        self.screen.blit(text_surface, (x,y))

    async def main(self):
        running = True
        while running:
            raw_dt = self.clock.tick(FPS) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT: running = False; return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE: running = False; return
                    if event.key == pg.K_F1: self.debug_mode = not self.debug_mode
                    if self.game_state == "level" and self.game_over and event.key == pg.K_r:
                        self.reset_game_hard()
                if self.game_state == "overworld" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    clicked_col = mouse_x // self.overworld_cell_size
                    clicked_row = mouse_y // self.overworld_cell_size
                    if (0 <= clicked_row < len(self.overworld_data) and
                        0 <= clicked_col < len(self.overworld_data[0])):
                        char_at_click = self.overworld_data[clicked_row][clicked_col]
                        if char_at_click in self.levels:
                            self.mario_overworld_pos = (clicked_col, clicked_row)
                            self.enter_level(char_at_click)
            if self.game_state == "level" and not self.game_over:
                self.player.update(raw_dt, self.platforms)
                for enemy in list(self.enemies):
                    enemy.update(raw_dt, self.platforms)
                for item in list(self.items):
                    item.update(raw_dt, self.platforms)
                for particle in list(self.particles):
                    particle.update(raw_dt, self.platforms)
                self.camera.update(self.player)
                if self.player.invincible_timer <= 0:
                    for enemy in list(self.enemies):
                        if self.player.rect.colliderect(enemy.rect):
                            is_stomp = (self.player.vel.y > 0 and
                                        self.player.rect.bottom < enemy.rect.centery + TILE_SIZE / 3 and
                                        not self.player.on_ground)
                            if isinstance(enemy, Goomba) and enemy.state == "walk":
                                if is_stomp: enemy.get_stomped(self.player)
                                else: self.player.take_damage()
                            elif isinstance(enemy, Koopa):
                                if enemy.state == "walk":
                                    if is_stomp: enemy.get_stomped(self.player)
                                    else: self.player.take_damage()
                                elif enemy.state == "shell":
                                    if is_stomp:
                                        enemy.get_stomped(self.player)
                                    elif enemy.vel.x != 0:
                                        self.player.take_damage()
                                    else:
                                        enemy.vel.x = KOOPA_SHELL_SPEED if self.player.rect.centerx < enemy.rect.centerx else -KOOPA_SHELL_SPEED
                                        enemy.facing_left = enemy.vel.x < 0
                            if self.game_over or self.player.invincible_timer > 0: break
                for shell_koopa in list(self.enemies):
                    if isinstance(shell_koopa, Koopa) and shell_koopa.state == "shell" and shell_koopa.vel.x != 0:
                        for other_enemy in list(self.enemies):
                            if other_enemy != shell_koopa and shell_koopa.rect.colliderect(other_enemy.rect):
                                other_enemy.take_hit(projectile=shell_koopa)
                                self.player.score += 200
                for item in list(self.items):
                    if self.player.rect.colliderect(item.rect):
                        if isinstance(item, Mushroom) and self.player.player_form == PLAYER_STATE_SMALL:
                            self.player.set_form(PLAYER_STATE_SUPER)
                            self.player.score += 1000
                            item.kill()
                        elif isinstance(item, SuperLeaf) and self.player.player_form != PLAYER_STATE_RACCOON:
                            if self.player.player_form == PLAYER_STATE_SMALL:
                                self.player.set_form(PLAYER_STATE_SUPER)
                            self.player.score += 1000
                            item.kill()
                for flagpole in self.flagpoles:
                    if self.player.rect.colliderect(flagpole.rect):
                        self.player.score += 5000
                        self.complete_level()
                        break
            self.screen.fill(BACKGROUND_COLOR)
            if self.game_state == "overworld":
                self.draw_overworld()
            elif self.game_state == "level":
                world_view = self.camera.get_world_view_rect()
                for sprite in self.all_sprites:
                    if sprite.rect.colliderect(world_view):
                        sprite.draw(self.screen, self.camera.offset.x, self.camera.offset.y)
                if self.player:
                    self.draw_text(f"SCORE: {self.player.score}", 20, 10, 'W')
                    self.draw_text(f"LIVES: {self.player.lives}", SCREEN_WIDTH - 150, 10, 'W')
                    self.draw_text(f"FORM: {self.player.player_form.upper()}", SCREEN_WIDTH // 2 - 50, 10, 'W')
                if self.game_over:
                    overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
                    overlay.fill((50, 50, 50, 180))
                    self.screen.blit(overlay, (0,0))
                    large_font = pg.font.Font(None, TILE_SIZE)
                    self.draw_text("GAME OVER", SCREEN_WIDTH // 2 - TILE_SIZE * 2, SCREEN_HEIGHT // 2 - TILE_SIZE, 'R', large_font)
                    self.draw_text("Press R to Restart!", SCREEN_WIDTH // 2 - TILE_SIZE * 2, SCREEN_HEIGHT // 2 + TILE_SIZE //2, 'W')
            pg.display.flip()
            await asyncio.sleep(0)
        pg.quit()

async def main():
    game_instance = Game()
    await game_instance.main()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
