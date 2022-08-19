Start and Step
======================

This shows a few alternative ways to run couplings. These modes are very useful for testing new plays or debugging.


.. _start_at_task:

Start-at-task
`````````````
If you want to start executing your coupling at a particular task, you can do so with the ``--start-at-task`` option::

    quantum-coupling coupling.yml --start-at-task="install packages"

The above will start executing your coupling at a task named "install packages".


.. _step:

Step
````

Playbooks can also be executed interactively with ``--step``::

    quantum-coupling coupling.yml --step

This will cause quantum to stop on each task, and ask if it should execute that task.
Say you had a task called "configure ssh", the coupling run will stop and ask::

    Perform task: configure ssh (y/n/c):

Answering "y" will execute the task, answering "n" will skip the task, and answering "c"
will continue executing all the remaining tasks without asking.

