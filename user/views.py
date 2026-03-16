from django.views import View
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import logout
from service.models import Project
from .models import User,Contract,Bid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Sum, Avg
from .models import Contract,Review,User,Submission


class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        now = timezone.now()
        total_spend = Contract.objects.filter(client=request.user,status="finished").aggregate(total=Sum("agreed_price") )["total"] or 0
        pending_proposals = Bid.objects.filter(project__client=request.user,status="pending" ).count()
        active_projects = Project.objects.filter(client=request.user,status="open")
        completed = Project.objects.filter(client=request.user,status='completed').count()
        count=len(active_projects)

        total_earnings = Contract.objects.filter(freelancer=request.user,status="finished").aggregate(total=Sum("agreed_price"))["total"] or 0
        active_contracts = Contract.objects.filter(freelancer=request.user, status="active").count()
        open_proposals = Bid.objects.filter(freelancer=request.user, status="pending").count()
        avg_rating = Review.objects.filter(contract__freelancer=request.user).aggregate(rating=Avg("rating"))["rating"] or 0
        active_projects_freelancer = (Project.objects.filter(status="open", contract__isnull=True).exclude(bids__freelancer=request.user).order_by("-created_at").distinct()[:3])
        context = {"total_earnings": total_earnings, "active_contracts": active_contracts, "open_proposals": open_proposals, "avg_rating": round(avg_rating, 1),'active_projects':active_projects,'count':count,'completed':completed,'total_spend':total_spend,'pending_proposals':pending_proposals,"active_projects_freelancer":active_projects_freelancer}

        return render(request, "home.html",context)


class RegisterView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return redirect("login")

        return render(request, "signup.html", {"form": form})


class LogoutUser(View):
    def post(self, request):
        logout(request)
        return redirect("login")


class ProfileView(View):
    def get(self, request):
        profile = User.objects.get(pk=request.user.pk)
        total_earnings = Contract.objects.filter(freelancer=request.user,status="finished").aggregate(total=Sum("agreed_price"))["total"] or 0
        active_contracts = Contract.objects.filter(freelancer=request.user, status="active").count()
        open_proposals = Bid.objects.filter(freelancer=request.user, status="pending").count()
        avg_rating = Review.objects.filter(contract__freelancer=request.user).aggregate(rating=Avg("rating"))["rating"] or 0
        active_projects_freelancer=Project.objects.filter(status="open").order_by("-created_at")
       #clientniki
        total_spend = Contract.objects.filter(client=request.user, status="finished").aggregate(total=Sum("agreed_price"))["total"] or 0
        pending_proposals = Bid.objects.filter(project__client=request.user, status="pending").count()
        active_projects = Project.objects.filter(client=request.user)
        completed = Project.objects.filter(client=request.user, status='completed').count()
        count = len(active_projects)

        context = {'count':count,'completed':completed,'pending_proposals':pending_proposals,'total_spend':total_spend,"total_earnings": total_earnings, "active_contracts": active_contracts,
                   "open_proposals": open_proposals, "avg_rating": round(avg_rating, 1),'active_projects_freelancer':active_projects_freelancer,'profile':profile}
        return render(request, 'profile.html', context)

class ProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.bio = request.POST.get("bio")

        if request.FILES.get("avatar"):
            user.avatar = request.FILES.get("avatar")
        user.save()
        return redirect("profile")


class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")
        if not check_password(current, user.password):
            messages.error(request, "Current password is incorrect.")
            return redirect("profile")

        if new != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("profile")
        user.set_password(new)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password updated successfully.")
        return redirect("profile")
