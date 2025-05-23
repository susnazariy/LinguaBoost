""" Django database models """

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not username:
            raise ValueError('User must have a username!')
        if not email:
            raise ValueError('User must have an email address!')

        username = self.model.normalize_username(username)
        email = self.normalize_email(email)

        user = self.model(username=username,
                          email=email,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not username:
            raise ValueError('User must have a username!')
        if not email:
            raise ValueError('User must have an email address!')

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = [('Адміністратор', 'Адміністратор'),
                            ('Викладач', 'Викладач'),
                            ('Учень', 'Учень')]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='Учень')
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = PhoneNumberField(null=False, blank=True, unique=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True, unique=False)
    image = models.ImageField(null=True, blank=True, upload_to='images/profile_images/',
                              default='images/profile_images/no_photo.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        if not self.account_type:
            self.account_type = 'Учень'
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class WebsiteInformation(models.Model):
    website_name = models.CharField(max_length=30)
    website_address = models.CharField(max_length=150)
    google_map = models.TextField()
    website_phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    website_email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    website_facebook = models.TextField()
    website_linkedin = models.TextField()
    website_instagram = models.TextField()

    class Meta:
        db_table = 'website_information'
        ordering = ['website_name']
        managed = True
        verbose_name = 'Website information'
        verbose_name_plural = 'Website information'

    def __str__(self):
        return f"{str(self.website_name)}"


class Course(models.Model):
    course_name = models.CharField(max_length=255)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses_info')
    creation_date = models.DateField(default=timezone.now)
    course_description = models.TextField()
    course_image = models.ImageField(null=True, blank=True, upload_to='images/course_images/',
                              default='images/course_images/no_photo.jpg')
    DIFFICULT_LEVEL_CHOICES = [('★★★', '★★★'), ('★★', '★★'), ('★', '★')]
    difficult_level = models.CharField(max_length=3, choices=DIFFICULT_LEVEL_CHOICES, default='★')

    def save(self, *args, **kwargs):
        if not self.course_image:
            self.course_image = 'images/course_images/no_photo.jpg'
        super(Course, self).save(*args, **kwargs)

    class Meta:
        db_table = 'courses'
        ordering = ['creator', 'id']
        managed = True
        verbose_name = 'Courses'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{str(self.course_name)} ({str(self.creator)})"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons_info')
    lesson_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'lessons'
        ordering = ['course', 'id']
        managed = True
        verbose_name = 'Lessons'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f"{str(self.course)} ({str(self.lesson_name)})"


class StudentApplication(models.Model):
    application_datetime = models.DateTimeField(null=True, default=timezone.now)
    course =  models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_applications_info')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_applications_info')
    STATUS_CHOICES = [('В обробці', 'В обробці'), ('Підтверджено', 'Підтверджено'),
                      ('Відхилено', 'Відхилено')]

    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В обробці')

    class Meta:
        db_table = 'student_applications'
        ordering = ['application_status', '-application_datetime']
        managed = True
        verbose_name = 'Student applications'
        verbose_name_plural = 'Student applications'

    def __str__(self):
        return (f"Статус: {str(self.application_status)} {str(self.application_datetime)[:19]} "
                f"({str(self.student.last_name)} {str(self.student.first_name)} - {str(self.course)})")


class StudentCourse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_courses_info')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_courses_info')

    class Meta:
        db_table = 'student_courses'
        ordering = ['student']
        managed = True
        verbose_name = 'Student courses'
        verbose_name_plural = 'Student courses'

    def __str__(self):
        return f"{str(self.student)} - {str(self.course)}"


class OneManyTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='one_many_tasks_info')
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    first_wrong_answer = models.CharField(max_length=255)
    second_wrong_answer = models.CharField(max_length=255)
    third_wrong_answer = models.CharField(max_length=255)

    class Meta:
        db_table = 'one_many_tasks'
        ordering = ['id']
        managed = True
        verbose_name = 'One many tasks'
        verbose_name_plural = 'One many tasks'

    def __str__(self):
        return f"{str(self.lesson)} - {str(self.text)}"


class FixSentenceTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='fix_sentence_tasks_info')
    correct_text = models.TextField()
    bad_text = models.TextField()

    class Meta:
        db_table = 'fix_sentence_tasks'
        ordering = ['id']
        managed = True
        verbose_name = 'Fix sentence tasks'
        verbose_name_plural = 'Fix sentence tasks'

    def __str__(self):
        return f"{str(self.lesson)} - {str(self.correct_text)}"


class TranslateWordTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='translate_word_tasks_info')
    english_word = models.CharField(max_length=255)
    ukrainian_word = models.CharField(max_length=255)

    class Meta:
        db_table = 'translate_word_tasks'
        ordering = ['id']
        managed = True
        verbose_name = 'Translate word tasks'
        verbose_name_plural = 'Translate word tasks'

    def __str__(self):
        return f"{str(self.lesson)} ({str(self.english_word)} - {str(self.ukrainian_word)})"


class SequenceTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sequence_tasks_info')
    sequence_text = models.TextField()

    class Meta:
        db_table = 'sequence_tasks'
        ordering = ['id']
        managed = True
        verbose_name = 'Sequence tasks'
        verbose_name_plural = 'Sequence tasks'

    def __str__(self):
        return f"{str(self.lesson)} ({str(self.sequence_text)})"


class AccordanceTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='accordance_tasks_info')

    class Meta:
        db_table = 'accordance_tasks'
        ordering = ['id']
        managed = True
        verbose_name = 'Accordance tasks'
        verbose_name_plural = 'Accordance tasks'

    def __str__(self):
        return f"Task - {str(self.id)} ({str(self.lesson)})"


