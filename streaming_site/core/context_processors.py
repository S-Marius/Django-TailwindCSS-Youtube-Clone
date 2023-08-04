from video.models import Playlist  # Import your Playlist model

def user_playlists(request):
    user_playlists = []
    if request.user.is_authenticated:
        user_playlists = Playlist.objects.filter(user=request.user)

    return {'user_playlists': user_playlists}
