#  Book Store API
This is a simple RESTful API built with Django and Django REST Framework. The API allows you to manage books and users.

## Getting started
1. Clone the repository
2. Install the required packages: pip install -r requirements.txt
3. Run the migrations: python manage.py migrate  
4. Start the server: python manage.py runserver
5. Go to http://127.0.0.1:8000/swagger/ to view the Swagger documentation.
## API endpoints
- The API responses are available in either JSON or XML format based on the "Accept" header specified in the request.
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
    'search': the value can be either a title, a username, an author pseudonym, or a price


- #### POST /books/: 
  - Creates a new book. 
  - **Authentication**: Required
  - **Note 1**: The cover_image size should be less than 1 MB. 
  - **Note 2**: The cover_image field can be submitted in three different formats: as a URL, a file path, or as the image file itself. If submitting the first two options, raw data string should be included in the request body, while for the file object, form data should be selected.
  - **Note 3**: For better performance, it is recommended to store media files in a separate storage service, such as AWS S3, rather than on our own server.
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
-   Tests are located in the tests.py file of each app. To run the tests, use the command: **_python manage.py test_**

Thank you for taking the time to read this README
