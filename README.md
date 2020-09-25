# Uonet+ Vulcan integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

View your vulcan timetable as Home Assistant sensors and use it in automations.  

To get started login as mobile app in Integrations page, and reboot Home Assistant.

# Timetable
You can get ten entities witch timetable. 
If you want to configure groups and student for which the information will be displayed (default is first on vulcan list), you must add this to your configuration.yaml file to configure groups you must add numbers before group.  
  
example:
```
vulcan:
  student_name: 'Jan Kowalski' #Optional, If is incorrect or none default is first in Vulcan list.
  groups: #optional
    1:
      'J. angielski- p.rozsz': 'A1'
    2:
      'Język niemiecki': 'NA'
    3:
      'Język francuski': 'None' 
    4:
      'Wychowanie fizyczne': 'WF-ch'
    5:
      'Religia': '1'
    6:
      'Informatyka': 'I1'
```  
![screenshot](https://raw.githubusercontent.com/Czapla-dev/hassio-doc/master/images/Screenshot_2020-09-14-06-03-19-820_io.homeassistant.companion.android.jpg)

# Graders
Actually one latest grade is available.
