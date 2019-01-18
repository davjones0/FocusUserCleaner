# FocusUserCleaner
Python script to remove stale Focus users from AD

Step 1. Provide a relative path to a csv resembling something similar
        to the templet(column header names and order do not matter)

Step 2. Provide your eidex focus login in credentials when prompted

Step 3. Select which state you wish to run the script on

Step 4. Use the arrow keys and spacebar to select the fields you wish
        to filter by. (the search option list is populated by the headers in the csv you provide)

Step 5. Wait for the script to fetch each user's delete url, you will
        be alerted if the script cannot find a user or if the script
        recieves multiple user entries after applying a filter

Step 6. Confirm and wait for the script to finish deleting everyone
