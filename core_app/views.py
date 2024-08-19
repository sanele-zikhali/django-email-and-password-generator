from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.contrib.auth import authenticate, login as authorise, logout
from django.contrib import messages
from . models import *
import random


def index(request):
    current_year = datetime.datetime.now().year
    context = {
        'current_year': current_year
    }
    return render(request, "core_app/home.html", context)


def generator(request):
    context = {}
    return render(request, "core_app/generator.html", context)


def register(request):
    username = ""
    password = ""
    confirm_password = ""

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if not username:
            messages.error(request, "Username is required !")
        if not password:
            messages.error(request, "Password is required !")
        if not confirm_password:
            messages.error(request, "Confirm Password is required !")
        else:
            exists = User.objects.filter(username=username).exists()
            if exists:
                messages.error(request,
                               username + "'s profile already exists !")
            if len(password) < 6:
                messages.error(
                    request, "Password must be at least 6 or more chars")
            else:
                if not password == confirm_password:
                    messages.error(request, "Confirm Password Does'nt match !")
                else:
                    User.objects.create_user(
                        username=username, password=password).save()
                    messages.success(
                        request, "Your account has been created !")
                    return redirect("login")
    context = {
        'username': username,
    }
    return render(request, "core_app/register.html", context)


def login(request):
    username = ""
    password = ""

    if request.user.is_authenticated:
        username = ""
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username:
            messages.info(request, "Username is required !")
        if not password:
            messages.info(request, "Password is required !")
        else:
            check_auth = authenticate(username=username, password=password)
            if check_auth is not None:
                authorise(request, check_auth)
                if get_object_or_404(User, username=username).is_superuser:
                    return redirect('/admin')
                return redirect("index")
            else:
                messages.error(request, "Login Failed !")

    context = {
        'username': username,
    }
    return render(request, "core_app/login.html", context)


def signout(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    return redirect("index")


def generate_email(request):
    platform = ""
    first_name = ""
    last_name = ""
    full_email = ""
    generated_password = ""
    generated_email = ""

    if request.method == "POST":
        platform = request.POST["platform"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        if not platform:
            messages.error(request, "Platform cannot be empty !")
        if not first_name:
            messages.error(request, "First name cannot be empty !")
        if not last_name:
            messages.error(request, "Last name cannot be empty !")
        else:
            numbers = "1234567890"
            generated_num = ""
            names = [first_name, last_name]
            capital_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            small_letters = capital_letters.lower()
            special_chars = "@!~&_?%*#$=+^"
            num_of_chars = 2

            # GENERATE PASSWORD

            def generate_random(raw_string):
                generated_str = ""
                for index in range(1, num_of_chars):
                    random_num = random.randint(0, len(raw_string) - 1)
                    generated_str += raw_string[random_num]
                return generated_str

            for i in range(1, 16):
                cap_letter = generate_random(capital_letters)
                sml_letter = generate_random(small_letters)
                sp_chrs = generate_random(special_chars)
                nums = generate_random(numbers)

                pass_array = [cap_letter, sml_letter, sp_chrs, nums]

                random_num = random.randint(0, len(pass_array) - 1)
                if (pass_array[random_num] in generated_password):
                    pass_array.pop()
                    pass_array.reverse()
                    pass_array.append(pass_array[random_num - 1])
                    generated_password += pass_array[random_num]
                else:
                    generated_password += pass_array[random_num]

            # GENERATE EMAIL
            for i in range(1, 4):
                random_num = random.randint(0, len(numbers) - 1)
                generated_num += numbers[random_num]

            for i in range(1, 3):
                random_num = random.randint(0, len(names) - 1)
                if not names[random_num] != generate_email:
                    generated_email += names[random_num]
                else:
                    generated_email = names[0] + names[1]

            full_email = generated_email.lower() + generated_num + "@" + platform + ".com"

    context = {
        'platform': platform,
        'firs_name': first_name,
        'last_name': last_name,
        'generated_email': full_email.lower(),
        'generated_password': generated_password,
    }
    return render(request, "core_app/generator.html", context)


def profile(request, pk):
    user_profile = get_object_or_404(User, profile_id=pk)
    context = {
        "profile": user_profile,
    }
    return render(request, "core_app/profile.html", context)


def manage(request):
    emails = EmailInfo.objects.filter(user=request.user).all()
    context = {
        'emails': emails
    }
    return render(request, "core_app/manage.html", context)


def save_data(request):
    if request.method == "POST":
        platform = request.POST["platform"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        generated_email = request.POST["generated_email"]
        generated_password = request.POST["generated_password"]

        if generated_email == "" or generated_password == "":
            messages.error(
                request, "No email generated!, Generate email and try again.")
            return redirect("email-generator")
        else:
            new_email = EmailInfo.objects.create(
                platform=platform,
                first_name=first_name,
                last_name=last_name,
                generated_email_address=generated_email,
                generated_password=generated_password,
                user=request.user
            )
            new_email.save()
            messages.success(request, "Email Info Saved")
            return redirect("manage")


def remove_email(request, pk):
    email_data = get_object_or_404(EmailInfo, info_id=pk)
    if request.method == "POST":
        if email_data is not None:
            email_data.delete()
            return redirect("manage")
    context = {
        'data': email_data
    }
    return render(request, "core_app/delete-email.html", context)


def search_record(request):
    search_text = request.GET["search_text"]

    emails = EmailInfo.objects.filter(
        generated_email_address__icontains=search_text, user=request.user)

    context = {
        'emails': emails
    }
    return render(request, "core_app/manage.html", context)


def about(request):
    return render(request, "core_app/about.html")
