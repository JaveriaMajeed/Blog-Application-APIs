# Blog-Application-APIs
Welcome to the Blogging Platform Project! This project provides a set of APIs and a user interface for a feature-rich blogging platform. It includes user registration, authentication, content creation, and commenting features. The project is built with Flask, uses a PostgreSQL database, and offers various validation and security measures.

## Features
- **User Registration**: Users can register with a unique username, email, and password. Duplicate username and email checks are in place to ensure data integrity.
- **User Login**: Registered users can log in using their email and password

- **User Authentication**: Authentication is handled with JWT tokens, securing access to the APIs.

- **Content Creation**: Users can create and post content to the platform.

- **Commenting**: Users can add comments to published content.

## API Endpoints (Local Development)

- `POST http://localhost:5000/api/login`: User login using email and password.
- `POST http://localhost:5000/api/register`: User registration with username, email, and password.
- `POST http://localhost:5000/api/post`: Create and post content.
- `GET http://localhost:5000/api/home`: Display content
- `POST/GET http://localhost:5000/api/comment`: Post a comment and display recent comment.
