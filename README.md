ek-calc
====================

Version 0.1.0
Simulation calculator for the game Elemental Kingdoms by Arcannis.

Motivation
-----------------

The intent of this simulator is to allow people to analyze different strategies for Demon Invasion events in Elemental Kingoms.  The fighting mechanics in this simulator should allow for people to simulate any PvP or PvE fight as well.

You can tell the simulator to run ``X`` times and it will report the average damage done per simulated fight as well as the average damage per minute based on the cost of the deck used.

Using this information it should be possible to optimize your deck based on the cards you have available in the game.

The way the simulator is designed allows for additional cards to be created without modifying the mechanics simulator.  Each card should inheret from the base class ``Card``, properly implement the methods and define the parameters.  If done properly the simulator can use the card.  If you decide to add a card you'll need to ensure that it's abilities are available as well.

Adding an ability is similar to adding a card.  Each ability should inheret from the base ``Ability`` class, properly implement the methods and define the parameters.  If done properly the simulator will know how the ability works with the each card that uses it.


Requirements
-----------------

Python 3.3+

Install
-----------------

I have not yet packaged this project and registered it with PyPI - although I plan to in the future.  For now you'll need to clone the project and run the simulation manually.

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

Currently the usage of the simulator requires some manual entries in the ``my_cards.py`` file.  Once the project matures the API will be built out to allow for a more elegant interface.

Within ``my_cards.py`` you can list cards that will be assigned to a player, the player level you want used, the demon card you want to fight against and which runes to use.  Simply list the card as a tuple with the card object and the level of the card.  Then execute the ``run_simulation.py`` script with an argument for the number of simulations per deck you want to run.

This example would create a level 25 player to fight against Sea King.  The simulator will take every deck combination possible with the following cards, and every rune permutation possible (rune order matters) with the runes listed below.:

    PLAYER_LVL = 25
    DEMON_CARD = demons.SeaKing
    
    player_deck = (
        (cards.HeadlessHorseman, 10),
        (cards.HeadlessHorseman, 10),
        (cards.SkeletonKing, 5),
        (cards.SkeletonKing, 8),
        (cards.WoodElfArcher, 6),
        (cards.WoodElfArcher, 10),
        (cards.DemonicImp, 8),
        (cards.DemonicImp, 10),
    )
    
    player_runes = (
        (runes.Revival, 1),
        (runes.Leaf, 4),
    )

Once you've defined the above lists just run the simulator.:

    $ python3 run_simulation.py <num_of_simulations_per_deck>
    
Suppose you want to run 100 simulations per deck combination:

    $ python3 run_simulation.py 100
    
Be careful with the number of simulations you ask for.  The formula for the number of combinations grows very rapidly (http://en.wikipedia.org/wiki/Combination).  The above example will give 102000 total simulations.

    

