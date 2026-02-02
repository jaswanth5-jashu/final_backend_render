from rest_framework import serializers
from .models import (
    CareerApplication,
    ContactMessage,
    MOU,
    GalleryImage,
    Project,
    CommunityItem,
    CpuInquiry,
)


class CareerApplicationSerializer(serializers.ModelSerializer):
    def validate_resume(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Resume must be a PDF file")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Resume size must be below 5MB")
        return value

    class Meta:
        model = CareerApplication
        fields = "__all__"


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"


class MOUSerializer(serializers.ModelSerializer):
    class Meta:
        model = MOU
        fields = "__all__"


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = ["id", "title", "category", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class CommunityItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityItem
        fields = "__all__"


class CpuInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuInquiry
        fields = "__all__"

from rest_framework import serializers
from .models import HackathonTeam, HackathonParticipant


class HackathonParticipantInputSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    branch = serializers.CharField(max_length=50)
    section = serializers.CharField(max_length=10)
    year = serializers.CharField(max_length=10)


class HackathonParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonParticipant
        fields = "__all__"


class HackathonTeamSerializer(serializers.ModelSerializer):
    participants = HackathonParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = HackathonTeam
        fields = ["id", "team_name", "total_participants", "created_at", "participants"]


class HackathonRegistrationSerializer(serializers.Serializer):
    # ✅ NOTE: these keys MUST match React payload
    team_name = serializers.CharField(max_length=150)
    total_participants = serializers.IntegerField(min_value=2, max_value=6)
    leader = HackathonParticipantInputSerializer()
    members = HackathonParticipantInputSerializer(many=True, required=False)

    def validate(self, attrs):
        members = attrs.get("members", [])
        expected_total = 1 + len(members)

        if attrs["total_participants"] != expected_total:
            raise serializers.ValidationError({
                "total_participants": f"Expected {expected_total} (leader + members)."
            })

        if expected_total < 2 or expected_total > 6:
            raise serializers.ValidationError("Team size must be 2–6 including leader.")

        return attrs

    def create(self, validated_data):
        leader_data = validated_data["leader"]
        members_data = validated_data.get("members", [])

        team = HackathonTeam.objects.create(
            team_name=validated_data["team_name"],
            total_participants=validated_data["total_participants"],
        )

        HackathonParticipant.objects.create(
            team=team,
            role="LEADER",
            **leader_data
        )

        for member in members_data:
            HackathonParticipant.objects.create(
                team=team,
                role="MEMBER",
                **member
            )

        return team
