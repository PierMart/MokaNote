import os, yt_dlp, subprocess
from faster_whisper import WhisperModel
from AI.resumeText import summarize_text_with_mistral
import io
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log', 'youtube.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("youtube")

def get_youtube_audio_stream_url(url):
    """
    Récupère l'URL du flux audio direct d'une vidéo YouTube sans la télécharger.
    Peut utiliser un fichier de cookies pour contourner certaines restrictions.
    """
    cookies_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cookies.txt'))
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'cookiesfromfile': cookies_path if os.path.exists(cookies_path) else None,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

def transcribe_youtube_stream(url):
    audio_stream_url = get_youtube_audio_stream_url(url)
    # Utilise ffmpeg pour convertir le flux audio en wav PCM mono 16kHz sur stdout
    ffmpeg_cmd = [
        'ffmpeg', '-i', audio_stream_url,
        '-f', 'wav', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', '-'
    ]
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    # Crée un buffer en mémoire
    audio_buffer = io.BytesIO(ffmpeg_proc.stdout.read())
    ffmpeg_proc.stdout.close()
    ffmpeg_proc.wait()
    # Transcription avec faster-whisper
    model = WhisperModel("base", device="cpu")
    segments, info = model.transcribe(audio_buffer)
    logger.info(f"Langue détectée : {info.language}")
    texte = " ".join([segment.text for segment in segments])
    return texte

# Exemple d'utilisation :
# texte = transcribe_youtube_stream('https://youtube.com/shorts/qBNojENvyfQ?si=VAQU4sdu7xdzbQCd')
# logger.info(texte)

from urllib.parse import unquote, urlparse

def handle_youtube(url: str):
    url = url.strip()
    if url.startswith("?url="):
        url = url[5:]
    url = unquote(url)
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return "URL YouTube invalide."
    try:
        audio_path = download_youtube_audio(url, "youtube_audio")
    except RuntimeError as e:
        # Gestion d'erreur élégante pour Discord
        msg = str(e)
        if "cookies" in msg.lower() or "sign in to confirm" in msg.lower():
            return ("Erreur lors du téléchargement YouTube : accès refusé ou vérification anti-bot. "
                    "Merci de vérifier/rafraîchir votre fichier cookies.txt exporté depuis une session YouTube connectée.")
        return f"Erreur lors du téléchargement YouTube : {msg}"
    logger.info(f"Audio téléchargé à : {audio_path}")
    for _ in range(20):
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            break
        time.sleep(0.1)
    else:
        logger.error(f"Erreur : fichier {audio_path} introuvable ou vide après téléchargement !")
        return "Erreur : impossible de télécharger l'audio YouTube."
    texte = transcribe_audio(audio_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)
    try:
        resume = summarize_text_with_mistral(texte)
        return (
            f"Voici la transcription :\n{texte}\n\n"
            f"Voici le résumé par Mistral :\n{resume}"
        )
    except Exception as e:
        return f"Erreur lors du résumé Mistral : {e}\nVoici la transcription :\n{texte}"
