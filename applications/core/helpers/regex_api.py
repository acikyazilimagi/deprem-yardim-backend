import unidecode
import pandas as pd
import copy
import re
from django.conf import settings
from typing import Dict, Union, Optional

DATA_PATH = settings.APPLICATIONS_DIR / "core" / "helpers" / "data"

neighbourhood_list = ["(mahallesi)", "(mah.)", "(mh\.)", "(mh)"]
street_list = [
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
block_list = ["blok", "etap", "kisim", "kısım"]


df = pd.read_csv(str(DATA_PATH / "il_ilce_v2.csv"))
city_pattern = re.compile(
    r"(" + "|".join(df["processed_il"].tolist()) + ")", re.IGNORECASE
)
distinct_pattern = re.compile(
    r"(" + "|".join(df["processed_ilce"].tolist()) + ")", re.IGNORECASE
)
neighbourhood_pattern = re.compile(
    r"(" + "|".join(df["processed_mahalle"].tolist()) + ")", re.IGNORECASE
)
neighbourhood_pattern_v2 = re.compile(
    r"((\d+\.)|([A-Za-zÖŞĞÇİÜı0-9]+))\s+\b(" + "|".join(neighbourhood_list) + r")\b",
    re.IGNORECASE,
)
street_road_boulevard_pattern = re.compile(
    r"(((\d+\.)|(\w+))\s+(" + "|".join(street_list) + "))", re.IGNORECASE
)
site_apartment_pattern = re.compile(
    r"(((\d+\.)|(\w+))\s+(" + "|".join(site_list) + "))", re.IGNORECASE
)
block_pattern = re.compile(
    r"(((\d+\.)|(\w+))\s+(" + "|".join(block_list) + "))", re.IGNORECASE
)
floor_pattern = re.compile(
    r"((\d+\.?(\s+)?(kat))|(kat(\s+)?\d+)|(kat:(\s+)?\d+))", re.IGNORECASE
)
apartment_no_pattern = re.compile(
    r"((no(\s+)?\d+)|(daire no(\s+?)\d+)|(daire(\s+?)\d+)|([Dd]\s?([0-9]+)))",
    re.IGNORECASE,
)
phone_number_pattern = re.compile(
    r"[+]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+[\s]?[0-9]+", re.IGNORECASE
)
city_dict = dict(zip(df["processed_il"].tolist(), df["il"].tolist()))
distinct_dict = dict(zip(df["processed_ilce"].tolist(), df["ilçe"].tolist()))
neighbourhood_dict = dict(zip(df["processed_mahalle"].tolist(), df["mahalle"].tolist()))
remove_punct_pattern = re.compile(
    r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]+\s*", re.IGNORECASE
)
number_regex = re.compile(r"\d{1,}", re.IGNORECASE)


