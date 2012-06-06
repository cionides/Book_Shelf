Bookshelf
==========
CREATED BY: Christina Ionides and Iana Boneva

OVERVIEW/OBJECTIVE:
An application that allows people to create, maintain, and update a virtual bookshelves. 
The site will also function for non-registered users as a resource to look up books and 
read comments. 

FUNCTIONALITY:
Actions that are possible as a guest:
	Search our databases for books
	View book profiles
	View a list of user profiles
	View a user profile to an extent
		Their bookshelves
		Their user bio
		NOT the books on their shelves

Actions that are possible as a registered user:
	Search our databases for books
	View book profiles
		add these books to an existing shelf
		Edit a book profile
		Add comments
	View a list of user profiles
	View a user profile
		Their bookshelves AND the books on them
		Their bio
	Create a new book shelf
		Add books to this shelf
		Delete books from this shelf
		Delete the shelf

Actions that only an administrator can do:
	All of the above
	Delete Book records
	Delete profiles

Division of tasks:
The work for this project was largely collaborative.  All the time spent working on it was done together.
Therefore, we feel the division of tasks is not necessarily possible and would not be indicative of the 
actual work done.

We created the logic of our application together. 
We worked together to create the tables in our databases, and to develop the interactions between the different pages. Along the way, we had to rework how some of the logic,and how different pages were talking to one another. 
We discussed this as a team, and implemented it together. 

Christina:
Found the layout and implemented mylayout.html and edited style.css.
Implemented the comments.

Iana:
Created the search box in both the index and book_shelf controllers by using the callback.
Functionality to add a book to a shelf