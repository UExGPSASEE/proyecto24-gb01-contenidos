from models.language import Language
from lang_client import LanguageClient

class LanguageCtrl:

    err_msg = 'Missing data or incorrect method';
    bad_request = '400 Bad Request';

    @staticmethod
    def get_language_by_id(idLanguage):
        if idLanguage:
            idLanguage = int(idLanguage)
            return LanguageClient.getLanguage(idLanguage)
        else:
            return jsonify({'error': LanguageCtrl.err_msg, 'status': LanguageCtrl.bad_request}), 400
