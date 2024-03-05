from django.conf import settings
from rest_framework.exceptions import ValidationError
from .models import ActivityLog, READ, CREATE, UPDATE, DELETE,

class ActivityLogMixin:

    log_message = None

    def _get_action_type(self, request):
        return self.action_type_mapper().get(f"{request.method.upper()}")

    def _build_log_message(self, request):
        return f"User: {self._get_user(request)} / Action Type: {self._get_action_type(request)} / Path: {request.path}"

    def get_log_message(self, request):
        return self.log_message or self._build_log_message(request)

    @staticmethod
    def action_type_mapper():
        return {
            "GET": READ,
            "POST": CREATE,
            "PUT": UPDATE,
            "PATCH": UPDATE,
            "DELETE": DELETE,
        }

    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None

    def _write_log(self, request, response):
        actor = self._get_user(request)
        # no log for unauthenticated user
        if actor and not getattr(settings, "ACTION_DETECTING", False):

            data = {
                "actor": actor,
                "action_type": self._get_action_type(request),
                "remarks": self.get_log_message(request),
            }
            try:
                data["content_type"] = ContentType.objects.get_for_model(
                    self.get_queryset().model
                )
                data["content_object"] = self.get_object()
            except (AttributeError, ValidationError):
                data["content_type"] = None
            except AssertionError:
                pass

            ActivityLog.objects.create(**data)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response
