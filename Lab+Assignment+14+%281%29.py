
# coding: utf-8

# # Lab Assignment 13
# 
# Find and tell an interesting story about games, players, teams, etc. using the [Lahman database](http://seanlahman.com/baseball-archive/statistics) or [Retrosheet](http://www.retrosheet.org/gamelogs/index.html) gamelogs for any season.
# 
# * Connect to the database and perform a query to retrieve data
# * Performs one groupby to summarize data over one or more columns.
# * Performs a second groupby with joining to identify the top cases.
# * Visualizes a bivariate relationship between the grouped values and some other values.
# 

# In[1]:

get_ipython().system('pip install pymysql')


# In[4]:

import seaborn as sb
import pandas as pd
import numpy as np
from datetime import datetime
get_ipython().magic('matplotlib inline')

from sqlalchemy import create_engine

user = 'lubo4991'
password = 'INFO2201'
host = 'lahman.cjuyvrfem14z.us-west-2.rds.amazonaws.com'
port = 3306
database = 'lahman2016'

# dialect[+driver]://user:password@host/dbname[?key=value..]
engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(user,password,host,port,database))
conn = engine.connect()


# In[ ]:

with engine.connect() as conn:
    tables = pd.read_sql_query('show tables',conn)
    
tables


# # Best pitchers of all time based on their ERA, IP, and total number of strikeouts. 

# In[ ]:

conn = engine.connect()
q = """  
SELECT 
    *
FROM
    Batting
    
    
    
"""
df = pd.read_sql_query(q,conn)
df


# In[ ]:

conn = engine.connect()
q = """  
SELECT 
    m.Name, p.ERA, p.IP, p.SO_Sum,p.teamID
FROM 
    (SELECT 
        playerID, 
        9*SUM(ER)/SUM(IPOuts/3) AS ERA,
        SUM(IPOuts/3) AS IP, 
        teamID, 
        sum(SO) AS SO_Sum
        FROM 
            Pitching
        GROUP BY 
            playerID
        HAVING 
            IP >=1000) p
    JOIN (SELECT 
            CONCAT(nameFirst," ",nameLast) AS Name,
            playerID FROM Master) m
         ON 
               p.playerID = m.playerID
GROUP BY
    teamID 
ORDER BY 
    p.IP DESC, p.ERA ASC, p.SO_Sum DESC
    
"""
#    `p.IP DESC`.`p.SO_Sum` DESC, `p.ERA` ASC 
# I couldn't figure out how to sort these three columns so they return 
#what I have in my ORDER BY statement
#Only returns the first ORDER BY variable

df = pd.read_sql_query(q,conn)
df
#Cy Young+(22)	7356.0
#^ this is most innings pitched so I'm not sure why my table is showing 
#Alexander as most innings pitched


# # It was hard to represent this data on a graph so I made a scatter showing the correlation between a pitcher's ERA and their total innings pitched. As you can see the pitchers that weren't in the league as long usually ended with terrible ERA's. Those that were in the league the longest had signigificanlty lower ERA's than the average pitcher. 

# In[ ]:

df.plot(x='ERA', y='IP',kind='scatter')


# 

# # Next, I wanted to look at the alltime leaders in homeruns per season.

# In[ ]:

conn = engine.connect()
q = """ 
select HR, playerID
FROM Batting
WHERE HR > 55

"""
pd.read_sql_query(q,conn)


# # From this, I then wanted to figure out when these top homerun hitters first started using steriods in their careers. 

# In[ ]:

conn = engine.connect()
q5 = """ 
SELECT playerID, yearID, HR
    FROM Batting
    
    
    WHERE playerID LIKE 'mcgwima01'
   
    OR playerID LIKE 'sosasa01'
    OR playerID LIKE 'bondsba01'
    OR playerID LIKE 'griffke02'
    OR playerID LIKE 'gonzalu01'
    OR playerID LIKE 'howarry01'
    GROUP BY playerID, yearID
    ORDER BY yearID Desc;
"""
Roids_df = pd.read_sql_query(q5,conn)
Roids_df




