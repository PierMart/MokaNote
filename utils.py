from platforms.tiktok import handle_tiktok
from platforms.youtube import handle_youtube
from platforms.instagram import handle_instagram
def detect_platform(url: str) -> str:
    """
    Détecte la plateforme (YouTube, TikTok, Instagram) à partir d'une URL.
    Retourne 'youtube', 'tiktok', 'instagram' ou 'unknown'.
    """
    url = url.lower()
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "instagram.com" in url:
        return "instagram"
    else:
        return "unknown"




def handle_unknown(url: str):
    # Traitement pour les plateformes inconnues
    return f"Plateforme inconnue pour l'URL : {url}"


def process_url(url: str):
    """
    Détecte la plateforme et appelle la fonction appropriée.
    """
    platform = detect_platform(url)
    if platform == "youtube":
        return handle_youtube(url)
    elif platform == "tiktok":
        return handle_tiktok(url)
    elif platform == "instagram":
        return handle_instagram(url)
    else:
        return handle_unknown(url)