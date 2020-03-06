"""
Celery example
"""
#TODO - delete this file in future # pylint: disable=fixme

import time

from app import CELERY


def call_task():
    """
    Example.
    Publish 2 messages. (Tasks info are inside messages)
    """
    reverse_result = example_reverse.apply_async(args=["TASK REVERSE"], queue="reverse_queue")
    add_result = example_add.apply_async(args=[1, 2], queue="add_queue")
    print(f'{reverse_result=}')
    print(f'{add_result=}')

    return 'Hello, World!'


#@CELERY.task(bind=True) # bind - to access self (Task object)
@CELERY.task(bind=True, name='ngfg.app.celery_tasks.example.example_reverse')
def example_reverse(self, string):
    """
    Example task - reverse string
    """
    print(f'Task reverse started, {self=}')
    time.sleep(5)
    print('Task slept')
    return string[::-1]

#@CELERY.task(bind=True, name='імя', auto_retry=[HTTPException], max_retries=3)
@CELERY.task(bind=True, name='ngfg.app.celery_tasks.example.example_add')
def example_add(self, val1, val2):
    """
    Example task - add 2 values
    """
    print(f'Task add started, {self=}')
    return val1 + val2
