# Redogörelse - Server Inventory Tool

## 1. Tre olika konstruktioner i koden
I menu.py, i funktionen add_server(), använder jag if-satser för att kontrollera användarens inmatning. Jag kontrollerar bland annat att inmatningen inte får vara tom och att servernamnet inte redan finns i listan. Jag har även lagt till möjligheten att skriva QUIT för att avbryta om man ångrar sig. Samma princip används i remove_server(), där användaren också kan avbryta borttagningen. Detta gör programmet mer användarvänligt och minskar risken för felaktig information.

I controller.py, i funktionen check_server(server), använder jag en parameter för att skicka in den server som ska kontrolleras. Funktionen hämtar serverns adress och använder ett villkor för att kontrollera om adressen är tom. Om den är tom sätts statusen till down. Annars körs ett ping-kommando för att kontrollera om servern svarar. Jag använder även try och except för att hantera fel och en timeout på tre sekunder så att programmet inte väntar för länge. Till sist uppdateras tiden för den senaste kontrollen och funktionen returnerar servern med dess uppdaterade information.

I storage.py, i funktionen export_to_csv(servers), använder jag parametern servers för att skicka in listan med servrar som ska exporteras. Funktionen skapar en CSV-fil i mappen reports och använder en for-loop för att gå igenom alla servrar och skriva deras information till filen. Jag använder även try och except för att hantera eventuella fel, till exempel om programmet saknar behörighet att skapa filen. Om exporten lyckas returneras filnamnet med return filename, annars returneras None.

I menu.py, i funktionen export_server_report(), laddas först alla servrar in. Om listan är tom avslutas funktionen utan att skapa någon CSV-fil. Annars skickas serverlistan vidare till export_to_csv() i storage.py.

## 2. Varför passar en lista med dictionaries för att lagra servrarna?
Jag använder en lista med dictionaries för att kunna spara flera servrar och deras information på ett enkelt sätt. Varje dictionary innehåller information om en server: namn, adress, miljö, roll, status och när servern senast kontrollerades. Det gör det enkelt att hitta och ändra information genom att använda olika nycklar, till exempel server["name"] för att komma åt serverns namn.

En lista passar bra eftersom jag enkelt kan lägga till nya servrar med append() och ta bort servrar med remove(). Detta använder jag i menu.py, i funktionerna add_server() och remove_server().

Alla värden i mina dictionaries är av datatypen string (sträng). Eftersom informationen i min JSON-fil består av text omvandlas värdena till strängar när Python läser in filen.

## 3. Varför sparar du data i JSON men exporterar rapporten som CSV?
Jag använder JSON för att spara serverinformationen eftersom det är enkelt för Python att läsa, ändra och spara data. Detta görs i storage.py, i funktionerna load_servers() och save_servers().

Jag använder CSV för rapporterna eftersom de visas i tabellform och enkelt kan öppnas i exempelvis Excel. Exporten görs i storage.py, i funktionen export_to_csv().

## 4. Hur är programmet uppdelat i moduler och funktioner? Vilket ansvar har varje fil?
Jag har delat upp programmet i fyra Python-filer för att hålla koden organiserad.

`main.py` – Startar programmet och hanterar kommandon från terminalen (CLI).

`menu.py` – Innehåller den interaktiva menyn där användaren kan visa, lägga till, ta bort och kontrollera servrar.

`controller.py` – Ansvarar för att kontrollera om servrar är tillgängliga genom ping och uppdatera deras status.

`storage.py` – Hanterar inläsning och sparning av serverinformation i JSON samt export av rapporter till CSV.

## 5. Vilka moduler från standardbiblioteket använder du och till vad?
`argparse` – Hanterar kommandon och argument från terminalen. (main.py)

`sys` – Används för att avsluta programmet med olika exitkoder. (main.py, menu.py)

`subprocess` – Kör ping-kommandon för att kontrollera servrar. (controller.py)

`platform` – Kontrollerar vilket operativsystem som används. (controller.py)

`datetime` – Hämtar datum och tid för senaste serverkontrollen och för CSV-filernas namn. (controller.py, storage.py)

`os` – Läser av miljövariabeln som bestämmer sökvägen till JSON-filen. (storage.py)

`json` – Läser och sparar serverinformationen i JSON-format. (storage.py)

`csv` – Skapar och skriver CSV-rapporter. (storage.py)

`pathlib` – Hanterar sökvägar och mappar. (storage.py)

## 6. Ge tre exempel på god praxis från din kod och förklara varför de är bra.
Jag har delat upp programmet i flera filer där varje fil har sitt eget ansvarsområde. Jag använder också funktioner för att dela upp olika delar av programmet. Detta gör koden lättare att läsa, förstå och ändra. Det blir också enklare att felsöka eftersom jag vet vilken fil jag ska leta i när något inte fungerar.

I storage.py, i funktionen export_to_csv(), använder jag datum och tid i filnamnet när en rapport skapas. Det gör att rapporterna får olika filnamn och att tidigare rapporter inte skrivs över.

I controller.py, i funktionen check_server(), använder jag modulen platform för att kontrollera vilket operativsystem programmet körs på. Beroende på om det är Windows eller Linux/macOS väljer programmet rätt kommando för att pinga en server. Detta gör att programmet fungerar på olika operativsystem utan att jag behöver ändra koden manuellt.

## 7. Vilka källor och hjälpmedel har du använt och till vad? Det kan till exempel vara kursboken, dokumentation, forum eller AI-verktyg.
Jag har gått tillbaka till tidigare övningar från kursen för att repetera och få hjälp med olika delar av Python. Jag har även tittat tillbaka på ett program som jag byggde under Java-kursen, eftersom det påminner mycket om detta projekt.

Jag har använt GitHub Copilot för att få förslag på kod, hitta fel och rätta till kod.

Vid felsökning har jag även använt ChatGPT och Gemini. Jag har bett AI-verktygen att förklara vad som är fel utan att direkt ge mig lösningen. När jag verkligen har kört fast har jag bett om hjälp med koden och sedan bett AI:n förklara hur den fungerar, så att jag verkligen förstår vad koden gör. ChatGPT har även hjälpt mig att strukturera och förbättra README.md så att dokumentationen blir tydlig och lättläst.