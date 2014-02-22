ek-calc
====================

Version .1.0
Simulation calculator for the game Elemental Kingdoms by Arcannis.

Motivation
-----------------

The intent of this simulator is to allow people to analyze different strategies for Demon Invasion events in Elemental Kingoms.  The fighting mechanics in this simulator should allow for people to simulate any PvP or PvE fight as well.

You can tell the simulator to run ``X`` times and it will report the average damage done per simulated fight as well as the average damage per minute based on the cost of the deck used.

Using this information it should be possible to optimize your deck based on the cards you have available in the game.

The way the simulator is designed allows for additional cards to be created without modifying the mechanics simulator.  Each card should inheret from the base class ``Card``, properly implement the methods and define the parameters.  If done properly the simulator can use the card.  If you decide to add a card you'll need to ensure that it's abilities are available as well.

Adding an ability is similar to adding a card.  Each ability should inheret from the base ``Ability`` class, properly implement the methods and define the parameters.  If done properly the simulator will know how the ability works with the card each card that uses it.


Requirements
-----------------

Python 3.3+

Install
-----------------

I have not yet packaged this project and registered it with PyPI - although I plan to in the future.  For now you'll need to clone the project and run the simulation manually.::

    $ git clone git@github.com:ricomoss/ek-calc.git
    
Or you can create your own fork to make code changes yourself.  If you plan to contribute to the project please fork and submit pull requests from a branch on your fork to the dev branch of this project.


Releases and Branches
-----------------

The master branch is meant for release.  Upon an update to the master branch the version will increment according to the format: (major).(minor).(micro)

The dev branch holds all approved updates to the project until a release milestone is met, at which time dev will be merged into master.

Development is done on branches from dev and merge via pull requests into dev. Everyone is encouraged to fork this repo and create pull requests with additions they would like to see in the project.


API Definition
-----------------

Due to the immaturity of this project an API hasn't been defined yet.  This should be available in future releases.

Usage
-----------------

Currently the usage of the simulator requires some manual entries in the ``run_simulation.py`` file.  Once the project matures the API will be built out to allow for a more elegant interface.

Within ``run_simulation.py`` you can create a player and assign cards to the player.  Simply instantiate a player with the desired level.  Then instantiate each card you want the player to have.  Then assign the card to the player.

This example would create a level 25 player with 2 cards in their deck - a level 1 Headless Horseman and a level 8 Headless Horseman.:

    player = Player(25)

    card1 = cards.HeadlessHorseman(1)
    card2 = cards.HeadlessHorseman(8)

    player.assign_card(card1)
    player.assign_card(card2)
    
Then create an opponent player or demon player in a similar fashion.:

    demon_player = demons.DemonPlayer()
    
    demon_card = demons.DarkTitan())
    
    demon_player.assign_card(demon_card)
    
Since demon players and demon cards have a pre-set level associated with them you do not instantiate them with any level information.

Once you've create the player and demons to have the cards you want to simulate just run the simulator.:

    $ python3 run_simulation.py
    

