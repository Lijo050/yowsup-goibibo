
==========================================================

## Yowsup WhatsApp service

Yowsup is a python library that enables you build application which use WhatsApp service. Yowsup has been used to create an unofficial WhatsApp client Nokia N9 through the Wazapp project which was in use by 200K + users as well as another fully featured unofficial client for Blackberry 10

We integrated Goibio's HTTP APIs to get the output for required queries in WhatsApp. 

## Installation 

 - To install python packages: 
>make install
 - To install yowsup:
>make yowsup-install 
 - To run:
>make run


if any installation fails, please retry


## To Login inside yowsup shell

> /L

if login fails, please retry


## At client side
 - save 918867447835 in contacts
 - add this number to any WhatsApp group
 - user can perfom these possible queries in WhatsApp
    - @help - for welcome screen
    - @bus - for bus related queries
    - @flight - for flight related queries
    - @hotel - for hotel related queries
    - @searchBus start_station end_station date_of_departure - to search buses with minimum fare
    - @searchFlight departure_airport arrival_arrival date_of_departure - to search flights with minimum fare
    - @searchHotels city_name checkIn_date checkOut_date start_range end_range - to search hotels within given range



