# coding=utf-8
import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup
from typing import List, Tuple



bot = telebot.TeleBot(config.access_token)
#telebot.apihelper.proxy = {'https': 'https://162.243.64.151:3128'}

def get_page(group: str, week: str='') -> str:
    if week:
        week = str(week) + '/'
    url = f'{config.domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'
    response = requests.get(url)
    web_page = response.text
    return web_page

def get_week() -> str:
    url = 'http://www.ifmo.ru/ru/schedule/0/K3141/1/raspisanie_zanyatiy_K3141.htm'
    response = requests.get(url)
    web_page = response.text
    soup = BeautifulSoup(web_page, "html5lib")
    string = str(soup.select_one(".schedule-week"))
    
    if string.find("Нечетная") != -1:
        return "2"
    else:
        return "1"

def get_schedule(web_page: str, weekday: str) -> Tuple[List[str], List[str], List[str]]:
    soup = BeautifulSoup(web_page, "html5lib")
    day_id = str(weekday) + "day"
    # Получаем таблицу с расписанием 
    schedule_table = soup.find("table", attrs={"id": day_id})
    if schedule_table is None:
        return None
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
    return times_list, locations_list, lessons_list



@bot.message_handler(commands=['near_lesson'])
def get_near_lesson(message: str) -> None:
    _, group = message.text.split()
    weekday = datetime.datetime.today().weekday() + 1
    week = get_week()
    web_page = get_page(group, week)
    if web_page is None:
        bot.send_message(message.chat.id, "Группа введена неправильно", parse_mode='HTML')
    else:
        flag = 0
        current_schedule = get_schedule(web_page, weekday)
        if current_schedule:
            times_lst, locations_lst, lessons_lst = current_schedule
            a = str(datetime.datetime.now().time())
            b = int(a[0:2] + a[3:5]) #Текущее время
            for i in range(len(times_lst)):
                if b < int(times_lst[i][6:8] + times_lst[i][9:11]):
                    resp = ''
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    flag = 1
                    break
        if flag == 0:            
            while True:
                if weekday == 7:
                    weekday = 1
                    if week == 1:
                        week = 2
                    else:
                        week = 1
                else:
                    weekday += 1

                current_schedule = get_schedule(web_page, weekday)
                if current_schedule:
                    times_lst, locations_lst, lessons_lst = current_schedule
                    resp = ''
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    break
                
@bot.message_handler(commands=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'])       
def get_weekday_schedule(message: str) -> None:
    weekday, week, group = message.text.split()
    A = ['/monday','/tuesday','/wednesday','/thursday','/friday','/saturday','/sunday']
    for i in range (7):
        if weekday == A[i]:
            weekday = i+1
    if week == 0:
        week = ''
    web_page = get_page(group, week)
    if web_page is None:
        bot.send_message(message.chat.id, "Группа введена неправильно", parse_mode='HTML')
    else:
        current_schedule = get_schedule(web_page, weekday)
        if current_schedule is None:
            bot.send_message(message.chat.id, "В этот день пар нет", parse_mode='HTML')            
        else:
            times_lst, locations_lst, lessons_lst = current_schedule
            resp = ''
            for i in range (len(times_lst)):
                resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    

@bot.message_handler(commands=['tommorow'])
def get_tommorow(message: str) -> None:
    _, group = message.text.split()
    weekday = datetime.datetime.today().weekday() + 2
    week = get_week()
    if weekday == 8 or weekday == 7:
        weekday = 1
        if week == 1:
            week = 2
        else:
            week = 1
    if week == 0:
        week = ''
    web_page = get_page(group, week)
    if web_page is None:
        bot.send_message(message.chat.id, "Группа введена неправильно", parse_mode='HTML')
    else:
        current_schedule = get_schedule(web_page, weekday)
        if current_schedule is None:
            bot.send_message(message.chat.id, "В этот день пар нет", parse_mode='HTML')            
        else:
            times_lst, locations_lst, lessons_lst = current_schedule
            resp = ''
            for i in range (len(times_lst)):
                resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_week_schedule(message: str) -> None:
    _, week, group = message.text.split()
    if week == 0:
        week = ''
    
    web_page = get_page(group, week)
    if web_page is None:
        bot.send_message(message.chat.id, "Группа введена неправильно", parse_mode='HTML')
    else:
        resp = ''
        for weekday in range(1,7):
            current_schedule = get_schedule(web_page, weekday)
            if current_schedule is None:
                continue         
            else:
                times_lst, locations_lst, lessons_lst = current_schedule
                
                for i in range (len(times_lst)):
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        



if __name__ == '__main__':
    bot.polling()
