from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Institute, University, Director
from .serializers import CreateTimeTableSerializer


class CreateTimeTable(ListAPIView):
    """
    get:Список зарегистрированных институтов
    post:Зарегистрировать институт и директора
    """

    serializer_class = CreateTimeTableSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(Institute.objects.all())

    def post(self, request):
        review = CreateTimeTableSerializer(data=request.data)
        if review.is_valid():
            try:
                pass
            except KeyError:
                return Response({"error": "incorrect data"})
        data = request.data
        univ = University(name=data.get('university_name'), link=data.get('university_site'))
        univ.save()
        inst = Institute(university=univ, name=data.get('institute_name'), link=data.get('institute_site'))
        inst.save()
        director = Director(username=data.get('login'), first_name=data.get('name'),
                            institute=inst)
        director.set_password(data.get('password'))
        director.save()
        return Response('Successfully')
