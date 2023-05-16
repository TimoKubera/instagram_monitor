<a name="readme-top"></a>
[![MIT License][https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge]][https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt]
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/timokubera/instagram_monitor">
    <img src="https://raw.githubusercontent.com/TimoKubera/instagram_monitor/dev/instagram/data/img/instagram_logo.png" alt="Logo" width="160" height="160">
  </a>

  <h3 align="center"><b>Instagram Monitor</b></h3>

  <p align="center">
  Sucht auf Instagram-Seiten nach Änderungen und stellt sie graphisch dar.
    <br />
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Inhalt</summary>
  <ol>
    <li>
      <a href="#about-the-project">Über das Projekt</a>
    </li>
    <li>
      <a href="#requirements">Requirements</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">Lizenz</a></li>
    <li><a href="#contact">Kontakt</a></li>
  </ol>
</details>

<a name="about-the-project"></a>
<!-- ABOUT THE PROJECT -->
## Über das Projekt

<p>Der Instagram Monitor lädt alle Unterseiten einer Instagram-Benutzerseite herunter und überprüft, ob es seit der letzten Überprüfung Veränderungen gab.</p>
<p>Je nach Granularität(fein oder grob) werden dabei entweder nur die einzelnen Beiträge und Stories des Benutzers überprüft oder aber auch die Anzahl der Followers, Followings, Likes, Videoaufrufe, sowie die Kommentare auf seiner Benutzerseite.</p>
<p>Das Script teilt sich in zwei Phasen auf: </br>
Die <b>Download-Phase</b> und die <b>Monitor-Phase</b>.</p>

Anwendungen:
* Checke, ob es auf Instagram-Seiten, seit dem Letzten Aufruf, Veränderungen gibt
  * Checke, ob sich die "Posts-Subpage" verändert hat
  * Checke, ob sich die "IG-TV-Subpage" verändert hat
  * Checke, ob sich "Tagged-Subpage" verändert hat
  * Checke, ob sich die Anzahl der "Abonnenten", "abonniert", oder "Beiträge" verändert hat
* Lade die Instagram-Seiten herunter und speichere sie, inklusive der Änderungen, in einer HTML-Datei

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="requirements"></a>
<!-- GETTING STARTED -->
## Requirements
Es ist Python>=3.0 erforderlich, um das Programm auszuführen, sowie die Installation der folgenden Packages:
* lxml
* selenium
* selenium-wire

### Installation

1. Die Repo von <a href="https://github.com/timokubera/instagram_monitor">GitHub</a> clonen.
2. Abhängigkeiten installieren
   ```sh
   cd ~/path/to/instagram_monitor
   pip3 install -r requirements.txt
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="usage"></a>
<!-- USAGE EXAMPLES -->
## Usage
<b>Programm ausführen</b>
   ```sh
   cd ~/path/to/instagram_monitor
   python instagram/src/ig.py
   ```
</br>
<b>Beschreibung des Programmablaufes</b>
<p>In der <b>Download-Phase</b> wird eine neue Version von allen Unterseiten einer Benutzerseite heruntergeladen(Posts, IGTVs, Tagged, etc.).</p>
<p>Es werden maximal zwei Kopien der Seite archiviert("new.html" und "old.html"). </br>
Gibt es keine vorherige Version (das Verzeichnis ist leer), so wird die neu heruntergeladene Version direkt als "new.html" gespeichert. </br>
Gibt es bereits eine "new.html" im Verzeichnis, so wird sie in “old.html” umbenannt und die neue heruntergeladene Version als "new.html" gespeichert. </br>Gibt es sowohl eine "old.html" als auch eine "new.html" im Verzeichnis, so wird die "old.html" gelöscht und "new.html" wird in "old.html" umbenannt. Die neue heruntergeladene Version wird als "new.html" gepeichert.</p>


<p>Dynamische Informationen durch z.B. Javascript sammeln wir und speichern sie in der "profile_data.py" geordnet ab, um später darauf zugreifen zu können (z.B. Um zu erkennen ob ein Post ein Video oder Bild ist).</p>

<p>In der "instagram_object.py" speichern wir die Informationen ab, die wir später in der Monitor-Phase brauchen, um Unterschiede zu erkennen. So verhindern wir ein doppeltes Iterien über die .html Dateien. Z.B. sind das Followers und Followings-Anzahl, aber auch LXML-Objekte, die Posts beinhalten.</p>

<p>Es werden zusätzlich in der <b>Download-Phase</b> alle relativen Links zu absoluten Links umgewandelt und Video Thumbnails mit einem Standard Thumbnail ersetzt, da die Video Thumbnails nur für 24 Stunden gültig sind.</p>

<p>In der <b>Monitor-Phase</b> vergleichen wir jeweils zwei Versionen einer Unterseite oder Story und schauen, wo Unterschiede auftreten. Gibt es Unterschiede, so wird das jeweilige Objekt mit grüner Farbe hervorgehoben.</p>

<p>Auf dem folgenden Bild wird exemplarisch dargestellt, wie die Abonnenten-Anzahl, bzw. die abonniert-Anzahl hervorgehoben werden, wenn sich die Zahlen, seit dem letzten Seitenaufruf, verändert haben:
<img src="https://raw.githubusercontent.com/TimoKubera/instagram_monitor/dev/instagram/data/img/ph-profile.png" alt="changed-follower-count-following-count"></p>

<p>Auf dem folgenden Bild ist zu sehen, dass die ersten drei Instagram-Posts, seit dem letzten Seitenaufruf, neu hinzugekommen sind. Außerdem hat sich bei den Posts 4 und 5 die Anzahl der Kommentare, bzw. der Likes, verändert und beim dritten Post hat sich beides verändert.
<img src="https://raw.githubusercontent.com/TimoKubera/instagram_monitor/dev/instagram/data/img/ph-posts.png" alt="changed-posts">
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="license"></a>
<!-- LICENSE -->
## Lizenz

Das Projekt wurde unter der MIT-Lizenz veröffentlicht. Siehe in die `LICENSE.txt` für weitere Informationen.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="contact"></a>
<!-- CONTACT -->
## Kontakt
Mail: [mail@timokubera.it](mailto:mail@timokubera.it)

Project Link: [https://github.com/TimoKubera/IIRA](https://github.com/TimoKubera/IIRA)

<p align="right">(<a href="#readme-top">back to top</a>)</p>