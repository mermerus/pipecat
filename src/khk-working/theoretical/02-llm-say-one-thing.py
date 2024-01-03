from dailyai.services.transport.DailyTransport import DailyTransportService
from dailyai.services.llm.AzureLLMService import AzureLLMService
from dailyai.services.tts.AzureTTSService import AzureTTSService

transport = None
llm = None
tts = None


def main():
    global transport
    global llm
    global tts

    transport = DailyTransportService()
    llm = AzureLLMService()
    tts = AzureTTSService()
    mic = transport.create_audio_queue()
    tts.set_output(mic)
    llm.set_output(tts)

    transport.on("error", lambda e: print(e))
    transport.on("joined-meeting", make_one_inference_call)
    transport.start()


def make_one_inference_call():
    # ask our llm to say one thing, then leave
    llm.run_llm("tell me a joke about llamas")
    transport.on("audio-queue-empty", shutdown)


def shutdown():
    transport.stop()
    tts.close()
