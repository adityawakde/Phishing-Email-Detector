document.addEventListener("DOMContentLoaded", function () {

    const button = document.getElementById("analyzeBtn");

    button.addEventListener("click", async function () {

        const text = document.getElementById("emailText").value;

        if (!text) {
            document.getElementById("result").innerHTML =
                "⚠️ Please enter email text";
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/analyze-hybrid", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            document.getElementById("result").innerHTML = `
                <p><b>Verdict:</b> ${data.final_verdict}</p>
                <p><b>Score:</b> ${data.hybrid_score}</p>
            `;

        } catch (error) {
            document.getElementById("result").innerHTML =
                "❌ API not reachable. Is FastAPI running?";
        }
    });

});