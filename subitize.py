# subitize.py - Subitizing Experiment
# Name: Mark Thomas
#
# This experiment aims to demonstrate the subitizing phenomenon. Subitizing, originating
# in EL Kaufman et al.'s "The Discrimination of Visual Number" in 1949, refers to
# the way that people can make quick, accurate counts of small numbers of items.
#
# Previous work has shown that humans can quickly count groups of up to size 4,
# but that accuracy decreases, and response time increases, for groups of size 5
# or greater. In this experiment, we will measure participants' performance when
# counting groups of circles of up to size 10.
#
# This experiment has 3 blocks of 10 trials. At each trial, after being shown a
# fixation cross for 1 second, participants are shown between 1-10 white circles
# on a black background for up to 1 second (or until the user presses a key).
# Then, the screen is cleared and participants are asked how many circles they
# counted. The program waits for the participant to press a number (between 0-9
# where 0 means 10) before beginning the next trial.
#
# For each trial, we store the block number, trial number, correct response (i.e.
# the actual number of circles shown), participant response (i.e. the number of
# circles that the participant counted/entered), whether or not their guess was
# correct, and their response time (in seconds, from the time the circles were
# shown to the time the participant entered their guess).
#
# After all trials are completed, some basic information about the participant's
# performance is printed to the terminal, and the results are saved to a .csv
# file in the ./data directry.


#=====================
#IMPORT MODULES
#=====================
import os                      # for handling paths
import random                  # for randomizing conditions
from datetime import datetime  # for getting the current dat

import pandas as pd            # for storing results in a dataframe/saving to .csv
from psychopy import core, event, gui, visual, monitors  # for experiment functions


#=====================
#PATH SETTINGS
#=====================
# set the path for our saved results files (./data)
directory = os.getcwd()
data_dir = os.path.join(directory, 'data')
if not os.path.exists(data_dir):  # if it doesn't already exist, create the directory
    os.makedirs(data_dir)


#=====================
#COLLECT PARTICIPANT INFO
#=====================
# create a dialog to collect participant info; we only collect a participant's
# subject number (which we use to create a unique filename)
experiment_info = {'subject_number': 1}
participant_info_dialog = gui.DlgFromDict(dictionary=experiment_info,
                                          title="Experiment Info")

# get the current date
date = datetime.now()
experiment_info['date'] = f"{date.day}-{date.month}-{date.year}"

# create a unique filename (based on the subject number and current date)
# for the experiment's results file
experiment_filename = (f"subject{experiment_info['subject_number']}_"
                       f"{experiment_info['date']}_"
                       f"results.csv")
experiment_filename = os.path.join(data_dir, experiment_filename)  # include directory


#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
N_BLOCKS = 3
N_TRIALS = 10

BLOCK_START_DURATION = 2  # number of seconds to wait before starting each block

CIRCLE_COLOR = 'white'
CIRCLE_RADIUS = 9                    # (pixels)
CIRCLE_DIAMETER = CIRCLE_RADIUS * 2  # (pixels)
CIRCLE_DURATION = 1  # number of seconds the circles are shown for on each trial

FIX_DURATION = 1       # number of seconds the fixation cross is shown for on each trial


#=====================
#PREPARE CONDITION LISTS
#=====================
# holds all conditions for a block; we vary the conditions by shuffling this list
# at the start of each block
# the condition list contains integers denoting the number of circles that should
# be shown for each trial
conditions = [trial_i for trial_i in range(1, N_TRIALS+1)]


#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
# lists holding information about each trial and participant interactions
block_n = []               # block number
trial_n = []               # trial number
correct_response = []      # the actual number of circles
participant_response = []  # the number of circles the participant counted
was_correct = []           # whether or not the participant counted the correct number of circles
rt_list = []               # participant response time


#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
# create a monitor
mon = monitors.Monitor('myMonitor', width=61, distance=60)  # horizontal width(cm), distance from monitor(cm)
mon.setSizePix([1920, 1080])                                # monitor's resolution (pixels)

# create window
WINDOW_X = 600      # width
WINDOW_Y = 600      # height
WINDOW_PADDING=200  # outer frame (stimuli will not be drawn within this many pixels from the edge)
win = visual.Window(
    monitor=mon,               # use the monitor defined above
    fullscr=False,             # don't use fullscreen mode
    size=(WINDOW_X,WINDOW_Y),  # size of the window
    color='black',             # use a black background
    units='pix'                # pixel units
)
win.mouseVisible = False  # make the mouse pointer invisible

# create a transparent rectangle with a white border (that acts as a frame to draw stimuli within)
border = visual.Rect(win=win,
                     lineColor='white',
                     fillColor=None,
                     width=WINDOW_X-WINDOW_PADDING,
                     height=WINDOW_Y-WINDOW_PADDING)

# create a fixation cross
fix_stim = visual.TextStim(win, text='+')

# experiment instructions to display to the participant
instructions_text = (f"Subitizing Experiment\n\n"
                     f"For each trial, between 1-10 circles will be shown.\n"
                     f"When asked, press the number key (0-9; 0 means 10)\n"
                     f"representing how many circles you counted.\n\n"
                     f"There will be {N_BLOCKS} blocks of {N_TRIALS} trials.\n\n"
                     f"Press any key to begin.")

