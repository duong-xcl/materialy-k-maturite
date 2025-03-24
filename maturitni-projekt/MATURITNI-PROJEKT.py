import pygame
import random
import time
import os
import sys
import sqlite3
import json

pygame.init()

CONFIG = {
    "WIDTH": 1200,
    "HEIGHT": 800,
    "CELL_SIZE": 40,
    "COLORS": {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "GRAY": (150, 150, 150),
    },
    "BORDER_THICKNESS": 8,
    "BORDER_MARGIN": 80,
    "HEART_SIZE": 50,
    "FONT_PATH": "./Chara.ttf",        # seeing this font on your screen fills you with determination. HP fully restored.
    "FONT_SIZE_DEFAULT": 56,
    "FONT_SIZE_SMALL": 32,
    "FONT_SIZE_BIG": 100,
    "INTRO_FADE_STEP": 8,
    "INTRO_FADE_SPEED": 30,
    "INTRO_HOLD_MS": 1000,
    "DEATH_ANIM_STAGE_1_MS": 1000,
    "DEATH_ANIM_STAGE_2_MS": 1400,
    "DEATH_ANIM_STAGE_3_MS": 2000,
    "MENU_MUSIC_VOLUME": 1.0,           # I unfortunately found out that it will be tested on a setup which doesn't even have speakers so all the music is useless :)
    "SNAKE_SPEED_INIT": 10,             # snake speed, lower speed = lower difficulty but it will scale up anyway
    "SNAKE_SPEED_LVUP_INCREMENT": 2,    # you only gain speed upon leveling up or reaching another stage so this is the only other difficulty setting you can adjust
    "LEVEL_UP_FOOD_THRESHOLD": 10,      # this is how much food you need for level up..
    "STAGE_UP_SOUND_DELAY": 1000,
    "REVIVAL_BLINK_MS": 1000,
    "REVIVAL_BLINK_INTERVAL": 250,
    "ANIM_HEART_TRANSITION_MS": 1000,
    "BONE_SPAWN_INTERVAL": 30,
    "BONE_SPEED": 11,                   # technically this is also a difficulty setting but if you adjust this, make sure to also adjust..
    "GRAVITY": 0.7,
    "JUMP_POWER": -14,
    "PLAYER_VELOCITY_X": 11,            # THIS! adjust this setting to approx. match the bone speed or else you might have made it more difficult for yourself
    "PRACTICE_DEFAULT_DURATION": 10,    # 10 seconds is also how much it normally takes. making it lower than 10 however seems too short.
    "PRACTICE_MAX_DURATION": 99,        # who in their right mind would set it to 99 anyways tbh
}

# Configs with notes are about the only things you can experiment with and adjust the values.
#  If you however adjust anything else, especially down from here, I do not guarantee anything will work anymore.

