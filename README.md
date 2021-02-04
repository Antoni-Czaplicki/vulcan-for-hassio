# Uonet+ Vulcan integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

View your vulcan data as Home Assistant sensors and use it in automations. You can add multiple students by adding integration again.

## Get started
To get started login as mobile app in Integrations page. In integration options you can select student and enable notifications. Actually only one student is supported.  \n
You can easily add sensors to the lovelace interface using the "Add to Lovelace UI" option in the device page.
![image](docs/images/dashboard.png)

## Configuration
All integration settings are available in the options in the integration configuration panel.
![image](docs/images/options.png)

## Timetable
Integration is creating ten entities for today and also ten for tomorrow. There are plans to add viewing entities in calendar.  
![image](docs/images/lesson.png)

## Graders
Student's latest grade.  
![image](docs/images/grade.png)

## Messages
~Latest message sensor. You can activate notification in integration options.~
Actualy not available - new API doesn't have this feature yet, it will be added again soon.
![image](docs/images/message.png)

## Attendance
Latest attendance sensor, you can enable notificatiosi in integration options.  
![image](docs/images/attendance.png)

## Lucky Number
Student's lucky number.  
![image](docs/images/lucky_number.png)

## Exam
Student's next Exam.  
![image](docs/images/exam.png)

## Homework
Student's next Homework.  
![image](docs/images/homework.png)
