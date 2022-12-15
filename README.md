# subitize.py - Subitizing Experiment
## Name: Mark Thomas

This experiment aims to demonstrate the subitizing phenomenon. Subitizing, originating in EL Kaufman et al.'s "The Discrimination of Visual Number" in 1949, refers to the way that people can make quick, accurate counts of small numbers of items. Previous work has shown that humans can quickly count groups of up to size 4, but that accuracy decreases, and response time increases, for groups of size 5 or greater. In this experiment, we will measure participants' performance when counting groups of circles of up to size 10.

This experiment has 3 blocks of 10 trials. At each trial, after being shown a fixation cross for 1 second, participants are shown between 1-10 white circles on a black background for up to 1 second (or until the user presses a key). Then, the screen is cleared and participants are asked how many circles they counted. The program waits for the participant to press a number (between 0-9 where 0 means 10) before beginning the next trial.

For each trial, we store the block number, trial number, correct response (i.e. the actual number of circles shown), participant response (i.e. the number of circles that the participant counted/entered), whether or not their guess was correct, and their response time (in seconds, from the time the circles were shown to the time the participant entered their guess).

After all trials are completed, some basic information about the participant's performance is printed to the terminal, and the results are saved to a .csv file in the ./data directry.
