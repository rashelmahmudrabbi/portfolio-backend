from django.db import models


class OrderedModel(models.Model):
    """Shared 'order' field so admins can control display order via a
    simple number, plus consistent default ordering everywhere."""
    order = models.IntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        abstract = True
        ordering = ['order', 'id']


# ---------------------------------------------------------------------------
# Singleton site settings + its small related lists (research interests,
# spoken languages, teaching roles/areas). Edited as one page in the admin
# via inlines.
# ---------------------------------------------------------------------------
class SiteSettings(models.Model):
    # --- Basic profile ---
    name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True, help_text="Headline, e.g. 'Graduate Researcher – Computer Vision & AI'")
    email = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    avatar = models.CharField(max_length=500, blank=True, help_text="Image path (e.g. media/profile/photo.jpg) or full URL")
    objective = models.TextField(blank=True, help_text="Career summary / objective shown on the homepage")

    # --- Homepage stats ---
    stat_publications = models.IntegerField(default=0)
    stat_projects = models.IntegerField(default=0)
    stat_awards = models.IntegerField(default=0)
    stat_certifications = models.IntegerField(default=0)

    # --- Social links ---
    social_github = models.CharField(max_length=300, blank=True)
    social_linkedin = models.CharField(max_length=300, blank=True)
    social_researchgate = models.CharField(max_length=300, blank=True)
    social_scholar = models.CharField(max_length=300, blank=True)
    social_orcid = models.CharField(max_length=300, blank=True)

    # --- Skills (comma-separated for simple admin editing) ---
    skills_languages = models.CharField(max_length=500, blank=True, help_text="Comma separated, e.g. Python, C/C++, Java")
    skills_frameworks = models.CharField(max_length=500, blank=True)
    skills_tools = models.CharField(max_length=500, blank=True)
    skills_research_methods = models.CharField(max_length=500, blank=True)

    # --- Personal info ---
    father_name = models.CharField(max_length=200, blank=True)
    mother_name = models.CharField(max_length=200, blank=True)
    dob = models.CharField(max_length=100, blank=True)
    religion = models.CharField(max_length=100, blank=True)
    nid = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=100, blank=True)
    blood_group = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    # --- Teaching ---
    teaching_philosophy = models.TextField(blank=True)
    teaching_mentoring_text = models.TextField(blank=True)

    # --- Footer / CV ---
    footer_text = models.CharField(max_length=300, blank=True)
    cv_last_updated = models.CharField(max_length=20, blank=True)
    cv_download_url = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent deleting the only settings row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Site Settings'

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    @property
    def skills_languages_list(self):
        return [s.strip() for s in self.skills_languages.split(',') if s.strip()]

    @property
    def skills_frameworks_list(self):
        return [s.strip() for s in self.skills_frameworks.split(',') if s.strip()]

    @property
    def skills_tools_list(self):
        return [s.strip() for s in self.skills_tools.split(',') if s.strip()]

    @property
    def skills_research_methods_list(self):
        return [s.strip() for s in self.skills_research_methods.split(',') if s.strip()]


class ResearchInterest(OrderedModel):
    settings = models.ForeignKey(SiteSettings, related_name='research_interests', on_delete=models.CASCADE)
    icon = models.CharField(max_length=100, blank=True, help_text="Bootstrap icon class, e.g. bi-eye")
    topic = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.topic


class SpokenLanguage(OrderedModel):
    settings = models.ForeignKey(SiteSettings, related_name='spoken_languages', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class TeachingRole(OrderedModel):
    settings = models.ForeignKey(SiteSettings, related_name='teaching_roles', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.title


class TeachingArea(OrderedModel):
    settings = models.ForeignKey(SiteSettings, related_name='teaching_areas', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.topic


# ---------------------------------------------------------------------------
# Repeatable collections
# ---------------------------------------------------------------------------
class Education(OrderedModel):
    degree = models.CharField(max_length=200, blank=True)
    major = models.CharField(max_length=200, blank=True)
    institution = models.CharField(max_length=300, blank=True)
    year = models.CharField(max_length=20, blank=True)
    grade = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.degree


class Experience(OrderedModel):
    title = models.CharField(max_length=300, blank=True)
    org = models.CharField(max_length=300, blank=True)
    period = models.CharField(max_length=100, blank=True)
    bullets = models.TextField(blank=True, help_text="One bullet point per line")

    def __str__(self):
        return self.title

    @property
    def bullets_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]


class Publication(OrderedModel):
    TYPE_CHOICES = [('conference', 'Conference'), ('journal', 'Journal'), ('thesis', 'Thesis')]
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('under-review', 'Under Review'),
        ('completed', 'Completed'),
        ('accepted', 'Accepted'),
        ('preprint', 'Preprint'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='conference')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    title = models.CharField(max_length=400, blank=True)
    authors = models.CharField(max_length=500, blank=True)
    venue = models.CharField(max_length=400, blank=True)
    year = models.CharField(max_length=20, blank=True)
    abstract = models.TextField(blank=True)
    doi_link = models.CharField(max_length=500, blank=True)
    pdf_link = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Project(OrderedModel):
    CATEGORY_CHOICES = [('thesis', 'Thesis'), ('research', 'Research'), ('development', 'Development')]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='research')
    title = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    tech = models.CharField(max_length=500, blank=True, help_text="Comma separated, e.g. PyTorch, OpenCV, LIME")
    year = models.CharField(max_length=20, blank=True)
    github_link = models.CharField(max_length=500, blank=True)
    paper_link = models.CharField(max_length=500, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech.split(',') if t.strip()]


class Certification(OrderedModel):
    title = models.CharField(max_length=300, blank=True)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)
    image = models.CharField(max_length=500, blank=True)
    verify_link = models.CharField(max_length=500, blank=True)
    pdf_link = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Award(OrderedModel):
    title = models.CharField(max_length=300, blank=True)
    org = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)
    image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title


class Activity(OrderedModel):
    text = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.text


class GalleryEvent(OrderedModel):
    title = models.CharField(max_length=300, blank=True)
    year = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title


class GalleryPhoto(OrderedModel):
    event = models.ForeignKey(GalleryEvent, related_name='photos', on_delete=models.CASCADE)
    src = models.CharField(max_length=500, help_text="Image path (e.g. media/gallery/Event/photo.jpg) or full URL")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.caption or self.src


class Course(OrderedModel):
    name = models.CharField(max_length=300, blank=True)
    institution = models.CharField(max_length=300, blank=True)
    period = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class BlogPost(OrderedModel):
    title = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(max_length=300, blank=True, unique=False)
    date = models.CharField(max_length=50, blank=True, help_text="e.g. 'March 2025'")
    read_time = models.CharField(max_length=50, blank=True, help_text="e.g. '8 min read'")
    category = models.CharField(max_length=100, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Reference(OrderedModel):
    name = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=300, blank=True)
    org = models.CharField(max_length=300, blank=True)
    note = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
