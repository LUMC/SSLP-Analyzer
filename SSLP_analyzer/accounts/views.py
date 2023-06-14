from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm


def login_and_register_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        register_form = UserCreationForm(request.POST or None)
        if 'login_form' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("/")
            else:
                messagesl = get_error_message(login_form)
                context = {
                "login_form": login_form,
                "register_form": register_form,
                "messagesl": messagesl,
                }
                return render(request, "accounts/signin.html", context)
        elif 'register_form' in request.POST:
            if register_form.is_valid():
                user_object = register_form.save()
                login(request, user_object)
                return redirect("/")
            else:
                messagesr = get_error_message(register_form)
                print(messagesr)
                context = {
                "login_form": login_form,
                "register_form": register_form,
                "messagesr": messagesr,
                }
                return render(request, "accounts/signin.html", context)
    else:
        login_form = AuthenticationForm(request, data=request.POST)
        register_form = UserCreationForm(request.POST or None)
        context = {
            "login_form": login_form,
            "register_form": register_form,
        }
        return render(request, "accounts/signin.html", context)
    
def get_error_message(form):
    error_msg_str = ""
    for field_name, errors in form.errors.items():
        for error_msg in errors:
            error_msg_str += f"{error_msg}\n"
    return error_msg_str
    
def logout_view(request):
    """logout
    Deze view logt de gebruiker uit en stuurt de gebruiker vervolgens naar de homepage. 
    Omdat je voor de homepage ingelogt moet zijn wordt je daarna weer naar de loginpagina gestuurd.
    """
    logout(request)
    return redirect("/")
