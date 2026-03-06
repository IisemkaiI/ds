import re
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'regularExpressions/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'regularExpressions/login.html', {'form': form})


def index(request):
    regex = ""
    test_string = ""
    matches = []
    error_message = None

    if request.method == "POST":
        regex = request.POST.get("regex", "")
        test_string = request.POST.get("test_string", "")
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            try:
                test_string = uploaded_file.read().decode('utf-8')
            except Exception:
                error_message = "Ошибка чтения файла"

        if regex and not error_message:
            try:
                matches = re.findall(regex, test_string)
                print(f"Найдено совпадений: {len(matches)}")
            except re.error:
                error_message = "Ошибка в регулярном выражении"
                matches = []
        elif not regex and not error_message:
            error_message = "Введите регулярное выражение"

    context = {
        "regex": regex,
        "test_string": test_string,
        "matches": matches,
        "error_message": error_message,
    }

    return render(request, "regularExpressions/base.html", context)