import streamlit as st
import os

# Set Streamlit page config
st.set_page_config(
    page_title="Khetri State Legal Archives (1910–1911)",
    page_icon="📜",
    layout="wide"
)

# App Header
st.title("📜 Khetri State Legal Archives (1910–1911 CE)")
st.caption("Interactive AI Chatbot & Historical Title Dossier • Rajputana Agency")

# Sidebar with context & quick prompts
with st.sidebar:
    st.header("About the Archive")
    st.info(
        """
        This system contains the complete court records, police inquests, sale deeds,
        and appellate decrees concerning the **Katra Haveli Dispute** in **Khetri State** (1910–1911 CE).
        """
    )
    
    st.subheader("Quick Questions")
    sample_queries = [
        "Give me a complete timeline of events from 1880 to 1911.",
        "Who was Bohra Kirparam and what was the mortgage amount?",
        "Why was Musammat Sundari's claim rejected by the court?",
        "Explain the family tree of Musammat Chanda and her sons.",
        "What is the significance of 'Sakin Kanund' (Kanodia)?",
        "Who was Ramzan Khan and what role did he play?"
    ]
    for q in sample_queries:
        if st.button(q, key=q):
            st.session_state["prefill_query"] = q

    api_key_input = st.text_input("Enter Gemini API Key (optional if set in env):", type="password")

