import os

import stripe
from stripe._error import StripeError
from stripe.checkout import Session

from src.Model.Order import Order
from src.utils.log_decorator import log


class StripeService:
    def __init__(self):
        stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
        self.base_url = os.environ["BASE_URL"]
        self.success_url = f"{self.base_url}/payment/success"

    @log
    def create_checkout_session(self, order: Order, customer_mail: str) -> Session:
        """
        _summary_

        Parameters
        ----------
        order : Order
            _description_
        customer_mail : str
            _description_

        Returns
        -------
        Session
            _description_

        Raises
        ------
        ValueError
            _description_
        ValueError
            _description_
        """
        if len(order.order_orderables) == 0:
            raise ValueError("Your order is empty.")

        line_items = []

        for orderable, quantity in order.order_orderables.items():
            if orderable.orderable_type == "item":
                orderable_name = orderable.item_name
                orderable_description = orderable.item_description

            if orderable.orderable_type == "bundle":
                orderable_name = orderable.bundle_name
                orderable_description = orderable.bundle_description

            price = int(orderable.price * 100)

            data = {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": price,
                    "product_data": {"name": orderable_name, "description": orderable_description},
                },
                "quantity": quantity,
            }
            line_items.append(data)

        try:
            session = Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"{self.success_url}?session_id={{CHECKOUT_SESSION_ID}}"
                f"&order_id={order.order_id}",
                customer_email=customer_mail,
                metadata={
                    "order_id": str(order.order_id),
                    "customer_id": str(order.order_customer_id),
                },
                payment_intent_data={
                    "metadata": {
                        "order_id": str(order.order_id),
                    }
                },
            )
            return session.url

        except StripeError as e:
            raise ValueError(f"Error while creating Stripe checkout session: {str(e)}") from e

    @log
    def verify_payment(self, session_id: int):
        """
        _summary_

        Parameters
        ----------
        session_id : int
            _description_

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        ValueError
            _description_
        """
        try:
            session = Session.retrieve(session_id)

            return {
                "paid": session.payment_status == "paid",
                "payment_status": session.payment_status,
                "order_id": session.metadata.get("order_id"),
                "customer_id": session.metadata.get("customer_id"),
                "amount_total": session.amount_total / 100,
                "currency": session.currency,
                "customer_email": session.customer_details.email,
            }

        except StripeError as e:
            raise ValueError(f"Error while retrieving payment status: {str(e)}") from e
