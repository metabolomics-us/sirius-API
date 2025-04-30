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
                for (let i = 0; i < result.formulas.length; i++) {
                    outputText += result.formulas[i] + '\t\t' + result.sirius_scores[i] + '\n';
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
