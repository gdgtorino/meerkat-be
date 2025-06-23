from typing import List

from google.cloud.firestore_v1 import DocumentReference

from app.database.firestore import get_firestore_client
from app.dto.talk import TalkDto
from app.models.talk import Talk


class TalkService():
    def __init__(self):
        self.db = get_firestore_client()

    def _doc_to_talk(self, talk_doc: DocumentReference) -> TalkDto:
        out = TalkDto(title="", speakers=[])
        if talk_doc.exists:
            out = TalkDto(id=talk_doc.id,
                          title=talk_doc.get("title").__str__(),
                          subtitle=talk_doc.get("subtitle").__str__(),
                          brief=talk_doc.get("brief").__str__(),
                          description=talk_doc.get("description").__str__(),
                          level=talk_doc.get("level").__str__(),
                          language=talk_doc.get("language").__str__(),
                          speakers=talk_doc.get("speakers"))

        return out

    def get_talk(self, id_talk) -> TalkDto:
        talk_doc = self.db.collection('talk').document(id_talk)
        return self._doc_to_talk(talk_doc.get())

    def put_talk(self, talk: TalkDto) -> TalkDto:
        talk_to_save = Talk(**talk.model_dump(exclude={}))
        # FIXME: add COMMON USER

        if talk_to_save.id:
            doc_talk = self.db.collection("talk").document(talk_to_save.id)
            doc_talk.update(talk_to_save.model_dump(exclude={"id"}))
            out = doc_talk.get()
        else:
            new_talk = self.db.collection("talk").add(talk_to_save.model_dump(exclude={"id"}))
            out = new_talk[1].get()

        return self._doc_to_talk(out)

    def get_all_talks(self) -> List[TalkDto]:
        out = []
        talks = self.db.collection('talk')

        for talk in talks.get():
            out.append(self._doc_to_talk(talk))

        return out
