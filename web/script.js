document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("input-form");
    const output = document.getElementById("output");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        output.innerHTML = "Fetching results<span class='loading-dots'></span>";
        const msms = document.getElementById("msms-input").value.trim();
        const pcm = document.getElementById("pcm-input").value.trim();

        try {
            const response = await fetch("/formulas", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    msms_str: msms,
                    pcm_str: pcm
                })
            });

            const result = await response.json();

            if (response.ok) {
                let outputText = '';
                if (result.sirius_scores.length == 0 || result.formulas.length == 0) {
                    outputText = "Sirius could not find any matching formulas.";
                } else {
                    outputText += "Formula".padEnd(25) + "Score\n"; // header
                    for (let i = 0; i < result.formulas.length; i++) {
                        const formula = result.formulas[i].padEnd(25);
                        const score = result.sirius_scores[i];
                        outputText += formula + score + '\n';
                    }
                }
                output.textContent = outputText;
            } else {
                output.textContent = "Error: " + (result.detail || JSON.stringify(result));
            }
        } catch (error) {
            output.textContent = "Network or server error occurred.";
            console.error(error);
        }
    });
});
