
const analyzeBtn = document.getElementById("analyzeBtn");
const answerInput = document.getElementById("answer");
const statusText = document.getElementById("status");
const results = document.getElementById("results");

analyzeBtn.addEventListener("click", async () => {
    const answer = answerInput.value.trim();

    if (!answer) {
        statusText.textContent = "Please enter an AI-generated answer.";
        answerInput.focus();
        return;
    }

    analyzeBtn.disabled = true;
    statusText.textContent = "Analyzing claims...";
    results.replaceChildren();

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ answer })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed.");
        }

        const supportedCount = data.claims.filter(
            item => item.label === "Supported"
        ).length;

        const contradictedCount = data.claims.filter(
            item => item.label === "Contradicted"
        ).length;

        const uncertainCount = data.claims.filter(
            item => item.label === "Not Enough Evidence"
        ).length;

        // Summary
        const summary = document.createElement("div");
        summary.className = "result-summary";
        summary.textContent =
            `Total Claims: ${data.total_claims} | ` +
            `Demo Risk Score: ${data.risk_score}%`;

        results.appendChild(summary);

        // Statistics
        const stats = document.createElement("div");

        stats.style.cssText =
            "display:grid;" +
            "grid-template-columns:repeat(auto-fit,minmax(120px,1fr));" +
            "gap:10px;margin:16px 0;";

        const categories = [
            {
                title: "Supported",
                count: supportedCount,
                color: "#22c55e",
                background: "#14532d"
            },
            {
                title: "Contradicted",
                count: contradictedCount,
                color: "#f87171",
                background: "#7f1d1d"
            },
            {
                title: "Not Enough Evidence",
                count: uncertainCount,
                color: "#facc15",
                background: "#713f12"
            }
        ];

        categories.forEach(category => {
            const stat = document.createElement("div");

            stat.style.cssText =
                `background:${category.background};` +
                `border:1px solid ${category.color};` +
                "border-radius:10px;padding:14px;text-align:center;";

            const count = document.createElement("div");
            count.textContent = category.count;
            count.style.cssText =
                `font-size:26px;font-weight:700;color:${category.color};`;

            const title = document.createElement("div");
            title.textContent = category.title;
            title.style.cssText =
                "font-size:12px;margin-top:6px;color:#f8fafc;";

            stat.append(count, title);
            stats.appendChild(stat);
        });

        results.appendChild(stats);

        // Risk score bar
        const riskScore = Math.max(
            0,
            Math.min(100, Number(data.risk_score) || 0)
        );

        const riskColor =
            riskScore >= 70
                ? "#ef4444"
                : riskScore >= 35
                    ? "#eab308"
                    : "#22c55e";

        const barContainer = document.createElement("div");
        barContainer.style.cssText =
            "height:12px;background:#263653;" +
            "border-radius:99px;overflow:hidden;margin:12px 0 10px;";

        const bar = document.createElement("div");
        bar.style.cssText =
            `height:100%;width:${riskScore}%;` +
            `background:${riskColor};border-radius:99px;`;

        barContainer.appendChild(bar);
        results.appendChild(barContainer);

        const riskText = document.createElement("p");
        riskText.style.cssText =
            "font-size:13px;color:#cbd5e1;margin-bottom:14px;";

        const riskLevel =
            riskScore >= 70
                ? "High"
                : riskScore >= 35
                    ? "Medium"
                    : "Low";

        riskText.textContent =
            `Demo risk indicator: ${riskScore}% (${riskLevel})`;

        results.appendChild(riskText);

        // Limitations note
        const note = document.createElement("p");
        note.className = "result-note";
        note.textContent = data.note || "";
        results.appendChild(note);

        // Individual claim cards
        for (const item of data.claims) {
            const card = document.createElement("article");
            card.className = "claim-card";

            const claim = document.createElement("p");
            claim.className = "claim-text";
            claim.textContent = item.claim;

            const label = document.createElement("span");
            label.className = "claim-label";
            label.textContent = item.label;
            label.dataset.label = item.label;

            const explanation = document.createElement("p");
            explanation.textContent =
                "Explanation: " + item.explanation;

            const evidence = document.createElement("p");
            evidence.textContent =
                "Evidence: " +
                (item.evidence || "No matching evidence found.");

            const confidence = document.createElement("p");
            confidence.textContent =
                "Confidence: " + (item.confidence || "Unverified");

            card.append(
                claim,
                label,
                explanation,
                evidence,
                confidence
            );

            // Semantic similarity score
            if (typeof item.similarity === "number") {
                const similarity = document.createElement("p");

                const percentage = Math.round(
                    item.similarity * 100
                );

                similarity.textContent =
                    `Semantic Similarity: ${percentage}%`;

                similarity.style.cssText =
                    "margin-top:10px;color:#60a5fa;" +
                    "font-weight:600;font-size:14px;";

                card.appendChild(similarity);
            }

            results.appendChild(card);
        }

        statusText.textContent = "Analysis complete.";

    } catch (error) {
        results.textContent = "Unable to analyze the answer.";

        statusText.textContent =
            error.message === "Failed to fetch"
                ? "Cannot connect to the backend. Check that the API server is running."
                : error.message;

    } finally {
        analyzeBtn.disabled = false;
    }
});
