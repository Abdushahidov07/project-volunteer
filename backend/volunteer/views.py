from django.shortcuts import render, redirect
from django.http import JsonResponse
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

