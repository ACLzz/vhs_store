from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.db.utils import ProgrammingError

from store.models import User, Cassette
from store.forms import RegistrationForm, LoginForm

from datetime import datetime


def login_required(view, *args, **kwargs):
    def is_login(request, *args, **kwargs):
        if request.session['uid'] == 0:
            return redirect('index')
        return view(request, *args, **kwargs)
    return is_login


def session_check(view, *args, **kwargs):
    """ Set default values for session """
    def is_new(request, *args, **kwargs):
        try:
            request.session['uid']
        except KeyError or ProgrammingError:
            request.session['uid'] = 0
            request.session['nickname'] = ''
            request.session['avatar'] = ''
            request.session['cart'] = 0

        return view(request, *args, **kwargs)

    return is_new


@session_check
def index(request):
    return render(request, 'store/index.html')


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'store/registration.html'

    def form_valid(self, form):
        data = form.cleaned_data
        print(data['password'])
        data['path'] = 'my/path'
        birth = datetime(day=int(data['day']),
                         month=int(data['month']),
                         year=int(data['year']))
        # TODO avatar
        user = User(
            nickname=data['nickname'],
            first_name=data['first_name'],
            birth_date=birth,
            password=data['password'],
            avatar=data['path']
        )
        user.save()
        return redirect('index')

    def form_invalid(self, form):
        self.form_class.error = form.error
        return self.get(self.request)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'store/login.html'

    def form_valid(self, form):
        user = User.objects.filter(nickname=form.cleaned_data['nickname'])[0]
        self.request.session['uid'] = user.id
        self.request.session['nickname'] = user.nickname
        self.request.session['avatar'] = user.avatar
        return redirect('index')

    def form_invalid(self, form):
        self.form_class.error = "Invalid username or password."
        return self.get(self.request)


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('index')


@session_check
def cassettes_redirect(request):
    return redirect('cassettes', page=1)


@session_check
def cassettes(request, page):
    x = (page - 1) * 16
    y = page * 16
    cas = get_cassettes(x, y)

    count_p = Cassette.objects.count()

    if count_p % 16 == 0:
        count_p = int(Cassette.objects.count() / 16)
    else:
        count_p = Cassette.objects.count() // 16 + 1

    count_p_list = list(range(1, count_p + 1))

    if len(cas) == 16:
        next_p = page + 1
    else:
        next_p = None

    return render(request, 'store/cassettes.html', {"cassettes": cas, "next": next_p, "pages": count_p_list})


def get_cassettes(x, y):
    cas = []
    for cassette in Cassette.objects.all()[x:y]:
        cover = cassette.cover
        price = int(cassette.price)
        title = cassette.film_id.title

        descrpt = cassette.film_id.description
        descrpt_len = len(descrpt[:100].split())
        description = ' '.join(descrpt.split()[:descrpt_len]) + '...'

        cas_dict = {
            "cover": cover,
            "title": title,
            "description": description,
            "price": price,
        }
        cas.append(cas_dict)

    return cas


class ProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'store/profile.html'