# # All these players generally peaked in the late 1990's and early 2000's. The mlb started testing for steroids around 2003 so thats when we see the decline

# In[ ]:

pd.read_sql_query(q5,conn).plot(x='yearID',y=('HR'),secondary_y='playerID')


# # Here I tried making a graph showing each individual player but wasn't able to figure it out

# In[ ]:

ax = pd.read_sql_query(q5,conn)['playerID'].plot(logy=True,legend=True)
ax.set_xlabel('yearID')
ax.set_ylabel('HR')
ax.set_title('Steroid Use') 


# 
# # Here we can look at an individual player to see when they first started using steriods

# In[ ]:

#Sammy Sosa
conn = engine.connect()
q6 = """ 
SELECT playerID, yearID, HR
    FROM Batting
    WHERE playerID LIKE 'sosasa01'
    GROUP BY playerID, yearID
    ORDER BY yearID Desc;
"""
Roids_df = pd.read_sql_query(q6,conn)
Roids_df




# In[ ]:

#Ken Griffey JR
conn = engine.connect()
q7 = """ 
SELECT playerID, yearID, HR
    FROM Batting
    WHERE playerID LIKE 'griffke02'
    GROUP BY playerID, yearID
    ORDER BY yearID Desc;
"""
Roids_df = pd.read_sql_query(q7,conn)
Roids_df




# In[ ]:

#Berry Bonds
conn = engine.connect()
q8 = """ 
SELECT playerID, yearID, HR
    FROM Batting
    WHERE playerID LIKE 'bondsba01'
    GROUP BY playerID, yearID
    ORDER BY yearID Desc;
"""
Roids_df = pd.read_sql_query(q8,conn)
Roids_df


# # Looking at each players individually 

# In[ ]:

#Sammy Sosa
pd.read_sql_query(q6,conn).plot(x='yearID',y=('HR'),secondary_y='playerID')


# In[ ]:

#Ken Griffey JR
pd.read_sql_query(q7,conn).plot(x='yearID',y=('HR'),secondary_y='playerID')


# In[ ]:

#Berry Bonds
pd.read_sql_query(q8,conn).plot(x='yearID',y=('HR'),secondary_y='playerID')


# # #EXTRAS __________________________________________________________________________________________________________________________________________

# # This problem I had trouble with but I wanted to see which teams had the best pitching of all time. 

# In[ ]:

conn = engine.connect()
q = """ 
SELECT 
        teamID,yearID, 9*SUM(ER)/SUM(IPOuts/3) AS ERA,
        SUM(IPOuts/3) AS IP
        FROM 
            Pitching 
        GROUP BY 
            teamID, yearID
        HAVING 
            yearID >= 1950) 
"""
pd.read_sql_query(q,conn)            


# In[ ]:

conn = engine.connect()
q = """ 
SELECT 
    CONCAT(m.nameFirst," ",m.nameLast) AS Name, Sum(p.SO) AS SO_Sum, teamID
FROM 
    Pitching p
INNER JOIN 
    Master m
    
ON 
    p.playerID = m.playerID
GROUP BY 
    p.playerID, m.nameLast, m.nameFirst
ORDER BY 
    SO_Sum DESC;
"""
pd.read_sql_query(q,conn)


# In[ ]:

# Here I wanted to see the best hitters of all time based on games played 
#and their batting average
conn = engine.connect()
q = """ 
SELECT 
    CONCAT(m.nameFirst," ",m.nameLast) AS Name, 
    Sum(p.SO) AS SO_Sum, SUM(b.G) AS Games_Played,
    round(SUM(b.H)/SUM(b.AB), 3) AS AVG
FROM 
    Pitching p

INNER JOIN
    Batting b
    
ON 
GROUP BY

INNER JOIN 
    Master m
ON 
    p.playerID = m.playerID
GROUP BY 
    p.playerID, m.nameLast, m.nameFirst
ORDER BY 
    SO_Sum DESC;
"""
pd.read_sql_query(q,conn)

