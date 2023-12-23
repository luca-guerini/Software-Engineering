This repository is a copy of the work I did during my semester in a Software Engineering course at Seton Hall University.
If you would like to see the Professor's assignments they are here:
https://jasonhemann.github.io/22FA-CSAS4117/index.html

PROJECT SUMMARY:
    The course had five small modules (A, B, C, D, and E) where the students selected two programming languages,
    the Professor approved one, and for five assignments the students completed modules in the approved language
    as exercises to vet the usefulness of the language for the semester's major project.

    Students were to complete all coursework in pairs or groups of three.

    These modules built up to "Fish.com,"---the chief project for the semester---which involved building a Game based off of "Hey! That's my Fish!", supporting online play, and possessing an API that allowed players to play games with their own bots. The project was to be completed in multiple project milestones (1-6) with each phase being revealed a week or two after the last.

    At a certain point, students would swap repositories with other student groups and pick up where they left off, hoping that the code they received was in some manner readable, and that during stand up and code walks the code they would receive would be thoroughly vetted and documented.

    The course has a reputation for being among the toughest CS courses taught by one of the toughest professors in the major,
    so the class started with 13 registered students, with only 3 arriving to the first class, and only myself and one other student
    sticking through the class until the end of the semester. Since the numbers in our class were so small, we had the unique
    opportunity to conduct coursework designed to be completed in groups as individuals.

    When I find the time to do so, I'd like to rewrite and recomplete the Fish project here in Haskell, Racket, or Rust because
    this course led me to become disillusioned with some of Python's design decisions; especially its packaging system. Still, Javascript remains by far my least favorite language and I pray every night before bed that I will not have to use that language.

SETUP:

    To run the python modules in this program, I've streamlined the process of installing dependencies to the build_venv
    script located at this layer of the directory tree. Simply run the bash script and it will peform the heavy lifting
    for you.

IMPORTANT NOTES:
    This script assumes python3.6 is the command to access Python 3.6.8. If your command is different, replace "python3.6" with the appropriate command.

    The script activates the virtual environment, installs the required packages from requirements.txt, and then deactivates the environment.
    Make sure you have the required permissions to execute these commands and create directories.