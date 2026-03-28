document.addEventListener('DOMContentLoaded', () => {

    // --- NAVIGATION ---
    const navBtns = document.querySelectorAll('.nav-btn');
    const viewPanels = document.querySelectorAll('.view-panel');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const targetView = btn.getAttribute('data-view');
            viewPanels.forEach(panel => {
                panel.classList.add('hidden');
                panel.classList.remove('active');
            });
            document.getElementById(targetView).classList.remove('hidden');
            document.getElementById(targetView).classList.add('active');
            
            // Trigger View Specific actions
            if(targetView === 'dashboard-view') loadDashboard();
        });
    });

    // --- PRACTICE SYSTEM: Question Generation ---
    const generateBtn = document.getElementById('generate-btn');
    const resultsContainer = document.getElementById('results-container');
    let currentQuestions = [];

    generateBtn.addEventListener('click', async () => {
        const topic = document.getElementById('topic').value || 'Data Structures and Algorithms';
        const difficulty = document.getElementById('difficulty').value;
        const language = document.getElementById('language').value;
        const orgText = generateBtn.innerHTML;

        generateBtn.innerHTML = '<span>⏳ Generating Coach Questions...</span>';
        generateBtn.classList.add('pulse-btn');
        resultsContainer.innerHTML = '';

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, difficulty, language })
            });

            const data = await response.json();

            if (!response.ok) {
                const detail = data.detail || JSON.stringify(data);
                resultsContainer.innerHTML = `<div class="error-box"><strong>⚠️ AI API Error:</strong><br/>${detail}</div>`;
                return;
            }
            
            currentQuestions = data.questions || [];
            
            if (currentQuestions.length === 0) {
                resultsContainer.innerHTML = '<p>No questions returned. Try another topic.</p>';
            } else {
                currentQuestions.forEach((q, index) => {
                    const card = document.createElement('div');
                    card.className = 'question-card glass-panel';
                    
                    const badgeClass = (q.difficulty || 'easy').toLowerCase();
                    const repeatedBadge = q.is_most_repeated ? '🔥 FAANG Favorite' : '';
                    
                    card.innerHTML = `
                        <div class="card-header">
                            <span class="badge ${badgeClass}">${q.difficulty}</span>
                            <span style="color:var(--error); font-size:0.8rem; font-weight:bold;">${repeatedBadge}</span>
                        </div>
                        <h3 style="margin-bottom: 0.8rem">${q.question}</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem">
                            Click to enter Practice Sandbox
                        </p>
                    `;
                    
                    card.addEventListener('click', () => openPracticeModal(q));
                    resultsContainer.appendChild(card);
                });
            }
        } catch (error) {
            resultsContainer.innerHTML = `<div class="error-box"><strong>⚠️ Network Error:</strong> Could not reach the backend. Make sure the server is running on port 8000.<br/><em>${error.message}</em></div>`;
        } finally {
            generateBtn.innerHTML = orgText;
            generateBtn.classList.remove('pulse-btn');
        }
    });

    // --- PRACTICE SYSTEM: Sandbox Modal ---
    const modal = document.getElementById('practice-modal');
    const closeBtn = document.querySelector('.close-modal');
    const modalTitle = document.getElementById('modal-q-title');
    const modalDesc = document.getElementById('modal-q-desc');
    const sandboxEditor = document.getElementById('sandbox-editor');
    const sandboxOutput = document.getElementById('sandbox-output');
    
    // Hint & Solution
    const hintBtn = document.getElementById('show-hint-btn');
    const hintBox = document.getElementById('modal-q-hint');
    const solBtn = document.getElementById('show-solution-btn');
    const solBox = document.getElementById('modal-q-solution');
    
    // Sandbox Controls
    const runBtn = document.getElementById('sandbox-run-btn');
    const analyzeBtn = document.getElementById('sandbox-analyze-btn');

    let currentActiveQuestion = null;

    function openPracticeModal(questionObj) {
        currentActiveQuestion = questionObj;
        modalTitle.textContent = "Problem: Challenge";
        modalDesc.innerHTML = `<h3 style="color:var(--text-primary); margin-bottom:1rem">${questionObj.question}</h3><br/><strong>AI Coach Suggestion:</strong><br/>${questionObj.logic_suggestion}`;
        
        hintBox.innerHTML = `<strong>Hint:</strong> ${questionObj.hint}`;
        hintBox.classList.add('hidden');
        
        const rawSolution = questionObj.solution;
        if (typeof marked !== 'undefined') {
             solBox.innerHTML = marked.parse(rawSolution);
        } else {
             solBox.innerHTML = `<pre style="white-space:pre-wrap;">${rawSolution}</pre>`;
        }
        
        solBox.classList.add('hidden');
        
        sandboxEditor.value = `def solve():\n    # Write logic for: ${questionObj.question}\n    pass\n\n# Test here\nprint("Running code...")`;
        sandboxOutput.textContent = "Ready... Click Output to run.";
        
        // Setup initial state
        analyzeBtn.classList.add('hidden'); 
        
        modal.classList.remove('hidden');
    }

    closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

    hintBtn.addEventListener('click', () => hintBox.classList.toggle('hidden'));
    solBtn.addEventListener('click', () => solBox.classList.toggle('hidden'));

    // --- CODE RUNNER & ANALYZER ---
    runBtn.addEventListener('click', async () => {
        const code = sandboxEditor.value;
        const language = "Python";
        
        sandboxOutput.style.color = "#e6edf3";
        sandboxOutput.textContent = "Executing code in Python Sandbox...";
        analyzeBtn.classList.add('hidden');
        
        try {
            const response = await fetch('/api/run_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, language })
            });
            const data = await response.json();
            
            if (data.error) {
                sandboxOutput.style.color = "#ff7b72";
                sandboxOutput.textContent = `[EXECUTION ERROR]\n\n${data.error}`;
                
                // Show AI Coach Why Did it Fail btn
                analyzeBtn.classList.remove('hidden');
            } else {
                sandboxOutput.style.color = "#7ee787";
                sandboxOutput.textContent = `[SUCCESS]\n\nOutput:\n${data.output}\n\nTime Complexity Estimate: ${data.complexity}`;
            }
            
        } catch (e) {
            sandboxOutput.textContent = "Sandbox cluster error (Backend down).";
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const code = sandboxEditor.value;
        const error = sandboxOutput.textContent;
        const troubleProblem = currentActiveQuestion ? currentActiveQuestion.question : "Unknown Code execution";
        
        const orgText = analyzeBtn.innerHTML;
        analyzeBtn.innerHTML = "Thinking...";
        analyzeBtn.disabled = true;
        
        try {
            const response = await fetch('/api/analyze_wrong_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, error, problem: troubleProblem })
            });
            const data = await response.json();
            
            sandboxOutput.style.color = "#79c0ff";
            sandboxOutput.textContent += `\n\n--- 🤖 AI COACH ANALYSIS ---\n${data.analysis}`;
            
        } catch(e) {
            sandboxOutput.textContent += "\n\nError connecting to Coach.";
        }
        
        analyzeBtn.innerHTML = orgText;
        analyzeBtn.disabled = false;
    });

    // --- VIEW: CODE EXPLAINER ---
    const explainBtn = document.getElementById('explain-btn');
    const explainOutput = document.getElementById('explanation-output');
    const explainCodeText = document.getElementById('explain-code-input');
    
    explainBtn.addEventListener('click', async () => {
        const code = explainCodeText.value;
        explainBtn.innerHTML = "Explaining Pipeline Running...";
        explainOutput.classList.remove('hidden');
        explainOutput.innerHTML = "Analyzing structure and dry running...";
        
        try {
            const response = await fetch('/api/explain_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            const data = await response.json();
            if (typeof marked !== 'undefined') {
                explainOutput.innerHTML = marked.parse(data.explanation);
            } else {
                explainOutput.textContent = data.explanation;
            }
            
        } catch(e) {
            explainOutput.innerHTML = "Error rendering explanation.";
        }
        explainBtn.innerHTML = "Explain Step-By-Step";
    });

    // --- VIEW: RESUME ANALYZER ---
    const resumeBtn = document.getElementById('analyze-resume-btn');
    const resumeOutput = document.getElementById('resume-feedback-output');
    const resumeInput = document.getElementById('resume-input');
    
    resumeBtn.addEventListener('click', async () => {
        const resume_text = resumeInput.value;
        resumeBtn.innerHTML = "Scanning Profile...";
        resumeOutput.classList.remove('hidden');
        resumeOutput.innerHTML = "Checking FAANG requirements against profile...";
        
        try {
            const response = await fetch('/api/resume_analyzer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_text })
            });
            const data = await response.json();
             if (typeof marked !== 'undefined') {
                resumeOutput.innerHTML = marked.parse(data.feedback);
            } else {
                resumeOutput.textContent = data.feedback;
            }
        } catch(e) {
            resumeOutput.innerHTML = "Error rendering profile score.";
        }
        resumeBtn.innerHTML = "Analyze Skills";
    });

    // --- VIEW: MOCK INTERVIEW ---
    const startMockBtn = document.getElementById('start-mock-btn');
    const timerSpan = document.getElementById('interview-timer');
    
    if (startMockBtn) {
        startMockBtn.addEventListener('click', async () => {
            const orgText = startMockBtn.innerHTML;
            startMockBtn.innerHTML = "Initializing Environment...";
            startMockBtn.disabled = true;

            try {
                // Fetch a hard question
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: "System Design or Arrays", difficulty: "Hard", language: "Python" })
                });
                
                if (!response.ok) throw new Error('Failed to connect');
                
                const data = await response.json();
                if (data.error) throw new Error(data.error);

                startMockBtn.innerHTML = "Simulator Running! Good Luck.";
                
                if (data.questions && data.questions.length > 0) {
                    openPracticeModal(data.questions[0]); // Open first hard question
                }
                
                // Start a visual timer countdown
                let minutes = 44;
                let seconds = 59;
                setInterval(() => {
                    seconds--;
                    if(seconds < 0) { seconds = 59; minutes--; }
                    timerSpan.textContent = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
                }, 1000);

            } catch (error) {
                // Fulfill user's request: "pls make sure this error is Error connecting to AI Coach API. Ensure backend is running and API key is set."
                startMockBtn.innerHTML = "Start Mock Interview";
                startMockBtn.disabled = false;
                alert("Error connecting to AI Coach API. Ensure backend is running and API key is set.");
            }
        });
    }

    // --- VIEW: DASHBOARD ---
    async function loadDashboard() {
        try {
            const response = await fetch('/api/progress');
            const data = await response.json();
            
            document.getElementById('stat-solved').textContent = data.problems_solved;
            document.getElementById('stat-acc').textContent = data.accuracy + "%";
            
            const tagsDiv = document.getElementById('stat-weak');
            tagsDiv.innerHTML = '';
            data.weak_topics.forEach(t => {
                const sp = document.createElement('span');
                sp.className = 'tag';
                sp.textContent = t.trim();
                tagsDiv.appendChild(sp);
            });
            
        } catch (e) {
            console.log("Could not load dashboard stats.");
        }
    }
});
