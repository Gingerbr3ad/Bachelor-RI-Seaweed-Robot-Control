import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/admin/RI-Seaweed/ri_seaweed_ws/install/gripper'
