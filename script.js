document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("analyzeBtn").addEventListener("click", uploadFile);
});

async function uploadFile() {
    const file = document.getElementById("fileInput").files[0];

    if (!file) {
        alert("Please upload a resume");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("result").innerHTML = "🔄 Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // Safe defaults
        const score = data.score || 0;
        const skills = data.skills || [];
        const keywords = data.keywords || [];
        const feedback = data.feedback || "No feedback";

        // Color logic
        let color = "#4CAF50";
        if (score < 50) color = "#e74c3c";
        else if (score < 80) color = "#f1c40f";

        // Format AI feedback (headings + bullets)
        const formattedFeedback = feedback
            .replace(/### (.*)/g, '<h4>$1</h4>')
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
            .replace(/- (.*)/g, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>');

        // UI
        document.getElementById("result").innerHTML = `
            <div class="score" style="color:${color}">
                Resume Score: ${score}/100
            </div>

            <div class="progress-bar">
                <div class="progress-fill" style="width:${score}%; background:${color}">
                    ${score}%
                </div>
            </div>

            <div class="section">
                <h3><i class="fa-solid fa-code"></i> Skills</h3>
                <div class="tags">
                    ${skills.map(s => `<span class="tag">${s}</span>`).join("")}
                </div>
            </div>

            <div class="section">
                <h3><i class="fa-solid fa-key"></i> Keywords</h3>
                <div class="tags">
                    ${keywords.map(k => `<span class="tag">${k}</span>`).join("")}
                </div>
            </div>

            <div class="feedback">
                <h3><i class="fa-solid fa-lightbulb"></i> AI Feedback</h3>
                ${formattedFeedback}
            </div>
        `;

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "❌ Error connecting to backend";
    }
}