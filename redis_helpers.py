import redis
from bot import DEFAULT_AUDIO_OUTPUT_FORMAT

#TODO: namespace by user_id and chat_id 
#TODO: put these in seperate file and import them
def get_output_for_user(user_id: int, cache: redis.Redis) -> str:
    redis_key = f"{user_id}_output_format_pref"
    result = cache.get(redis_key)
    if result is None:
        return DEFAULT_AUDIO_OUTPUT_FORMAT
    return result.decode('utf-8')

#TODO: return code to say if it was succesful
def set_output_for_user(user_id: int, output_format: str, cache: redis.Redis) -> None:
    redis_key = f"{user_id}_output_format_pref"
    cache.set(redis_key,output_format)
    return None