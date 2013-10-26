from StringIO import StringIO
import json
import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, mixins, generics, filters
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import ArticleSerializer, TagSerializer, CategorySerializer
from .serializers import ProductSerializer, Product
from .models import Article, Tag, Category
from .filters import ArticleFilter


# api root
@api_view(('GET',))
def api_root(request, format=None):

    return Response({
        'low-level-articles-list': reverse('blog:low-articles-list', request=request, format=format),
        'func-view-articles-list': reverse('blog:func-articles-list', request=request, format=format),
        'class-based-view-articles-list': reverse('blog:class-articles-list', request=request, format=format),
        'mixins-view-articles-list': reverse('blog:mixins-articles-list', request=request, format=format),
        'mixins-view-articles-list': reverse('blog:mixins-articles-list', request=request, format=format),
        'generic-articles-list': reverse('blog:generic-articles-list', request=request, format=format),
    })


# rest framework magic features
class ArticleViewSet(viewsets.ModelViewSet):
    # queryset = Article.objects.all()
    model = Article
    serializer_class = ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# low level django views
class JsonResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)


@csrf_exempt
def article_list(request):
    """
    Articles list/create
    """

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        print serializer.data

        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
        
        
@csrf_exempt
def article_detail(request, pk):
    """
    Retrieve, update or delete a article.
    """

    article = get_object_or_404(Article, pk=pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        put_data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=put_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)


# api using rest framewor helpers
@api_view(['GET', 'POST'])
def article_list_rest(request):
    """
    Article list using @api_view decorator.
    """

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def article_detail_rest(request, pk):
    """
    Article detail @api_veiw decorator.
    """

    article = get_object_or_404(Article, pk=pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        pass


# api using rest framewor helpers with class based views
class ArticleList(APIView):
    """
    Article list. Extend APIView class.
    """

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):

        print request.DATA

        serializer = ArticleSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    """
    Article detail. Extend APIView class.
    """

    def __get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.__get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.__get_object(pk)
        serializer = ArticleSerializer(article, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        article = self.__get_object(pk)
        serializer = ArticleSerializer(article, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.__get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#api using mixins
class ArticleListMixin(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleDetailMixins(mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#api using generic class based views
class ArticleListGeneric(generics.ListCreateAPIView):

    model = Article
    serializer_class = ArticleSerializer
    ordering = ('id', 'date', 'category')
    filter_class = ArticleFilter
    #filter_fields = ('category',)

    def get_queryset(self):
        """
        Some dummy actions with queryset
        """
        queryset = super(ArticleListGeneric, self).get_queryset()

        if 'user' in self.request.QUERY_PARAMS:
            queryset = queryset.filter(author__username__iexact=self.request.GET['user'])

        return queryset


class ArticleDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    model = Article
    serializer_class = ArticleSerializer


###########################
## play with serializers ##
###########################

@api_view(['GET', 'POST'])
def play_with_serializers(request):

    products = []
    products.append(Product(120, 25000, 'Porsche'))
    products.append(Product(122, 15000, 'Ford'))
    products.append(Product(130, 17000, 'Opel'))
    serializer = ProductSerializer(products)

    car = {"sku": 4, 'price': 3000, 'title': 'ford'}
    json_car = json.dumps(car)

    stream = StringIO(json_car)
    data = JSONParser().parse(stream)

    serializer_car = ProductSerializer(data=data)

    if serializer_car.is_valid():
        print serializer_car.save()
    else:
        print serializer_car.errors

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def play_model_serializers(request):

    # update
    article_data = {'title': u'New Cars',
                    'author': 1,
                    'category': 1,
                    'date': datetime.date(2014, 9, 16),
                    'tags': [1, 2, 3]}
    serializer_article = ArticleSerializer(Article.objects.get(pk=1),
                                           data=article_data)

    # create
    # article_data = {'title': u'Old Cars',
    #                 'author': 1,
    #                 'category': 1,
    #                 'date': datetime.date(2013, 9, 16),
    #                 'tags': [1, 2]}
    # serializer_article = ArticleSerializer(data=article_data)

    if serializer_article.is_valid():
        print 'Valid'
        print serializer_article.save()
    else:
        print serializer_article.errors


    # serializer_articles = ArticleSerializer(Article.objects.all())
    # print serializer_articles.is_valid()
    # print serializer_articles.errors

    return Response()
























