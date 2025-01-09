# Writeup for 2024 SANS Holiday Hack Challenge: Snow-maggedon

The write up is available at https://holidayhackchallenge.thedead91.com/.  
This repository serves as a collection of files related to the challenge and scripts developed during it.

The developed scripts are:
- [2024-01 - Prologue - Elf Connect/getAnswers.js](2024-01%20-%20Prologue%20-%20Elf%20Connect/getAnswers.js)  
Nodejs script to extract the answers
- [2024-04 - Act I - Frosty Keypad/solveKeypad.py](2024-04%20-%20Act%20I%20-%20Frosty%20Keypad/solveKeypad.py)  
Python script to bruteforce the keypad
- [2024-06-01 - Act I - Hardware Hacking 101 - Part 1/dad.py](2024-06-01%20-%20Act%20I%20-%20Hardware%20Hacking%20101%20-%20Part%201/dad.py)  
Python script to retrieve the dad jokes
- [2024-06-02 - Act I - Hardware Hacking 101 - Part 2/generateSignature.py](2024-06-02%20-%20Act%20I%20-%20Hardware%20Hacking%20101%20-%20Part%202/generateSignature.py)  
Python script to generate a HMAC signature given the secret_key and the access_key
- [2024-08 - Act II - Drone Path/sqli.py](2024-08%20-%20Act%20II%20-%20Drone%20Path/sqli.py)  
Python script easing up the exploitation of the SQL injection in the search function of the Elf Drone Workshop
- [2024-08 - Act II - Drone Path/drawMap.py](2024-08%20-%20Act%20II%20-%20Drone%20Path/drawMap.py)  
Python script using Folium to print the map from the CSV
- [2024-08 - Act II - Drone Path/gold.py](2024-08%20-%20Act%20II%20-%20Drone%20Path/gold.py)  
Python script extracting and converting the data as needed from `ELF-HAWK-dump.csv` to obtain the flag for the gold trophy
- [2024-09 - Act II - PowerShell/Silver - Question 10.ps1](2024-09%20-%20Act%20II%20-%20PowerShell/Silver%20-%20Question%2010.ps1)  
Powershell script solving the Question 10 of the silver trophy for this challenge
- [2024-09 - Act II - PowerShell/Gold.ps1](2024-09%20-%20Act%20II%20-%20PowerShell/Gold.ps1)  
Powershell script solving to obtain the gold trophy
- [2024-13 - Act III - Elf Stack/bruteforce.py](2024-13%20-%20Act%20III%20-%20Elf%20Stack/bruteforce.py)  
Python script to bruteforce answers based on a dictionary for this challenge
- [2024-14 - Act III - Decrypt the Naughty-Nice List/lfi.py](2024-14%20-%20Act%20III%20-%20Decrypt%20the%20Naughty-Nice%20List/lfi.py)  
Python script to exploit the LFI in the status_id file
- [2024-15 - Act III - Deactivate Frostbit Naughty-Nice List Publication/aql_blind.py](2024-15%20-%20Act%20III%20-%20Deactivate%20Frostbit%20Naughty-Nice%20List%20Publication/aql_blind.py)  
Python script to exploit the Blind Injection in ArangoDB