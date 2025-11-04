import json
from datetime import datetime
from typing import Dict, List, OrderedDict, Tuple, Union

from flask import Response, current_app
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms.payment import AddPaymentForm, UpdatePaymentForm
from app.models.payment import Payment
from app.types import ColumnID, ColumnName


@bp.get("/fetch/payments")
@login_required
def fetch_payments() -> Response:
    payments: List[Payment] = Payment.query.all()

    response: Response = Response(
        json.dumps([payment.to_dict() for payment in payments]),
        status=200,
        headers={"Content-Type": "application/json"},
    )
    return response


@bp.get("/fetch/rows/payments")
@login_required
def fetch_payments_rows() -> Response:
    response: Response = Response(headers={"Content-Type": "application/json"})

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("payment_id"), ColumnName("Payment ID")),
        (ColumnID("enrollment_id"), ColumnName("Enrollment ID")),
        (ColumnID("amount"), ColumnName("Amount")),
        (ColumnID("payment_date"), ColumnName("Payment Date")),
        (ColumnID("month_for"), ColumnName("For Month")),
    ]

    payments: List[Payment] = Payment.query.all()
    rows: List[List] = []

    for payment in payments:
        row: List = []
        for col_id, _ in cols:
            val = getattr(payment, col_id, None)

            match col_id:
                case "payment_date":
                    row.append(payment.display_payment_date)
                case "amount":
                    row.append(payment.display_amount)
                case "month_for":
                    row.append(payment.display_month_for)
                case _:
                    row.append(val)

        rows.append(row)

    dct: Dict = {"cols": cols, "rows": rows}
    response.response = json.dumps(dct)
    response.status_code = 200
    return response


@bp.get("/fetch/payment/<int:payment_id>")
@login_required
def fetch_payment(payment_id: int) -> Response:
    payment: Union[Payment, None] = Payment.query.filter_by(
        payment_id=payment_id
    ).first()

    r: Response = Response(headers={"Content-Type": "application/json"})

    if payment:
        r.response = json.dumps(OrderedDict(payment.to_dict()))
        r.status_code = 200
    else:
        dct = {"message": "Payment not found", "category": "error"}
        r.response = json.dumps(dct)
        r.status_code = 404

    return r


@bp.get("/fetch/row/payment/<int:payment_id>")
@login_required
def fetch_payment_row(payment_id: int) -> Response:
    payment: Union[Payment, None] = Payment.query.filter_by(
        payment_id=payment_id
    ).first()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if payment:
        dct = OrderedDict(
            {
                "payment_id": payment.payment_id,
                "enrollment_id": payment.enrollment_id,
                "amount": payment.display_amount,
                "payment_date": payment.display_payment_date,
                "month_for": payment.display_month_for,
            }
        )
        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        response.response = json.dumps(
            {"message": "Payment not found", "category": "error"}
        )
        response.status_code = 404

    return response


@bp.post("/update/payment")
@login_required
def update_payment() -> Response:
    form: UpdatePaymentForm = UpdatePaymentForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        payment: Union[Payment, None] = Payment.query.filter_by(
            payment_id=form.payment_id.data
        ).first()

        if payment:
            payment.enrollment_id = form.enrollment_id.data
            payment.amount = form.amount.data

            if form.month_for.data:
                payment.month_for = form.month_for.data.strftime(r"%Y-%m")

            db.session.commit()

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Payment updated successfully!",
                    "category": "success",
                }
            )
        else:
            pass
    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/payment/<int:payment_id>")
@login_required
def delete_payment(payment_id: int) -> Response:
    payment: Union[Payment, None] = Payment.query.filter_by(
        payment_id=payment_id
    ).first()
    response: Response = Response()

    if payment:
        db.session.delete(payment)
        db.session.commit()

        dct = {
            "message": "Payment deleted successfully",
            "category": "success",
            "status": 200,
        }

        response.response = json.dumps(dct)
        response.status_code = 200

    else:
        dct = {
            "message": "Payment with the given ID was not found :(",
            "category": "error",
            "status": 404,
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/add/payment")
@login_required
def add_payment() -> Response:
    form: AddPaymentForm = AddPaymentForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        payment: Payment = Payment()

        payment.enrollment_id = form.enrollment_id.data
        payment.amount = form.amount.data
        if form.month_for.data:
            payment.month_for = form.month_for.data.strftime("%Y-%m")
        payment.payment_date = datetime.now()

        db.session.add(payment)
        db.session.commit()

        dct = {}

        dct["message"] = "Payment added successfully."
        dct["title"] = "Added!"
        dct["category"] = "success"
        dct["id"] = payment.payment_id

        response.response = json.dumps(dct)
    else:
        dct = {"errors": form.errors}

        response.response = json.dumps(dct)

    return response
