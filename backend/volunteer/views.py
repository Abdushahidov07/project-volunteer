from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserLocation
from django.utils import timezone
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


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


@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        try:
            # Получаем данные из запроса
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is not None and longitude is not None:
                # Получаем все записи для текущего пользователя
                user_locations = UserLocation.objects.filter(user=request.user)
                
                if user_locations.exists():
                    # Если запись уже существует, обновляем её
                    user_location = user_locations.first()  # Берем первую запись, можно применить другие фильтры
                    user_location.latitude = latitude
                    user_location.longitude = longitude
                    user_location.timestamp = timezone.now()
                    user_location.save()
                else:
                    # Если записей нет, создаем новую
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


def get_volunteers(request):
    volunteers = CustomUser.objects.filter(status ="валантер")
    data = [{"name": volunteer.username, "latitude": volunteer.latitude, "longitude": volunteer.longitude} for volunteer in volunteers]
    return JsonResponse(data, safe=False)

def get_markers(request):
    markers = Marker.objects.all()
    data = [{"volunteer": marker.volunteer.username, "latitude": marker.latitude, "longitude": marker.longitude, "description": marker.description} for marker in markers]
    return JsonResponse(data, safe=False)

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




class HelpListView(ListView):
    model = ApplyHelp
    template_name = 'help_list.html'
    context_object_name = 'apply_helps'
    
    def get_queryset(self):
        queryset = ApplyHelp.objects.all()
        category_filter = self.request.GET.get('category', None)
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ApplyHelpCreateView(CreateView):
    model = ApplyHelp
    template_name = 'applyhelp_form.html'
    fields = ['user', 'description', 'image', 'category', 'status', 'is_active']
    success_url = reverse_lazy('help_list')


class ApplyHelpUpdateView(UpdateView):
    model = ApplyHelp
    template_name = 'applyhelp_form.html'
    fields = ['user', 'description', 'image', 'category', 'status', 'is_active']
    success_url = reverse_lazy('applyhelp_list')


class ApplyHelpDeleteView(DeleteView):
    model = ApplyHelp
    template_name = 'applyhelp_confirm_delete.html'
    success_url = reverse_lazy('applyhelp_list')


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
    


class ApplicationCreateView(CreateView):
    model = Application
    template_name = 'application_form.html'
    fields = ['user', 'applay', 'description', 'status', 'is_active']
    success_url = reverse_lazy('application_list')


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


class ApplicationCharityCreateView(CreateView):
    model = ApplicationCharity
    template_name = 'applicationcharity_form.html'
    fields = ['user', 'company_charity', 'description', 'status', 'is_active']
    success_url = reverse_lazy('applicationcharity_list')


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



class MissingPersonListView(ListView):
    model = MissingPerson
    template_name = 'missing_person_list.html'
    context_object_name = 'missing_people'
    paginate_by = 10  # Можно настроить, сколько пропавших людей выводить на страницу

    def get_queryset(self):
        queryset = MissingPerson.objects.all()

        # Получаем фильтр по дате из GET параметров
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            queryset = queryset.filter(reported_time__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(reported_time__lte=date_to)

        return queryset