# Text Summarization Flask App

This is a Flask web application that performs text summarization based on a provided URL using Natural Language Processing (NLP) and AI techniques. The application allows you to generate summaries in both paragraph and bullet point formats.

## Code Formatting

The code in this project has been formatted using Black, a popular Python code formatter. Black enforces a consistent code style throughout the project. To format the code in this project:

1. Install Black using pip: ```pip install black```
2. Navigate to the project directory in your terminal.
3. Run Black to format the project files: ```black .```

This ensures that the code maintains a uniform style for improved readability and maintainability.

## Table of Contents
- [Setup and Installation](#setup-and-installation)
- [Running the Flask App](#running-the-flask-app)
- [Usage & Endpoints](#usage)
- [Code Explanation](#code-explanation)
- [License](#license)

## Setup and Installation

1. Clone this repository to your local machine:

   ```bash
   git clone replace with URL
   ```

2. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key in the Flask app:
   Open the `app.py` file and locate the line:
   ```python
   openai.api_key = "YOUR_OPENAI_API_KEY"
   ```
   Replace `"YOUR_OPENAI_API_KEY"` with your actual OpenAI API key.

## Running the Flask App

1. Navigate to the project directory:

   ```bash
   cd Summariser
   ```

2. Start the Flask app:

   ```bash
   python app.py
   ```

   The app will be accessible at `http://127.0.0.1:5000/`.

## Usage & Endpoints

1. Access the API in your web browser or in Postman at `http://127.0.0.1:5000/`.

Endpoints:-
1. `http://127.0.0.1:5000/api/summarise/?url=your_url/&paragraph=bool&length=int`


2. `http://127.0.0.1:5000/api/summarise/?url=your_url/&paragraph=bool&length=int`

Make sure to replace url, paragraph and length parameter with the value

Eg. `http://127.0.0.1:5000/api/summarise/?url=https://www.amnesty.org/en/what-we-do/arms-control/gun-violence/&paragraph=False&length=2`

## Code Explanation

### `app.py`

This is the main Flask app file containing the route for summarization, OpenAI API integration, and error handling.

### `fetch_and_extract(url)`

A function that scrapes and extracts text content from a given URL using the `newspaper` and `BeautifulSoup` modules.

### `summarise(url, paragraph, length)`

An NLP algorithm that takes a URL, paragraph and length flag as parameters to generate text summaries. It calculates sentence scores based on word frequencies and returns summaries in paragraph or bullet point format of desired length.

## License

This project is licensed under the [MIT License](LICENSE).