class ExtractInfo:
    result: Dict[str, Optional[Union[str, int]]]
    text: str

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

    def get_sim_based_city_distinct_neighbourhood(self):
        for token in self.text.split():
            token_lower = token.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

            for city in city_dict.values():
                city_lower = city.translate(str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")).lower()

                if (
                    textdistance.levenshtein.normalized_similarity(
                        token_lower, city_lower
                    )
                    >= 0.9
                ):
                    self.result["city"] = city
                    break

            for distinct in distinct_dict.values():
                distinct_lower = distinct.translate(
                    str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")
                ).lower()

                if (
                    textdistance.levenshtein.normalized_similarity(
                        token_lower, distinct_lower
                    )
                    >= 0.9
                ):
                    self.result["distinct"] = distinct
                    break

            for neighbourhood in neighbourhood_dict.values():
                neighbourhood_lower = neighbourhood.translate(
                    str.maketrans("ĞIİÖÜŞÇ", "ğıiöüşç")
                ).lower()

                if (
                    textdistance.levenshtein.normalized_similarity(
                        token_lower, neighbourhood_lower
                    )
                    >= 0.9
                ):
                    self.result["neighbourhood"] = neighbourhood
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
            "city": None,
            "distinct": None,
            "neighbourhood": None,
            "street_road": None,
            "apartment": None,
            "block": None,
            "floor": None,
            "apartment_no": None,
            "excessData": {},
            "originalText": copy.deepcopy(text),
        }
        self.text = self.text.split("\n")[-1]
        self.text = remove_punct_pattern.sub(" ", self.text)
        unidecoded_text = self.process_text(self.text)

        # extract city
        try:
            extracted_il = city_pattern.findall(unidecoded_text)[0]
            unidecoded_text = unidecoded_text.replace(extracted_il, "")
            self.result["city"] = city_dict[extracted_il].title()
        except Exception as e:
            print(str(e))
            self.result["city"] = ""

        # extract distinct
        try:
            extracted_distinct = distinct_pattern.findall(unidecoded_text)[0]
            unidecoded_text = unidecoded_text.replace(extracted_distinct, "")
            self.result["distinct"] = distinct_dict[extracted_distinct].title()
        except Exception as e:
            print(str(e))
            self.result["distinct"] = ""

        # extract mahalle
        try:
            self.result["neighbourhood"] = neighbourhood_pattern_v2.findall(self.text)[
                0
            ][0].strip()
            # extended_mahalle = self.get_until_stopword(self.result["originalText"], self.result["mahalle"])
            # self.result["mahalle"] = extended_mahalle
            self.text = self.text.replace(self.result["neighbourhood"], "")

        except Exception as e:
            print(str(e))
            try:
                extracted_neighbourhood = neighbourhood_pattern.findall(unidecoded_text)[0]
                # unidecoded_text = unidecoded_text.replace(extracted_extracted_neighbourhood, "")
                self.result["neighbourhood"] = neighbourhood_dict[extracted_neighbourhood]
            except Exception as e:
                print(str(e))
                self.result["neighbourhood"] = ""

        # extract street / road
        try:
            self.result["street_road"] = street_road_boulevard_pattern.findall(
                self.text
            )[0][1].strip()
            self.text = self.text.replace(self.result["street_road"], "")
        except Exception as e:
            print(str(e))
            self.result["street_road"] = ""

        # extract site / apartment / bina

        try:
            self.result["apartment"] = site_apartment_pattern.findall(self.text)[0][
                1
            ].strip()
            # extended_site = self.get_until_stopword(self.result["originalText"], self.result["site_apartman_bina"])
            # self.result["site_apartment_bina"] = extended_site
            self.text = self.text.replace(self.result["apartment"], "")
        except Exception as e:
            print(str(e))
            self.result["apartment"] = ""

        # extract block
        try:
            self.result["block"] = block_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["block"], "")
            self.result["block"] = self.result["block"].replace("block", "").strip()
        except Exception as e:
            print(str(e))
            self.result["block"] = ""

        # extract kat

        try:
            self.result["floor"] = floor_pattern.findall(self.text)[0][0].strip()
            self.text = self.text.replace(self.result["floor"], "")
            self.result["floor"] = int(self.result["floor"].lower().replace("floor", "").strip())
        except Exception as e:
            print(str(e))
            self.result["floor"] = ""

        # extract apartment no
        try:
            self.result["apartment_no"] = apartment_no_pattern.findall(self.text)[0][
                0
            ].strip()
            self.text = self.text.replace(self.result["apartment_no"], "")
            self.result["apartment_no"] = int(
                self.result["apartment_no"]
                .lower()
                .replace("no", "")
                .replace("daire", "")
                .replace("d ", "")
                .strip()
            )
        except Exception as e:
            print(str(e))
            self.result["apartment_no"] = ""

        # extract phone
        try:
            phone_number = [
                phone_number
                for phone_number in sorted(
                    re.findall(
                        r"[+]?\d+\s?\d+\s?\d+\s?\d+\s?\d+",
                        self.text,
                    ),
                    key=len,
                    reverse=True,
                )
                if 9 <= len(phone_number) <= 18
            ][0]
            self.result["excessData"]["phone"] = (
                phone_number
                if 9 <= len(phone_number) <= 18
                else ""
            )
            self.text = self.text.replace(self.result["excessData"]["phone"], "")

        except Exception as e:
            print(str(e))
            self.result["excessData"]["phone"] = ""

        self.concat_address()
        self.calculate_score()
        return self.result

    def concat_address(self):
        address_str = ""
        for key, value in self.result.items():
            if value != "":
                if key == "city":
                    address_str = address_str + value + " ili "
                if key == "distinct":
                    address_str = address_str + value + " ilcesi "
                if key == "neighbourhood":
                    address_str = address_str + value + " mahallesi "
                if key == "street_road":
                    address_str = address_str + value + " caddesi "
                if key == "apartment":
                    address_str = address_str + value + " apartmani "
        self.result["address"] = address_str

    def calculate_score(self):
        weighted_score = 0

        if self.result["city"] != "":
            weighted_score += 5
        if self.result["distinct"] != "":
            weighted_score += 5
        if self.result["neighbourhood"] != "":
            weighted_score += 4
        if self.result["street_road"] != "":
            weighted_score += 3
        if self.result["apartment"] != "":
            weighted_score += 3
        if self.result["block"] != "":
            weighted_score += 1
        if self.result["floor"] != "":
            weighted_score += 1
        if self.result["apartment_no"] != "":
            weighted_score += 1
        if self.result["excessData"]["phone"] != "":
            weighted_score += 1

        self.result["ws"] = weighted_score / (5 + 5 + 4 + 3 + 3 + 1 + 1 + 1 + 1)
        return self.result
