from django.shortcuts import render, get_object_or_404
from django.views import View
from django.shortcuts import render, redirect
from .forms import ProjectForm,BidForm
from .models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import Bid,Review,Contract,Submission
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Sum,Avg

User = get_user_model()


class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'project_create.html', {'form': ProjectForm()})

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect('home')
        return render(request, 'project_create.html', {'form': form})

class ProjectUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.client != request.user:
            raise PermissionDenied
        form = ProjectForm(instance=project)
        return render(request, "project_update.html", {"form": form,"project": project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.client != request.user:
            raise PermissionDenied
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, "project_update.html", {"form": form})

class ProjectDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.client != request.user:
            raise PermissionDenied
        project.delete()
        return redirect("home")


class MyProjectsView(View):
    def get(self, request):
        active_projects = Project.objects.filter(client=request.user,status='open')
        projects = Project.objects.filter(client=request.user)
        completed = Project.objects.filter(client=request.user, status='completed').count()
        progress = Project.objects.filter(client=request.user, status='in_progress').count()
        count = len(active_projects)
        return render(request, "my_projects.html", {"active_projects": active_projects,'count':count,'completed':completed,'progress':progress,'projects':projects})

class ProjectDetailView(View):
    def get(self,request,pk):
        project=get_object_or_404(Project,pk=pk)
        return render(request,'project_detail.html',{'project':project})

class ProjectsView(View):
    def get(self,request):
        projects = Project.objects.filter(status="open").order_by("-created_at")
        context = {"projects": projects}
        return render(request, "project_list.html", context)

class ProjectDetailFreelancerView(View):
    def get(self,request, pk):
        project = get_object_or_404(Project, id=pk)
        form = BidForm()
        user_bid = Bid.objects.filter(project=project,freelancer=request.user).first()
        context = { "project": project,"form": form,"user_bid": user_bid}
        return render(request, "project_detail_freelancer.html", context)


class BidCreateView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        form = BidForm()
        context = {"project": project,"form": form}
        return render(request, "send_bid.html", context)

    def post(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        if Bid.objects.filter(project=project, freelancer=request.user).exists():
            return redirect("project_detail", project_id=project.pk)
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.project = project
            bid.freelancer = request.user
            bid.save()
            return redirect("project_list")

        context = { "project": project,"form": form}
        return render(request, "send_bid.html", context)


class FreelancerBidListView(View):
    def get(self, request):
        bids = Bid.objects.filter(freelancer=request.user).select_related("project").order_by("-created_at")
        context = {"bids": bids}
        return render(request, "freelancer_bid_list.html", context)

class BidDetailView(View):
    def get(self, request, pk):
        bid = get_object_or_404(Bid, pk=pk, freelancer=request.user)
        context = {"bid": bid}
        return render(request, "bid_detail.html", context)


class ProjectBidListView(View):

    def get(self, request, project_id):

        project = get_object_or_404(Project, id=project_id)
        if project.client != request.user:
            raise PermissionDenied

        bids = Bid.objects.filter(project=project)

        context = {
            "project": project,
            "bids": bids
        }

        return render(request, "project_bids.html", context)

class ClientBidListView(View):
    def get(self, request):
        bids = Bid.objects.filter(project__client=request.user)
        context = {"bids": bids}

        return render(request, "client_bid_list.html", context)



class AcceptBidView(View):
    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project
        if project.client != request.user:
            raise PermissionDenied

        with transaction.atomic():
            bid.status = "accepted"
            bid.save()

            Bid.objects.filter(project=project).exclude(id=bid.id).update(status="rejected")

            project.status = "in_progress"
            project.save()

            Contract.objects.create(
                project=project,
                client=project.client,
                freelancer=bid.freelancer,
                agreed_price=bid.price,
                status="active"
            )

        return redirect("client_bid_list")


class RejectBidView(View):
    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project
        if project.client != request.user:
            raise PermissionDenied
        bid.status = "rejected"
        bid.save()
        return redirect("client_bid_list")

class ContractListView(View):
    def get(self, request):
        contracts = Contract.objects.filter(client=request.user) | Contract.objects.filter(freelancer=request.user)
        return render(request, "contract_list.html", {"contracts": contracts})

class ContractDetailView(View):
    def get(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if request.user not in [contract.client, contract.freelancer]:
            raise PermissionDenied
        return render(request, "contract_detail.html", {"contract": contract})

class SubmitWorkView(View):
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.freelancer != request.user:
            raise PermissionDenied
        Submission.objects.create(
            contract=contract,
            freelancer=request.user,
            file=request.FILES['file'],
            message=request.POST.get('message', '')
        )
        return redirect('contract_detail', contract_id=contract.id)
    def get(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        return render(request, 'submit_work.html', {'contract': contract})


class FinishContractView(View):
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.client != request.user:
            raise PermissionDenied
        contract.status = "finished"
        contract.save()
        project = contract.project
        project.status = "completed"
        project.save()

        return redirect("contract_detail", contract_id=contract.id)


class ReviewCreateView(View):
    def get(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.client != request.user:
            raise PermissionDenied
        return render(request, "review_create.html", {"contract": contract})

    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.client != request.user:
            raise PermissionDenied
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        Review.objects.create(
            contract=contract,
            rating=rating,
            comment=comment
        )
        return redirect("contract_detail", contract_id=contract.id)



class FreelancerListView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        freelancers = User.objects.filter(role="freelancer")
        if query:
            freelancers = freelancers.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(bio__icontains=query)
            )
        context = {"freelancers": freelancers,"query": query}

        return render(request, "freelancer_list.html", context)


class ClientPaymentHistoryView(View):
    def get(self, request):
        finished_contracts = Contract.objects.filter(client=request.user,status="finished").select_related("project", "freelancer")
        total_spent = finished_contracts.aggregate(total=Sum("agreed_price"))["total"] or 0
        context = {"contracts": finished_contracts,"total_spent": total_spent,}
        return render(request,"client_payment_history.html", context)



class FreelancerEarningsHistoryView(View):
    def get(self, request):
        finished_contracts = Contract.objects.filter(freelancer=request.user,status="finished").select_related("project", "client")
        total_earnings = finished_contracts.aggregate(total=Sum("agreed_price"))["total"] or 0
        average_payment = finished_contracts.aggregate(avg=Avg("agreed_price"))["avg"] or 0
        context = {"contracts": finished_contracts, "total_earnings": total_earnings,"average_payment": average_payment,"completed_projects": finished_contracts.count(),}
        return render(request, "freelancer_earnings_history.html", context)



class FreelancerReviewsView(View):
    def get(self, request):
        reviews = Review.objects.filter( contract__freelancer=request.user).select_related("contract", "contract__client")
        context = {"reviews": reviews}
        return render(request, "reviews.html", context)

class AboutView(View):
    def get(self,request):
        return render(request,'about.html')