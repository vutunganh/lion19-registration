"""Service for payment gate."""

import base64
import logging
import urllib.parse

from registration_app.app import app

import gpwebpay.config as gpwebpay_config
from gpwebpay import gpwebpay
from gpwebpay.config import configuration as GPWebpayConfig

logger = logging.getLogger(__name__)


class PaymentGateException(RuntimeError):
    """Raised if any issue with the payment gate processing occurs."""


class PaymentUnsuccessfulException(RuntimeError):
    """Raised if the payment was not successful for some reason."""

    def __init__(self, err_msg: str) -> None:
        """Initializes this exception.

        Args:
            err_msg: Error message that should be displayed to the user!
        """
        super().__init__(err_msg)
        self.err_msg = err_msg


# Inspired by:
#   https://github.com/filias/gpwebpay_demoshop/blob/master/app.py#L32
#   https://github.com/filias/gpwebpay
def request_payment(order_num: int, payment_amount: int) -> str:
    """Requests a payment.

    Args:
        order_num: ID of the order to be created. Should be unique.
        payment_amount: Payment amount. Specified in the smallest unit of a currency.
            E.g. halers in Czech crowns, cents in Euros, etc.
    Returns:
        Payment link for the new order.
    Raises:
        PaymentGateException: In case of any issues when communicating with the payment
            gate.
    """
    gw = gpwebpay.GpwebpayClient()
    key_bytes = base64.b64decode(GPWebpayConfig.GPWEBPAY_MERCHANT_PRIVATE_KEY)
    try:
        resp = gw.request_payment(str(order_num), payment_amount, key_bytes)
    except Exception as e:
        raise PaymentGateException from e
    if not resp.ok:
        logger.error(
            f"Could not create a payment link for '{order_num}'."
            f" Code: '{resp.status_code}'."
            f" Reason: '{resp.reason}'."
            f" URL: '{resp.url}'."
            f" Content: '{resp.content}.'"
        )
        raise PaymentGateException
    return resp.url


def handle_payment_callback(callback_url: str) -> int:
    """Handles the callback from payment gate.

    Args:
        callback_url: The entire callback URL. So take `LocalRequest.url` and pass it
            here.
    Returns:
        Order number in the callback. Corresponds to the participant's database ID.
    Raises:
        PaymentUnsuccessfulException: If the payment did not end successfully.
    """
    url_qs = urllib.parse.parse_qs(urllib.parse.urlparse(callback_url).query)
    order_num = url_qs["ORDERNUMBER"][0]
    if order_num is None:
        logger.error(f"Found no order number in '{callback_url}'")
        raise PaymentUnsuccessfulException(
            "The payment gate did not provide your order number to us."
        )
    gw = gpwebpay.GpwebpayClient()
    key_bytes = base64.b64decode(GPWebpayConfig.GPWEBPAY_PUBLIC_KEY)
    payment_verification_result = gw.get_payment_result(callback_url, key_bytes)
    if payment_verification_result == {
        "RESULT": "The payment communication was compromised."
    }:
        logger.error(f"Payment compromised. ID: '{order_num}', URL: '{callback_url}'")
        raise PaymentUnsuccessfulException("The payment was compromised.")
    if payment_verification_result["PRCODE"] != "0":
        logger.error(f"Payment unsuccessful. URL: '{callback_url}'")
        raise PaymentUnsuccessfulException("Your payment did not end successfully.")
    return int(order_num)


def configure_gpwebpay() -> None:
    """gpwebpay uses a dumb way to configure itself. Here we override the way the
    configuration is done.

    Basically, we take configuration from the toml file and we create a new config
    object using our information.
    """
    gpwebpay_config.configuration.GPWEBPAY_CURRENCY = app.config[
        "registration_app.Payment.gpwebpay.currency"
    ]
    gpwebpay_config.configuration.GPWEBPAY_DEPOSIT_FLAG = app.config[
        "registration_app.Payment.gpwebpay.deposit_flag"
    ]
    gpwebpay_config.configuration.GPWEBPAY_MERCHANT_CALLBACK_URL = app.config[
        "registration_app.Payment.gpwebpay.callback_url"
    ]
    gpwebpay_config.configuration.GPWEBPAY_MERCHANT_ID = app.config[
        "registration_app.Payment.gpwebpay.merchant_id"
    ]
    gpwebpay_config.configuration.GPWEBPAY_MERCHANT_PRIVATE_KEY = app.config[
        "registration_app.Payment.gpwebpay.private_key"
    ]
    gpwebpay_config.configuration.GPWEBPAY_MERCHANT_PRIVATE_KEY_PASSPHRASE = app.config[
        "registration_app.Payment.gpwebpay.private_key_passphrase"
    ]
    gpwebpay_config.configuration.GPWEBPAY_PUBLIC_KEY = app.config[
        "registration_app.Payment.gpwebpay.public_key"
    ]
    gpwebpay_config.configuration.GPWEBPAY_URL = app.config[
        "registration_app.Payment.gpwebpay.url"
    ]
