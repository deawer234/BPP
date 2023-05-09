Pro spuětení webové ovládací aplikace je potřeba nainstalovat potřebné knihovny. Tyto knihovny lze nainstalovat spuštěním skriptu ```install.sh``` Pokud skript nejde spustit z důvodu práv je nutné použít příkaz ```chmod u+x install.sh```. Po instalaci všech potřebných knihoven je dále nutné spustit ovladač knihovny pigpio pro komunikaci s GPIO piny Raspberry Pi, toto lze příkazem ```sudo pigpiod```. Pro spuštění aplikace na jiné platformě než Raspberry Pi, je nutné zakomentovat v souboru *website/model/robot_controll.py* všechny výskyty funkce **pi.set_servo_pulsewidth()**!!. Po spuštění ovladače knihovny pigpio je nutné zjistit IP adresu využívané Raspberry Pi desky pomocí příkazu ```ifconfig```. Po získání IP adresy lze aplikaci spustit příkazem ```flask run --host=<IP adresa> ``` kde <IP adresa> je adresa Raspberry Pi v síti. Pokud není využívána deska Raspberry Pi, lze aplikaci spustit na localhost.
Po spuštění lze na webu přistoupit k webové aplikaci s <IP adresa>:5000 (port).