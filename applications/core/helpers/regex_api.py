import re
import unidecode
import pandas as pd
import copy
import numpy as np
import re

mahalle_list = ["(mahallesi)", "(mah.)", "(mh\.)", "(mh)"]
sokak_list = [
    "sokağı",
    "sokagi",
    "caddesi",
    "sokak",
    "cadde",
    "bulvarı",
    "bulvari",
    "yol",
    "yolu",
    "sk",
    "cd",
    "sok",
    "cad",
    "sok\.",
    "cad\.",
    "cd\.",
]
site_list = [
    "sitesi",
    "apartmanı",
    "apartmani",
    "rezidans",
    "evleri",
    "bina",
    "site",
    "evi",
    "apt",
    "konutlari",
]
blok_list = ["blok", "etap", "kisim", "kısım"]



df = pd.read_csv("il_ilce_v2.csv")
il_pattern = re.compile(
    r"(" + "|".join(df["processed_il"].tolist()) + ")", re.IGNORECASE
)
ilçe_pattern = re.compile(
    r"(" + "|".join(df["processed_ilce"].tolist()) + ")", re.IGNORECASE
)
mahalle_pattern = re.compile(
    r"(" + "|".join(df["processed_mahalle"].tolist()) + ")", re.IGNORECASE
)
mahalle_pattern_v2 = re.compile(
    r"((\d+\.)|([A-Za-zÖŞĞÇİÜı0-9]+))\s+\b(" + "|".join(mahalle_list) + r")\b",
    re.IGNORECASE,
)
sokak_cadde_bulvar_yol_pattern = re.compile(
    r"(((\d+\.)|(\w+))\s+(" + "|".join(sokak_list) + "))", re.IGNORECASE
)
site_apartman_pattern = re.compile(
    r"(((\d+\.)|(\w+))\s+(" + "|".join(site_list) + "))", re.IGNORECASE
)
blok_pattern = re.compile(
    r"(((\d+\.)|(\w+))\s+(" + "|".join(blok_list) + "))", re.IGNORECASE
)
kat_pattern = re.compile(
    r"((\d+\.?(\s+)?(kat))|(kat(\s+)?\d+)|(kat:(\s+)?\d+))", re.IGNORECASE
)
daire_no_pattern = re.compile(
    r"((no(\s+)?\d+)|(daire no(\s+?)\d+)|(daire(\s+?)\d+)|([Dd]\s?([0-9]+)))",
    re.IGNORECASE,
)
telefon_no_pattern = re.compile(
    r"[+]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+", re.IGNORECASE
)
il_dict = dict(zip(df["processed_il"].tolist(), df["il"].tolist()))
ilçe_dict = dict(zip(df["processed_ilce"].tolist(), df["ilçe"].tolist()))
mahalle_dict = dict(zip(df["processed_mahalle"].tolist(), df["mahalle"].tolist()))
remove_punct_pattern = re.compile(
    r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]+\ *", re.IGNORECASE
)
number_regex = re.compile(r"\d{1,}", re.IGNORECASE)


