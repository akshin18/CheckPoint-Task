from django.contrib import admin
from .models import Pattern, FlaggedMessage


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "regex",
        "matched_patterns_count",
        "created_at",
        "updated_at",
    )

    def matched_patterns_count(self, obj):
        return FlaggedMessage.objects.filter(matched_pattern=obj).count()

    matched_patterns_count.description = "Matched patterns count"


@admin.register(FlaggedMessage)
class FlaggedMessageAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "is_checked",
        "matched_pattern",
        "client_msg_id",
        "created_at",
        "updated_at",
    )
