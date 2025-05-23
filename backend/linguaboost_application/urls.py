""" URL configuration for linguaboost project """

from django.urls import path, include
from .views import (Registration, UserProfileView, UpdateProfileView, ImageUploadView, HomePageView, CourseFullDataView,
                    CourseAndLessonsDataView, AddNewCourse, SelectedCourseData, UpdateCourse, DeleteCourse,
                    AddNewLesson, DeleteLesson, UpdateLesson, LessonsListView, AddStudentApplication, ChangeApplicationStatus,
                    StudentApplicationsInfo, AddStudentToCourse, ProfileStudentCoursesView, ProfileTeacherCoursesView, TasksListView,
                    CourseFinalRandomTasksList, AddOneManyTask, AddFixSentenceTask, AddTranslateWordTask, AddSequenceTask,
                    AddAccordanceTask, SelectedOneManyTaskData, SelectedFixSentenceTaskData, SelectedTranslateWordTaskData,
                    SelectedSequenceTaskData, SelectedAccordanceTaskData, UpdateOneManyTask, UpdateFixSentenceTask,
                    UpdateTranslateWordTask, UpdateSequenceTask, UpdateAccordanceTask, DeleteOneManyTask,
                    DeleteFixSentenceTask, DeleteTranslateWordTask, DeleteSequenceTask, DeleteAccordanceTask, ExercisesListView,
                    AddDiscussionExercise, AddReadingExercise, AddListeningExercise, AddVocabularyExercise, AddRulesExercise,
                    SelectedDiscussionExerciseData, SelectedReadingExerciseData, SelectedListeningExerciseData,
                    SelectedVocabularyExerciseData, SelectedRulesExerciseData, UpdateDiscussionExercise,
                    UpdateReadingExercise, UpdateListeningExercise, UpdateVocabularyExercise, UpdateRulesExercise,
                    DeleteDiscussionExercise, DeleteReadingExercise, DeleteListeningExercise, DeleteVocabularyExercise,
                    DeleteRulesExercise, AddLessonTestResult, LessonTestResults, AddCourseFinalTestResult,
                    CourseDataAndFinalTestResults)

urlpatterns = [
    path('registration/', Registration.as_view()),
    path('authorization/', include('djoser.urls')),
    path('authorization/', include('djoser.urls.authtoken')),
    path('profile/', UserProfileView.as_view()),
    path('update_profile/', UpdateProfileView.as_view()),
    path('image_upload/', ImageUploadView.as_view()),

    path('home/', HomePageView.as_view()),
    path('courses_full_data/', CourseFullDataView.as_view()),
    path('course_and_lessons_data/', CourseAndLessonsDataView.as_view()),
    path('add_course/', AddNewCourse.as_view()),
    path('selected_course_data/', SelectedCourseData.as_view()),
    path('update_course/', UpdateCourse.as_view()),
    path('delete_course/', DeleteCourse.as_view()),
    path('add_lesson/', AddNewLesson.as_view()),
    path('delete_lesson/', DeleteLesson.as_view()),
    path('update_lesson/', UpdateLesson.as_view()),
    path('lessons_list/', LessonsListView.as_view()),
    path('add_student_application/', AddStudentApplication.as_view()),
    path('change_application_status/', ChangeApplicationStatus.as_view()),
    path('student_applications_data/', StudentApplicationsInfo.as_view()),
    path('add_student_to_course/', AddStudentToCourse.as_view()),
    path('profile_student_courses/', ProfileStudentCoursesView.as_view()),
    path('profile_teacher_courses/', ProfileTeacherCoursesView.as_view()),


    path('tasks_list/', TasksListView.as_view()),
    path('course_final_random_tasks_list/', CourseFinalRandomTasksList.as_view()),

    path('add_one_many_task/', AddOneManyTask.as_view()),
    path('add_fix_sentence_task/', AddFixSentenceTask.as_view()),
    path('add_translate_word_task/', AddTranslateWordTask.as_view()),
    path('add_sequence_task/', AddSequenceTask.as_view()),
    path('add_accordance_task/', AddAccordanceTask.as_view()),

    path('selected_one_many_task_data/', SelectedOneManyTaskData.as_view()),
    path('selected_fix_sentence_task_data/', SelectedFixSentenceTaskData.as_view()),
    path('selected_translate_word_task_data/', SelectedTranslateWordTaskData.as_view()),
    path('selected_sequence_task_data/', SelectedSequenceTaskData.as_view()),
    path('selected_accordance_task_data/', SelectedAccordanceTaskData.as_view()),

    path('update_one_many_task/', UpdateOneManyTask.as_view()),
    path('update_fix_sentence_task/', UpdateFixSentenceTask.as_view()),
    path('update_translate_word_task/', UpdateTranslateWordTask.as_view()),
    path('update_sequence_task/', UpdateSequenceTask.as_view()),
    path('update_accordance_task/', UpdateAccordanceTask.as_view()),

    path('delete_one_many_task/', DeleteOneManyTask.as_view()),
    path('delete_fix_sentence_task/', DeleteFixSentenceTask.as_view()),
    path('delete_translate_word_task/', DeleteTranslateWordTask.as_view()),
    path('delete_sequence_task/', DeleteSequenceTask.as_view()),
    path('delete_accordance_task/', DeleteAccordanceTask.as_view()),


    path('exercises_list/', ExercisesListView.as_view()),

    path('add_discussion_exercise/', AddDiscussionExercise.as_view()),
    path('add_reading_exercise/', AddReadingExercise.as_view()),
    path('add_listening_exercise/', AddListeningExercise.as_view()),
    path('add_vocabulary_exercise/', AddVocabularyExercise.as_view()),
    path('add_rules_exercise/', AddRulesExercise.as_view()),

    path('selected_discussion_exercise_data/', SelectedDiscussionExerciseData.as_view()),
    path('selected_reading_exercise_data/', SelectedReadingExerciseData.as_view()),
    path('selected_listening_exercise_data/', SelectedListeningExerciseData.as_view()),
    path('selected_vocabulary_exercise_data/', SelectedVocabularyExerciseData.as_view()),
    path('selected_rules_exercise_data/', SelectedRulesExerciseData.as_view()),

    path('update_discussion_exercise/', UpdateDiscussionExercise.as_view()),
    path('update_reading_exercise/', UpdateReadingExercise.as_view()),
    path('update_listening_exercise/', UpdateListeningExercise.as_view()),
    path('update_vocabulary_exercise/', UpdateVocabularyExercise.as_view()),
    path('update_rules_exercise/', UpdateRulesExercise.as_view()),

    path('delete_discussion_exercise/', DeleteDiscussionExercise.as_view()),
    path('delete_reading_exercise/', DeleteReadingExercise.as_view()),
    path('delete_listening_exercise/', DeleteListeningExercise.as_view()),
    path('delete_vocabulary_exercise/', DeleteVocabularyExercise.as_view()),
    path('delete_rules_exercise/', DeleteRulesExercise.as_view()),


    path('add_lesson_test_result/', AddLessonTestResult.as_view()),
    path('lesson_test_results/', LessonTestResults.as_view()),
    path('add_course_final_test_result/', AddCourseFinalTestResult.as_view()),
    path('course_data_and_final_test_results/', CourseDataAndFinalTestResults.as_view()),
]
