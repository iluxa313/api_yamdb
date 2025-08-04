from rest_framework import routers
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import (CategoryViewSet, GenreViewSet, UserViewSet, GetTokenAPIView,
					TitleViewSet, ReviewViewSet, CommentViewSet, SignUpAPIView)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
				CommentViewSet, basename='comments')

urlpatterns = [
	path('', include(router.urls)),
	path('auth/signup/', SignUpAPIView.as_view()),
	path('auth/token/', GetTokenAPIView.as_view(), name='token_obtain_pair'),
]

if settings.DEBUG:
	urlpatterns += static(
		settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
	)
