from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


# All content is edited through the Django admin (/admin), so the public
# API only ever needs to be readable - no auth/write endpoints required.
class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    pass


class EducationViewSet(ReadOnlyViewSet):
    queryset = models.Education.objects.all()
    serializer_class = serializers.EducationSerializer


class ExperienceViewSet(ReadOnlyViewSet):
    queryset = models.Experience.objects.all()
    serializer_class = serializers.ExperienceSerializer


class PublicationViewSet(ReadOnlyViewSet):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer


class ProjectViewSet(ReadOnlyViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class CertificationViewSet(ReadOnlyViewSet):
    queryset = models.Certification.objects.all()
    serializer_class = serializers.CertificationSerializer


class AwardViewSet(ReadOnlyViewSet):
    queryset = models.Award.objects.all()
    serializer_class = serializers.AwardSerializer


class ActivityViewSet(ReadOnlyViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class GalleryViewSet(ReadOnlyViewSet):
    queryset = models.GalleryEvent.objects.prefetch_related('photos').all()
    serializer_class = serializers.GalleryEventSerializer


class CourseViewSet(ReadOnlyViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class BlogPostViewSet(ReadOnlyViewSet):
    queryset = models.BlogPost.objects.all()
    serializer_class = serializers.BlogPostSerializer


class ReferenceViewSet(ReadOnlyViewSet):
    queryset = models.Reference.objects.all()
    serializer_class = serializers.ReferenceSerializer


class SettingsView(APIView):
    """
    Returns the singleton site settings in the exact nested shape the
    frontend's assets/js/site-*.js files expect, e.g.:
      { profile: {...}, researchInterests: [...], skills: {...}, ... }
    """

    def get(self, request):
        s = models.SiteSettings.load()
        data = {
            'profile': {
                'name': s.name,
                'title': s.title,
                'email': s.email,
                'phone': s.phone,
                'location': s.location,
                'avatar': s.avatar,
                'objective': s.objective,
                'stats': {
                    'publications': s.stat_publications,
                    'projects': s.stat_projects,
                    'awards': s.stat_awards,
                    'certifications': s.stat_certifications,
                },
                'socials': {
                    'github': s.social_github,
                    'linkedin': s.social_linkedin,
                    'researchgate': s.social_researchgate,
                    'scholar': s.social_scholar,
                    'orcid': s.social_orcid,
                },
            },
            'researchInterests': [
                {'icon': r.icon, 'topic': r.topic, 'desc': r.desc}
                for r in s.research_interests.all()
            ],
            'skills': {
                'languages': s.skills_languages_list,
                'frameworks': s.skills_frameworks_list,
                'tools': s.skills_tools_list,
                'researchMethods': s.skills_research_methods_list,
            },
            'spokenLanguages': [
                {'name': l.name, 'level': l.level} for l in s.spoken_languages.all()
            ],
            'personalInfo': {
                'fatherName': s.father_name,
                'motherName': s.mother_name,
                'dob': s.dob,
                'religion': s.religion,
                'nid': s.nid,
                'maritalStatus': s.marital_status,
                'bloodGroup': s.blood_group,
                'nationality': s.nationality,
                'address': s.address,
            },
            'teaching': {
                'philosophy': s.teaching_philosophy,
                'roles': [{'title': r.title, 'desc': r.desc} for r in s.teaching_roles.all()],
                'areas': [{'topic': a.topic, 'desc': a.desc} for a in s.teaching_areas.all()],
                'mentoringText': s.teaching_mentoring_text,
            },
            'footerText': s.footer_text,
            'cvLastUpdated': s.cv_last_updated,
            'cvDownloadUrl': s.cv_download_url,
        }
        return Response(data)
