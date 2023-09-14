import heapq
import re
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import nltk


# Downloading required packages, Need to be run only once
# nltk.download('stopwords')


# Fetch webpage content and extract text(scraping the site)
def fetch_and_extract(url):
    """
    Extract and clean text content from a given URL.

    This function scrapes text content from the provided URL using the newspaper module.
    If the scraped data is not sufficient (too short or not extracted properly), it
    falls back to using BeautifulSoup to extract relevant paragraphs. The extracted text
    is then cleaned by removing HTML tags, unnecessary spaces, and numeric references.

    Args:
        url (str): The URL from which text will be extracted.

    Returns:
        str: The cleaned text content extracted from the URL.
    """
    # using newspaper module for scraping data
    try:
        article = Article(url)
        article.download()
        article.parse()
    except Exception as e:
        pass
    # if data is not scraped properly from newspaper or is too short then using bs4 to scrape
    if len(article.text) < 50:
        # Fetching the url and finding all the p tags
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        relevant_paragraphs = soup.find_all("p")

        # Combining the list
        for paragraph in relevant_paragraphs:
            article_text = paragraph.get_text()
        ans = article_text
    else:
        ans = article.text

    # removing unnecessary elements using regex
    final = re.sub(r"<.*?>", "", re.sub(r"\s+", " ", re.sub(r"\[[0-9]*\]", " ", ans)))
    return final


def summarise(url, paragraph, length):
    """
    NLP algorithm to Summarize text extracted from a given URL.

    This function takes a URL and a paragraph flag as input and generates a summary
    of the text extracted from the URL. The summary is based on sentence scores
    calculated from word frequencies.

    Args:
        url (str): The URL from which text will be extracted.
        paragraph (bool): Flag indicating whether to return the summary as a paragraph
                         (True) or bullet points (False).
        length (int): It defines the length of the summary that will be generated

    Returns:
        str or list: The generated summary. If paragraph is True, the summary is a
                     single string paragraph. If paragraph is False, the summary is a
                     list of sentences.
    """
    # Getting the scraped data
    text = fetch_and_extract(url)

    # Tokenizing the text
    stopwords = nltk.corpus.stopwords.words("english")
    # Tokenize the text into sentences
    sentence_list = nltk.sent_tokenize(text)

    # Calculate word frequencies
    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Calculate maximum word frequency
    maximum_frequency = max(word_frequencies.values())

    # Normalize word frequencies
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequency

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if (
                    len(sent.split(" ")) < 30
                ):  # Consider sentences with less than 30 words
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    # Select top sentences for summary
    summary_sentences = heapq.nlargest(
        length * 10, sentence_scores, key=sentence_scores.get
    )

    # Return summary as paragraphs or bullet points based on paragraph flag
    if paragraph:
        return " ".join(summary_sentences)
    return summary_sentences
