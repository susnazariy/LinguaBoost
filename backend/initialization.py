""" Project initialization '"""

import os
import django
from colorama import init, Fore, Style

init(autoreset=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguaboost_settings.settings')
django.setup()


def database_creations():
    from psycopg2 import connect, errors, OperationalError

    try:
        db_connect = connect(host='localhost',
                                user='postgres',
                                port='5433',
                                password='1111')
        db_connect.autocommit = True
    except OperationalError:
        print(Fore.RED + f'Postgres server connection error!\n')
        return False
    else:
        db_cursor = db_connect.cursor()

        with open('database_queries/creating_a_database.sql', encoding='UTF-8') as file:
            creating_database_file_info = file.read()

        with open('database_queries/deleting_a_database.sql', encoding='UTF-8') as file:
            deleting_database_file_info = file.read()

        try:
            db_cursor.execute(creating_database_file_info)
        except errors.ObjectInUse:
            print(Fore.RED + f"Database in use!")
            return False
        except errors.DuplicateDatabase:
            try:
                print(f'Database already exist')
                db_cursor.execute(deleting_database_file_info)
                print('Database successfully deleted')
                db_cursor.execute(creating_database_file_info)
                print(f'Database `{creating_database_file_info[16:len(creating_database_file_info) - 1]}` has been created')
            except errors.ObjectInUse:
                print(Fore.RED + f"Database in use!")
                return False
            else:
                return True
        else:
            print(f'Database `{creating_database_file_info[16:len(creating_database_file_info) - 1]}` has been created')
            return True


def database_migrations():
    from django.db import connections
    from django.db.utils import OperationalError

    try:
        connections['default'].cursor()
    except OperationalError:
        return False
    else:
        files_list = os.listdir('linguaboost_application/migrations')

        for file in files_list:
            if file != '__init__.py' and file != '__pycache__':
                os.remove(f'linguaboost_application/migrations/{file}')

        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
        return True


def test_superuser_creations():
    from linguaboost_application.models import CustomUser
    from django.db.utils import ProgrammingError, IntegrityError

    superuser_information = [{'username': 'admin',
                             'account_type': 'Адміністратор',
                             'password': '1111',
                             'email': 'admin@gmail.com',
                             'first_name': '-',
                             'last_name': '-',
                             'patronymic': '-',
                             'phone_number': '-',
                             'image': 'images/profile_images/admin.jpg'}]

    for superuser_info in superuser_information:
        try:
            CustomUser.objects.create_user(username=superuser_info.get('username'),
                                    account_type=superuser_info.get('account_type'),
                                    password=superuser_info.get('password'),
                                    email=superuser_info.get('email'),
                                    first_name=superuser_info.get('first_name'),
                                    last_name=superuser_info.get('last_name'),
                                    patronymic=superuser_info.get('patronymic'),
                                    phone_number=superuser_info.get('phone_number'),
                                    image=superuser_info.get('image'),
                                    is_staff=True,
                                    is_superuser=True)

        except ProgrammingError:
            print(Fore.RED + f"Problem with database! Maybe it doesn't exist...")
            return False
        except IntegrityError:
            print(Fore.RED + f"Username `{superuser_info.get('username')}` already exist or other error is "
                             f"appeared!")
            return False
        else:
            print(f'Superuser profile `{superuser_info.get('username')}` has been created!')
    return True


def test_user_creations():
    from linguaboost_application.models import CustomUser
    from django.db.utils import ProgrammingError, IntegrityError

    users_information = [{'username': 'Olena',
                          'account_type': 'Викладач',
                           'password': '1111',
                           'first_name': 'Олена',
                           'last_name': 'Шафран',
                            'patronymic': '',
                           'email': 'olenashafran06@gmail.com',
                            'phone_number': '',
                            'birthday': '2000-01-01',
                           'image': 'images/profile_images/Olena.jpg'},
                          {'username': 'Nazar',
                           'account_type': 'Викладач',
                           'password': '1111',
                           'first_name': 'Назар',
                           'last_name': 'Сус',
                           'patronymic': '',
                           'email': 'susnazariy@gmail.com',
                           'phone_number': '',
                           'birthday': '2000-01-01',
                           'image': 'images/profile_images/Nazar.png'},
                         {'username': 'StepanBabaico',
                          'account_type': 'Викладач',
                          'password': '1111',
                          'first_name': 'Степан',
                          'last_name': 'Бабайко',
                          'patronymic': 'Андрійович',
                          'email': 'StepanBabaico@gmail.com',
                          'phone_number': '+380667734232',
                          'birthday': '1998-11-04',
                          'image': 'images/profile_images/StepanBabaico.jpg'},
                         {'username': 'PavloOstapchuk',
                          'account_type': 'Викладач',
                          'password': '1111',
                          'first_name': 'Павло',
                          'last_name': 'Остапчук',
                          'patronymic': 'Ігорович',
                          'email': 'PavloOstapchuk@gmail.com',
                          'phone_number': '+380984833769',
                          'birthday': '2000-04-13',
                          'image': 'images/profile_images/PavloOstapchuk.jpg'},
                         {'username': 'DmytroPankiv',
                          'account_type': 'Учень',
                          'password': '1111',
                          'first_name': 'Дмитро',
                          'last_name': 'Паньків',
                          'patronymic': 'Олександрович',
                          'email': 'DmytroPankiv@gmail.com',
                          'phone_number': '+380668439044',
                          'birthday': '1997-04-21',
                          'image': 'images/profile_images/DmytroPankiv.jpg'},
                         {'username': 'MykolaOstafiishuk',
                          'account_type': 'Учень',
                          'password': '1111',
                          'first_name': 'Микола',
                          'last_name': 'Остафійчук',
                          'patronymic': 'Володимирович',
                          'email': 'MykolaOstafiishuk@gmail.com',
                          'phone_number': '+380983374880',
                          'birthday': '1999-12-09',
                          'image': 'images/profile_images/MykolaOstafiishuk.jpg'},
                         {'username': 'ViktoriaAbramenko',
                          'account_type': 'Учень',
                          'password': '1111',
                          'first_name': 'Вікторія',
                          'last_name': 'Абраменко',
                          'patronymic': 'Сергіївна',
                          'email': 'ViktoriaAbramenko@gmail.com',
                          'phone_number': '+380684678121',
                          'birthday': '2004-08-13',
                          'image': 'images/profile_images/ViktoriaAbramenko.jpg'},
                         {'username': 'UliaGrabovets',
                          'account_type': 'Учень',
                          'password': '1111',
                          'first_name': 'Юлія',
                          'last_name': 'Грабовець',
                          'patronymic': 'Назарівна',
                          'email': 'UliaGrabovets@gmail.com',
                          'phone_number': '+380668344430',
                          'birthday': '2003-11-21',
                          'image': 'images/profile_images/UliaGrabovets.jpg'}]

    for user in users_information:
        try:
            CustomUser.objects.create_user(username=user.get('username'),
                                    account_type=user.get('account_type'),
                                    password=user.get('password'),
                                    email=user.get('email'),
                                    phone_number=user.get('phone_number'),
                                    first_name=user.get('first_name'),
                                    last_name=user.get('last_name'),
                                    patronymic=user.get('patronymic'),
                                    birthday=user.get('birthday'),
                                    image=user.get('image'),
                                    is_active=True,
                                    is_staff=False,
                                    is_superuser=False)
        except ProgrammingError:
            print(Fore.RED + f"Problem with database! Maybe it doesn't exist...")
            return False
        except IntegrityError:
            print(Fore.RED + f"User `{user.get('username')}` already exist!")
            return False
        else:
            print(f'User profile `{user.get('username')}` has been created!')
    return True


def create_triggers():
    from psycopg2 import connect, errors, OperationalError

    db_connect = connect(host='localhost',
                        user='postgres',
                        port='5433',
                        password='1111',
                        database='linguaboost_db')
    db_connect.autocommit = True
    db_cursor = db_connect.cursor()

    with open('database_queries/creating_a_triggers.sql', encoding='UTF-8') as file:
        file_data = file.read()

        triggers = file_data.split('\n\n')
        for trigger in triggers:
            try:
                db_cursor.execute(trigger)
            except OperationalError:
                print(Fore.RED + 'Creating trigger error!')
                return False
            except errors.UndefinedTable:
                print(Fore.RED + 'Undefined trigger data or relationship error!')
                return False
            else:
                pass
        rows = file_data.split('\n')
        triggers_names = []

        for row in rows:
            if row[:14] == 'create trigger':
                triggers_names.append(row[15:])

        for name in triggers_names:
            print(f'Created `{name}` trigger!')
    return True


def insert_test_data_into_db():
    from psycopg2 import connect, errors, OperationalError

    db_connect = connect(host='localhost',
                        user='postgres',
                        port='5433',
                        password='1111',
                        database='linguaboost_db')
    db_connect.autocommit = True
    db_cursor = db_connect.cursor()

    with open('database_queries/inserting_test_data.sql', encoding='UTF-8') as file:
        file_data = file.read()

        queries = file_data.split('\n\n')
        for query in queries:
            table_name = ''
            for letter in query[12::]:
                if letter != ' ':
                    table_name += letter
                else:
                    break
            try:
                db_cursor.execute(query)
            except OperationalError:
                print(Fore.RED + 'Inserting error!')
                return False
            except errors.UndefinedTable:
                print(Fore.RED + f'Undefined table or relationship error! Name of table > {table_name}')
                return False
            else:
                print(f'Inserted data into `{table_name}` table!')
    return True


def starting_initialization_modules():
    if not database_creations():
        print(Fore.RED + Style.BRIGHT + 'Database initialization failed!')
    else:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Database initialization successful!\n\n')
        if not database_migrations():
            print(Fore.RED + Style.BRIGHT + 'Database migrations failed!')
        else:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Database migrations successful!\n\n')
            if not test_superuser_creations():
                print(Fore.RED + Style.BRIGHT + 'Superusers initialization failed!')
            else:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Superusers initialization successful!\n\n')
                if not test_user_creations():
                    print(Fore.RED + Style.BRIGHT + 'Users initialization failed!')
                else:
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Users initialization successful!\n\n')
                if not create_triggers():
                    print(Fore.RED + Style.BRIGHT + 'Triggers initialization failed!')
                else:
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Triggers initialization successful!\n\n')
                if not insert_test_data_into_db():
                    print(Fore.RED + Style.BRIGHT + 'Add database data initialization failed!')
                else:
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + 'Database data initialization successful!')


if __name__ == '__main__':
    starting_initialization_modules()
