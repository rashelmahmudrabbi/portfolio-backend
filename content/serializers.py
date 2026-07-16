from rest_framework import serializers
from . import models


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Education
        fields = ['id', 'degree', 'major', 'institution', 'year', 'grade', 'order']


class ExperienceSerializer(serializers.ModelSerializer):
    bullets = serializers.SerializerMethodField()

    class Meta:
        model = models.Experience
        fields = ['id', 'title', 'org', 'period', 'bullets', 'order']

    def get_bullets(self, obj):
        return obj.bullets_list


class PublicationSerializer(serializers.ModelSerializer):
    doiLink = serializers.CharField(source='doi_link')
    pdfLink = serializers.CharField(source='pdf_link')

    class Meta:
        model = models.Publication
        fields = ['id', 'type', 'status', 'title', 'authors', 'venue', 'year', 'abstract', 'doiLink', 'pdfLink', 'order']


class ProjectSerializer(serializers.ModelSerializer):
    tech = serializers.SerializerMethodField()
    githubLink = serializers.CharField(source='github_link')
    paperLink = serializers.CharField(source='paper_link')

    class Meta:
        model = models.Project
        fields = ['id', 'category', 'title', 'description', 'tech', 'year', 'githubLink', 'paperLink', 'featured', 'order']

    def get_tech(self, obj):
        return obj.tech_list


class CertificationSerializer(serializers.ModelSerializer):
    verifyLink = serializers.CharField(source='verify_link')
    pdfLink = serializers.CharField(source='pdf_link')

    class Meta:
        model = models.Certification
        fields = ['id', 'title', 'issuer', 'year', 'image', 'verifyLink', 'pdfLink', 'order']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Award
        fields = ['id', 'title', 'org', 'year', 'image', 'order']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ['id', 'text', 'order']


class GalleryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GalleryPhoto
        fields = ['src', 'caption']


class GalleryEventSerializer(serializers.ModelSerializer):
    photos = GalleryPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.GalleryEvent
        fields = ['id', 'title', 'year', 'photos', 'order']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'name', 'institution', 'period', 'role', 'order']


class BlogPostSerializer(serializers.ModelSerializer):
    readTime = serializers.CharField(source='read_time')

    class Meta:
        model = models.BlogPost
        fields = ['id', 'title', 'slug', 'date', 'readTime', 'category', 'excerpt', 'content', 'featured', 'order']


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        fields = ['id', 'name', 'role', 'org', 'note', 'phone', 'email', 'order']
