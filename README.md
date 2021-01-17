# Keywords-Forward
Author: Nachiket Subbaraman            
Using a corpus of 1.5 million computer science research documents from kaggle and an oxford dictionary of common computer science phrases, I made a Python server to
index and store these documents using Whoosh. I created a second Whoosh index to store more documents; each document has a computer science phrase as a title and a 
corresponding dictionary as its content, which contains the title’s related keywords as keys and a numerical ranking representing how related they are to the title as values.
Users enter computer science phrase queries in the frontend HTML, then the server uses Whoosh to search for the query from the titles of the second Whoosh index and retrieve 
that title’s content and displays the dictionary in the HTML browser.
