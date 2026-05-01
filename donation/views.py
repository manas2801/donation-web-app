from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import qrcode
import base64
from io import BytesIO

from .models import Donation


def home(request):
    return redirect('login')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "register.html")


@login_required
def donate(request):
    qr_code = None
    amount = None
    donor_name = None
    donation_id = None

    if request.method == "POST":
        donor_name = request.POST.get("donor_name")
        amount = request.POST.get("amount")

        donation = Donation.objects.create(
            user=request.user,
            donor_name=donor_name,
            amount=amount,
            status="Pending"
        )

        donation_id = donation.id

        upi_id = "8709791448@pthdfc"   # put your real UPI ID
        name = "Manas Mayank"

        upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

        qr = qrcode.make(upi_link)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code = base64.b64encode(buffer.getvalue()).decode()

    donations = Donation.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "donate.html", {
        "qr_code": qr_code,
        "amount": amount,
        "donor_name": donor_name,
        "donation_id": donation_id,
        "donations": donations
    })


@login_required
def complete_payment(request, id):
    donation = Donation.objects.get(id=id, user=request.user)
    donation.status = "Completed"
    donation.save()

    messages.success(request, "Payment completed successfully!")
    return redirect("donate")