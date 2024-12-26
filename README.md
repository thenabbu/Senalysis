# Sentiment Analysis Web Application

This web application allows users to register, log in, submit feedback on products, and allows companies to register, log in, add products, and view feedback. The application uses **Flask**, **SQLite**, and a **Hugging Face Transformers pipeline** for sentiment analysis.

## Project Structure

The project consists of the following main components:

*   `app.py`: This file contains the main application logic, including routes, database interactions, and sentiment analysis functionality.
*   `schema.txt`: This file contains the database schema definition for SQLite database.
*   `templates`: This folder contains the HTML templates for the web application's user interface.
*   A database named `senti.db` which stores user, company, product, and feedback information.

## Functionality

### User Features

*   **Registration:** Users can register with their personal information, including first name, last name, email, password, gender, date of birth, state, and city.
    *   The application checks if the email is already registered.
*   **Login:** Registered users can log in using their email and password.
*   **Profile:** After logging in, users can view their profile, list of available products, and their past feedback.
*   **Feedback Submission:** Users can submit feedback on products, which is then analyzed for sentiment (positive or negative) and stored in the database.

### Company Features

*   **Registration:** Companies can register with their company name, email, and password.
    *   The application checks if the email is already registered.
*   **Login:** Registered companies can log in using their email and password.
*   **Company Profile:** After logging in, companies can view their profile and a list of their products, including a sentiment score.
*  **Product Management**: Companies can add new products, including a product name and thumbnail URL.

### Feedback Features
*   **Viewing Feedbacks**:  Companies can view detailed feedbacks including the user email, feedback text and sentiment, as well as a timestamp for each feedback, associated with a particular product

*   **API for Feedbacks**: The application provides an API endpoint that allows users to retrieve feedback based on product ID, sentiment, and date range. The API supports sorting the feedback by timestamp.

## Database

The application uses an SQLite database named `senti.db`. The schema includes the following tables:

*   `users`: Stores user information.
*   `companies`: Stores company information.
*   `products`: Stores product information, including the company that added it.
*  `feedback`: Stores user feedback on products, including a sentiment analysis of the feedback text.

## Technologies Used

*   **Flask:** A Python web framework used to build the application.
*   **SQLite:** A lightweight database used to store application data.
*   **Hugging Face Transformers:** A library used for sentiment analysis.
*   **HTML/CSS**: Used to create the user interface.

## How to Run

1.  Ensure you have Python installed.
2.  Install the required libraries: `pip install flask transformers torch requests`
3.  Run the application: `python app.py`
4.  Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.
