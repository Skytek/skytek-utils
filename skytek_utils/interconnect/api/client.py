import requests
from django.conf import settings

from .jwt import generate_jwt


class Client:
    def __init__(self, remote_module: str) -> None:
        self.remote_module = remote_module

    def _get_host(self):
        environment_domain = settings.INTERCONNECT_ENVIRONMENT_DOMAIN
        return f"{self.remote_module}.{environment_domain}"

    def _make_url(self, path: str):
        host = self._get_host()
        protocol = (
            "https" if getattr(settings, "INTERCONNECT_USE_SSL", True) else "http"
        )
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{protocol}://{host}{path}"

    def _call_api(self, method, path, *args, **kwargs):
        method_function = getattr(requests, method)
        url = self._make_url(path)
        headers = {
            **kwargs.pop("headers", {}),
            **self._make_headers(),
        }
        result = method_function(
            url,
            *args,
            headers=headers,
            **kwargs,
        )
        return result

    def _make_headers(self):
        jwt = generate_jwt()
        headers = {
            "Authorization": f"Bearer {jwt}",
        }
        return headers

    def get(self, path, *args, **kwargs):
        return self._call_api("get", path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self._call_api("post", path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self._call_api("patch", path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self._call_api("delete", path, *args, **kwargs)