class AccordanceTaskVariant(models.Model):
    accordance_task = models.ForeignKey(AccordanceTask, on_delete=models.CASCADE, related_name='accordance_task_variants_info')
    first_variant = models.CharField(max_length=255)
    second_variant = models.CharField(max_length=255)

    class Meta:
        db_table = 'accordance_task_variants'
        ordering = ['id']
        managed = True
        verbose_name = 'Accordance task variants'
        verbose_name_plural = 'Accordance task variants'

    def __str__(self):
        return f"{str(self.accordance_task)} ({str(self.first_variant)} - {str(self.second_variant)})"


class DiscussionExercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='discussion_exercises_info')
    image = models.ImageField(null=True, blank=True, upload_to='images/exercise_images/',
                                     default='images/exercise_images/no_photo.jpg')
    first_question = models.CharField()
    second_question = models.CharField()
    third_question = models.CharField()
    fourth_question = models.CharField()

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'images/exercise_images/no_photo.jpg'
        super(DiscussionExercise, self).save(*args, **kwargs)

    class Meta:
        db_table = 'discussion_exercises'
        ordering = ['id']
        managed = True
        verbose_name = 'Discussion exercises'
        verbose_name_plural = 'Discussion exercises'

    def __str__(self):
        return f"{str(self.id)} ({str(self.lesson)})"


class ReadingExercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reading_exercises_info')
    image = models.ImageField(null=True, blank=True, upload_to='images/exercise_images/',
                                     default='images/exercise_images/no_photo.jpg')
    text = models.TextField()

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'images/exercise_images/no_photo.jpg'
        super(ReadingExercise, self).save(*args, **kwargs)

    class Meta:
        db_table = 'reading_exercises'
        ordering = ['id']
        managed = True
        verbose_name = 'Reading exercises'
        verbose_name_plural = 'Reading exercises'

    def __str__(self):
        return f"{str(self.id)} ({str(self.lesson)})"


class ListeningExercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='listening_exercises_info')
    name = models.CharField()
    audio = models.FileField(null=True, blank=True, upload_to='audio/', default='audio/no_audio.mp3')
    text = models.TextField()

    def save(self, *args, **kwargs):
        if not self.audio:
            self.audio = 'audio/no_audio.mp3'
        super(ListeningExercise, self).save(*args, **kwargs)

    class Meta:
        db_table = 'listening_exercises'
        ordering = ['id']
        managed = True
        verbose_name = 'Listening exercises'
        verbose_name_plural = 'Listening exercises'

    def __str__(self):
        return f"{str(self.id)} ({str(self.lesson)})"


class VocabularyExercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='vocabulary_exercises_info')

    class Meta:
        db_table = 'vocabulary_exercises'
        ordering = ['id']
        managed = True
        verbose_name = 'Vocabulary exercises'
        verbose_name_plural = 'Vocabulary exercises'

    def __str__(self):
        return f"{str(self.id)} ({str(self.lesson)})"


class VocabularyWord(models.Model):
    vocabulary_exercise = models.ForeignKey(VocabularyExercise, on_delete=models.CASCADE, related_name='vocabulary_words_info')
    english_word = models.CharField(max_length=255)
    ukrainian_word = models.CharField(max_length=255)
    transcription = models.CharField(max_length=255)

    class Meta:
        db_table = 'vocabulary_words'
        ordering = ['id']
        managed = True
        verbose_name = 'Vocabulary words'
        verbose_name_plural = 'Vocabulary words'

    def __str__(self):
        return f"{str(self.id)} ({str(self.vocabulary_exercise)})"


class RulesExercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='rules_exercises_info')
    image = models.ImageField(null=True, blank=True, upload_to='images/exercise_images/',
                                     default='images/exercise_images/no_photo.jpg')
    text = models.TextField()

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'images/exercise_images/no_photo.jpg'
        super(RulesExercise, self).save(*args, **kwargs)

    class Meta:
        db_table = 'rules_exercises'
        ordering = ['id']
        managed = True
        verbose_name = 'Rules exercises'
        verbose_name_plural = 'Rules exercises'

    def __str__(self):
        return f"{str(self.id)} ({str(self.lesson)})"


class LessonTestResult(models.Model):
    test_datetime = models.DateTimeField(null=True, default=timezone.now)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_test_results')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_test_results')
    number_of_tests = models.PositiveIntegerField()
    test_result = models.PositiveIntegerField()
    is_successfully_passed = models.BooleanField()

    class Meta:
        db_table = 'lesson_test_results'
        ordering = ['id']
        managed = True
        verbose_name = 'Lesson test results'
        verbose_name_plural = 'Lesson test results'

    def __str__(self):
        return (f"{str(self.test_datetime)} ({str(self.lesson)}) ({str(self.student)}) "
                f"{str(self.test_result)}/{str(self.number_of_tests)}")


class CourseFinalTestResult(models.Model):
    test_datetime = models.DateTimeField(null=True, default=timezone.now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_final_test_results')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_final_test_results')
    number_of_tests = models.PositiveIntegerField()
    test_result = models.PositiveIntegerField()
    is_successfully_passed = models.BooleanField()

    class Meta:
        db_table = 'course_final_test_results'
        ordering = ['id']
        managed = True
        verbose_name = 'Course final test results'
        verbose_name_plural = 'Course final test results'

    def __str__(self):
        return (f"{str(self.test_datetime)} ({str(self.course)}) ({str(self.student)}) "
                f"{str(self.test_result)}/{str(self.number_of_tests)}")
