import re
import unidecode
import pandas as pd
from tqdm.auto import tqdm
from flashtext import KeywordProcessor
import joblib
import copy

from django.conf import settings

DATA_PATH = settings.APPLICATIONS_DIR / "core" / "helpers" / "data"

mahalle_list = ["mahallesi", "mah", "mh", "MAHALLELERİ"]
sokak_list = ['sokağı', 'sokagi', 'caddesi', 'sokak', 'cadde', "bulvar", "bulvarı", "bulvari", "blvd", "yol", "yolu", 'sk', 'cd', "sok", "cad"]
site_list = ['sitesi', "siteleri", 'evleri', "konut", "konutları", "konutlari", "kooperatif", "kent", 'site', "home", "qpt", "spt", "köyü", "koyu", "koy"]
apartman_list = ['apartmanı', 'apartmani', "aprtman", "rezidans", 'evi', 'apt', "aprt", 'bina', 'binası', "binasi", "karşısı", "karsisi"]
blok_list = ['blok', 'etap']
kisim_list = ['kisim', 'kısım']

#il_pattern = re.compile(r"(" + '|'.join(city_data["processed_il"].tolist()) + ")", re.IGNORECASE)
#ilçe_pattern = re.compile(r"(" + '|'.join(city_data["processed_ilce"].tolist()) + ")", re.IGNORECASE)
#mahalle_pattern = re.compile(r"(" + '|'.join(city_data["processed_mahalle"].tolist()) + ")", re.IGNORECASE)
sehir_data = pd.read_csv(str(DATA_PATH / "il_ilce_v3.csv"))
kp_dict = joblib.load(str(DATA_PATH / "sehir_kp_objs.joblib"))
sehir_dict = joblib.load(str(DATA_PATH / "sehir_dict.joblib"))


mahalle_pattern = re.compile(r"(((\d+\.)|(\w+))(\s+)?(" + '|'.join(mahalle_list) + "))", re.IGNORECASE)
sokak_cadde_bulvar_yol_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(sokak_list) + "))", re.IGNORECASE)
site_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(site_list) + "))", re.IGNORECASE)
apartman_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(apartman_list) + "))", re.IGNORECASE)
blok_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(blok_list) + "))", re.IGNORECASE)
kisim_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(kisim_list) + "))", re.IGNORECASE)
kat_pattern = re.compile(r"((\d+\.?(\s+)?(kat))|(kat(\s+)?\d+)|(katı(\s+)?\d+)|(\d+\.?(\s+)?(katı)))", re.IGNORECASE)
no_pattern = re.compile(r"((no(\s+)?\d+)|(daire no(\s+?)\d+)|(daire(\s+?)\d+)|([Dd]\s?([0-9]+)))", re.IGNORECASE)
no_pattern_v2 = re.compile(r"\b((\d+)\/(\d+))\b", re.IGNORECASE)
no_pattern_v3 = re.compile(r'(\b(\d{3})\b)|(\b(\d{2})\b)|(\b(\d{1})\b)', re.IGNORECASE)
no_pattern_v4 = re.compile(r'(\b\d+\/\w+\b)|(\b\d+\/\d+\b)', re.IGNORECASE|re.UNICODE)
telefon_no_pattern = re.compile(r"\b(5\d{9}|05\d{9}|905\d{9})\b", re.IGNORECASE)
remove_punct_pattern = re.compile(r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]+\ *", re.IGNORECASE)
#number_regex = re.compile(r"\d{1,}", re.IGNORECASE)
            
