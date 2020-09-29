from homeassistant.helpers.entity import Entity
import json
from vulcan import Vulcan
from datetime import datetime  
from datetime import timedelta 
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import (
    CONF_STUDENT_NAME,
)
from .__init__ import client
from . import DOMAIN

def get_lesson_info(self, days_to_add=0):
    self.lesson_1 = {}
    self.lesson_2 = {}
    self.lesson_3 = {}
    self.lesson_4 = {}
    self.lesson_5 = {}
    self.lesson_6 = {}
    self.lesson_7 = {}
    self.lesson_8 = {}
    self.lesson_9 = {}
    self.lesson_10 = {}

    for Lesson in client.get_lessons(datetime.now() + timedelta(days=days_to_add)):
        temp_dict = {}
        temp_dict['number'] = Lesson.number
        lesson = str(Lesson.number)
        temp_dict['lesson'] = Lesson.subject.name
        temp_dict['room'] = Lesson.room
        temp_dict['group'] = Lesson.group
        temp_dict['teacher'] = Lesson.teacher.name
        temp_dict['time'] = Lesson.time.from_.strftime("%H:%M") + '-' + Lesson.time.to.strftime("%H:%M")
        if self.groups is not {}:
            i = 1
            for x in self.groups:
                setattr(self, 'group_subject_name', next(iter(self.groups[i])))
                setattr(self, 'group_name', self.groups[i][next(iter(self.groups[i]))])
                i+=1
                if temp_dict['lesson'] == self.group_subject_name:
                    if temp_dict['group'] == self.group_name:
                        setattr(self, 'lesson_' + lesson, temp_dict)
                    
        if temp_dict['group'] == 'None' or temp_dict['group'] == None:
            setattr(self, 'lesson_' + lesson, temp_dict)


    lesson_ans = {}
    if self.lesson_1 ==  {}:
        self.lesson_1 = {'number': 1, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_2 ==  {}:
        self.lesson_2 = {'number': 2, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_3 ==  {}:
        self.lesson_3 = {'number': 3, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_4 ==  {}:
        self.lesson_4 = {'number': 4, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_5 ==  {}:
        self.lesson_5 = {'number': 5, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_6 ==  {}:
        self.lesson_6 = {'number': 6, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_7 ==  {}:
        self.lesson_7 = {'number': 7, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_8 ==  {}:
        self.lesson_8 = {'number': 8, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_9 ==  {}:
        self.lesson_9 = {'number': 9, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_10 ==  {}:
        self.lesson_10 = {'number': 10, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
        
    i = 1
    for _ in range (10):
        dict_ans = {
        'lesson_1': self.lesson_1,
        'lesson_2': self.lesson_2,
        'lesson_3': self.lesson_3,
        'lesson_4': self.lesson_4,
        'lesson_5': self.lesson_5,
        'lesson_6': self.lesson_6,
        'lesson_7': self.lesson_7,
        'lesson_8': self.lesson_8,
        'lesson_9': self.lesson_9,
        'lesson_10': self.lesson_10
    
        }
    return dict_ans


def get_t_lesson_info(self):
    self.lesson_1 = {}
    self.lesson_2 = {}
    self.lesson_3 = {}
    self.lesson_4 = {}
    self.lesson_5 = {}
    self.lesson_6 = {}
    self.lesson_7 = {}
    self.lesson_8 = {}
    self.lesson_9 = {}
    self.lesson_10 = {}

    for Lesson in client.get_lessons(datetime.now() + timedelta(days=1)):
        temp_dict = {}
        temp_dict['number'] = Lesson.number
        lesson = str(Lesson.number)
        temp_dict['lesson'] = Lesson.subject.name
        temp_dict['room'] = Lesson.room
        temp_dict['group'] = Lesson.group
        temp_dict['teacher'] = Lesson.teacher.name
        temp_dict['time'] = Lesson.time.from_.strftime("%H:%M") + '-' + Lesson.time.to.strftime("%H:%M")
        if self.groups is not {}:
            i = 1
            for x in self.groups:
                setattr(self, 'group_subject_name', next(iter(self.groups[i])))
                setattr(self, 'group_name', self.groups[i][next(iter(self.groups[i]))])
                i+=1
                if temp_dict['lesson'] == self.group_subject_name:
                    if temp_dict['group'] == self.group_name:
                        setattr(self, 'lesson_' + lesson, temp_dict)
                    
        if temp_dict['group'] == 'None' or temp_dict['group'] == None:
            setattr(self, 'lesson_' + lesson, temp_dict)


    lesson_ans = {}
    if self.lesson_1 ==  {}:
        self.lesson_1 = {'number': 1, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_2 ==  {}:
        self.lesson_2 = {'number': 2, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_3 ==  {}:
        self.lesson_3 = {'number': 3, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_4 ==  {}:
        self.lesson_4 = {'number': 4, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_5 ==  {}:
        self.lesson_5 = {'number': 5, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_6 ==  {}:
        self.lesson_6 = {'number': 6, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_7 ==  {}:
        self.lesson_7 = {'number': 7, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_8 ==  {}:
        self.lesson_8 = {'number': 8, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_9 ==  {}:
        self.lesson_9 = {'number': 9, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
    if self.lesson_10 ==  {}:
        self.lesson_10 = {'number': 10, 'lesson': '-', 'room': '-', 'group': '-', 'teacher': '-', 'time': '-'}
        
    i = 1
    for _ in range (10):
        dict_ans = {
        'lesson_1': self.lesson_1,
        'lesson_2': self.lesson_2,
        'lesson_3': self.lesson_3,
        'lesson_4': self.lesson_4,
        'lesson_5': self.lesson_5,
        'lesson_6': self.lesson_6,
        'lesson_7': self.lesson_7,
        'lesson_8': self.lesson_8,
        'lesson_9': self.lesson_9,
        'lesson_10': self.lesson_10
    
        }
    return dict_ans
    
    
def get_id():
    for Student in client.get_students():
        id = Student.id
    return str(id)
    
    
def get_latest_grade(self):
    self.latest_grade = {}

    for grade in client.get_grades():
        temp_dict = {}
        temp_dict['content'] = grade.content
        temp_dict['weight'] = grade.weight
        temp_dict['description'] = grade.description
        temp_dict['value'] = grade.value
        temp_dict['teacher'] = grade.teacher.name
        temp_dict['subject'] = grade.subject.name
        temp_dict['date'] = grade.date
        setattr(self, 'latest_grade', temp_dict)
                    
    if self.latest_grade ==  {}:
        self.latest_grade = {'content': '-', 'date': '-', 'weight': '-', 'description': '-', 'subkect': '-', 'teacher': '-', 'value': 0}
    
    return self.latest_grade


def get_latest_message(self):
    self.latest_message = {}

    for message in client.get_messages():
        temp_dict = {}
        temp_dict['title'] = message.title
        temp_dict['content'] = message.content
        if message.sender is not None:
            temp_dict['sender'] = message.sender.name
        else:
            temp_dict['sender'] = 'Nieznany'
        temp_dict['date'] = message.sent_date.strftime("%Y.%m.%d") + ' ' + message.sent_time.strftime("%H:%M")
        setattr(self, 'latest_message', temp_dict)
                    
    if self.latest_message ==  {}:
        self.latest_message = {'content': '-', 'date': '-', 'weight': '-', 'description': '-', 'subkect': '-', 'teacher': '-', 'value': 0}
    
    return self.latest_message
    
