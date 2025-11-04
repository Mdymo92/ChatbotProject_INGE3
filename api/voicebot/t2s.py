import pyttsx3

class TextToSpeech:
  def __init__(self):
    self.engine = pyttsx3.init()
    self.rate = 180
    self.volume = 2.0
    self.language = 'english-us'
    self.voices_list = self.engine.getProperty('voices')
    self.languages_list = []
    self.bot_engine = pyttsx3.init()
    
    # configure the engine
    print("Configuring engine...")
    self.bot_rate = self.configure_rate(180)
    self.configure_volume(2.0)
    self.configure_voice('english-us')
  
  def configure_rate(self, rate): # configure speaking rate and returns the current rate
    self.engine.setProperty('rate', rate)
    return rate

  def configure_volume(self, volume): # configure speaking volume
    self.engine.setProperty('volume', volume)
  
  def configure_voice(self, language): # configure speaking voice with language and gender and returns True if successful raises RuntimeError if not
    print("Selected parameters : Language '{}'".format(language))
    for voice in self.voices_list:
      self.languages_list.append(voice.id)
    print("-----------------------------------")
    
    for voice in self.engine.getProperty('voices'):
      if language in self.languages_list:
        language_id = self.languages_list.index(language)
        self.engine.setProperty('voice', self.voices_list[language_id].id)
        return True
        
    raise RuntimeError("Language '{}'not found".format(language)) 

  def save_to_file(self, input_text, filename): # save text to speech to a file
    self.engine.save_to_file(input_text, filename)
    self.engine.runAndWait()
    print("File saved as: ", filename)
    
  def stop(self):
    self.engine.stop()
    print("Engine stopped")
    

def process_bot_answer(query):
  tts = TextToSpeech()
  print(f'engine status: {tts.engine.isBusy()}')
  print(f'query: {query}')
  print('--' * 20)
  
  print("Converting and saving to file...")
  print(f"Bot answer being converted: {query}")# stuck here
  tts.save_to_file(query, "bot_answer.mp3")
  
  print("Done")
  print('--' * 20)
  tts.stop()


if __name__ == "__main__":  
  print("Testing TextToSpeech class")
  process_bot_answer("Hello, how are you?")
  
