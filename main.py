from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import stripe

app = FastAPI()

# Enable CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your React frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Stripe API key
stripe.api_key = 'your stripe api key here'
print(stripe.Price.list(active=True))
YOUR_DOMAIN = 'http://localhost:3000'  # Update with your React frontend URL

@app.post('/create-checkout-session')
async def create_checkout_session(price_id: str = Form(...)):
    try:
      
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/checkout?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/canceled',
        )
        print(checkout_session)
        return JSONResponse(content={"sessionId": checkout_session})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")

@app.post('/create-portal-session')
async def customer_portal(session_id: str = Form(...)):
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    return_url = YOUR_DOMAIN

    portal_session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url,
    )
    return JSONResponse(content={"url": portal_session.url})

@app.post('/')
async def webhook_received(request: Request):
    webhook_secret = 'we_1PDLONP9Qs0RE483O7Gzv5be'
    request_data = await request.json()


    if webhook_secret=="hello":
        print("if")
        # signature = request.headers.get('stripe-signature')
        signature='whsec_yfEuDk9NbHBrAj2PkdXlF4KPW3v8AU2j'
        try:
            event = stripe.Webhook.construct_event(
                payload=await request.body(), sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            print(e)
            return str(e)
        event_type = event['type']
    else:
        print("else")
        data = request_data['data']
        event_type = request_data['type']

    print('event ' + event_type)

    if event_type == 'invoice.paid':
       print('paid invoice')
    #  Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
       
    elif event_type == 'checkout.session.completed':
        # print('Session')
        session = stripe.checkout.Session.retrieve(
        request_data['data']['object']['id'],
        expand=['line_items'],
        )
        print("session printing",session)
    elif event_type == 'customer.subscription.trial_will_end':
        print('Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('Subscription created %s', event_type)
    elif event_type == 'customer.subscription.updated':
        print('Subscription created %s', event_type)
    elif event_type == 'customer.subscription.deleted':
        print('Subscription canceled: %s', event_type)
   
        print(request_data)
    return JSONResponse(content={'status': 'success'})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
