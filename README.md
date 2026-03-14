# QudSpecies API

An API for studying the creatures featured in the game 'Caves of Qud'.

This API provides endpoints for sorting through creature's stats, mutations, anatomy, and even specific body parts. It also has features for analysing patterns between creatures, such as the most common mutations or average stats by tier.

Developed to be a reasource for players and the modding community. Hopefully this will help you create some crazy builds or creatures!

## Using the API

Import scripts -
- To use import scripts, move them and the XML files from Caves of Qud's Source (Bodies.XML, Creatures.XML, Mutations.XML, HiddenMutations.XML, Skills.XML) to the root. Run them all.

To run the server, do
- python manage.py runserver

The API will be accessible at http://127.0.0.1:8000/api/

The API has also been deployed on PythonAnywhere, accessible here https://kaddykins.eu.pythonanywhere.com/api/

## Documentation

The documentation can be accessed at http://127.0.0.1:8000/api/docs/ or at as a PDF [here](<QudSpecies API Docs.pdf>)