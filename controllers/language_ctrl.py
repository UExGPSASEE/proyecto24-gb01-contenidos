from models.language import Language
from lang_client import LanguageClient

class LanguageCtrl:

    @staticmethod
    def getLanguageById(idLanguage):
        if idLanguage:
            idLanguage = int(idLanguage)
            return LanguageClient.getLanguage(idLanguage)
        else:
            return jsonify({'error': 'Missing data or incorrect method', 'status': '400 Bad Request'}), 400
