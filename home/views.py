from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Person
from .serializers import PeopleSerializer,LoginSerializer,RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator




# Create your views here.
@api_view(['GET','POST','PUT'])
def index(request):
    course={
        'course_name':'pyhton',
        'features':['Django','flask','restAPI'],
        'course_provider':'Ayush Bisht'
    }
    if request.method=='GET':
        print ('You hit a get method')
        return Response(course)


    elif request.method=='POST':
        print ('You hit a post method')
        data=request.data
        print('****')
        print(data)
        print(data['age'])
        return Response(course)
    
    elif request.method=='PUT':
        print ('You hit a put method')
        return Response(course)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method=='GET':
        objs=Person.objects.filter(color__isnull=False)
        serializer=PeopleSerializer(objs,many=True)
        return Response(serializer.data) 
    
    elif request.method=='POST':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method=='PUT':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    elif request.method=='PATCH':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    else:
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'Person deleted successfully'})
    
@api_view(['POST'])
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)
    if serializer.is_valid():
        data=serializer.data
        print(data)
        return Response({'message':'Posted Successfully'},status=status.HTTP_200_OK)
    
    return Response (serializer.errors)

# Same but using APIView 

class personAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self,request):
        # objs=Person.objects.filter(color__isnull=False)
        # serializer=PeopleSerializer(objs,many=True)
        # return Response(serializer.data)
        # return Response({'message':'This is get request '})

        # Using pagination to split the data into pages /?page=2 do this after the url to change the page
        # try:
            objs=Person.objects.all()
            page=request.GET.get('page',1)
            page_size=2
            paginator=Paginator(objs,page_size)
            serializer=PeopleSerializer(paginator.page(page),many=True)
            return Response(serializer.data)
            
        # except Exception as e:
        #     return Response({
        #         status:False,
        #         'message':'Page end Invalid page number'
        #     })

    def post(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # return Response({'message':'This is post request '})
    
    def put(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # return Response({'message':'This is put request '})
    
    def patch(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # return Response({'message':'This is patch request '})
    
    def delete(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'Person deleted successfully'})
        # return Response({'message':'This is delete request '})

# Best way to perform CRUD operations
class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()


class RegisterAPI(APIView):

    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                status:False,
                'message':"Error while registering user"
            },status.HTTP_404_NOT_FOUND)
        
        serializer.save()
        return Response({'message':'User Registered successfully'},status.HTTP_200_OK)








        
    




