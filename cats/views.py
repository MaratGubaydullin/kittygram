from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cat
from .serializers import CatSerializer


@api_view(['GET', 'POST'])
def cat_list(request):
    if request.method == 'POST':
        # Создаём объект сериализатора
        # и передаём в него данные из POST-запроса
        serializer = CatSerializer(data=request.data, many=False)
        # many=True, если надо обработать список объектов
        # если стоит many=True то отдельные оъекты не воспринимаются
        # вернется "Expected a list of items but got type dict."
        if serializer.is_valid():
            # Если полученные данные валидны —
            # сохраняем данные в базу через save().
            serializer.save()
            # Возвращаем JSON со всеми данными нового объекта
            # и статус-код 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Если данные не прошли валидацию —
        # возвращаем информацию об ошибках и соответствующий статус-код:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Получаем все объекты модели
    cats = Cat.objects.all()
    # Передаём queryset в конструктор сериализатора
    serializer = CatSerializer(cats, many=True,)
    # Если при обработке GET-запроса в сериализаторе не указать параметр
    # many=True, вернётся ошибка AttributeError.
    return Response(serializer.data)
