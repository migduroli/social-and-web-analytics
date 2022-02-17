from enum import Enum
from google.cloud import language_v1


class Callables(Enum):
    CLASSIFY_TEXT = 1
    ANALYSE_SYNTAX = 2
    ANALYSE_SENTIMENT = 3
    ANALYSE_ENTITY_SENTIMENT = 4


class GoogleNLApi:

    def __init__(
            self,
            doc_type: language_v1.Document.Type = language_v1.Document.Type.PLAIN_TEXT,
            encoding: language_v1.EncodingType = language_v1.EncodingType.UTF8,
            language: str = None
    ):
        self.type_ = doc_type
        self.document = {
            "type_": self.type_,
            "language": language
        }
        # Available values: NONE, UTF8, UTF16, UTF32
        self.encoding_type = encoding
        self.client = language_v1.LanguageServiceClient()

        self.callables = {
            Callables.ANALYSE_SENTIMENT: self.client.analyze_sentiment,
            Callables.CLASSIFY_TEXT: self.client.classify_text,
            Callables.ANALYSE_SYNTAX: self.client.analyze_syntax,
            Callables.ANALYSE_ENTITY_SENTIMENT: self.client.analyze_entity_sentiment
        }

    def _proto_call(self, text, func):
        document = {
            **self.document,
            "content": text,
        }

        params = {"document": document}
        if func != Callables.CLASSIFY_TEXT:
            params = {
                **params,
                "encoding_type": self.encoding_type
            }

        response = self.callables[func](request=params)
        return response

    def analyse_sentiment(self, text):
        return self._proto_call(
            text=text,
            func=Callables.ANALYSE_SENTIMENT
        )

    def classify_text(self, text):
        return self._proto_call(
            text=text,
            func=Callables.CLASSIFY_TEXT
        )

    def analyse_syntax(self, text):
        return self._proto_call(
            text=text,
            func=Callables.ANALYSE_SYNTAX
        )

    def analyse_entity_sentiment(self, text):
        return self._proto_call(
            text=text,
            func=Callables.ANALYSE_ENTITY_SENTIMENT
        )
