# robot-poc

A small Proof-of-Concept style web application for imaginary polling station staff, so they may log
number of voters and information about possible incidents.

The purpose here is to demostrate usage of Robot Framework and Selenium in software testing or process automation.


## Architechture
The web app is implemented using Flask and it has a main page and two sub pages with forms.
Once user fills a form and submits it, the data is saved to sqlite database.

## Testing
First, Robot Framework test cases use Selenium to browse to the form pages from the main page, then fill out
the needed information and submit the form.

Second, the test cases use a simple custom library to interface with the database. The relevant
table is queried and the saved data is compared to the input data, to confirm that form submission
process works as expected.