#МАРК ЭТО ТЕБЕ мне кароч стало лень чет тут тебе говорить ты человек умный сам справишся куда и что добавлять интернет у тебя есть удачи кароч
#но в templates>regularExpressions и там есть все .html а в static>regularExpressions>css находятся стили
import re # стандартная библиотека Python для работы с регулярными выражениями
from django.shortcuts import render, redirect #функции для отображения HTML и перенаправления (перекидывает на другую страницу).
from django.contrib.auth import login #функция, которая авторизует пользователя (начинает сессию).
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #встроенные формы Django для регистрации и входа.

def register(request): #функция представления в Django, которая реализует регистрацию нового пользователя
    #Параметр request позволяет функции получить доступ к данным, введённым пользователем при регистрации на сайте
    if request.method == 'POST': #проверка, что пользователь отправил форму (нажали кнопку «Зарегистрироваться»).
        form = UserCreationForm(request.POST) # создаём форму из данных, которые прислал браузер
        if form.is_valid(): #проверяем правильность заполнения формы (например, пароли совпадают, поля заполнены).
            user = form.save() #сохраняем нового пользователя в базу.
            login(request, user) # автоматически авторизуем нового пользователя (все детали Django уже позаботится о том, чтобы его переместить внутрь системы).
            return redirect('index') #переходим на главную страницу (у нас там редактор regex).
    else: #В случае GET (например, пользователь просто зашел на страницу),
        form = UserCreationForm() # создается пустая форма UserCreationForm().
    return render(request, 'regularExpressions/register.html', {'form': form}) #В конце возвращается готовая страница (register.html) с формой.

def user_login(request): #Обрабатывает вход пользователя.
    if request.method == 'POST': #Аналогично — при POST пользователь прислал логин и пароль.
        form = AuthenticationForm(data=request.POST) # создаем форму авторизации.
        if form.is_valid(): #проверяем правильность логина/пароля.
            user = form.get_user() #получаем пользователя из формы.
            login(request, user) # засекаем его в системе, начинаем сессию.
            return redirect('index') # Перенаправляем на главную страницу (редактор).
    else:#При GET — показываем пустую форму входа.
        form = AuthenticationForm() # создается пустая форма AuthenticationForm().
    return render(request, 'regularExpressions/login.html', {'form': form}) #В конце вызывается шаблон login.html, где пользователь вводит логин и пароль.


def index(request):
    regex = ""
    test_string = ""
    matches = []
    error_message = None

    if request.method == "POST":
        # ИСПРАВЛЕНО: имена должны точь-в-точь как в HTML name="..."
        regex = request.POST.get("regex", "")
        test_string = request.POST.get("test_string", "")
        uploaded_file = request.FILES.get("file")

        # Если загружен файл, читаем его вместо текстового поля
        if uploaded_file:
            try:
                test_string = uploaded_file.read().decode('utf-8')
            except Exception:
                error_message = "Ошибка чтения файла"

        # Логика поиска
        if regex and not error_message:
            try:
                matches = re.findall(regex, test_string)
                # ДЛЯ ПРОВЕРКИ: смотри консоль терминала после нажатия кнопки
                print(f"Найдено совпадений: {len(matches)}")
            except re.error:
                error_message = "Ошибка в регулярном выражении!"
                matches = []
        elif not regex and not error_message:
            error_message = "Введите регулярное выражение"

    context = {
        "regex": regex,
        "test_string": test_string,
        "matches": matches,
        "error_message": error_message,
    }

    # Убедись, что имя файла здесь совпадает с реальным файлом в папке templates
    return render(request, "regularExpressions/base.html", context)
    #Функция render берет файл base.html, находит там места, помеченные как {{ regex }} или {{ matches }},
    #вставляет в них данные из словаря context и возвращает пользователю готовую страницу.




# И помимо этого я изменял urls.py, settings.py, Шаблоны, CSS, logout

