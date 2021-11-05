# CheckRetailerPagesForUpdates
Because you need to buy toliet paper ... or a Intel Core i9-10900K.

### Description
You can configure a list of URLs to observe for changes.  The changes are observed via a list of specified XPaths, which you can also configure. 

### Requirements
I made the choice to use Discord Webhooks as I didn't want to purchase a Twilio subscription, so you'll need to generate a webhook for your Discord server.  I'm using Selenium to drive the webbrowser, so feel free to use your WebDriver of choice.  Both of the aforementioned options can be configured in the main driver Python script.  This also makes use of the "say" command on MacOS so your computer can yell at you when your product of choice is available.
