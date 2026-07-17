from django.contrib import admin
from . import models


# ---------------------------------------------------------------------------
# Site Settings (singleton) — inline editors for small related lists
# ---------------------------------------------------------------------------
class ResearchInterestInline(admin.TabularInline):
    model = models.ResearchInterest
    extra = 1
    verbose_name = "Research Interest"
    verbose_name_plural = "Research Interests"


class SpokenLanguageInline(admin.TabularInline):
    model = models.SpokenLanguage
    extra = 1
    verbose_name = "Spoken Language"
    verbose_name_plural = "Spoken Languages"


class TeachingRoleInline(admin.TabularInline):
    model = models.TeachingRole
    extra = 1


class TeachingAreaInline(admin.TabularInline):
    model = models.TeachingArea
    extra = 1


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [ResearchInterestInline, SpokenLanguageInline, TeachingRoleInline, TeachingAreaInline]
    fieldsets = (
        ('🧑 Basic Profile', {
            'description': 'Your name, title, contact details and profile photo path.',
            'fields': ('name', 'title', 'email', 'phone', 'location', 'avatar', 'objective'),
        }),
        ('📊 Homepage Stats', {
            'description': 'Numbers shown in the hero section (Publications / Projects / Awards / Certifications).',
            'fields': ('stat_publications', 'stat_projects', 'stat_awards', 'stat_certifications'),
        }),
        ('🔗 Social Links', {
            'fields': ('social_github', 'social_linkedin', 'social_researchgate', 'social_scholar', 'social_orcid'),
        }),
        ('💻 Skills', {
            'description': 'Enter each list as comma-separated values, e.g. "Python, C++, Java".',
            'fields': ('skills_languages', 'skills_frameworks', 'skills_tools', 'skills_research_methods'),
        }),
        ('👤 Personal Information', {
            'description': 'Shown in the CV personal info section.',
            'classes': ('collapse',),
            'fields': ('father_name', 'mother_name', 'dob', 'religion', 'nid', 'marital_status', 'blood_group', 'nationality', 'address'),
        }),
        ('📚 Teaching', {
            'classes': ('collapse',),
            'fields': ('teaching_philosophy', 'teaching_mentoring_text'),
        }),
        ('📄 CV Settings', {
            'description': 'Metadata for the CV/resume page.',
            'fields': ('cv_last_updated', 'cv_download_url', 'footer_text'),
        }),
    )

    # Enforce singleton: no "add" once one exists, no delete at all.
    def has_add_permission(self, request):
        return not models.SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = models.SiteSettings.load()
        from django.shortcuts import redirect
        return redirect(f'/admin/content/sitesettings/{obj.pk}/change/')


# ---------------------------------------------------------------------------
# CV-related models — grouped under "CV Content" via Meta.app_label proxy
# ---------------------------------------------------------------------------

# ── Education ───────────────────────────────────────────────────────────────
@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'major', 'institution', 'year', 'grade', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fieldsets = (
        (None, {
            'description': 'Add one row per degree/diploma. Lower "order" numbers appear first in the CV.',
            'fields': ('degree', 'major', 'institution', 'year', 'grade', 'order'),
        }),
    )


# ── Experience ──────────────────────────────────────────────────────────────
@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'org', 'period', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fieldsets = (
        (None, {
            'description': 'Each entry becomes a card in the "Research Experience" timeline on the CV.',
            'fields': ('title', 'org', 'period', 'bullets', 'order'),
        }),
    )


# ── Publications ────────────────────────────────────────────────────────────
@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'venue', 'year', 'order')
    list_filter = ('type', 'status')
    list_editable = ('type', 'status', 'order')
    ordering = ('order', 'id')
    fieldsets = (
        ('Metadata', {
            'fields': ('type', 'status', 'year', 'order'),
        }),
        ('Content', {
            'fields': ('title', 'authors', 'venue', 'abstract'),
        }),
        ('Links', {
            'fields': ('doi_link', 'pdf_link'),
        }),
    )


# ── Projects ────────────────────────────────────────────────────────────────
@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'featured', 'order')
    list_filter = ('category', 'featured')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'year', 'featured', 'order'),
        }),
        ('Details', {
            'fields': ('description', 'tech'),
        }),
        ('Links', {
            'fields': ('github_link', 'paper_link'),
        }),
    )


# ── Certifications ──────────────────────────────────────────────────────────
@admin.register(models.Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'year', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fieldsets = (
        (None, {
            'fields': ('title', 'issuer', 'year', 'order'),
        }),
        ('Links & Media', {
            'fields': ('image', 'verify_link', 'pdf_link'),
        }),
    )


# ── Awards ──────────────────────────────────────────────────────────────────
@admin.register(models.Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'org', 'year', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fieldsets = (
        (None, {
            'fields': ('title', 'org', 'year', 'image', 'order'),
        }),
    )


# ── References ──────────────────────────────────────────────────────────────
@admin.register(models.Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'org', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    fieldsets = (
        (None, {
            'description': 'These appear at the bottom of the CV as referee cards.',
            'fields': ('name', 'role', 'org', 'note', 'phone', 'email', 'order'),
        }),
    )


# ---------------------------------------------------------------------------
# Other collections
# ---------------------------------------------------------------------------
@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('text', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


class GalleryPhotoInline(admin.TabularInline):
    model = models.GalleryPhoto
    extra = 1


@admin.register(models.GalleryEvent)
class GalleryEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')
    inlines = [GalleryPhotoInline]


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'period', 'role', 'order')
    list_editable = ('order',)
    ordering = ('order', 'id')


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'featured', 'order')
    list_filter = ('category', 'featured')
    list_editable = ('order',)
    ordering = ('order', 'id')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'date', 'read_time', 'category', 'featured', 'order'),
        }),
        ('Content', {
            'fields': ('excerpt', 'content'),
        }),
    )


# ---------------------------------------------------------------------------
# Admin site branding
# ---------------------------------------------------------------------------
admin.site.site_header  = '📁 Portfolio Admin'
admin.site.site_title   = 'Portfolio Admin'
admin.site.index_title  = (
    'Welcome — manage all your portfolio content below.\n'
    'CV-related sections: Education · Experience · Publications · '
    'Projects · Certifications · Awards · References · Site Settings'
)
