# Подключаем модуль для Телеграма, Яндекса
import telebot
import random
import glob, os
import sys
import time
from datetime import datetime
import sqlite3 as sl
# Указываем токены
import os

from dotenv import load_dotenv

load_dotenv()
# Теперь переменная TOKEN, описанная в файле .env,
# доступна в пространстве переменных окружения

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
#from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re

#Обрабатываем старт
@bot.message_handler(content_types=['text'])
def get_start_messages(message):
  if message.text == "/start":
    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст и обработчик для каждого пунка меню
    key_zakaz = types.InlineKeyboardButton(text='Мне нужны материалы от заказчика',
                                         callback_data='zakazchik')
    # И добавляем кнопку на экран
    keyboard.add(key_zakaz)
    key_doc = types.InlineKeyboardButton(text='Мне нужны примеры документов',
                                         callback_data='doc')
    keyboard.add(key_doc)
    key_dog = types.InlineKeyboardButton(text='Просто хочу посмотреть милоту 🐶 🐱',
                                         callback_data='dog')
    keyboard.add(key_dog)
    bot.send_message(
        message.from_user.id,
        text=
        'Привет! Это бот-помощник 👻 Чем тебе помочь?',
        reply_markup=keyboard)
  elif message.text == "/help":
    bot.send_message(message.from_user.id, "Для взаимодействия с меню бота, необходимо нажать команду меню /start")
  elif message.text == "/about":
    bot.send_message(message.from_user.id, "Этот бот создан для помощи в работе. В нем можно найти как документацию от заказчика по проектам, так и шаблоны и образцы документов, которые нужно написать на разных фазах. Для перехода к запуску бота-помощника нажми команду меню /start. Для поддержки автора бота, напиши аккаунту @ksakharova")
  else:
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")

def get_url_dog():
  contents = requests.get('https://random.dog/woof.json').json()
  url = contents['url']
  return url

def get_url_cat():
  response = requests.get('https://api.thecatapi.com/v1/images/search').json()
  random_cat = response[0].get('url')
  return random_cat

def random_animal():
    animal = [get_url_cat(), get_url_dog()]
    return random.choice(animal)

#def search_word(word):
   # if word

    # Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
  # Если нажали на одну из 2 кнопок, выбираем 1ый или 2ой путь
  if call.data == "zakazchik":
    msg1 = 'Выбери проект, по которому тебе нужны документы'
        # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    key_pr_1 = types.InlineKeyboardButton(text='Проект_1', callback_data='proekt_1')
    keyboard.add(key_pr_1)
    key_pr_2 = types.InlineKeyboardButton(text='Проект_2', callback_data='proekt_2')
    keyboard.add(key_pr_2)
    bot.send_message(call.message.chat.id, msg1, reply_markup=keyboard)
  elif call.data == "doc":
      msg4 = ('Введите слово, по которому осуществить поиск')
      bot.send_message(call.message.chat.id, msg4)
  elif call.data == "dog":
      bot.send_photo(call.message.chat.id, photo=random_animal())
  elif call.data == "proekt_1":
      doc = open('Document_1_Proj_1.docx', 'rb')
      bot.send_document(call.message.chat.id, doc)
  elif call.data == "proekt_2":
      doc = open('Document_1_Proj_2.docx', 'rb')
      bot.send_document(call.message.chat.id, doc)
  elif call.data == "proekt_2":
    bot.send_message(call.message.chat.id, document=get_proj_1())

bot.polling(none_stop=True, interval=0)