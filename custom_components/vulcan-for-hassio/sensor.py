"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import json
from vulcan import Vulcan
from homeassistant.helpers import config_validation as cv, entity_platform, service

with open('vulcan.json') as f:
    certificate = json.load(f)
client = Vulcan(certificate)



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
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    
    
    def update(self):
        import json
        from vulcan import Vulcan
        with open('vulcan.json') as f:
            certificate = json.load(f)
        client = Vulcan(certificate)
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
            temp_dict['time'] = Lesson.time.from_.strftime("%H:%M"), '-', Lesson.time.to.strftime("%H:%M")
            if temp_dict['lesson'] == 'Informatyka':
                if temp_dict['group'] == it_group or temp_dict['group'] == 'None':
                    exec('lesson_' + lesson + " = temp_dict")
            elif temp_dict['lesson'] == 'J. angielski- p.rozsz':
                if temp_dict['group'] == en_group or temp_dict['group'] == 'None':
                    exec('lesson_' + lesson + " = temp_dict")
            elif temp_dict['lesson'] == 'Religia':
                if temp_dict['group'] == rel_group or temp_dict['group'] == 'None':
                    exec('lesson_' + lesson + " = temp_dict")
            elif temp_dict['lesson'] == 'Język niemiecki':
                if temp_dict['group'] == de_group or temp_dict['group'] == 'None':
                    exec('lesson_' + lesson + " = temp_dict")
            elif temp_dict['lesson'] == 'Wychowanie fizyczne':
                if temp_dict['group'] == pe_group or temp_dict['group'] == 'None':
                    exec('lesson_' + lesson + " = temp_dict")
            elif temp_dict['lesson'] == 'Język francuski':
                if temp_dict['group'] == fr_group or temp_dict['group'] == 'None':
                    exec('lesson_' + lesson + " = temp_dict")
            else:
                exec('lesson_' + lesson + " = temp_dict")
    
        self._state = str(lesson_1['lesson'])


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'



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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'


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
    def icon(self):
        return 'mdi:timetable'

    @property
    def device_state_attributes(self):
        test = {
            "room": "3",
            "teacher": "E. K",
            "time": "8.00-8.45"
        }
        return test
    
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 'lesson'
