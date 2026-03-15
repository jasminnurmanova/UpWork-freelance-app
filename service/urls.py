from django.urls import path
from .views import ProjectCreateView, MyProjectsView, ProjectDetailView, ProjectsView, ProjectDetailFreelancerView, \
    BidCreateView, BidDetailView, FreelancerBidListView, ProjectBidListView, ClientBidListView, AcceptBidView, \
    ContractDetailView, FinishContractView, ReviewCreateView, ContractListView,SubmitWorkView,ProjectDeleteView,ProjectUpdateView,RejectBidView,FreelancerListView,ClientPaymentHistoryView,FreelancerEarningsHistoryView,FreelancerReviewsView,AboutView

urlpatterns = [
    path("projects/create/", ProjectCreateView.as_view(), name="project_create"),
    path("my-projects/", MyProjectsView.as_view(), name="my_projects"),
    path("project-detail/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("project-list/", ProjectsView.as_view(), name="project_list"),
    path("project-detail-freelancer/<int:pk>", ProjectDetailFreelancerView.as_view(), name="project_detail_freelancer"),
    path("send-bid/<int:pk>", BidCreateView.as_view(), name="send_bid"),
    path("bid-detail/<int:pk>", BidDetailView.as_view(), name="bid_detail"),
    path("bid-list/", FreelancerBidListView.as_view(), name="freelancer_bid_list"),
    path("projects/<int:project_id>/bids/",ProjectBidListView.as_view(),name="project_bids"),
    path("client/bids/", ClientBidListView.as_view(), name="client_bid_list"),
    path("bids/<int:bid_id>/accept/", AcceptBidView.as_view(), name="accept_bid"),
    path("contracts/<int:contract_id>/", ContractDetailView.as_view(), name="contract_detail"),
    path("contracts/<int:contract_id>/finish/", FinishContractView.as_view(), name="finish_contract"),
    path("contracts/<int:contract_id>/review/", ReviewCreateView.as_view(), name="create_review"),
    path("contract-list/", ContractListView.as_view(), name="contract_list"),
    path("contracts/<int:contract_id>/submit/", SubmitWorkView.as_view(), name="submit_work"),
    path("projects/<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("bids/<int:bid_id>/reject/", RejectBidView.as_view(), name="reject_bid"),
    path("find-freelancers/", FreelancerListView.as_view(), name="freelancer_list"),
    path("client/payment-history/",ClientPaymentHistoryView.as_view(), name="client_payment_history"),
    path("freelancer/earnings-history/",FreelancerEarningsHistoryView.as_view(),name="freelancer_earnings_history"),
    path("freelancer/reviews/",FreelancerReviewsView.as_view(),name="freelancer_reviews"),
    path("about/",AboutView.as_view(),name="about"),
    ]