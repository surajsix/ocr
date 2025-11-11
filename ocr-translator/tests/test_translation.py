import unittest
from deep_translator import GoogleTranslator
from typing import Dict, Tuple
import time

class TestTranslationAccuracy(unittest.TestCase):    
    # Test cases: (source_text, expected_translation, language_code, language_name)
    TEST_CASES = [
        # English to other languages
        ("Hello, how are you?", "Hola, ¿cómo estás?", "es", "Spanish"),
        ("Hello, how are you?", "Bonjour, comment ça va?", "fr", "French"),
        ("Hello, how are you?", "नमस्ते, आप कैसे हैं?", "hi", "Hindi"),
        ("Hello, how are you?", "Hallo, wie geht's?", "de", "German"),
        ("Hello, how are you?", "Ciao, come stai?", "it", "Italian"),
        
        # Non-English to English
        ("こんにちは、お元気ですか？", "Hello, how are you?", "en", "English"),
        ("안녕하세요, 어떻게 지내세요?", "Hello, how are you?", "en", "English"),
        
        # Special characters and numbers
        ("The price is $19.99", "O preço é $19.99", "pt", "Portuguese"),
        ("100% real", "100% real", "es", "Spanish"),
        
        # Long text
        ("This is a longer text to test if the translation maintains context and meaning across multiple sentences.", 
         "Este es un texto más largo para probar si la traducción mantiene el contexto y el significado en varias oraciones.",
         "es", "Spanish")
    ]
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.translator = GoogleTranslator()
        self.threshold = 0.7  # Minimum similarity score to consider translation acceptable (0-1)
    
    def _get_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings (0-1)."""
        # Simple character-based similarity (can be enhanced with more sophisticated algorithms)
        if not text1 or not text2:
            return 0.0
            
        text1 = text1.lower()
        text2 = text2.lower()
        
        # Count matching characters
        matches = 0
        min_len = min(len(text1), len(text2))
        max_len = max(len(text1), len(text2))
        
        for i in range(min_len):
            if text1[i] == text2[i]:
                matches += 1
                
        # Normalize by max length to get a 0-1 score
        return matches / max(1, max_len)
    
    def _test_translation_accuracy(self, source_text: str, expected_translation: str, 
                                 target_lang: str, language_name: str):
        """Test if translation from source_text to target_lang matches expected_translation."""
        try:
            # Translate the text
            translated = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
            
            # Calculate similarity between expected and actual translation
            similarity = self._get_similarity(expected_translation, translated)
            
            # Print test results
            print(f"\n{'='*50}")
            print(f"Testing {language_name} ({target_lang}):")
            print(f"Original:    {source_text}")
            print(f"Expected:    {expected_translation}")
            print(f"Translated:  {translated}")
            print(f"Similarity:  {similarity:.2f} (Threshold: {self.threshold})")
            
            # Verify similarity meets threshold
            self.assertGreaterEqual(
                similarity, self.threshold,
                f"Translation to {language_name} failed. Similarity ({similarity:.2f}) "
                f"is below threshold ({self.threshold})."
            )
            
            # Verify back-translation for additional validation
            if target_lang != 'en':
                back_translated = GoogleTranslator(source=target_lang, target='en').translate(translated)
                back_similarity = self._get_similarity(source_text.lower(), back_translated.lower())
                print(f"Back to EN:  {back_translated}")
                print(f"Back Similarity: {back_similarity:.2f}")
                
                # Verify back-translation makes sense
                self.assertGreaterEqual(
                    back_similarity, 0.5,  # Lower threshold for back-translation
                    f"Back-translation from {language_name} to English failed. "
                    f"Original: '{source_text}', Back-translated: '{back_translated}'"
                )
            
        except Exception as e:
            self.fail(f"Error testing {language_name} translation: {str(e)}")
    
    def test_all_translations(self):
        """Run all translation tests."""
        for source_text, expected_translation, lang_code, lang_name in self.TEST_CASES:
            with self.subTest(language=lang_name):
                self._test_translation_accuracy(
                    source_text, expected_translation, lang_code, lang_name
                )
                time.sleep(1)  # Add delay to avoid rate limiting

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
