from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, SavedAnime, WatchLater
from .serializers import UserProfileSerializer, SavedAnimeSerializer, WatchLaterAnimeSerializer
from core.models import Anime



class UserProfileView(APIView):
    """
    API view to retrieve the authenticated user's profile.

    Methods:
    - GET: Retrieves the user's profile details.
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the user profile for the authenticated user.
        """
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user_profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFavouritesShows(generics.ListCreateAPIView):
    """
    API view to list and add animes to the user's saved favorites.

    Methods:
    - GET: Retrieves the list of saved favorite animes for the authenticated user.
    - POST: Adds an anime to the saved favorites list.
    """
    
    serializer_class = SavedAnimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter and return the saved favorite animes for the authenticated user.
        """
        return SavedAnime.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Create a new favorite anime entry if it doesn't already exist.
        """
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Custom POST method for adding an anime to favorites.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserWatchLaterShows(generics.ListCreateAPIView):
    """
    API view to list and add animes to the user's "watch later" list.

    Methods:
    - GET: Retrieves the list of "watch later" animes for the authenticated user.
    - POST: Adds an anime to the "watch later" list.
    """
    
    serializer_class = WatchLaterAnimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter and return the watch later animes for the authenticated user.
        """
        return WatchLater.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Create a new watch later anime entry if it doesn't already exist.
        """
        anime_id = self.request.data.get('id', None)
        if not anime_id:
            raise ValueError("Anime ID is required.")
        
        try:
            anime = Anime.objects.get(unique_id=anime_id)
            serializer.save(user=self.request.user, anime=anime)
        except Anime.DoesNotExist:
            raise ValueError("Anime not found.")
    
    def create(self, request, *args, **kwargs):
        """
        Custom POST method for adding an anime to watch later.
        """
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserAnimeRemove(APIView):
    """
    API view to remove an anime from the user's saved or watch later list.

    Methods:
    - DELETE: Removes an anime from the user's saved or watch later list.
    """
    
    permission_classes = [IsAuthenticated]

    def delete(self, request, list_type):
        """
        Remove an anime from the specified list (either favorites or watch later).
        """
        saved_anime_id = request.data.get('id')

        if not saved_anime_id:
            return Response({'message': 'Anime ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        model = None
        if list_type == "favourite":
            model = SavedAnime
        elif list_type == "watch_later":
            model = WatchLater
        else:
            return Response({'message': 'Invalid list type.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = model.objects.get(user=request.user, anime__unique_id=saved_anime_id)
            item.delete()
            return Response({'message': f'Anime removed from {list_type} list.'}, status=status.HTTP_200_OK)

        except model.DoesNotExist:
            return Response({'message': 'Anime not found in the specified list.'}, status=status.HTTP_404_NOT_FOUND)



class CheckListStatus(APIView):
    """
    API view to check whether a given anime (by unique_id) 
    is in the authenticated user's favorites or watch-later lists.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        GET /user/check_status/<anime_unique_id>/
        Returns:
          {
            "exist": bool,
            "existsIn": ["SavedAnime", "WatchLater"]
          }
        """
        exist, existsIn = self.checkAnimeList(request.user, id)
        return Response({
            'exist': exist,
            'existsIn': existsIn
        }, status=status.HTTP_200_OK)

    def checkAnimeList(self, user, anime_unique_id):
        existsIn = []

        # Check the user's favorites
        if SavedAnime.objects.filter(
            user=user,
            anime__unique_id=anime_unique_id
        ).exists():
            existsIn.append('SavedAnime')

        # Check the user's watch-later
        if WatchLater.objects.filter(
            user=user,
            anime__unique_id=anime_unique_id
        ).exists():
            existsIn.append('WatchLater')

        return bool(existsIn), existsIn