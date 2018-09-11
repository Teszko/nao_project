
API
===

This document contains automatically generated api docs.

---------------
Class reference
---------------

agent.py
--------
.. autoclass:: misc.agent.Sense
   :members:
.. autoclass:: misc.agent.Think
   :members:
.. autoclass:: misc.agent.Act
   :members:

commandqueue.py
---------------
.. autoclass:: misc.commandqueue.QueueElement
   :members:
.. autoclass:: misc.commandqueue.CommandQueue
   :members:

commands.py
-----------
.. autofunction:: misc.commands.init_scan
.. autofunction:: misc.commands.scan_view_step
.. autofunction:: misc.commands.scan_front
.. autofunction:: misc.commands.look_straight
.. autofunction:: misc.commands.pose_ready
.. autofunction:: misc.commands.go_to

recognizer.py
-------------
.. autoclass:: misc.recognizer.Recognizer
   :members:

robot.py
--------
.. autoclass:: misc.robot.Robot
   :members:

states.py
---------
.. autoclass:: misc.states.StateMachine
   :members:
.. autofunction:: misc.states.state_wait_fn
.. autofunction:: misc.states.state_done_fn
.. autofunction:: misc.states.state_search_fn

vision.py
---------
.. autofunction:: misc.vision.detect_blob
.. autofunction:: misc.vision.get_blob_center
.. autofunction:: misc.vision.get_distance
