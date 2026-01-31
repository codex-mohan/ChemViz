"""
API Client for Django Backend Communication
"""
import requests
from typing import Optional, Dict, Any, List


class ApiClient:
    """HTTP client for communicating with Django REST API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.user_id: Optional[int] = None
        self.username: Optional[str] = None
        self.token: Optional[str] = None # Added token storage
    
    def _url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        return f"{self.base_url}/{endpoint.lstrip('/')}"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with auth token if logged in"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Process API response and handle errors"""
        try:
            data = response.json()
        except ValueError:
            data = {"error": "Invalid response from server"}
        
        if not response.ok:
            error_msg = data.get("error", f"Request failed with status {response.status_code}")
            if isinstance(error_msg, dict) or isinstance(error_msg, list):
                error_msg = str(error_msg)
            raise ApiError(error_msg, response.status_code)
        
        return data
    
    # ============ Authentication ============
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and store session info"""
        response = self.session.post(
            self._url("login/"),
            json={"username": username, "password": password}
        )
        data = self._handle_response(response)
        self.user_id = data.get("user_id")
        self.username = data.get("username")
        self.token = data.get("token") # Store token
        return data
    
    def register(self, username: str, password: str, email: str = "") -> Dict[str, Any]:
        """Register new user account"""
        response = self.session.post(
            self._url("register/"),
            json={"username": username, "password": password, "email": email}
        )
        data = self._handle_response(response)
        # Auto login after register
        if "token" in data:
            self.user_id = data.get("user_id")
            self.token = data.get("token") # Store token
            self.username = username
        return data
    
    def logout(self):
        """Clear session data"""
        self.user_id = None
        self.username = None
        self.token = None
        self.session = requests.Session()
    
    @property
    def is_logged_in(self) -> bool:
        return self.token is not None # Check token instead of user_id
    
    # ============ Dataset Operations ============
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """Upload CSV file to backend"""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('\\')[-1].split('/')[-1], f, 'text/csv')}
            response = self.session.post(self._url("upload/"), files=files, headers=self._get_headers())
        return self._handle_response(response)
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """Get list of all datasets"""
        response = self.session.get(self._url("datasets/"), headers=self._get_headers())
        return self._handle_response(response)
    
    def get_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Get single dataset details"""
        response = self.session.get(self._url(f"datasets/{dataset_id}/"), headers=self._get_headers())
        return self._handle_response(response)
    
    def get_equipment(self, dataset_id: int) -> List[Dict[str, Any]]:
        """Get equipment list for a dataset"""
        response = self.session.get(self._url(f"datasets/{dataset_id}/equipment/"), headers=self._get_headers())
        return self._handle_response(response)
    
    def get_summary(self, dataset_id: int) -> Dict[str, Any]:
        """Get summary statistics for a dataset"""
        response = self.session.get(self._url(f"datasets/{dataset_id}/summary/"), headers=self._get_headers())
        return self._handle_response(response)
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get last 5 uploaded datasets"""
        response = self.session.get(self._url("history/"), headers=self._get_headers())
        return self._handle_response(response)
    
    def download_report(self, dataset_id: int) -> bytes:
        """Download PDF report for dataset"""
        response = self.session.get(self._url(f"datasets/{dataset_id}/report/"), headers=self._get_headers())
        if not response.ok:
            raise ApiError(f"Failed to download report: {response.status_code}", response.status_code)
        return response.content


class ApiError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


# Global API client instance
api_client = ApiClient()
