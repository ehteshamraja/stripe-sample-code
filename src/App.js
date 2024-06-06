import React, { useState, useEffect } from 'react';
import './App.css';

const ProductDisplay = ({ handleCheckout }) => (
  <section>
    <div className="product">
      {/* <Logo /> */}
      <div className="description">
        <h3>Starter plan</h3>
        <h5>$20.00 / month</h5>
      </div>
    </div>
    <button onClick={handleCheckout}>
      Checkout
    </button>
  </section>
);

const SuccessDisplay = ({ sessionId, handleManageBilling }) => (
  <section>
    <div className="product Box-root">
      {/* <Logo /> */}
      <div className="description Box-root">
        <h3>Subscription to starter plan successful!</h3>
      </div>
    </div>
    <button onClick={() => handleManageBilling(sessionId)}>
      Manage your billing information
    </button>
  </section>
);

const Message = ({ message }) => (
  <section>
    <p>{message}</p>
  </section>
);

export default function App() {
  let [message, setMessage] = useState('');
  let [success, setSuccess] = useState(false);
  let [sessionId, setSessionId] = useState('');

  const handleCheckout = async () => {
    console.log("hello")
    try {
      const formData = new FormData();
      formData.append('price_id','price_1P9PuJK6Mh3He5TZgUdjQUgG' ); // Replace with actual lookup key
  
      const response = await fetch('http://localhost:8000/create-checkout-session', {
        method: 'POST',
        body: formData
      });

      console.log("hello",response)
      
  
      const data = await response.json();
      
      console.log(data)
      window.location.href = data.sessionId.url;
    } catch (error) {
      console.error('Error creating checkout session:', error);
      setMessage('Error creating checkout session. Please try again later.');
    }
  };

  useEffect(() => {
    // console.log(window.location.origin+window.location.pathname+window.location.search)
    const url = new URL(window.location.origin+window.location.pathname+window.location.search);
    const params = new URLSearchParams(url.search);

  console.log(params);

    console.log(params)
  
    if (params.get('session_id')) {
      setSuccess(true);
      setSessionId(params.get('session_id'));
    }

    if (params.get('canceled')) {
      setSuccess(false);
      setMessage(
        "Order canceled -- continue to shop around and checkout when you're ready."
      );
    }
  }, [sessionId]);

 
  

  const handleManageBilling = async (sessionId) => {
    try {
      const formData = new FormData();
      formData.append('session_id', sessionId);
      const response = await fetch('http://localhost:8000/create-portal-session', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      window.location.href = data.url;
    } catch (error) {
      console.error('Error creating portal session:', error);
      setMessage('Error creating portal session. Please try again later.');
    }
  };

  if (!success && message === '') {
    return <ProductDisplay handleCheckout={handleCheckout} />;
  } else if (success && sessionId !== '') {
    return <SuccessDisplay sessionId={sessionId} handleManageBilling={handleManageBilling} />;
  } else {
    return <Message message={message} />;
  }
}


