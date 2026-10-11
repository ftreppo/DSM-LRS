# DSM-LRS Parent Prompt QUICK v0.2 — micro-validation feedback mode

**Task:** T042  
**Decision:** D026  
**Derived from:** verified T041 QUICK v0.1 and T035 FULL master; both preserved unchanged  
**Status:** prototype/tested with fictitious data — parent micro-validation candidate; not distributed/published  
**Languages:** IT + DE primary, EN supported  
**Scope:** generic/non-personalized parent resource; no Operational Profile or real student/private data.

This is a **DSM-LRS project resource**, not official DSM guidance, not a clinical tool, and not a substitute for school instructions.

v0.2 preserves the T041 adaptation guardrails and adds the D026 feedback mode. The exact language-neutral close-of-trial trigger is `DSM-LRS FEEDBACK V1`. It produces a minimized/pseudonymous report, not a transcript or school-material summary.

The directly copyable variants are archived separately as:
- `DSM_LRS_PARENT_PROMPT_QUICK_v0.2_IT.txt`
- `DSM_LRS_PARENT_PROMPT_QUICK_v0.2_DE.txt`
- `DSM_LRS_PARENT_PROMPT_QUICK_v0.2_EN.txt`

## IT

```text
PARENT PROMPT QUICK — DSM-LRS v0.2 — IT

RISORSA DI PROGETTO DSM-LRS — generica e non personalizzata. Non è una guida ufficiale DSM, non è uno strumento clinico e non sostituisce le indicazioni della scuola.

Aiutami ad adattare questo materiale scolastico per uso a casa.

PRIVACY: non inserire né usare nomi, diagnosi, PDP, certificazioni, referti, dati sanitari, scuola, docenti, contatti o altri identificatori. Se compaiono, fermati: non elaborarli né ripeterli e chiedi una versione anonimizzata.

Ti fornirò solo:
- Materia:
- Tipo di attività: STUDIO / COMPITI / ESERCIZIO / VERIFICA-VALUTAZIONE
- Obiettivo didattico:
- Materiale o consegna già anonimizzati:

REGOLE
1. Mantieni invariati obiettivo didattico, difficoltà, fatti, numeri, domande e contenuto. Applica il minimo intervento sufficiente: cambia solo ciò che serve per rendere il materiale più chiaro o leggibile, senza semplificarlo inutilmente.
2. Per STUDIO/COMPITI puoi chiarire struttura o termini, ma non svolgere il compito e non dare la risposta finale. Se serve aiuto sul metodo, usa domande guida o un esempio diverso che non risolva l'esercizio assegnato.
3. Per VERIFICA/VALUTAZIONE, se non è chiara la competenza valutata, chiedila prima di adattare. Non dare soluzioni, suggerimenti, answer cues o passaggi che facilitino la risposta. Non mettere in evidenza numeri, parole chiave o dati rilevanti con grassetto, colore, sottolineatura o posizione speciale. Non aggiungere aiuti che possano cambiare la competenza valutata.
4. Se una modifica rischia di cambiare ciò che viene valutato o la difficoltà, non applicarla: limita l'intervento a impaginazione/segmentazione neutra senza vantaggio informativo.

Rispondi con: VERSIONE ADATTATA; COSA HAI CAMBIATO; COSA HAI PRESERVATO. Per una verifica aggiungi anche: NOTA VALUTAZIONE — conferma che non hai aggiunto soluzioni, answer cues o enfasi su dati rilevanti.

FEEDBACK MICRO-VALIDAZIONE (facoltativo, solo se sto partecipando alla prova)
Usiamo preferibilmente una chat privata dedicata per tutto il periodo di prova; un Project privato è opzionale, non necessario e non va condiviso per la validazione. La stessa procedura vale per ogni genitore partecipante.

Quando scrivo esattamente: DSM-LRS FEEDBACK V1
passa alla modalità feedback e genera SOLO il report minimizzato tra i marker indicati sotto. Non trascrivere, citare o riassumere la chat o il materiale scolastico. Non inserire nomi, diagnosi/PDP/dati sanitari, scuola/docenti/contatti/identificatori, estratti del materiale, screenshot, link a chat/Project/account, account export o trascrizioni. Se queste informazioni sono comparse nella chat, omettile.

Genera un feedback_id breve e pseudonimo, per esempio P-7K3M, usando caratteri casuali e mai dati personali. Non inferire il mio giudizio: se una risposta soggettiva non è stata espressa chiaramente, scrivi unknown. Le osservazioni ricavate dalla chat devono essere solo grossolane, marcate "approximate — not measured telemetry"; se un conteggio o evento non è affidabile, scrivi unknown.

Usa esattamente questa struttura:
----- BEGIN DSM-LRS FEEDBACK V1 -----
feedback_id: [codice pseudonimo casuale]
language: IT
use_period: [durata approssimativa oppure unknown]
approx_uses: [numero/intervallo approssimativo oppure unknown]

PARENT FEEDBACK
1. clarity_1_5: [1-5 oppure unknown]
   clarity_comment: [cosa è chiaro/ambiguo oppure unknown]
2. ease_of_use_1_5: [1-5 oppure unknown]
   ease_comment: [facilità di copia/uso senza istruzioni tecniche oppure unknown]
3. usefulness_1_5: [1-5 oppure unknown]
   usefulness_comment: [utile/non utile senza abbassare difficoltà o svolgere il compito oppure unknown]
4. hesitation_or_doubts: [dove ho esitato o non sapevo cosa inserire oppure unknown]
5. possible_misuse_or_too_much_help: [soluzione, suggerimento troppo forte, vantaggio in verifica, oppure none/unknown]
6. would_use_again: [yes/no/maybe/unknown]
   home_use_context: [per quale uso domestico lo userei/non lo userei e breve motivo, oppure unknown]

CHAT OBSERVATIONS — approximate, not measured telemetry
privacy_stop_count_approx: [numero/intervallo oppure unknown]
clarification_requests_approx: [numero/intervallo oppure unknown]
homework_solution_blocking: [yes/no/unknown]
assessment_competence_or_no_cue_blocking: [yes/no/unknown]
recurring_usability_friction: [nota generica senza citazioni/materiale oppure unknown]

privacy_check: no names, diagnosis/PDP/health data, school/teacher/contact identifiers, school-material excerpts or chat quotations included.
PARENT REVIEW REQUIRED: controlla il report, elimina o modifica ciò che non vuoi condividere e invia manualmente SOLO il report rivisto, come testo/Markdown, via email individuale o WhatsApp diretto. Il canale di invio può identificare il mittente: il report è minimizzato/pseudonimo, non garantito anonimo.
----- END DSM-LRS FEEDBACK V1 -----
```

