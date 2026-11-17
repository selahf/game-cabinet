# Game Cabinet: External API Research

## Purpose

This document explains why Game Cabinet would benefit from external game databases and outlines some potential options.

## Potential API Providers

**BoardGameGeek** is the strongest contender for a game API at this time. It has a substantial database of board games,
and its XML API allows developers to search for games and retreive detailed information about them.

However, there are some important technical considerations with this API:
- Developers are required to *register* applications and obtain authorization for nearly all API usage
- Noncommercial applications may qualify for a free license, but approval is not guaranteed
- It is recommended that requests are made from the application's server and results are cached rather than repeatedly querying
- It is recommended that there users wait five seconds before making another request
- Public-facing applications must credit BoardGameGeek and display its logo

Another option for a game API was **Board Game Atlas**, but upon further research, it was revealed that this database no longer
exists, so it would not be possible for us to use it.

There is no obvious choice for puzzle APIs. Most manufacturers have product catalogs, but they may not be publicly available
as APIs suitable for this application.

## Available Information

The **BoardGameGeek** API provides information such as:
- Identifiers and titles
- Minimum and maximum players
- Minimum suggested age
- Playing times
- High-resolution cover images
- Publishers
- Genres
- Data from community polls

## Recommendation

There are a few paths forward, some of which are more enticing than others. I have arranged them in a spectrum of sorts.

### 1. Apply for a License through BoardGameGeek

One method forward would be to apply for a license. However, since we do not know when this would be approved (or denied), it may
not be the most suitable for this project.

### 2. Download BoardGameGeek Data Once

Registered users can download a small amount of data themselves, so we could simply create an account and download game data from
a single point in time. It would not update as BoardGameGeek maintains it, but that might be okay for our purposes.

### 3. Use a Smaller BoardGameGeek Dataset

There are some smaller datasets that have been made available by people online. They are similarly snapshots in time and will not
update alongside BoardGameGeek, but they may be more manageable than the enormous dataset provided by the website itself.

### 4. Use Citizen Science-Style Game Logging

If it becomes too complicated to use a dataset or we decide to go in a different direction, we could ultimately create a way for users
to input their own games, both as a part of their household collection and as a part of the global database. Submitting to the
global database would need to require administrative approval so that multiple copies of a single game are not submitted.

## Sources:

- https://boardgamegeek.com/using_the_xml_api
- https://boardgamegeek.com/wiki/page/BGG_XML_API2
- https://mixedconclusions.com/blog/boardgames_part_one/#:~:text=The%20BoardGameGeek%20XML%20API%20*%20type%3Dboardgame%2Cboardgameexpansion%2Cboardgameaccessory%2Cvideogame%2Crpgitem%2Crpgissue%20is,gets%20ratings%20and%20other%20statistics.%20*%20id%3D1%2C4%2C
