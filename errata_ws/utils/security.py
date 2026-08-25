"""
.. module:: security.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Wraps security related functions.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import base64
import binascii
import json
import os

import requests



# GitHub API - credentials.
_GH_API_CREDENTIALS = ('esdoc-system-user', os.getenv('ESDOC_GITHUB_ACCESS_TOKEN'))
_GH_API_HEADERS = {
    'Authorization': 'token {}'.format(os.getenv('ESDOC_GITHUB_ACCESS_TOKEN')),
}

# GitHub API - teams.
_GH_API_TEAMS = "https://api.github.com/teams"

# GitHub API - user.
_GH_API_USER = "https://api.github.com/user"
_GH_API_USERS = "https://api.github.com/users"

# Map of recognized teams and their GitHub identifiers.
_GH_TEAMS = {
    'cdf2cim-publication': 2375689,
    'documentation-publication': 2375693,
    'errata-moderation': 7098570,
    'errata-publication': 2375691,

    'cmip5-bcc': 2567241,
    'cmip5-bnu': 2567242,
    'cmip5-cccma': 2567243,
    'cmip5-cmcc': 2567244,
    'cmip5-cnrm-cerfacs': 2567245,
    'cmip5-csiro': 2567246,
    'cmip5-csiro-bom': 2567247,
    'cmip5-csiro-qccce': 2567248,
    'cmip5-doe-cola-cmmap-gmu': 2567249,
    'cmip5-fio': 2567250,
    'cmip5-ichec': 2567251,
    'cmip5-inm': 2567252,
    'cmip5-ipsl': 2567253,
    'cmip5-lasg-cess': 2567254,
    'cmip5-lasg-iap': 2567255,
    'cmip5-miroc': 2567256,
    'cmip5-mohc': 2567257,
    'cmip5-mpi-m': 2567258,
    'cmip5-mri': 2567259,
    'cmip5-nasa-giss': 2567260,
    'cmip5-nasa-gmao': 2567261,
    'cmip5-ncar': 2567262,
    'cmip5-ncc': 2567263,
    'cmip5-nicam': 2567264,
    'cmip5-nimr-kma': 2567265,
    'cmip5-noaa-gfdl': 2567266,
    'cmip5-nsf-doe-ncar': 2567267,
    'cmip5-unsw': 2567268,

    'cmip6-awi': 2567269,
    'cmip6-bcc': 2567270,
    'cmip6-bnu': 2567271,
    'cmip6-cams': 2567272,
    'cmip6-cas': 2567273,
    'cmip6-cccma': 2567274,
    'cmip6-cccr-iitm': 2567275,
    'cmip6-cmcc': 2567276,
    'cmip6-cnrm-cerfacs': 2567277,
    'cmip6-csir-csiro': 2567278,
    'cmip6-csiro-bom': 2567279,
    'cmip6-csiro': 2942355,
    'cmip6-csiro-arccss': 3532044,
    'cmip6-dwd': 2648414,
    'cmip6-dkrz': 2942354,
    'cmip6-ec-earth-consortium': 2567280,
    'cmip6-e3sm-project': 2942350,
    'cmip6-fio-ronm': 2567281,
    'cmip6-hammoz-consortium': 2567282,
    'cmip6-inm': 2567283,
    'cmip6-inpe': 2567284,
    'cmip6-ipsl': 2567285,
    'cmip6-messy-consortium': 2567286,
    'cmip6-miroc': 2567287,
    'cmip6-mohc': 2567288,
    'cmip6-mpi-m': 2567289,
    'cmip6-mri': 2567290,
    'cmip6-nasa-giss': 2567291,
    'cmip6-ncar': 2567292,
    'cmip6-ncc': 2567293,
    'cmip6-nerc': 2567294,
    'cmip6-nims-kma': 2567295,
    'cmip6-niwa': 2567296,
    'cmip6-noaa-gfdl': 2567297,
    'cmip6-nuist': 2567298,
    'cmip6-pcmdi': 2567299,
    'cmip6-snu': 2567300,
    'cmip6-thu': 2567301,

    'cordex-auth-lhtee': 2567302,
    'cordex-auth-met': 2567303,
    'cordex-awi': 2567304,
    'cordex-bccr': 2567305,
    'cordex-cccma': 2567306,
    'cordex-chmi': 2567307,
    'cordex-clmcom': 2567308,
    'cordex-cnrm': 2567309,
    'cordex-crp-gl': 2567310,
    'cordex-cuni': 2567311,
    'cordex-dhmz': 2567312,
    'cordex-dmi': 2567313,
    'cordex-enea': 2567314,
    'cordex-gerics': 2567315,
    'cordex-hms': 2567316,
    'cordex-ictp': 2567317,
    'cordex-idl': 2567318,
    'cordex-iitm': 2567319,
    'cordex-ipsl-ineris': 2567320,
    'cordex-knmi': 2567321,
    'cordex-mgo': 2567322,
    'cordex-miub': 2567323,
    'cordex-mohc': 2567324,
    'cordex-mpi-csc': 2567325,
    'cordex-nuim': 2567326,
    'cordex-rmib-ugent': 2567327,
    'cordex-smhi': 2567328,
    'cordex-ucan': 2567329,
    'cordex-uclm': 2567330,
    'cordex-uhoh': 2567331,
    'cordex-ulg': 2567332,
    'cordex-uqam': 2567333,


    'cmip6plus-aer': 18322120,
    'cmip6plus-aor': 18322185,
    'cmip6plus-as-rcec': 18322205,
    'cmip6plus-auot': 18322133,
    'cmip6plus-awi': 18322138,
    'cmip6plus-bas': 18322153,
    'cmip6plus-bcc': 18322117,
    'cmip6plus-cams': 18322123,
    'cmip6plus-cas': 18322141,
    'cmip6plus-cccma': 18322169,
    'cmip6plus-cccr-iitm': 18322175,
    'cmip6plus-ceda': 18322196,
    'cmip6plus-cmcc': 18322154,
    'cmip6plus-cnes': 18322161,
    'cmip6plus-cnrm-cerfacs': 18322136,
    'cmip6plus-csiro': 18322212,
    'cmip6plus-csiro-arccss': 18322129,
    'cmip6plus-csiro-cosima': 18322149,
    'cmip6plus-dkrz': 18322140,
    'cmip6plus-dlr-bira': 18322132,
    'cmip6plus-dwd': 18322150,
    'cmip6plus-e3sm-project': 18322134,
    'cmip6plus-eawag': 18322126,
    'cmip6plus-ec-earth-consortium': 18322116,
    'cmip6plus-ecmwf': 18322183,
    'cmip6plus-espri-ipsl': 18322113,
    'cmip6plus-esso': 18322211,
    'cmip6plus-fio-qlnm': 18322190,
    'cmip6plus-fmi': 18322206,
    'cmip6plus-fuberlin': 18322171,
    'cmip6plus-hammoz-consortium': 18322122,
    'cmip6plus-iaceth': 18322173,
    'cmip6plus-iamc': 18322166,
    'cmip6plus-ifm-geomar': 18322142,
    'cmip6plus-imperialcollege': 18322148,
    'cmip6plus-incois-nio-ipsl': 18322204,
    'cmip6plus-inm': 18322157,
    'cmip6plus-ipsl': 18322156,
    'cmip6plus-issi': 18322164,
    'cmip6plus-jaxa': 18322181,
    'cmip6plus-kiost': 18322174,
    'cmip6plus-kit': 18322124,
    'cmip6plus-llnl': 18322200,
    'cmip6plus-lpc2e': 18322170,
    'cmip6plus-messy-consortium': 18322193,
    'cmip6plus-miroc': 18322203,
    'cmip6plus-mohc': 18322115,
    'cmip6plus-mpi-b': 18322180,
    'cmip6plus-mpi-m': 18322165,
    'cmip6plus-mps': 18322159,
    'cmip6plus-mri': 18322131,
    'cmip6plus-nasa-giss': 18322210,
    'cmip6plus-nasa-gsfc': 18322176,
    'cmip6plus-nasa-jpl': 18322186,
    'cmip6plus-nasa-larc': 18322162,
    'cmip6plus-ncar': 18322158,
    'cmip6plus-ncas': 18322168,
    'cmip6plus-ncc': 18322128,
    'cmip6plus-nerc': 18322125,
    'cmip6plus-nims-kma': 18322155,
    'cmip6plus-niwa': 18322207,
    'cmip6plus-noaa-gfdl': 18322143,
    'cmip6plus-noaa-ncei': 18322130,
    'cmip6plus-ntu': 18322119,
    'cmip6plus-nuist': 18322160,
    'cmip6plus-osu': 18322152,
    'cmip6plus-pcmdi': 18322201,
    'cmip6plus-pmod': 18322127,
    'cmip6plus-pnnl-jgcri': 18322198,
    'cmip6plus-pnnl-waccem': 18322184,
    'cmip6plus-rss': 18322146,
    'cmip6plus-rte-rrtmgp-consortium': 18322195,
    'cmip6plus-rubisco': 18322209,
    'cmip6plus-snu': 18322151,
    'cmip6plus-solaris-heppa': 18322139,
    'cmip6plus-thu': 18322163,
    'cmip6plus-ua': 18322137,
    'cmip6plus-ubern': 18322191,
    'cmip6plus-uci': 18322114,
    'cmip6plus-ucolorado': 18322147,
    'cmip6plus-ucsb': 18322213,
    'cmip6plus-ucsd-sio': 18322145,
    'cmip6plus-uhh': 18322121,
    'cmip6plus-uib': 18322208,
    'cmip6plus-uobergen': 18322177,
    'cmip6plus-uofmd': 18322188,
    'cmip6plus-uoleeds': 18322135,
    'cmip6plus-uom': 18322167,
    'cmip6plus-uomontreal': 18322182,
    'cmip6plus-uootago': 18322172,
    'cmip6plus-uooulu': 18322118,
    'cmip6plus-ureading': 18322178,
    'cmip6plus-uw': 18322179,
    'cmip6plus-vua': 18322144,
    'cmip7-awi': 18322096,
    'cmip7-bas': 18322104,
    'cmip7-bnu': 18322093,
    'cmip7-cas': 18322098,
    'cmip7-cccma': 18322108,
    'cmip7-cnrm': 18322097,
    'cmip7-cnrm-cerfacs': 18322095,
    'cmip7-dmi': 18322100,
    'cmip7-dwd': 18322103,
    'cmip7-ec-earth-consortium': 18322089,
    'cmip7-fmi': 18322111,
    'cmip7-ipsl': 18322105,
    'cmip7-kiost': 18322109,
    'cmip7-knmi': 18322110,
    'cmip7-metno': 18322102,
    'cmip7-mohc': 18322088,
    'cmip7-mpi-m': 18322106,
    'cmip7-ncas': 18322107,
    'cmip7-nerc': 18322091,
    'cmip7-noaa-gfdl': 18322099,
    'cmip7-smhi': 18322092,
    'cmip7-sysu': 18322090,
    'cmip7-uaf': 18322094,
    'cmip7-ukncsp': 18322112,
    'cmip7-unsw': 18322101,
    'cordex-auth-lhtee': 2567302,
    'cordex-auth-met': 2567303,
    'cordex-awi': 2567304,
    'cordex-bccr': 2567305,
    'cordex-cccma': 2567306,
    'cordex-chmi': 2567307,
    'cordex-clmcom': 2567308,
    'cordex-cmip6-auth': 18322241,
    'cordex-cmip6-bas': 18322231,
    'cordex-cmip6-bccr-ucan': 18322259,
    'cordex-cmip6-bom': 18322240,
    'cordex-cmip6-cccma': 18322242,
    'cordex-cmip6-cesam-ua': 18322227,
    'cordex-cmip6-clmcom-awi': 18322248,
    'cordex-cmip6-clmcom-btu': 18322230,
    'cordex-cmip6-clmcom-cmcc': 18322244,
    'cordex-cmip6-clmcom-dwd': 18322250,
    'cordex-cmip6-clmcom-eth': 18322257,
    'cordex-cmip6-clmcom-fzj': 18322246,
    'cordex-cmip6-clmcom-gerics': 18322247,
    'cordex-cmip6-clmcom-guf': 18322254,
    'cordex-cmip6-clmcom-hereon': 18322237,
    'cordex-cmip6-clmcom-imwm': 18322261,
    'cordex-cmip6-clmcom-kit': 18322256,
    'cordex-cmip6-clmcom-kul': 18322260,
    'cordex-cmip6-clmcom-list': 18322262,
    'cordex-cmip6-clmcom-wegc': 18322235,
    'cordex-cmip6-cnr-isac': 18322221,
    'cordex-cmip6-cnrm': 18322223,
    'cordex-cmip6-cnrm-mf': 18322225,
    'cordex-cmip6-cornell': 18322219,
    'cordex-cmip6-csiro': 18322268,
    'cordex-cmip6-cyi': 18322226,
    'cordex-cmip6-dwd-bsh': 18322253,
    'cordex-cmip6-enea': 18322251,
    'cordex-cmip6-gerics': 18322238,
    'cordex-cmip6-hclimcom-dmi': 18322217,
    'cordex-cmip6-hclimcom-metno': 18322233,
    'cordex-cmip6-hclimcom-smhi': 18322265,
    'cordex-cmip6-ictp': 18322267,
    'cordex-cmip6-idl-fcul': 18322264,
    'cordex-cmip6-ifca': 18322229,
    'cordex-cmip6-imwm': 18322245,
    'cordex-cmip6-ird-mf': 18322216,
    'cordex-cmip6-ium-fdu': 18322220,
    'cordex-cmip6-knmi': 18322263,
    'cordex-cmip6-mohc': 18322215,
    'cordex-cmip6-ncar': 18322234,
    'cordex-cmip6-nims-kma': 18322232,
    'cordex-cmip6-nkua': 18322224,
    'cordex-cmip6-norce-bccr': 18322228,
    'cordex-cmip6-ouranos': 18322255,
    'cordex-cmip6-rmib-ugent': 18322236,
    'cordex-cmip6-ru-core': 18322218,
    'cordex-cmip6-senamhi-per': 18322214,
    'cordex-cmip6-task-imwm': 18322252,
    'cordex-cmip6-uba-cima-ifaeci': 18322266,
    'cordex-cmip6-unsw-ccrc': 18322243,
    'cordex-cmip6-uq-dec': 18322222,
    'cordex-cmip6-uu-imau': 18322239,
}

# Request authentication error HTTP response code.
_HTTP_UNAUTHENTICATED_ERROR = 401

# Request authorization error HTTP response code.
_HTTP_UNAUTHORIZED_ERROR = 403


class AuthenticationError(Exception):
    """Raised when an authentication assertion fails.

    """
    def __init__(self, msg=None):
        """Instance constructor.

        """
        err = "AUTHENTICATION FAILED"
        if msg is not None:
           err = "{} : {}".format(err, msg) 
        super(AuthenticationError, self).__init__(err)
        self.response_code = _HTTP_UNAUTHENTICATED_ERROR


class AuthorizationError(Exception):
    """Raised when an authorization assertion fails.

    """
    def __init__(self, msg=None):
        """Instance constructor.

        """
        err = "AUTHORIZATION FAILED"
        if msg is not None:
           err = "{} : {}".format(err, msg) 
        super(AuthorizationError, self).__init__(err)
        self.response_code = _HTTP_UNAUTHORIZED_ERROR


def authenticate_user(credentials):
    """Authenticates user credentials request against GitHub user api.

    :param tuple credentials: 2 member tuple (GitHub username, GitHub access token)

    :returns: GitHub username
    :rtype: str

    """
    # Unpack credentials.
    user_id, _ = credentials

    # Invoke GitHub API.
    r = requests.get(_GH_API_USER, auth=credentials)

    # Assert access token is valid (status_code = 200).
    if r.status_code != 200:
        raise AuthenticationError("GitHub user authentication with access token failed")

    # Assert user has granted application read:org permissions.
    if 'admin:org' not in r.headers['X-OAuth-Scopes'] and \
       'read:org' not in r.headers['X-OAuth-Scopes']:
        raise AuthenticationError("Access token must have either admin:org or read:org scope enabled")

    # Assert user id matches access token.
    if json.loads(r.text)['login'] != user_id:
        raise AuthenticationError("Github User ID is not matched with access token")

    return user_id


def authorize_user(team_id, user_id):
    """Verifies a user is a member of a team.

    :param str team_id: GitHub team identifier.
    :param str user_id: GitHub user login.

    """
    # Validate inputs.
    assert team_id in _GH_TEAMS, "Invalid team identifier {}".format(team_id)

    # Invoke GitHub API.
    url = '{}/{}/memberships/{}'.format(_GH_API_TEAMS, _GH_TEAMS[team_id], user_id)
    r = requests.get(url, headers=_GH_API_HEADERS)

    # Assert user is a team member.
    if r.status_code != 200:
        raise AuthorizationError()


def get_team_members(team_id):
    """Returns GitHub logins of all members of a team.

    :param str team_id: GitHub team identifier.
    :returns: List of GitHub usernames.
    :rtype: list[str]
    """
    assert team_id in _GH_TEAMS, "Invalid team identifier {}".format(team_id)

    url = '{}/{}/members'.format(
        _GH_API_TEAMS,
        _GH_TEAMS[team_id],
    )

    r = requests.get(url, headers=_GH_API_HEADERS)

    if r.status_code != 200:
        raise AuthorizationError(
            "Unable to retrieve GitHub team members"
        )

    return [member['login'] for member in r.json()]


def strip_credentials(credentials):
    """Strips and decodes HTTP Basic authentication credentials.

    Accepts either:
        - str (Authorization header value)
        - bytes (raw header value)

    Expected format after decoding:
        "username:password" (Base64-encoded)

    :param credentials: Base64 encoded HTTP Basic credentials.
    :type credentials: str | bytes

    :returns: (username, password)
    :rtype: tuple[str, str]

    :raises AuthenticationError: If decoding or parsing fails.
    """

    # Normalize to string first
    if isinstance(credentials, bytes):
        credentials = credentials.decode("utf-8")

    # Remove "Basic " prefix if present
    credentials = credentials.replace("Basic ", "")

    try:
        # Base64 decode -> bytes
        decoded = base64.b64decode(credentials)
    except (TypeError, binascii.Error):
        raise AuthenticationError()

    try:
        # Convert to string and split
        decoded = decoded.decode("utf-8")
        username, password = decoded.split(":", 1)
    except ValueError:
        raise AuthenticationError()

    return username, password
