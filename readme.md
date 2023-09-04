#YouTube Searcher 
This is simple python script that find all YouTube videos (for particular channel) that contains `YOUR WORLD or PATTERN` in title or in subtitles.

##Motivation:
I wanted to find all videos related to python from one YouTube channel.
Wrote this script to resolve this problem.

## How you use
- Clone this repo
- Create venv
- Run `pip install -r requirements.txt`
- Run `python main.py -key your_api_key -c channel_name -s search_world -r result.txt -f True`

This is all parameters that supports:
    ```

    argument("-key", "--api_key", type=str, required=True, help="The YouTube API KEY.")
    argument("-c", "--channel_name", type=str, required=True, help="The YouTube channel name.")
    argument("-s", "--search", type=str, required=True, help="World that should contain in video.")
    argument("-r", "--result_path", type=str, required=True, help="File where to put result")
    add_argument("-f", "--fast_search", type=bool, default=False, help="Scan only first 500 subtitles")

    ```

###Step-by-step instructions on how to create a YouTube Data API key:

1. Create a Google Cloud Project:
- Go to the Google Cloud Console.
- If you're not already signed in with your Google account, sign in.
- Click on the project selector at the top left corner of the page and create a new project if you don't have one already.

2. Enable the YouTube Data API:
- In the Google Cloud Console, select your project from the project selector.
- Click the hamburger menu (☰) in the top left corner and go to "APIs & Services" > "Dashboard."
- Click the "+ ENABLE APIS AND SERVICES" button.
- Search for "YouTube Data API" in the search bar.
- Select the "YouTube Data API v3" result.
- Click the "Enable" button for the API.

3. Create API Key:
- In the Google Cloud Console, navigate to "APIs & Services" > "Credentials."
- Click the "+ CREATE CREDENTIALS" button and select "API key."
- A new API key will be generated. You'll see a notification confirming this.

4. Restrict the API Key (Optional but Recommended):
 - For security reasons, it's a good practice to restrict the usage of your API key.
 - Click the API key you just created to configure it.
 - Under "Application restrictions," you can choose between:
 - "HTTP referrers (web sites)": You can specify which websites or IP addresses can use the API key.
 - "IP addresses": You can specify the exact IP addresses or range of addresses that can use the API key.
 - Under "API restrictions," you can restrict the key to specific APIs (in this case, the "YouTube Data API v3").

5. Save and Use Your API Key:
- After creating and configuring your API key, you'll see it displayed on the Credentials page.
- Copy the API key to use it in your applications.