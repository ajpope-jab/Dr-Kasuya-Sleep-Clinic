import streamlit as st
import os
from PIL import Image

# Set webpage tab title and wide layout to fill the screen
st.set_page_config(
    page_title="The Sleep Clinic Resident",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom retro styling to make it feel like a video game console
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    /* Force dark-mode theme across the entire Streamlit App */
    .stApp {
        background-color: #0F172A !important;
        color: #F1F5F9 !important;
    }
    
    /* Make standard Streamlit sidebars match the dark console theme */
    div[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #475569;
    }
    
    /* Style Streamlit buttons to feel like arcade console switches */
    button[kind="secondary"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 2px solid #38BDF8 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    button[kind="secondary"]:hover {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        box-shadow: 0 0 12px #38BDF8 !important;
    }
    
    /* Style primary (CTA) buttons */
    button[kind="primary"] {
        background-color: #F43F5E !important;
        color: #FFFFFF !important;
        border: 2px solid #F43F5E !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    button[kind="primary"]:hover {
        background-color: #FFFFFF !important;
        color: #F43F5E !important;
        box-shadow: 0 0 12px #F43F5E !important;
    }

    /* Style disabled buttons to show they have been clicked */
    button:disabled {
        background-color: #1E293B !important;
        color: #64748B !important;
        border: 2px solid #334155 !important;
        opacity: 0.65;
    }

    /* Style the image container border */
    [data-testid="stImage"] img {
        border: 3px solid #3B82F6 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.35) !important;
    }

    .retro-font {
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Main retro game container */
    .game-header {
        background-color: #1E293B;
        border: 4px double #60A5FA;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #F8FAFC;
        margin-bottom: 20px;
    }
    
    .game-header h1 {
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        color: #60A5FA;
        margin: 0;
        font-size: 2.2rem;
    }
    
    .game-header p {
        font-family: 'Courier New', Courier, monospace;
        color: #94A3B8;
        margin: 5px 0 0 0;
    }

    /* Dr. Kasuya's Speech Box */
    .speech-box-kasuya {
        background-color: #064E3B;
        border: 3px solid #10B981;
        border-radius: 12px;
        padding: 18px;
        color: #ECFDF5;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    .speech-title-kasuya {
        font-weight: bold;
        color: #34D399;
        font-size: 1.1rem;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Patient Speech Box */
    .speech-box-patient {
        background-color: #500724;
        border: 3px solid #EC4899;
        border-radius: 12px;
        padding: 15px;
        color: #FDF2F8;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    .speech-title-patient {
        font-weight: bold;
        color: #F472B6;
        font-size: 1.0rem;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Feedback Speech Box */
    .feedback-box-correct {
        background-color: #14532D;
        border: 3px solid #22C55E;
        border-radius: 12px;
        padding: 18px;
        color: #F0FDF4;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
    }
    .feedback-box-incorrect {
        background-color: #7F1D1D;
        border: 3px solid #EF4444;
        border-radius: 12px;
        padding: 18px;
        color: #FEF2F2;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
    }

    /* Progress and Stats Box */
    .stats-box {
        background-color: #1E293B;
        border: 2px solid #475569;
        border-radius: 8px;
        padding: 10px 15px;
        color: #E2E8F0;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
    }

    /* Patient Presenting State Box */
    .case-box {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #475569;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Retro style custom list */
    .retro-hint-box {
        background-color: #1E3A8A;
        border-left: 5px solid #3B82F6;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 10px;
        color: #EFF6FF;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# Define the game database (with cleaned medical titles and clinical scenario focus)
CASES = {
    1: {
        "title": "PATIENT FILE 1: 45-YEAR-OLD MALE WITH SEVERE DAYTIME FATIGUE",
        "intro_desc": "This patient has checked into the examination room complaining of profound, constant exhaustion.",
        "dr_kasuya_intro": "Ah, our first patient of the day has checked into the examination room, Resident! Let's practice our clinical interviewing skills. I'll let you choose up to TWO questions to ask before you make your diagnosis. Keep an eye out for high-yield diagnostic triggers!",
        "questions": [
            "Ask about sleep behaviors and snoring patterns.",
            "Ask about morning symptoms and how they feel upon waking.",
            "Ask about daytime impairment and medical history.",
            "Ask about diet, activity, and weight."
        ],
        "answers": [
            "Patient: 'My wife says I snort and snore like an absolute chainsaw, Dr. Kasuya. She actually woke me up last night terrified because she said I stopped breathing entirely for at least 10 seconds! It happens multiple times a night.'",
            "Patient: 'I wake up with these pounding headaches almost every single morning, doctor. And honestly, I feel completely unrefreshed, like I haven't slept a wink, even if I was in bed for 9 hours.'",
            "Patient: 'I'm incredibly drowsy during the day—which is scary because I'm a long-haul truck driver. I've almost run off the road twice. Oh, and my primary doctor recently diagnosed me with hypertension (high blood pressure).'",
            "Patient: 'Well, I sit behind the wheel of my truck all day, so I don't get much exercise. I've gained about 35 pounds over the last year, mostly around my neck and midsection.'"
        ],
        "diagnoses": [
            "Insomnia Disorder",
            "Central Sleep Apnea (CSA)",
            "Obstructive Sleep Apnea (OSA)",
            "Hypersomnolence Disorder"
        ],
        "correct_answer": "Obstructive Sleep Apnea (OSA)",
        "explanation_correct": "Absolutely brilliant, Resident! This is indeed Obstructive Sleep Apnea (OSA). The loud irregular snoring, witnessed apnea events lasting 10+ seconds, daytime sleepiness, and morning headaches are classic signs. The physical airway collapses, causing oxygen drops and micro-arousals. Superb work!",
        "explanation_incorrect": "Close, but not quite! This is Obstructive Sleep Apnea (OSA). Witnessed apneas of 10+ seconds and morning headaches are clinical dead-ringers. This upper airway collapse leads to sleep fragmentation and secondary hypertension. Let's head to our next patient in the lobby—I'll buy you a soda if you get this next one!"
    },
    2: {
        "title": "PATIENT FILE 2: 60-YEAR-OLD VETERAN WITH NIGHTTIME AGITATION",
        "intro_desc": "The patient's wife has brought him into the clinic due to dangerous nighttime physical movements.",
        "dr_kasuya_intro": "Ah, Resident! Our next patient is waiting. He is experiencing very dramatic and physical nighttime events. Let's ask him some investigative questions to get to the bottom of this.",
        "questions": [
            "Ask about what physical movements occur during sleep.",
            "Ask about their state of mind and memory immediately upon awakening.",
            "Ask if they experience an uncomfortable 'creepy-crawly' or restless sensation in their legs in the evening.",
            "Ask when during the night these episodes typically happen."
        ],
        "answers": [
            "Patient: 'My wife is terrified because I keep thrashing, kicking, and screaming in my sleep. Last night, I dreamt I was wrestling a wild wolf, and I actually woke up on the floor because I threw myself out of bed to escape! I've accidentally bruised my wife a few times too.'",
            "Wife: 'If I shake him to wake him up during one of these wild fits, he wakes up instantly. He is immediately fully oriented, alert, and can tell me in vivid detail the violent nightmare he was just having. He doesn't look confused at all.'",
            "Patient: 'No, my legs feel perfectly fine when I'm awake or lying in bed. I only move them because I'm fighting for my life in those dreams!'",
            "Wife: 'These fits don't happen right when he falls asleep. They almost always happen in the second half or last third of the night, during the early morning hours.'"
        ],
        "diagnoses": [
            "Sleepwalking Disorder (NREM Parasomnia)",
            "REM Sleep Behavior Disorder (RBD)",
            "Sleep Seizure Disorder",
            "Restless Legs Syndrome (RLS)"
        ],
        "correct_answer": "REM Sleep Behavior Disorder (RBD)",
        "explanation_correct": "Magnificent! You nailed it. This is REM Sleep Behavior Disorder (RBD). Unlike NREM Sleepwalking (which happens in the first third of the night with blank stares and complete amnesia), RBD happens during REM sleep (second half). The brain loses its normal muscle atonia (paralysis), letting the patient physically act out vivid, violent dreams. Perfect diagnosis!",
        "explanation_incorrect": "Ah, a common pitfall! It's REM Sleep Behavior Disorder (RBD). A key differentiator from Sleepwalking is that RBD patients are instantly awake, fully oriented, and remember their dreams when woken. Sleepwalking occurs in NREM, where waking them up is extremely difficult and they have amnesia. Let's head to our final consultation of the morning!"
    },
    3: {
        "title": "PATIENT FILE 3: 72-YEAR-OLD FEMALE WITH SUDDEN-ONSET ENURESIS",
        "intro_desc": "Our final patient of the day is visiting our clinic. She is highly embarrassed about a distressing symptom that started suddenly last month.",
        "dr_kasuya_intro": "Don't worry, ma'am, we are here to help. Resident, this patient is dealing with a distressing symptom that started suddenly. Let's ask her some targeted questions about her medical history and lifestyle.",
        "questions": [
            "Ask about the exact nature of the symptom and when it occurs.",
            "Ask about any new medications or treatments she started recently.",
            "Ask about any daytime neurological symptoms, confusion, or memory issues.",
            "Ask if she experiences a creepy, crawling, or pulling feeling in her calves at night."
        ],
        "answers": [
            "Patient: 'It is so humiliating to talk about... but I have started wetting the bed. I wake up in the middle of the night or in the morning and my pajamas and sheets are completely soaked. This has never happened to me in my adult life until last month.'",
            "Patient: 'Well, my cardiologist recently diagnosed me with mild hypertension and started me on a water pill—I think it's called hydrochlorothiazide. He told me to take it at dinner, so I take it right before I get ready for bed.'",
            "Patient: 'My memory is sharp as a tack! No confusion, no balance issues, nothing like that during the day. Just this terrible bladder problem at night.'",
            "Patient: 'No crawling sensations in my legs. My ankles are a little swollen from my blood pressure, but my legs feel totally fine.'"
        ],
        "diagnoses": [
            "Primary Nocturnal Enuresis",
            "Secondary Nocturnal Enuresis (Drug-Induced)",
            "NREM Sleepwalking Disorder with enuresis",
            "Sleep Seizure Disorder"
        ],
        "correct_answer": "Secondary Nocturnal Enuresis (Drug-Induced)",
        "explanation_correct": "Sensational! That is exactly correct. This is Secondary Nocturnal Enuresis. In older adults, enuresis can be caused by a physiological decline in nighttime vasopressin (antidiuretic hormone) secretion. Most importantly, diuretics like hydrochlorothiazide are major drug-induced causes! Taking them near bedtime forces a major diuresis at night, leading directly to enuresis. Moving the medication to the morning will cure this!",
        "explanation_incorrect": "Ah, close! It is Secondary Nocturnal Enuresis. Primary enuresis means they've wet the bed their whole life without a 6-month dry period, which is rare in elderly patients without other causes. Here, she recently started hydrochlorothiazide (a diuretic) and took it right before bed! This drug forces urine production at night, causing secondary bedwetting. Moving her diuretic dose to the morning is the perfect treatment!"
    }
}

# Session state management
if "game_state" not in st.session_state:
    st.session_state.game_state = "intro" # intro, clinic, summary
if "case_num" not in st.session_state:
    st.session_state.case_num = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = [] # list of ints
if "phase" not in st.session_state:
    st.session_state.phase = "interview" # interview, diagnose, feedback
if "selected_diagnosis" not in st.session_state:
    st.session_state.selected_diagnosis = None

def reset_game():
    st.session_state.game_state = "intro"
    st.session_state.case_num = 1
    st.session_state.score = 0
    st.session_state.questions_asked = []
    st.session_state.phase = "interview"
    st.session_state.selected_diagnosis = None

def load_kasuya_avatar():
    if os.path.exists("dr_kasuya_retro_avatar.png"):
        return Image.open("dr_kasuya_retro_avatar.png")
    return None

avatar = load_kasuya_avatar()

# HEADER
st.markdown("""
<div class="game-header">
    <h1>THE SLEEP CLINIC RESIDENT</h1>
    <p>Clinical Practice Simulator with Dr. Kasuya</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with game control
with st.sidebar:
    st.header("🎛️ Game Controls")
    if st.button("🔄 Reset / Start Over"):
        reset_game()
        st.rerun()
    st.markdown("---")
    st.markdown("**Dr. Kasuya's Status:**")
    st.markdown("🥤 *Sipping a cold soda*")
    st.markdown("📖 *Reviewing Case Notes*")

# --- GAME SCREEN: INTRO ---
if st.session_state.game_state == "intro":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if avatar:
            st.image(avatar, use_container_width=True)
        else:
            st.subheader("👨‍⚕️ Dr. Kasuya")
            st.caption("[Missing Avatar Image]")
            
    with col2:
        st.markdown(f"""
        <div class="speech-box-kasuya">
            <div class="speech-title-kasuya">Dr. Kasuya</div>
            "Welcome to our sleep clinic, Resident! I'm Dr. Kasuya. <br><br>\
            Crack open a cold soda, and let's get ready for our morning rounds.<br><br>\
            We have three patients scheduled to come into the clinic today. Your job is to act as the lead clinical resident, interview them, and identify their correct primary sleep disorder.<br><br>\
            Let's see if you can get a perfect score! Ready to begin?"
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎮 Start Clinic Shift", type="primary", use_container_width=True):
            st.session_state.game_state = "clinic"
            st.session_state.case_num = 1
            st.session_state.phase = "interview"
            st.session_state.questions_asked = []
            st.session_state.selected_diagnosis = None
            st.rerun()

# --- GAME SCREEN: CLINIC MAIN (3-COLUMN COHESIVE LAYOUT) ---
elif st.session_state.game_state == "clinic":
    case = CASES[st.session_state.case_num]
    
    # Progress Display
    st.markdown(f"""
    <div class="stats-box">
        <span>📋 <b>Active Patient:</b> Patient {st.session_state.case_num}</span>
        <span>🏆 <b>Class Score:</b> {st.session_state.score} / {st.session_state.case_num - 1} Correct</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 3-COLUMN COHESIVE LAYOUT:
    # Column 1: Dr. Kasuya Portrait & Patient Chief Complaint
    # Column 2: Dr. Kasuya guidance and Question / Diagnosis Buttons
    # Column 3: The Patient Interview Q&A log (Side-by-side to prevent scrolling!)
    col_left, col_mid, col_right = st.columns([1.0, 1.3, 1.5])
    
    with col_left:
        if avatar:
            st.image(avatar, use_container_width=True)
        else:
            st.subheader("👨‍⚕️ Dr. Kasuya")
        
        # Presenting case container (using clean, single HTML block to prevent auto-close)
        st.markdown(f"""
        <div class="case-box">
            <span style="color:#94A3B8; font-size:0.85rem; font-weight:bold; letter-spacing:1px; display:block; margin-bottom:5px;">📋 CURRENT PATIENT STATE:</span>
            <span style="color:#F1F5F9; font-size:0.95rem; line-height:1.4;"><i>"{case['intro_desc']}"</i></span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_mid:
        # --- PHASE 1: INTERVIEWING ---
        if st.session_state.phase == "interview":
            st.markdown(f"""
            <div class="speech-box-kasuya">
                <div class="speech-title-kasuya">Dr. Kasuya</div>
                "{case['dr_kasuya_intro']}"
            </div>
            """, unsafe_allow_html=True)
            
            questions_remaining = 2 - len(st.session_state.questions_asked)
            st.markdown(f"💡 *Select up to **{questions_remaining}** trigger questions to ask:*")
            
            # Show interactive question buttons
            for i, q_text in enumerate(case['questions']):
                if i in st.session_state.questions_asked:
                    st.button(f"✅ Asked: {q_text}", key=f"q_{i}", disabled=True, use_container_width=True)
                else:
                    is_disabled = (questions_remaining <= 0)
                    if st.button(f"❓ Ask: {q_text}", key=f"q_{i}", disabled=is_disabled, use_container_width=True):
                        st.session_state.questions_asked.append(i)
                        st.rerun()

        # --- PHASE 2: DIAGNOSING ---
        elif st.session_state.phase == "diagnose":
            st.markdown(f"""
            <div class="speech-box-kasuya">
                <div class="speech-title-kasuya">Dr. Kasuya</div>
                "*Sips soda...* Excellent, we've gathered our two clinical clues! Based on the patient's symptoms, what is your official clinical diagnosis, Resident?"
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("🩺 **Submit your Diagnosis:**")
            
            # Diagnosis buttons - clean string replacement to ensure syntactically valid unique keys
            for diag_option in case['diagnoses']:
                diag_key = diag_option.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
                if st.button(diag_option, key=f"diag_{diag_key}", use_container_width=True):
                    st.session_state.selected_diagnosis = diag_option
                    st.session_state.phase = "feedback"
                    if diag_option == case['correct_answer']:
                        st.session_state.score += 1
                    st.rerun()

        # --- PHASE 3: FEEDBACK ---
        elif st.session_state.phase == "feedback":
            user_ans = st.session_state.selected_diagnosis
            correct_ans = case['correct_answer']
            is_correct = (user_ans == correct_ans)
            
            if is_correct:
                st.markdown(f"""
                <div class="feedback-box-correct">
                    <h4><b>🎉 CORRECT DIAGNOSIS!</b></h4>
                    <p style="margin:0;"><b>Your choice:</b> {user_ans}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="speech-box-kasuya">
                    <div class="speech-title-kasuya">Dr. Kasuya</div>
                    "{case['explanation_correct']}"
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-box-incorrect">
                    <h4><b>❌ DIAGNOSIS INCORRECT</b></h4>
                    <p style="margin:0;"><b>Your choice:</b> {user_ans}<br>\
                    <b>Correct diagnosis:</b> {correct_ans}</p>\
                </div>\
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="speech-box-kasuya">
                    <div class="speech-title-kasuya">Dr. Kasuya</div>
                    "{case['explanation_incorrect']}"
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("---")
            
            # Proceed buttons
            if st.session_state.case_num < 3:
                if st.button("⏩ Call Next Patient into Exam Room", type="primary", use_container_width=True):
                    st.session_state.case_num += 1
                    st.session_state.phase = "interview"
                    st.session_state.questions_asked = []
                    st.session_state.selected_diagnosis = None
                    st.rerun()
            else:
                if st.button("🏁 Finish Rounds & Get Evaluation", type="primary", use_container_width=True):
                    st.session_state.game_state = "summary"
                    st.rerun()

    with col_right:
        # Build the entire interview log HTML in Python first to guarantee no auto-closed div bugs
        log_html = f"""
        <div style="background-color:#0F172A; padding:20px; border-radius:12px; border:3px double #3B82F6; min-height:480px; font-family: 'Courier New', Courier, monospace;">
            <h3 style="color:#60A5FA; margin-top:0; font-family: 'Courier New', Courier, monospace;">📋 PATIENT INTERVIEW LOG</h3>
            <hr style="border-top: 1px solid #3B82F6; margin-bottom: 15px;">
        """
        
        if len(st.session_state.questions_asked) > 0:
            for q_idx in st.session_state.questions_asked:
                asked_q = case['questions'][q_idx]
                patient_ans = case['answers'][q_idx]
                
                log_html += f"""
                <div class="speech-box-patient">
                    <div class="speech-title-patient">Asked: "{asked_q}"</div>
                    "{patient_ans}"
                </div>
                """
        else:
            log_html += """
            <div style="text-align: center; color: #64748B; padding-top: 100px;">
                <p style="font-size: 1.2rem;">🚪 No questions asked yet.</p>
                <p>Click a trigger question in the middle column to interview the active patient!</p>
            </div>
            """
            
        log_html += "</div>"
        
        # Render the cohesive HTML block
        st.markdown(log_html, unsafe_allow_html=True)
        
        # Display the action button cleanly beneath the log container
        if len(st.session_state.questions_asked) >= 2 and st.session_state.phase == "interview":
            st.markdown("<div style='margin-top:15px;'>", unsafe_allow_html=True)
            if st.button("🚨 Move to Diagnosis", type="primary", use_container_width=True):
                st.session_state.phase = "diagnose"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- GAME SCREEN: SUMMARY / OUTRO ---
elif st.session_state.game_state == "summary":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if avatar:
            st.image(avatar, use_container_width=True)
        else:
            st.subheader("👨‍⚕️ Dr. Kasuya")
            
    with col2:
        st.markdown(f"""
        <div class="game-header" style="background-color: #0F172A; border-color: #10B981;">\
            <h2>SHIFT SUMMARY</h2>\
            <p style="color: #34D399; font-size: 1.2rem; font-weight: bold;">Final Score: {st.session_state.score} / 3 Correct Diagnoses</p>\
        </div>\
        """, unsafe_allow_html=True)
        
        # Determine feedback based on score
        if st.session_state.score == 3:
            rating = "⭐⭐⭐ Chief of Sleep Medicine"
            msg = "Flawless! Dr. Kasuya hands you a fresh, ice-cold soda. 'Absolutely spectacular work, Resident! You analyzed the clinical cues perfectly and didn't miss a single diagnosis. You're ready to run this clinic yourself! Your classmates have a fantastic physician in the making!'"
        elif st.session_state.score >= 1:
            rating = "⭐⭐ Sleep Clinic Fellow"
            msg = "Well done! Dr. Kasuya nods with satisfaction. 'Great clinical instincts, Resident. You correctly identified key sleep pathology markers. With a little more practice on those tricky differential diagnoses, you'll be an absolute expert! Here's a soda for a job well done!'"
        else:
            rating = "⭐ Med Student On Call"
            msg = "A great learning experience! Dr. Kasuya hands you a soda to boost your energy. 'The sleep world can be tricky, Resident. REM vs NREM parasomnias and secondary drug triggers take time to master. Keep reviewing your physiological pathways and you'll crush it next time!'"
            
        st.markdown(f"""
        <div class="speech-box-kasuya">
            <div class="speech-title-kasuya">Dr. Kasuya ({rating})</div>
            "{msg}"
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Play Again", use_container_width=True):
            reset_game()
            st.rerun()
