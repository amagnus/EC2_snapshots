# Usage: python snap.py volume_id number_of_snapshots_to_keep

import boto
import sys
from datetime import datetime

conn = boto.connect_ec2()
regions = boto.ec2.regions()

# us-west-1 region is selected here
conn_us = regions[5].connect()

vol_id = sys.argv[1]
keep = int(sys.argv[2])

volumes = conn_us.get_all_volumes([vol_id])
volume = volumes[0]

description = 'Created by snap.py at ' + datetime.today().isoformat(' ')

volume.create_snapshot(description)
snapshots = volume.snapshots()

def date_compare(snap1, snap2):
    if snap1.start_time < snap2.start_time:
        return -1
    elif snap1.start_time == snap2.start_time:
        return 0
    return 1

snapshots.sort(date_compare)
delta = len(snapshots) - keep
for i in range(delta):
    print 'Deleting snapshot ' + snapshots[i].description
    snapshots[i].delete()
