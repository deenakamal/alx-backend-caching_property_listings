import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    try:
        # Connect to Redis
        redis_conn = get_redis_connection("default")

        # Get Redis INFO stats
        info = redis_conn.info()

        # Extract metrics
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio safely
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        # Log metrics
        logger.info(f"Redis Cache Metrics: {metrics}")

        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis cache metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0}

def get_all_properties():
    
    properties = cache.get("all_properties")

    if not properties:
        
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
      
        cache.set("all_properties", properties, 3600)

    return properties
