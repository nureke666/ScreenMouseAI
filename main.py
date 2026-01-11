#!/usr/bin/env python3
import os
import sys
import re
import io
import threading
import time
import itertools
import math
import platform
import google.generativeai as genai
import pyautogui
from pynput import keyboard
from mss import mss
from PIL import Image
from config import (
    GEMINI_KEYS,
    MODEL_VERSION,
    MOVE_PIXELS,
    PAUSE_BETWEEN_QUESTIONS,
    PAUSE_BETWEEN_ACTIONS,
    MOVE_DURATION,
    CURVE_STRENGTH,
    FORCE_RESET_TIMEOUT,
    PROMPT
)

# --- Определение системы ---
SYSTEM = platform.system()
print(f"Запущено на ОС: {SYSTEM}")

# Адаптация скролла
if SYSTEM == 'Windows':
    SCROLL_AMOUNT_DOWN = -100
    SCROLL_AMOUNT_UP = 100
else:
    SCROLL_AMOUNT_DOWN = -5
    SCROLL_AMOUNT_UP = 5

if GEMINI_KEYS:
    gemini_key_cycle = itertools.cycle(GEMINI_KEYS)
else:
    gemini_key_cycle = None
    print("⚠️  Внимание: Ключи Gemini не найдены в .env")

pyautogui.PAUSE = 0.0

# --- Глобальные переменные ---
is_processing = False
is_awaiting_exit_confirmation = False
processing_start_time = 0
current_request_id = 0

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def move_mouse_smoothly_curved(dx, dy):
    try:
        start_x, start_y = pyautogui.position()
        end_x, end_y = start_x + dx, start_y + dy
        mid_x, mid_y = start_x + dx / 2, start_y + dy / 2
        dist = math.hypot(dx, dy)
        if dist == 0: dist = 1
        control_x = mid_x - CURVE_STRENGTH * (dy / dist)
        control_y = mid_y + CURVE_STRENGTH * (dx / dist)

        num_points = 20
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            x = (1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * end_x
            y = (1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * end_y
            points.append((x, y))

        time_per_point = MOVE_DURATION / len(points)
        for x, y in points:
            pyautogui.moveTo(x, y)
            time.sleep(time_per_point)
    except pyautogui.FailSafeException:
        pass


def perform_mouse_action(result_text):
    lines = result_text.strip().split('\n')
    for line in lines:
        try:
            line_lower = line.lower()

            # --- ЛОГИКА TRUE / FALSE ---
            if 'true' in line_lower:
                move_mouse_smoothly_curved(0, -MOVE_PIXELS)  # Двигаем вверх
                time.sleep(PAUSE_BETWEEN_QUESTIONS)
                continue  # Переходим к след. строке, буквы искать не нужно

            if 'false' in line_lower:
                move_mouse_smoothly_curved(0, MOVE_PIXELS)  # Двигаем вниз
                time.sleep(PAUSE_BETWEEN_QUESTIONS)
                continue

            # --- ЛОГИКА A, B, C, D ---
            answer_letters = re.findall(r'\b[a-f]\b', line_lower)
            for letter in answer_letters:
                letter = letter.strip()
                if letter == 'a':
                    move_mouse_smoothly_curved(0, -MOVE_PIXELS)  # Вверх
                elif letter == 'b':
                    move_mouse_smoothly_curved(MOVE_PIXELS, 0)  # Вправо
                elif letter == 'c':
                    move_mouse_smoothly_curved(0, MOVE_PIXELS)  # Вниз
                elif letter == 'd':
                    move_mouse_smoothly_curved(-MOVE_PIXELS, 0)  # Влево
                elif letter == 'e':
                    pyautogui.scroll(SCROLL_AMOUNT_DOWN)
                elif letter == 'f':
                    pyautogui.scroll(SCROLL_AMOUNT_UP)
                time.sleep(PAUSE_BETWEEN_ACTIONS)
            time.sleep(PAUSE_BETWEEN_QUESTIONS)
        except Exception as e:
            print(f"Ошибка в действии: {e}")


def analyze_task(my_request_id):
    global is_processing, current_request_id
    try:
        if gemini_key_cycle:
            new_key = next(gemini_key_cycle)
            genai.configure(api_key=new_key)
            local_model = genai.GenerativeModel(MODEL_VERSION)
            print(f"🔑 Смена ключа. Использую ключ, заканчивающийся на ...{new_key[-4:]}")
        else:
            print("Ошибка: Нет ключей!")
            return

        with mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

        image_part = {"mime_type": "image/png", "data": img_byte_arr}
        prompt_parts = [PROMPT, image_part]

        print("Запрос отправлен...")

        response = local_model.generate_content(
            prompt_parts,
            request_options={"timeout": 45}
        )

        if my_request_id != current_request_id:
            return

        result_text = response.text
        print(f"Ответ:\n{result_text}")
        perform_mouse_action(result_text)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if my_request_id == current_request_id:
            is_processing = False
            print("Готово. Ожидание F9.")


def on_press(key):
    global is_processing, is_awaiting_exit_confirmation, processing_start_time, current_request_id

    if key == keyboard.Key.f8:
        restart_program()
        return

    if is_awaiting_exit_confirmation:
        if key == keyboard.Key.f9:
            return False
        else:
            is_awaiting_exit_confirmation = False
            return

    if key == keyboard.Key.f9:
        current_time = time.time()
        if is_processing and (current_time - processing_start_time > FORCE_RESET_TIMEOUT):
            is_processing = False

        if not is_processing:
            is_processing = True
            processing_start_time = current_time
            current_request_id += 1
            threading.Thread(target=analyze_task, args=(current_request_id,)).start()

    elif key == keyboard.Key.esc:
        is_awaiting_exit_confirmation = True
        print("Нажмите F9 для выхода, любую клавишу для отмены.")


def on_release(key):
    pass


if __name__ == "__main__":
    if SYSTEM == 'Linux' and os.environ.get('XDG_SESSION_TYPE') == 'wayland':
        print("\n!!! ВНИМАНИЕ: Wayland !!! Переключитесь на Xorg.\n")

    print("Скрипт готов (True=Вверх, False=Вниз). Нажмите F9.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()