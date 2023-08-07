#########################################################################
#
# Copyright (C) 2018 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import os
import json
import time
import uuid
import shutil
import logging
import zipfile
import requests
import tempfile
import warnings
import pathlib
from typing import Union
from datetime import datetime

from .utils import utils

from distutils import dir_util
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse, urljoin

from geonode.br.models import RestoredBackup
from geonode.br.tasks import restore_notification
from geonode.utils import DisableDjangoSignals, copy_tree, extract_archive, chmod_tree
from geonode.base.models import Configuration

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Restore the GeoNode application data"

    def add_arguments(self, parser):
        # Named (optional) arguments
        utils.option(parser)

        utils.geoserver_option_list(parser)

        
    def handle(self, **options):
       
        config = Configuration.load()


        utils.setup_logger()

        try:
            self.execute_restore(**options)
        except Exception:
            raise
        finally:
            pass

    def execute_restore(self, **options):
        #self.test()
        self.restore_geoserver_backup()
                        
    def test(self):
        url = settings.OGC_SERVER["default"]["LOCATION"]

        payload = json.dumps({
        "restore": {
            "archiveFile": "/backup_restore/geoserver_catalog.zip",
            "options": {
            "option": [
                "BK_PURGE_RESOURCES=true",
                "BK_CLEANUP_TEMP=true",
                "BK_SKIP_SETTINGS=true",
                "BK_SKIP_SECURITY=true",
                "BK_BEST_EFFORT=true",
                "exclude.file.path="
            ]
            }
        }
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            #'Authorization': 'Basic YWRtaW46Z2Vvc2VydmVy',
        }
        user = settings.OGC_SERVER["default"]["USER"]
        passwd = settings.OGC_SERVER["default"]["PASSWORD"]

        response = requests.request("POST", f"{url}rest/br/restore/", headers=headers, data=payload,
                                    auth=HTTPBasicAuth(user, passwd))

        print(response.text)

    def restore_geoserver_backup(
        self
    ):
        """Restore GeoServer Catalog"""
        url = settings.OGC_SERVER["default"]["LOCATION"]
        user = settings.OGC_SERVER["default"]["USER"]
        passwd = settings.OGC_SERVER["default"]["PASSWORD"]
        geoserver_bk_file = '/backup_restore/geoserver_catalog.zip'

        logger.info(f"*** Restoring GeoServer catalog [{url}] from '{geoserver_bk_file}'")

        if not os.path.exists(geoserver_bk_file) or not os.access(geoserver_bk_file, os.R_OK):
            raise Exception(f'ERROR: geoserver restore: file "{geoserver_bk_file}" not found.')

        def bstr(x):
            return "true" if x else "false"

        # Best Effort Restore: 'options': {'option': ['BK_BEST_EFFORT=true']}
        _options = [
            f"BK_PURGE_RESOURCES=true",
            "BK_CLEANUP_TEMP=true",
            f"BK_SKIP_SETTINGS=true",
            f"BK_SKIP_SECURITY=true",
            "BK_BEST_EFFORT=true",
            f"exclude.file.path=",
        ]
        _options = [
                "BK_PURGE_RESOURCES=true",
                "BK_CLEANUP_TEMP=true",
                "BK_SKIP_SETTINGS=true",
                "BK_SKIP_SECURITY=true",
                "BK_BEST_EFFORT=true",
                "exclude.file.path="
            ]
        data = {"restore": {"archiveFile": geoserver_bk_file, "options": {"option": _options}}}
        headers = {
            "Accept": "application/json", 
            "Content-type": "application/json"
        }

        payload = json.dumps({
        "restore": {
            "archiveFile": "/backup_restore/geoserver_catalog.zip",
            "options": {
            "option": [
                "BK_PURGE_RESOURCES=true",
                "BK_CLEANUP_TEMP=true",
                "BK_SKIP_SETTINGS=true",
                "BK_SKIP_SECURITY=true",
                "BK_BEST_EFFORT=true",
                "exclude.file.path="
            ]
            }
        }
        })
        print(payload)
        r = requests.post(
            f"{url}rest/br/restore/", data=payload, headers=headers, auth=HTTPBasicAuth(user, passwd)
        )
        error_backup = "Could not successfully restore GeoServer catalog [{}rest/br/restore/]: {} - {}"
        print("===============")
        print(r.status_code)
        print(r.text)
        print("===============")
        if r.status_code in (200, 201, 406):
            try:
                r = requests.get(
                    f"{url}rest/br/restore.json", headers=headers, auth=HTTPBasicAuth(user, passwd), timeout=10
                )
                print(f"==============={url}rest/br/restore.json")
                print(r.status_code)
                print(r.text)
                print("===============")
                if r.status_code == 200:
                    gs_backup = r.json()
                    _url = urlparse(gs_backup["restores"]["restore"][len(gs_backup["restores"]["restore"]) - 1]["href"])
                    _url = f"{urljoin(url, _url.path)}?{_url.query}"
                    r = requests.get(_url, headers=headers, auth=HTTPBasicAuth(user, passwd), timeout=10)
                    print(f"==============={_url}")
                    print(r.status_code)
                    print(r.text)
                    print("===============")
                    if r.status_code == 200:
                        gs_backup = r.json()

                if r.status_code != 200:
                    raise ValueError(error_backup.format(url, r.status_code, r.text))
            except ValueError:
                raise ValueError(error_backup.format(url, r.status_code, r.text))
            
            time.sleep(3)
            gs_bk_exec_id = gs_backup["restore"]["execution"]["id"]
            r = requests.get(
                f"{url}rest/br/restore/{gs_bk_exec_id}.json",
                headers=headers,
                auth=HTTPBasicAuth(user, passwd),
                timeout=10,
            )

            
            print(f"==============={url}rest/br/restore/{gs_bk_exec_id}.json")
            print(r.status_code)
            print(r.text)
            print("===============")
            if r.status_code in (200,):
                gs_bk_exec_status = gs_backup["restore"]["execution"]["status"]
                gs_bk_exec_progress = gs_backup["restore"]["execution"]["progress"]
                gs_bk_exec_progress_updated = "0/0"
                while gs_bk_exec_status != "COMPLETED" and gs_bk_exec_status != "FAILED":
                    if gs_bk_exec_progress != gs_bk_exec_progress_updated:
                        gs_bk_exec_progress_updated = gs_bk_exec_progress
                    r = requests.get(
                        f"{url}rest/br/restore/{gs_bk_exec_id}.json",
                        headers=headers,
                        auth=HTTPBasicAuth(user, passwd),
                        timeout=10,
                    )

                    if r.status_code == 200:
                        try:
                            gs_backup = r.json()
                        except ValueError:
                            raise ValueError(error_backup.format(url, r.status_code, r.text))

                        gs_bk_exec_status = gs_backup["restore"]["execution"]["status"]
                        gs_bk_exec_progress = gs_backup["restore"]["execution"]["progress"]
                        logger.info(f"Async backup status: {gs_bk_exec_status} - {gs_bk_exec_progress}")
                        time.sleep(3)
                    else:
                        raise ValueError(error_backup.format(url, r.status_code, r.text))

                if gs_bk_exec_status != "COMPLETED":
                    raise ValueError(error_backup.format(url, r.status_code, r.text))

            else:
                raise ValueError(error_backup.format(url, r.status_code, r.text))

        else:
            raise ValueError(error_backup.format(url, r.status_code, r.text))