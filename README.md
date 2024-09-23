# Uonet+ Vulcan integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs) 
[![usage_badge](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=Usage&query=vulcan.total&url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json)](https://analytics.home-assistant.io) 
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=vulcan)  
View your vulcan data as Home Assistant sensors and use it in automations. You can add multiple students by adding integration again.

# Important note
This integration will only work with Vulcan accounts that still use the old UONET+ API. If your school has already switched to the new API (eduVulcan), this integration will not work.

## Get started
If you already installed integration you can add it to home assistant by clicking [this link](https://my.home-assistant.io/redirect/config_flow_start/?domain=vulcan) or add it manually this integrations page, then login as mobile app in Integrations page. In integration options you can select student and enable notifications. Actually only one student is supported.   
You can easily add sensors to the lovelace interface using the "Add to Lovelace UI" option in the device page.
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/dashboard.png)

## Configuration
All integration settings are available in the options in the integration configuration panel.
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/options.png)

## Timetable
### Calendar
Calendar view with all lessons, homeworks and exams.

#### Month
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/calendar-month.png)
#### Week
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/calendar-week.png)


#### Calendar entity
Integration is also creating calendar entity wich can be used in automations.
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/calendar-entity.png)

### Sensors
Integration is creating ten entities for today and also ten for tomorrow.
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/lesson.png)

## Graders
Student's latest grade.  
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/grade.png)

## Messages
Latest message sensor. You can activate notification in integration options.
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/message.png)

## Attendance
Latest attendance sensor, you can enable notificatiosi in integration options.  
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/attendance.png)

## Lucky Number
Student's lucky number.  
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/lucky_number.png)

## Exam
Student's next Exam.  
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/exam.png)

## Homework
Student's next Homework.  
![image](https://raw.githubusercontent.com/Antoni-Czaplicki/vulcan-for-hassio/master/docs/images/homework.png)
