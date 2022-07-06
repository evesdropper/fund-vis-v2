import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import api

def cmd_input(args):
    command = args[0]
    if command == "cron":
        api.write_to_csv()
    else:
        print("Imposter Alert")

args = sys.argv[1:]
if len(args) == 0:
    print(f"No arguments given.")
else:
    cmd_input(args)