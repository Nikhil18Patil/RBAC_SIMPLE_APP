from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# View to handle Post-related operations
class PostView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="Retrieve Posts",
        operation_description="Retrieve a list of all posts.",
        responses={
            200: openapi.Response(
                description="List of posts retrieved successfully.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "title": "Sample Post",
                            "content": "This is a sample post.",
                            "created_by": "username",
                            "created_at": "2024-12-01T12:34:56Z"
                        }
                    ]
                }
            ),
            500: openapi.Response(
                description="Error retrieving posts.",
                examples={
                    "application/json": {
                        "message": "Error retrieving posts: <error_details>"
                    }
                }
            ),
        }
    )
    def get(self, request):
        """
        Retrieve all posts.
        """
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error retrieving posts: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_id="Create Post",
        operation_description="Create a new post.",
        request_body=PostSerializer,
        responses={
            201: openapi.Response(
                description="Post created successfully.",
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "New Post",
                        "content": "This is a new post.",
                        "created_by": "username",
                        "created_at": "2024-12-01T12:34:56Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation errors occurred.",
                examples={
                    "application/json": {
                        "title": ["This field is required."],
                        "content": ["This field is required."]
                    }
                }
            ),
            500: openapi.Response(
                description="Error creating post.",
                examples={
                    "application/json": {
                        "message": "Error creating post: <error_details>"
                    }
                }
            ),
        }
    )
    def post(self, request):
        """
        Create a new post.
        """
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Error creating post: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_id="Delete Post",
        operation_description="Delete a post by its ID. Only the admin or the creator of the post can delete it.",
        responses={
            200: openapi.Response(
                description="Post deleted successfully.",
                examples={
                    "application/json": {
                        "message": "Post deleted successfully"
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden. User is not allowed to delete this post.",
                examples={
                    "application/json": {
                        "message": "You cannot delete this post."
                    }
                }
            ),
            404: openapi.Response(
                description="Post not found.",
                examples={
                    "application/json": {
                        "message": "Post not found."
                    }
                }
            ),
            500: openapi.Response(
                description="Error deleting post.",
                examples={
                    "application/json": {
                        "message": "Error deleting post: <error_details>"
                    }
                }
            ),
        }
    )
    def delete(self, request, pk):
        """
        Delete a post. Only the admin or the post's creator can delete the post.
        """
        try:
            post = Post.objects.get(pk=pk)
            if request.user.role != 'admin' and request.user != post.created_by:
                return Response({"message": "You cannot delete this post."}, status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Error deleting post: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Comment View
class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="Create Comment",
        operation_description="Create a new comment for a post.",
        request_body=CommentSerializer,
        responses={
            201: openapi.Response(
                description="Comment created successfully.",
                examples={
                    "application/json": {
                        "id": 1,
                        "post": 1,
                        "content": "This is a comment.",
                        "created_by": "username",
                        "created_at": "2024-12-01T12:34:56Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation errors occurred.",
                examples={
                    "application/json": {
                        "post": ["This field is required."],
                        "content": ["This field is required."]
                    }
                }
            ),
            500: openapi.Response(
                description="Error creating comment.",
                examples={
                    "application/json": {
                        "message": "Error creating comment: <error_details>"
                    }
                }
            ),
        }
    )
    def post(self, request):
        """
        Create a new comment.
        """
        try:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Error creating comment: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)