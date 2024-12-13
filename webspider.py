import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url, keywords):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant job or study-related content
        results = []
        for keyword in keywords:
            # Search for the keyword in the page's content
            for element in soup.find_all(string=lambda text: text and keyword.lower() in text.lower()):
                # Find the parent element for better context
                parent = element.find_parent()
                if parent:
                    results.append(parent.text.strip())

        # Remove duplicates and return the results
        return list(set(results))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []

def save_keywords_to_csv(keywords, filename):
    try:
        # Write keywords to a CSV file
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Keywords"])
            for keyword in keywords:
                writer.writerow([keyword])
        print(f"Keywords saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

# Example usage
if __name__ == "__main__":
    # URL of the website to scrape (example: Python job listings from a public site)
    url = "https://app.kavigai.com/#/goal/list"
    
    # Keywords related to jobs or studies
    keywords = ["Python", "developer", "Brand", "internship"]

    # Scrape the website
    results = scrape_website(url, keywords)

    # Display the results
    if results:
        print("Relevant Content Found:")
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result}")

        # Save keywords to a CSV file
        save_keywords_to_csv(keywords, "keywords.csv")
    else:
        print("No relevant content found.")

