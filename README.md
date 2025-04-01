# Проєкт: Мапа популярності локацій

## Опис

Веб-додаток, який дозволяє користувачам переглядати та оцінювати популярні локації на інтерактивній мапі. Популярність визначається на основі активності користувачів, рейтингу та відгуків.

## Функціонал

### 1. Аутентифікація та авторизація

- **Реєстрація та вхід користувачів** через вбудовану Django authentication (username, email, пароль).
- **Авторизація** через сесії та cookies (без JWT).
- **Захист сторінок** авторизованих користувачів за допомогою `LoginRequiredMixin`.
- **Скидання пароля** через email.

### 2. CRUD-операції для локацій

- **Створення, редагування, перегляд та видалення локацій.**
- **Валідація даних** перед збереженням у базі.

### 3. Відгуки та рейтинги

- **Залишення коментарів** під локаціями користувачами.
- **Система лайків/дизлайків** для відгуків.

### 4. Пошук та фільтрація

- **Фільтрація локацій** за:
  - Рейтингом.
  - Категорією.
- **Пошук локацій** за назвою та описом.

### 5. Експорт даних

- **Експорт локацій** у форматі JSON або CSV.

### 6. Додатковий функціонал (бонус)

- **Надсилання email-сповіщень** при нових відгуках.
- **Endpoint для підписки**, що дозволяє користувачам отримувати нові відгуки до локацій.

## Технологічний стек

- **Back-end**: Django, Django REST Framework, PostgreSQL
- **Auth**: Django Authentication (сесії та cookies)
- **Кешування**: Redis
- **Фільтрація**: Django-filter
- **Експорт**: Pandas

## Вимоги до коду

### Чистий код

- Код має бути зрозумілим, добре структурованим, з чіткими назвами змінних та функцій.
- Використання принципів **DRY** (Don't Repeat Yourself).
- Дотримання стандарту **PEP 8** для Python.
- Написання **юніт-тестів** для ключових функцій та API.

### Реалізація за принципами REST

- Використання стандартів REST для створення API:
  - **GET, POST, PUT, DELETE** для відповідних операцій.
  - Використання правильних **HTTP статус-кодів**.
  - Створення API-ендпоінтів, що відповідають стандартам REST.

## API Ендпоінти

### 1. Аутентифікація та авторизація (Users)

- **POST** `/api/users/register/`  
  Реєстрація нового користувача.  
  _View: `RegisterView`_
- **POST** `/api/users/login/`  
  Вхід користувача.  
  _View: `LoginView`_
- **GET/POST** `/api/users/logout/`  
  Вихід користувача (залежно від реалізації).  
  _View: `LogoutView`_
- **POST** `/api/users/password-reset/`  
  Скидання пароля через email.  
  _View: `ResetPasswordView`_

### 2. Локації

- **POST** `/api/locations/`  
  Створення нової локації.  
  _View: `CreateLocationView`_
- **GET, PUT, DELETE** `/api/locations/<int:pk>/`  
  Отримання деталей, редагування або видалення локації за її ідентифікатором.  
  _View: `LocationDetailView`_
- **GET** `/api/locations/export/`  
  Експорт даних локацій у форматі JSON або CSV.  
  _View: `ExportLocationsView`_

- http://127.0.0.1:8000/api/locations/export/?format=csv&download=true  
- http://127.0.0.1:8000/api/locations/export/?format=json&download=true

для завантаження

### 3. Відгуки

- **POST** `/api/locations/<int:location_id>/reviews/`  
  Створення нового відгуку для конкретної локації.  
  _View: `CreateReviewView`_
