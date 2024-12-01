from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserLocation
from django.utils import timezone
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import MissingPerson, SearchGroup, SearchMarker
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
import json


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "profile.html"


@api_view(['GET', 'POST'])
def message_list(request, missing_person_id):
    if request.method == 'GET':
        messages = Message.objects.filter(missing_person_id=missing_person_id).order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return JsonResponse({'messages': serializer.data})

    elif request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('message')
        user = User.objects.get(id=data.get('user_id')) 
        missing_person = MissingPerson.objects.get(id=missing_person_id)

        # Создаем новое сообщение
        new_message = Message.objects.create(
            text=text,
            author=user,
            missing_person=missing_person
        )
        
        # Возвращаем сообщение
        serializer = MessageSerializer(new_message)
        return JsonResponse({'message': 'Сообщение отправлено!', 'data': serializer.data})



class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['category_name']
    success_url = reverse_lazy('category_list')

from django.http import JsonResponse
from .models import Marker

# def get_markers(request):
#     if request.user.is_authenticated:
#         markers = Marker.objects.filter(user=request.user)
#         data = [{"volunteer": marker.user.username, "latitude": marker.latitude, "longitude": marker.longitude, "description": marker.description} for marker in markers]
#         return JsonResponse({'markers': data})
#     else:
#         return JsonResponse({'error': 'Не авторизован'}, status=403)