class ExtractInfo:
    def __init__(self, kp_dict, sehir_dict, sehir_data):
        self.kp_dict = kp_dict
        self.sehir_dict = sehir_dict
        self.sehir_data = sehir_data

    @staticmethod
    def lowercase_turkish(text):
        return text.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

    def process_text(self, text, is_unidecode=True):
        return unidecode.unidecode(self.lowercase_turkish(text)) if is_unidecode else self.lowercase_turkish(text)

    def check_intersection(self, text1, list1):
        return len(set(self.process_text(text1).split()).intersection(set(list1))) > 0

    def extract(self, text):
        self.result = {
            "city": "",
            "distinct": "",
            "neighbourhood": "",
            "excessData": {
                "street_road": "",
                "complex": "",
                "apartment": "",
                "part": "",
                "block": "",
                "floor": "",
                "apartment_no": "",
                "phone": ""
            },
            "originalText": ""
        }
        
        if pd.isna(text): return self.result

        self.result["originalText"] = copy.deepcopy(text)
        text = text.replace('Ä±', 'ı').replace('ÅŸ', 'ş').replace('ÄŸ', 'ğ').replace('Ä°', 'İ').replace('ÅŸ', 'Ş').replace('Äž', 'Ğ').replace('Ã§', 'ç').replace('Ã¼', 'ü').replace('Ã¶', 'ö').replace('Ã‡', 'Ç').replace('Ãœ', 'Ü').replace('Ã–', 'Ö').replace('Ã‡', 'Ç').replace('ã¼','i').replace('åž','ş')

        self.text_df = pd.DataFrame(
            {
                "originalText": [text]
            }
        )

        self.text = self.lowercase_turkish(' '.join(text.replace("\n", " ").strip().split()))
        self.text = remove_punct_pattern.sub(" ", self.text)
        self.text = self.text.replace(" cad", " caddesi").replace(" cd", " caddesi").replace(" sk", " sokak").replace(" sok", " sokak").replace(" blv", " bulvarı")
        self.unidecoded_text = unidecode.unidecode(self.text)
        
        # extract şehir
        extracted_sehir = self.kp_dict["kp_sehir"].extract_keywords(self.unidecoded_text)
        
        if len(extracted_sehir):
            self.result["city"] = self.sehir_dict["sehir"][extracted_sehir[0]]

        # extract ilçe
        extracted_ilce = self.kp_dict["kp_ilce"].extract_keywords(self.unidecoded_text)

        if len(extracted_ilce):
            for elem in extracted_ilce:
                self.result["distinct"] = self.sehir_dict["ilce"][extracted_ilce[0]]
            
            if self.result["city"] == "":
                try:
                    self.result["city"] = self.sehir_dict["sehir_ilce"][self.result["distinct"]]
                except:
                    pass

        # extract mahalle, step 1
        extracted_mahalle = self.kp_dict["kp_mahalle"].extract_keywords(self.unidecoded_text)
        
        if len(extracted_mahalle):
            extracted_mahalle = sorted(extracted_mahalle, key=lambda x: len(x.split())*len(x), reverse=True)
            
            for elem in extracted_mahalle:
                if self.sehir_dict["sehir_mahalle"][elem] == self.process_text(self.result["neighbourhood"]):
                    self.result["neighbourhood"] = self.sehir_dict["mahalle"][elem]
                    break

        # extract mahalle, step 2
        try:
            extracted_mahalle_part2 = mahalle_pattern.findall(self.text)
            extracted_mahalle += [extracted_mahalle_part2[0][0]]
        except:
            pass

        # merge
        if len(extracted_mahalle):
            extracted_mahalle = sorted(extracted_mahalle, key=lambda x: len(x.split())*len(x), reverse=True) 
            self.result["neighbourhood"] = extracted_mahalle[0]

        # extract sokak / cadde, step 1
        extracted_sokak_cadde = self.kp_dict["kp_sokak_cadde"].extract_keywords(self.unidecoded_text)
        
        try:
            extracted_sokak_cadde_part2 = sokak_cadde_bulvar_yol_pattern.findall(self.text)
            extracted_sokak_cadde += [extracted_sokak_cadde_part2[0][0]]
        except:
            pass

        if len(extracted_sokak_cadde):
            extracted_sokak_cadde = sorted(extracted_sokak_cadde, key=lambda x: len(x.split())*len(x), reverse=True)
            
            for elem in extracted_sokak_cadde:
                if elem != self.process_text(self.result["city"]) and self.check_intersection(elem, sokak_list):
                    self.result["excessData"]["street_road"] = elem
                    break

        try:
            self.result["excessData"]["complex"] = site_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["excessData"]["complex"], "")
        except:
            self.result["excessData"]["complex"] = ""

        try:
            self.result["excessData"]["apartment"] = apartman_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["excessData"]["apartment"], "")
        except:
            self.result["excessData"]["apartment"] = ""

        # extract kısım
        try:
            self.result["excessData"]["part"] = kisim_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["excessData"]["part"], "")
            self.result["excessData"]["part"] = self.result["excessData"]["part"].replace("kısım", "").replace("Kısım", "").strip()
        except:
            pass

        # extract blok
        try:
            self.result["excessData"]["block"] = blok_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["excessData"]["block"], "")
            self.result["excessData"]["block"] = self.result["excessData"]["block"].replace("blok", "").replace("Blok", "").strip()
        except:
            pass
        
        # extract kat
        try:
            self.result["excessData"]["floor"] = kat_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["excessData"]["floor"], "")
            self.result["excessData"]["floor"] = self.result["excessData"]["floor"].lower().replace("kat", "").replace("k", "").strip()
        except:
            pass

        # extract daire no
        try:
            self.result["excessData"]["apartment_no"] = no_pattern_v2.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["excessData"]["apartment_no"], "")
            self.result["excessData"]["apartment_no"] = self.result["excessData"]["apartment_no"].lower().replace("no", "").replace("daire", "").strip()
        except:
            try:
                self.result["excessData"]["apartment_no"] = no_pattern.findall(self.text)[0][0].strip()
                self.text = self.text.replace(self.result["excessData"]["apartment_no"], "")
                self.result["excessData"]["apartment_no"] = self.result["excessData"]["apartment_no"].lower().replace("no", "").replace("daire", "").strip()
            except:
                try:
                    self.result["excessData"]["apartment_no"] = no_pattern_v4.findall(self.result["originalText"])[0][0].strip()
                    self.text = self.text.replace(self.result["excessData"]["apartment_no"], "")
                    self.result["excessData"]["apartment_no"] = self.result["excessData"]["apartment_no"].lower().replace("no", "").replace("daire", "").strip()
                except:
                    try:
                        self.result["excessData"]["apartment_no"] = no_pattern_v3.findall(self.text)[0][0].strip()
                        self.text = self.text.replace(self.result["excessData"]["apartment_no"], "")
                        self.result["excessData"]["apartment_no"] = self.result["excessData"]["apartment_no"].lower().replace("no", "").replace("daire", "").strip()
                    except:
                        pass


        # extract telefon
        try:
            self.result["excessData"]["phone"] = telefon_no_pattern.findall(self.text)[0].strip()
            self.text = self.text.replace(self.result["excessData"]["phone"], "")

            if self.result["excessData"]["phone"].startswith("9"):
                self.result["excessData"]["phone"] = self.result["excessData"]["phone"][2:]
            
            elif self.result["excessData"]["phone"].startswith("0"):
                self.result["excessData"]["phone"] = self.result["excessData"]["phone"][1:]
            
            self.result["excessData"]["phone"] = self.result["excessData"]["phone"].replace(" ", "")

            # (\d{3} \d{3} \d{2} \d{2})|(\d{4} \d{3} \d{4})|(\d{1} \d{3} \d{3} \d{2} \d{2})|(\d{1} \d{3} \d{3} \d{4})|(\d{11})|(\d{10})|(\d{3} \d{3} \d{4})|(\d{3} \d{3} \d{2} \d{2})
            self.result["excessData"]["phone"] = self.result["excessData"]["phone"][:3] + " " + self.result["excessData"]["phone"][3:6] + " " + self.result["excessData"]["phone"][6:8] + " " + self.result["excessData"]["phone"][8:]

        except:
            pass   
        
        # post process
        cond1 = self.process_text(self.result["distinct"]) in self.result["neighbourhood"]
        cond2 = self.lowercase_turkish(self.result["distinct"]) in self.result["neighbourhood"]

        cond3 = self.process_text(self.result["distinct"]) in self.result["excessData"]["complex"]
        cond4 = self.lowercase_turkish(self.result["distinct"]) in self.result["excessData"]["complex"]

        cond5 = self.process_text(self.result["distinct"]) in self.result["excessData"]["apartment"]
        cond6 = self.lowercase_turkish(self.result["distinct"]) in self.result["excessData"]["apartment"]

        cond7 = self.process_text(self.result["distinct"]) in self.result["city"]
        cond8 = self.lowercase_turkish(self.result["distinct"]) in self.result["city"]

        if any([cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8]):
            self.result["distinct"] = ""
      
        # check sehir - ilce match
        try:
            cond1 = self.result["city"] != ""
            cond2 = self.result["distinct"] != ""
            cond3 = self.sehir_dict["sehir_ilce"][self.process_text(self.result["distinct"])] != self.process_text(self.result["city"])

            if all([cond1, cond2, cond3]):
                self.result["city"] = self.sehir_dict["city"][self.sehir_dict["sehir_ilce"][self.process_text(self.result["distinct"])]]
        except:
            pass
        
        # fill sehir if ilce available
        try:
            if self.result["distinct"] != "" and self.result["city"] == "":
                self.result["city"] = self.sehir_dict["city"][self.sehir_dict["sehir_ilce"][self.process_text(self.result["distinct"])]]
        except:
            pass
        
        if self.result["city"] != "":
            ' '.join([self.result["city"], "ili"])
        
        if self.result["distinct"] != "":
            ' '.join([self.result["distinct"], "ilcesi"])

        # merge address
        part1 = ' '.join([val for key, val in list(self.result.items()) if key not in ["excessData", "originalText"]])
        part2 = ' '.join(list(self.result["excessData"].values()))
        self.result["address"] = ' '.join(' '.join([part1, part2]).split())
        self.calculate_score()
      
        return self.result
    
    def concat_address(self):
        address_str = ""
        #for key, value in self.result.items():
        #    if value != "":
                #if key == "city":
                #    address_str = address_str + value + " ili "
                #if key == "distinct":
                #    address_str = address_str + value + " ilcesi "
                #if key == "neighbourhood":
                #    address_str = address_str + value + " mahallesi "
                #if key == "street_road":
                #    address_str = address_str + value + " caddesi "
                #if key == "apartment":
                #    address_str = address_str + value + " apartmani "

        self.result["address"] = address_str

    def calculate_score(self):
        weighted_score = 0

        if self.result["city"] != "":
            weighted_score += 5
        if self.result["distinct"] != "":
            weighted_score += 5
        if self.result["neighbourhood"] != "":
            weighted_score += 4
        if self.result["excessData"]["street_road"] != "":
            weighted_score += 3
        if self.result["excessData"]["apartment"] != "":
            weighted_score += 3
        if self.result["excessData"]["complex"] != "":
            weighted_score += 3

        if self.result["excessData"]["part"] != "":
            weighted_score += 1
        if self.result["excessData"]["block"] != "":
            weighted_score += 1
        if self.result["excessData"]["floor"] != "":
            weighted_score += 1
        if self.result["excessData"]["apartment_no"] != "":
            weighted_score += 1
        if self.result["excessData"]["phone"] != "":
            weighted_score += 1

        self.result["ws"] = weighted_score / (5 + 5 + 4 + 3 + 3 + 3 + 1 + 1 + 1 + 1 + 1)
        return self.result