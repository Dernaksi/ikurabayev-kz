#!/usr/bin/env python3
"""Build deterministic RU/EN public CV drafts and block-level provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "public-facts.json"
GRAPH_PATH = ROOT / "data" / "public-research-graph.json"
RU_PATH = ROOT / "cv" / "IKurabayev_Public_CV_RU.md"
EN_PATH = ROOT / "cv" / "IKurabayev_Public_CV_EN.md"
PROVENANCE_PATH = ROOT / "cv" / "IKurabayev_Public_CV_PROVENANCE.json"

DOCUMENT_PATHS = {
    "cv.ru": "cv/IKurabayev_Public_CV_RU.md",
    "cv.en": "cv/IKurabayev_Public_CV_EN.md",
}
STATUS_ORDER = {
    "verified_public": 0,
    "partially_verified": 1,
    "owner_approved": 2,
    "roadmap_only": 3,
}


@dataclass(frozen=True)
class Block:
    """One ordered, bilingual CV content block with explicit provenance."""

    id: str
    section_id: str
    claim_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    ru_lines: tuple[str, ...]
    en_lines: tuple[str, ...]
    exclusions: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def lines(self, language: str) -> tuple[str, ...]:
        return self.ru_lines if language == "ru" else self.en_lines


SECTION_HEADINGS = {
    "ru": {
        "cv.section.identity": "Профиль",
        "cv.section.research_focus": "Исследовательский фокус",
        "cv.section.current_roles": "Текущие роли",
        "cv.section.education": "Образование",
        "cv.section.credential": "Профессиональная квалификация",
        "cv.section.research_grant": "Исследовательский проект",
        "cv.section.publications": "Избранные публикации",
        "cv.section.patents": "Патенты",
        "cv.section.recognition": "Избранные награды",
        "cv.section.projects": "Проекты в разработке",
        "cv.section.public_routes": "Публичные профили и связь",
    },
    "en": {
        "cv.section.identity": "Profile",
        "cv.section.research_focus": "Research focus",
        "cv.section.current_roles": "Current roles",
        "cv.section.education": "Education",
        "cv.section.credential": "Professional credential",
        "cv.section.research_grant": "Research project",
        "cv.section.publications": "Selected publications",
        "cv.section.patents": "Patents",
        "cv.section.recognition": "Selected recognition",
        "cv.section.projects": "Projects in development",
        "cv.section.public_routes": "Public profiles and contact",
    },
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read_json_bytes(path: Path) -> tuple[bytes, dict[str, object]]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return raw, value


def index_by_id(items: object, label: str) -> dict[str, dict[str, object]]:
    if not isinstance(items, list):
        raise ValueError(f"{label} must be an array")
    result: dict[str, dict[str, object]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError(f"{label} contains an item without a string id")
        item_id = item["id"]
        if item_id in result:
            raise ValueError(f"duplicate {label} id: {item_id}")
        result[item_id] = item
    return result


def value_of(claims: dict[str, dict[str, object]], claim_id: str) -> dict[str, object]:
    claim = claims.get(claim_id)
    if not claim or not isinstance(claim.get("value"), dict):
        raise ValueError(f"missing structured claim: {claim_id}")
    return claim["value"]


def required_text(value: dict[str, object], key: str, claim_id: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item:
        raise ValueError(f"{claim_id}: missing string value.{key}")
    return item


def required_iso_date(value: dict[str, object], key: str, claim_id: str) -> str:
    item = required_text(value, key, claim_id)
    try:
        date.fromisoformat(item)
    except ValueError as exc:
        raise ValueError(f"{claim_id}: value.{key} must be an ISO date") from exc
    return item


def relation_id_for(
    relations: dict[str, dict[str, object]],
    relation_id: str,
) -> str:
    if relation_id not in relations:
        raise ValueError(f"missing relation: {relation_id}")
    return relation_id


def source_url_for_claim(
    claim: dict[str, object],
    sources: dict[str, dict[str, object]],
    source_kind: str,
) -> str:
    for source_id in claim.get("evidence", []):
        source = sources.get(source_id)
        if source and source.get("kind") == source_kind:
            url = source.get("url")
            if isinstance(url, str) and url:
                return url
    raise ValueError(f"{claim.get('id')}: no {source_kind} URL")


def build_blocks(
    registry: dict[str, object], graph: dict[str, object]
) -> tuple[
    list[Block],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
]:
    claims = index_by_id(registry.get("claims"), "claims")
    sources = index_by_id(registry.get("sources"), "sources")
    relations = index_by_id(graph.get("relations"), "relations")
    topics = index_by_id(graph.get("topics"), "topics")

    identity = value_of(claims, "identity.name")
    review_date = registry.get("generated_or_reviewed_at")
    if not isinstance(review_date, str) or not review_date:
        raise ValueError("registry generated_or_reviewed_at must be a date string")

    blocks: list[Block] = []
    blocks.append(
        Block(
            id="cv.identity",
            section_id="cv.section.identity",
            claim_ids=("identity.name",),
            relation_ids=(),
            ru_lines=(
                f"- **Имя:** {required_text(identity, 'ru_full_name', 'identity.name')}.",
                f"- **Дата проверки исходного реестра:** {review_date}.",
            ),
            en_lines=(
                f"- **Name:** {required_text(identity, 'preferred_public_name', 'identity.name')}.",
                f"- **Source-registry review date:** {review_date}.",
            ),
            notes=("generated_public_draft_not_complete_cv",),
        )
    )

    focus_relation_ids = (
        relation_id_for(
            relations,
            "relation.research_focus.addresses_topic.insulation_parameters",
        ),
        relation_id_for(
            relations,
            "relation.research_focus.addresses_topic.energy_efficiency",
        ),
    )
    focus_topic_ids = [relations[item]["to"] for item in focus_relation_ids]
    ru_topics: list[str] = []
    en_topics: list[str] = []
    for topic_id in focus_topic_ids:
        topic = topics.get(str(topic_id))
        labels = topic.get("labels") if topic else None
        if not isinstance(labels, dict):
            raise ValueError(f"missing labels for topic {topic_id}")
        ru_topics.append(required_text(labels, "ru", str(topic_id)))
        en_topics.append(required_text(labels, "en", str(topic_id)))
    blocks.append(
        Block(
            id="cv.research_focus",
            section_id="cv.section.research_focus",
            claim_ids=("research.focus.ungrounded_power_systems",),
            relation_ids=focus_relation_ids,
            ru_lines=tuple(f"- {topic}." for topic in ru_topics),
            en_lines=tuple(f"- {topic}." for topic in en_topics),
            notes=("broad_official_profile_topics_only",),
        )
    )

    university = value_of(claims, "role.university.current")
    blocks.append(
        Block(
            id="cv.roles.university",
            section_id="cv.section.current_roles",
            claim_ids=("role.university.current",),
            relation_ids=(
                relation_id_for(relations, "relation.person.holds_role.university_current"),
            ),
            ru_lines=(
                "- **Старший преподаватель**, Казахский агротехнический "
                "исследовательский университет имени С. Сейфуллина. "
                f"Роль отмечена как текущая по состоянию на "
                f"{required_text(university, 'current_as_of', 'role.university.current')}.",
            ),
            en_lines=(
                "- **Senior Lecturer**, S. Seifullin Kazakh Agrotechnical "
                "Research University. The role is recorded as current as of "
                f"{required_text(university, 'current_as_of', 'role.university.current')}.",
            ),
            exclusions=("start_date_omitted_due_to_source_conflict",),
            notes=("role_and_organization_only",),
        )
    )

    astana = value_of(claims, "role.astana_energy.current")
    blocks.append(
        Block(
            id="cv.roles.astana_energy",
            section_id="cv.section.current_roles",
            claim_ids=("role.astana_energy.current",),
            relation_ids=(
                relation_id_for(
                    relations, "relation.person.holds_role.astana_energy_current"
                ),
            ),
            ru_lines=(
                "- **Независимый директор и член Совета директоров**, "
                "АО «Астана-Энергия». Избран: "
                f"{required_text(astana, 'elected', 'role.astana_energy.current')}; "
                "роль отмечена как текущая по состоянию на "
                f"{required_text(astana, 'current_as_of', 'role.astana_energy.current')}.",
            ),
            en_lines=(
                "- **Independent Director and Board Member**, Astana-Energy JSC. "
                f"Elected: {required_text(astana, 'elected', 'role.astana_energy.current')}; "
                "the role is recorded as current as of "
                f"{required_text(astana, 'current_as_of', 'role.astana_energy.current')}.",
            ),
            notes=("point_in_time_currentness",),
        )
    )

    education_specs = (
        (
            "education.phd.electrical_complexes_systems",
            "relation.person.holds_credential.education_phd",
            "PhD — «Электротехнические комплексы и системы»",
            "PhD — Electrical complexes and systems",
            "cv.education.phd",
        ),
        (
            "education.master.electrical_power_engineering",
            "relation.person.holds_credential.education_master",
            "Магистр технических наук — электроэнергетика",
            "Master of Technical Sciences — Electrical Power Engineering",
            "cv.education.master",
        ),
        (
            "education.specialist.industrial_power_supply",
            "relation.person.holds_credential.education_specialist",
            "Специалитет — электроснабжение промышленных предприятий; инженер-электрик",
            "Specialist degree — Industrial power supply; Engineer-electrician",
            "cv.education.specialist",
        ),
    )
    for claim_id, relation_id, ru_text, en_text, block_id in education_specs:
        value_of(claims, claim_id)
        blocks.append(
            Block(
                id=block_id,
                section_id="cv.section.education",
                claim_ids=(claim_id,),
                relation_ids=(relation_id_for(relations, relation_id),),
                ru_lines=(f"- {ru_text}.",),
                en_lines=(f"- {en_text}.",),
                exclusions=(
                    "education_dates_omitted",
                    "education_honours_omitted",
                    "document_identifiers_omitted",
                ),
            )
        )

    credential = value_of(claims, "credential.energy_auditor")
    practice_since = credential.get("professional_practice_since")
    if not isinstance(practice_since, int):
        raise ValueError("credential.energy_auditor: missing professional_practice_since")
    certificate_issued_on = required_iso_date(
        credential, "certificate_issued_on", "credential.energy_auditor"
    )
    certificate_valid_until = required_iso_date(
        credential, "certificate_valid_until", "credential.energy_auditor"
    )
    if date.fromisoformat(certificate_issued_on) >= date.fromisoformat(
        certificate_valid_until
    ):
        raise ValueError(
            "credential.energy_auditor: certificate issue date must precede validity end"
        )
    blocks.append(
        Block(
            id="cv.credential.energy_auditor",
            section_id="cv.section.credential",
            claim_ids=("credential.energy_auditor",),
            relation_ids=(
                relation_id_for(relations, "relation.person.holds_credential.energy_auditor"),
                relation_id_for(
                    relations,
                    "relation.credential.energy_auditor.addresses_topic.energy_audit",
                ),
                relation_id_for(
                    relations,
                    "relation.credential.energy_auditor.addresses_topic.energy_efficiency",
                ),
            ),
            ru_lines=(
                "- Сертифицированный энергоаудитор в области энергосбережения и "
                "повышения энергоэффективности. Сертификат выдан "
                f"{certificate_issued_on} и действителен до {certificate_valid_until}; "
                f"профессиональная практика указана с {practice_since} года.",
            ),
            en_lines=(
                "- Certified energy auditor in the field of energy saving and energy "
                "efficiency improvement. Certificate issued on "
                f"{certificate_issued_on} and valid until {certificate_valid_until}; "
                f"professional practice is recorded since {practice_since}.",
            ),
            exclusions=(
                "certificate_identifier_omitted",
                "civil_identifier_omitted",
                "qr_content_omitted",
                "address_omitted",
                "signature_and_seal_omitted",
                "raw_document_and_path_omitted",
            ),
            notes=(
                "certificate_dates_from_sanitized_owner_supplied_document_review",
                "certificate_dates_not_independently_verified_publicly",
                "professional_practice_since_is_owner_approved",
            ),
        )
    )

    grant = value_of(claims, "grant.ap22787517")
    period = grant.get("period")
    if not isinstance(period, dict):
        raise ValueError("grant.ap22787517: missing period")
    grant_start = period.get("start_year")
    grant_end = period.get("end_year")
    if not isinstance(grant_start, int) or not isinstance(grant_end, int):
        raise ValueError("grant.ap22787517: invalid period")
    blocks.append(
        Block(
            id="cv.grants.ap22787517",
            section_id="cv.section.research_grant",
            claim_ids=("grant.ap22787517",),
            relation_ids=(
                relation_id_for(relations, "relation.person.leads.ap22787517"),
                relation_id_for(
                    relations,
                    "relation.grant.ap22787517.addresses_topic.isolated_neutral_networks",
                ),
                relation_id_for(
                    relations,
                    "relation.grant.ap22787517.addresses_topic.measurement_diagnostics",
                ),
            ),
            ru_lines=(
                f"- **AP22787517** ({grant_start}–{grant_end}), руководитель проекта. "
                "Разработка и испытание прототипа прибора для измерения параметров "
                "изоляции в электрических сетях с изолированной нейтралью.",
            ),
            en_lines=(
                f"- **AP22787517** ({grant_start}–{grant_end}), Principal Investigator. "
                f"{required_text(grant, 'project_title', 'grant.ap22787517')}.",
            ),
            notes=("owner_approved_independent_grant_verification_incomplete",),
        )
    )

    publication_ids = sorted(
        (
            "publication.isolated_neutral_experimental_studies",
            "publication.gtd2_12436",
            "publication.icecet_9873012",
            "publication.yiuh4401",
            "publication.kazatc_error_estimation",
        ),
        key=lambda item: (
            -int(value_of(claims, item).get("year", 0)),
            item,
        ),
    )
    publication_relations = {
        "publication.isolated_neutral_experimental_studies": (
            "relation.person.authored.isolated_neutral_experimental_studies",
            "relation.publication.isolated_neutral_studies.addresses_topic.insulation_parameters",
        ),
        "publication.gtd2_12436": (
            "relation.person.authored.gtd2_12436",
            "relation.publication.gtd2_12436.addresses_topic.isolated_neutral_networks",
        ),
        "publication.icecet_9873012": (
            "relation.person.authored.icecet_9873012",
            "relation.publication.icecet_9873012.addresses_topic.measurement_diagnostics",
        ),
        "publication.yiuh4401": (
            "relation.person.authored.yiuh4401",
            "relation.publication.yiuh4401.addresses_topic.measurement_diagnostics",
        ),
        "publication.kazatc_error_estimation": (
            "relation.person.authored.kazatc_error_estimation",
            "relation.publication.kazatc_error_estimation.addresses_topic.insulation_parameters",
        ),
    }
    for claim_id in publication_ids:
        value = value_of(claims, claim_id)
        title = required_text(value, "title", claim_id)
        year = value.get("year")
        url = required_text(value, "url", claim_id)
        if not isinstance(year, int):
            raise ValueError(f"{claim_id}: invalid year")
        doi = value.get("doi")
        link_label = f"DOI {doi}" if isinstance(doi, str) else "Public article"
        ru_link_label = f"DOI {doi}" if isinstance(doi, str) else "Публичная статья"
        relation_ids = tuple(
            relation_id_for(relations, item) for item in publication_relations[claim_id]
        )
        blocks.append(
            Block(
                id=f"cv.publications.{claim_id.removeprefix('publication.')}",
                section_id="cv.section.publications",
                claim_ids=(claim_id,),
                relation_ids=relation_ids,
                ru_lines=(f"- **{year}.** {title}. [{ru_link_label}]({url})",),
                en_lines=(f"- **{year}.** {title}. [{link_label}]({url})",),
                exclusions=("coauthor_lists_omitted", "metrics_omitted"),
                notes=("selected_not_complete",),
            )
        )

    patent_specs = (
        (
            "patent.kz37923",
            "relation.person.inventor_on.kz37923",
            "active",
            "действует по состоянию на",
            "active as of",
        ),
        (
            "patent.kz35922",
            "relation.person.inventor_on.kz35922",
            "not_in_force",
            "не действует; проверено",
            "not in force; checked",
        ),
        (
            "patent.ea041128",
            "relation.person.inventor_on.ea041128",
            "not_in_force",
            "не действует; проверено",
            "not in force; checked",
        ),
    )
    for claim_id, inventor_relation, expected_status, ru_status, en_status in patent_specs:
        claim = claims[claim_id]
        value = value_of(claims, claim_id)
        if value.get("legal_status") != expected_status:
            raise ValueError(f"{claim_id}: unexpected legal status")
        number = required_text(value, "patent_number", claim_id)
        title = required_text(value, "title", claim_id)
        checked_at = required_text(value, "legal_status_checked_at", claim_id)
        publication_date = value.get("publication_date") or value.get(
            "patent_publication_date"
        )
        if not isinstance(publication_date, str):
            raise ValueError(f"{claim_id}: missing publication date")
        registry_url = source_url_for_claim(claim, sources, "official_patent_registry")
        blocks.append(
            Block(
                id=f"cv.patents.{claim_id.removeprefix('patent.')}",
                section_id="cv.section.patents",
                claim_ids=(claim_id,),
                relation_ids=(relation_id_for(relations, inventor_relation),),
                ru_lines=(
                    f"- **{number}.** {title}. Опубликован: {publication_date}; "
                    f"статус: {ru_status} {checked_at}. "
                    f"[Официальный реестр]({registry_url})",
                ),
                en_lines=(
                    f"- **{number}.** {title}. Published: {publication_date}; "
                    f"status: {en_status} {checked_at}. "
                    f"[Official register]({registry_url})",
                ),
                exclusions=(
                    "termination_reason_omitted",
                    "other_person_metadata_omitted",
                ),
                notes=("legal_status_is_point_in_time",),
            )
        )

    award_specs = (
        (
            "award.energy_saving_contribution",
            "relation.person.received_award.energy_saving_contribution",
            "«За вклад в энергосбережение» — отраслевая награда",
            "For contribution to energy saving — industry award",
        ),
        (
            "award.energy_ministry.distinguished_power_engineer",
            "relation.person.received_award.distinguished_power_engineer",
            "«Заслуженный энергетик» — Министерство энергетики Республики Казахстан",
            "Distinguished Power Engineer — Ministry of Energy of the Republic of Kazakhstan",
        ),
        (
            "award.energy_ministry.honoured_energy_worker",
            "relation.person.received_award.energy_ministry_honoured_energy_worker",
            "«Почётный энергетик» — Министерство энергетики Республики Казахстан",
            "Honoured Energy Worker — Ministry of Energy of the Republic of Kazakhstan",
        ),
        (
            "award.keea.honoured_energy_worker",
            "relation.person.received_award.keea_honoured_energy_worker",
            "«Почётный энергетик» — Казахстанская электроэнергетическая ассоциация",
            "Honoured Energy Worker — Kazakhstan Electric Energy Association",
        ),
    )
    for claim_id, relation_id, ru_text, en_text in award_specs:
        award = value_of(claims, claim_id)
        year = award.get("year")
        if not isinstance(year, int):
            raise ValueError(f"{claim_id}: invalid year")
        blocks.append(
            Block(
                id=f"cv.recognition.{claim_id.removeprefix('award.')}",
                section_id="cv.section.recognition",
                claim_ids=(claim_id,),
                relation_ids=(relation_id_for(relations, relation_id),),
                ru_lines=(f"- **{year}.** {ru_text}.",),
                en_lines=(f"- **{year}.** {en_text}.",),
                exclusions=("award_document_identifiers_omitted",),
                notes=("evidence_status_recorded_in_provenance",),
            )
        )

    project_specs = (
        (
            "project.ai_energy_auditor",
            "relation.person.develops.ai_energy_auditor",
            (
                "relation.project.ai_energy_auditor.addresses_topic.energy_audit",
                "relation.project.ai_energy_auditor.addresses_topic.ai_assisted_engineering",
            ),
            "**AI Energy Auditor** — в разработке. Черновой концепт "
            "AI-ассистированного энергоаудита с трассируемыми выводами; "
            "не запущенный продукт и не действующий AI-сервис.",
            "**AI Energy Auditor** — in development. Draft concept for "
            "AI-assisted energy audit with traceable reasoning; not a launched "
            "product or active AI service.",
        ),
        (
            "project.stm32_lab",
            "relation.person.develops.stm32_lab",
            (
                "relation.project.stm32_lab.addresses_topic.embedded_measurement_systems",
                "relation.project.stm32_lab.addresses_topic.measurement_diagnostics",
            ),
            "**STM32 / измерительная лаборатория** — в разработке. Захват "
            "аппаратных сигналов и измерительный стенд; подтверждённые показатели "
            "пока не заявляются.",
            "**STM32 / measurement lab** — in development. Hardware signal "
            "capture and a measurement test bench; no validated performance "
            "claim is made.",
        ),
    )
    for claim_id, develops_relation, topic_relations, ru_text, en_text in project_specs:
        project = value_of(claims, claim_id)
        if project.get("stage") != "in_development":
            raise ValueError(f"{claim_id}: project must remain in development")
        relation_ids = (relation_id_for(relations, develops_relation),) + tuple(
            relation_id_for(relations, item) for item in topic_relations
        )
        blocks.append(
            Block(
                id=f"cv.projects.{claim_id.removeprefix('project.')}",
                section_id="cv.section.projects",
                claim_ids=(claim_id,),
                relation_ids=relation_ids,
                ru_lines=(f"- {ru_text}",),
                en_lines=(f"- {en_text}",),
                notes=("roadmap_only_in_development_not_launched",),
            )
        )

    orcid = value_of(claims, "profile.orcid")
    scopus = value_of(claims, "profile.scopus")
    blocks.append(
        Block(
            id="cv.public_routes",
            section_id="cv.section.public_routes",
            claim_ids=("profile.orcid", "profile.scopus"),
            relation_ids=(),
            ru_lines=(
                "- Публичный профиль и профессиональный маршрут связи: "
                "https://ikurabayev.kz/",
                f"- ORCID: [{required_text(orcid, 'identifier', 'profile.orcid')}]"
                f"({required_text(orcid, 'url', 'profile.orcid')})",
                f"- Scopus Author ID: "
                f"[{required_text(scopus, 'identifier', 'profile.scopus')}]"
                f"({required_text(scopus, 'url', 'profile.scopus')})",
            ),
            en_lines=(
                "- Public profile and professional contact route: "
                "https://ikurabayev.kz/",
                f"- ORCID: [{required_text(orcid, 'identifier', 'profile.orcid')}]"
                f"({required_text(orcid, 'url', 'profile.orcid')})",
                f"- Scopus Author ID: "
                f"[{required_text(scopus, 'identifier', 'profile.scopus')}]"
                f"({required_text(scopus, 'url', 'profile.scopus')})",
            ),
            exclusions=("literal_email_omitted_use_public_site_route",),
            notes=("profile_links_do_not_imply_metrics_or_completeness",),
        )
    )

    return blocks, claims, relations


def ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def render_document(language: str, blocks: list[Block]) -> bytes:
    if language == "ru":
        lines = [
            "# Искандер Курабаев — публичное CV",
            "",
            "> Детерминированно сформированный публичный черновик. Это "
            "избранное, а не исчерпывающее CV; перед публикацией или добавлением "
            "скачиваемой версии требуется человеческая проверка.",
            "",
        ]
    else:
        lines = [
            "# Iskander Kurabayev — Public CV",
            "",
            "> Deterministically generated public draft. This is a selected, "
            "not exhaustive CV; human review is required before publication or "
            "adding a downloadable version.",
            "",
        ]

    current_section = ""
    for block in blocks:
        if block.section_id != current_section:
            current_section = block.section_id
            heading = SECTION_HEADINGS[language][current_section]
            lines.extend((f"## {heading}", ""))
        lines.extend(block.lines(language))
        lines.append("")

    if language == "ru":
        lines.extend(
            (
                "---",
                "",
                "Источник фактов и связей: публичные JSON-реестры репозитория. "
                "Хеши и происхождение блоков записаны в сопроводительном манифесте; "
                "они не являются юридической или цифровой подписью.",
                "",
            )
        )
    else:
        lines.extend(
            (
                "---",
                "",
                "Fact and relationship sources: the repository's public JSON "
                "registries. Block provenance and hashes are recorded in the "
                "companion manifest; they are not a legal or digital signature.",
                "",
            )
        )
    return "\n".join(lines).encode("utf-8")


def build_provenance(
    blocks: list[Block],
    claims: dict[str, dict[str, object]],
    relations: dict[str, dict[str, object]],
    registry_raw: bytes,
    graph_raw: bytes,
    review_date: str,
    ru_bytes: bytes,
    en_bytes: bytes,
) -> bytes:
    section_ids = ordered_unique([block.section_id for block in blocks])
    block_ids = [block.id for block in blocks]
    documents = [
        {
            "id": "cv.ru",
            "language": "ru",
            "path": DOCUMENT_PATHS["cv.ru"],
            "sha256": sha256_bytes(ru_bytes),
            "section_ids": section_ids,
            "block_ids": block_ids,
        },
        {
            "id": "cv.en",
            "language": "en",
            "path": DOCUMENT_PATHS["cv.en"],
            "sha256": sha256_bytes(en_bytes),
            "section_ids": section_ids,
            "block_ids": block_ids,
        },
    ]

    provenance_blocks: list[dict[str, object]] = []
    for block in blocks:
        statuses = {
            str(claims[claim_id]["status"]) for claim_id in block.claim_ids
        }
        statuses.update(
            str(relations[relation_id]["status"])
            for relation_id in block.relation_ids
        )
        ordered_statuses = sorted(
            statuses, key=lambda item: (STATUS_ORDER.get(item, 99), item)
        )
        provenance_blocks.append(
            {
                "id": block.id,
                "section_id": block.section_id,
                "document_ids": ["cv.ru", "cv.en"],
                "claim_ids": list(block.claim_ids),
                "relation_ids": list(block.relation_ids),
                "effective_evidence_statuses": ordered_statuses,
                "exclusions": list(block.exclusions),
                "notes": list(block.notes),
            }
        )

    manifest = {
        "schema_version": "0.1",
        "cv_version": "0.2",
        "source_registry_sha256": sha256_bytes(registry_raw),
        "source_graph_sha256": sha256_bytes(graph_raw),
        "source_review_date": review_date,
        "hash_scope_note": (
            "SHA-256 values cover exact input/output bytes for reproducibility; "
            "they are not a legal or digital signature."
        ),
        "documents": documents,
        "blocks": provenance_blocks,
    }
    return (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")


def build_outputs() -> dict[Path, bytes]:
    registry_raw, registry = read_json_bytes(REGISTRY_PATH)
    graph_raw, graph = read_json_bytes(GRAPH_PATH)
    if graph.get("subject") != registry.get("subject", {}).get("id"):
        raise ValueError("graph subject does not match registry subject")
    blocks, claims, relations = build_blocks(registry, graph)
    ru_bytes = render_document("ru", blocks)
    en_bytes = render_document("en", blocks)
    review_date = registry.get("generated_or_reviewed_at")
    if not isinstance(review_date, str):
        raise ValueError("registry review date must be a string")
    provenance_bytes = build_provenance(
        blocks,
        claims,
        relations,
        registry_raw,
        graph_raw,
        review_date,
        ru_bytes,
        en_bytes,
    )
    return {
        RU_PATH: ru_bytes,
        EN_PATH: en_bytes,
        PROVENANCE_PATH: provenance_bytes,
    }


def write_outputs(outputs: dict[Path, bytes]) -> int:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        print(f"wrote {path.relative_to(ROOT)} ({len(content)} bytes)")
    return 0


def check_outputs(outputs: dict[Path, bytes]) -> int:
    drift: list[str] = []
    for path, expected in outputs.items():
        try:
            actual = path.read_bytes()
        except OSError:
            drift.append(f"missing {path.relative_to(ROOT)}")
            continue
        if actual != expected:
            drift.append(f"drift in {path.relative_to(ROOT)}")
    if drift:
        print("Public CV generation check FAILED:", file=sys.stderr)
        for item in drift:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("Public CV generation check PASS: all three artifacts are byte-identical.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write generated artifacts")
    mode.add_argument("--check", action="store_true", help="check artifacts for drift")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"Public CV generation FAILED: {exc}", file=sys.stderr)
        return 1
    return write_outputs(outputs) if args.write else check_outputs(outputs)


if __name__ == "__main__":
    raise SystemExit(main())
