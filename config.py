#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# --- API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_VERSION = 'gemini-2.5-flash'

# --- Mouse Settings ---
MOVE_PIXELS = 35
PAUSE_BETWEEN_QUESTIONS = 3.0
PAUSE_BETWEEN_ACTIONS = 0.75
MOVE_DURATION = 0.5
CURVE_STRENGTH = 8

# --- Timeouts ---
FORCE_RESET_TIMEOUT = 30

# --- Prompt ---
PROMPT = """
Проанализируй это изображение с тестом.
Ответ предоставь строго в формате, где каждая строка соответствует одному вопросу.

Правила форматирования:
1. Если вопрос с вариантами A, B, C, D: 
   - Напиши только букву ответа.
   - Если ответов несколько, перечисли буквы через запятую БЕЗ пробелов (пример: a,c,d).

2. Если вопрос типа True/False (Верно/Неверно):
   - Если ответ True (Верно/Истина) -> пиши строго слово: TRUE
   - Если ответ False (Неверно/Ложь) -> пиши строго слово: FALSE
"""