## DE

```text
PARENT PROMPT QUICK — DSM-LRS v0.2 — DE

DSM-LRS-PROJEKTRESSOURCE — generisch und nicht personalisiert. Keine offizielle DSM-Handreichung, kein klinisches Instrument und kein Ersatz für schulische Vorgaben.

Hilf mir, dieses Schulmaterial für die Nutzung zu Hause anzupassen.

DATENSCHUTZ: Verwende keine Namen, Diagnosen, PDP-/Förder-/Nachteilsausgleichsdokumente, Bescheinigungen, Befunde, Gesundheitsdaten, Schulnamen, Lehrernamen, Kontaktdaten oder andere Identifikatoren. Falls solche Angaben vorkommen, stoppe: verarbeite oder wiederhole sie nicht und bitte um eine anonymisierte Fassung.

Ich gebe nur an:
- Fach:
- Art der Aufgabe: LERNEN / HAUSAUFGABE / ÜBUNG / TEST-BEWERTUNG
- Lernziel:
- Bereits anonymisiertes Material oder Aufgabenstellung:

REGELN
1. Lernziel, Schwierigkeit, Fakten, Zahlen, Fragen und Inhalt bleiben erhalten. Wende die kleinstmögliche ausreichende Intervention an: ändere nur, was für bessere Klarheit oder Lesbarkeit nötig ist, ohne den Inhalt unnötig zu vereinfachen.
2. Bei LERNEN/HAUSAUFGABE darfst du Struktur oder Begriffe klären, aber die Aufgabe nicht lösen und keine Endantwort geben. Bei Hilfe zum Vorgehen nutze Leitfragen oder ein anderes Beispiel, das die gestellte Aufgabe nicht löst.
3. Bei TEST/BEWERTUNG: Wenn die geprüfte Kompetenz nicht klar ist, frage zuerst danach und passe noch nichts an. Gib keine Lösungen, Hinweise, Antwortsignale oder Zwischenschritte, die die Antwort erleichtern. Hebe antwortrelevante Zahlen, Schlüsselwörter oder Daten nicht durch Fettdruck, Farbe, Unterstreichung oder besondere Position hervor. Füge keine Hilfen hinzu, die die geprüfte Kompetenz verändern könnten.
4. Wenn eine Änderung die geprüfte Kompetenz oder Schwierigkeit verändern könnte, wende sie nicht an: beschränke dich auf neutrale Layout-/Segmentierungsänderungen ohne Informationsvorteil.

Antworte mit: ANGEPASSTE VERSION; WAS DU GEÄNDERT HAST; WAS DU ERHALTEN HAST. Bei einem Test ergänze: HINWEIS BEWERTUNG — bestätige, dass keine Lösung, Antwortsignale oder Hervorhebung antwortrelevanter Daten hinzugefügt wurden.

FEEDBACK-MIKROVALIDIERUNG (optional, nur wenn ich an der Erprobung teilnehme)
Nutze für den gesamten Testzeitraum vorzugsweise einen eigenen privaten Chat; ein privates Project ist optional, nicht erforderlich und wird für die Validierung nicht geteilt. Für alle teilnehmenden Eltern gilt dasselbe Verfahren.

Wenn ich exakt schreibe: DSM-LRS FEEDBACK V1
wechsle in den Feedback-Modus und erzeuge NUR den minimierten Bericht zwischen den unten angegebenen Markern. Transkribiere, zitiere oder fasse den Chat oder Schulmaterial nicht zusammen. Nenne keine Namen, Diagnosen/PDP-/Gesundheitsdaten, Schule/Lehrkräfte/Kontakte/Identifikatoren, Materialauszüge, Screenshots, Chat-/Project-/Account-Links, Account-Exporte oder Transkripte. Falls solche Informationen im Chat vorkamen, lasse sie weg.

Erzeuge eine kurze pseudonyme feedback_id, z. B. P-7K3M, aus zufälligen Zeichen und niemals aus persönlichen Daten. Leite mein Urteil nicht ab: Wenn eine subjektive Antwort nicht klar von mir geäußert wurde, schreibe unknown. Beobachtungen aus dem Chat dürfen nur grob sein und müssen als "approximate — not measured telemetry" gekennzeichnet werden; wenn eine Anzahl oder ein Ereignis nicht zuverlässig feststellbar ist, schreibe unknown.

Verwende exakt diese Struktur:
----- BEGIN DSM-LRS FEEDBACK V1 -----
feedback_id: [zufälliger pseudonymer Code]
language: DE
use_period: [ungefähre Dauer oder unknown]
approx_uses: [ungefähre Zahl/Spanne oder unknown]

PARENT FEEDBACK
1. clarity_1_5: [1-5 oder unknown]
   clarity_comment: [was klar/unklar ist oder unknown]
2. ease_of_use_1_5: [1-5 oder unknown]
   ease_comment: [Kopieren/Nutzung ohne technische Anleitung oder unknown]
3. usefulness_1_5: [1-5 oder unknown]
   usefulness_comment: [hilfreich/nicht hilfreich ohne Schwierigkeitsabsenkung oder Aufgabenlösung oder unknown]
4. hesitation_or_doubts: [wo ich unsicher war oder nicht wusste, was einzugeben ist, oder unknown]
5. possible_misuse_or_too_much_help: [Lösung, zu starker Hinweis, Bewertungsvorteil, oder none/unknown]
6. would_use_again: [yes/no/maybe/unknown]
   home_use_context: [wofür ich es zu Hause nutzen/nicht nutzen würde und kurzer Grund, oder unknown]

CHAT OBSERVATIONS — approximate, not measured telemetry
privacy_stop_count_approx: [Zahl/Spanne oder unknown]
clarification_requests_approx: [Zahl/Spanne oder unknown]
homework_solution_blocking: [yes/no/unknown]
assessment_competence_or_no_cue_blocking: [yes/no/unknown]
recurring_usability_friction: [generische Notiz ohne Zitate/Material oder unknown]

privacy_check: no names, diagnosis/PDP/health data, school/teacher/contact identifiers, school-material excerpts or chat quotations included.
PARENT REVIEW REQUIRED: Prüfe den Bericht, entferne oder ändere alles, was du nicht teilen möchtest, und sende manuell NUR den geprüften Bericht als Text/Markdown per Einzel-E-Mail oder Direktnachricht über WhatsApp. Der Übertragungskanal kann den Absender identifizieren: Der Bericht ist minimiert/pseudonymisiert, nicht garantiert anonym.
----- END DSM-LRS FEEDBACK V1 -----
```

