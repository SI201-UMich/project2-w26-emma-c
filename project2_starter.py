# SI 201 HW4 (Library Checkout System)
# Your name: Yan Emma Chen
# Your student id: 44141446
# Your email: yanechen@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# 
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure, and also for a list of functions that I might need for get_listing_details() 
# I then used those suggestions to guide my implementation of those functions, but I did not copy any code directly from ChatGPT.
#
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)


        This function takes in the argument html_path representing the path of the

    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    with open(html_path, 'r', encoding="utf-8-sig") as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

    listings = soup.find_all(id=lambda x: x and x.startswith("title_"))

    listing_results = []

    for listing in listings:
        
        title = ' '.join(listing.get_text().split())

        listing_id = listing["id"].replace("title_", "").strip()
        
        listing_results.append((title, listing_id))

  
    return listing_results
   
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    
    with open(f"html_files/listing_{listing_id}.html", 'r', encoding="utf-8-sig") as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

    #ul class="fhhmddr dir dir-ltr"
    # get the unordered list that contains the policy number with a the unique class
    unordered_list = soup.find('ul', class_="fhhmddr dir dir-ltr") 

    # policy number is first in the list and is contained in a span
    spans = unordered_list.find_all('span', class_="ll4r2nl dir dir-ltr")
    policy_number = spans[0].text.split()[0].strip() 

    # host type is the third item in the unordered list with a unique class, but some listings dont have a host type so i check if there are more than 2 items in the list before trying to access it
    # print(soup.find('ul', class_="tq6hspd h1aqtv1m dir dir-ltr").find_all('li'))
    host_type = soup.find('ul', class_="tq6hspd h1aqtv1m dir dir-ltr").find_all('li')
    if len(host_type) > 2:
        host_type = host_type[2].find('span', class_="l1dfad8f dir dir-ltr").text
    else:
        #some of the listings dont have a host type so i just set it to regular host
        host_type = "Regular"

    # getting host name, and removing "Hosted by" to get just the name(s)
    host_name = soup.find('div', class_="tehcqxo dir dir-ltr").find('h2').text.replace("Hosted by ", "").strip()

    # assigning room type based on the listing subtitle
    room_type_str = soup.find('div', class_="_tqmy57").get_text().strip()
    if "Entire" in room_type_str:
        room_type = "Entire Room"
    elif "Private" in room_type_str:
        room_type = "Private Room"
    else:
        room_type = "Shared Room"
    #print(room_type)
    # finding location rating if there is one, otherwise set to 0.0
    # find the unique div class that holds location, get the list of divs thats inside, 
    # find the span that holds the rating
    # get the text inside the span, and remove all whitespaces and newlines only get the rating
    divs = soup.find('div', class_="r1f90fvr dir dir-ltr")
    if divs is not None:
        divs = divs.find_all('div', class_="rjiv01r dir dir-ltr")[3].find('span', class_="_4oybiu").get_text().split()[0]
        location_rating_str = divs
        location_rating = float(location_rating_str)
    else:
        location_rating = 0.0

    # making nested dictionary with listing_id as key and details as values
    details_dict = {}

    details_dict[listing_id] = {
        "policy_number": policy_number,
        "host_type": host_type,
        "host_name": host_name,
        "room_type": room_type,
        "location_rating": location_rating
    }

    return details_dict

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing_title_id = load_listing_results(html_path)

    listing_database = []

    for listing in listing_title_id:
        listing_title = listing[0]
        listing_id = str(listing[1])
        details = get_listing_details(listing_id)
        policy_number = details[listing_id]["policy_number"]
        host_type = details[listing_id]["host_type"]
        host_name = details[listing_id]["host_name"]
        room_type = details[listing_id]["room_type"]
        location_rating = details[listing_id]["location_rating"]

        listing_tuple = (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        listing_database.append(listing_tuple)
    
    return listing_database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    try:
        with open(filename, 'w', newline='', encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["listing_title", "listing_id", "policy_number", "host_type", "host_name", "room_type", "location_rating"])
            sorted_data = sorted(data, key=lambda x: x[6], reverse=True)
            for row in sorted_data:
                writer.writerow(row)
    except:
        print("Error writing to CSV file.")
    
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    avg_dict = {}
    
    for listing in data:
        room_type = listing[5]
        location_rating = float(listing[6])
        if location_rating != 0.0:
            if room_type not in avg_dict:
                avg_dict[room_type] = location_rating
            else:
                avg_dict[room_type] += location_rating
    
    for room_type in avg_dict:
        count = sum(1 for listing in data if listing[5] == room_type and listing[6] != 0.0)
        avg_dict[room_type] = round(avg_dict[room_type] / count, 1)
    
    return avg_dict
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_listings = []
    for listing in data:
        listing_id = listing[1]
        policy_number = listing[2]
        valid_pattern = r"^\S+-.+" # pattern for valid policy numbers, basically checks that there is some non-whitespace characters followed by a dash and more characters after
        if policy_number.capitalize() == "Pending" or policy_number == "Exempt":
            continue

        elif not re.match(valid_pattern, policy_number):
            invalid_listings.append(listing_id)

        else:
            continue

    return invalid_listings

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18)
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        details = []
        for id in html_list:
            details.append(get_listing_details(id))

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(details[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(details[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(details[2]["1944564"]["room_type"], "Entire Room")
        self.assertEqual(details[2]["1944564"]["location_rating"], 4.9)


    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for listing in self.detailed_data:
            self.assertEqual(len(listing), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(self.detailed_data[-1], ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8))

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        output_csv(self.detailed_data, out_path)

        # TODO: Read the CSV back in and store rows in a list.
        with open(out_path, 'r', encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            rows = list(reader)

        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        self.assertEqual(rows[1], ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"])

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        avg_ratings = avg_location_rating_by_room_type(self.detailed_data)

        # TODO: Check that the average for "Private Room" is 4.9.
        self.assertEqual(avg_ratings["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        invalid_listings = validate_policy_numbers(self.detailed_data)

        # TODO: Check that the list contains exactly "16204265" for this dataset.
        self.assertEqual(invalid_listings, ["16204265"])


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    # get_listing_details("467507")
    output_csv(detailed_data, "airbnb_dataset.csv")

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)