# create a text stimulus (with text initialized to the instructions)
text_stim = visual.TextStim(win, text=instructions_text)


#=====================
#START EXPERIMENT
#=====================
# initialize a clock to measure RT
timer = core.Clock()

# display experiment instructions
text_stim.draw()
win.flip()
# wait for the participant to press a key before beginning the experiment
keys = event.waitKeys()


#=====================
#BLOCK SEQUENCE
#=====================
for block_i in range(1, N_BLOCKS+1):
    # display block start message
    text_stim.text = f"Starting Block {block_i}"
    text_stim.draw()
    border.draw()
    win.flip()
    core.wait(BLOCK_START_DURATION)  # wait before starting each block

    #=====================
    #TRIAL SEQUENCE
    #=====================
    random.shuffle(conditions)  # randomize conditions' order for the block
    for trial_i in range(N_TRIALS):
        n_circles = conditions[trial_i]  # get the number of circles for this trial
        #=====================
        #START TRIAL
        #=====================
        # display fixation cross
        fix_stim.draw()
        border.draw()
        win.flip()
        core.wait(FIX_DURATION)

        # randomly generate positions for each circle; ensure that no two circles overlap
        valid_positions = []
        for circle_i in range(n_circles):
            valid = False
            # continuously try to generate new positions until we find a valid one
            while not valid:
                valid = True
                # generate random(x, y) coordinates
                x = random.randint((-WINDOW_X/2)+CIRCLE_DIAMETER+WINDOW_PADDING+1,
                                   (WINDOW_X/2)-CIRCLE_DIAMETER-WINDOW_PADDING-1)

                y = random.randint((-WINDOW_Y/2)+CIRCLE_DIAMETER+WINDOW_PADDING+1,
                                   (WINDOW_Y/2)-CIRCLE_DIAMETER-WINDOW_PADDING-1)

                # compare the new point against each of the valid positions
                # we've already found; if their distance is less than the circles'
                # diameter, it means they overlap, so the new position is not valid
                for pos_x, pos_y in valid_positions:
                    # measure Euclidean distance between points
                    if ((x - pos_x)**2 + (y - pos_y)**2)**(1/2) <= CIRCLE_DIAMETER:
                        valid = False
                        break

            # store the position that we found (we know it is valid)
            valid_positions.append((x, y))
            # draw a circle at the position
            visual.Circle(win=win,
                          radius=CIRCLE_RADIUS,
                          pos=(x, y),
                          lineColor=CIRCLE_COLOR,
                          fillColor=CIRCLE_COLOR,
                          units='pix').draw()
        border.draw()
        # quickly display the circles we generated to the participant
        event.clearEvents()  # ensure the event buffer is empty (in case the participant pressed keys earlier)
        win.flip()
        core.wait(CIRCLE_DURATION)

        text_stim.text = "How many circles did you count?\nEnter a number from 0-9 (0 means 10)."
        text_stim.draw()
        border.draw()
        win.flip()  # the screen will be cleared
        time_asked = timer.getTime()

        # ask the participant how many circles they counted
        keys = event.getKeys()
        if not keys or not keys[0].isnumeric() or not 0 <= int(keys[0]) <= 9:
            keys = event.waitKeys(keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
        rt = timer.getTime() - time_asked
        response = int(keys[0])  # get the first key the participant pressed

        # save information about the trial and the participant's response
        block_n.append(block_i)
        trial_n.append(trial_i)
        correct_response.append(n_circles)
        participant_response.append(response)
        was_correct.append(n_circles == response)
        rt_list.append(rt)

#======================
# END OF EXPERIMENT
#======================
# after all blocks, wait for the participant to press any key to end the experiment
text_stim.text = "Experiment complete.\n Press any key to exit."
text_stim.draw()
border.draw()
win.flip()
keys = event.waitKeys()

# close the window
win.close()

# create a DataFrame from the gathered results
results = zip(block_n, trial_n, correct_response, participant_response, was_correct, rt_list)
results = pd.DataFrame(results, columns=['block',
                                         'trial',
                                         'n_objects_actual',
                                         'n_objects_guessed',
                                         'correct',
                                         'rt'])


# print information about the participant's performance
## accuracy
print("\nPer-Block Accuracy")
for block_i, percent_correct in results.groupby('block')['correct'].agg("mean").items():
    print(f"Block {block_i}: {round(percent_correct*100, 5)}%")

print("\nPer-Circles Accuracy")
for n_objects, percent_correct in results.groupby('n_objects_actual')['correct'].agg("mean").items():
    print(f"{n_objects} circles: {round(percent_correct*100, 5)}%")
print()

print(f"Overall Accuracy: {round(results['correct'].agg('mean')*100, 5)}%")


print('-'*10)


## RT
print("\nPer-Block RT")
for block_i, rt in results.groupby('block')['rt'].agg("mean").items():
    print(f"Block {block_i}: {round(rt, 5)}s")

print("\nPer-Circles RT")
for n_objects, rt in results.groupby('n_objects_actual')['rt'].agg("mean").items():
    print(f"{n_objects} circles: {round(rt, 5)}s")
print()

print(f"Overall RT: {round(results['rt'].agg('mean'), 5)}s")


# write results to a .csv file
results.to_csv(experiment_filename, index=False)
