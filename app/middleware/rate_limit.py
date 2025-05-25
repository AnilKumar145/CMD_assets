import time
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from collections import defaultdict

logger = logging.getLogger("assets-service")

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute=60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Clean up old requests
        current_time = time.time()
        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip] 
            if current_time - timestamp < 60
        ]
        
        # Check if rate limit exceeded
        if len(self.request_counts[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return Response(
                content='{"detail":"Rate limit exceeded. Please try again later."}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json"
            )
        
        # Add current request timestamp
        self.request_counts[client_ip].append(current_time)
        
        # Process the request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self.requests_per_minute - len(self.request_counts[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + 60))
        
        return response