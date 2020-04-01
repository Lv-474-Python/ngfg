import mock

from app.celery_tasks.example import call_task, example_reverse, example_add


@mock.patch('app.celery_tasks.example.example_add')
@mock.patch('app.celery_tasks.example.example_reverse')
def test_call_task(example_reverse_mock, example_add_mock):
    example_reverse_mock.return_value = 1
    example_add_mock.return_value = 1

    test_instance = call_task()

    assert test_instance == 'Hello, World!'


def test_example_add():
    test_instance = example_add('val1', 'val2')

    assert test_instance == 'val1val2'


def test_example_reverse():
    test_instance = example_reverse('string')

    assert test_instance == 'gnirts'
