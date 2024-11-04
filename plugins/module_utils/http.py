# Copyright 2024, Itential Inc. All Rights Reserved

# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import urllib3
import traceback
import functools

import urllib.parse

from dataclasses import dataclass, field

from ansible.errors import AnsibleError

from ansible_collections.itential.core.plugins.module_utils import display

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    raise AnsibleError("missing required library: requests")


def send_request(method, url, headers=None, data=None, params=None, auth=None, timeout=None,
                certificate_file=None, private_key_file=None, verify=None, disable_warnings=None,
                session=None) -> requests.Response:
    """ Send the request to the host and return the response

    This function sends the request to the host and waits for the
    response.  The raw response object is returned to the calling
    function.

    Args:
        method (str): The HTTP method for the request
        url (str): The full HTTP URL to send the request to
        headers (dict): A dictionary that contains any headers to include
            in the request
        data (bytes): A byte array to include in the body of the HTTP
            API request
        params (dict): A dictionary that cotains one or more values used
            to construct a query string to include with the request
        auth (typing.Any): A `requests` auth object
        timeout (int): Configures the timeout for waiting for a response
            from the remote API
        verify (bool): Enable or disable certificate validation
        disable_warnings (bool): Enable or disable `urllib3` warnings
        session (requests.Session): A `requests.Session` object

    Returns
        A `Response` object that contains the response from the API call
    """
    display.trace("http.send_request")

    if disable_warnings is True:
        urllib3.disable_warnings()

    kwargs = {
        "method": method,
        "url": url,
        "headers": headers,
        "data": data,
        "params": params,
        "verify": verify,
    }

    if auth is not None:
        kwargs["auth"] = auth

    if timeout is not None:
        kwargs["timeout"] = timeout

    if certificate_file is not None and private_key_file is not None:
        kwargs["cert"] = (certificate_file, private_key_file)

    if isinstance(kwargs.get("data"), (dict, list)):
        kwargs["data"] = json.dumps(data)

    display.vvvvv(f"Request object: {kwargs}")

    try:
        if session is not None:
            resp = session.request(**kwargs)
        else:
            resp = requests.request(**kwargs)

        display.vvv(f"HTTP response is {resp.status_code} {resp.reason}")
        display.vvvvv(f"Start of response body\n{resp.text}\nEnd of response body")
        display.vvvvv(f"Call completed in {resp.elapsed}")

    except requests.exceptions.ConnectionError as exc:
        display.vvvvv(traceback.format_exc())
        raise AnsibleError(f"Failed to establish a connection to {url}")

    except Exception as exc:
        display.vvvvv(traceback.format_exc())
        raise AnsibleError(str(exc))

    return resp


get = functools.partial(send_request, "GET")
post = functools.partial(send_request, "POST")
put = functools.partial(send_request, "PUT")
delete = functools.partial(send_request, "DELETE")
patch = functools.partial(send_request, "PATCH")


def make_url(host, path, port=0, use_tls=True) -> str:
    """ Join parts of the request to construct a valid URL

    This function will take the request object and join the
    individual parts together to cnstruct a full URL.

    Args:
        host (str): The hostname or IP address of the API endpoint
        port (int): The port used to connect to the API
        path (str): The URI path of the endpoint
        use_tls (bool): Enable or disable TLS support

    Returns:
        A string that represents the full URL
    """
    display.trace("http.make_url")

    if port == 0:
        port = 443 if use_tls is True else 80

    if port not in (None, 80, 443):
        host = f"{host}:{port}"

    if path[0] == "/":
        path = path[1:]

    proto = "https" if use_tls else "http"

    return urllib.parse.urlunsplit((proto, host, path, None, None))


def basic_auth(username, password) -> HTTPBasicAuth:
    """Constructs a basic authentication object

    This function accepts a `username` and `password` argument
    and will construct a basic authentication object that can
    be used to in a request.

    Args:
        username (str): The username to use when authenticating
        password (str): The password to use when authenticating

    Returns:
        A `requests.HTTPBasicAuth` object
    """
    display.trace("http.basic_auth")
    return HTTPBasicAuth(username, password)


@dataclass
class Response(object):
    """ Response respresents a response from an HTTP request

    The Response object provides access to the response from
    a HTTP request that includes the body of the response, response
    status and header information.

    Args:
        headers (dict): Set of key/value pairs returned from the API call

        body (bytes): The body of the response

        status_code (int): The HTTP status code in the response

        status (str):  The HTTP status text in the response
    """
    headers: dict
    body: bytes
    status_code: int
    status: str


@dataclass
class Request(object):
    """Request represents an HTTP request

    The Request object represents an HTTP request to be sent
    to an API endpoint.  The Request object is used to create
    and send an API call.

    Args:
        host (str): The hostname or IP address of the API endpoint

        port (int): The port used to connect to the API endpoint.  If
            the value of the port is 0, it will automatically be
            determined based on the `use_tls`

        method (str): The HTTP method to invoke.  Valid values include
            `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

        path (str): The URI to send the request to.  The URI will be
            combined with the `host` and `port` to construct the full
            URL to send the request to.

        body (bytes): The body of the HTTP request.

        headers (dict): The HTTP headers to set in the API request

        use_tls (bool): Enable or disable the use of TLS when sending
            the request to the API

        disable_warnings (bool): Enable or disable Python warnings
            generated by urllib3

        verify (bool): Enable or disable certificate validation when
            connecting to the API host.

    """
    host: str
    port: int = 0
    method: str = "GET"
    path: str = None
    body: bytes = None
    headers: dict = field(default_factory=dict)
    use_tls: bool = True
    disable_warnings: bool = True
    verify: bool = True


class Session(object):
    """Session maintains an HTTP session with an API endpoint

    The Session object holds the HTTP session with an API endpoint
    include all session state such as authentication tokens,
    cookies and more.

    Args:
        name (str): The name of the session
        session (requests.Session): The requests library session.
    """
    def __init__(self, name):
        display.trace("http.Session.init")
        self.name = name
        self.session = requests.Session()

    def send(self, request) -> Response:
        """Send will send the request to the API endpoint and return the response

        Args:
            request (Request): A `Request` object used to construct the HTTP
                API call

        Returns:
            A `Response` object
        """
        display.trace("http.Session.send")

        url = make_url(
            request.host,
            request.path,
            request.port,
            request.use_tls,
        )

        resp = send_request(
            method=request.method,
            url=url,
            headers=request.headers,
            data=request.body,
            verify=request.verify,
            disable_warnings=request.disable_warnings,
            session=self.session
        )

        return Response(
            status_code=resp.status_code,
            status=resp.reason,
            headers=resp.headers,
            body=resp.text
        )
