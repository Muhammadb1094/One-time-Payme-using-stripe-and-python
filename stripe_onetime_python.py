import stripe
import json

stripe.api_key = "STRIPE_SECRET_KEY"


def pay_from_stripe(data):

    try:
        card_number = data['card_number']
        cvc = data['cvc']
        exp_month = data['exp_month']
        exp_year = data['exp_year']
        amount = data['amount']
        email = data['email']
    except Exception as e:
        return {'error': str(e) + " is required"}
      
    try:
        # Check if Stripe customer exists, otherwise create a new customer
        customer = stripe.Customer.list(email=email).data[0] if stripe.Customer.list(
            email=email).data else stripe.Customer.create(email=email)
        customer_id = customer["id"]

        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                'number': card_number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc
            },
        )
        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer_id,
        )

        intent = stripe.PaymentIntent.create(
            amount=amount * 100,
            currency="gbp", # usd or whatever currency you have
            customer=customer_id,
            payment_method=payment_method.id,
            confirmation_method="manual",
            confirm=True,
            description="writ any small key description, purpose of payment"
        )

        if intent.status == "succeeded":
            return {'result': 'Payment succeeded'}
        else:
          return {'result': 'Payment succeeded'}

    except Exception as e:
        return {'error': str(e)}
      
