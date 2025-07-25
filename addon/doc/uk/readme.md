# Note Diary для NVDA

Додаток NVDA, який дозволяє швидко та ефективно створювати, змінювати, імпортувати та експортувати нотатки.

## Особливості

*   **Керування щоденниками та розділами**: Організуйте свої нотатки в щоденники та розділи для кращої структури.
*   **Швидке редагування**: Легко відкривайте та редагуйте розділи.
*   **Імпорт та експорт**: Зберігайте та відновлюйте свої щоденники та розділи у файлах `.ndn`.
*   **Вбудований пошук**: Швидко знаходьте щоденники та розділи за назвою.
*   **Покращена доступність**: Розроблено з урахуванням доступності для користувачів NVDA.
*   **Настроювані звуки**: Налаштуйте звуки для ключових подій у додатку.

## Встановлення

1.  Завантажте останню версію додатка за посиланням для завантаження.
2.  Відкрийте завантажений файл `.nvda-addon`.
3.  Підтвердьте встановлення, коли NVDA запитає.
4.  Перезапустіть NVDA, щоб зміни набули чинності.

## Як використовувати додаток

Щоб використовувати додаток, виконайте наступні дії:

1.  **Відкрити додаток**: Доступ до Note Diary здійснюється з меню NVDA, у розділі `Інструменти` > `Note Diary`. Ви можете призначити комбінацію клавіш у `Налаштування` > `Жести введення` у категорії `Note Diary`.
2.  **Створити щоденник**: Натисніть кнопку меню `Більше опцій` і виберіть `Новий щоденник`, або використовуйте `CTRL+N` у дереві щоденників. Введіть назву щоденника (наприклад, "Мій особистий щоденник", "Курс Python").
3.  **Створити розділи**: Вибравши щоденник, натисніть `Більше опцій` > `Новий розділ`, або використовуйте `CTRL+P`. Дайте розділу назву (наприклад, "Урок 01 Привіт світ", "05/07/2025").
4.  **Написати в розділі**: Виберіть розділ і натисніть `Enter`, або `Програми` / `Shift+F10` і виберіть `Редагувати`. Почніть писати в багаторядковому полі.
5.  **Зберегти розділ**: Натисніть `Alt+G` або перейдіть за допомогою `Tab` до кнопки `Зберегти` і натисніть її. Якщо є зміни і ви закриєте вікно, вам буде запропоновано зберегти.

## Пояснення інтерфейсу

### Список щоденників

Це деревоподібне представлення, яке дозволяє переміщатися по щоденниках та розділах. Щоденники знаходяться на рівні 0. Використовуйте стрілки вгору/вниз для переміщення, `Enter` або стрілки вліво/вправо для розгортання/згортання щоденників. Ви також можете переміщатися за допомогою літер алфавіту.

### Кнопка "Більше опцій"

При натисканні цієї кнопки або фокусуванні на ній та натисканні стрілки вниз з'являються наступні опції:

*   **Новий щоденник**: Створює новий щоденник.
*   **Новий розділ**: Створює новий розділ у вибраному щоденнику.
*   **Імпортувати щоденники**: Відновлює щоденники з файлу `.ndn`.
*   **Експортувати щоденники**: Зберігає всі ваші щоденники та розділи у файл `.ndn` для резервного копіювання або обміну.
*   **Довідка**: Містить `Про програму...` (основна інформація про додаток) та `Документація` (відкриває цей файл у браузері).

### Поле інформації лише для читання

Після списку щоденників ви знайдете поле редагування лише для читання з основною інформацією про вибраний щоденник або розділ.

*   **Щоденники**: Показує назву, дату створення, дату зміни та кількість розділів.
*   **Розділи**: Показує назву розділу, щоденник, до якого він належить, дату створення, дату зміни та кількість сторінок.

### Кнопка закриття

Закриває вікно додатка. Ви також можете використовувати клавішу `Escape`.

## Список гарячих клавіш

### Головне вікно

*   `Ctrl+N`: Створює новий щоденник.
*   `Ctrl+P`: Створює новий розділ у вибраному щоденнику.
*   `Delete`: Видаляє щоденник (з усіма його розділами) або розділ.
*   `Enter`: Відкриває/закриває щоденник; відкриває вікно редагування розділу.
*   `F5`: Оновлює вікно.
*   `F2`: Перейменовує вибраний щоденник або розділ.
*   `F1`: Відкриває цей документ.
*   `Applications` або `Shift+F10`: Відкриває контекстне меню для вибраного щоденника або розділу.

### Корисні гарячі клавіші в головному вікні

*   `Alt+M`: Відкриває меню `Більше опцій`.
*   `Alt+D`: Фокусує список щоденників.
*   `Alt+I`: Фокусує поле редагування інформації.
*   `Alt+C`: Закриває вікно додатка.

### Корисні гарячі клавіші у вікні редагування розділу

*   `Alt+N`: Фокусує поле редагування.
*   `Alt+P`: Копіює весь вміст розділу в буфер обміну.
*   `Alt+G`: Зберігає розділ.
*   `Alt+C`: Закриває діалог розділу.

## Налаштування додатка

У параметрах NVDA, у розділі `Note Diary`, ви можете ввімкнути або вимкнути звуки додатка. При активації звуки відтворюватимуться під час таких подій, як зміна щоденника або розділу.

## Завантажити

Ви можете завантажити останню версію додатка за наступним посиланням:
[Завантажити Note Diary для NVDA](https://github.com/JohanAnim/Note-diary/releases/latest/download/Note.diary.for.NVDA.nvda-addon)

## Автори

Подяка наступним користувачам за співпрацю з частиною вихідного коду та деякими функціями:

*   [Héctor J. Benítez Corredera](https://github.com/hxebolax/): Реалізував початкову частину цього додатка.
*   [metalalchemist](https://github.com/metalalchemist/): Реалізація деяких функцій додатка.

---

© 2023-2025 Johan G

## Історія змін

Ви можете переглянути всі зміни та версії додатка в [Історії змін](CHANGELOG.md).