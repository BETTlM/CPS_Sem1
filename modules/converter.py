import pdfminer.high_level as pdfminer
from modules import writer
from modules import audiorecorder
def convert(pdflocation):
        content = pdfminer.extract_text(pdflocation)
        writer.writenow(content)
        audiorecorder.record('Bettim/book.txt','Bettim/recordedaudio.mp3')
        print('PASSED A')
    