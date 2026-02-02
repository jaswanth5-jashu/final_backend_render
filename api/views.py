from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests

from .models import (
    CareerApplication,
    ContactMessage,
    MOU,
    GalleryImage,
    Project,
    CommunityItem,
    CpuInquiry,
    HackathonTeam,
)
from .serializers import (
    CareerApplicationSerializer,
    ContactMessageSerializer,
    MOUSerializer,
    GalleryImageSerializer,
    ProjectSerializer,
    CommunityItemSerializer,
    CpuInquirySerializer,
    HackathonTeamSerializer, 
    HackathonRegistrationSerializer,
)

#send messages to telegram 

def send_telegram(bot_token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=5)
    except:
        pass


class CareerApplicationCreate(APIView):

    def get(self, request):
        qs = CareerApplication.objects.all().order_by("-applied_at")
        serializer = CareerApplicationSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CareerApplicationSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            resume_url = ""
            if obj.resume:
                resume_url = request.build_absolute_uri(
                    settings.MEDIA_URL + obj.resume.name
                )

            send_telegram(
                settings.TELEGRAM_CAREER_BOT_TOKEN,
                settings.TELEGRAM_CAREER_CHAT_ID,
                f"Career Application\n\n"
                f"Name: {obj.full_name}\n"
                f"Email: {obj.email}\n"
                f"Phone: {obj.phone}\n"
                f"College: {obj.college}\n"
                f"CGPA: {obj.cgpa}\n"
                f"Year: {obj.year_of_passing}\n"
                f"Experience: {obj.experience}\n"
                f"Skills: {obj.skills}\n\n"
                f"Resume:\n{resume_url}"
            )

            return Response(
                {"message": "Application submitted successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(CareerApplication, pk=pk)
        obj.delete()
        return Response(
            {"message": "Career application deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ContactMessageCreate(APIView):

    def get(self, request):
        qs = ContactMessage.objects.all().order_by("-created_at")
        serializer = ContactMessageSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            send_telegram(
                settings.TELEGRAM_CONTACT_BOT_TOKEN,
                settings.TELEGRAM_CONTACT_CHAT_ID,
                f"Contact Message\n\n"
                f"Name: {obj.name}\n"
                f"Email: {obj.email}\n"
                f"Phone: {obj.phone}\n"
                f"Subject: {obj.subject}\n"
                f"Message: {obj.message}"
            )

            return Response(
                {"message": "Contact saved"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(ContactMessage, pk=pk)
        obj.delete()
        return Response(
            {"message": "Contact message deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "POST", "DELETE"])
def create_inquiry(request, pk=None):

    if request.method == "GET":
        qs = CpuInquiry.objects.all().order_by("-created_at")
        serializer = CpuInquirySerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CpuInquirySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            send_telegram(
                settings.TELEGRAM_CPU_BOT_TOKEN,
                settings.TELEGRAM_CPU_CHAT_ID,
                f"CPU Inquiry\n\n"
                f"Name: {obj.full_name}\n"
                f"Email: {obj.email}\n"
                f"Phone: {obj.phone}\n"
                f"CPU: {obj.cpu_model}\n"
                f"Quantity: {obj.quantity}\n"
                f"RAM: {obj.ram}\n"
                f"Storage: {obj.storage}\n"
                f"Message: {obj.message}"
            )

            return Response(
                {"message": "Inquiry submitted successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        obj = get_object_or_404(CpuInquiry, pk=pk)
        obj.delete()
        return Response(
            {"message": "CPU inquiry deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MOUListAPIView(ListAPIView):
    serializer_class = MOUSerializer

    def get_queryset(self):
        return MOU.objects.filter(is_active=True)


class GalleryImageListAPIView(ListAPIView):
    serializer_class = GalleryImageSerializer
    queryset = GalleryImage.objects.all().order_by("-created_at")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProjectListAPIView(APIView):
    def get(self, request):
        qs = Project.objects.all()
        serializer = ProjectSerializer(qs, many=True)
        return Response(serializer.data)


class CommunityItemListAPIView(ListAPIView):
    serializer_class = CommunityItemSerializer

    def get_queryset(self):
        return CommunityItem.objects.filter(section="giveback").order_by("-created_at")

class HackathonRegistrationCreate(APIView):

    def get(self, request):
        teams = HackathonTeam.objects.all().order_by("-created_at")
        serializer = HackathonTeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HackathonRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()

        # Get leader
        leader = team.participants.filter(role="LEADER").first()

        # Get members
        members = team.participants.filter(role="MEMBER")

        members_text = ""
        for i, member in enumerate(members, start=1):
            members_text += (
                f"\nMember {i}:\n"
                f"Name: {member.full_name}\n"
                f"Email: {member.email}\n"
                f"Phone: {member.phone}\n"
                f"Branch: {member.branch}\n"
                f"Section: {member.section}\n"
                f"Year: {member.year}\n"
            )

        message = (
            f"Hackathon Registration\n\n"
            f"Team Name: {team.team_name}\n"
            f"Total Participants: {team.total_participants}\n\n"
        )

        if leader:
            message += (
                f"Leader:\n"
                f"Name: {leader.full_name}\n"
                f"Email: {leader.email}\n"
                f"Phone: {leader.phone}\n"
                f"Branch: {leader.branch}\n"
                f"Section: {leader.section}\n"
                f"Year: {leader.year}\n"
            )

        message += members_text

        send_telegram(
            settings.TELEGRAM_HACKATHON_TOKEN,
            settings.TELEGRAM_HACKATHON_ID,
            message
        )

        return Response(
            {"message": "Hackathon registration successful", "team_id": team.id},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        team = get_object_or_404(HackathonTeam, pk=pk)
        team.delete()
        return Response(
            {"message": "Hackathon registration deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
