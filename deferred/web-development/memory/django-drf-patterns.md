# Django + DRF Common Patterns

**Version**: 1.0.0
**Last Updated**: 2025-10-16

This document contains proven patterns for Django REST Framework API development.

## Core Philosophy

- **RESTful Design**: Use standard HTTP methods (GET, POST, PUT, DELETE)
- **Serializer-First**: Validation and transformation in serializers
- **ViewSet Architecture**: DRY principle with ViewSets and routers
- **Permission-Based Security**: Authentication + authorization on every endpoint

## Pattern 1: Model-Serializer-ViewSet Trio

**The Standard CRUD API Pattern**

**Model** (`models.py`):
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.title
```

**Serializer** (`serializers.py`):
```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'excerpt',
            'author', 'author_name',
            'is_published', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_excerpt(self, obj):
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters")
        return value

    def validate(self, attrs):
        # Cross-field validation
        if attrs.get('is_published') and not attrs.get('content'):
            raise serializers.ValidationError("Cannot publish post without content")
        return attrs
```

**ViewSet** (`views.py`):
```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['is_published', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        # Users only see published posts unless they're the author
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)
        if not self.request.user.is_staff:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(is_published=True) | Q(author=self.request.user)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_posts = self.get_queryset()[:10]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = True
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
```

**URLs** (`urls.py`):
```python
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = router.urls
```

**Resulting Endpoints**:
```
GET    /api/posts/                  List posts (paginated)
POST   /api/posts/                  Create post
GET    /api/posts/{id}/             Retrieve post
PUT    /api/posts/{id}/             Update post
PATCH  /api/posts/{id}/             Partial update
DELETE /api/posts/{id}/             Delete post
GET    /api/posts/recent/           Custom action (last 10)
POST   /api/posts/{id}/publish/     Custom action (publish)
```

## Pattern 2: Custom Permissions

**permissions.py**:
```python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Object owner can edit, others can only read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS) allowed for all
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for author
        return obj.author == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Only owner or admin can access
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class IsPublishedOrAuthor(permissions.BasePermission):
    """
    Published objects are public, unpublished only for author
    """
    def has_object_permission(self, request, view, obj):
        if obj.is_published:
            return True
        return obj.author == request.user
```

**Usage in ViewSet**:
```python
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
        IsPublishedOrAuthor
    ]
