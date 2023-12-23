To run tests, make sure that your virtual environment is set to the one inside this repository,
or that your local environment is Python 3.6.8 with Hypothesis, Pytest, and any other requirements
installed.

Some of these tests are property-based, others are behavior-based. Specific unit-tests are reserved
to the modules that ask for them (xboard, xstate, xtree, etc.), and there would be no gain from running
the tests twice.

Anyway, if your aim is to run these tests,
simply run 'pytest [name of test file]'.

Some will appear to run slow, because the default minimum number of tests
is 100, and in no cases have I decreased the minimum number of tests runs
(in some cases I increase the number).
