from redis.asyncio import Redis
from app.config import DatabaseSettings

_token_blacklist =Redis(
    host=DatabaseSettings().REDIS_HOST,
    port=DatabaseSettings().REDIS_PORT,
    db=0,
)

async def add_jti_to_blacklist(jti: str, expiration_seconds: int = 86400):
    """Add a token to the Redis blacklist with an expiration time.
    
    Args:
        jti: The JWT ID to blacklist
        expiration_seconds: Time in seconds until the blacklist entry expires (default: 24 hours)
    """
    await _token_blacklist.setex(jti, expiration_seconds, "blacklisted")
    

async def is_jti_blacklisted(jti: str) -> bool:
    """Check if a token is blacklisted."""
    return await _token_blacklist.exists(jti)