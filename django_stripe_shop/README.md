Project Overview

This is a simple e-commerce application that allows customers to purchase products through Stripe Checkout. The application lists products, lets users select quantities, and processes payments securely via Stripe.

Assumptions

Products are pre-populated in the database.

Prices are fixed and stored in the database.

The application uses Stripe Checkout for simplicity and reliability.

No complex cart system; quantities are entered directly in the form.

Orders are considered paid only after successful Stripe Checkout completion.

Flow Chosen

Stripe Checkout Sessions were chosen instead of Payment Intents because:

Checkout Sessions provide a complete pre-built payment UI.

They handle tax, shipping, and payment authentication automatically.

They reduce complexity in backend logic and speed up development.

Ideal for quick checkout without building a custom payment flow.


Avoiding Double Charge / Inconsistent State

Orders are created only after successful payment confirmation from Stripe webhook events.

No order creation happens until a checkout session is completed.

Webhooks ensure the system state stays consistent even if the user closes the browser after payment.

Idempotency is ensured by using Stripe session IDs to prevent duplicate order creation.

Notes on Code Quality & Logic

Code follows Django’s MVC structure for clarity.

Stripe keys are stored securely in environment variables.

Templates use Bootstrap for responsive design and clean UI.

Code is modular to allow easy extension for additional payment features.

Comments are included to explain critical logic and Stripe integration.

AI-assist.md
AI Tools Used

ChatGPT (GPT-5-mini): Assisted in writing README.md, AI-assist.md, and improving HTML/CSS for Stripe Checkout integration.

Stack Overflow & Stripe Docs: Used for reference and best practices.

Time Spent

Total Hours Spent: ~4 hours

Stripe integration & testing: 2 hours

MVT/HTML/CSS styling: 1 hour

Documentation: 1 hour
