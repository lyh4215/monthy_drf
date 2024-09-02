import logging

logger = logging.getLogger('django.request')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 요청 정보를 로깅
        logger.info(
            f"[{request.method}] {request.path}"
        )
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # 에러 발생 시 요청 정보를 로깅
        logger.error(
            f"Exception occurred: {exception}\n"
            f"[{request.method}] {request.path} {request.body.decode('utf-8', errors='replace')}"
        )