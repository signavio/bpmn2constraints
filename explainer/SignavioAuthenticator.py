import requests


class SignavioAuthenticator:
    def __init__(self, system_instance, tenant_id, email, pw):
        self.system_instance = system_instance
        self.tenant_id = tenant_id
        self.email = email
        self.pw = pw

    """
    Takes care of authentication against Signavio systems
    """

    def authenticate(self):
        """
        Authenticates user at Signavio system instance and initiates session.
        Returns:
            dictionary: Session information
        """
        login_url = self.system_instance + "/p/login"
        data = {"name": self.email, "password": self.pw, "tokenonly": "true"}
        if "tenant_id" in locals():
            data["tenant"] = self.tenant_id
        # authenticate
        login_request = requests.post(login_url, data)

        # retrieve token and session ID
        auth_token = login_request.content.decode("utf-8")
        jsesssion_ID = login_request.cookies["JSESSIONID"]

        # The cookie is named 'LBROUTEID' for base_url 'editor.signavio.com'
        # and 'editor.signavio.com', and 'AWSELB' for base_url
        # 'app-au.signavio.com' and 'app-us.signavio.com'
        lb_route_ID = login_request.cookies["LBROUTEID"]

        # return credentials
        return {
            "jsesssion_ID": jsesssion_ID,
            "lb_route_ID": lb_route_ID,
            "auth_token": auth_token,
        }
