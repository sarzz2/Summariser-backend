from functools import wraps
from urllib.parse import urlparse
from flask import jsonify, request


def validate_params(func):
    """
    A decorator to validate URL and paragraph parameters for a Flask route.

    This decorator checks the validity of the URL, paragraph and length parameters received
    in a Flask request. It ensures that the URL is valid and properly formatted, and
    that the paragraph parameter is either 'True' or 'False' and the length is valid.
     The decorator raises
    appropriate error responses if validation fails.

    Args:
        func (function): The route function to be decorated.

    Returns:
        function: The decorated route function with parameter validation.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get URL, paragraph and length parameters from the request
        url = request.args.get("url")
        paragraph = request.args.get("paragraph")
        length = request.args.get("length")
        # Validate the URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return jsonify({"error": "Invalid URL"}), 422

        # Validate the paragraph parameter
        if paragraph == "true":
            paragraph_value = True
        elif paragraph == "false":
            paragraph_value = False
        else:
            return jsonify({"error": "Missing or invalid parameter paragraph"}), 400

        # validating the length parameter
        if length is None or int(length) > 3:
            return jsonify({"error": "Missing or invalid parameter length"}), 400

        # Call the route function with validated parameters
        return func(url, paragraph_value, length, *args, **kwargs)

    return wrapper
