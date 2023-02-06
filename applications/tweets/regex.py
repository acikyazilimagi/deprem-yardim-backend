import re
import unidecode
import pandas as pd

mahalle_list = ["mahallesi", "mh\.", "mh", "mah."]
sokak_list = ['sokağı', 'sokagi', 'caddesi', 'sokak', 'cadde', "bulvarı", "bulvari", "yol", "yolu", 'sk', 'cd', "sok", "cad"]
site_list = ['sitesi', 'apartmanı', 'apartmani', "rezidans", 'evleri', 'bina', 'site', 'evi', 'apt', 'aprt']
blok_list = ['blok', 'etap', 'kisim', 'kısım']


df = pd.read_csv("/content/il_ilce_v2.csv")
il_pattern = re.compile(r"(" + '|'.join(df["processed_il"].tolist()) + ")", re.IGNORECASE)
ilçe_pattern = re.compile(r"(" + '|'.join(df["processed_ilce"].tolist()) + ")", re.IGNORECASE)
mahalle_pattern = re.compile(r"(" + '|'.join(df["processed_mahalle"].tolist()) + ")", re.IGNORECASE)
mahalle_pattern_v2 = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(mahalle_list) + "))", re.IGNORECASE)
sokak_cadde_bulvar_yol_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(sokak_list) + "))", re.IGNORECASE)
site_apartman_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(site_list) + "))", re.IGNORECASE)
blok_pattern = re.compile(r"(((\d+\.)|(\w+))\s+(" + '|'.join(blok_list) + "))", re.IGNORECASE)
kat_pattern = re.compile(r"((\d+\.?(\s+)?(kat))|(kat(\s+)?\d+)|(kat:(\s+)?\d+))", re.IGNORECASE)
daire_no_pattern = re.compile(r"((no(\s+)?\d+)|(daire no(\s+?)\d+)|(daire(\s+?)\d+))", re.IGNORECASE)
telefon_no_pattern = re.compile(r"\b(5\d{9}|05\d{9})\b", re.IGNORECASE)
il_dict = dict(zip(df["processed_il"].tolist(), df["il"].tolist()))
ilçe_dict = dict(zip(df["processed_ilce"].tolist(), df["ilçe"].tolist()))
mahalle_dict = dict(zip(df["processed_mahalle"].tolist(), df["mahalle"].tolist()))
remove_punct_pattern = re.compile(r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]+\ *", re.IGNORECASE)
number_regex = re.compile(r"\d{1,}", re.IGNORECASE)

class ExtractInfo:
    def __init__(self, text):
        self.text = ' '.join(text.strip().split())
        self.result = {
            "il": "",
            "ilçe": "",
            "mahalle": "",
            "sokak_cadde_bulvar_yol": "",
            "site_apartman_bina": "",
            "blok": "",
            "kat": "",
            "daire_no": "",
            "telefon": ""
        }

    @staticmethod
    def process_text(text, is_unidecode=True):
        text = text.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

        if is_unidecode:
            text = unidecode.unidecode(text)

        return text
    
    @staticmethod
    def number_exact_match(text1, text2):
        return True if set(number_regex.findall(text1)) == set(number_regex.findall(text2)) else False
    

    def get_sim_based_city_ilce_mahalle(self):
        for token in self.text.split():
            token_lower = token.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()
                
            for city in il_dict.values():
                city_lower = city.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

                if textdistance.levenshtein.normalized_similarity(token, city) >= 0.9:
                    self.result["il"] = city
                    break
            
            for ilçe in ilçe_dict.values():
                ilçe_lower = ilçe.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

                if textdistance.levenshtein.normalized_similarity(token, ilçe) >= 0.9:
                    self.result["ilçe"] = ilçe
                    break
            

            for mahalle in mahalle_dict.values():
                mahalle_lower = mahalle.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

                if textdistance.levenshtein.normalized_similarity(token, mahalle_lower) >= 0.9:
                    self.result["mahalle"] = mahalle
                    break


    def extract(self):
        self.text = self.text.split("\n")[-1]
        self.text = remove_punct_pattern.sub(" ", self.text)
        unidecoded_text = self.process_text(self.text)
            
        # extract şehir
        try:
            extracted_il = il_pattern.findall(unidecoded_text)[0]
            unidecoded_text = unidecoded_text.replace(extracted_il, "")
            self.result["il"] = il_dict[extracted_il].title()
        except:
            self.result["il"] = ""

        # extract ilçe
        try:
            extracted_ilçe = ilçe_pattern.findall(unidecoded_text)[0]
            unidecoded_text = unidecoded_text.replace(extracted_ilçe, "")
            self.result["ilçe"] = ilçe_dict[extracted_ilçe].title()
        except:
            self.result["ilçe"] = ""

        # extract mahalle
        try:
            self.result["mahalle"] = mahalle_pattern_v2.findall(self.text)[0][1].strip()
            self.text = self.text.replace(self.result["mahalle"], "")

        except:
            try:
                extracted_mahalle = mahalle_pattern.findall(unidecoded_text)[0]
                unidecoded_text = unidecoded_text.replace(extracted_mahalle, "")
                self.result["mahalle"] = mahalle_dict[extracted_mahalle]
            except:
                self.result["mahalle"] = ""


        # extract sokak / cadde
        try:
            self.result["sokak_cadde_bulvar_yol"] = sokak_cadde_bulvar_yol_pattern.findall(self.text)[0][1].strip()
            self.text = self.text.replace(self.result["sokak_cadde_bulvar_yol"], "")
        except:
            self.result["sokak_cadde_bulvar_yol"] = ""


        # extract site / apartman / bina

        try:
            self.result["site_apartman_bina"] = site_apartman_pattern.findall(self.text)[0][1].strip()
            self.text = self.text.replace(self.result["site_apartman_bina"], "")
        except:
            self.result["site_apartman_bina"] = ""
            

        # extract blok
        try:
            self.result["blok"] = blok_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["blok"], "")
            self.result["blok"] = self.result["blok"].replace("blok", "").strip()
        except:
            self.result["blok"] = ""
        
        # extract kat

        try:
            self.result["kat"] = kat_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["kat"], "")
            self.result["kat"] = int(self.result["kat"].lower().replace("kat", "").strip()) 
        except:
            self.result["kat"] = ""

        # extract daire no
        try:
            self.result["daire_no"] = daire_no_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["daire_no"], "")
            self.result["daire_no"] = int(self.result["daire_no"].lower().replace("no", "").replace("daire", "").strip())    
        except:
            self.result["daire_no"] = ""

        # extract telefon
        try:
            self.result["telefon"] = telefon_no_pattern.findall(self.text)[0].strip()
            self.text = self.text.replace(self.result["telefon"], "")
        except:
            self.result["telefon"] = ""

        return self.result

def extractAdressUsingRegex(address):
    ei = ExtractInfo(address)
    return ei.extract()