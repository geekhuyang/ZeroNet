import shutil
import os

import pytest


@pytest.mark.usefixtures("resetSettings")
class TestSite:
    def testClone(self, site):
        assert site.storage.directory == "src/Test/testdata/1TeSTvb4w2PWE81S2rEELgmX2GCCExQGT"

        # Remove old files
        if os.path.isdir("src/Test/testdata/159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL"):
            shutil.rmtree("src/Test/testdata/159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL")
        assert not os.path.isfile("src/Test/testdata/159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL/content.json")

        # Clone 1TeSTvb4w2PWE81S2rEELgmX2GCCExQGT to 15E5rhcAUD69WbiYsYARh4YHJ4sLm2JEyc
        new_site = site.clone(
            "159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL", "5JU2p5h3R7B1WrbaEdEDNZR7YHqRLGcjNcqwqVQzX2H4SuNe2ee", address_index=1
        )

        # Check if clone was successful
        assert new_site.address == "159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL"
        assert new_site.storage.isFile("content.json")
        assert new_site.storage.isFile("index.html")
        assert new_site.storage.isFile("data/users/content.json")
        assert new_site.storage.isFile("data/zeroblog.db")

        # Test re-cloning (updating)

        # Changes in non-data files should be overwritten
        new_site.storage.write("index.html", "this will be overwritten")
        assert new_site.storage.read("index.html"), "this will be overwritten"

        # Changes in data file should be kept after re-cloning
        changed_contentjson = new_site.storage.loadJson("content.json")
        changed_contentjson["description"] = "Update Description Test"
        new_site.storage.writeJson("content.json", changed_contentjson)

        changed_data = new_site.storage.loadJson("data/data.json")
        changed_data["title"] = "UpdateTest"
        new_site.storage.writeJson("data/data.json", changed_data)

        # Re-clone the site
        site.clone("159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL")

        assert new_site.storage.loadJson("data/data.json")["title"] == "UpdateTest"
        assert new_site.storage.loadJson("content.json")["description"] == "Update Description Test"
        assert new_site.storage.read("index.html") != "this will be overwritten"

        # Delete created files
        if os.path.isdir("src/Test/testdata/159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL"):
            new_site.storage.closeDb()
            shutil.rmtree("src/Test/testdata/159EGD5srUsMP97UpcLy8AtKQbQLK2AbbL")