# Flask Web Application README

## Project Description
This Flask web application is a simple example of a web-based user interface for managing company information. Users can register, log in, update their company's information (including company name and logo).

## Features
- User Registration: Users can create accounts by providing a username, password, company name, and company logo.
- User Login: Registered users can log in to access their account.
- Company Information Update: Logged-in users can update their company's information, including the company name and logo.
- User Authentication: The application uses user authentication to restrict access to certain features to logged-in users.
- File Upload: Users can upload company logos in supported image formats (e.g., PNG, JPG, JPEG, GIF).
- Flash Messages: The app displays flash messages to provide feedback to users.

## Project Structure
The project follows a typical Flask web application structure:<br>
├── app.py # Main application file<br>
├── static/ # Static files (CSS, JavaScript, images)<br>
│ └── uploads/ #logo images<br>
│ └── style.css # CSS styles for the application<br>
├── templates/ # HTML templates<br>
│ ├── layout.html # Base HTML layout template<br>
│ ├── home.html # Home page template<br>
│ ├── login.html # Login page template<br>
│ ├── register.html # Registration page template<br>
│ ├── change_company_info.html # Company information update page template<br>
├── instance/<br>
│ ├── users.db # SQLite database for user data<br>

## Requirements
- Python 3.9.18
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.5
- Werkzeug 3.0.1

## Usage
Run the Flask application: `python app.py`.

## Acknowledgments
- This project is based on Flask, a lightweight Python web framework.
- We thank the Flask community for their contributions and support.



