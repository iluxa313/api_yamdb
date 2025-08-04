from rest_framework import (viewsets, views, permissions, mixins, status,
                            filters, pagination, serializers)
from .serializers import (UserSerializer, CategorySerializer, CommentSerializer, SignUpUserSerializer,
                          UserCreateSerializer, GenreSerializer, ReviewSerializer, MyTokenObtainPairSerializer,
                          TitleWriteSerializer, TitleReadSerializer)
from reviews.models import User, Category, Genre, Title, Review, Comment, ConfirmationCode
from rest_framework.decorators import action
from .permissions import AdminPermission, UserOrModeratorPermission, AdminPermissionForUsers
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
import uuid


class ListCreateDeleteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                              mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


def send_mails(user, email):
    confirmation_code = str(uuid.uuid4().hex)[:6]
    ConfirmationCode.objects.filter(user=user).delete()
    ConfirmationCode.objects.create(user=user, code=confirmation_code)
    send_mail(
        'Код подтверждения',
        f'Вот ваш код подтверждения, не сообщайте никому: {confirmation_code}',
        'yamdbmoderation@gmail.com',
        [f'{email}', ],
        fail_silently=False,
    )


class GetTokenAPIView(views.APIView):

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class SignUpAPIView(views.APIView):

    def post(self, request):
        serializer = SignUpUserSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')

        user = User.objects.filter(username=username).first()
        email_user = User.objects.filter(email=email).first()

        if user and email_user:
            existing_user = user if user else email_user
            send_mails(existing_user, email)
            return Response(status=status.HTTP_200_OK)

        elif serializer.is_valid():
            user = serializer.save()
            send_mails(user, email)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermissionForUsers,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = pagination.PageNumberPagination
    search_fields = ('username',)
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        me = request.user
        data = request.data.copy()
        data['role'] = request.user.role
        serializer = UserSerializer(me, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            slug = request.data.get('slug')
            if Category.objects.filter(slug=slug).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            slug = request.data.get('slug')
            if Genre.objects.filter(slug=slug).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'category__slug', 'year')

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        return super().get_serializer_class()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserOrModeratorPermission,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.AllowAny(),)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title, author=self.request.user).exists():
            raise serializers.ValidationError(
                {'detail': 'Вы уже оставляли отзыв на это произведение.'},
                code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (UserOrModeratorPermission,)

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return (permissions.AllowAny(),)
        return super().get_permissions()

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
