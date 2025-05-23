""" Application views"""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from random import sample
from .models import (CustomUser, WebsiteInformation, Course, Lesson, StudentApplication, StudentCourse, OneManyTask,
                     FixSentenceTask, TranslateWordTask, SequenceTask, AccordanceTask, AccordanceTaskVariant,
                     DiscussionExercise, ReadingExercise, ListeningExercise, VocabularyExercise, VocabularyWord, RulesExercise,
                     LessonTestResult, CourseFinalTestResult)
from .serializer import (WebsiteInfoSerializer, CoursesMainSerializer, CoursesDescriptionSerializer, SelectedCourseSerializer,
                         StudentCoursesSerializer, StudentApplicationsSerializer, CoursesMainInfoSerializer, LessonsInfoSerializer,
                         TasksListSerializer, AllCourseTasksListSerializer, SelectedOneManyTaskSerializer, SelectedFixSentenceTaskSerializer,
                         SelectedTranslateWordTaskSerializer, SelectedSequenceTaskSerializer, SelectedAccordanceTaskSerializer,
                         ExercisesListSerializer, SelectedDiscussionExerciseSerializer, SelectedReadingExerciseSerializer,
                         SelectedListeningExerciseSerializer, SelectedVocabularyExerciseSerializer, SelectedRulesExerciseSerializer,
                         LessonTestResultsSerializer, CourseFinalTestResultsSerializer, LessonsAndLessonTestResultsSerializer)


