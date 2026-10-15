import time
import requests
from config.settings import settings
from models.request_models import AssetTemplateRequest
from typing import Optional
import requests

class AssetTemplateClient:
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.session.headers.update(settings.DEFAULT_HEADERS)

    def _parse_response_json(self, response: requests.Response, endpoint: str) -> dict:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(f"'{endpoint}' returned HTTP {response.status_code}: {response.text}") from exc
        
        try:
            return response.json()
        except ValueError as exc:
            raise ValueError(f"'{endpoint}' returned invalid JSON") from exc

    def check_health(self) -> dict:
        response = self.session.get(settings.HEALTH_URL, timeout=settings.REQUEST_TIMEOUT_SECONDS)
        health_data = self._parse_response_json(response, settings.HEALTH_URL)
        if not isinstance(health_data, dict) or health_data.get("status") != "ok":
            raise ValueError("The API health response was invalid or not ready")
        return health_data

    def generate_asset_template(self, request_data: AssetTemplateRequest) -> dict:
        # 1. Health check
        self.check_health()

        # 2. Submit job
        response = self.session.post(
            settings.SUBMIT_URL,
            json=request_data.to_payload(),
            timeout=settings.REQUEST_TIMEOUT_SECONDS
        )
        submission = self._parse_response_json(response, settings.SUBMIT_URL)
        
        if not isinstance(submission, dict) or not submission.get("job_id"):
            raise ValueError("The API submission response did not contain a job_id")
        
        job_id = submission["job_id"]
        status_url = f"{settings.SUBMIT_URL}/{job_id}"
        deadline = time.monotonic() + settings.REQUEST_TIMEOUT_SECONDS

        # 3. Polling loop
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"Template generation exceeded {settings.REQUEST_TIMEOUT_SECONDS} seconds; job_id='{job_id}'")

            resp_status = self.session.get(
                status_url,
                timeout=min(settings.REQUEST_TIMEOUT_SECONDS, remaining)
            )
            status_data = self._parse_response_json(resp_status, status_url)

            if not isinstance(status_data, dict):
                raise ValueError("The API status response was not a JSON object")

            status = status_data.get("status")
            if status == "completed":
                result = status_data.get("result")
                if not isinstance(result, dict):
                    raise ValueError("The completed job did not contain a template object")
                return result
            
            if status in ("failed", "error"):
                raise RuntimeError(f"Template generation status: {status_data.get('errors') or 'no error details'}")
            
            if status not in ("queued", "processing"):
                raise ValueError(f"Unexpected generation status: '{status}'")

            time.sleep(min(settings.POLL_INTERVAL_SECONDS, max(0, deadline - time.monotonic())))