# SunOye-1
A basic chat-room application. 
Created using tkinter (for GUI), pymysql (for MySQL DBMS), paho-mqtt (for MQTT Protocol) library of Python.

##Introduction
This project was created for IoT Lab Project in 3rd Year (6th Semester). It is a chat room application currently programmed to work on a local host machine and it's connected network. The messaging rooms are temporarily created and all the conversation is vanished after the room is closed. The concept for room creation and identification is based on "_Roomm Number_" and "_password_".
A person could access a room with Room Number and Password of that room. A random room can be started and infromation can be stored in a local database using MySQL, one could access the rooms from the credentials of the rooms created. This is a leraning porject to use these technologies.

##How does it Work?
 * Using _tkinter_ library in Python we create a basic GUI for the intial Room Login, Create Room and Room Windows. These Rooms have their credentials stored in the local database (created using MySQL on the localhost).
 * The new Room queries are stored in the _sunoye_ database created on the local machine (You can change the login credentials for your cloud connection, or your own localhost). The existing room queries are verified from the _sunoye_ database only.
 * For messaging purpose MQTT Protocol is used and Hive MQ's **MQTT Public broker** is defined as our MQTT Broker for Publish/Subscribe purpose. Implemetation of MQTT is through _paho-mqtt_ library present in Python.
 * When an user join a room, it is subscribed to the _topic_, which is defined by the Unique Room Number in the Broker. All the conversations are done in the Room Window of the user.
 * When a message is sent in the Room Window, it is published to the Room Number topic in the broker and received by all the subcribers of the room.
 * Database also tracks the number of members in the rooms, when a room is empty it is set to inactive and won't be available for use without creating.
 * 

##Tools and Technologies