class ExtractInfo:
    def __init__(self):
        self.stopword_list = [
            "yardım",
            "haber",
            "mahsur",
            "altında",
            "acil",
            "\n",
            "alamıyoruz",
            "kalanlar",
            "alınamıyor",
            "altındalar",
            "lütfen",
            "\/" "-",
            "\.",
            "\,",
            "\!",
            "\?",
        ]

    @staticmethod
    def process_text(text, is_unidecode=True):
        text = text.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

        if is_unidecode:
            text = unidecode.unidecode(text)

        return text

    @staticmethod
    def number_exact_match(text1, text2):
        return (
            True
            if set(number_regex.findall(text1)) == set(number_regex.findall(text2))
            else False
        )

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
                mahalle_lower = mahalle.translate(
                    str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")
                ).lower()

                if (
                    textdistance.levenshtein.normalized_similarity(token, mahalle_lower)
                    >= 0.9
                ):
                    self.result["mahalle"] = mahalle
                    break

    def get_until_stopword(self, text, key):
        index = text.find(key)
        current_text = text[:index] + f" {key}"
        stopword_index = -1
        for stopword in self.stopword_list:
            index = [el.end() for el in re.finditer(stopword, current_text)]
            if index:
                st_index = index[-1]
            else:
                continue
            if st_index > stopword_index:
                stopword_index = st_index
        if stopword_index != -1:
            current_text = current_text[stopword_index:]
        current_text = " ".join(current_text.split(" ")[-3:])
        return re.sub("\s+", " ", current_text).strip()

    def extract(self, text):
        self.text = " ".join(text.strip().split())
        self.result = {
            "sehir": "",
            "ilce": "",
            "mahalle": "",
            "sokak_cadde_bulvar_yol": "",
            "site_apartman_bina": "",
            "blok": "",
            "kat": "",
            "daire_no": "",
            "excessData": {},
            "originalText": copy.deepcopy(text),
        }
        self.text = self.text.split("\n")[-1]
        self.text = remove_punct_pattern.sub(" ", self.text)
        unidecoded_text = self.process_text(self.text)

        # extract şehir
        try:
            extracted_il = il_pattern.findall(unidecoded_text)[0]
            unidecoded_text = unidecoded_text.replace(extracted_il, "")
            self.result["sehir"] = il_dict[extracted_il].title()
        except:
            self.result["sehir"] = ""

        # extract ilçe
        try:
            extracted_ilçe = ilçe_pattern.findall(unidecoded_text)[0]
            unidecoded_text = unidecoded_text.replace(extracted_ilçe, "")
            self.result["ilce"] = ilçe_dict[extracted_ilçe].title()
        except:
            self.result["ilce"] = ""

        # extract mahalle
        try:
            self.result["mahalle"] = mahalle_pattern_v2.findall(self.text)[0][0].strip()
            # extended_mahalle = self.get_until_stopword(self.result["originalText"], self.result["mahalle"])
            # self.result["mahalle"] = extended_mahalle
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
            self.result[
                "sokak_cadde_bulvar_yol"
            ] = sokak_cadde_bulvar_yol_pattern.findall(self.text)[0][1].strip()
            # extended_sokak = self.get_until_stopword(self.result["originalText"], self.result["sokak_cadde_bulvar_yol"])
            # self.result["sokak_cadde_bulvar_yol"] = extended_sokak
            self.text = self.text.replace(self.result["sokak_cadde_bulvar_yol"], "")
        except:
            self.result["sokak_cadde_bulvar_yol"] = ""

        # extract site / apartman / bina

        try:
            self.result["site_apartman_bina"] = site_apartman_pattern.findall(
                self.text
            )[0][1].strip()
            # extended_site = self.get_until_stopword(self.result["originalText"], self.result["site_apartman_bina"])
            # self.result["site_apartman_bina"] = extended_site
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
            self.result["kat"] = int(
                self.result["kat"].lower().replace("kat", "").strip()
            )
        except:
            self.result["kat"] = ""

        # extract daire no
        try:
            self.result["daire_no"] = daire_no_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["daire_no"], "")
            self.result["daire_no"] = int(
                self.result["daire_no"]
                .lower()
                .replace("no", "")
                .replace("daire", "")
                .replace("d ", "")
                .strip()
            )
        except:
            self.result["daire_no"] = ""

        # extract telefon
        try:
            phone_number = [
                phone_number
                for phone_number in sorted(
                    re.findall(
                        r"[+]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+",
                        self.text,
                    ),
                    key=len,
                    reverse=True,
                )
                if len(phone_number) >= 9 and len(phone_number) <= 18
            ][0]
            self.result["excessData"]["phone"] = (
                phone_number
                if len(phone_number) >= 9 and len(phone_number) <= 18
                else ""
            )
            self.text = self.text.replace(self.result["excessData"]["phone"], "")

        except:
            self.result["excessData"]["phone"] = ""

        self.concataneate_addres()
        self.calculate_score()
        return self.result

    def concataneate_addres(self):
        adres_str = ""
        for key, value in self.result.items():
            if value != "":
                if key == "sehir":
                    adres_str = adres_str + value + " ili "
                if key == "ilçe":
                    adres_str = adres_str + value + " ilcesi "
                if key == "mahalle":
                    adres_str = adres_str + value + " mahallesi "
                if key == "sokak_cadde_bulvar_yol":
                    adres_str = adres_str + value + " caddesi "
                if key == "site_apartman_bina":
                    adres_str = adres_str + value + " apartmani "
        self.result["adres"] = adres_str

    def calculate_score(self):
        weighted_score = 0

        if self.result["sehir"] != "":
            weighted_score += 5
        if self.result["ilce"] != "":
            weighted_score += 5
        if self.result["mahalle"] != "":
            weighted_score += 4
        if self.result["sokak_cadde_bulvar_yol"] != "":
            weighted_score += 3
        if self.result["site_apartman_bina"] != "":
            weighted_score += 3
        if self.result["blok"] != "":
            weighted_score += 1
        if self.result["kat"] != "":
            weighted_score += 1
        if self.result["daire_no"] != "":
            weighted_score += 1
        if self.result["excessData"]["phone"] != "":
            weighted_score += 1

        self.result["ws"] = weighted_score / (5 + 5 + 4 + 3 + 3 + 1 + 1 + 1 + 1)
        return self.result