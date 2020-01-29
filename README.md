# Assignment1: ETL
## Due: Jan 30, 2020
The goal of this assignment to learn how to get data from the web and load it into a database so it can be used in your project. We will use ACS data here from the US Census Bureau since you will probably use it for projects that have any spatial/location component in the US.

## Tasks:
1. Get Data: Pick a US state and (write a script to) download the most recent ACS data (at the block group level) for every block group in that state.
* There are various download sites and APIs available for this task. Feel free to pick one and justify why.
* There will be many variables available in the US. You don't have to get them all. Select 10-20 that you will find useful for your project (such as age, gender, race, income, education status, etc.).
2. Transform/Prep: Once you've downloaded the data, get it ready (with code) so that it can be loaded into a postgres database table.
3. Load:  the data you've downloaded into a postgres database table.
*	You'll need to create the table schema
*	Copy the data into the table


## You might find the following resources useful as you do this:
*	https://dssg.github.io/hitchhikers-guide/curriculum/1_getting_and_keeping_data/csv-to-db/ (Links to an external site.)
*	https://github.com/dssg/ohio (Links to an external site.)

## What you need to submit:
1. Code to do all three things. Try to keep it modular and generalizable so you can do it for a different geography, granularity (state, city, zipcode, etc.), and additional variables. Commit the code on github (in the repo for your project) and submit the link on canvas.
2. Location of where the database table is in your database. Submit it as part of the report on canvas
3. A short (1 page) write-up describing what you did and why. Submit it as a pdf on canvas.
