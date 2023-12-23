Greetings Professor.

The xstate harness works by:
1. Marshalling the JSON
2. Performing the LazyStrategy transformation.
3. Comparing the JSON of the board state that results from it to the value of #-out.json

Note. The test harness xstate ASSUMES that every file named (something)-in.json has a
companion called (something)-out.json. If one does not exist, it will inform you that
the test failed.

Additionally, the test harness ASSUMES that all test files are suffixed as:
-in.json and
-out.json

If every (something)-in.json corresponds with a (something_-out.json all tests should succeed

Cheers.
