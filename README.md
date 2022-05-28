# oauth2-notion

This project aims at providing the basis for building a public Notion integration on top of their API. 
Notion API uses Google Oauth2 as a standard for user authentication. As long as I have researched, this is the first public project showing a full framework for the implementation of the authorization using Python. 

## About Notion API
The API provides a lot of features for interacting with workspaces remotely. Complexity comes when you try to connect with a third party workspace.
This project requires previous knowledge:

* Private integrations in Notion: 

## Technical details
This project was built to be integrated with some cloud service - such as Heroku, Ocean or AWS. I've tested this script in both Heroku and DigitalOcean.
The project also integrates a Postgres relational database to store the secret gotten during the authorization process.

## How to use it
oauth2-notion is almost ready to use. A simple deploy in your cloud provider will make it work. 
The only point you will need to set up manually is the private key to connect with yout Notion App. oauth2-notion assumes you have your secret declared as a environment variable named SECRET_KEY.In case you decide not to use it this way, make sure you get the proper adjustments on the main session of this project.

After deployed, access to yout Notion App could be granted to any user if they access the link formed by:
__________________

