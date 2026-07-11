import sys
import argparse
import os
import time
import subprocess
import warnings

warnings.filterwarnings("ignore")

import requests

def prepare() -> str:
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker nie jest zainstalowany. Zainstaluj Dockera. https://docs.docker.com/desktop/setup/install/windows-install/")
        sys.exit(1)
    
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    compose_path = os.path.join(project_dir, "docker-compose.yml")
    
    subprocess.run(["docker", "compose", "-f", compose_path, "up", "-d"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    api = "http://localhost:5000/"
    
    while True:
        try:
            api_test = requests.get(api)
            if api_test.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        print("API nie jest gotowe, czekanie 5s")
        time.sleep(5)
        
    return api

def run():
    api = prepare()
    
    parser = argparse.ArgumentParser(description="Szybki translator CLI")
    
    parser.add_argument("-t", "--text", type=str, help="Tekst, który chcesz przetłumaczyć")
    parser.add_argument("-f", "--file", type=str, help="Plik, którego zawartość chcesz przetłumaczyć (.txt)")
    parser.add_argument("-ls", "--list", action="store_true", help="Wyswietla liste dostepnych jezykow")
    parser.add_argument("-src", "--source", type=str, default="auto", help="Język źródłowy")
    parser.add_argument("-tg", "--target", type=str, default="en",help="Język docelowy")
    parser.add_argument("-alt", "--alternative", type=int, help="Wyświetla dodatkowo alternatywne tłumaczenia (liczba)")
    parser.add_argument("-d", "--detect", type=str, help="Wykrywa język tekstu")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    if args.list:
        print(f"Dostępne języki tłumaczenia: {requests.get(api + '/languages').json()[0]['targets']}")

    if args.detect:
        detect = requests.post(api + "detect", data={"q": args.detect}).json()
        print(f"Język wykryty: {detect[0]['language']} (pewność: {detect[0]['confidence']}%)")
        
    if args.text:            
        payload = {
            "q": args.text,
            "source": args.source if args.source else "auto",
            "target": args.target if args.target else "en",
            "format": "text"
        }
        
        if args.alternative:
            payload["alternatives"] = args.alternative

        try:
            response = requests.post(api + "translate", data=payload)
            if response.status_code == 200:
                print(response.json().get("translatedText"))
                if args.alternative:
                    print(f"Alternatywne tłumaczenia: {response.json().get('alternatives')}")
            else:
                print(f"Błąd API: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia: {e}")
        
    if args.file:
        if os.stat(args.file).st_size == 0:
            raise Exception("Podany plik jest pusty.")
        if os.path.splitext(args.file)[1] != ".txt":
            raise Exception(f"Tylko pliki (.txt) są obsługiwane. Podany plik ma rozszerzenie \"{os.path.splitext(args.file)[1]}\"")
        try:
            with open(args.file, "rb") as file:

                response = requests.post(
                    api + "translate_file",
                    files={"file": file},
                    data={
                        "source": args.source,
                        "target": args.target,
                        "format": "text"
                    }
                )
                
            if response.status_code == 200:
                download_url = response.json().get("translatedFileUrl")
                
                file_name, file_ext = os.path.splitext(args.file)
                output_name = f"{file_name}_translated_{args.target}{file_ext}"
                
                download_res = requests.get(download_url, stream=True)
                if download_res.status_code == 200:
                    with open(output_name, "wb") as out_file:
                        for chunk in download_res.iter_content(chunk_size=8192):
                            out_file.write(chunk)
                    print(f"Przetłumaczony plik zapisano jako: {output_name}")
                else:
                    print(f"Błąd pobierania pliku: {download_res.status_code}")
            else:
                print(f"Błąd API: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia: {e}")