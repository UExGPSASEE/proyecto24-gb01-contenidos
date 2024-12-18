from models.language import Language
from lang_client import LanguageClient

class LanguageCtrl:

    err_msg = 'Missing data or incorrect method';

    @staticmethod
    def getLanguageById(idLanguage):
        if idLanguage:
            idLanguage = int(idLanguage)
            return LanguageClient.getLanguage(idLanguage)
        else:
            return jsonify({'error': LanguageCtrl.err_msg, 'status': '400 Bad Request'}), 400
