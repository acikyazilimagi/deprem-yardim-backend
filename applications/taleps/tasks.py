from trquake.celery import app
import requests, json

from taleps.models import TalepAddress, TalepLocation

# @app.task
def collect_taleps():
    """
    This task routinely acquires new data from different websites
    that gather taleps and inserts them into our central database. 
    """

    # Eger cookie expire ederse, Chrome devtools'dan kendi cookie'nizi yapistirabilirsiniz. Daha iyi bi cozum bulmak lazim.
    req = requests.get(
        url="https://www.depremyardim.com/json.php",
        headers={
            "accept-encoding": "br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "PHPSESSID=777d39076d0c9c13f18cea2bbb1aba40; cf_clearance=hiLEDBOaCZaagDk5gyrrpGEU60sGK1KE.IXsWyslCeQ-1675753096-0-160",
            "dnt": "1",
            "origin": "https://www.depremyardim.com",
            "referer": "https://www.depremyardim.com/json.php?__cf_chl_tk=yD5XjyfCrNN2lwcZ_h6_86YOtyNjlzujh5M0b8zfm_g-1675753095-0-gaNycGzNC6U",
            "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
        }
        )
    
    # Bu request unstable. Bazen br encodingle yollanabiliyor, ondan extra package (brotli) gerekebilir. 
    all_taleps = json.loads(req.text)
    
    objects = []
    for talep in all_taleps:
        address = TalepAddress.objects.create(
            address=f'{talep["konum_il"]} {talep["konum_ilce"]} {talep["konum_mahalle"]}',
            city=talep["konum_il"],
            distinct=talep["konum_ilce"],
            neighbourhood=talep["konum_mahalle"],
            street=None,
            no=None,
            name_surname=talep["name_surname"],
            tel=None,
        )

        # Bunu Trendyol API'ni daha iyi anlayan birinin yapmasi daha iyi olur
        # geolocation_response = requests.get(
        #     url=ty_geolocation_url, params={"address": full_address}
        # )
        # geolocation_data = geolocation_response.json()
        # if geolocation_results := geolocation_data.get("results", []):
        #     geolocation = geolocation_results[0]
        #     geometry = geolocation["geometry"]
        #     location = geometry.get("location", {"lat": 0.0, "lng": 0.0})
        #     viewport = geometry.get(
        #         "viewport",
        #         {
        #             "northeast": {"lat": 0.0, "lng": 0.0},
        #             "southwest": {"lat": 0.0, "lng": 0.0},
        #         },
        #     )
        #     TalepLocation.objects.create(
        #         address=address,
        #         latitude=location["lat"],
        #         longitude=location["lng"],
        #         northeast_lat=viewport["northeast"]["lat"],
        #         northeast_lng=viewport["northeast"]["lng"],
        #         southwest_lat=viewport["southwest"]["lat"],
        #         southwest_lng=viewport["southwest"]["lng"],
        #         formatted_address=geolocation["formatted_address"]
        #     )
        #     address.is_resolved = True
        #     address.save()
   

    # TalepAddress.objects.bulk_create()


if __name__ == "__main__":
    collect_taleps()