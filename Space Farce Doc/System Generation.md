# Space Farce Doc/System Generation.md

## Star System Generation

For each system, generate the system type, star type, warp points, planet numbers and types, and maximum EP. An example is provided.

### 1. System Type

| Roll | System Type      |
| :--- | :--------------- |
| 1-7  | Single Star      |
| 8-9  | Binary Star      |
| 0    | Starless Nexus   |

**3.21** System Type: Determine the type of the system. Roll a d10. The system will consist of a single star, binary star, or a starless nexus. If the system is a single or double star, complete all the remaining sections. If the system is a nexus, only complete the system warp point section.

### 2. Star Type

| Roll | Star Type |
| :--- | :-------- |
| 1-2  | Red      |
| 3-4  | Orange   |
| 5-6  | Yellow   |
| 7-8  | White    |
| 9-0  | Blue     |

**3.22** Star Type: For each star in the system, roll a die to determine its type. Any system planets will be determined based on the star type. Binary systems will determine planets twice, once for each star.

### 3. System Warp Points

| Roll | Warp Points |
| :--- | :---------- |
| 1    | 0          |
| 2-4  | 1          |
| 5-6  | 2          |
| 7-8  | 3          |
| 9-10 | 4          |
| 11   | 5          |
| 12   | 6          |

**3.23** System Warp Points: Roll a die to determine the number of open warp points present in the star system. Modify the die roll based on the system and star type:  
**Number of System Warp Points**  
Modifiers (Cumulative)  
-1  Orange/Red Star  
+1  Blue Star  
+1  Binary Stars  
+2  Starless Nexus  

After rolling for the number of warp points, roll a d100 for each warp point to determine the destination system of each warp point (or a dX based on the size x of your galaxy).

### 4. Number and Type of Planets

| *Type* | *0* | *4* | *5* | *6* | *7* | *8* | *9* |
| :----- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Red    | 1-4 | 5-6 | 7   | 8   | 9   | 0   | X   |
| Orange | 1-3 | 4-5 | 6-7 | 8   | 9   | 0   | X   |
| Yellow | 1-2 | 3   | 4-5 | 6-7 | 8   | 9   | 0   |
| White  | 1-2 | 3-4 | 5-6 | 7   | 8   | 9   | 0   |
| Blue   | 1-3 | X   | 4-5 | 6   | 7   | 8-9 | 0   |

**3.24** Number and Type of Planets: For each star, roll a d10 to determine the number of planets around that star. A result of “0” on the chart (not a die roll of zero) means that star has no planets. Consult the Star Type tables based on the number of planets you have rolled to determine the type of planets in the system. Example: Star System 01 is a Blue star system. The referee rolls a “9” on the number of planets table, and sees there will be eight planets in the system. Consulting the Blue Star table, he sees that there will be 3x R planets, 1x rH planet, 3x G planets, and one I planet. 

**Adjusting Planet Types:**  
- **3.241** rH planets--are habitable on a roll of 1-5. If habitable, record the planet as H. If not habitable, treat as R.  
- **3.242** G planets--gravity may destroy inner planets. Start with outermost G planet and work in. Roll a die. 1 or 2 means the next planet becomes asteroids. Roll for each G planet.  
- **3.243** Binary Stars--roll for the number of planets for each star. Divide the number at each star by 4 and round. This is the number of planets present for each star. If any planets are present, automatically add one belt of asteroids after the last planet.

### 5. Planet EP

| Planet Type | Economic Points          |
| :---------- | :----------------------- |
| H           | 40                       |
| R           | 10                       |
| G           | 4x(number moons)        |
| I           | 4                        |
| Asteroids   | 2 per group (max 10)    |

**3.25** Planet EP: For each planet, determine the maximum possible EP. Consult the *Max EP on Planets/Moons/Asteroids Table*. For G planets, roll the number of exploitable moons around each G planet to determine the maximum EP for the G planet. For asteroids, each asteroid belt, up to 5 separate areas may be colonized to a maximum of 2 EP each. Note that only H planet population grows (increases EP) through natural means.

| Roll | Moons |
| :--- | :---- |
| 1    | 0     |
| 2-3  | 1     |
| 4-6  | 2     |
| 7-8  | 3     |
| 9-0  | 4     |

### Planet Number and Types per Star Classification

#### Red

| **4** |  |  | **R** |  | **G** |  |  | **I** |  |  | **I** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ----- | :--- | :--- | ----- | :--- | ----- | :--- | :--- | ----- | :--- | :--- | ----- | :--- | :--- | ----- | :--- | :--- | ----- | :--- | :--- | ----- | :--- | :--- | ----- | :--- | :--- | :--- | :--- |
| **5** |  |  | **R** |  | **G** |  |  | **G** |  |  | **I** |  |  | **I** |  |  |  |  |  |  |  |  |  |  |  |  |
| **6** |  |  | **R** |  | **G** |  |  | **G** |  |  | **I** |  |  | **I** |  |  | **I** |  |  |  |  |  |  |  |  |  |
| **7** |  |  | **R** |  | **R** |  |  | **G** |  |  | **G** |  |  | **I** |  |  | **I** |  |  | **I** |  |  |  |  |  |  |  |
| **8** |  |  | **rH** |  | **R** |  |  | **G** |  |  | **G** |  |  | **G** |  |  | **I** |  |  | **I** |  |  | **I** |  |  |  |  |

#### Orange

| **4** | **R** | **G** | **I** | **I** |  |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **5** | **R** | **G** | **G** | **I** | **I** |  |  |  |
| **6** | **R** | **G** | **G** | **G** | **I** | **I** |  |  |
| **7** | **rH** | **R** | **G** | **G** | **G** | **I** | **I** |  |
| **8** | **R** | **rH** | **R** | **G** | **G** | **G** | **I** | **I** |

#### Yellow

| **4** | **R** | **G** | **G** | **I** |  |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **5** | **rH** | **G** | **G** | **I** | **I** |  |  |  |
| **6** | **R** | **rH** | **G** | **G** | **I** | **I** |  |  |
| **7** | **R** | **rH** | **G** | **G** | **G** | **I** | **I** |  |
| **8** | **R** | **rH** | **rH** | **G** | **G** | **G** | **I** | **I** |  |
| **9** | **R** | **rH** | **rH** | **R** | **G** | **G** | **G** | **I** | **I** |

#### White

| **4** | **R** | **G** | **G** | **I** |  |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **5** | **R** | **G** | **G** | **G** | **I** |  |  |  |
| **6** | **R** | **rH** | **G** | **G** | **I** | **I** |  |  |
| **7** | **R** | **rH** | **G** | **G** | **G** | **I** | **I** |  |
| **8** | **R** | **rH** | **rH** | **G** | **G** | **G** | **I** | **I** |  |
| **9** | **R** | **rH** | **rH** | **R** | **G** | **G** | **G** | **I** | **I** |

#### Blue

| **5** | **R** | **G** | **G** | **G** | **I** |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **6** | **R** | **rH** | **G** | **G** | **G** | **I** |  |  |
| **7** | **R** | **R** | **rH** | **G** | **G** | **G** | **I** |  |
| **8** | **R** | **R** | **R** | **rH** | **G** | **G** | **G** | **I** |  |
| **9** | **R** | **R** | **rH** | **rH** | **G** | **G** | **G** | **G** | **I** |
