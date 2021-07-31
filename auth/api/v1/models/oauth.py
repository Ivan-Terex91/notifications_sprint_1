from api import api
from core.enums import OAuthProvider
from flask_restx import fields

OAuthAccountModel = api.model(
    "OAuthAccountModel",
    {
        "provider": fields.String(enum=[provider.value for provider in OAuthProvider]),
        "exp": fields.DateTime(),
    },
)
