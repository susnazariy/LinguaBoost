""" Rest Framework JSON serializers """

from rest_framework.serializers import ModelSerializer
from .models import (WebsiteInformation, Course, CustomUser, Lesson, StudentCourse, StudentApplication, OneManyTask,
                     FixSentenceTask, TranslateWordTask, SequenceTask, AccordanceTask, AccordanceTaskVariant,
                     DiscussionExercise, ReadingExercise, ListeningExercise, VocabularyExercise, VocabularyWord, RulesExercise,
                     LessonTestResult, CourseFinalTestResult)


class WebsiteInfoSerializer(ModelSerializer):
    class Meta:
        model = WebsiteInformation
        fields = ['website_name',
                  'website_address',
                  'google_map',
                  'website_phone_number',
                  'website_email',
                  'website_facebook',
                  'website_linkedin',
                  'website_instagram']


class CoursesMainInfoSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id',
                  'course_name',
                  'creation_date',
                  'course_image',
                  'difficult_level']


class CoursesMainSerializer(ModelSerializer):
    courses_info = CoursesMainInfoSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['last_name',
                  'first_name',
                  'courses_info']


class SelectedCourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = ['id',
                  'course_name',
                  'course_description',
                  'course_image',
                  'difficult_level']


class LessonsInfoSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id',
                  'lesson_name']


class CoursesDescriptionSerializer(ModelSerializer):
    lessons_info = LessonsInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id',
                  'course_name',
                  'course_description',
                  'lessons_info']


class StudentCoursesSerializer(ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ['student',
                'course']


class StudentApplicationsSerializer(ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = ['id',
                  'application_datetime',
                  'course',
                  'student',
                  'application_status']


class SelectedOneManyTaskSerializer(ModelSerializer):
    class Meta:
        model = OneManyTask
        fields = ['id',
                  'text',
                  'correct_answer',
                  'first_wrong_answer',
                  'second_wrong_answer',
                  'third_wrong_answer']


class SelectedFixSentenceTaskSerializer(ModelSerializer):
    class Meta:
        model = FixSentenceTask
        fields = ['id',
                  'correct_text',
                  'bad_text']


class SelectedTranslateWordTaskSerializer(ModelSerializer):
    class Meta:
        model = TranslateWordTask
        fields = ['id',
                'english_word',
                'ukrainian_word']


class SelectedSequenceTaskSerializer(ModelSerializer):
    class Meta:
        model = SequenceTask
        fields = ['id',
                'sequence_text']


class SelectedAccordanceTaskVariantsSerializer(ModelSerializer):
    class Meta:
        model = AccordanceTaskVariant
        fields = ['id',
                  'first_variant',
                  'second_variant']


class SelectedAccordanceTaskSerializer(ModelSerializer):
    accordance_task_variants_info = SelectedAccordanceTaskVariantsSerializer(many=True, read_only=True)

    class Meta:
        model = AccordanceTask
        fields = ['id',
                  'accordance_task_variants_info']


class TasksListSerializer(ModelSerializer):
    one_many_tasks_info = SelectedOneManyTaskSerializer(many=True, read_only=True)
    fix_sentence_tasks_info = SelectedFixSentenceTaskSerializer(many=True, read_only=True)
    translate_word_tasks_info = SelectedTranslateWordTaskSerializer(many=True, read_only=True)
    sequence_tasks_info = SelectedSequenceTaskSerializer(many=True, read_only=True)
    accordance_tasks_info = SelectedAccordanceTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id',
                  'one_many_tasks_info',
                  'fix_sentence_tasks_info',
                  'translate_word_tasks_info',
                  'sequence_tasks_info',
                  'accordance_tasks_info']


class AllCourseTasksListSerializer(ModelSerializer):
    lessons_info = TasksListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id',
                'course_name',
                'lessons_info']


class SelectedDiscussionExerciseSerializer(ModelSerializer):
    class Meta:
        model = DiscussionExercise
        fields = ['id',
                  'image',
                  'first_question',
                  'second_question',
                  'third_question',
                  'fourth_question']


class SelectedReadingExerciseSerializer(ModelSerializer):
    class Meta:
        model = ReadingExercise
        fields = ['id',
                  'image',
                  'text']


class SelectedListeningExerciseSerializer(ModelSerializer):
    class Meta:
        model = ListeningExercise
        fields = ['id',
                  'name',
                  'audio',
                  'text']


class SelectedVocabularyWordsSerializer(ModelSerializer):
    class Meta:
        model = VocabularyWord
        fields = ['id',
                  'english_word',
                  'ukrainian_word',
                  'transcription']


class SelectedVocabularyExerciseSerializer(ModelSerializer):
    vocabulary_words_info = SelectedVocabularyWordsSerializer(many=True, read_only=True)

    class Meta:
        model = VocabularyExercise
        fields = ['id',
                  'vocabulary_words_info']


class SelectedRulesExerciseSerializer(ModelSerializer):
    class Meta:
        model = RulesExercise
        fields = ['id',
                  'image',
                  'text']


class ExercisesListSerializer(ModelSerializer):
    discussion_exercises_info = SelectedDiscussionExerciseSerializer(many=True, read_only=True)
    reading_exercises_info = SelectedReadingExerciseSerializer(many=True, read_only=True)
    listening_exercises_info = SelectedListeningExerciseSerializer(many=True, read_only=True)
    vocabulary_exercises_info = SelectedVocabularyExerciseSerializer(many=True, read_only=True)
    rules_exercises_info = SelectedRulesExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id',
                  'discussion_exercises_info',
                  'reading_exercises_info',
                  'listening_exercises_info',
                  'vocabulary_exercises_info',
                  'rules_exercises_info']


class LessonTestResultsSerializer(ModelSerializer):
    class Meta:
        model = LessonTestResult
        fields = ['test_datetime',
                  'student',
                  'number_of_tests',
                  'test_result',
                  'is_successfully_passed']


class CourseFinalTestResultsSerializer(ModelSerializer):
    class Meta:
        model = CourseFinalTestResult
        fields = ['test_datetime',
                  'number_of_tests',
                  'test_result',
                  'is_successfully_passed']


class LessonsAndLessonTestResultsSerializer(ModelSerializer):
    lesson_test_results = LessonTestResultsSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id',
                  'lesson_test_results']
