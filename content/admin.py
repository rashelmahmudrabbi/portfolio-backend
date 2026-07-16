from django.contrib import admin
from . import models


# ---------------------------------------------------------------------------
# Site Settings (singleton) with inline editors for its small related lists
# ---------------------------------------------------------------------------
class ResearchInterestInline(admin.TabularInline):
    model = models.ResearchInterest
    extra = 1


class SpokenLanguageInline(admin.TabularInline):
    model = models.SpokenLanguage
    extra = 1


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
        ('Basic Profile', {'fields': ('name', 'title', 'email', 'phone', 'location', 'avatar', 'objective')}),
        ('Homepage Stats', {'fields': ('stat_publications', 'stat_projects', 'stat_awards', 'stat_certifications')}),
        ('Social Links', {'fields': ('social_github', 'social_linkedin', 'social_researchgate', 'social_scholar', 'social_orcid')}),
        ('Skills', {'fields': ('skills_languages', 'skills_frameworks', 'skills_tools', 'skills_research_methods')}),
        ('Personal Information', {'fields': ('father_name', 'mother_name', 'dob', 'religion', 'nid', 'marital_status', 'blood_group', 'nationality', 'address')}),
        ('Teaching', {'fields': ('teaching_philosophy', 'teaching_mentoring_text')}),
        ('Footer & CV', {'fields': ('footer_text', 'cv_last_updated', 'cv_download_url')}),
    )

    # Enforce singleton: no "add" once one exists, no delete at all.
    def has_add_permission(self, request):
        return not models.SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Skip the list page entirely - jump straight to the (only) settings record,
        # creating it on first visit if it doesn't exist yet.
        obj = models.SiteSettings.load()
        from django.shortcuts import redirect
        return redirect(f'/admin/content/sitesettings/{obj.pk}/change/')


# ---------------------------------------------------------------------------
# Repeatable collections
# ---------------------------------------------------------------------------
@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'year', 'grade', 'order')
    list_editable = ('order',)


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'org', 'period', 'order')
    list_editable = ('order',)


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'venue', 'year', 'order')
    list_filter = ('type', 'status')
    list_editable = ('type', 'status', 'order')


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'featured', 'order')
    list_filter = ('category', 'featured')
    list_editable = ('order',)


@admin.register(models.Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'year', 'order')
    list_editable = ('order',)


@admin.register(models.Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'org', 'year', 'order')
    list_editable = ('order',)


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('text', 'order')
    list_editable = ('order',)


class GalleryPhotoInline(admin.TabularInline):
    model = models.GalleryPhoto
    extra = 1


@admin.register(models.GalleryEvent)
class GalleryEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'order')
    list_editable = ('order',)
    inlines = [GalleryPhotoInline]


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'period', 'role', 'order')
    list_editable = ('order',)


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'featured', 'order')
    list_filter = ('category', 'featured')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'org', 'order')
    list_editable = ('order',)


admin.site.site_header = 'Portfolio Admin'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Manage your portfolio content'
