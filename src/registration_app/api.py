"""API endpoints of the app."""

import json

from gnu_cauldron_reg.app import app
from gnu_cauldron_reg.service.acm import can_apply_acm_membership_discount
from gnu_cauldron_reg.service.participant import can_apply_ieee_membership

from bottle import request


@app.post("/api/v1/verify-acm")
def verify_acm_membership():
    try:
        json_body = json.loads(request.body.read(1024).decode("UTF-8"))
    except json.JSONDecodeError:
        return "Request data is not valid", 400
    return json.dumps(
        can_apply_acm_membership_discount(
            json_body["acmMembershipNumber"],
            json_body["email"],
        ),
    )


@app.post("/api/v1/verify-ieee")
def verify_ieee_membership():
    try:
        json_body = json.loads(request.body.read(1024).decode("UTF-8"))
    except json.JSONDecodeError:
        return "Request data is not valid", 400
    return json.dumps(
        can_apply_ieee_membership(
            json_body["ieeeMembershipNumber"],
            json_body["email"],
        )
    )