def get_all_markers(request):
    markers = Marker.objects.all()
    marker_data = [{
        'latitude': marker.latitude,
        'longitude': marker.longitude,
        'user': marker.user.username,
        'missing_person_id': marker.missing_person.id if marker.missing_person else None,  # Пример: передаем только ID пропавшего человека
        'missing_person_name': marker.missing_person.name if marker.missing_person else None,  # Или передаем имя пропавшего человека
        'created_at': marker.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for marker in markers]

    return JsonResponse({'markers': marker_data})

@csrf_exempt
@login_required
def save_marker(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lng = data.get('longitude')
            missing_person_id = data.get('missing_person_id')  # передаем id пропавшего человека

            if missing_person_id:
                # Проверяем существование пропавшего человека
                missing_person = MissingPerson.objects.get(id=missing_person_id)

                # Создаем маркер для текущего пользователя и привязываем к пропавшему человеку
                marker = Marker.objects.create(
                    latitude=lat,
                    longitude=lng,
                    user=request.user,  # текущий авторизованный пользователь
                    missing_person=missing_person  # Связываем с пропавшим человеком
                )
                return JsonResponse({'message': 'Метка сохранена'})
            else:
                return JsonResponse({'error': 'ID пропавшего человека не предоставлен'}, status=400)
        except MissingPerson.DoesNotExist:
            return JsonResponse({'error': 'Пропавший человек с таким ID не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Неверный запрос'}, status=400)

@csrf_exempt
@login_required
def remove_marker(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('latitude')
        lng = data.get('longitude')

        try:
            marker = Marker.objects.get(latitude=lat, longitude=lng, user=request.user)
            marker.delete()  # Удаляем метку
            return JsonResponse({'message': 'Метка удалена'})
        except Marker.DoesNotExist:
            return JsonResponse({'error': 'Метка не найдена'}, status=404)
    return JsonResponse({'error': 'Неверный запрос'}, status=400)


from django.http import JsonResponse
from .models import Marker

from django.http import JsonResponse
from .models import Marker

def get_markers(request):
    if request.user.is_authenticated:
        markers = Marker.objects.all()
        data = [{"User": marker.user.username, "latitude": marker.latitude, "longitude": marker.longitude,} for marker in markers]
        return JsonResponse({'markers': data})
    else:
        return JsonResponse({'error': 'Не авторизован'}, status=403)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    try:
        user_location = UserLocation.objects.get(user=user)
        user_location.is_active = False
        user_location.save()
    except UserLocation.DoesNotExist:
        pass


def get_active_user_locations(request):
    active_locations = UserLocation.objects.filter(is_active=True)
    locations_data = [{
        'latitude': loc.latitude,
        'longitude': loc.longitude,
        'username': loc.user.username,
    } for loc in active_locations]

    return JsonResponse({'locations': locations_data})


def login(request):
    return redirect("accounts/login")
    


def logout(request):
    return redirect("accounts/logout")
    

@login_required
def view_missing_person(request, person_id):
    missing_person = get_object_or_404(MissingPerson, id=person_id)
    search_group = None

    try:
        search_group = SearchGroup.objects.get(missing_person=missing_person, user=request.user)
    except SearchGroup.DoesNotExist:
        pass  # Пользователь не состоит в группе поиска

    user_location = UserLocation.objects.filter(user=request.user, is_active=True)
    return render(request, 'missing_person.html', {
        'missing_person': missing_person,
        'search_group': search_group,
        'user_location': user_location
    })



@login_required
def join_search_group(request, person_id):
    missing_person = get_object_or_404(MissingPerson, id=person_id)

    # Если пользователь еще не состоит в группе поиска, создаем новую запись
    if not SearchGroup.objects.filter(missing_person=missing_person, user=request.user).exists():
        SearchGroup.objects.create(missing_person=missing_person, user=request.user)

    return redirect('view_missing_person', person_id=person_id)


@login_required
def save_search_marker(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        missing_person_id = data.get('missing_person_id')

        if latitude is not None and longitude is not None and missing_person_id:
            missing_person = get_object_or_404(MissingPerson, id=missing_person_id)
            search_group = get_object_or_404(SearchGroup, missing_person=missing_person, user=request.user)

            # Создаем новую метку на карте
            SearchMarker.objects.create(
                search_group=search_group,
                latitude=latitude,
                longitude=longitude
            )

            return JsonResponse({'message': 'Метка сохранена!'}, status=200)

        return JsonResponse({'error': 'Недостаточно данных!'}, status=400)

    return JsonResponse({'error': 'Неверный метод запроса!'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from .models import UserLocation

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is not None and longitude is not None:
                user_locations = UserLocation.objects.filter(user=request.user)
                
                if user_locations.exists():
                    user_location = user_locations.first()
                    user_location.latitude = latitude
                    user_location.longitude = longitude
                    user_location.timestamp = timezone.now()
                    user_location.save()
                else:
                    user_location = UserLocation(user=request.user, latitude=latitude, longitude=longitude)
                    user_location.timestamp = timezone.now()
                    user_location.save()

                return JsonResponse({'message': 'Местоположение сохранено!'}, status=200)
            else:
                return JsonResponse({'error': 'Недостаточно данных!'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректные данные!'}, status=400)

    return JsonResponse({'error': 'Неверный метод запроса!'}, status=405)


def index(request):
    return render(request, 'index.html')

def Home(request):
    return render(request, 'home.html')


def get_volunteers(request):
    volunteers = CustomUser.objects.filter(status ="валантер")
    data = [{"name": volunteer.username, "latitude": volunteer.latitude, "longitude": volunteer.longitude} for volunteer in volunteers]
    return JsonResponse(data, safe=False)

# def get_markers(request):
#     markers = Marker.objects.all()
#     data = [{"volunteer": marker.volunteer.username, "latitude": marker.latitude, "longitude": marker.longitude, "description": marker.description} for marker in markers]
#     return JsonResponse(data, safe=False)

from django.shortcuts import render, get_object_or_404
from .models import MissingPerson

def show_missing_person_map(request, person_id):
    # Получаем пропавшего человека по ID
    missing_person = get_object_or_404(MissingPerson, id=person_id)

    # Местоположение пропавшего человека
    missing_person_lat = missing_person.last_known_latitude
    missing_person_lon = missing_person.last_known_longitude


    # Передаем данные в шаблон
    return render(request, 'missing_people.html', {
        'missing_person_name': missing_person.name,
        'missing_person_lat': missing_person_lat,
        'missing_person_lon': missing_person_lon,
        'missing_person_description': missing_person.description,
    })

# CATEGORY CRUD
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['category_name']
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['category_name']
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')





class ApplyHelpCreateView(LoginRequiredMixin, CreateView):
    model = ApplyHelp
    template_name = 'applyhelp_form.html'
    fields = ['description', 'image', 'category', 'is_active']  # Убираем 'user'
    success_url = reverse_lazy('help_list')

    def form_valid(self, form):
        # Проверка на статус пользователя
        if self.request.user.status != 'Нуждающийся':
            return HttpResponseForbidden("У вас нет прав для создания заявки.")
        
        # Устанавливаем пользователя, который создает заявку
        form.instance.user = self.request.user

        # Устанавливаем статус заявки, если он не указан
        if not form.instance.status:
            form.instance.status = 'В процессе'  # или любой другой статус по умолчанию
        
        return super().form_valid(form)


class HelpListView(LoginRequiredMixin, ListView):
    model = ApplyHelp
    template_name = 'help_list.html'
    context_object_name = 'apply_helps'
    def get_queryset(self):
        # Получаем статус пользователя
        user_status = self.request.user.status
        
        # Фильтруем по статусу
        queryset = ApplyHelp.objects.all()
        
        if user_status == 'валантер':
            queryset = queryset.filter(is_active=True)  # Заявки только от текущего волонтера
        elif user_status == 'Нуждающийся':
            queryset = queryset.filter(user=self.request.user)  # Только активные заявки для нуждающихся

        category_filter = self.request.GET.get('category', None)
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        
        return queryset

class HelpListViewUser(LoginRequiredMixin, ListView):
    model = ApplyHelp
    template_name = 'help_list.html'
    context_object_name = 'apply_helps'

    def get_queryset(self):
        # Фильтруем заявки, чтобы показывать только те, которые созданы текущим пользователем
        queryset = ApplyHelp.objects.filter(user=self.request.user)
        
        category_filter = self.request.GET.get('category', None)
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ApplyHelpUpdateView(LoginRequiredMixin, UpdateView):
    model = ApplyHelp
    template_name = 'applyhelp_form.html'
    fields = ['user', 'description', 'image', 'category', 'status', 'is_active']
    success_url = reverse_lazy('help_list')

    def get_queryset(self):
        if self.request.user.status == 'валантер':
            return ApplyHelp.objects.filter(user=self.request.user)
        return ApplyHelp.objects.none()

    def form_valid(self, form):
        if self.request.user.status != 'валантер':
            return HttpResponseForbidden("У вас нет прав для редактирования заявки.")
        return super().form_valid(form)


class ApplyHelpDeleteView(LoginRequiredMixin, DeleteView):
    model = ApplyHelp
    template_name = 'applyhelp_confirm_delete.html'
    success_url = reverse_lazy('help_list')

    def get_queryset(self):
        if self.request.user.status == 'валантер':
            return ApplyHelp.objects.filter(user=self.request.user)
        return ApplyHelp.objects.none()

# APPLICATION CRUD
# class ApplicationListView(ListView):
#     model = Application
#     template_name = 'application_list.html'
#     context_object_name = 'applications'


class ApplicationListView(ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'applications'
    paginate_by = 10  # Optional: Enables pagination with 10 items per page
    def get_queryset(self):
        queryset = super().get_queryset()
        user_query = self.request.GET.get('user', '').strip()
        status_query = self.request.GET.get('status', '').strip()

        # Filter the queryset based on search parameters
        if user_query:
            queryset = queryset.filter(user__username__icontains=user_query)
        if status_query:
            queryset = queryset.filter(status__icontains=status_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include search fields in the context to retain entered values in the form
        context['search_user'] = self.request.GET.get('user', '')
        context['search_status'] = self.request.GET.get('status', '')
        return context
    

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ApplyHelp, Application

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    template_name = 'application_form.html'
    fields = ['description',]  
    success_url = reverse_lazy('application_list')

    def form_valid(self, form):
        form.instance.user = self.request.user        
        applay_id = self.kwargs.get('applay_id')
        if applay_id:
            applay = get_object_or_404(ApplyHelp, pk=applay_id)
            form.instance.applay = applay
        else:
            return HttpResponseForbidden("Заявка не найдена или отсутствует")

        form.instance.status = 'впроцессе'

        # Далее сохраняем форму
        return super().form_valid(form)

class ApplicationUpdateView(UpdateView):
    model = Application
    template_name = 'application_form.html'
    fields = ['user', 'applay', 'description', 'status', 'is_active']
    success_url = reverse_lazy('application_list')


class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = 'application_confirm_delete.html'
    success_url = reverse_lazy('application_list')


# CHARITY COMPANY CRUD
class CharityCompanyListView(ListView):
    model = CharityCompany
    template_name = 'charitycompany_list.html'
    context_object_name = 'charity_companies'


class CharityCompanyCreateView(CreateView):
    model = CharityCompany
    template_name = 'charitycompany_form.html'
    fields = ['company_name', 'location', 'descriptions']
    success_url = reverse_lazy('charitycompany_list')


class CharityCompanyUpdateView(UpdateView):
    model = CharityCompany
    template_name = 'charitycompany_form.html'
    fields = ['company_name', 'location', 'descriptions']
    success_url = reverse_lazy('charitycompany_list')


class CharityCompanyDeleteView(DeleteView):
    model = CharityCompany
    template_name = 'charitycompany_confirm_delete.html'
    success_url = reverse_lazy('charitycompany_list')


# APPLICATION CHARITY CRUD
class ApplicationCharityListView(ListView):
    model = ApplicationCharity
    template_name = 'applicationcharity_list.html'
    context_object_name = 'application_charities'


from django.http import HttpResponseForbidden

class ApplicationCharityCreateView(CreateView):
    model = ApplicationCharity
    template_name = 'applicationcharity_form.html'
    fields = ['description','category'] 
    success_url = reverse_lazy('applicationcharity_list')

    def form_valid(self, form):
        # Проверка на статус пользователя
        if self.request.user.status != 'Нуждающийся':
            return HttpResponseForbidden("У вас нет прав для создания заявки.")
        
        form.instance.user = self.request.user
        form.instance.status = 'впроцессе'
        return super().form_valid(form)


class ApplicationCharityUpdateView(UpdateView):
    model = ApplicationCharity
    template_name = 'applicationcharity_form.html'
    fields = ['user', 'company_charity', 'description', 'status', 'is_active']
    success_url = reverse_lazy('applicationcharity_list')






class ApplicationCharityDeleteView(DeleteView):
    model = ApplicationCharity
    template_name = 'applicationcharity_confirm_delete.html'
    success_url = reverse_lazy('applicationcharity_list')


# USER LOCATION CRUD
class UserLocationListView(ListView):
    model = UserLocation
    template_name = 'userlocation_list.html'
    context_object_name = 'user_locations'


class UserLocationCreateView(CreateView):
    model = UserLocation
    template_name = 'userlocation_form.html'
    fields = ['user', 'latitude', 'longitude', 'is_active']
    success_url = reverse_lazy('userlocation_list')


class UserLocationUpdateView(UpdateView):
    model = UserLocation
    template_name = 'userlocation_form.html'
    fields = ['user', 'latitude', 'longitude', 'is_active']
    success_url = reverse_lazy('userlocation_list')


class UserLocationDeleteView(DeleteView):
    model = UserLocation
    template_name = 'userlocation_confirm_delete.html'
    success_url = reverse_lazy('userlocation_list')


# MARKER CRUD
class MarkerListView(ListView):
    model = Marker
    template_name = 'marker_list.html'
    context_object_name = 'markers'


class MarkerCreateView(CreateView):
    model = Marker
    template_name = 'marker_form.html'
    fields = ['volunteer', 'latitude', 'longitude', 'description']
    success_url = reverse_lazy('marker_list')


class MarkerUpdateView(UpdateView):
    model = Marker
    template_name = 'marker_form.html'
    fields = ['volunteer', 'latitude', 'longitude', 'description']
    success_url = reverse_lazy('marker_list')


class MarkerDeleteView(DeleteView):
    model = Marker
    template_name = 'marker_confirm_delete.html'
    success_url = reverse_lazy('marker_list')


from datetime import datetime

class MissingPersonListView(ListView):
    model = MissingPerson
    template_name = 'missing_person_list.html'
    context_object_name = 'missing_people'
    paginate_by = 10

    def get_queryset(self):
        queryset = MissingPerson.objects.all()

        # Получаем фильтры по датам из GET параметров
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        # Фильтрация по дате "с"
        if date_from:
            try:
                # Преобразуем строку в объект datetime
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(reported_time__gte=date_from)
            except ValueError:
                pass  # Если формат даты неверен, просто игнорируем фильтрацию по этой дате

        # Фильтрация по дате "по"
        if date_to:
            try:
                # Преобразуем строку в объект datetime
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(reported_time__lte=date_to)
            except ValueError:
                pass  # Если формат даты неверен, просто игнорируем фильтрацию по этой дате

        return queryset
