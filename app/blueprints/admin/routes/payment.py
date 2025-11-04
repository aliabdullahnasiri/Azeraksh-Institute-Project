from flask import render_template
from flask_login import login_required

from app.forms.payment import AddPaymentForm, UpdatePaymentForm

from .. import bp


@bp.get("/payments")
@login_required
def payments() -> str:
    add_payment_form: AddPaymentForm = AddPaymentForm()
    update_payment_form: UpdatePaymentForm = UpdatePaymentForm()

    return render_template(
        "admin/pages/payments.html",
        title="Payments",
        update_payment_form=update_payment_form,
        add_payment_form=add_payment_form,
    )