WIDTH = CONFIG["WIDTH"]
HEIGHT = CONFIG["HEIGHT"]
CELL_SIZE = CONFIG["CELL_SIZE"]
WHITE = CONFIG["COLORS"]["WHITE"]
BLACK = CONFIG["COLORS"]["BLACK"]
RED = CONFIG["COLORS"]["RED"]
GREEN = CONFIG["COLORS"]["GREEN"]
GRAY = CONFIG["COLORS"]["GRAY"]
BORDER_THICKNESS = CONFIG["BORDER_THICKNESS"]
BORDER_MARGIN = CONFIG["BORDER_MARGIN"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SLITHER")

def initialize_db():
    """
    Creates (if not exists) a SQLite database with a scoreboard table.
    """
    # Using a file named "scoreboard.db" inside script_dir
    db_path = os.path.join(script_dir, "scoreboard.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # CREATE TABLE with fields: id, name, score
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scoreboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def load_font(size=CONFIG["FONT_SIZE_DEFAULT"]):
    #Loads a Pygame font at the specified size. 
    #Because readable text is kinda important, right?

    #Args:
    #    size (int): The font size you want, 
    #                defaulting to the one in CONFIG.

    #Returns:
    #pygame.font.Font: The font you can use to 
    #                      show messages with determination.
    return pygame.font.Font(CONFIG["FONT_PATH"], size)

font = load_font()
small_font = load_font(CONFIG["FONT_SIZE_SMALL"])

def draw_text(text, x, y, color=WHITE, center=True, font_used=font):
    #Renders the given text at (x, y). 
    #If 'center' is True, it centers the text around x; 
    #otherwise, it just starts from x.

    #Args:
    #    text (str): The content to display.
    #    x (int): - coordinate.
    #    y (int): | coordinate.
    #    color (tuple): RGB color, default is white.
    #    center (bool): Whether to center text around x.
    #    font_used (pygame.font.Font): Which font to use.

    #Returns:
    #    int: The width of the rendered text,.
    text_surface = font_used.render(text, True, color)
    if center:
        x -= text_surface.get_width() // 2
    screen.blit(text_surface, (x, y))
    return text_surface.get_width()

language = "English"
music_enabled = True

def translate(text):
    #Translates English text to Korean (if language is set to Korean).
    #Defaults to returning the English text if there's no match
    #or if the current language is English.

    #Args:
    #    text (str): The original English string.

    #Returns:
    #    str: The translated text if available, else the original.
    translations = {
        "English": {
            "Slither": "SLITHER",
            "Play": "Play",
            "Practice": "Practice",
            "Practice Menu": "Practice Menu",
            "Battle 1": "Battle 1",
            "Select Duration": "Select Duration",
            "sec": "sec",
            "Press X = Play, C = Back": "Press X = Play, C = Back",
            "Settings": "Settings",
            "Exit": "Exit",
            "Score": "Score",
            "Again? Press X": "Again? Press X",
            "Go back? Press C": "Go back? Press C",
            "Language": "Language",
            "English": "English",
            "Korean": "Korean",
            "Back": "Back",
            "Level": "Level",
            "Stage": "STAGE",
            "LEVEL UP!!!! +SPEED": "LEVEL UP!!!! +SPEED",
            "STAGE UP!!!": "STAGE UP!!!",
            "SURVIVE!!!": "SURVIVE!!!",
            "of course": "of course",
            "+1 HEART!!": "+1 HEART!!",
            "Sans Fight - First Attack": "Sans Fight - First Attack",
            "Music": "Music",
            "On": "On",
            "Off": "Off",
            "Music Composer": "Music Composer",
            "Developer": "Developer",
            "Scoreboard": "Scoreboard",
            "Enter your name": "Enter your name",
            "Name": "Name",
            "You made it to the scoreboard!": "You made it to the scoreboard!",
            "You didn't make it to the scoreboard": "You didn't make it to the scoreboard",
            "Press C": "Press C",
            "Enter": "Enter",
            "OK": "OK",
            "ESC": "ESC",
            "Cancel": "Cancel"
        },
        "Korean": {
            "Slither": "슬리더",
            "Play": "게임 시작",
            "Practice": "연습",
            "Practice Menu": "연습 메뉴",
            "Battle 1": "배틀 1",
            "Select Duration": "시간 선택",
            "sec": "초",
            "Press X = Play, C = Back": "X = 시작, C = 뒤로",
            "Settings": "설정",
            "Exit": "종료",
            "Score": "점수",
            "Again? Press X": "다시 하기? X",
            "Go back? Press C": "메뉴로 가기? C",
            "Language": "언어",
            "English": "영어",
            "Korean": "한국어",
            "Back": "뒤로",
            "Level": "레벨",
            "Stage": "스테이지",
            "LEVEL UP!!!! +SPEED": "레벨 업!!!! + 속도 증가",
            "STAGE UP!!!": "스테이지 업!!!",
            "SURVIVE!!!": "버텨!!!",
            "of course": "당연하지",
            "+1 HEART!!": "+1 하트!!",
            "Sans Fight - First Attack": "샌즈 전투 - 첫 공격",
            "Music": "음악",
            "On": "켬",
            "Off": "끔",
            "Music Composer": "음악 작곡가",
            "Developer": "개발자",
            "Scoreboard": "스코어보드",
            "Enter your name": "이름을 입력하세요",
            "Name": "이름",
            "You made it to the scoreboard!": "축하합니다, 스코어보드에 등록되었습니다!",
            "You didn't make it to the scoreboard": "아쉽게도 스코어보드에 오르지 못했습니다",
            "Press C": "C 키를 누르세요",
            "Enter": "엔터",
            "OK": "확인",
            "ESC": "ESC",
            "Cancel": "취소"
        }
    }
    return translations.get(language, translations["English"]).get(text, text)

script_dir = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(script_dir, "settings.json")

def load_user_settings():
    global language, music_enabled
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                language = data.get("language", "English")
                music_enabled = data.get("music_enabled", True)
        except Exception as e:
            print("Error loading settings:", e)
            language = "English"
            music_enabled = True
    else:
        language = "English"
        music_enabled = True

def save_user_settings():
    data = {
        "language": language,
        "music_enabled": music_enabled
    }
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error saving settings:", e)


heart_img = pygame.image.load("./heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (44, 44))

death_heart_img = pygame.image.load(os.path.join(script_dir, "heart.png"))
heartbroken_img = pygame.image.load(os.path.join(script_dir, "heartbroken.png"))
death_sound = pygame.mixer.Sound(os.path.join(script_dir, "death.mp3"))

HEART_SIZE = CONFIG["HEART_SIZE"]
death_heart_img = pygame.transform.scale(death_heart_img, (HEART_SIZE, HEART_SIZE))
heartbroken_img = pygame.transform.scale(heartbroken_img, (HEART_SIZE, HEART_SIZE))



def play_menu_music():
    #Fires up the main menu music if music is enabled 
    #and the 'startmenu.mp3' file is present.
    #Because silent menus are kinda depressing.
    if not music_enabled:
        return
    menu_music_path = os.path.join(script_dir, "startmenu.mp3")
    if os.path.isfile(menu_music_path):
        pygame.mixer.music.load(menu_music_path)
        pygame.mixer.music.set_volume(CONFIG["MENU_MUSIC_VOLUME"])
        pygame.mixer.music.play(-1)

def intro_sequence():
    #Plays the fancy intro with a fade-in, fade-out
    #of the 'Slither' title and the heart image. 
    #Includes optional intro music if available.
    intro_path = os.path.join(script_dir, "intro.mp3")
    if music_enabled and os.path.isfile(intro_path):
        pygame.mixer.music.load(intro_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

    fade_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fade_surf.fill(BLACK)
    text_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    text_surf.fill((0, 0, 0, 0))
    big_font = load_font(CONFIG["FONT_SIZE_BIG"])
    text_render = big_font.render(translate("Slither"), True, WHITE)
    text_x = (WIDTH // 2) - (text_render.get_width() // 2)
    text_y = (HEIGHT // 2) - (text_render.get_height() // 2)
    text_surf.blit(text_render, (text_x, text_y))

    heart_pos_x = text_x + text_render.get_width() + 20
    heart_pos_y = text_y + (text_render.get_height() // 2 - heart_img.get_height() // 2)
    text_surf.blit(heart_img, (heart_pos_x, heart_pos_y))

    clock_intro = pygame.time.Clock()
    # Fade in...
    for alpha in range(0, 256, CONFIG["INTRO_FADE_STEP"]):
        screen.fill(BLACK)
        fade_surf.fill((0, 0, 0, 0))
        fade_surf.blit(text_surf, (0, 0))
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.flip()
        clock_intro.tick(CONFIG["INTRO_FADE_SPEED"])

    hold_start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - hold_start < CONFIG["INTRO_HOLD_MS"]:
        screen.fill(BLACK)
        fade_surf.set_alpha(255)
        screen.blit(text_surf, (0, 0))
        pygame.display.flip()
        clock_intro.tick(CONFIG["INTRO_FADE_SPEED"])

    # Fade out!!!
    for alpha in range(255, -1, -CONFIG["INTRO_FADE_STEP"]):
        screen.fill(BLACK)
        fade_surf.fill((0, 0, 0, 0))
        fade_surf.blit(text_surf, (0, 0))
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.flip()
        clock_intro.tick(CONFIG["INTRO_FADE_SPEED"])

    pygame.mixer.music.stop()

def animate_heart(start_pos, end_pos, duration=500):
    #Animates the heart image from a start position 
    #to an end position over 'duration' milliseconds.
    #The screen also shows a few static menu items 
    #so things don't look empty.

    #Args:
    #    start_pos (tuple): (x, y) of where the heart starts.
    #    end_pos (tuple): (x, y) of where the heart ends.
    #    duration (int): Time in ms to complete the animation.
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        t = (pygame.time.get_ticks() - start_time) / duration
        x = int(start_pos[0] * (1 - t) + end_pos[0] * t)
        y = int(start_pos[1] * (1 - t) + end_pos[1] * t)
        screen.fill(BLACK)
        dynamic_options = [translate("Play"), translate("Practice"), translate("Scoreboard"), translate("Settings"), translate("Exit")]
        for i, option in enumerate(dynamic_options):
            draw_text(option, WIDTH // 2, 320 + i * 100)
        draw_text(translate("Slither"), WIDTH // 2, 160)
        screen.blit(heart_img, (x, y))
        pygame.display.flip()
        pygame.time.delay(10)

class Fragment:
    #A tiny chunk from the broken heart 
    #that flies around during the death animation.
    #Each fragment has a position, velocity, angle, 
    #and an absolutely amazing spin:)
    def __init__(self, x, y):
        #Sets up a single fragment at (x, y)
        #with randomized velocity and rotation.
        self.x = x
        self.y = y
        self.vel_x = random.choice([-3, 3])
        self.vel_y = random.randint(-5, -2)
        self.rotation = random.uniform(-5, 5)
        self.angle = 0
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (210, 0, 0), [(0,0),(15,7),(7,15)])
        self.original_image = self.image.copy()

    def update(self):
        #Moves the fragment according to its velocity,
        #adds a bit of gravity, and rotates it 
        #for an absolutely amazing spin:)
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.3
        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def draw(self, surface):
        #Draws this fragment onto the given surface.
        #Usually called each frame in the animation loop.
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect.topleft)

def play_death_animation(x, y):
    #Plays a multi-stage death animation:
    #1. Shows a normal heart
    #2. Shows a cracked heart, plays a death sound
    #3. Launches fragments outward

    #Args:
    #    x (int): The heart's x-position.
    #    y (int): The heart's y-position.
    clock_anim = pygame.time.Clock()
    running = True
    stage = 0
    timer = pygame.time.get_ticks()
    fragments = []
    sound_played = False

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        current_time = pygame.time.get_ticks()

        if stage == 0:
            screen.blit(death_heart_img, (x, y))
            if current_time - timer > CONFIG["DEATH_ANIM_STAGE_1_MS"]:
                stage = 1
                timer = pygame.time.get_ticks()
        elif stage == 1:
            screen.blit(heartbroken_img, (x, y))
            if not sound_played:
                death_sound.play()
                sound_played = True
            if current_time - timer > CONFIG["DEATH_ANIM_STAGE_2_MS"]:
                stage = 2
                timer = pygame.time.get_ticks()
                for _ in range(3):
                    frag = Fragment(x + HEART_SIZE//2, y + HEART_SIZE//2)
                    fragments.append(frag)
        elif stage == 2:
            for frag in fragments:
                frag.update()
                frag.draw(screen)
            if current_time - timer > CONFIG["DEATH_ANIM_STAGE_3_MS"]:
                running = False

        pygame.display.update()
        clock_anim.tick(60)

def main_menu():
    #Draws and controls the main menu, letting the player choose 
    #to Play, Practice, enter Settings, or Exit the game.
    #Cycles through options with up/down arrows and uses X to confirm.
    selected = 0
    play_menu_music()

    while True:
        screen.fill(BLACK)
        dynamic_options = [translate("Play"), translate("Practice"), translate("Scoreboard"), translate("Settings"), translate("Exit")]
        draw_text(translate("Slither"), WIDTH // 2, 160)
        composer_txt = f"{translate('Music Composer')} - Toby Fox"
        developer_txt = f"{translate('Developer')} - Jaroslav Horak"
        c_surf = small_font.render(composer_txt, True, WHITE)
        d_surf = small_font.render(developer_txt, True, WHITE)
        screen.blit(c_surf, (20, HEIGHT - 80))
        screen.blit(d_surf, (20, HEIGHT - 50))

        if language == "English":
            instructions = ["Arrows - movement", "Space - jump", "X - continue", "C - back"]
        else:
            instructions = ["화살표 - 움직이기", "스페이스 - 점프", "X - 계속", "C - 뒤로"]
        inst_gap = 20
        current_y = HEIGHT - 20
        for line in reversed(instructions):
            surf = small_font.render(line, True, WHITE)
            screen.blit(surf, (WIDTH - surf.get_width() - 20, current_y - surf.get_height()))
            current_y -= (surf.get_height() + inst_gap)

        for i, option in enumerate(dynamic_options):
            text_width = draw_text(option, WIDTH // 2, 320 + i * 100)
            if i == selected:
                screen.blit(heart_img, (WIDTH // 2 - text_width // 2 - 60, 322 + i * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % len(dynamic_options)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % len(dynamic_options)
                elif event.key == pygame.K_x:
                    if selected == 0:
                        player_name = ask_for_player_name()
                        if not player_name:
                            continue

                        pygame.mixer.music.stop()

                        text_width = font.render(dynamic_options[selected], True, WHITE).get_width()
                        animate_heart((WIDTH // 2 - text_width // 2 - 60, 322), (WIDTH - 80, 20))

                        game_loop(player_name)



                    elif selected == 1:
                        pygame.mixer.music.stop()
                        practice_menu()
                        if music_enabled:
                            play_menu_music()
                    elif selected == 2:  # scoreboard
                        pygame.mixer.music.stop()
                        show_scoreboard()
                        if music_enabled:
                            play_menu_music()
                    elif selected == 3:
                        settings_menu()
                    elif selected == 4:
                        pygame.quit()
                        return

def practice_menu():
    selected = 0
    while True:
        screen.fill(BLACK)
        practice_options = [translate("Battle 1"), translate("Back")]
        draw_text(translate("Practice Menu"), WIDTH // 2, 160)

        for i, option in enumerate(practice_options):
            text_width = draw_text(option, WIDTH // 2, 320 + i * 100)
            if i == selected:
                screen.blit(heart_img, (WIDTH // 2 - text_width // 2 - 60, 322 + i * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % len(practice_options)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % len(practice_options)
                elif event.key == pygame.K_x:
                    if selected == 0:
                        practice_duration_menu()
                    elif selected == 1:
                        return

def practice_duration_menu():
    duration = CONFIG["PRACTICE_DEFAULT_DURATION"]
    while True:
        screen.fill(BLACK)
        draw_text(translate("Select Duration"), WIDTH // 2, 160)
        dur_str = f"{duration} {translate('sec')}"
        text_width = draw_text(dur_str, WIDTH // 2, 320)
        instruction_line = translate("Press X = Play, C = Back")
        draw_text(instruction_line, WIDTH // 2, 420, font_used=small_font)
        screen.blit(heart_img, (WIDTH // 2 - text_width // 2 - 60, 322))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    duration = max(CONFIG["PRACTICE_DEFAULT_DURATION"], duration - 1)
                elif event.key == pygame.K_RIGHT:
                    duration = min(CONFIG["PRACTICE_MAX_DURATION"], duration + 1)
                elif event.key == pygame.K_x:
                    pygame.mixer.music.stop()
                    practice_sequence(duration)
                    return
                elif event.key == pygame.K_c:
                    return

def practice_sequence(duration):
    start_sound_path = os.path.join(script_dir, "revivalstart.mp3")
    practice_music_path = os.path.join(script_dir, "revival.mp3")
    if music_enabled and os.path.isfile(start_sound_path):
        try:
            start_sound = pygame.mixer.Sound(start_sound_path)
            start_sound.set_volume(1.0)
            start_sound.play()
        except:
            pass

    heart_start = (WIDTH - 80, 20)
    blink_duration = CONFIG["REVIVAL_BLINK_MS"]
    blink_interval = CONFIG["REVIVAL_BLINK_INTERVAL"]
    blink_start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - blink_start_time < blink_duration:
        elapsed = pygame.time.get_ticks() - blink_start_time
        screen.fill(BLACK)
        if (elapsed // blink_interval) % 2 == 1:
            screen.blit(heart_img, heart_start)
        pygame.display.flip()
        pygame.time.delay(30)

    if music_enabled and os.path.isfile(practice_music_path):
        try:
            pygame.mixer.music.load(practice_music_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
        except:
            pass

    heart_center = (WIDTH // 2 - 22, HEIGHT // 2 - 22)
    start_time = pygame.time.get_ticks()
    anim_dur = CONFIG["ANIM_HEART_TRANSITION_MS"]
    while pygame.time.get_ticks() - start_time < anim_dur:
        t = (pygame.time.get_ticks() - start_time) / anim_dur
        x = int(heart_start[0] * (1 - t) + heart_center[0] * t)
        y = int(heart_start[1] * (1 - t) + heart_center[1] * t)
        screen.fill(BLACK)
        screen.blit(heart_img, (x, y))
        pygame.display.flip()
        pygame.time.delay(10)

    flashing_text_revive(translate("SURVIVE!!!"), 1)
    survived = revive_game(game_time=duration)
    if survived:
        flashing_text_revive(translate("+1 HEART!!"), 1)
    pygame.mixer.music.stop()

def ask_for_player_name():
    """
    Ask the user to enter their name via a simple Pygame text input loop.
    Returns the name (str) the player entered.
    """
    player_name = ""
    active = True
    clock = pygame.time.Clock()

    input_font = load_font(CONFIG["FONT_SIZE_DEFAULT"])

    while active:
        screen.fill(BLACK)
        
        prompt = translate("Enter your name")
        draw_text(prompt, WIDTH // 2, HEIGHT // 2 - 80, center=True, font_used=small_font)

        draw_text(player_name, WIDTH // 2, HEIGHT // 2, center=True, font_used=input_font)

        # Show instructions: Press ENTER to confirm, ESC to cancel
        draw_text(f"[{translate('Enter')}] {translate('OK')}   [{translate('ESC')}] {translate('Cancel')}",
          WIDTH // 2, HEIGHT // 2 + 80, center=True, font_used=small_font)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_ESCAPE:
                    return ""
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12:
                        player_name += event.unicode

        clock.tick(30)

    return player_name

def insert_score(player_name, score):
    """
    Insert a new score into the scoreboard,
    then keep only top 10 by score (descending).
    """
    db_path = os.path.join(script_dir, "scoreboard.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO scoreboard (player_name, score) VALUES (?, ?)",
                   (player_name, score))
    conn.commit()

    cursor.execute("""
        SELECT id, score FROM scoreboard
        ORDER BY score DESC, id ASC
    """)
    rows = cursor.fetchall()

    if len(rows) > 10:
        ids_to_delete = [row[0] for row in rows[10:]]
        cursor.executemany("DELETE FROM scoreboard WHERE id = ?", [(i,) for i in ids_to_delete])
        conn.commit()

    conn.close()

def check_in_top_10(player_name, score):
    """
    Checks whether the given (player_name, score) tuple appears among the top 10.
    """
    db_path = os.path.join(script_dir, "scoreboard.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, score FROM scoreboard ORDER BY score DESC, id ASC LIMIT 10")
    top_scores = cursor.fetchall()
    conn.close()
    return (player_name, score) in top_scores


def show_scoreboard():
    """
    Displays the top 10 scores from the scoreboard table.
    """
    db_path = os.path.join(script_dir, "scoreboard.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, score FROM scoreboard ORDER BY score DESC, id ASC LIMIT 10")
    top_scores = cursor.fetchall()
    conn.close()

    running = True
    selected = 0

    while running:
        screen.fill(BLACK)

        draw_text(translate("Scoreboard"), WIDTH // 2, 100)

        y_offset = 200
        for index, (p_name, p_score) in enumerate(top_scores):
            line = f"{index+1}. {p_name}: {p_score}"
            draw_text(line, WIDTH // 2, y_offset, center=True, font_used=small_font)
            y_offset += 50

        draw_text(f"[{translate('Back')}] -> {translate('Press C')}",
          WIDTH // 2, HEIGHT - 80, font_used=small_font)


        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False

        pygame.time.Clock().tick(30)



def settings_menu():
    global language, music_enabled
    selected = 0

    while True:
        screen.fill(BLACK)
        settings_options = [translate("Language"), translate("Music"), translate("Back")]
        draw_text(translate("Settings"), WIDTH // 2, 160)

        for i, option in enumerate(settings_options):
            text_width = draw_text(option, WIDTH // 2, 320 + i * 100)
            if i == selected:
                screen.blit(heart_img, (WIDTH // 2 - text_width // 2 - 60, 322 + i * 100))
            if i == selected:
                if option == translate("Language"):
                    draw_text(translate(language), WIDTH // 2 + 200, 320, center=False)
                elif option == translate("Music"):
                    mus_txt = translate("On") if music_enabled else translate("Off")
                    draw_text(mus_txt, WIDTH // 2 + 200, 420, center=False)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % len(settings_options)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % len(settings_options)
                elif event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                    if settings_options[selected] == translate("Language"):
                        language = "English" if language == "Korean" else "Korean"
                        save_user_settings()
                    elif settings_options[selected] == translate("Music"):
                        music_enabled = not music_enabled
                        save_user_settings()
                        if music_enabled:
                            play_menu_music()
                        else:
                            pygame.mixer.music.stop()
                elif event.key == pygame.K_x:
                    if settings_options[selected] == translate("Back"):
                        return

def spawn_food(snake):
    while True:
        x = random.randrange(BORDER_MARGIN + CELL_SIZE, WIDTH - BORDER_MARGIN - CELL_SIZE, CELL_SIZE)
        y = random.randrange(BORDER_MARGIN + CELL_SIZE, HEIGHT - BORDER_MARGIN - CELL_SIZE, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)

def flicker_message(message, score, level, stage):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 1000:
        screen.fill(BLACK)
        pygame.draw.rect(
            screen, WHITE,
            (BORDER_MARGIN, BORDER_MARGIN, WIDTH - 2*BORDER_MARGIN, HEIGHT - 2*BORDER_MARGIN),
            BORDER_THICKNESS
        )
        label_score = "EXP" if language == "English" else translate("Score")
        label_level = "LV" if language == "English" else translate("Level")
        label_stage = "STAGE" if language == "English" else translate("Stage")
        draw_text(f"{label_score}: {score}", 60, 20, center=False)
        draw_text(f"{label_level}: {level}", 300, 20, center=False)
        draw_text(f"{label_stage}: {stage}", 540, 20, center=False)
        screen.blit(heart_img, (WIDTH - 80, 20))
        elapsed = pygame.time.get_ticks() - start_time
        if (elapsed // 100) % 2 == 0:
            draw_text(message, WIDTH // 2, HEIGHT // 2, (255, 255, 0))
        pygame.display.flip()
        clock.tick(30)

def game_loop(player_name):
    global food_in_current_life
    food_in_current_life = 0
    song_path = os.path.join(script_dir, "song.mp3")
    if music_enabled and os.path.isfile(song_path):
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1)

    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = (CELL_SIZE, 0)
    food = spawn_food(snake)
    clock = pygame.time.Clock()
    score = 0
    speed = CONFIG["SNAKE_SPEED_INIT"]
    total_food_eaten = 0
    level = 1
    stage = 1
    direction_changed_this_frame = False

    while True:
        direction_changed_this_frame = False
        screen.fill(BLACK)
        pygame.draw.rect(
            screen, WHITE,
            (BORDER_MARGIN, BORDER_MARGIN, WIDTH - 2*BORDER_MARGIN, HEIGHT - 2*BORDER_MARGIN),
            BORDER_THICKNESS
        )
        label_score = "EXP" if language == "English" else translate("Score")
        label_level = "LV" if language == "English" else translate("Level")
        label_stage = "STAGE" if language == "English" else translate("Stage")
        draw_text(f"{label_score}: {score}", 60, 20, center=False)
        draw_text(f"{label_level}: {level}", 300, 20, center=False)
        draw_text(f"{label_stage}: {stage}", 540, 20, center=False)
        screen.blit(heart_img, (WIDTH - 80, 20))
        player_name_surface = small_font.render(player_name, True, WHITE)
        screen.blit(player_name_surface, (WIDTH - player_name_surface.get_width() - 20, HEIGHT - 40))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return False
            elif event.type == pygame.KEYDOWN:
                if not direction_changed_this_frame:
                    if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                        snake_dir = (0, -CELL_SIZE)
                        direction_changed_this_frame = True
                    elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                        snake_dir = (0, CELL_SIZE)
                        direction_changed_this_frame = True
                    elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                        snake_dir = (-CELL_SIZE, 0)
                        direction_changed_this_frame = True
                    elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                        snake_dir = (CELL_SIZE, 0)
                        direction_changed_this_frame = True

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        # If the snake hits itself or walls:
        if (new_head in snake[1:] or
        new_head[0] < BORDER_MARGIN or
        new_head[1] < BORDER_MARGIN or
        new_head[0] >= WIDTH - BORDER_MARGIN or
        new_head[1] >= HEIGHT - BORDER_MARGIN):

    
            pygame.mixer.music.stop()

            if food_in_current_life >= 20:
                survived, played_death = revival_sequence()
                if survived:
                    snake = [(WIDTH // 2, HEIGHT // 2)]
                    snake_dir = (CELL_SIZE, 0)
                    food = spawn_food(snake)
                    food_in_current_life = 0
                    if music_enabled and os.path.isfile(song_path):
                        pygame.mixer.music.load(song_path)
                        pygame.mixer.music.play(-1)
                    continue
                else:
                    if not played_death:
                        play_death_animation(WIDTH - 80, 20)
                    insert_score(player_name, score)
                    return game_over(score, check_in_top_10(player_name, score))
            else:
                # If revival isn't possible
                play_death_animation(WIDTH - 80, 20)
                insert_score(player_name, score)
                return game_over(score, check_in_top_10(player_name, score))




            

        snake.insert(0, new_head)
        if new_head == food:
            food = spawn_food(snake)
            score += 1
            total_food_eaten += 1
            food_in_current_life += 1
            if total_food_eaten % CONFIG["LEVEL_UP_FOOD_THRESHOLD"] == 0:
                level += 1
                if level > 3:
                    stage += 1
                    level = 1
                    snake = [(WIDTH // 2, HEIGHT // 2)]
                    snake_dir = (CELL_SIZE, 0)
                    food = spawn_food(snake)
                    stageup_path = os.path.join(script_dir, "STAGEUP.mp3")
                    if music_enabled and os.path.isfile(stageup_path):
                        stageup_sound = pygame.mixer.Sound(stageup_path)
                        stageup_sound.set_volume(1.0)
                        stageup_sound.play()
                    flicker_message(translate("STAGE UP!!!"), score, level, stage)
                else:
                    speed += CONFIG["SNAKE_SPEED_LVUP_INCREMENT"]
                    lvup_path = os.path.join(script_dir, "LVUP.mp3")
                    if music_enabled and os.path.isfile(lvup_path):
                        lvup_sound = pygame.mixer.Sound(lvup_path)
                        lvup_sound.set_volume(1.0)
                        lvup_sound.play()
                    flicker_message(translate("LEVEL UP!!!! +SPEED"), score, level, stage)
        else:
            snake.pop()

        for segment in snake:
            pygame.draw.rect(screen, WHITE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(speed)

def game_over(score, in_top_10):
    screen.fill(BLACK)
    gameover_path = os.path.join(script_dir, "gameover.mp3")
    if music_enabled and os.path.isfile(gameover_path):
        pygame.mixer.music.load(gameover_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
    label_score = "EXP" if language == "English" else translate("Score")
    draw_text(f"{label_score}: {score}", WIDTH // 2, HEIGHT // 2 - 80)
    draw_text(translate("Go back? Press C"), WIDTH // 2, HEIGHT // 2 + 60, font_used=small_font)
    if in_top_10:
        draw_text(translate("You made it to the scoreboard!"), WIDTH // 2, HEIGHT // 2 + 120, font_used=small_font)
    else:
        draw_text(translate("You didn't make it to the scoreboard"), WIDTH // 2, HEIGHT // 2 + 120, font_used=small_font)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.mixer.music.stop()
                    return main_menu()

def revival_sequence():
    pygame.mixer.music.stop()
    start_sound_path = os.path.join(script_dir, "revivalstart.mp3")
    revival_path = os.path.join(script_dir, "revival.mp3")

    if os.path.isfile(start_sound_path):
        try:
            start_sound = pygame.mixer.Sound(start_sound_path)
            start_sound.set_volume(1.0)
            if music_enabled:
                start_sound.play()
        except:
            pass

    heart_start = (WIDTH - 80, 20)
    blink_duration = CONFIG["REVIVAL_BLINK_MS"]
    blink_interval = CONFIG["REVIVAL_BLINK_INTERVAL"]
    blink_start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - blink_start_time < blink_duration:
        elapsed = pygame.time.get_ticks() - blink_start_time
        screen.fill(BLACK)
        if (elapsed // blink_interval) % 2 == 1:
            screen.blit(heart_img, heart_start)
        pygame.display.flip()
        pygame.time.delay(30)

    if os.path.isfile(revival_path) and music_enabled:
        try:
            pygame.mixer.music.load(revival_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
        except:
            pass

    heart_center = (WIDTH // 2 - 22, HEIGHT // 2 - 22)
    start_time = pygame.time.get_ticks()
    duration = CONFIG["ANIM_HEART_TRANSITION_MS"]
    while pygame.time.get_ticks() - start_time < duration:
        t = (pygame.time.get_ticks() - start_time) / duration
        x = int(heart_start[0] * (1 - t) + heart_center[0] * t)
        y = int(heart_start[1] * (1 - t) + heart_center[1] * t)
        screen.fill(BLACK)
        screen.blit(heart_img, (x, y))
        pygame.display.flip()
        pygame.time.delay(10)

    flashing_text_revive(translate("SURVIVE!!!"), 1)

    survived, already_played = revive_game(game_time=10)

    if survived:
        flashing_text_revive(translate("+1 HEART!!"), 1)
        heal_path = os.path.join(script_dir, "heal.mp3")
        if music_enabled and os.path.isfile(heal_path):
            heal_sound = pygame.mixer.Sound(heal_path)
            heal_sound.set_volume(1.0)
            heal_sound.play()
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration:
            t = (pygame.time.get_ticks() - start_time) / duration
            x = int(heart_center[0] * (1 - t) + heart_start[0] * t)
            y = int(heart_center[1] * (1 - t) + heart_start[1] * t)
            screen.fill(BLACK)
            screen.blit(heart_img, (x, y))
            pygame.display.flip()
            pygame.time.delay(10)
        pygame.mixer.music.stop()
        already_played = False
        return (survived, already_played)


    already_played = True
    return (False, already_played)



def flashing_text_revive(message, duration=1):
    local_font = pygame.font.Font("./Chara.ttf", 50)
    start_timev = time.time()
    while time.time() - start_timev < duration:
        screen.fill(BLACK)
        if int(time.time() * 4) % 2 == 0:
            text = local_font.render(message, True, (255, 255, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def revive_game(game_time=10):
    # This used to be completely separate project but it seemed fitting with what I was going for so.. Here it is
    heart_img_revive = pygame.image.load("./heart.png")
    bone_img = pygame.image.load("./bone.png")
    player_size = 40
    heart_img_revive = pygame.transform.scale(heart_img_revive, (player_size, player_size))
    bone_width = 40
    bone_height = 100
    bone_img = pygame.transform.scale(bone_img, (bone_width, bone_height))

    BLACK2 = (0, 0, 0)
    WHITE2 = (255, 255, 255)
    YELLOW2 = (255, 255, 0)
    clock2 = pygame.time.Clock()
    funny_font = pygame.font.Font("./funny.ttf", 50)
    arena_width = 600
    arena_height = 400
    border_left2 = (WIDTH // 2) - (arena_width // 2)
    border_right2 = border_left2 + arena_width
    border_top2 = (HEIGHT // 2) - (arena_height // 2)
    border_bottom2 = border_top2 + arena_height
    ground_y = border_bottom2 - 20

    player_x = (border_left2 + border_right2) // 2
    player_y = ground_y - player_size
    player_vel_x = 0
    player_vel_y = 0
    jump_power = CONFIG["JUMP_POWER"]
    gravity = CONFIG["GRAVITY"]
    on_ground = False
    bone_speed = CONFIG["BONE_SPEED"]
    bones = []
    bone_spawn_timer = 0
    start_ticks = pygame.time.get_ticks()
    chara_font2 = pygame.font.Font("./Chara.ttf", 50)

    def draw_player(x, y):
        screen.blit(heart_img_revive, (x, y))

    def draw_bones():
        for b in bones:
            screen.blit(bone_img, (b.x, b.y))

    def draw_border():
        pygame.draw.rect(screen, WHITE2, (border_left2, border_top2, arena_width, arena_height), 5)

    def draw_timer():
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, game_time - elapsed_time)
        timer_text = chara_font2.render(str(remaining_time), True, YELLOW2)
        screen.blit(timer_text, (border_right2 - 60, border_top2 + 10))
        return remaining_time

    def flashing_text_custom_font(msg, dur, the_font):
        st = time.time()
        while time.time() - st < dur:
            screen.fill(BLACK2)
            if int(time.time() * 4) % 2 == 0:
                txt_surf = the_font.render(msg, True, YELLOW2)
                rect = txt_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(txt_surf, rect)
            pygame.display.flip()
            clock2.tick(30)

    def check_collision():
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for b in bones:
            if player_rect.colliderect(b):
                pygame.mixer.music.stop()
                play_death_animation(player_x, player_y)
                of_course = translate("of course")
                flashing_text_custom_font(of_course, 1, funny_font)
                return True
        return False

    running = True
    while running:
        screen.fill(BLACK2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_vel_x = -CONFIG["PLAYER_VELOCITY_X"]
                elif event.key == pygame.K_RIGHT:
                    player_vel_x = CONFIG["PLAYER_VELOCITY_X"]
                elif event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = jump_power
                    on_ground = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player_vel_x = 0

        player_y += player_vel_y
        if player_y + player_size >= ground_y:
            player_y = ground_y - player_size
            on_ground = True
            player_vel_y = 0
        else:
            player_vel_y += gravity

        player_x += player_vel_x
        if player_x < border_left2:
            player_x = border_left2
        if player_x + player_size > border_right2:
            player_x = border_right2 - player_size
        if player_y < border_top2:
            player_y = border_top2

        bone_spawn_timer += 1
        if bone_spawn_timer > CONFIG["BONE_SPAWN_INTERVAL"]:
            bones.append(pygame.Rect(border_right2, ground_y - bone_height, bone_width, bone_height))
            bone_spawn_timer = 0

        for b in bones:
            b.x -= bone_speed
        bones = [b for b in bones if b.x > border_left2 - bone_width]

        draw_border()
        draw_player(player_x, player_y)
        draw_bones()
        remain = draw_timer()
        if check_collision():
            return False, True
        if remain == 0:
            return True, False

        pygame.display.flip()
        clock2.tick(60)
    return False

def flashing_text_revive(message, duration=1):
    # Uh..
    local_font = pygame.font.Font("./Chara.ttf", 50)
    start_timev = time.time()
    while time.time() - start_timev < duration:
        screen.fill(BLACK)
        if int(time.time() * 4) % 2 == 0:
            text = local_font.render(message, True, (255, 255, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def main():
    initialize_db()
    load_user_settings()
    intro_sequence()
    main_menu()
    pygame.quit()


if __name__ == "__main__":
    main()
    # good job getting to the end!