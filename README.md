# Download installer

-- [Download Keezy_setup.exe](https://github.com/celbax95/Keezy_Installer/raw/main/Keezy_setup.exe) --


## Ignorer l'antivirus

Ignorer l'antivirus. Je n'ai pas de liscence applicative windows pour qu'elle soit reconnue et ce sera le cas tant que l'application sera en beta.

Ajouter une exception avec le path d'installation par defaut :
 - WIN + R
 - Taper "cmd"
 - CTRL + SHIFT + ENTER
 - Cliquer "OUI"
 - Coller la ligne suivante
  - powershell -Command Add-MpPreference -ExclusionPath "\"C:\Program Files (x86)\Keezy\""


Il est possible d'accéder aux exclusions de l'antivirus comme ceci :
 - WIN
 - Taper "Windows defender" + ENTER
 - Aller dans la section "Protection contre les virus et les menaces"
 - Dans la deuxième section horizontale, cliquer "Gérer les paramètres"
 - Dans l'avant dernière section horizontale, cliquer "Ajouter au supprimer des exclusions"