class Registration(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        try:
            user_data = request.data
            username = user_data.get("username")
            password = user_data.get("password")
            account_type = user_data.get("account_type")
            first_name = user_data.get("first_name")
            last_name = user_data.get("last_name")
            patronymic = user_data.get("patronymic")
            phone_number = user_data.get("phone_number")
            email = user_data.get("email")
            birthday = user_data.get("birthday")

            if CustomUser.objects.filter(username=username).exists():
                raise NameError
            elif CustomUser.objects.filter(email=email).exists():
                raise ValueError
            elif CustomUser.objects.filter(phone_number=phone_number).exists():
                raise KeyError
            else:
                user = CustomUser.objects.create_user(username=username,
                                                      account_type=account_type,
                                                      password=password,
                                                      first_name=first_name,
                                                      last_name=last_name,
                                                      patronymic=patronymic,
                                                      phone_number=phone_number,
                                                      email=email,
                                                      birthday=birthday,
                                                      image='images/profile_images/no_photo.jpg',
                                                      is_active=True,
                                                      is_staff=False,
                                                      is_superuser=False)
                user.set_password(password)
                user.save()

                print(f'User profile `{username}` has been created!')
                return Response(f"Message: user register is success!")

        except NameError:
            return Response(f"Error: username is already taken!")
        except ValueError:
            return Response(f"Error: email is already taken!")
        except KeyError:
            return Response(f"Error: phone number is already taken!")


class UpdateProfileView(APIView):

    @staticmethod
    def post(request):
        try:
            update_data = request.data

            new_username = update_data.get("username")
            new_first_name = update_data.get("first_name")
            new_last_name = update_data.get("last_name")
            new_patronymic = update_data.get("patronymic")
            new_email = update_data.get("email")
            new_birthday = update_data.get("birthday")
            new_phone_number = update_data.get("phone_number")
            current_username = update_data.get("current_username")  # If True, NameError don't raise
            current_email = update_data.get("current_email")  # If True, ValueError don't raise
            current_phone_number = update_data.get("current_phone_number")  # If True, KeyError don't raise

            if current_username is not True and CustomUser.objects.filter(username=new_username).exists():
                raise NameError
            elif current_email is not True and CustomUser.objects.filter(email=new_email).exists():
                raise ValueError
            elif (current_phone_number is not True and
                  CustomUser.objects.filter(phone_number=new_phone_number).exists()):
                raise KeyError

            request.user.username = new_username
            request.user.first_name = new_first_name
            request.user.last_name = new_last_name
            request.user.patronymic = new_patronymic
            request.user.email = new_email
            request.user.phone_number = new_phone_number
            request.user.birthday = new_birthday
            request.user.save()

        except NameError:
            return Response(f"Error: username is already taken!")
        except ValueError:
            return Response(f"Error: email is already taken!")
        except KeyError:
            return Response(f"Error: phone number is already taken!")
        else:
            return Response(f"User profile updated successfully!")


class ImageUploadView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        user_id = request.user.id
        new_profile_info = CustomUser.objects.get(id=user_id)

        new_image = request.FILES.get('image')

        new_profile_info.image = new_image
        new_profile_info.save()

        return Response(f"Image uploaded successfully!")


class UserProfileView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        try:
            username = request.user.username
            account_type = request.user.account_type
            first_name = request.user.first_name
            last_name = request.user.last_name
            patronymic = request.user.patronymic
            phone_number = request.user.phone_number
            email = request.user.email
            birthday = request.user.birthday
            image = request.user.image

            user_info = [{f"username: {username}",
                          f"account_type: {account_type}",
                          f"first_name: {first_name}",
                          f"last_name: {last_name}",
                          f"patronymic: {patronymic}",
                          f"phone_number: {phone_number}",
                          f"email: {email}",
                          f"birthday: {birthday}",
                          f"image: {image}"}]

            return Response({'user_info': user_info})

        except AttributeError:
            return Response(f"User profile error!")


class WebsiteInfo:
    @staticmethod
    def get():
        website_info = WebsiteInfoSerializer(WebsiteInformation.objects, many=True)
        return website_info.data


class HomePageView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        website_info = WebsiteInfo.get()
        return Response(website_info)


class CoursesFullData:
    @staticmethod
    def get():
        courses_full_info = CoursesMainSerializer(CustomUser.objects, many=True)
        return courses_full_info.data

    
class CourseFullDataView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        courses_full_info = CoursesFullData.get()
        return Response(courses_full_info)


class CourseAndLessonsDataView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")

        courses_and_lessons_raw_data = CoursesDescriptionSerializer(Course.objects.get(id=course_id)).data

        number_of_lessons = len(courses_and_lessons_raw_data.get('lessons_info'))

        number_of_tasks = 0
        lessons_ids = Lesson.objects.filter(course_id=course_id).values_list('id', flat=True)
        for lesson_id in lessons_ids:
            number_of_tasks += len(OneManyTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(FixSentenceTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(TranslateWordTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(SequenceTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(AccordanceTask.objects.filter(lesson_id=lesson_id))

        number_of_students = 0
        for course_and_student in StudentCoursesSerializer(StudentCourse.objects, many=True).data:
            if int(course_and_student.get('course')) == int(course_id):
                number_of_students += 1

        courses_and_lessons_data = courses_and_lessons_raw_data

        courses_and_lessons_data['number_of_lessons'] = number_of_lessons
        courses_and_lessons_data['number_of_tasks'] = number_of_tasks
        courses_and_lessons_data['number_of_students'] = number_of_students
        if request.user.is_authenticated:
            courses_and_lessons_data['user_type'] = CustomUser.objects.get(username=request.user).account_type
            if CustomUser.objects.get(username=request.user).account_type == 'Учень':
                access_course = StudentCourse.objects.filter(student_id=request.user.id, course_id=course_id)
                if len(access_course) == 0:
                    courses_and_lessons_data['access_course'] = False
                elif len(access_course) != 0:
                    courses_and_lessons_data['access_course'] = True
        else:
            courses_and_lessons_data['user_type'] = None

        return Response(courses_and_lessons_data)


class AddNewCourse(APIView):

    @staticmethod
    def post(request):
        user_id = request.user.id
        course_name = request.data.get("course_name")
        course_description = request.data.get("course_description")
        course_image = request.FILES.get('course_image')
        difficult_level = request.data.get("difficult_level")

        try:
            date_and_time = timezone.now()
            new_course_data = Course(course_name=str(course_name),
                                   creator_id=user_id,
                                   creation_date=str(date_and_time)[0:10],
                                   course_description=str(course_description),
                                    course_image=course_image,
                                   difficult_level=str(difficult_level))

            new_course_data.save()
        except AttributeError:
            return Response(f"Add course error!")
        return Response(f"Course successfully added!")


class SelectedCourseData(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")
        course_info = SelectedCourseSerializer(Course.objects.filter(id=course_id), many=True)
        return Response(course_info.data)


class UpdateCourse(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")
        new_course_name = request.data.get('new_course_name')
        new_image = request.FILES.get('new_image')
        new_description = request.data.get('new_description')
        new_difficult_level = request.data.get('new_difficult_level')

        try:
            if new_image is None:
                course_object = Course.objects.get(id=course_id)
                course_object.course_name = new_course_name
                course_object.course_description = new_description
                course_object.difficult_level = new_difficult_level
                course_object.save()
            else:
                course_object = Course.objects.get(id=course_id)
                course_object.course_name = new_course_name
                course_object.course_image = new_image
                course_object.course_description = new_description
                course_object.difficult_level = new_difficult_level
                course_object.save()
        except AttributeError:
            return Response(f"Update course error!")
        return Response(f"Course successfully updated!")


class DeleteCourse(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")

        try:
            course_object = Course.objects.get(id=course_id)
            course_object.delete()
        except AttributeError:
            return Response(f"Delete course error!")
        return Response(f"Course successfully deleted!")


class AddNewLesson(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")
        lesson_name = request.data.get("lesson_name")

        try:
            new_lesson_data = Lesson(course_id=course_id,
                                   lesson_name=str(lesson_name))

            new_lesson_data.save()
        except AttributeError:
            return Response(f"Add lesson error!")
        return Response(f"Lesson successfully added!")


class DeleteLesson(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")

        try:
            lesson_object = Lesson.objects.get(id=lesson_id)
            lesson_object.delete()
        except AttributeError:
            return Response(f"Delete lesson error!")
        return Response(f"Lesson successfully deleted!")


class UpdateLesson(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        new_lesson_name = request.data.get('new_lesson_name')

        try:
            lesson_object = Lesson.objects.get(id=lesson_id)
            lesson_object.lesson_name = new_lesson_name
            lesson_object.save()
        except AttributeError:
            return Response(f"Update lesson error!")
        return Response(f"Lesson successfully updated!")


class LessonsListView(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")
        lessons_info = LessonsInfoSerializer(Lesson.objects.filter(course_id=course_id), many=True)
        return Response(lessons_info.data)


class AddStudentApplication(APIView):

    @staticmethod
    def post(request):
        user_id = request.user.id
        application_datetime = timezone.now()
        course_id = request.data.get("course_id")
        application_status = 'В обробці'

        all_student_application = StudentApplication.objects.filter(course_id=course_id, student_id=user_id,
                                                                    application_status__in=['Підтверджено', 'В обробці'])

        if not all_student_application:
            try:
                new_application_data = StudentApplication(student_id=user_id,
                                                            application_datetime=str(application_datetime),
                                                          course_id=course_id,
                                                          application_status=application_status)

                new_application_data.save()
            except AttributeError:
                return Response(f"Add student application error!")
            return Response(f"Student application successfully added!")
        else:
            return Response(f"You have already send application for this course!")


class ChangeApplicationStatus(APIView):

    @staticmethod
    def post(request):
        application_id = request.data.get("application_id")
        new_status = request.data.get("new_status")

        try:
            application_object = StudentApplication.objects.get(id=application_id)
            application_object.application_status = str(new_status)
            application_object.save()
        except AttributeError:
            return Response(f"Update application status error!")
        return Response(f"Application status successfully updated!")


class StudentApplicationsInfo(APIView):

    @staticmethod
    def get(request):
        teacher_id = request.user.id

        student_applications = []

        teacher_courses_ids = Course.objects.filter(creator_id=teacher_id).values_list('id', flat=True)
        filtered_student_applications = StudentApplicationsSerializer(StudentApplication.objects.filter(
            course_id__in=teacher_courses_ids), many=True).data

        for application in filtered_student_applications:
            course_name = Course.objects.get(id=application.get('course')).course_name

            student_first_name = CustomUser.objects.get(id=application.get('student')).first_name
            student_last_name = CustomUser.objects.get(id=application.get('student')).last_name
            student_patronymic = CustomUser.objects.get(id=application.get('student')).patronymic
            student_fullname = f'{str(student_last_name)} {str(student_first_name)} {str(student_patronymic)}'

            application['course_name'] = str(course_name)
            application['student_fullname'] = str(student_fullname)

            student_applications.append(application)

        return Response({'student_applications_data': student_applications})


class AddStudentToCourse(APIView):

    @staticmethod
    def post(request):
        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")

        try:
            add_student_to_course_data = StudentCourse(student_id=student_id, course_id=course_id)
            add_student_to_course_data.save()
        except AttributeError:
            return Response(f"Add a student to a course error!")
        return Response(f"Student successfully added to the course!")


class ProfileStudentCoursesView(APIView):

    @staticmethod
    def get(request):
        user_id = request.user.id
        student_courses_ids = StudentCourse.objects.filter(student_id=user_id).values_list('course_id', flat=True)
        student_courses_info = CoursesMainInfoSerializer(Course.objects.filter(id__in=student_courses_ids), many=True).data

        return Response(student_courses_info)


class ProfileTeacherCoursesView(APIView):

    @staticmethod
    def get(request):
        user_id = request.user.id
        teacher_courses_ids = Course.objects.filter(creator_id=user_id).values_list('id', flat=True)
        teacher_courses_info = CoursesMainInfoSerializer(Course.objects.filter(id__in=teacher_courses_ids), many=True).data

        return Response(teacher_courses_info)


class TasksListView(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        tasks_info = TasksListSerializer(Lesson.objects.filter(id=lesson_id), many=True)
        return Response(tasks_info.data)


class CourseFinalRandomTasksList(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")
        all_course_tasks = AllCourseTasksListSerializer(Course.objects.filter(id=course_id), many=True).data

        grouped_tasks = {}
        for course in all_course_tasks:
            for lesson in course["lessons_info"]:
                for task_type, tasks in lesson.items():
                    if isinstance(tasks, list):
                        if task_type not in grouped_tasks:
                            grouped_tasks[task_type] = []
                        grouped_tasks[task_type].extend(tasks)

        total_tasks = sum(len(category) for category in grouped_tasks.values())

        if total_tasks > 15:
            all_tasks = []
            for category, tasks in grouped_tasks.items():
                for task in tasks:
                    all_tasks.append({"category": category, "task": task})

            random_tasks = sample(all_tasks, 15)
            random_sample = {}
            for entry in random_tasks:
                category = entry["category"]
                task = entry["task"]

                if category not in random_sample:
                    random_sample[category] = []
                random_sample[category].append(task)
            return Response(random_sample)
        else:
            return Response(grouped_tasks)


class AddOneManyTask(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        text = request.data.get("text")
        correct_answer = request.data.get("correct_answer")
        first_wrong_answer = request.data.get("first_wrong_answer")
        second_wrong_answer = request.data.get("second_wrong_answer")
        third_wrong_answer = request.data.get("third_wrong_answer")

        try:
            add_one_to_many_task_data = OneManyTask(lesson_id=lesson_id,
                                                    text=text,
                                                    correct_answer=correct_answer,
                                                    first_wrong_answer=first_wrong_answer,
                                                    second_wrong_answer=second_wrong_answer,
                                                    third_wrong_answer=third_wrong_answer)
            add_one_to_many_task_data.save()
        except AttributeError:
            return Response(f"Add a one to many task error!")
        return Response(f"One to many task successfully added to the lesson!")


class AddFixSentenceTask(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        correct_text = request.data.get("correct_text")
        bad_text = request.data.get("bad_text")

        try:
            fix_sentence_task_data = FixSentenceTask(lesson_id=lesson_id,
                                                    correct_text=correct_text,
                                                    bad_text=bad_text)
            fix_sentence_task_data.save()
        except AttributeError:
            return Response(f"Add a fix sentence task error!")
        return Response(f"Fix sentence task successfully added to the lesson!")


class AddTranslateWordTask(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        english_word = request.data.get("english_word")
        ukrainian_word = request.data.get("ukrainian_word")

        try:
            translate_word_task_data = TranslateWordTask(lesson_id=lesson_id,
                                                     english_word=english_word,
                                                     ukrainian_word=ukrainian_word)
            translate_word_task_data.save()
        except AttributeError:
            return Response(f"Add a translate word task error!")
        return Response(f"Translate word task successfully added to the lesson!")


class AddSequenceTask(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        sequence_text = request.data.get("sequence_text")

        try:
            sequence_task_data = SequenceTask(lesson_id=lesson_id,
                                        sequence_text=sequence_text)
            sequence_task_data.save()
        except AttributeError:
            return Response(f"Add a sequence task error!")
        return Response(f"Sequence task successfully added to the lesson!")


class AddAccordanceTask(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        variants_list = request.data.get("variants")

        try:
            accordance_task_data = AccordanceTask(lesson_id=lesson_id)
            accordance_task_data.save()
            accordance_task_id = max(AccordanceTask.objects.values_list('id', flat=True))

            for pair in variants_list:
                accordance_pair_data = AccordanceTaskVariant(accordance_task_id=accordance_task_id,
                                                  first_variant=pair.get('left'),
                                                  second_variant=pair.get('right'))
                accordance_pair_data.save()

        except AttributeError:
            return Response(f"Add a sequence task error!")
        return Response(f"Sequence task successfully added to the lesson!")


class SelectedOneManyTaskData(APIView):

    @staticmethod
    def post(request):
        one_many_task_id = request.data.get("one_many_task_id")
        one_many_task_info = SelectedOneManyTaskSerializer(OneManyTask.objects.filter(id=one_many_task_id), many=True)
        return Response(one_many_task_info.data)


class SelectedFixSentenceTaskData(APIView):

    @staticmethod
    def post(request):
        fix_sentence_task_id = request.data.get("fix_sentence_task_id")
        fix_sentence_task_info = SelectedFixSentenceTaskSerializer(FixSentenceTask.objects.filter(id=fix_sentence_task_id), many=True)
        return Response(fix_sentence_task_info.data)


class SelectedTranslateWordTaskData(APIView):

    @staticmethod
    def post(request):
        translate_word_task_id = request.data.get("translate_word_task_id")
        translate_word_task_info = SelectedTranslateWordTaskSerializer(TranslateWordTask.objects.filter(id=translate_word_task_id), many=True)
        return Response(translate_word_task_info.data)


class SelectedSequenceTaskData(APIView):

    @staticmethod
    def post(request):
        sequence_task_id = request.data.get("sequence_task_id")
        sequence_task_info = SelectedSequenceTaskSerializer(SequenceTask.objects.filter(id=sequence_task_id), many=True)
        return Response(sequence_task_info.data)


class SelectedAccordanceTaskData(APIView):

    @staticmethod
    def post(request):
        accordance_task_id = request.data.get("accordance_task_id")
        accordance_task_info = SelectedAccordanceTaskSerializer(AccordanceTask.objects.filter(id=accordance_task_id), many=True)
        return Response(accordance_task_info.data)


class UpdateOneManyTask(APIView):

    @staticmethod
    def post(request):
        one_many_task_id = request.data.get("one_many_task_id")
        new_text = request.data.get('new_text')
        new_correct_answer = request.data.get('new_correct_answer')
        new_first_wrong_answer = request.data.get('new_first_wrong_answer')
        new_second_wrong_answer = request.data.get('new_second_wrong_answer')
        new_third_wrong_answer = request.data.get('new_third_wrong_answer')

        try:
            one_many_task_object = OneManyTask.objects.get(id=one_many_task_id)
            one_many_task_object.text = new_text
            one_many_task_object.correct_answer = new_correct_answer
            one_many_task_object.first_wrong_answer = new_first_wrong_answer
            one_many_task_object.second_wrong_answer = new_second_wrong_answer
            one_many_task_object.third_wrong_answer = new_third_wrong_answer
            one_many_task_object.save()
        except AttributeError:
            return Response(f"Update one many task error!")
        return Response(f"One many task successfully updated!")


class UpdateFixSentenceTask(APIView):

    @staticmethod
    def post(request):
        fix_sentence_task_id = request.data.get("fix_sentence_task_id")
        new_correct_text = request.data.get('new_correct_text')
        new_bad_text = request.data.get('new_bad_text')

        try:
            fix_sentence_task_object = FixSentenceTask.objects.get(id=fix_sentence_task_id)
            fix_sentence_task_object.correct_text = new_correct_text
            fix_sentence_task_object.bad_text = new_bad_text
            fix_sentence_task_object.save()
        except AttributeError:
            return Response(f"Update fix sentence task error!")
        return Response(f"Fix sentence task successfully updated!")


class UpdateTranslateWordTask(APIView):

    @staticmethod
    def post(request):
        translate_word_task_id = request.data.get("translate_word_task_id")
        new_english_word = request.data.get("new_english_word")
        new_ukrainian_word = request.data.get("new_ukrainian_word")

        try:
            translate_word_task_object = TranslateWordTask.objects.get(id=translate_word_task_id)
            translate_word_task_object.english_word = new_english_word
            translate_word_task_object.ukrainian_word = new_ukrainian_word
            translate_word_task_object.save()
        except AttributeError:
            return Response(f"Update translate word task error!")
        return Response(f"Translate word task successfully updated!")


class UpdateSequenceTask(APIView):

    @staticmethod
    def post(request):
        sequence_task_id = request.data.get("sequence_task_id")
        new_sequence_text = request.data.get("new_sequence_text")

        try:
            sequence_task_object = SequenceTask.objects.get(id=sequence_task_id)
            sequence_task_object.sequence_text = new_sequence_text
            sequence_task_object.save()
        except AttributeError:
            return Response(f"Update sequence task error!")
        return Response(f"Sequence task successfully updated!")


class UpdateAccordanceTask(APIView):

    @staticmethod
    def post(request):
        accordance_task_id = request.data.get("accordance_task_id")
        accordance_task_variants_ids = request.data.get("accordance_task_variants_ids")
        new_variants_list = request.data.get("new_variants")

        try:
            for variant_id in accordance_task_variants_ids:
                accordance_task_variants_object = AccordanceTaskVariant.objects.get(id=variant_id)
                accordance_task_variants_object.delete()

            for pair in new_variants_list:
                accordance_pair_data = AccordanceTaskVariant(accordance_task_id=accordance_task_id,
                                                             first_variant=pair.get('left'),
                                                             second_variant=pair.get('right'))
                accordance_pair_data.save()

        except AttributeError:
            return Response(f"Update accordance task error!")
        return Response(f"Accordance task successfully updated!")


class DeleteOneManyTask(APIView):

    @staticmethod
    def post(request):
        one_many_task_id = request.data.get("one_many_task_id")
        try:
            one_many_task_object = OneManyTask.objects.get(id=one_many_task_id)
            one_many_task_object.delete()
        except AttributeError:
            return Response(f"Delete one many task error!")
        return Response(f"One many task successfully deleted!")


class DeleteFixSentenceTask(APIView):

    @staticmethod
    def post(request):
        fix_sentence_task_id = request.data.get("fix_sentence_task_id")
        try:
            fix_sentence_task_object = FixSentenceTask.objects.get(id=fix_sentence_task_id)
            fix_sentence_task_object.delete()
        except AttributeError:
            return Response(f"Delete fix sentence task error!")
        return Response(f"Fix sentence task successfully deleted!")


class DeleteTranslateWordTask(APIView):

    @staticmethod
    def post(request):
        translate_word_task_id = request.data.get("translate_word_task_id")
        try:
            translate_word_task_object = TranslateWordTask.objects.get(id=translate_word_task_id)
            translate_word_task_object.delete()
        except AttributeError:
            return Response(f"Delete translate word task error!")
        return Response(f"Translate word task successfully deleted!")


class DeleteSequenceTask(APIView):

    @staticmethod
    def post(request):
        sequence_task_id = request.data.get("sequence_task_id")
        try:
            sequence_task_object = SequenceTask.objects.get(id=sequence_task_id)
            sequence_task_object.delete()
        except AttributeError:
            return Response(f"Delete sequence task error!")
        return Response(f"Sequence task successfully deleted!")


class DeleteAccordanceTask(APIView):

    @staticmethod
    def post(request):
        accordance_task_id = request.data.get("accordance_task_id")
        try:
            accordance_task_object = AccordanceTask.objects.get(id=accordance_task_id)
            accordance_task_object.delete()
        except AttributeError:
            return Response(f"Delete accordance task error!")
        return Response(f"Accordance task successfully deleted!")


class ExercisesListView(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        exercises_info = ExercisesListSerializer(Lesson.objects.filter(id=lesson_id), many=True)
        return Response(exercises_info.data)


class AddDiscussionExercise(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        image = request.FILES.get("image")
        first_question = request.data.get("first_question")
        second_question = request.data.get("second_question")
        third_question = request.data.get("third_question")
        fourth_question = request.data.get("fourth_question")

        try:
            discussion_exercise_data = DiscussionExercise(lesson_id=lesson_id,
                                                        image=image,
                                                        first_question=first_question,
                                                        second_question=second_question,
                                                        third_question=third_question,
                                                        fourth_question=fourth_question)
            discussion_exercise_data.save()
        except AttributeError:
            return Response(f"Add a discussion exercise error!")
        return Response(f"Discussion exercise successfully added to the lesson!")


class AddReadingExercise(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        image = request.FILES.get("image")
        text = request.data.get("text")

        try:
            reading_exercise_data = ReadingExercise(lesson_id=lesson_id,
                                                  image=image,
                                                  text=text)
            reading_exercise_data.save()
        except AttributeError:
            return Response(f"Add a reading exercise error!")
        return Response(f"Reading exercise successfully added to the lesson!")


class AddListeningExercise(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        name = request.data.get("name")
        audio = request.FILES.get("audio")
        text = request.data.get("text")

        try:
            listening_exercise_data = ListeningExercise(lesson_id=lesson_id,
                                                    name=name,
                                                    audio=audio,
                                                    text=text)
            listening_exercise_data.save()
        except AttributeError:
            return Response(f"Add a listening exercise error!")
        return Response(f"Listening exercise successfully added to the lesson!")


class AddVocabularyExercise(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        vocabulary_words_list = request.data.get("vocabulary_words_list")

        try:
            vocabulary_exercise_data = VocabularyExercise(lesson_id=lesson_id)
            vocabulary_exercise_data.save()
            vocabulary_exercise_id = max(VocabularyExercise.objects.values_list('id', flat=True))

            for word in vocabulary_words_list:
                vocabulary_word_data = VocabularyWord(vocabulary_exercise_id=vocabulary_exercise_id,
                                                         english_word=word.get('english_word'),
                                                         ukrainian_word=word.get('ukrainian_word'),
                                                         transcription=word.get('transcription'))
                vocabulary_word_data.save()

        except AttributeError:
            return Response(f"Add a vocabulary exercise error!")
        return Response(f"Vocabulary exercise successfully added to the lesson!")


class AddRulesExercise(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        image = request.FILES.get("image")
        text = request.data.get("text")

        try:
            rules_exercise_data = RulesExercise(lesson_id=lesson_id,
                                                image=image,
                                                text=text)
            rules_exercise_data.save()
        except AttributeError:
            return Response(f"Add a rules exercise error!")
        return Response(f"Rules exercise successfully added to the lesson!")


class SelectedDiscussionExerciseData(APIView):

    @staticmethod
    def post(request):
        discussion_exersice_id = request.data.get("discussion_exersice_id")
        discussion_exersice_info = SelectedDiscussionExerciseSerializer(DiscussionExercise.objects.filter(id=discussion_exersice_id), many=True)
        return Response(discussion_exersice_info.data)


class SelectedReadingExerciseData(APIView):

    @staticmethod
    def post(request):
        reading_exersice_id = request.data.get("reading_exersice_id")
        reading_exersice_info = SelectedReadingExerciseSerializer(ReadingExercise.objects.filter(id=reading_exersice_id), many=True)
        return Response(reading_exersice_info.data)


class SelectedListeningExerciseData(APIView):

    @staticmethod
    def post(request):
        listening_exersice_id = request.data.get("listening_exersice_id")
        listening_exersice_info = SelectedListeningExerciseSerializer(ListeningExercise.objects.filter(id=listening_exersice_id),
                                                                      many=True)
        return Response(listening_exersice_info.data)


class SelectedVocabularyExerciseData(APIView):

    @staticmethod
    def post(request):
        vocabulary_exersice_id = request.data.get("vocabulary_exersice_id")
        vocabulary_exersice_info = SelectedVocabularyExerciseSerializer(VocabularyExercise.objects.filter(id=vocabulary_exersice_id),
                                                                      many=True)
        return Response(vocabulary_exersice_info.data)


class SelectedRulesExerciseData(APIView):

    @staticmethod
    def post(request):
        rules_exersice_id = request.data.get("rules_exersice_id")
        rules_exersice_info = SelectedRulesExerciseSerializer(RulesExercise.objects.filter(id=rules_exersice_id),
                                                                      many=True)
        return Response(rules_exersice_info.data)


class UpdateDiscussionExercise(APIView):

    @staticmethod
    def post(request):
        discussion_exercise_id = request.data.get("discussion_exercise_id")
        new_image = request.FILES.get("new_image")
        new_first_question = request.data.get("new_first_question")
        new_second_question = request.data.get("new_second_question")
        new_third_question = request.data.get("new_third_question")
        new_fourth_question = request.data.get("new_fourth_question")

        try:
            if new_image is None:
                discussion_exercise_object = DiscussionExercise.objects.get(id=discussion_exercise_id)
                discussion_exercise_object.first_question = new_first_question
                discussion_exercise_object.second_question = new_second_question
                discussion_exercise_object.third_question = new_third_question
                discussion_exercise_object.fourth_question = new_fourth_question
                discussion_exercise_object.save()
            else:
                discussion_exercise_object = DiscussionExercise.objects.get(id=discussion_exercise_id)
                discussion_exercise_object.image = new_image
                discussion_exercise_object.first_question = new_first_question
                discussion_exercise_object.second_question = new_second_question
                discussion_exercise_object.third_question = new_third_question
                discussion_exercise_object.fourth_question = new_fourth_question
                discussion_exercise_object.save()
        except AttributeError:
            return Response(f"Update discussion exercise error!")
        return Response(f"Discussion exercise successfully updated!")


class UpdateReadingExercise(APIView):

    @staticmethod
    def post(request):
        reading_exercise_id = request.data.get("reading_exercise_id")
        new_image = request.FILES.get("new_image")
        new_text = request.data.get("new_text")

        try:
            if new_image is None:
                reading_exercise_object = ReadingExercise.objects.get(id=reading_exercise_id)
                reading_exercise_object.text = new_text
                reading_exercise_object.save()
            else:
                reading_exercise_object = ReadingExercise.objects.get(id=reading_exercise_id)
                reading_exercise_object.image = new_image
                reading_exercise_object.text = new_text
                reading_exercise_object.save()
        except AttributeError:
            return Response(f"Update reading exercise error!")
        return Response(f"Reading exercise successfully updated!")


class UpdateListeningExercise(APIView):

    @staticmethod
    def post(request):
        listening_exercise_id = request.data.get("listening_exercise_id")
        new_name = request.data.get("new_name")
        new_audio = request.FILES.get("new_audio")
        new_text = request.data.get("new_text")

        try:
            if new_audio is None:
                listening_exercise_object = ListeningExercise.objects.get(id=listening_exercise_id)
                listening_exercise_object.name = new_name
                listening_exercise_object.text = new_text
                listening_exercise_object.save()
            else:
                listening_exercise_object = ListeningExercise.objects.get(id=listening_exercise_id)
                listening_exercise_object.name = new_name
                listening_exercise_object.audio = new_audio
                listening_exercise_object.text = new_text
                listening_exercise_object.save()
        except AttributeError:
            return Response(f"Update listening exercise error!")
        return Response(f"Listening exercise successfully updated!")


class UpdateVocabularyExercise(APIView):

    @staticmethod
    def post(request):
        vocabulary_exercise_id = request.data.get("vocabulary_exercise_id")
        vocabulary_words_ids = request.data.get("vocabulary_words_ids")
        new_vocabulary_words_list = request.data.get("new_vocabulary_words_list")

        try:
            for vocabulary_word_id in vocabulary_words_ids:
                vocabulary_word_object = VocabularyWord.objects.get(id=vocabulary_word_id)
                vocabulary_word_object.delete()

            for word in new_vocabulary_words_list:
                vocabulary_word_data = VocabularyWord(vocabulary_exercise_id=vocabulary_exercise_id,
                                                      english_word=word.get('english_word'),
                                                      ukrainian_word=word.get('ukrainian_word'),
                                                      transcription=word.get('transcription'))
                vocabulary_word_data.save()

        except AttributeError:
            return Response(f"Update vocabulary exercise error!")
        return Response(f"Vocabulary exercise successfully updated!")


class UpdateRulesExercise(APIView):

    @staticmethod
    def post(request):
        rules_exercise_id = request.data.get("rules_exercise_id")
        new_image = request.FILES.get("new_image")
        new_text = request.data.get("new_text")

        try:
            if new_image is None:
                rules_exercise_object = RulesExercise.objects.get(id=rules_exercise_id)
                rules_exercise_object.text = new_text
                rules_exercise_object.save()
            else:
                rules_exercise_object = RulesExercise.objects.get(id=rules_exercise_id)
                rules_exercise_object.image = new_image
                rules_exercise_object.text = new_text
                rules_exercise_object.save()
        except AttributeError:
            return Response(f"Update rules exercise error!")
        return Response(f"Rules exercise successfully updated!")


class DeleteDiscussionExercise(APIView):

    @staticmethod
    def post(request):
        discussion_exercise_id = request.data.get("discussion_exercise_id")
        try:
            discussion_exercise_object = DiscussionExercise.objects.get(id=discussion_exercise_id)
            discussion_exercise_object.delete()
        except AttributeError:
            return Response(f"Delete discussion exercise error!")
        return Response(f"Discussion exercise successfully deleted!")


class DeleteReadingExercise(APIView):

    @staticmethod
    def post(request):
        reading_exercise_id = request.data.get("reading_exercise_id")
        try:
            reading_exercise_object = ReadingExercise.objects.get(id=reading_exercise_id)
            reading_exercise_object.delete()
        except AttributeError:
            return Response(f"Delete reading exercise error!")
        return Response(f"Reading exercise successfully deleted!")


class DeleteListeningExercise(APIView):

    @staticmethod
    def post(request):
        listening_exercise_id = request.data.get("listening_exercise_id")
        try:
            listening_exercise_object = ListeningExercise.objects.get(id=listening_exercise_id)
            listening_exercise_object.delete()
        except AttributeError:
            return Response(f"Delete listening exercise error!")
        return Response(f"Listening exercise successfully deleted!")


class DeleteVocabularyExercise(APIView):

    @staticmethod
    def post(request):
        vocabulary_exercise_id = request.data.get("vocabulary_exercise_id")
        try:
            vocabulary_exercise_object = VocabularyExercise.objects.get(id=vocabulary_exercise_id)
            vocabulary_exercise_object.delete()
        except AttributeError:
            return Response(f"Delete vocabulary exercise error!")
        return Response(f"Vocabulary exercise successfully deleted!")


class DeleteRulesExercise(APIView):

    @staticmethod
    def post(request):
        rules_exercise_id = request.data.get("rules_exercise_id")
        try:
            rules_exercise_object = RulesExercise.objects.get(id=rules_exercise_id)
            rules_exercise_object.delete()
        except AttributeError:
            return Response(f"Delete rules exercise error!")
        return Response(f"Rules exercise successfully deleted!")


class AddLessonTestResult(APIView):

    @staticmethod
    def post(request):
        test_datetime = timezone.now()
        lesson_id = request.data.get("lesson_id")
        student_id = request.user.id
        number_of_tests = request.data.get("number_of_tests")
        test_result = request.data.get("test_result")
        is_successfully_passed = request.data.get("is_successfully_passed")

        try:
            lesson_test_result = LessonTestResult(test_datetime=test_datetime,
                                                lesson_id=lesson_id,
                                                student_id=student_id,
                                                  number_of_tests=number_of_tests,
                                                  test_result=test_result,
                                                  is_successfully_passed=is_successfully_passed)
            lesson_test_result.save()
        except AttributeError:
            return Response(f"Add a lesson test result error!")
        return Response(f"Lesson test result successfully added!")


class LessonTestResults(APIView):

    @staticmethod
    def post(request):
        lesson_id = request.data.get("lesson_id")
        student_id = request.user.id
        lesson_test_results = LessonTestResultsSerializer(LessonTestResult.objects.filter(
            lesson_id=lesson_id, student_id=student_id), many=True)
        return Response(lesson_test_results.data)


class AddCourseFinalTestResult(APIView):

    @staticmethod
    def post(request):
        test_datetime = timezone.now()
        course_id = request.data.get("course_id")
        student_id = request.user.id
        number_of_tests = request.data.get("number_of_tests")
        test_result = request.data.get("test_result")
        is_successfully_passed = request.data.get("is_successfully_passed")

        try:
            course_final_test_result = CourseFinalTestResult(test_datetime=test_datetime,
                                                              course_id=course_id,
                                                              student_id=student_id,
                                                              number_of_tests=number_of_tests,
                                                              test_result=test_result,
                                                              is_successfully_passed=is_successfully_passed)
            course_final_test_result.save()
        except AttributeError:
            return Response(f"Add a course final test result error!")
        return Response(f"Course final test result successfully added!")


class CourseDataAndFinalTestResults(APIView):

    @staticmethod
    def post(request):
        course_id = request.data.get("course_id")
        student_id = request.user.id

        courses_and_lessons_raw_data = CoursesDescriptionSerializer(Course.objects.get(id=course_id)).data

        number_of_lessons = len(courses_and_lessons_raw_data.get('lessons_info'))

        number_of_tasks = 0
        lessons_ids = Lesson.objects.filter(course_id=course_id).values_list('id', flat=True)
        for lesson_id in lessons_ids:
            number_of_tasks += len(OneManyTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(FixSentenceTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(TranslateWordTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(SequenceTask.objects.filter(lesson_id=lesson_id))
            number_of_tasks += len(AccordanceTask.objects.filter(lesson_id=lesson_id))

        number_of_students = 0
        for course_and_student in StudentCoursesSerializer(StudentCourse.objects, many=True).data:
            if int(course_and_student.get('course')) == int(course_id):
                number_of_students += 1

        courses_and_lessons_data = courses_and_lessons_raw_data

        courses_and_lessons_data['number_of_lessons'] = number_of_lessons
        courses_and_lessons_data['number_of_tasks'] = number_of_tasks
        courses_and_lessons_data['number_of_students'] = number_of_students
        if request.user.is_authenticated:
            courses_and_lessons_data['user_type'] = CustomUser.objects.get(username=request.user).account_type
            if CustomUser.objects.get(username=request.user).account_type == 'Учень':
                access_course = StudentCourse.objects.filter(student_id=request.user.id, course_id=course_id)
                if len(access_course) == 0:
                    courses_and_lessons_data['access_course'] = False
                elif len(access_course) != 0:
                    courses_and_lessons_data['access_course'] = True
        else:
            courses_and_lessons_data['user_type'] = None
        course_test_results = CourseFinalTestResultsSerializer(CourseFinalTestResult.objects.filter(
            course_id=course_id, student_id=student_id), many=True)


        course_lesson_ids = Lesson.objects.filter(course_id=course_id).values_list('id', flat=True)
        tasks_info = TasksListSerializer(Lesson.objects.filter(id__in=course_lesson_ids), many=True).data
        lesson_ids_with_tasks = []

        for lesson in tasks_info:
            if (lesson.get("one_many_tasks_info") or
                    lesson.get("fix_sentence_tasks_info") or
                    lesson.get("translate_word_tasks_info") or
                    lesson.get("sequence_tasks_info") or
                    lesson.get("accordance_tasks_info")):
                lesson_ids_with_tasks.append(lesson["id"])

        passed_tests = LessonsAndLessonTestResultsSerializer(Lesson.objects.filter(id__in=lesson_ids_with_tasks), many=True).data
        passed_tests_for_student = [{
        "id": lesson["id"],
        "lesson_test_results": [
            result for result in lesson["lesson_test_results"] if result["student"] == student_id
        ]
    }
    for lesson in passed_tests if any(result["student"] == student_id for result in lesson["lesson_test_results"])
    ]

        id_no_success = []

        for lesson in passed_tests_for_student:
            if not any(test['is_successfully_passed'] for test in lesson['lesson_test_results']):
                id_no_success.append(lesson['id'])

        if len(passed_tests_for_student) == 0:
            id_no_success = lesson_ids_with_tasks

        number_of_tests = len(LessonsInfoSerializer(Lesson.objects.filter(id__in=lesson_ids_with_tasks), many=True).data)
        number_of_passed_tests = number_of_tests - len(id_no_success)
        tests_info = {'number_of_tests': number_of_tests, 'number_of_passed_tests': number_of_passed_tests}

        return Response({'course_and_lessons_data': courses_and_lessons_data,
                         'course_test_results': course_test_results.data,
                         'tests_info': tests_info})
