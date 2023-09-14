from flask import Flask, jsonify
from algorithm import summarise, fetch_and_extract
from flask_cors import CORS
import openai
from validation import validate_params

# creating a Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

openai.api_key = "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"


@app.route("/api/summarise/", methods=["GET"])
@validate_params
def get_summarise(url, paragraph, length):
    """
    Endpoint for generating a summary of a web page.

    Args:
        url (str): The URL of the web page to summarize.
        paragraph (bool): Indicates whether to return the summary as a single paragraph or in bullet points.
        length (str): Length category of the summary, 1, 2, or 3.

    Returns:
        jsonify: A JSON response containing the generated summary or an error message.
    """
    try:
        # Calling the NLP function to summarise
        summary = summarise(url, paragraph, int(length))
        return jsonify({"summary": summary})
    except Exception as e:
        print(e)
        # logger.error("Error: %s", e)
        return jsonify({"error": str(e)}), 400


@app.route("/api/ai/summarise/", methods=["GET"])
@validate_params
def summarise_ai(url, paragraph, length):
    """
    Generate a summary of a web page using the OpenAI API.

    Args:
        url (str): The URL of the web page to summarize.
        paragraph (bool): Indicates whether to return the summary as a single paragraph or in bullet points.
        length (int): Length category of the summary, 1, 2, or 3.

    Returns:
        jsonify: A JSON response containing the generated summary or an error message.
    """
    # getting the scraped data from the url
    data = fetch_and_extract(url)
    try:
        if paragraph:
            input_text = f"Summary of{data}"
        else:
            input_text = f"Summary of {data} in bullet points using •"

        # Use OpenAI API to generate a summary
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use ChatGPT
            prompt=input_text,
            max_tokens=int(length) * 40,  # Set the desired length of the summary
        )

        summary = response.choices[0].text.strip()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# driver function
if __name__ == "__main__":
    app.run(debug=True)
