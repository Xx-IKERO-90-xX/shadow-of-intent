from extensions import db
from models.EvilDomain import EvilDomain
from models.Repository import Repository
import aiohttp
import requests
from urllib.parse import urlparse
from flask import current_app


async def extract_from_JSON_repository(repo: Repository):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(repo.url) as response:
                if response != 200:
                    return
                
                data = await response.json()

                with current_app.app_context():
                    for item in data:
                        try:
                            item_http = "http://" + item
                            domain_http = EvilDomain(item_http)

                            db.session.add(domain_http)
                            db.session.commit()
                        except:
                            pass

                        try:
                            item_https = "https://" + item
                            domain = EvilDomain(item_https)

                            db.session.add(domain)
                            db.session.commit()
                        except:
                            pass
                        
        except Exception as e:
            print(f"Error fetching JSON repository: {e}")


async def extract_from_TXT_repository(repo: Repository):
    response = requests.get(repo.url, timeout=10)
    
    if response.status_code == 200:
        data = response.text.splitlines()
        
        with current_app.app_context():
            for item in data:
                try:
                    item_http = "http://" + item
                    domain = EvilDomain(item_http)

                    db.session.add(domain)
                    db.session.commit()
                except:
                    pass

                try:
                    item_https = "https://" + item
                    domain = EvilDomain(item_https)

                    db.session.add(domain)
                    db.session.commit()
                except:
                    pass
    else:
        return
    



