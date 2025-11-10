import requests
from typing import Optional
from ..config import LIBRETRANSLATE_URL, DEEPL_API_KEY, TRANSLATION_SERVICE

class TranslationService:
    """Handles text translation using different translation providers"""
    
    def __init__(self):
        self.provider = TRANSLATION_SERVICE.lower()
        self.session = requests.Session()
        
    def translate(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'es', 'fr')
            source_lang: Source language code (default: 'auto' for auto-detection)
            
        Returns:
            Translated text
        """
        if not text.strip():
            return text
            
        if self.provider == 'deepl' and DEEPL_API_KEY:
            return self._translate_deepl(text, target_lang, source_lang)
        else:
            return self._translate_libretranslate(text, target_lang, source_lang)
    
    def _translate_libretranslate(self, text: str, target_lang: str, source_lang: str) -> str:
        """Translate using LibreTranslate API"""
        try:
            payload = {
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text',
                'api_key': ''  # Add API key if required
            }
            
            response = self.session.post(
                f"{LIBRETRANSLATE_URL}/translate",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json().get('translatedText', text)
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text  # Fallback to original text
    
    def _translate_deepl(self, text: str, target_lang: str, source_lang: str) -> str:
        """Translate using DeepL API"""
        if not DEEPL_API_KEY:
            raise ValueError("DeepL API key not configured")
            
        try:
            url = "https://api-free.deepl.com/v2/translate"
            headers = {
                "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text": [text],
                "target_lang": target_lang.upper(),
                "source_lang": source_lang.upper() if source_lang != 'auto' else None
            }
            
            response = self.session.post(
                url,
                headers=headers,
                json={k: v for k, v in data.items() if v is not None},
                timeout=30
            )
            response.raise_for_status()
            return response.json()['translations'][0]['text']
            
        except Exception as e:
            print(f"DeepL translation error: {str(e)}")
            # Fallback to LibreTranslate
            return self._translate_libretranslate(text, target_lang, source_lang)
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        if self.provider == 'deepl' and DEEPL_API_KEY:
            return self._get_deepl_languages()
        else:
            return self._get_libretranslate_languages()
    
    def _get_libretranslate_languages(self) -> list:
        """Get supported languages from LibreTranslate"""
        try:
            response = self.session.get(f"{LIBRETRANSLATE_URL}/languages", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            # Return a default list of common languages if API is not available
            return [
                {'code': 'en', 'name': 'English'},
                {'code': 'es', 'name': 'Spanish'},
                {'code': 'fr', 'name': 'French'},
                {'code': 'de', 'name': 'German'},
                {'code': 'it', 'name': 'Italian'},
                {'code': 'pt', 'name': 'Portuguese'},
                {'code': 'ru', 'name': 'Russian'},
                {'code': 'zh', 'name': 'Chinese'},
                {'code': 'ja', 'name': 'Japanese'},
                {'code': 'hi', 'name': 'Hindi'},
            ]
    
    def _get_deepl_languages(self) -> list:
        """Get supported languages from DeepL"""
        # DeepL doesn't provide a public API for this, so we return common languages
        return [
            {'code': 'BG', 'name': 'Bulgarian'},
            {'code': 'CS', 'name': 'Czech'},
            {'code': 'DA', 'name': 'Danish'},
            {'code': 'DE', 'name': 'German'},
            {'code': 'EL', 'name': 'Greek'},
            {'code': 'EN', 'name': 'English'},
            {'code': 'ES', 'name': 'Spanish'},
            {'code': 'ET', 'name': 'Estonian'},
            {'code': 'FI', 'name': 'Finnish'},
            {'code': 'FR', 'name': 'French'},
            {'code': 'HU', 'name': 'Hungarian'},
            {'code': 'ID', 'name': 'Indonesian'},
            {'code': 'IT', 'name': 'Italian'},
            {'code': 'JA', 'name': 'Japanese'},
            {'code': 'KO', 'name': 'Korean'},
            {'code': 'LT', 'name': 'Lithuanian'},
            {'code': 'LV', 'name': 'Latvian'},
            {'code': 'NB', 'name': 'Norwegian'},
            {'code': 'NL', 'name': 'Dutch'},
            {'code': 'PL', 'name': 'Polish'},
            {'code': 'PT', 'name': 'Portuguese'},
            {'code': 'RO', 'name': 'Romanian'},
            {'code': 'RU', 'name': 'Russian'},
            {'code': 'SK', 'name': 'Slovak'},
            {'code': 'SL', 'name': 'Slovenian'},
            {'code': 'SV', 'name': 'Swedish'},
            {'code': 'TR', 'name': 'Turkish'},
            {'code': 'UK', 'name': 'Ukrainian'},
            {'code': 'ZH', 'name': 'Chinese'},
        ]
