"""
Celery configuration
"""

from celery import Celery


def make_celery(app):
    """
    Seting up celery for flask application
    - creates a new Celery object, configures it with the broker from the application config
    - updates the rest of the Celery config from the Flask config

    :param app: Flask object (flask application)
    :return: Celery object
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """
        Subclass of the task that wraps the task execution in an application context
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
