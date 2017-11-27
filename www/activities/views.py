from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from common.qiniuSettings import httpsUrl, imageStyle, avatarStyle
from .forms import ActCreateForm
from .models import Act
from common.models import MyUser
from .choices import ACTLICENCE


@login_required
def act_create(request):
    if request.method == "GET":
        form = ActCreateForm
        return render(
            request, "act/new.html", {"form": form, "httpsUrl": httpsUrl})


def act_list(request, act_list):
    if request.method == "GET":
        url = "https://o3e6g3hdp.qnssl.com/"
        style_name = "-actCoverInterS"
        act_details = Act.objects.filter(act_type=2)[:12]
        return render(
                request, "act/activities_list.html",
                {
                    "act_list": act_details,
                    "url": url,
                    "style_name": style_name
                }
            )
    else:
        error = "Method not allowed."
        return render(request, "error.html", {"error": error})


def act_details(request, act_url):
    if request.method == "GET":
        act_author = act_url.split("/")[0]
        try:
            act_author = MyUser.objects.get(
                    user_name=act_author
                    )
            act_details = Act.objects.get(
                    act_url=act_url,
                    )
        except ValueError:
            error = "Activity Not exist."
            return render(request, "error.html", {"error": error})
        else:
            act_license = ACTLICENCE[act_details.act_licence]
            act_thumb = httpsUrl + act_details.act_thumb_url + imageStyle
            return render(
                    request, "post/posts_list.html",
                    {
                        "act_details": act_details,
                        "act_author": act_author,
                        "act_thumb": act_thumb,
                        "httpsUrl": httpsUrl,
                        "imageStyle": imageStyle,
                        "avatarStyle": avatarStyle,
                        "act_license": act_license[1]
                    }
                )
    else:
        error = "Method not allowed."
        return render(request, "error.html", {"error": error})


def act_intro(request, act_intro):
    if request.method == "GET":
        act_url = act_intro.split('details')[0]
        try:
            act_details = Act.objects.get(
                    act_url=act_url,
                    )
        except ObjectDoesNotExist:
            error = "Activity Not exist."
            return render(request, "error.html", {"error": error})
        else:
            act_license = ACTLICENCE[act_details.act_licence]
            act_thumb = httpsUrl + act_details.act_thumb_url + imageStyle
            return render(
                    request, "act/act_intro.html",
                    {
                        "act_details": act_details,
                        "act_author": act_details.user,
                        "act_thumb": act_thumb,
                        "httpsUrl": httpsUrl,
                        "imageStyle": imageStyle,
                        "avatarStyle": avatarStyle,
                        "act_license": act_license[1]
                    }
                )
