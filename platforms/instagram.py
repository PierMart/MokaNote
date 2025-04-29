import os, time, yt_dlp
from faster_whisper import WhisperModel
from AI.resumeText import summarize_text_with_mistral
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log', 'instagram.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("instagram")

def download_instagram_audio(url, output_basename="instagram_audio"):
    """
    Télécharge l'audio d'une vidéo Instagram à partir de l'URL fournie.
    Retourne le chemin du fichier audio MP3 téléchargé.
    """
    abs_output_path = os.path.abspath(output_basename)
    ydl_opts = {
        'format': 'bestaudio/best',  # On récupère le meilleur flux audio
        'outtmpl': abs_output_path + '.%(ext)s',  # Nom de sortie
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Conversion en mp3
        }],
        'quiet': True,  # Pas de sortie verbeuse
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return abs_output_path + '.mp3'

def transcribe_audio(audio_path):
    model = WhisperModel("base", device="cpu")
    segments, info = model.transcribe(audio_path)
    logger.info(f"Langue détectée : {info.language}")
    texte = " ".join([segment.text for segment in segments])
    return texte

def handle_instagram(url: str):
    audio_path = download_instagram_audio(url, "instagram_audio")
    logger.info(f"Audio téléchargé à : {audio_path}")
    for _ in range(20):
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            break
        time.sleep(0.1)
    else:
        logger.error(f"Erreur : fichier {audio_path} introuvable ou vide après téléchargement !")
        return "Erreur : impossible de télécharger l'audio Instagram."
    texte = transcribe_audio(audio_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)
    try:
        resume = summarize_text_with_mistral(texte)
        return (
            f"Voici le texte de base :\n{texte}\n\n"
            f"Voici le texte résumé par Mistral :\n{resume}"
        )
    except Exception as e:
        return f"Erreur lors du résumé Mistral : {e}\nVoici le texte original :\n{texte}"
