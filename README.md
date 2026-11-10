# Game Cabinet

**Your collection. Your game nights. All in one place.**

Game Cabinet is a web application designed to help people organize, catalog, and keep track of their board game and puzzle
collections. Beyond simply storing information about the games you own, Game Cabinet aims to capture experiences, ratings, and
statistics associated with playing them.

Whether you are looking for your next family game night activity, trying to remember someone's favorite game, or deciding what
game to buy as a birthday present, Game Cabinet helps you make more of your collection.

## Table of Contents

- Project Overview
- Goals and Features
- Planned Database Structure
- Technology Stack
- Project Structure
- Getting Started
- Git Workflow and Branching
- Contributing
- Future Possibilities

## Project Overview

Game Cabinet is a collection management and game-tracking application that allows users to maintain a digital catalog of their
board games and puzzles.

Users will be able to:
- Maintain a personal catalog of the games and puzzles they own
- Record individual game sessions and track who participated
- Rate games and review their ratings over time
- View statistics about their collections and playing habits
- Discover personal favorites and receive recommendations

The application is intended to support multiple users, each with their own collections, player profiles, and game histories.

An additional goal is to develop a shared game catalog containing standardized information about games and puzzles. Users will be
able to select existing entries from this catalog or submit new entries for review.

## Goals and Features

### Core Features

The following features represent the primary goals of the project:

| Feature              | Description                                            | Status  |
| :------------------- | :----------------------------------------------------- | :------ |
| User Accounts        | Allow users to create accounts and sign in             | Planned |
| Game Catalog         | Browse and search a catalog of board games             | Planned |
| Puzzle Catalog       | Browse and search a catalog of puzzles                 | Planned |
| Personal Collections | Add games or puzzles to a user's collection            | Planned |
| Player Profiles      | Create and manage player profiles                      | Planned |
| Game Sessions        | Record individual instances of playing a game          | Planned |
| Game Ratings         | Allow players to rate game sessions out of five stars  | Planned |
| Statistics           | Calculate averages, play counts, and player statistics | Planned |

## Additional Features

Potential features for future development include:
- **Personalized Recommendations:** suggest games based on a player's previous ratings and preferences
- **Birthday Recommendations:** identify a player's favorite games and genres to suggest birthday gifts or activities
- **Collection Analytics:** visualize playing habits, most-played games, highest-rated games, and other statistics
- **Shared Game Catalog:** allow users to submit new games and puzzles for review and inclusion in the global catalog
- **Game Images:** include images of game boxes and puzzles to make identification easier
- **Player Profile Images:** allow users to personalize their player profiles
- **Expansion Tracking:** keep track of expansions and additional content owned for individual games

## Planned Database Structure

The database will use a relational structure to organize games, puzzles, users, players, and game sessions.

The following tables represent the initial conceptual design. The schema may evolve as development progresses.

| Table                | Purpose                                                                |
| :------------------- | :--------------------------------------------------------------------- |
| Games                | Stores standardized information and authentication-related data        |
| Genres               | Stores standardized game genres                                        |
| Puzzles              | Stores standardized information about puzzles                          |
| Players              | Stores account information and authentication-related data             |
| Play Sessions        | Records individual game sessions                                       |
| Session Participants | Connects players to sessions and stores individual results and ratings |
| Collections          | Connects users to the games and puzzles they own                       |

### Database Design Considerations

- Each table should have a unique primary key
- Foreign keys should be used to maintain relationships between tables
- Many-to-many relationships should be handled through junction tables
- Game and puzzle information should be separated from user-specific collection information
- Ratings should be associated with individual game sessions and players rather than stored as a single value on a game
- Calculated statistics (average ratings, total play counts) should be derived from recorded data wherever possible

The database will be designed with **scalability** and future feature development in mind.

## Technology Stack

The technology stack is currently being determined.
- Front-end: Django
- Back-end: Django
- Database: SQLite
- Authentication: Django
- Deployment: Firebase
- Version Control: Git and GitHub

## Project Structure

The project directory structure will be documented here as development progresses.

The current project structure is:
```
README.md
```

## Getting Started

### Prerequisites

Installation requirements will be documented as the technology stack is finalized.

### Installation

Clone the repository:
```
git clone https://github.com/selahf/game-cabinet
```

Navigate to the project directory:
```
cd game-closet
```

Install dependencies:
```
pip install -r requirements.txt
```

Detailed setup instructions will be added as the project develops.

## Git Workflow and Branching

**IMPORTANT:** Please use branches when developing new features or making changes!

Branches allow multiple contributors to work on different parts of the project simultaneously without directly modifying the main
codebase. They help keep development organized, make it easier to review changes, and reduce the risk of accidentally breaking
working code.

### Branch Structure

- `main`: the stable, primary branch; should contain working, reviewed code
- `feature/<feature-name>`: new features and functionality
- `bugfix/<bug-name>`: fixes for existing bugs
- `docs/<description>`: documentation changes

Examples include:
```bash
feature/user-authentication
bugfix/database-connection
docs/readme-update
```

### Starting a New Feature

1. Make sure your local main branch is up to date.

```bash
git switch main
git pull origin main
```

2. Create a new branch for your work.

```bash
git switch -c feature/your-feature-name
```

3. Make changes and commit to your own branch.

```bash
git add .
git commit -m "Add description of changes"
```

4. Push your branch to GitHub.

```bash
git push -u origin feature/your-feature-name
```

5. Create a Pull Request (PR).

Open GitHub and create a Pull Request from your feature branch into `main`.
- Describe what you changed
- Explain any important implementation decisions
- Request review from that week's team leader
- Address any feedback before merging

6. Merge your PR.

Once the changes have been made, the team leader for the week will merge your PR into `main`.

Then you can start the process all over again!

### Important Reminders

- **Never work directly on `main`**
- Always create a new branch for a feature, bug fix, or substantial change
- Keep branches focused on one task whenever possible
- Commit regularly with descriptive commit messages
- Pull the latest changes from `main` before beginning new work
- Use Pull Requests to merge changes into `main`
- Communicate with teammates when modifying shared files or working on overlapping features

## If You Need to Update Your Feature Branch

If `main` has changed while you are working on your feature, you may need to bring those changes into your branch.

```bash
git switch main
git pull origin main
git switch feature/your-feature-name
git merge main
```

Resolve any merge conflicts, test your changes, and push to the updated branch.

**Remember:** Branches are there to make collaboration easier. Please use them!

## Contributing

Game Cabinet is a collaborative development project.

When contributing:

1. Check the project board for assigned tasks and ongoing work.
2. Coordinate with teammates before beginning overlapping work.
3. Follow the Git branch workflow.
4. Write clear, descriptive commit messages.
5. Test your changes before submitting a Pull Request.
6. Document significant changes when appropriate.

All contributors are encouraged to communicate, ask questions, and share ideas as the project evolves.

## Future Possibilities

Game Cabinet is designed to grow beyond its initial functionality.

Some longer-term possibilities include:
- A dedicated mobile application
- Advanced game recommendation algorithms
- Collection sharing between family members and friends
- Global game and puzzle catalog contributions
- Visual dashboards and interactive statistics
- Integration with external board game databases
- Achievement systems and personalized gaming summaries

The goal is to create an application that makes organizing and enjoying your game collection easier while preserving the
experiences associated with it.

## Project Information

**Project Name:** Game Cabinet
**Course:** Web Application Development
**Repository:** https://github.com/selahf/game-cabinet
**Contributors:**
- Selah Frederickson
- Carter Hoffman
- Caden Schneider
