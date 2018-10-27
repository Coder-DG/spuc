# SPUC - Cross Platform User Creator
This tool can create users in different platforms given credential configurations
 and user configurations.

## Usage

### Quickstart

This example will show how to create a user in Google Apps.

First, to turn on Google Directory API follow step 1 at [this quickstart
tutorial](https://developers.google.com/admin-sdk/directory/v1/quickstart/python#step_1_turn_on_the_api_name)

Second, write user parameters in a json format to represent and save it. For this
quickstart tutorial we'll use a simple set of parameters:
 ```
 {
   "name": {
     "familyName": "Surname",
     "givenName": "Firstname"
   },
   "password": "Aa123456!@#",
   "primaryEmail": "test@gigaspaces.com"
 }
 ```

Now here comes the fun part. Run the command `spuc googleapps create -p
"/path/to/client_secret.json" -u "/path/to/google_user.json"`.

If you haven't authenticated for a while, spuc will open a browser window and
will ask you to log in. Once you've logged in, the user will be created and
 spuc will print the user configuration in a json format.
