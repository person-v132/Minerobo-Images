import os
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Tuple, Iterator

import requests
from bs4 import BeautifulSoup

data: Dict[str, List[Tuple[str, str]]] = {
    "A": [
        ("actinolite", "amphibole group"),
        ("agate", "quartz varieties"),
        ("alabaster", "gypsum varieties"),
        ("albite", "feldspar - plagioclase"),
        ("almandine", "garnet group"),
        ("amazonite", "feldspar - potassium"),
        ("amethyst", "quartz varieties"),
        ("amphibolite", "metamorphic"),
        ("andesite", "igneous"),
        ("anthracite", "coal varieties"),
        ("apatite", "phosphates"),
        ("apophyllite", "silicates"),
        ("aragonite", "carbonates"),
        ("arkose", "sandstone varieties"),
        ("augite", "pyroxene group"),
        ("aventurine", "quartz varieties"),
        ("azurite", "carbonates"),
    ],
    "B": [
        ("banded iron", "sedimentary"),
        ("barite", "sulfates"),
        ("basalt", "igneous"),
        ("bauxite", "sedimentary"),
        ("beryl", "silicates"),
        ("biotite", "mica group"),
        ("bituminous coal", "coal varieties"),
        ("bornite", "sulfides"),
        ("breccia", "sedimentary"),
    ],
    "C": [
        ("calcite", "carbonates"),
        ("celestite", "sulfates"),
        ("chalcedony", "quartz varieties"),
        ("chalcopyrite", "sulfides"),
        ("chalk", "limestone varieties"),
        ("chert", "sedimentary"),
        ("citrine", "quartz varieties"),
        ("conglomerate", "sedimentary"),
        ("copper", "native elements"),
        ("coquina", "limestone varieties"),
        ("corundum", "(hydr)oxides"),
    ],
    "D": [
        ("diamond", "native elements"),
        ("diatomite", "sedimentary"),
        ("diorite", "igneous"),
        ("dolomite", "carbonates"),
        ("dolostone", "sedimentary"),
    ],
    "E": [("epidote", "silicates")],
    "F": [("fluorite", "halides"), ("fossiliferous limestone", "limestone varieties")],
    "G": [
        ("gabbro", "igneous"),
        ("galena", "sulfides"),
        ("garnet", "garnet group"),
        ("garnet schist", "schist varieties"),
        ("gneiss", "metamorphic"),
        ("goethite", "(hydr)oxides"),
        ("gold", "native elements"),
        ("granite", "igneous"),
        ("graphite", "native elements"),
        ("greywacke", "sandstone varieties"),
    ],
    "H": [
        ("halite", "halides"),
        ("hematite", "(hydr)oxides"),
        ("hornblende", "amphibole group"),
    ],
    "J": [("jasper", "quartz varieties")],
    "K": [("kaolinite", "silicates"), ("kyanite", "silicates")],
    "L": [
        ("labradorite", "feldspar - plagioclase"),
        ("lepidolite", "mica group"),
        ("lignite", "coal varieties"),
        ("limonite", "(hydr)oxides"),
    ],
    "M": [
        ("magnetite", "(hydr)oxides"),
        ("malachite", "carbonates"),
        ("marble", "metamorphic"),
        ("mica schist", "schist varieties"),
        ("microcline", "feldspar - potassium"),
        ("milky quartz", "quartz varieties"),
        ("muscovite", "mica group"),
    ],
    "O": [
        ("obsidian", "igneous"),
        ("olivine", "silicates"),
        ("oolitic limestone", "limestone varieties"),
        ("opal", "quartz varieties"),
        ("orthoclase", "feldspar - potassium"),
    ],
    "P": [
        ("pegmatite", "igneous"),
        ("peridotite", "igneous"),
        ("phyllite", "metamorphic"),
        ("pumice", "igneous"),
        ("pyrite", "sulfides"),
        ("pyrolusite", "(hydr)oxides"),
        ("pyromorphite", "phosphates"),
    ],
    "Q": [("quartz sandstone", "sandstone varieties"), ("quartzite", "metamorphic")],
    "R": [
        ("rhodochrosite", "carbonates"),
        ("rhodonite", "pyroxene group"),
        ("rhyolite", "igneous"),
        ("rock crystal", "quartz varieties"),
        ("rock gypsum", "sedimentary"),
        ("rock salt", "sedimentary"),
        ("rose quartz", "quartz varieties"),
        ("rutile", "(hydr)oxides"),
    ],
    "S": [
        ("satin spar", "gypsum varieties"),
        ("scoria", "igneous"),
        ("selenite", "gypsum varieties"),
        ("serpentinite", "metamorphic"),
        ("shale", "sedimentary"),
        ("silver", "native elements"),
        ("slate", "metamorphic"),
        ("smoky quartz", "quartz varieties"),
        ("soapstone", "schist varieties"),
        ("sodalite", "silicates"),
        ("sphalerite", "sulfides"),
        ("spodumene", "pyroxene group"),
        ("staurolite", "silicates"),
        ("stibnite", "sulfides"),
        ("stilbite", "silicates"),
        ("sulfur", "native elements"),
        ("syenite", "igneous"),
    ],
    "T": [
        ("talc", "silicates"),
        ("topaz", "silicates"),
        ("tourmaline group", "silicates"),
        ("travertine", "limestone varieties"),
        ("tremolite", "amphibole group"),
        ("tuff", "igneous"),
        ("turquoise", "phosphates"),
    ],
    "U": [("ulexite", "borates")],
    "V": [("vanadinite", "phosphates")],
    "W": [("willemite", "silicates")],
    "Z": [("zincite", "(hydr)oxides"), ("zircon", "silicates")],
}


def download_file(url, path):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except requests.exceptions.HTTPError as e:
        print(f"Error downloading {url} to {path}: {e}")
        return None


image_counts: Dict[str, int] = {}

base_url = "https://www.minerals.net/"
images_url = base_url + "MineralImages/"
image_gallery_url = images_url + "{}.aspx"

for letter, specimens in data.items():
    print("letter: ", letter)

    page = requests.get(image_gallery_url.format(letter))
    soup = BeautifulSoup(page.content, "lxml")
    image_links: Iterator[Tuple[str, str]] = map(
        lambda x: (x["href"].split("/")[-1].split(".")[0], x["href"]),
        soup.findAll("a", href=lambda x: "../Image/" in x),
    )
    found_specimens: Dict[str, List[str]] = {}
    for name, link in image_links:
        found_specimens.setdefault(name, [])
        found_specimens[name].append(link)

    for specimen, category in specimens:
        print("specimen: ", specimen)
        os.makedirs(dest_path := os.path.join(category, specimen), exist_ok=True)
        if specimen in found_specimens:
            image_counts[specimen] = 0
            for i, image_link in enumerate(found_specimens[specimen]):
                print("processing ", i, " of ", len(found_specimens[specimen]))
                info_card = requests.get(images_url + image_link)
                card_soup = BeautifulSoup(info_card.content, "lxml")
                image_url = (
                    base_url
                    + parse_qs(
                        urlparse(
                            card_soup.find("img", src=lambda x: "thumbnail.aspx" in x)[
                                "src"
                            ]
                        ).query
                    )["image"][0]
                )
                res = download_file(
                    image_url, dest_path + "/" + image_url.split("/")[-1]
                )
                if res:
                    image_counts[specimen] += 1
        else:
            print("none found")
            image_counts[specimen] = 0
            with open(dest_path + "/.keep", "w") as f:
                f.write("")


print(image_counts)
with open("counts.txt", "w") as f:
    for member, count in image_counts.items():
        f.write("{},{}\n".format(member, count))
