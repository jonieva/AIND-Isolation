import SpearmintClient
import time
from subprocess import call
import json

spearmint_parameters = {}
spearmint_parameters['w_my_moves'] = {'min': -10., 'max': 10., 'type': 'float'}
spearmint_parameters['w_opponent_moves'] = {'min': -10., 'max': 10., 'type': 'float'}
spearmint_parameters['w_center_distance'] = {'min': -10., 'max': 10., 'type': 'float'}
spearmint_parameters['w_opponent_center_distance'] = {'min': -10., 'max': 10., 'type': 'float'}
spearmint_parameters['w_opponent_distance'] = {'min': -10., 'max': 10., 'type': 'float'}
spearmint_parameters['w_chase_opponent_factor'] = {'min': -10., 'max': 10., 'type': 'float'}


# w_my_moves = float(lines[0])                # Weight for my moves
#     w_opponent_moves = float(lines[1])          # Weight for opponent moves
#     w_center_distance = float(lines[2])         # Weight for distance to the center of the board
#     w_opponent_center_distance = float(lines[3])# Weight for opponent distance to the center of the board
#     w_opponent_distance = float(lines[4])       # Weight for distance to the opponent
#     w_chase_opponent_factor = float(lines[5])   # Extra boost. If we are in one of the opponents legal moves,
#



outcome = {'name': 'Wins', 'minimize': False}
scientist = SpearmintClient.Experiment(name="Udacity_Isolation_6_AB_Improved_Only_lower_range",
                                       parameters=spearmint_parameters,
                                       outcome=outcome,
                                       access_token='oMYJ0G0iERenyZNlfSetN5fbuC3lKs',
                                       run_mode='local')

num_reps = 1
for it in range(1000):
    # Execute the function num_reps times and do an average
    total_score = 0.0
    suggested_spearmint_parameters = scientist.suggest()
    with open("/Users/jonieva/Projects/jorge/udacity/ia/term1/AIND-Isolation/params.txt", 'w') as f:
        # for p in suggested_spearmint_parameters.values():
        #     f.write("{}\n".format(p))
        f.write(json.dumps(suggested_spearmint_parameters, indent=4, sort_keys=False))

    t1 = time.time()
    for rep in range(num_reps):
        t_it = time.time()
        # Start the tournament
        call(["/Users/jonieva/miniconda3/envs/challenge/bin/python",
              "/Users/jonieva/Projects/jorge/udacity/ia/term1/AIND-Isolation/tournament2.py"])
        print ("Iteration time: {}s".format(time.time()-t_it))
        # Read the result
        with open("/Users/jonieva/Projects/jorge/udacity/ia/term1/AIND-Isolation/out.txt", 'r') as f:
            score = float(f.read())
        total_score += score
    total_score /= num_reps
    print("Total configuration time: {}s. Score: {}".format(time.time()-t1, total_score))
    scientist.update(suggested_spearmint_parameters, total_score)