```

## Pattern 3: Nested Serializers

**Use Case**: Include related objects in API response

**Models**:
```python
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    website = models.URLField(blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Serializers**:
```python
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'username', 'bio', 'website']


class PostDetailSerializer(serializers.ModelSerializer):
    """Extended serializer with nested relationships"""
    author = AuthorSerializer(source='author.author', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content',
            'author', 'comments', 'comment_count',
            'created_at', 'updated_at'
        ]
```

**ViewSet with Multiple Serializers**:
```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer  # Nested data for detail view
        return PostSerializer  # Minimal data for list view

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            # Optimize for detail view with nested data
            queryset = queryset.prefetch_related('comments', 'comments__author')
        return queryset.select_related('author__author')
```

## Pattern 4: Pagination Strategies

**Default Pagination** (`settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

**Custom Pagination**:
```python
from rest_framework.pagination import PageNumberPagination, CursorPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostCursorPagination(CursorPagination):
    """Better for large datasets, prevents deep pagination performance issues"""
    page_size = 20
    ordering = '-created_at'  # Must have ordering
```

**Usage**:
```python
class PostViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination

    @action(detail=False)
    def all(self, request):
        """Large dataset endpoint"""
        queryset = self.filter_queryset(self.get_queryset())
        paginator = LargeResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
```

## Pattern 5: Filtering and Search

**Install django-filter**:
```bash
pip install django-filter
```

**Settings** (`settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

**ViewSet with Filtering**:
```python
from django_filters import rest_framework as filters

class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    author_name = filters.CharFilter(field_name='author__username', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['is_published', 'author']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
```

**API Usage**:
```
GET /api/posts/?is_published=true
GET /api/posts/?title__icontains=django
GET /api/posts/?created_after=2025-01-01
GET /api/posts/?search=tutorial
GET /api/posts/?ordering=-created_at
GET /api/posts/?author_name=john&is_published=true
```

## Pattern 6: Bulk Operations

**Bulk Create**:
```python
class PostViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        posts = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

**Bulk Update**:
```python
@action(detail=False, methods=['patch'])
def bulk_update(self, request):
    ids = [item['id'] for item in request.data]
    posts = Post.objects.filter(id__in=ids, author=request.user)

    updated_posts = []
    for data in request.data:
        post = posts.get(id=data['id'])
        serializer = self.get_serializer(post, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_posts.append(serializer.data)

    return Response(updated_posts)
```

**Bulk Delete**:
```python
@action(detail=False, methods=['delete'])
def bulk_delete(self, request):
    ids = request.data.get('ids', [])
    deleted_count = Post.objects.filter(
        id__in=ids,
        author=request.user
    ).delete()[0]

    return Response({
        'deleted': deleted_count
    }, status=status.HTTP_204_NO_CONTENT)
```

## Pattern 7: File Upload

**Model**:
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    attachments = models.FileField(upload_to='attachments/', blank=True)
```

**Serializer**:
```python
class PostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'image_url', 'attachments']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def validate_image(self, value):
        # Validate file size (max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be less than 5MB")

        # Validate file type
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("Only image files are allowed")

        return value
```

**ViewSet**:
```python
from rest_framework.parsers import MultiPartParser, FormParser

class PostViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

**Client Usage** (JavaScript):
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/api/posts/123/upload_image/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token YOUR_TOKEN'
  },
  body: formData
});
```

## Pattern 8: API Versioning

**URL Path Versioning** (`urls.py`):
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSetV1)

router_v2 = DefaultRouter()
router_v2.register(r'posts', PostViewSetV2)

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v2/', include(router_v2.urls)),
]
```

**Or Accept Header Versioning** (`settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

**ViewSet Version Handling**:
```python
class PostViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return PostSerializerV2
        return PostSerializerV1
```

## Pattern 9: API Documentation (drf-spectacular)

**Install**:
```bash
pip install drf-spectacular
```

**Settings** (`settings.py`):
```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My API',
    'DESCRIPTION': 'API for my awesome project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

**URLs**:
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

**Enhanced Documentation with Decorators**:
```python
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class PostViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary="List all posts",
        description="Returns a paginated list of posts. Users see published posts unless they're the author.",
        parameters=[
            OpenApiParameter('is_published', type=bool, description='Filter by publication status'),
            OpenApiParameter('search', type=str, description='Search in title and content'),
        ],
        responses={200: PostSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Example Response',
                value=[
                    {
                        'id': 1,
                        'title': 'My First Post',
                        'content': '...',
                        'author_name': 'john',
                        'created_at': '2025-10-16T10:30:00Z'
                    }
                ],
                response_only=True,
            )
        ]
    )
    def list(self, request):
        return super().list(request)

    @extend_schema(
        summary="Publish a post",
        description="Makes an unpublished post publicly visible",
        request=None,
        responses={200: PostSerializer},
    )
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = True
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
```

## Pattern 10: Rate Limiting

**Install**:
```bash
pip install django-ratelimit
```

**Usage**:
```python
from django_ratelimit.decorators import ratelimit

class PostViewSet(viewsets.ModelViewSet):
    @ratelimit(key='user', rate='10/m', method='POST')
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        # Limited to 10 requests per minute per user
        ...
```

**Or use DRF throttling** (`settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    }
}
```

**Custom Throttle**:
```python
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    rate = '10/min'

class SustainedRateThrottle(UserRateThrottle):
    rate = '1000/day'

class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
```

## Testing Patterns

**Fixture Setup**:
```python
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from myapp.models import Post

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(user, api_client):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def post(user):
    return Post.objects.create(
        title='Test Post',
        content='Test content',
        author=user
    )
```

**API Tests**:
```python
@pytest.mark.django_db
class TestPostAPI:
    def test_list_posts(self, api_client):
        response = api_client.get('/api/posts/')
        assert response.status_code == 200

    def test_create_post_authenticated(self, authenticated_client):
        data = {'title': 'New Post', 'content': 'Content'}
        response = authenticated_client.post('/api/posts/', data)
        assert response.status_code == 201
        assert response.data['title'] == 'New Post'

    def test_create_post_unauthenticated(self, api_client):
        data = {'title': 'New Post', 'content': 'Content'}
        response = api_client.post('/api/posts/', data)
        assert response.status_code == 401

    def test_update_own_post(self, authenticated_client, post):
        data = {'title': 'Updated Title'}
        response = authenticated_client.patch(f'/api/posts/{post.pk}/', data)
        assert response.status_code == 200
        assert response.data['title'] == 'Updated Title'

    def test_update_others_post(self, authenticated_client, user, db):
        other_user = User.objects.create_user(username='other', password='pass')
        other_post = Post.objects.create(
            title='Other Post',
            content='Content',
            author=other_user
        )
        data = {'title': 'Hacked Title'}
        response = authenticated_client.patch(f'/api/posts/{other_post.pk}/', data)
        assert response.status_code == 403
```

---

*These patterns are battle-tested with Django 4.2+ and Django REST Framework 3.14+*
*Always write tests for permissions and edge cases*
