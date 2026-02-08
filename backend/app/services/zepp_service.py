import json
import logging
import re
from typing import Optional, Dict, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class ZeppService:
    def __init__(self, timeout: int = 10):
        self.headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)'
        }
        self.login_token = None
        self.app_token = None
        self.user_id = None
        self.timeout = timeout
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST"),
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def login(self, phone: str, password: str) -> bool:
        """Authenticate with Zepp API"""
        try:
            # Step 1: Get access code
            url1 = f"https://api-user.huami.com/registrations/+86{phone}/tokens"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2"
            }
            data1 = {
                "client_id": "HuaMi",
                "password": password,
                "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
                "token": "access"
            }

            r1 = self.session.post(
                url1,
                data=data1,
                headers=headers,
                allow_redirects=False,
                timeout=self.timeout,
            )
            if r1.status_code != 302:
                return False

            location = r1.headers["Location"]
            code_pattern = re.compile(r"(?<=access=).*?(?=&)")
            code = code_pattern.findall(location)[0]

            # Step 2: Get login token
            url2 = "https://account.huami.com/v2/client/login"
            data2 = {
                "app_name": "com.xiaomi.hm.health",
                "app_version": "4.6.0",
                "code": code,
                "country_code": "CN",
                "device_id": "2C8B4939-0CCD-4E94-8CBA-CB8EA6E613A1",
                "device_model": "phone",
                "grant_type": "access_token",
                "third_name": "huami_phone",
            }

            r2_response = self.session.post(url2, data=data2, headers=headers, timeout=self.timeout)
            r2_response.raise_for_status()
            r2 = r2_response.json()
            if 'token_info' not in r2:
                return False

            self.login_token = r2["token_info"]["login_token"]
            self.user_id = r2["token_info"]["user_id"]

            # Step 3: Get app token
            self.app_token = self._get_app_token()
            return True

        except Exception as exc:
            logger.exception("Zepp login error: %s", exc)
            return False

    def _get_app_token(self) -> Optional[str]:
        """Get app token for API access"""
        try:
            url = f"https://account-cn.huami.com/v1/client/app_tokens?app_name=com.xiaomi.hm.health&dn=api-user.huami.com%2Capi-mifit.huami.com%2Capp-analytics.huami.com&login_token={self.login_token}&os_version=4.1.0"
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
            return payload['token_info']['app_token']
        except Exception as exc:
            logger.exception("Error getting app token: %s", exc)
            return None

    def get_latest_health_data(self) -> Optional[Dict[str, Any]]:
        """Fetch latest health data from Zepp"""
        if not self.app_token or not self.user_id:
            return None

        try:
            # Get current timestamp
            time_url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
            time_response = self.session.get(time_url, headers=self.headers, timeout=self.timeout)
            time_response.raise_for_status()
            time_payload = time_response.json()
            t = time_payload['data']['t']

            # Request today's data
            import time as time_module
            today = time_module.strftime("%F")

            url = f'https://api-mifit-cn.huami.com/v1/data/band_data.json?&t={t}'
            head = {
                "apptoken": self.app_token,
                "Content-Type": "application/x-www-form-urlencoded"
            }

            # Request data for today
            data = f'userid={self.user_id}&last_sync_data_time=0&device_type=0&last_deviceid=DA932FFFFE8816E7&data_len=1'

            response = self.session.post(url, data=data, headers=head, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()

            if 'data' in payload and payload['data']:
                # Parse the response to extract health metrics
                return self._parse_health_data(payload['data'][0])
            else:
                logger.warning("No data found in Zepp response")
                return None

        except Exception as exc:
            logger.exception("Error fetching Zepp data: %s", exc)
            return None

    def _parse_health_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Zepp API response into health metrics"""
        try:
            summary = data.get('summary', '{}')
            if isinstance(summary, str):
                summary = json.loads(summary)

            # Extract step data
            steps_data = summary.get('stp', {})
            total_steps = steps_data.get('ttl', 0)
            calories = steps_data.get('cal', 0)

            # For demo purposes, we'll create a basic health entry
            # In a real implementation, you'd parse more detailed data
            return {
                'calories_burned': float(calories),
                'exercise_minutes': 0,  # Would need to parse activity data
                'stand_hours': 0,       # Would need to parse stand data
                'resting_heart_rate': None,  # Would need heart rate data
                'respiratory_rate': None,    # Would need respiratory data
                'sleep_duration': None,      # Would need sleep data
                'sleep_quality': None,       # Would need sleep data
                'sleep_stages': None,        # Would need sleep stages data
            }

        except Exception as exc:
            logger.exception("Error parsing health data: %s", exc)
            return None

# Global service instance
zepp_service = ZeppService()
