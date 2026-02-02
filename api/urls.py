from django.urls import path 
from .views import (
    CareerApplicationCreate,
    ContactMessageCreate,
    MOUListAPIView,
    GalleryImageListAPIView,
    ProjectListAPIView,
    CommunityItemListAPIView,
    create_inquiry,
     HackathonRegistrationCreate,
)

urlpatterns = [
    path("apply/", CareerApplicationCreate.as_view()),
    path("apply/<int:pk>/", CareerApplicationCreate.as_view()),
    path("contact/", ContactMessageCreate.as_view()),
    path("contact/<int:pk>/", ContactMessageCreate.as_view()),
    path("mous/", MOUListAPIView.as_view(), name="mous"),
    path("gallery/", GalleryImageListAPIView.as_view()),
    path("projects/", ProjectListAPIView.as_view()),
    path("giveback/", CommunityItemListAPIView.as_view()),
    path("inquiry/", create_inquiry),
    path("inquiry/<int:pk>/", create_inquiry),
    path("hackathon/", HackathonRegistrationCreate.as_view()),
    path("hackathon/<int:pk>/", HackathonRegistrationCreate.as_view()),
]

#urls