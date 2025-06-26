from typing import List

from google.cloud.firestore_v1 import DocumentReference

from app.database.firestore import get_firestore_client
from app.dto.page_elements import Image, Btn
from app.dto.sponsor import SponsorDto
from app.models.common.common import SponsorLevel
from app.models.sponsor import Sponsor


class SponsorService():
    def __init__(self):
        self.db = get_firestore_client()

    def _doc_to_sponsor(self, sponsor_doc: DocumentReference) -> SponsorDto:
        out = SponsorDto(title="", level=SponsorLevel("Media_partner"))
        if sponsor_doc.exists:
            out = SponsorDto(id=sponsor_doc.id,
                          title=sponsor_doc.get("title").__str__(),
                          subtitle=sponsor_doc.get("subtitle").__str__(),
                          brief=sponsor_doc.get("brief").__str__(),
                          level=SponsorLevel(sponsor_doc.get("level")),
                          order=int(sponsor_doc.get("order").__str__()),
                          image=Image.model_validate(sponsor_doc.get("image")) if sponsor_doc.get("image") else None,
                          btn=Btn.model_validate(sponsor_doc.get("btn")) if sponsor_doc.get("btn") else None)


        return out

    def get_sponsor(self, id_sponsor) -> SponsorDto:
        sponsor_doc = self.db.collection('sponsor').document(id_sponsor)
        return self._doc_to_sponsor(sponsor_doc.get())

    def put_sponsor(self, sponsor: SponsorDto) -> SponsorDto:
        if (sponsor.btn):
            sponsor.btn.open_new_tab = True
        sponsor_to_save = Sponsor(**sponsor.model_dump(exclude={}))
        # FIXME: add COMMON USER

        if sponsor_to_save.id:
            doc_sponsor = self.db.collection("sponsor").document(sponsor_to_save.id)
            doc_sponsor.update(sponsor_to_save.model_dump(exclude={"id"}))
            out = doc_sponsor.get()
        else:
            new_sponsor = self.db.collection("sponsor").add(sponsor_to_save.model_dump(exclude={"id", }))
            out = new_sponsor[1].get()

        return self._doc_to_sponsor(out)

    def get_all_sponsors(self) -> List[SponsorDto]:
        out = []
        sponsors = self.db.collection('sponsor')

        for sponsor in sponsors.get():
            out.append(self._doc_to_sponsor(sponsor))

        return out
