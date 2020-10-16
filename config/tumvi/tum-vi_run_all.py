#!/usr/bin/env python3

import argparse
import subprocess
import os.path
from send2trash import send2trash
import time

sequences = [
    "room1",
    "room2",
    "room3",
    "room4",
    "room5",
    "room6"
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
    This script runs over many sequences (specified in 'sequences') of the TUM-VI dataset. Every sequence is executed 'runs_per_sequence' times. The evaluation script from TUM-RGBD (also used by ORB-SLAM3) is used to calculate the Root Mean Square Absolute Trajectory Error (RMS ATE). The median of all runs is reported in 'rmsate_summary.txt'.
    ''')
    parser.add_argument(
        "--dataset_path", help="Path to the TUM-VI dataset. Should lead to a directory that contains the folders '1024_16' and '512_16'.")
    parser.add_argument(
        "--resolution", help="Either '1024_16' or '512_16'. Default: '512_16'", default="512_16")
    parser.add_argument('--runs_per_sequence',
                        help='How often should every sequence be evaluated. Default: 3', default=3)
    args = parser.parse_args()

    runs_per_sequence = int(args.runs_per_sequence)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    # run over all sequences
    for sequence in sequences:

        bag_file = "%s/%s/dataset-%s_%s.bag" % (
            args.dataset_path, args.resolution, sequence, args.resolution)

        print("Will play the data in %s" % bag_file)

        # execute this sequence runs_per_sequence times
        for run_number in range(runs_per_sequence):
            print("Running VINS-Fusion on sequence %s run number %d" %
                  (sequence, run_number + 1))

            # execute VINS Fusion
            roscore = subprocess.Popen(["roscore"])

            time.sleep(5)

            rviz = subprocess.Popen(["roslaunch", "vins", "vins_rviz.launch"])

            vins_proc = subprocess.Popen(["rosrun",
                                          "vins",
                                          "vins_node",
                                          "%s/tumvi_stereo_imu_config_%s.yaml" % (dir_path, args.resolution.split("_")[0])],
                                         cwd=dir_path)

            subprocess.run(["rosbag", "play", bag_file], cwd=dir_path)

            vins_proc.kill()
            rviz.kill()
            roscore.kill()
