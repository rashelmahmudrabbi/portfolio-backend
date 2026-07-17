import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from content import models


class Command(BaseCommand):
    help = (
        "Seeds the database with the original portfolio content and creates the admin superuser.\n"
        "By default, skips any section that already has data.\n"
        "Pass --force to wipe and re-seed everything (WARNING: overwrites all your changes)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Wipe existing data and re-seed everything. WARNING: all admin edits will be lost.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.force = options['force']
        if self.force:
            self.stdout.write(self.style.WARNING(
                'Running in FORCE mode — all existing data will be overwritten.'
            ))
        self.create_superuser()
        self.seed_settings()
        self.seed_education()
        self.seed_experience()
        self.seed_publications()
        self.seed_projects()
        self.seed_certifications()
        self.seed_awards()
        self.seed_activities()
        self.seed_gallery()
        self.seed_courses()
        self.seed_blog()
        self.seed_references()
        self.stdout.write(self.style.SUCCESS('Seed complete!'))

    # ── helpers ──────────────────────────────────────────────────────────────
    def _skip(self, label, qs):
        """Return True (and print a skip message) if data exists and --force was NOT passed."""
        if not self.force and qs.exists():
            self.stdout.write(f'  Skipping {label} — data already exists (use --force to overwrite).')
            return True
        return False

    # ── superuser ────────────────────────────────────────────────────────────
    def create_superuser(self):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'change_this_password')
        if User.objects.filter(username=username).exists():
            self.stdout.write('Admin user already exists, leaving password untouched.')
            return
        User.objects.create_superuser(username=username, email='', password=password)
        self.stdout.write(self.style.SUCCESS(f'Admin user created: {username}'))

    # ── settings (singleton — only seed if name is blank or --force) ─────────
    def seed_settings(self):
        s = models.SiteSettings.load()
        # For the singleton we treat "name is already set" as "already configured"
        if not self.force and s.name:
            self.stdout.write(
                f'  Skipping Site Settings — already configured as "{s.name}" (use --force to overwrite).'
            )
            return

        s.name = 'Rashel Mahmud Rabbi'
        s.title = 'Graduate Researcher – Computer Vision & AI'
        s.email = 'raselmahud6757@gmail.com'
        s.phone = '+8801613-000855'
        s.location = 'Bangladesh'
        s.avatar = 'media/profile/Prof._Passport_size_image.jpg'
        s.objective = (
            'Aspiring AI researcher and deep learning engineer passionate about computer vision, medical image '
            'analysis, and explainable AI. Focused on developing intelligent healthcare solutions through '
            'innovative research in CNNs, Transformers, and hybrid deep learning architectures. Experienced in '
            'dataset curation, model development, and academic writing with a strong publication record. '
            'Committed to advancing AI research for real-world impact in healthcare and remote sensing.'
        )
        s.stat_publications = 3
        s.stat_projects = 7
        s.stat_awards = 2
        s.stat_certifications = 2
        s.social_github = 'https://github.com/rashelmahmudrabbi'
        s.social_linkedin = 'https://www.linkedin.com/in/rashelmahmudrabbi'
        s.social_researchgate = 'https://www.researchgate.net/profile/rashel-mahmud-rabbi'
        s.social_scholar = 'https://scholar.google.com/citations?hl=en&user=agrATD8AAAAJ'
        s.social_orcid = 'https://orcid.org/0009-0004-6070-4496'
        s.skills_languages = 'Python, C/C++, Java'
        s.skills_frameworks = 'PyTorch, TensorFlow, OpenCV, Scikit-learn, FastAI, Django'
        s.skills_tools = 'Git, Jupyter Notebook, Google Colab, LaTeX, VS Code'
        s.skills_research_methods = 'LIME / SHAP, Statistical Analysis, Dataset Curation, Academic Writing'
        s.father_name = 'Md. Ahsan Habib'
        s.mother_name = 'Mst. Rina Parvin'
        s.dob = '13 January 2003'
        s.religion = 'Islam'
        s.nid = '8712333650'
        s.marital_status = 'Single'
        s.blood_group = 'O (+ve)'
        s.nationality = 'Bangladeshi'
        s.address = 'Barigram, Hat-Gangopara, Bagmara, Rajshahi, Bangladesh'
        s.teaching_philosophy = (
            'I believe effective teaching in AI and Computer Science bridges theory and hands-on practice. My '
            'goal is to cultivate critical thinking and research curiosity — helping students not just implement '
            'models, but understand why they work, where they fail, and how to push the boundaries of existing '
            'knowledge.'
        )
        s.teaching_mentoring_text = (
            "I'm happy to help undergraduate and graduate students with research questions, project guidance, "
            "or academic writing in AI and Computer Vision."
        )
        s.footer_text = 'I certify that all information in this portfolio is accurate and true.'
        s.cv_last_updated = '2025'
        s.cv_download_url = ''
        s.save()

        s.research_interests.all().delete()
        for i, (icon, topic, desc) in enumerate([
            ('bi-eye', 'Computer Vision', 'Image classification, object detection, segmentation'),
            ('bi-heart-pulse', 'Medical Image Analysis', 'AI-driven diagnostics, histology, radiology imaging'),
            ('bi-diagram-3', 'Deep Learning', 'CNN, Transformer, LSTM architectures'),
            ('bi-lightbulb', 'Explainable AI', 'LIME, SHAP, model interpretability'),
            ('bi-globe', 'Remote Sensing', 'Satellite image processing and analysis'),
            ('bi-chat-text', 'Natural Language Processing', 'Text classification, information extraction'),
        ]):
            models.ResearchInterest.objects.create(settings=s, order=i, icon=icon, topic=topic, desc=desc)

        s.spoken_languages.all().delete()
        for i, (name, level) in enumerate([
            ('Bangla', 'Mother Tongue'), ('English', 'Fluent'), ('Hindi', 'Fluent'),
        ]):
            models.SpokenLanguage.objects.create(settings=s, order=i, name=name, level=level)

        s.teaching_roles.all().delete()
        for i, (title, desc) in enumerate([
            ('Club President', 'As President of NBIU Computer Society, organized tech talks, seminars, and research orientation sessions.'),
            ('Workshop Facilitator', 'Led hands-on workshops in Deep Learning and Computer Vision for fellow students and academic clubs.'),
        ]):
            models.TeachingRole.objects.create(settings=s, order=i, title=title, desc=desc)

        s.teaching_areas.all().delete()
        for i, (topic, desc) in enumerate([
            ('Computer Vision', 'image classification, detection, segmentation'),
            ('Deep Learning', 'CNNs, LSTMs, Transformers, training pipelines'),
            ('Medical Image Analysis', 'histology, radiology, AI diagnostics'),
            ('Explainable AI', 'LIME, SHAP, interpretability frameworks'),
            ('Remote Sensing', 'satellite imagery, land-use classification'),
            ('Python for Research', 'PyTorch, TensorFlow, OpenCV, Pandas'),
        ]):
            models.TeachingArea.objects.create(settings=s, order=i, topic=topic, desc=desc)

        self.stdout.write('  Settings seeded.')

    # ── education ────────────────────────────────────────────────────────────
    def seed_education(self):
        if self._skip('Education', models.Education.objects.all()):
            return
        models.Education.objects.all().delete()
        rows = [
            ('B.Sc in CSE', 'Computer Science & Engineering', 'North Bengal International University', '2025', '3.87/4.00'),
            ('HSC', 'Science', 'Mymensingh - 01', '2020', '5.00/5.00'),
            ('SSC', 'Science', 'Rajshahi', '2018', '5.00/5.00'),
            ('JSC', '–', 'Rajshahi', '2016', '4.65/5.00'),
            ('PSC', '–', 'Bagmara, Rajshahi', '2012', '4.25/5.00'),
        ]
        for i, (degree, major, institution, year, grade) in enumerate(rows):
            models.Education.objects.create(order=i, degree=degree, major=major, institution=institution, year=year, grade=grade)
        self.stdout.write('  Education seeded.')

    # ── experience ───────────────────────────────────────────────────────────
    def seed_experience(self):
        if self._skip('Experience', models.Experience.objects.all()):
            return
        models.Experience.objects.all().delete()
        models.Experience.objects.create(
            order=0,
            title='Graduate Researcher – Computer Vision / Medical Imaging',
            org='North Bengal International University',
            period='2023 – 2025',
            bullets='\n'.join([
                'Developed deep learning models for satellite and medical image classification',
                'Worked with CNN, LSTM, and Transformer-based architectures',
                'Applied Explainable AI techniques (LIME)',
                'Experienced in dataset preprocessing, model optimization, and evaluation',
            ]),
        )
        self.stdout.write('  Experience seeded.')

    # ── publications ─────────────────────────────────────────────────────────
    def seed_publications(self):
        if self._skip('Publications', models.Publication.objects.all()):
            return
        models.Publication.objects.all().delete()
        models.Publication.objects.create(
            order=0, type='conference', status='published',
            title='An Explainable Approach to Land-Use Classification Using CNN-LSTM and LIME',
            authors='Md Ashik Ahmmed; Rashel Mahmud Rabbi; Md Shafiuzzaman; Tithi Podder; Most. Tasnina Jaman; Afsana Tasnim',
            venue='IEEE International Conference on Quantum Photonics, Artificial Intelligence, and Networking (QPAIN)',
            year='2025',
            abstract='This paper presents an explainable approach to land-use classification using a hybrid CNN-LSTM architecture combined with LIME. Experiments on the EuroSAT dataset demonstrate competitive classification accuracy while offering meaningful insight into model decisions.',
            doi_link='https://ieeexplore.ieee.org/document/11172239',
            pdf_link='https://ieeexplore.ieee.org/document/11172239',
        )
        models.Publication.objects.create(
            order=1, type='journal', status='under-review',
            title='Enhancing Multi-Class Satellite Image Classification with MRCL-ELM: A Hybrid Explainable Deep Learning Approach',
            authors='Md Ashik Ahmmed; Rashel Mahmud Rabbi; Md Shafiuzzaman',
            venue='Neural Computing and Applications',
            year='',
            abstract='Designed a novel hybrid deep learning approach to classify images from satellites with 98.33% accuracy on EuroSAT and 98.10% accuracy on UC Merced datasets. Integrated LIME and SHAP for explainable AI, and deployed the system as a real-time web application.',
            doi_link='', pdf_link='',
        )
        models.Publication.objects.create(
            order=2, type='thesis', status='completed',
            title='HYBSWINEFF: Hybrid CNN-Transformer Fusion for Binary and Multi-Stage Blood Cell Cancer Classification',
            authors='Rashel Mahmud Rabbi',
            venue='B.Sc. Thesis, Department of CSE, North Bengal International University',
            year='2025',
            abstract='A lightweight hybrid CNN-Transformer architecture for automated, interpretable, multi-stage acute lymphoblastic leukemia (ALL) classification, combining an EfficientNetV2-RW-T backbone with a Swin Transformer Tiny, achieving 99.69% binary accuracy and 100% staging accuracy.',
            doi_link='', pdf_link='',
        )
        self.stdout.write('  Publications seeded.')

    # ── projects ─────────────────────────────────────────────────────────────
    def seed_projects(self):
        if self._skip('Projects', models.Project.objects.all()):
            return
        models.Project.objects.all().delete()
        rows = [
            dict(order=0, category='thesis', featured=True,
                 title='HYBSWINEFF: Hybrid CNN-Transformer Fusion for Binary and Multi-Stage Blood Cell Cancer Classification',
                 description='Created a hybrid CNN-Transformer model that performs binary and multi-stage leukemia classification of peripheral blood smear images. Incorporates Swin Transformer with CNN feature fusion and explainable AI methods (Grad-CAM, LIME) to make predictions interpretable for clinical use.',
                 tech='PyTorch, Swin Transformer, CNN, Grad-CAM, LIME, OpenCV', year='2025',
                 github_link='https://github.com/rashelmahmudrabbi/HybSwinEff', paper_link=''),
            dict(order=1, category='research', featured=False,
                 title='MRCL-ELM – Multi-Class Satellite Image Classifier',
                 description='Novel hybrid deep learning approach for satellite image classification achieving 98.33% accuracy on EuroSAT and 98.10% on UC Merced. Integrates LIME and SHAP for explainability; deployed as a real-time web application. Submitted to a Q1 journal.',
                 tech='PyTorch, LIME, SHAP, Flask, EuroSAT', year='2024',
                 github_link='https://github.com/rashelmahmudrabbi/MRCL-ELM', paper_link=''),
            dict(order=2, category='research', featured=False,
                 title='SatelliteNet – CNN-LSTM Land-Use Classifier',
                 description='Hybrid CNN-LSTM network for land-use classification on EuroSAT achieving 98.30% accuracy. Generates LIME-based explainability visualisations. Published and presented at IEEE QPAIN 2025.',
                 tech='TensorFlow, Keras, LIME, NumPy, Google Colab', year='2024',
                 github_link='https://github.com/rashelmahmudrabbi/CNN-LSTM', paper_link=''),
            dict(order=3, category='research', featured=False,
                 title='NeuroFusion – Brain Tumor Detection',
                 description='Hybrid CNN-Transformer framework for brain tumor detection from MRI images. Combines MobileNetV3 with channel attention and Transformer encoder architectures, using advanced augmentation and optimisation to enhance generalisation.',
                 tech='PyTorch, MobileNetV3, Transformer, OpenCV, scikit-learn', year='2026',
                 github_link='https://github.com/rashelmahmudrabbi', paper_link=''),
            dict(order=4, category='development', featured=False,
                 title='Academic Portfolio Website',
                 description='Designed and implemented this responsive academic portfolio using Django and Bootstrap, with a dynamic content management system for easy content updates.',
                 tech='Django, Bootstrap 5, SQLite, HTML/CSS/JS', year='2025',
                 github_link='https://github.com/rashelmahmudrabbi', paper_link=''),
            dict(order=5, category='development', featured=False,
                 title='RentalHub – E-commerce Web App',
                 description='Responsive rental marketplace with user authentication, interactive UI, and full listing, browsing, and management of properties and items for rent.',
                 tech='Django, Tailwind CSS, SQLite, REST API', year='2024',
                 github_link='https://github.com/rashelmahmudrabbi', paper_link=''),
            dict(order=6, category='development', featured=False,
                 title='OUR RAJSHAHI – Regional Info Platform',
                 description='Comprehensive info and tour platform for the Rajshahi region with categorised local services, tourist attractions, emergency contacts, authentication, interactive navigation, and feedback modules.',
                 tech='Django, Bootstrap, SQLite, Google AdSense', year='2023',
                 github_link='https://github.com/rashelmahmudrabbi', paper_link=''),
        ]
        for row in rows:
            models.Project.objects.create(**row)
        self.stdout.write('  Projects seeded.')

    # ── certifications ───────────────────────────────────────────────────────
    def seed_certifications(self):
        if self._skip('Certifications', models.Certification.objects.all()):
            return
        models.Certification.objects.all().delete()
        models.Certification.objects.create(
            order=0, title='Data Science Math Skills', issuer='Coursera', year='2024',
            image='media/certifications/images/Coursera__Data_Science_Math_Skills_7HHNEO5MT8WO_pages-to-jpg-0001.jpg',
            verify_link='https://www.coursera.org/account/accomplishments/verify/7HHNEO5MT8WO',
            pdf_link='media/certifications/pdfs/Coursera__Data_Science_Math_Skills_7HHNEO5MT8WO.pdf',
        )
        models.Certification.objects.create(
            order=1, title='Python Basics', issuer='Coursera', year='2025',
            image='media/certifications/images/Coursera_Python_Basics_KJ1TIFBGN6W3_pages-to-jpg-0001.jpg',
            verify_link='https://coursera.org/verify/KJ1TIFBGN6W3',
            pdf_link='media/certifications/pdfs/Coursera_Python_Basics_KJ1TIFBGN6W3.pdf',
        )
        self.stdout.write('  Certifications seeded.')

    # ── awards ───────────────────────────────────────────────────────────────
    def seed_awards(self):
        if self._skip('Awards', models.Award.objects.all()):
            return
        models.Award.objects.all().delete()
        models.Award.objects.create(order=0, title='2nd Runner-Up, IEEE ProCon App Idea Competition', org='IEEE', year='2025', image='media/awards/Idea_with_Poster_Presentation.jpg')
        models.Award.objects.create(order=1, title='1st Position, Research Olympiad – Rajshahi Regional', org='Rajshahi University Research Society (RURS)', year='2024', image='media/awards/Research_Olympiad.jpg')
        self.stdout.write('  Awards seeded.')

    # ── activities ───────────────────────────────────────────────────────────
    def seed_activities(self):
        if self._skip('Activities', models.Activity.objects.all()):
            return
        models.Activity.objects.all().delete()
        for i, text in enumerate([
            'President, Computer Society – NBIU',
            'Participation in research seminars and higher study camps',
            'Active involvement in tech competitions and academic events',
        ]):
            models.Activity.objects.create(order=i, text=text)
        self.stdout.write('  Activities seeded.')

    # ── gallery ──────────────────────────────────────────────────────────────
    def seed_gallery(self):
        if self._skip('Gallery', models.GalleryEvent.objects.all()):
            return
        models.GalleryEvent.objects.all().delete()
        ev1 = models.GalleryEvent.objects.create(order=0, title='IEEE ProCon App Idea Competition', year='2025')
        models.GalleryPhoto.objects.create(event=ev1, order=0, src='media/gallery/ProCON/Group Photo.jpg', caption='Group Photo')
        models.GalleryPhoto.objects.create(event=ev1, order=1, src='media/gallery/ProCON/Award Ceremony.jpg', caption='Award Ceremony')
        ev2 = models.GalleryEvent.objects.create(order=1, title='Research Olympiad – Rajshahi Regional', year='2024')
        models.GalleryPhoto.objects.create(event=ev2, order=0, src='media/gallery/Research-Olympiad/Stage Award.jpg', caption='Stage Award')
        models.GalleryPhoto.objects.create(event=ev2, order=1, src='media/gallery/Research-Olympiad/Cover.jpg', caption='Cover')
        self.stdout.write('  Gallery seeded.')

    # ── courses ──────────────────────────────────────────────────────────────
    def seed_courses(self):
        if self._skip('Courses', models.Course.objects.all()):
            return
        models.Course.objects.all().delete()
        models.Course.objects.create(order=0, name='CSE-22', institution='NBIU, Rajshahi', period='2023 – 2024', role='Teaching Assistant')
        self.stdout.write('  Courses seeded.')

    # ── blog ─────────────────────────────────────────────────────────────────
    def seed_blog(self):
        if self._skip('Blog posts', models.BlogPost.objects.all()):
            return
        models.BlogPost.objects.all().delete()
        rows = [
            dict(order=0, featured=True, title='Why Explainability Matters in Medical AI — and How LIME Helps',
                 slug='explainability-medical-ai-lime', date='March 2025', read_time='8 min read', category='Explainable AI',
                 excerpt='When an AI model tells a doctor a lesion is malignant, "trust me" isn\'t good enough. I explore how LIME bridges the gap between black-box accuracy and clinical trust in skin lesion classification.',
                 content=''),
            dict(order=1, featured=False, title='Transfer Learning on Satellite Imagery: Lessons from EuroSAT',
                 slug='transfer-learning-eurosat', date='Jan 2025', read_time='6 min read', category='Computer Vision',
                 excerpt='What I learned training ResNet-50 on the EuroSAT dataset — from data augmentation strategies to achieving 96.4% accuracy on 10 land-use categories.',
                 content=''),
            dict(order=2, featured=False, title='LSTM for ECG Signal Analysis: A Practical Guide',
                 slug='lstm-ecg-signal-analysis', date='Nov 2024', read_time='5 min read', category='Deep Learning',
                 excerpt='A walkthrough of building an LSTM-based arrhythmia detector from scratch using the MIT-BIH dataset, including preprocessing ECG signals with the Wfdb library.',
                 content=''),
            dict(order=3, featured=False, title='How I Won 1st at the Research Olympiad — and What I Learned',
                 slug='research-olympiad-win', date='Sep 2024', read_time='4 min read', category='Academic Life',
                 excerpt='My experience presenting at the Rajshahi Regional Research Olympiad, the feedback I received, and how it shaped my thinking on communicating research to non-technical audiences.',
                 content=''),
            dict(order=4, featured=False, title='My 2024 Deep Learning Paper Reading List',
                 slug='2024-paper-reading-list', date='Jul 2024', read_time='7 min read', category='Resources',
                 excerpt='A curated list of the 10 most impactful papers I read this year in Computer Vision and Medical AI, with short summaries and why each one matters.',
                 content=''),
        ]
        for row in rows:
            models.BlogPost.objects.create(**row)
        self.stdout.write('  Blog posts seeded.')

    # ── references ───────────────────────────────────────────────────────────
    def seed_references(self):
        if self._skip('References', models.Reference.objects.all()):
            return
        models.Reference.objects.all().delete()
        models.Reference.objects.create(order=0, name='Md. Emdadul Haque', role='Lecturer & Head, Department of CSE', org='North Bengal International University', note='', phone='+8801773-897585', email='haque.emdadul.one5@gmail.com')
        models.Reference.objects.create(order=1, name='Md. Shafiuzzaman', role='Lecturer, Department of CSE', org='North Bengal International University', note='Research Supervisor', phone='+8801780-165924', email='shafiuzzaman.ruet@gmail.com')
        models.Reference.objects.create(order=2, name='Saifur Rahman', role='Lecturer, Department of CSE', org='North Bengal International University', note='Thesis External Examiner', phone='+8801738-663624', email='saifur.naim30@gmail.com')
        self.stdout.write('  References seeded.')
