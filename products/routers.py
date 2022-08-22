from rest_framework.routers import SimpleRouter

from .views import CommentViewSet

router = SimpleRouter()

router.register('comments', CommentViewSet)
