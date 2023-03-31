### Objective

Your assignment is to implement a bookstore REST API using Python and any framework. While we will allow the use of any framework you prefer (incl. none at all) we would be grateful if you could complete the assignment in FastAPI or Django if you prefer.

### Brief

Lohgarra, a Wookie from Kashyyyk, has a great idea. She wants to build a marketplace that allows her and her friends to
self-publish their adventures and sell them online to other Wookies. The profits would then be collected and donated to purchase medical supplies for an impoverished Ewok settlement.

### Tasks

-   Implement assignment using:
    -   Language: **Python**
    -   Framework: **any framework** (preferred: FastAPI or Django)
-   Implement a REST API returning JSON or XML based on the `Content-Type` header
-   Implement a custom user model with a "author pseudonym" field
-   Implement a book model. Each book should have a title, description, author (your custom user model), cover image and price
    -   Choose the data type for each field that makes the most sense
-   Provide an endpoint to authenticate with the API using username, password and return a JWT
-   Implement REST endpoints for the `/books` resource
    -   No authentication required
    -   Allows only GET (List/Detail) operations
    -   Make the List resource searchable with query parameters
-   Provide REST resources for the authenticated user
    -   Implement the typical CRUD operations for this resource
    -   Implement an endpoint to unpublish a book (DELETE)
-   Implement tests as you see fit
    -   These could be unit test as well as API tests
    -   We would also count schema based validation as testing

### Evaluation Criteria

-   **Python** best practices
-   If you are using a framework make sure best practices are followed for models, configuration and tests
-   Sanity and usefulness of tests
-   Protect users' data
    -   Make sure that users may only unpublish and change their own books
-   Bonus: Make sure the user _Darth Vader_ is unable to publish his work on Wookie Books

### CodeSubmit

Please organize, design, test and document your code as if it were
going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The aidhere GmbH Team

---------------------------------------------------------------------------------------------------
# Book Store API
This is a simple RESTful API built with Django and Django REST Framework. The API allows you to manage books and users.

## Getting started
1. Clone the repository
2. Install the required packages: pip install -r requirements.txt
3. Run the migrations: python manage.py migrate  ###
4. Start the server: python manage.py runserver
5. Go to http://127.0.0.1:8000/swagger/ to view the Swagger documentation.
## API endpoints
### Books

- #### GET /books/
  - Returns a list of all books. 
  - **Authentication**: Not required
  
  ****Available Filters**** via query parameters:


    'title': filter books by title
    'author': filter books by author username
    'author_pseudonym': filter books by author pseudonym
    'price__lt': filter books by price less than the value
    'price__gt': filter books by price greater than the value
    'search': the value can be either a title, a username, an author_pseudonym, or a price


- #### POST /books/: 
  - Creates a new book. 
  - **Authentication**: Required
- #### GET /books/{id}/: 
  - Retrieves a specific book by ID. 
  - **Authentication**: Not required
- #### PUT /books/{id}/: 
  - Updates a specific book by ID. 
  - **Authentication**: Required 
  - Requires the requester be the owner of the book. 
- #### DELETE /books/{id}/: 
  - Deletes a specific book by ID. 
  - **Authentication**: Required 
  - Requires the requester be the owner of the book. 
### Users
- #### POST /users/register/: 
  - registers a user by username and password
  - **Authentication**: Not required
  - 'email' and 'author_pseudonym' are optional fields
- #### GET /users/published-books/: 
  - Returns the list of books published by the requester
  - **Authentication**: Required
    
### Authentication
- #### POST /api/token/: 
  - Retrieves an access token and a refresh token.
- #### POST /api/token/refresh/: 
  - Retrieves a new access token using a refresh token.
### Authorization
  - Some endpoints require the user to be authenticated and authorized. To authorize a request, you must provide an Authorization header in the request with the value Bearer <access_token> where <access_token> is the access token obtained from the POST /api/token/ endpoint.

### API documentation
  - **Swagger** is used to generate API documentation. Go to http://127.0.0.1:8000/swagger/ to view the documentation.

### Testing
-   Tests are located in the tests.py file of each app. To run the tests, use the command python manage.py test.
