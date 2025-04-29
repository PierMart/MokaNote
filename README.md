# ☕ MokaNote — Le bot Discord doux comme un café

> *Votre compagnon de transcription sur Discord.*

MokaNote est un bot Discord qui vous aide à transcrire, résumer et organiser du contenu audio ou vidéo directement dans vos salons ou en privé. Pensé pour les communautés studieuses, créatives ou simplement curieuses, il rend la parole plus lisible.

---

## ✨ Fonctionnalités

- 🎙️ Transcription d’audio envoyé ou streamé
- 📹 Transcription de vidéos (Instagram,TikTok et Youtube et fichier en cours de dev...)
- 🧠 Résumé automatique avec IA (Mistral)
- 📌 Création de notes claires et organisées
- 🔒 Respect de la vie privée (aucun enregistrement conservé sans consentement)

---

## 🔧 Commandes principales

```
$url [fichier|url]     → Transcrit un audio ou une vidéo
```

---

## 🚀 Installation (auto-hébergement)

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/MokaNoteBot.git
cd MokaNoteBot
```

### 2. Configurer l'environnement

Crée un fichier `config.json` avec le contenu suivant :

```config.json
{
    "DISCORD_TOKEN": "VOTRE API",
    "MISTRAL_API_KEY": "VOTRE API"
}

### 3. Lancer le bot

```bash
npm install
npm start
```

> 📦 Compatible Node.js 18+

---

## 🛠️ Stack technique

- **Discord.py** pour l’interaction avec l’API Discord
- **Mistral / OpenRouter** pour la génération des résumés
- **Whisper** pour la transcription audio

---

## 🧭 Idées futures

- [ ] Transcription en direct des salons vocaux
- [ ] Intégration avec Notion ou Obsidian
- [ ] Export PDF ou Markdown
- [ ] Commandes personnalisables par serveur
- [ ] Mode "voix douce" avec synthèse vocale

---

## 🧑‍💻 Auteur

Développé par **Pierre Martinez**  
🎓 Bachelor DevOps — EPSI Nantes  
☕ Projet cosy issu de **MokaNote**  
> *Le confort d'une note chaude, même sur Discord.*

---
Lien pour l'utilisé :
https://discord.com/oauth2/authorize?client_id=1362150260201357464 

## 📄 Licence

Ce projet est sous licence MIT. Consulte le fichier [LICENSE](LICENSE) pour plus d’informations.
