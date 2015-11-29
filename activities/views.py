from django.shortcuts import render, redirect

def new_act(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return render(request, "act/new.html")
        else:
            redirect('/login/') 
    else:
        error = "不允许使用此方法。"
        return render(request, "error.html", {"error": error})