## EN

```text
PARENT PROMPT QUICK — DSM-LRS v0.2 — EN

DSM-LRS PROJECT RESOURCE — generic and non-personalized. It is not official DSM guidance, not a clinical tool, and not a substitute for school instructions.

Help me adapt this school material for use at home.

PRIVACY: Do not use names, diagnoses, PDP/accommodation plans, certificates, clinical reports, health data, school names, teacher names, contact details, or other identifiers. If any appear, stop: do not process or repeat them and ask for an anonymized version.

I will provide only:
- Subject:
- Activity type: STUDY / HOMEWORK / PRACTICE / ASSESSMENT-GRADED TASK
- Learning objective:
- Material or instruction, already anonymized:

RULES
1. Preserve the learning objective, difficulty, facts, numbers, questions, and content. Apply the smallest sufficient intervention: change only what is needed for clearer access or readability, without unnecessary simplification.
2. For STUDY/HOMEWORK, you may clarify structure or terms, but do not complete the assignment or give the final answer. If method help is needed, use guiding questions or a different example that does not solve the assigned task.
3. For ASSESSMENT/GRADED TASKS, if the assessed competence is unclear, ask for it before adapting. Do not give solutions, hints, answer cues, or intermediate steps that make the answer easier. Do not highlight answer-relevant numbers, keywords, or data with bold, color, underlining, or special placement. Do not add aids that could change the assessed competence.
4. If a change could alter what is being assessed or the difficulty, do not apply it: limit the adaptation to neutral layout/segmentation that gives no informational advantage.

Reply with: ADAPTED VERSION; WHAT YOU CHANGED; WHAT YOU PRESERVED. For an assessment also add: ASSESSMENT NOTE — confirm that you added no solution, answer cues, or answer-relevant emphasis.

MICRO-VALIDATION FEEDBACK (optional, only if I am taking part in the trial)
Prefer one dedicated private chat for the whole trial period; a private Project is optional, not required, and must not be shared for the validation. The same procedure applies to every parent participant.

When I type exactly: DSM-LRS FEEDBACK V1
switch to feedback mode and generate ONLY the minimized report between the markers below. Do not transcribe, quote, or summarize the chat or school material. Do not include names, diagnoses/PDP/health data, school/teacher/contact identifiers, material excerpts, screenshots, chat/Project/account links, account exports, or transcripts. If such information appeared in the chat, omit it.

Generate a short pseudonymous feedback_id, for example P-7K3M, using arbitrary random characters and never personal data. Do not infer my judgment: if a subjective answer was not clearly expressed by me, write unknown. Observations inferred from the chat must be coarse only and labelled "approximate — not measured telemetry"; if a count or event cannot be determined reliably, write unknown.

Use exactly this structure:
----- BEGIN DSM-LRS FEEDBACK V1 -----
feedback_id: [random pseudonymous code]
language: EN
use_period: [approximate duration or unknown]
approx_uses: [approximate number/range or unknown]

PARENT FEEDBACK
1. clarity_1_5: [1-5 or unknown]
   clarity_comment: [what is clear/ambiguous or unknown]
2. ease_of_use_1_5: [1-5 or unknown]
   ease_comment: [ease of copying/using without technical instructions or unknown]
3. usefulness_1_5: [1-5 or unknown]
   usefulness_comment: [useful/not useful without lowering difficulty or doing the task, or unknown]
4. hesitation_or_doubts: [where I hesitated or did not know what to enter, or unknown]
5. possible_misuse_or_too_much_help: [solution, overly strong hint, assessment advantage, or none/unknown]
6. would_use_again: [yes/no/maybe/unknown]
   home_use_context: [what home use I would/would not use it for and short reason, or unknown]

CHAT OBSERVATIONS — approximate, not measured telemetry
privacy_stop_count_approx: [number/range or unknown]
clarification_requests_approx: [number/range or unknown]
homework_solution_blocking: [yes/no/unknown]
assessment_competence_or_no_cue_blocking: [yes/no/unknown]
recurring_usability_friction: [generic note without quotations/material or unknown]

privacy_check: no names, diagnosis/PDP/health data, school/teacher/contact identifiers, school-material excerpts or chat quotations included.
PARENT REVIEW REQUIRED: review the report, remove or change anything you do not want to share, and manually send ONLY the reviewed report as text/Markdown by one-to-one email or direct WhatsApp. The transport channel may identify the sender: the report is minimized/pseudonymous, not guaranteed anonymous.
----- END DSM-LRS FEEDBACK V1 -----
```

## Boundary
T035 FULL remains the verified reference master and T041 QUICK v0.1 remains prior verified evidence. v0.2 adds only the D026 micro-validation feedback flow. It grants no individualized accommodation, collects no raw chat by design, creates no automatic ingest, and does not authorize publication or external sending.
