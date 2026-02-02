from django.contrib import admin
from .models import CareerApplication,ContactMessage,MOU,GalleryImage,Project,CommunityItem

from django.contrib import admin
from .models import CpuInquiry

@admin.register(CpuInquiry)
class CpuInquiryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'cpu_model',
        'quantity',
        'ram',
        'storage',
        'created_at'
    )

    list_filter = ('cpu_model', 'created_at')
    search_fields = ('full_name', 'email', 'cpu_model')
    ordering = ('-created_at',)

    readonly_fields = ()   

@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'college',
        'year_of_passing',
        'applied_at'
    )
    search_fields = ('full_name', 'email', 'skills')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

@admin.register(MOU)
class MOUAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "start_date",
        "is_active",
    )
    list_filter = ("category", "is_active")
    search_fields = ("title",)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "status",
        "progress",
        "start_date",
        "end_date",
    )
    list_filter = ("status",)
    search_fields = ("title", "client")
    list_editable = ("status", "progress")

@admin.register(CommunityItem)
class CommunityItemAdmin(admin.ModelAdmin):

    list_display = ("title", "section", "item_type", "created_at")
    list_filter = ("section", "item_type")
    search_fields = ("title",)

    fieldsets = (
        ("Basic", {
            "fields": ("section", "item_type", "title", "description")
        }),
        ("Workshop Details", {
            "fields": ("date", "status", "participants"),
            "classes": ("workshop-fields",),
        }),
        ("Gallery Image", {
            "fields": ("image",),
            "classes": ("gallery-fields",),
        }),
    )

    class Media:
        js = ("admin/js/community_toggle.js",)

from django.contrib import admin
from .models import HackathonTeam, HackathonParticipant


@admin.register(HackathonTeam)
class HackathonTeamAdmin(admin.ModelAdmin):
    list_display = ("id", "team_name", "total_participants", "created_at")
    search_fields = ("team_name",)
    ordering = ("-created_at",)


@admin.register(HackathonParticipant)
class HackathonParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "role", "full_name", "email", "phone", "branch", "section", "year")
    search_fields = ("full_name", "email", "phone", "team__team_name")
    list_filter = ("role", "branch", "section", "year")
    ordering = ("-id",)
