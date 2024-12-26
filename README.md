# Sentiment Analysis Web Application

This web application allows users to register, log in, submit feedback on products, and allows companies to register, log in, add products, and view feedback. The application uses **Flask**, **SQLite**, and a **Hugging Face Transformers pipeline** for sentiment analysis.

## Project Structure

The project consists of the following main components:

*   `app.py`: This file contains the main application logic, including routes, database interactions, and sentiment analysis functionality [1].
*   `schema.txt`: This file contains the database schema definition for SQLite database [2, 3].
*   `templates`: This folder contains the HTML templates for the web application's user interface (not detailed in the provided source code).
*   A database named `senti.db` which stores user, company, product, and feedback information [1].

## Functionality

### User Features

*   **Registration:** Users can register with their personal information, including first name, last name, email, password, gender, date of birth, state, and city [4, 5].
    *   The application checks if the email is already registered [5].
*   **Login:** Registered users can log in using their email and password [6, 7].
*   **Profile:** After logging in, users can view their profile, list of available products, and their past feedback [8, 9].
*   **Feedback Submission:** Users can submit feedback on products, which is then analyzed for sentiment (positive or negative) and stored in the database [9, 10].

### Company Features

*   **Registration:** Companies can register with their company name, email, and password [6, 11].
    *   The application checks if the email is already registered [11].
*   **Login:** Registered companies can log in using their email and password [7, 8].
*   **Company Profile:** After logging in, companies can view their profile and a list of their products, including a sentiment score [8, 12].
*  **Product Management**: Companies can add new products, including a product name and thumbnail URL [13, 14].

### Feedback Features
*   **Viewing Feedbacks**:  Companies can view detailed feedbacks including the user email, feedback text and sentiment, as well as a timestamp for each feedback, associated with a particular product [14, 15]

*   **API for Feedbacks**: The application provides an API endpoint that allows users to retrieve feedback based on product ID, sentiment, and date range. The API supports sorting the feedback by timestamp [15, 16].

## Database

The application uses an SQLite database named `senti.db` [1]. The schema includes the following tables [2, 3]:

*   `users`: Stores user information [3].
*   `companies`: Stores company information [2].
*   `products`: Stores product information, including the company that added it [2].
*  `feedback`: Stores user feedback on products, including a sentiment analysis of the feedback text [3].

## Technologies Used

*   **Flask:** A Python web framework used to build the application [1].
*   **SQLite:** A lightweight database used to store application data [1].
*   **Hugging Face Transformers:** A library used for sentiment analysis [1].
*   **HTML/CSS**: Used to create the user interface (not detailed in the source code).

## How to Run

1.  Ensure you have Python installed.
2.  Install the required libraries: `pip install flask transformers torch requests`
3.  Run the application: `python app.py`
4.  Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.
