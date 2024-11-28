from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# View to handle Post-related operations
class PostView(APIView):
    permission_classes = [IsAuthenticated]

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

    def delete(self, request, pk):
        """
        Delete a post. Only the 'admin' or the post's creator can delete the post.
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

# View to handle Comment-related operations
class CommentView(APIView):
    permission_classes = [IsAuthenticated]

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
