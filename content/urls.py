from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

# trailing_slash=False so routes are /api/education (matching the existing
# frontend fetch calls) instead of DRF's default /api/education/
router = DefaultRouter(trailing_slash=False)
router.register(r'education', views.EducationViewSet, basename='education')
router.register(r'experience', views.ExperienceViewSet, basename='experience')
router.register(r'publications', views.PublicationViewSet, basename='publications')
router.register(r'projects', views.ProjectViewSet, basename='projects')
router.register(r'certifications', views.CertificationViewSet, basename='certifications')
router.register(r'awards', views.AwardViewSet, basename='awards')
router.register(r'activities', views.ActivityViewSet, basename='activities')
router.register(r'gallery', views.GalleryViewSet, basename='gallery')
router.register(r'courses', views.CourseViewSet, basename='courses')
router.register(r'blog', views.BlogPostViewSet, basename='blog')
router.register(r'references', views.ReferenceViewSet, basename='references')

urlpatterns = [
    path('settings', views.SettingsView.as_view()),
] + router.urls
