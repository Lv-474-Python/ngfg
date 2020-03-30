import mock
from app.helper.redis_manager import RedisManager


@mock.patch('app.REDIS.delete')
def test_redis_delete(redis_mock):
    redis_mock.return_value = 0
    redis_delete = RedisManager.delete('form_fields:')
    assert redis_delete == 0
