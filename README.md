# Uonet+ Vulcan integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

View your vulcan timetable as Home Assistant sensor and use it in automations.

# Timetable
You can get ten entities witch timetable. 
If you want to configure groups and student for which the information will be displayed (default is first on vulcan list), you must add this to your configuration.yaml file.
```
vulcan:
  student_name: '<student name'> #Optional If is incorrect or none default is first in Vulcan list.
  groups: #optional
    1:
      'J. angielski- p.rozsz': '2A9'
    2:
      'Język niemiecki': '2NH'
    3:
      'Język francuski': 'None'
    4:
      'Wychowanie fizyczne': 'WF-ch'
    5:
      'Religia': 'r22p'
    6:
      'Informatyka': 'I2'
```
# Graders
Available soon
