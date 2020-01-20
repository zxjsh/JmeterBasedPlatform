from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import signInForm, signUpForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def userSignIn(request):
    massage = None
    userId = None
    if request.user.id:
        return redirect('TestScripts:ScriptList')

    if request.method == 'POST':
        form = signInForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            user = authenticate(request, username=cleanedData[u'username'], password=cleanedData[u'password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('TestScripts:ScriptList')
                else:
                    return render(request, 'Users/SignIn.html', {'form': form, 'isActive': False})
            else:
                return render(request, 'Users/SignIn.html', {'form': form, 'isWrong': True})

    else:
        form = signInForm()
    context = {'form': form}
    return render(request, 'Users/SignIn.html', context)


def userSignOut(request):
    logout(request)
    return redirect('Users:SignIn')


def userSignUp(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            newUser.set_password(form.cleaned_data['password'])
            newUser.save()
            return render(request, 'Users/SignUpSuccess.html', {'newUser': newUser})
    else:
        form = signUpForm()
    return render(request, 'Users/SignUp.html', {'form': form})
