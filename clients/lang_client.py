import requests


class LanguageClient:
    BASE_URL = "http://127.0.0.1:8083"

    @staticmethod
    def getLanguage(id_language):
        url = f"{LanguageClient.BASE_URL}/languages/{id_language}"
        response = requests.get(url)
        return LanguageClient.handleResponse(response)

    @staticmethod
    def handleResponse(response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
