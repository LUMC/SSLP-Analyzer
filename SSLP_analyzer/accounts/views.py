from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_and_register_view(request):
    """
    Returns:
        HttpResponse: The HTTP response containing the rendered login page or a redirection to the homepage.
    Summary:
        This view function handles the login and registration process for users. If the request method is 'POST', it checks
        if the login form is submitted. If the form is valid, it logs in the user and redirects them to the homepage. If the
        form is not valid, it renders the login page with the error messages.
        If the request method is not 'POST', it simply renders the login page with an empty login form.
    """
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if 'login_form' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("/")
            else:
                messagesl = get_error_message(login_form)
                context = {
                "login_form": login_form,
                "messagesl": messagesl,
                }
                print(messagesl)
                return render(request, "accounts/signin.html", context)
    else:
        login_form = AuthenticationForm(request, data=request.POST)
        context = {
            "login_form": login_form,
        }
        return render(request, "accounts/signin.html", context)
    
def get_error_message(form):
    """
    Returns:
        str: A formatted string containing error messages for the form fields.
    Summary:
        Retrieve error messages from a Django form object.
    """
    error_msg_str = ""
    for field_name, errors in form.errors.items():
        for error_msg in errors:
            error_msg_str += f"{error_msg}\n"
    return error_msg_str
    
def logout_view(request):
    """
    Returns:
        HttpResponseRedirect: Redirects the user to the homepage.
    Summary:
        This view logs out the user and then redirects them to the homepage.
        Since being logged in is required to access the homepage, the user is
        redirected back to the login page after logging out.
    """
    logout(request)
    return redirect("/")
