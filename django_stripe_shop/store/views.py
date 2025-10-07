
import uuid
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from .models import Product, Order
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    client_token = request.session.get("client_token")
    if not client_token:
        client_token = uuid.uuid4().hex
        request.session["client_token"] = client_token

    products = Product.objects.all().order_by("id")
    orders = Order.objects.filter(paid=True).order_by("-created_at")

    session_id = request.GET.get("session_id")
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception as e:
            session = None

        if session and session.payment_status == "paid":
            try:
                order = Order.objects.get(stripe_session_id=session_id)
                if not order.paid:
                    order.paid = True
                    order.save()
            except Order.DoesNotExist:
                pass
            orders = Order.objects.filter(paid=True).order_by("-created_at")

    context = {
        "products": products,
        "orders": orders,
        "client_token": client_token,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, "store/index.html", context)


@require_POST
def create_checkout_session(request):
    client_token = request.POST.get("client_token")
    if not client_token or client_token != request.session.get("client_token"):
        return HttpResponseBadRequest("Invalid client token.")

    try:
        existing_order = Order.objects.get(client_token=client_token)
        if existing_order.stripe_session_url:
            return redirect(existing_order.stripe_session_url)
    except Order.DoesNotExist:
        existing_order = None

    items = []
    total_cents = 0
    product_ids = request.POST.getlist("product_id")
    qtys = request.POST.getlist("qty")
    if not product_ids or not qtys or len(product_ids) != len(qtys):
        return HttpResponseBadRequest("Invalid form submission.")

    line_items = []
    for pid, q in zip(product_ids, qtys):
        try:
            p = Product.objects.get(id=int(pid))
        except Product.DoesNotExist:
            continue
        qty = int(q) if q and q.isdigit() else 0
        if qty <= 0:
            continue
        items.append({"product_id": p.id, "name": p.name, "qty": qty, "unit_price_cents": p.price_cents})
        total_cents += p.price_cents * qty
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": p.name},
                "unit_amount": p.price_cents,
            },
            "quantity": qty,
        })

    if not items:
        return HttpResponseBadRequest("No quantities selected.")

    if existing_order is None:
        order = Order.objects.create(client_token=client_token, items=items, total_cents=total_cents)
    else:
        order = existing_order
        order.items = items
        order.total_cents = total_cents
        order.save()

    base_url = request.build_absolute_uri("/")[:-1]  
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=base_url + "/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=base_url + "/",
            metadata={"order_id": str(order.id)},
        )
    except Exception as e:
        return HttpResponseBadRequest(f"Stripe error: {str(e)}")

    order.stripe_session_id = checkout_session.id
    order.stripe_session_url = checkout_session.url
    order.save()

    return redirect(checkout_session.url)
