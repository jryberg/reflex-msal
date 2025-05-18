from typing import List, Optional
import msal
import reflex as rx
from decouple import config
from .base import State

client_id: str = config("AZURE_CLIENT_ID", cast=str)
client_secret: str = config("AZURE_CLIENT_SECRET", cast=str)
tenant_id: str = config("AZURE_TENANT_ID", cast=str)
authority = f"https://login.microsoftonline.com/{tenant_id}"
login_redirect = "/authenticated"
cache = msal.TokenCache()

sso_app = msal.ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority,
    token_cache=cache,
)


class Auth(State):
    _access_token: str = ""
    _flow: dict

    def redirect_sso(self, scope: Optional[List] = None) -> rx.Component:
        if scope is None:
            scope = []
        self._flow = sso_app.initiate_auth_code_flow(
            scopes=scope,
            redirect_uri=f"{self.router.page.host}/callback",
        )
        return rx.redirect(self._flow["auth_uri"])

    def require_auth(self):
        if not self._token:
            return self.redirect_sso()

    @rx.var(cache=False)
    def check_auth(self) -> bool:
        return True if self._token else False

    @rx.var(cache=True)
    def token(self) -> dict:
        return self._token

    def logout(self):
        self._token = {}
        return rx.redirect(authority + "/oauth2/v2.0/logout")

    def callback(self):
        query_components = self.router.page.params
        print("query_components", query_components)
        print("Raw path", self.router.page.raw_path)
        auth_response = {
            "code": query_components.get("code"),
            "client_info": query_components.get("client_info"),
            "state": query_components.get("state"),
            "session_state": query_components.get("session_state"),
            "client-secret": client_secret,
        }
        try:
            result = sso_app.acquire_token_by_auth_code_flow(
                self._flow, auth_response, scopes=[]
            )
        except Exception as e:
            print("ops", e)
            #return rx.toast(f"error something went wrong")
            return self.redirect_sso()
        # this can be used for accessing graph
        self._access_token = result.get("access_token")
        self._token = result.get("id_token_claims", {})
        return rx.redirect(login_redirect)

