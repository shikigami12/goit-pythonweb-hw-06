
# Проект бази даних для університету

Цей проект є простою системою на основі ORM (SQLAlchemy) для керування базою даних університету. Він включає моделі для студентів, груп, викладачів, предметів та оцінок. Управління базою даних здійснюється через міграції Alembic та CLI-інтерфейс на `argparse`.

## Технології

- Python 3
- PostgreSQL
- Docker
- Pipenv
- SQLAlchemy
- Alembic
- Faker

## Встановлення та запуск

#### Крок 1: Клонування репозиторію

```bash
git clone <URL_вашого_репозиторію>
cd <назва_папки_проекту>
```

#### Крок 2: Запуск бази даних

Переконайтеся, що у вас встановлено та запущено Docker. Виконайте команду для створення та запуску контейнера з PostgreSQL:

```bash
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

**Примітка:** Якщо ви змінили пароль `mysecretpassword`, не забудьте оновити його у файлі `database.py`.

#### Крок 3: Встановлення залежностей

Проект використовує `pipenv` для керування залежностями. 

```bash
# Встановлюємо залежності з Pipfile.lock
pipenv install

# Активуємо віртуальне середовище
pipenv shell
```

#### Крок 4: Створення таблиць (Міграції)

Після активації середовища виконайте команду для застосування міграцій Alembic. Це створить усі необхідні таблиці в базі даних.

```bash
alembic upgrade head
```

#### Крок 5: Заповнення бази даних (Seeding)

Щоб заповнити базу даних тестовими даними, запустіть скрипт `seed.py`.

```bash
python seed.py
```

## Використання

### Виконання запитів (`my_select.py`)

Для виконання 12 попередньо визначених запитів до бази даних запустіть скрипт `my_select.py`.

```bash
python my_select.py
```

### Інтерфейс командного рядка (`main.py`)

Для CRUD-операцій (Create, Read, Update, Delete) використовуйте скрипт `main.py`.

**Загальна структура команди:**

```bash
python main.py -a <дія> -m <модель> [параметри]
```

- `-a`, `--action`: дія (`create`, `list`, `update`, `remove`)
- `-m`, `--model`: модель (`Teacher`, `Group`, `Student`, `Subject`, `Grade`)

#### Приклади команд:

**Teacher**
- `python main.py -a create -m Teacher -n 'Ілон Маск'`
- `python main.py -a list -m Teacher`
- `python main.py -a update -m Teacher --id 1 -n 'Джефф Безос'`
- `python main.py -a remove -m Teacher --id 1`

**Group**
- `python main.py -a create -m Group -n 'ПМ-101'`
- `python main.py -a list -m Group`
- `python main.py -a update -m Group --id 1 -n 'ПМ-102'`
- `python main.py -a remove -m Group --id 1`

**Student**
- `python main.py -a create -m Student -n 'Студент Студентенко' --group_id 1`
- `python main.py -a list -m Student`
- `python main.py -a update -m Student --id 1 -n 'Новий Студент' --group_id 2`
- `python main.py -a remove -m Student --id 1`

**Subject**
- `python main.py -a create -m Subject -n 'Веб-програмування' --teacher_id 1`
- `python main.py -a list -m Subject`
- `python main.py -a update -m Subject --id 1 -n 'Основи Python' --teacher_id 2`
- `python main.py -a remove -m Subject --id 1`

**Grade**
- `python main.py -a create -m Grade --grade 95 --date_of '2025-09-07' --student_id 1 --subject_id 1`
- `python main.py -a list -m Grade`
- `python main.py -a update -m Grade --id 1 --grade 100`
- `python main.py -a remove -m Grade --id 1`
