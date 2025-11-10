from deep_translator import GoogleTranslator

def test_translation():
    # Test text to translate
    text = "Fuit optimum temporibus, fuit pessimus temporum, saeculi sapientiae, erat aetas stultitiae."
    
    # Translate to Hindi
    try:
        print("Translating to Hindi...")
        translated = GoogleTranslator(source='auto', target='hi').translate(text)
        print("Hindi Translation:", translated)
        
        # Translate back to English to verify
        print("\nTranslating back to English...")
        back_to_eng = GoogleTranslator(source='auto', target='en').translate(translated)
        print("Back to English:", back_to_eng)
        
    except Exception as e:
        print("Error during translation:", str(e))

if __name__ == "__main__":
    test_translation()
