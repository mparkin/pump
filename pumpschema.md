# Pump Database Schema

## Overview

The peristaltic pump has settings and run data that needs to be 
persistant. To store and fetch these efficiently, an sqlite database 
has been selected to do this

## Tables

1. PumpRun  - This table stores data on how long the pump has run. It 
will store data in minutes. A record will be added to the table when the 
user resets the time counter ( this will be done when the tube is replaced
of other maintenance action is performed. 

 | Field Name | Type |
 |------------|------|
 | Start Time | DateTime |
 | Run Minutes| Minutes |

2. Speed  - This table stores the delay between pulses that determines
speed. These will be indexed by a unique character string

 | Field Name | Type |
 |------------|------|
 | Speed Name | Str[40]|
 | Pulse Wodth| float |

3. Recipes - Use selectable and defineable recipes to select the desired 
speeds, volume etc.

| Field Name | Type |
|------------|------|
| Recipe Name| str[40]|
| Speed | Speed Name |
| Volume| Float |
| Tube type| Tube Type |

4. Tube Type = Where tube ID is specified for volume calculation

|Field Name | Type |
|-----------|------|
| Rube Name | text|
| ID        | float|

5. Records - a date indexed table of recordable pump actions. 

|Field Name | Type |
|----------|------|
|Date      | DateTime|
| Message  | char blob |
