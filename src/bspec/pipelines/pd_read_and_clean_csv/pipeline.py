import os
import sys
import json


if getattr(sys, "frozen", False):
    # running as bundle (aka frozen)
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # running live
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

pipeline_path = os.path.join(BASE_DIR, "pipeline.json")

with open(pipeline_path) as file:
    pipeline = json.load(file)
