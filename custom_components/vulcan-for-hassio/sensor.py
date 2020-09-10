from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import json
from vulcan import Vulcan
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import (
    CONF_STUDENT_NAME,
)

def get_lesson_info(self, int_number):
    with open('vulcan.json') as f:
        certificate = json.load(f)
    client = Vulcan(certificate)

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

    en_group = '2A9'
    it_group = 'I2'
    rel_group = 'r22p'
    de_group = '2NH'
    fr_group = 'None'
    pe_group = 'Wf-ch'
    for Lesson in client.get_lessons():
        temp_dict = {}
        temp_dict['number'] = Lesson.number
        lesson = str(Lesson.number)
        temp_dict['lesson'] = Lesson.subject.name
        temp_dict['room'] = Lesson.room
        temp_dict['group'] = Lesson.group
        temp_dict['teacher'] = Lesson.teacher.name
        temp_dict['time'] = Lesson.time.from_.strftime("%H:%M") + '-' + Lesson.time.to.strftime("%H:%M")
        if temp_dict['lesson'] == 'Informatyka':
            if temp_dict['group'] == it_group or temp_dict['group'] == 'None':
                setattr(self, 'lesson_' + lesson, temp_dict)
        elif temp_dict['lesson'] == 'J. angielski- p.rozsz':
            if temp_dict['group'] == en_group or temp_dict['group'] == 'None':
                setattr(self, 'lesson_' + lesson, temp_dict)
        elif temp_dict['lesson'] == 'Religia':
            if temp_dict['group'] == rel_group or temp_dict['group'] == 'None':
                setattr(self, 'lesson_' + lesson, temp_dict)
        elif temp_dict['lesson'] == 'Język niemiecki':
            if temp_dict['group'] == de_group or temp_dict['group'] == 'None':
                setattr(self, 'lesson_' + lesson, temp_dict)
        elif temp_dict['lesson'] == 'Wychowanie fizyczne':
            if temp_dict['group'] == pe_group or temp_dict['group'] == 'None':
                setattr(self, 'lesson_' + lesson, temp_dict)
        elif temp_dict['lesson'] == 'Język francuski':
            if temp_dict['group'] == fr_group or temp_dict['group'] == 'None':
                setattr(self, 'lesson_' + lesson, temp_dict)
        else:
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
    
    if self.lesson_1['number'] == int_number:
        lesson_ans = self.lesson_1
    elif self.lesson_2['number'] == int_number:
        lesson_ans = self.lesson_2
    elif self.lesson_3['number'] == int_number:
        lesson_ans = self.lesson_3
    elif self.lesson_4['number'] == int_number:
        lesson_ans = self.lesson_4
    elif self.lesson_5['number'] == int_number:
        lesson_ans = self.lesson_5
    elif self.lesson_6['number'] == int_number:
        lesson_ans = self.lesson_6
    elif self.lesson_7['number'] == int_number:
        lesson_ans = self.lesson_7
    elif self.lesson_8['number'] == int_number:
        lesson_ans = self.lesson_8
    elif self.lesson_9['number'] == int_number:
        lesson_ans = self.lesson_9
    elif self.lesson_10['number'] == int_number:
        lesson_ans = self.lesson_10
    return lesson_ans


def get_id(self):
    with open('vulcan.json') as f:
        certificate = json.load(f)
    client = Vulcan(certificate)
    for Student in client.get_students():
        id = Student.id
    return str(id)
    

    
def setup_platform(hass, config, add_entities, discovery_info=None):
#    Set up the sensor platform.
    if discovery_info is None:
        return
    add_entities([Lesson1()])
    add_entities([Lesson2()])
    add_entities([Lesson3()])
    add_entities([Lesson4()])
    add_entities([Lesson5()])
    add_entities([Lesson6()])
    add_entities([Lesson7()])
    add_entities([Lesson8()])
    add_entities([Lesson9()])
    add_entities([Lesson10()])
 

class Lesson1(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 1'

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_1_' + id

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 1)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    
    
    def update(self):
        lesson_1 = get_lesson_info(self, 1)
    
        self._state = lesson_1['lesson']


class Lesson2(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 2'
        
    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_2_' + id
     
    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 2)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr

    @property
    def icon(self):
        return 'mdi:timetable'
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_2 = get_lesson_info(self, 2)
    
        self._state = lesson_2['lesson']


class Lesson3(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 3'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_3_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 3)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_3 = get_lesson_info(self, 3)
    
        self._state = lesson_3['lesson']


class Lesson4(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 4'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_4_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 4)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_4 = get_lesson_info(self, 4)
    
        self._state = lesson_4['lesson']


class Lesson5(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 5'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_5_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 5)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_5 = get_lesson_info(self, 5)
    
        self._state = lesson_5['lesson']


class Lesson6(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 6'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_6_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 6)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_6 = get_lesson_info(self, 6)
    
        self._state = lesson_6['lesson']




class Lesson7(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 7'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_7_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 7)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_7 = get_lesson_info(self, 7)
    
        self._state = lesson_7['lesson']



class Lesson8(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 8'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_8_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 8)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_8 = get_lesson_info(self, 8)
    
        self._state = lesson_8['lesson']



class Lesson9(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 9'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_9_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 9)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_9 = get_lesson_info(self, 9)
    
        self._state = lesson_9['lesson']



class Lesson10(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Lesson 10'

    @property
    def unique_id(self):
        id = get_id(self)
        return 'lesson_10_' + id

    @property
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        lesson_info = get_lesson_info(self, 10)
        atr = {
            "room": lesson_info['room'],
            "teacher": lesson_info['teacher'],
            "time": lesson_info['time']
        }
        return atr
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        lesson_10 = get_lesson_info(self, 10)
    
        self._state = lesson_10['lesson']
