import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("assets-service")

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Add request ID to logger context
        logger_adapter = logging.LoggerAdapter(
            logger, 
            {"request_id": request_id}
        )
        
        start_time = time.time()
        
        # Log request details
        logger_adapter.info(
            f"Request started: {request.method} {request.url.path}"
        )
        
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            
            # Log response details
            logger_adapter.info(
                f"Request completed: {request.method} {request.url.path} "
                f"- Status: {response.status_code} - Time: {process_time:.4f}s"
            )
            
            return response
            
        except Exception as e:
            # Log exception
            process_time = time.time() - start_time
            logger_adapter.error(
                f"Request failed: {request.method} {request.url.path} "
                f"- Error: {str(e)} - Time: {process_time:.4f}s",
                exc_info=True
            )
            raise