# The Master Knowledge Base Context
KNOWLEDGE_BASE = """
MASTER LEGAL DOSSIER & ARCHIVES: KHETRI STATE (1910–1911 CE)

1. GEOGRAPHIC & ADMINISTRATIVE CONTEXT:
- State & Court: Princely State of Khetri (Rajputana Agency).
- Courts Involved: Kachehri Faujdari (Magistrate Ahmad Ali Faujdar Ahmadi), Kachehri Nizamat (District Judge Lukin), Mahakma Khas / Mahakma Suratiyari (High Sovereign Council under Raja Amar Singh Bahadur).
- Locality: Katra quarter (an enclosed commercial/bazaar settlement outside the town gate) within the overarching capital town and state of Qasba Khetri.
- Property: A two-story permanent masonry Haveli facing West, residential rooms, three-bay shops, North and South courtyard compounds (nohras), and an attached mature Neem tree.

2. CAST OF CHARACTERS & LINEAGE:
- Musammat Chanda: Matriarch of the Bhagat lineage. Mother to four sons:
  1. Shweik: Died childless.
  2. Laba: Died childless.
  3. Mohanlal / Pannalal Bhagat: Married to Musammat Bhoori (Barji); predeceased Baya.
  4. Baya Bhagat (Baya, son of Dulla Bhagat): Surviving brother who held undisputed possession until his death on 25 August 1910.
- Musammat Bhoori (also recorded as Bhooti / Barji): Daughter of Moga Bhagat, widow of Pannalal, and sole legally wedded surviving wife (aurat shadi-shuda) of Baya Bhagat. Held possession, funded last rites, and sold the property.
- Musammat Rajli: Secondary customary partner (aurat gardawasa / nata) from Peerwala/Nimau. Abandoned Baya during his illness, moved to her maternal village (Peehar), and was absent upon his death. Had no legal inheritance rights.
- Chunne: An ancestral brother who died childless around 1880–1890 (over 20–34 years before the trial) without leaving heirs or holding possession.
- Musammat Sundari: Widow of Chunne (Plaintiff/Appellant). Vacated the haveli decades earlier. In 1911, filed lawsuits to cancel the sale deed and extract money; her claims were dismissed with costs.
- Hanuman Mahajan (Kanodia): Bona fide purchaser. Native of Kanund / Kanod (Sakin Kanund, the ancestral origin of the Kanodia clan), resident of Khetri. Bought the property for Rs. 3,400 Imperial Chehra Shahi currency.
- Jagannath Mahajan: Elder/manager from the purchaser family community. Reported Baya's death to Katra Kotwali, helped inventory the property, and managed title affairs.
- Bohra Kirparam Bihari Lal: Prominent banker/creditor in Khetri. Held a possessory mortgage (Rahn-bil-Qaba) of Rs. 1,000 at Rs. 50/month occupancy rent. Fully redeemed upon sale.
- Ahmad Ali Faujdar Ahmadi: Officiating Faujdar who led the 1910 police inquest and confirmed Bhoori's heirship.
- Lukin: Judicial Superintendent / Presiding Judge across the Nizamat and Appellate Courts.
- Ramzan Khan: Defense Pleader (Vakil) who represented Musammat Bhoori and Hanuman Mahajan.

3. DOCUMENTARY CORPUS (7 DOCUMENTS):
- Doc 1: Deed of Absolute Sale (Bainama) dated 14 September 1910, registered 6 February 1911. Consideration Rs. 3,400. Page 4 Line 11 identifies buyer as 'Sakin Kanund' (Kanodia) resident of Khetri. Rs. 1,000 mortgage redeemed, Rs. 1,900 net cash paid to Bhoori.
- Doc 2: Nizamat Court Judgment (27 April 1911). Judge Lukin dismisses Sundari's suit (Na-Manzoor). Upholds sale deed to Hanuman Mahajan as valid (Ba-haal).
- Doc 3: Faujdari Court Inquest File No. 616/1910 (August–November 1910). Baya dies; Kotwali seals house; inquiry proves Bhoori performed rites and holds keys while Rajli was absent; keys handed to Bhoori as owner (malik-o-qabiz).
- Doc 4: Appellate Dossier & Underlying Mortgage. Contains notice of appeal to Mahakma Suratiyari (1911), grounds of appeal, and the registered 1900s mortgage deed with Bohra Kirparam for Rs. 1,000 with Rs. 50/month rent and discharge endorsement.
- Doc 5: Sovereign High Council (Mahakma Mualla) Affirmation (19 November 1910). Approves Faujdari findings, confirms Bhoori's title, and sanctions her legal power of sale (ikhtiyar-e-bai).
- Doc 6: Written Statement (Jawab-Dawa) of Musammat Bhoori (8 pages, 1911). Defends sale to Hanuman Mahajan for Rs. 3,400; cites 20+ years abandonment by Sundari, mortgage liquidation, and estoppel.
- Doc 7: Definitive High Appellate Decree (20 pages, 13 October 1911). High Sovereign Bench under Raja Amar Singh Bahadur dismisses Sundari's appeal (Kharij Shud); confirms registered sale deed to Hanuman Mahajan (Kanodia) as absolute, final, and irrevocable.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to the Khetri State Archives portal (1910–1911 CE). You can ask any question regarding the Katra haveli sale, the Bhagat lineage, the court decrees, or specific legal clauses across all seven documents."
        }
    ]

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle prefilled query from sidebar buttons
prefilled = st.session_state.pop("prefill_query", None)
user_prompt = st.chat_input("Ask a question about the Khetri legal archives...") or prefilled

if user_prompt:
    # Append user prompt
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Resolve API Key
    api_key = api_key_input or os.getenv("GEMINI_API_KEY")

    with st.chat_message("assistant"):
        if not api_key:
            response_text = (
                "⚠️ **API Key Missing**: Please provide your Gemini API key in the sidebar "
                "or set `GEMINI_API_KEY` as an environment variable to query the AI assistant."
            )
            st.markdown(response_text)
        else:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                
                # Combine system instructions and knowledge base
                sys_prompt = f"""
                You are a legal historian and expert archivist specializing in the 1910–1911 CE Khetri State judicial records.
                Answer user questions accurately, thoroughly, and citing exact documentary sources (Doc 1 through Doc 7), 
                characters, dates, and legal principles based on the following comprehensive knowledge base:
                
                {KNOWLEDGE_BASE}
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {"role": "user", "parts": [{"text": sys_prompt + "

User Question: " + user_prompt}]}
                    ]
                )
                response_text = response.text
                st.markdown(response_text)
            except Exception as e:
                response_text = f"❌ Error communicating with LLM API: {str(e)}"
                st.markdown(response_text)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response_text})
